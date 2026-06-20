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


def make_resource_row(slug, m):
    title = m.get("title") or slug
    desc = m.get("description") or ""
    rel = m.get("related_experiment") or ""
    supports = f"[{rel}](./experiments/{rel}/)" if rel else "—"
    contributor = m.get("contributor") or "—"
    return f"| [{title}](./resources/{slug}/) | {desc} | {supports} | {contributor} |"


def build_table(subdir, header, row_fn):
    rows = []
    for meta in sorted(glob.glob(os.path.join(ROOT, subdir, "*", "metadata.yml"))):
        folder = os.path.basename(os.path.dirname(meta))
        m = parse_metadata(meta)
        rows.append(((m.get("title") or folder).lower(), row_fn(m.get("slug") or folder, m)))
    rows.sort()
    return ("\n".join([header] + [r for _, r in rows]) if rows else header), len(rows)


def replace_block(text, start, end, block):
    if start not in text or end not in text:
        return text, False
    out = re.sub(
        re.escape(start) + r".*?" + re.escape(end),
        lambda _: start + "\n" + block + "\n" + end,
        text,
        flags=re.S,
    )
    return out, True


def main():
    exp_header = (
        "| Experiment | Claim tested | Cost | Difficulty | Safety | Status |\n"
        "|---|---|---|---|---|---|"
    )
    res_header = (
        "| Resource | What it is | Supports | Contributor |\n"
        "|---|---|---|---|"
    )
    exp_table, n_exp = build_table("experiments", exp_header, make_row)
    res_table, n_res = build_table("resources", res_header, make_resource_row)

    with open(README, encoding="utf-8") as f:
        text = f.read()
    text, ok = replace_block(text, "<!-- CATALOG:START -->", "<!-- CATALOG:END -->", exp_table)
    if not ok:
        sys.exit("ERROR: CATALOG:START / CATALOG:END markers not found in README.md")
    text, _ = replace_block(text, "<!-- RESOURCES:START -->", "<!-- RESOURCES:END -->", res_table)

    with open(README, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Catalog updated: {n_exp} experiment(s), {n_res} resource(s).")


if __name__ == "__main__":
    main()
