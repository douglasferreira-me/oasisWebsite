#!/usr/bin/env python3
"""Small production-output validator for the OASIS Hugo site."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_ROUTES = [
    "index.html",
    "about/index.html",
    "team/index.html",
    "studies/index.html",
    "media/index.html",
    "projects/index.html",
    "contact/index.html",
    "en/index.html",
    "en/about/index.html",
    "es/index.html",
    "es/about/index.html",
    "admin/index.html",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-dir", type=Path, required=True)
    args = parser.parse_args()
    root = args.site_dir.resolve()
    errors: list[str] = []

    for route in REQUIRED_ROUTES:
        if not (root / route).is_file():
            errors.append(f"missing route: {route}")

    html_files = list(root.rglob("*.html"))
    for path in html_files:
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(root)
        if relative.parts[0] == "admin":
            if "noindex" not in text:
                errors.append(f"admin page is indexable: {relative}")
            continue
        if path.name == "404.html" or "http-equiv=refresh" in text or 'http-equiv="refresh"' in text:
            continue
        markers = {
            "canonical": r"rel=(?:\"canonical\"|canonical)",
            "hreflang": r"hreflang=",
            "structured data": r"application/ld\+json",
        }
        for label, pattern in markers.items():
            if not re.search(pattern, text):
                errors.append(f"{relative} missing {label}")
        for block in re.findall(
            r"<script\s+type=(?:\"application/ld\+json\"|application/ld\+json)>(.*?)</script>",
            text,
            re.DOTALL,
        ):
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                errors.append(f"{relative} contains invalid structured data: {exc}")
        if len(re.findall(r"<h1(?:\s|>)", text)) != 1:
            errors.append(f"{relative} must contain exactly one h1")
        for image_tag in re.findall(r"<img\b[^>]*>", text):
            if not re.search(r"\balt(?:=(?:\"[^\"]*\"|'[^']*'|[^\s>]+)|(?=\s|>))", image_tag):
                errors.append(f"{relative} contains an image without alt text")
        for target in re.findall(r"(?:href|src)=(?:\"([^\"]+)\"|'([^']+)'|([^\s>]+))", text):
            url = next(part for part in target if part)
            if not url.startswith("/oasisWebsite/"):
                continue
            local = url.removeprefix("/oasisWebsite/").split("?", 1)[0].split("#", 1)[0]
            candidate = root / local
            if url.endswith("/"):
                candidate /= "index.html"
            if not candidate.exists():
                errors.append(f"{relative} links to missing local target: {url}")
        if re.search(r'(href|src)="/(?!oasisWebsite/)', text):
            errors.append(f"{relative} contains a root-absolute asset or link")

    sitemap = root / "sitemap.xml"
    robots = root / "robots.txt"
    if not sitemap.is_file():
        errors.append("missing sitemap.xml")
    elif "/admin/" in sitemap.read_text(encoding="utf-8"):
        errors.append("admin appears in sitemap.xml")
    if not robots.is_file() or "Disallow: /oasisWebsite/admin/" not in robots.read_text(encoding="utf-8"):
        errors.append("robots.txt does not exclude admin")

    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(html_files)} HTML files and {len(REQUIRED_ROUTES)} required routes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
