# AHQandA (Eleventy + Tailwind)
To Preview on localhost:7986
npm run dev

Static renderer for daily `yyyymmdd.json` summary files stored in `content/`.

files are saved in /content
by running extract_summary.ps1 for each file to process

## Dev

- Install: `npm install`
- Run dev server: `npm run dev`
- Preview: `http://localhost:7986/`
- Build: `npm run build`

## Search index
- using Microsoft Docfind https://github.com/microsoft/docfind?tab=readme-ov-file#creating-a-search-index
- Generate/update `search/documents.json` from `content/*.json`: `python search/build_documents.py`
- A GitHub Action is included to auto-update this file on every push: `.github/workflows/update-documents-json.yml`

Output is written to `_site/`.

## CI/CD
Workflow: update-documents-json.yml
Triggers on push (but ignores pushes that only change documents.json to prevent an infinite loop)
Uses GITHUB_TOKEN with contents: write to push the update commit