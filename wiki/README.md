# Software Engineer Atlas

Wiki + grafo de conceitos em cima dos markdowns deste repositório.

## Rodar local

```bash
cd wiki
npm install
npm run dev
```

Abre em `http://localhost:5173/software-engineer-txt/`.

## Build

```bash
cd wiki
npm run build
npm run preview
```

O script `ingest` varre os `.md` na raiz do repo (pastas = categorias) e gera `src/generated/notes.json`.

## Wiki links

Nos seus markdowns, use:

```md
Veja também [[JWT]] e [[OAuth 2.0]].
```

O título precisa bater com o `# Título` (ou título derivado) da nota alvo. Links relativos `.md` também viram arestas no grafo.

## GitHub Pages

1. Settings → Pages → Source: **GitHub Actions**
2. Push em `main` dispara `.github/workflows/wiki-pages.yml`
3. Site: `https://saulofilho.github.io/software-engineer-txt/`

Edição de conteúdo continua no Git (link “Editar no GitHub” em cada nota).
