# OASIS — UFRJ

Site institucional multilíngue do **Observatório de Algoritmos e Sistemas de Informação com Impacto Social**, construído em Hugo a partir do TailBliss 1.2.0 e publicado no GitHub Pages.

## Desenvolvimento local

Requisitos:

- Hugo Extended 0.164.0 ou superior;
- Node.js 22 ou superior;
- pnpm 11.10.0.

```bash
pnpm install --frozen-lockfile
pnpm run dev:watch
```

O site será servido normalmente em `http://localhost:1313/oasisWebsite/`. Para gerar a versão de produção:

```bash
pnpm run build
python3 scripts/validate_site.py --site-dir public
```

## Conteúdo e idiomas

Português é o idioma padrão. Traduções usam arquivos separados:

- `pagina.pt.md` — português;
- `pagina.en.md` — inglês;
- `pagina.es.md` — espanhol.

As páginas fixas ficam em `content/`. Integrantes, estudos, registros de mídia e projetos ficam em suas coleções `*-items`.

## Sveltia CMS

Depois do deploy, o painel estará em:

`https://douglasferreira-me.github.io/oasisWebsite/admin/`

1. Abra o painel e selecione **Sign In with Token**.
2. Use o link oferecido pelo Sveltia para criar um token de acesso do GitHub com permissão de escrita no repositório `douglasferreira-me/oasisWebsite`.
3. Cole o token no painel. O token fica somente no armazenamento local do navegador e nunca deve ser salvo no repositório.
4. Edite as três traduções antes de publicar uma alteração.

O CMS controla Home, Sobre, Equipe, Estudos, Na mídia, Projetos, Contato e as coleções repetíveis. Uploads são versionados em `static/uploads/`.

## Publicação

Commits na branch `main` acionam `.github/workflows/pages.yml`. O workflow compila CSS com Vite, gera o site com Hugo Extended 0.164.0, valida a saída e publica o diretório `public/` no GitHub Pages.

## Créditos e licença

O site usa a identidade visual fornecida pelo OASIS e foi baseado no tema [TailBliss](https://github.com/nusserstudios/tailbliss), licenciado sob Apache 2.0. Consulte [LICENSE](LICENSE).
