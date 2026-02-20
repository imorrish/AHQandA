#!/usr/bin/env python3
"""Builds/updates search/documents.json from content/*.json.

- title: taken from filename stem (e.g. 20260220)
- body: taken from summary_data.brief_summary
- href: /summary/<yyyymmdd>/

This script is intended to be idempotent: re-running updates summary entries.
Non-summary entries already present in documents.json are preserved.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

DATE_FILE_RE = re.compile(r"^(\d{8})\.json$", re.IGNORECASE)
SUMMARY_HREF_RE = re.compile(r"^/summary/(\d{8})/?$")


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _safe_get_brief_summary(content_json: dict[str, Any]) -> str:
    summary_data = content_json.get("summary_data")
    if isinstance(summary_data, dict):
        brief = summary_data.get("brief_summary")
        if isinstance(brief, str):
            return brief
    return ""


def _is_summary_doc(doc: dict[str, Any]) -> bool:
    href = doc.get("href")
    return isinstance(href, str) and SUMMARY_HREF_RE.match(href) is not None


def _load_existing_documents(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    data = _read_json(path)
    if data is None:
        return []

    if not isinstance(data, list):
        raise ValueError(f"{path} must be a JSON array")

    docs: list[dict[str, Any]] = []
    for i, item in enumerate(data):
        if isinstance(item, dict):
            docs.append(item)
        else:
            raise ValueError(f"{path} item {i} must be an object")

    return docs


def build_documents(content_dir: Path, output_path: Path) -> tuple[int, int]:
    existing_docs = _load_existing_documents(output_path)

    non_summary_docs = [d for d in existing_docs if not _is_summary_doc(d)]

    generated: list[dict[str, str]] = []
    for file_path in sorted(content_dir.glob("*.json"), key=lambda p: p.name, reverse=True):
        m = DATE_FILE_RE.match(file_path.name)
        if not m:
            continue

        date = m.group(1)
        title = date
        href = f"/summary/{date}/"

        try:
            content_json = _read_json(file_path)
        except Exception as e:  # noqa: BLE001
            body = f"(Error reading {file_path.name}: {e})"
        else:
            if isinstance(content_json, dict):
                body = _safe_get_brief_summary(content_json)
            else:
                body = ""

        generated.append(
            {
                "title": title,
                "category": "summary",
                "href": href,
                "body": body,
            }
        )

    merged = non_summary_docs + generated
    _write_json(output_path, merged)

    return (len(generated), len(non_summary_docs))


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate/append search/documents.json from content JSON files")

    default_root = Path(__file__).resolve().parents[1]
    parser.add_argument(
        "--content-dir",
        default=str(default_root / "content"),
        help="Directory containing yyyymmdd.json files (default: ./content)",
    )
    parser.add_argument(
        "--output",
        default=str(default_root / "search" / "documents.json"),
        help="Output documents.json path (default: ./search/documents.json)",
    )

    args = parser.parse_args()
    content_dir = Path(args.content_dir)
    output_path = Path(args.output)

    if not content_dir.exists():
        raise SystemExit(f"Content directory does not exist: {content_dir}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    generated_count, preserved_count = build_documents(content_dir, output_path)
    print(f"Wrote {output_path} ({generated_count} summaries, preserved {preserved_count} existing docs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
