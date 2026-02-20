# AHQandA (Eleventy + Tailwind)

Static renderer for daily `yyyymmdd.json` summary files stored in `content/`.

## Dev

- Install: `npm install`
- Run dev server: `npm run dev`
- Preview: `http://localhost:7986/`
- Build: `npm run build`

## Search index

- Generate/update `search/documents.json` from `content/*.json`: `python search/build_documents.py`
- A GitHub Action is included to auto-update this file on every push: `.github/workflows/update-documents-json.yml`

Output is written to `_site/`.
