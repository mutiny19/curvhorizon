#!/usr/bin/env python3
"""Regenerate the catalog table in README.md from each experiment's metadata.yml.

Pure standard library, no dependencies. Reads experiments/*/metadata.yml and
rewrites the table between the <!-- CATALOG:START --> and <!-- CATALOG:END -->
markers in README.md. Don't edit the table by hand; edit the metadata and re-run:

    python scripts/build_index.py
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")

STATUS_EMOJI = {
    "replicated": "✅ replicated",
    "refuted": "❌ refuted",
    "inconclusive": "\U0001f7e8 inconclusive",
    "untested": "⬜ untested",
}


def parse_metadata(path):
    """Minimal reader for the flat experiment schema (key: value, tags: [..])."""
    data = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            m = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
            if not m:
                continue
            key, val = m.group(1), m.group(2).strip()
            # strip an inline comment when the value is not quoted/bracketed
            if val and val[0] not in "\"'[" and " #" in val:
                val = val.split(" #", 1)[0].strip()
            if len(val) >= 2 and val[0] in "\"'" and val[-1] == val[0]:
                val = val[1:-1]
            data[key] = val
    return data


def money(low, high):
    low = (low or "0").strip() or "0"
    high = (high or "0").strip() or "0"
    return f"${low}" if low == high else f"${low}-${high}"


def make_row(slug, m):
    title = m.get("title") or slug
    claim = m.get("claim") or ""
    cost = money(m.get("cost_usd_low"), m.get("cost_usd_high"))
    diff = m.get("difficulty") or ""
    safety = m.get("safety_level") or ""
    status_key = (m.get("status") or "untested").strip()
    status = STATUS_EMOJI.get(status_key, status_key)
    return f"| [{title}](./experiments/{slug}/) | {claim} | {cost} | {diff} | {safety} | {status} |"


def main():
    rows = []
    for meta in sorted(glob.glob(os.path.join(ROOT, "experiments", "*", "metadata.yml"))):
        folder = os.path.basename(os.path.dirname(meta))
        m = parse_metadata(meta)
        slug = m.get("slug") or folder
        rows.append(((m.get("title") or folder).lower(), make_row(slug, m)))
    rows.sort()

    header = (
        "| Experiment | Claim tested | Cost | Difficulty | Safety | Status |\n"
        "|---|---|---|---|---|---|"
    )
    table = "\n".join([header] + [r for _, r in rows]) if rows else header

    with open(README, encoding="utf-8") as f:
        text = f.read()
    if "<!-- CATALOG:START -->" not in text or "<!-- CATALOG:END -->" not in text:
        sys.exit("ERROR: CATALOG:START / CATALOG:END markers not found in README.md")

    new = re.sub(
        r"(<!-- CATALOG:START -->).*?(<!-- CATALOG:END -->)",
        lambda mm: mm.group(1) + "\n" + table + "\n" + mm.group(2),
        text,
        flags=re.S,
    )
    with open(README, "w", encoding="utf-8") as f:
        f.write(new)
    print(f"Catalog updated: {len(rows)} experiment(s).")


if __name__ == "__main__":
    main()
