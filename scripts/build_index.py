#!/usr/bin/env python3
"""Regenerate the catalog from each experiment/resource metadata.yml.

Single source of truth: experiments/<slug>/metadata.yml and
resources/<slug>/metadata.yml. This script rewrites, between START/END marker
comments:
  - the catalog + resources tables in README.md, and
  - the experiment + resource cards on the landing page (index.html).

Edit a metadata.yml (or add a new folder), then run:

    python scripts/build_index.py

Nothing on the landing page or in the README table is hand-maintained.
Pure standard library, no dependencies.
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
LANDING = os.path.join(ROOT, "index.html")
GH = "https://github.com/ReplicationBench/RB/tree/master"

STATUS_EMOJI = {
    "replicated": "✅ replicated",
    "refuted": "❌ refuted",
    "inconclusive": "\U0001f7e8 inconclusive",
    "untested": "⬜ untested",
}
STATUS_GLYPH = {"replicated": "✅", "refuted": "❌", "inconclusive": "\U0001f7e8", "untested": "⬜"}


def parse_metadata(path):
    """Minimal reader for the flat schema (key: value, tags: [..])."""
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
            if val and val[0] not in "\"'[" and " #" in val:
                val = val.split(" #", 1)[0].strip()
            if len(val) >= 2 and val[0] in "\"'" and val[-1] == val[0]:
                val = val[1:-1]
            data[key] = val
    return data


def load_dir(subdir):
    items = []
    for meta in sorted(glob.glob(os.path.join(ROOT, subdir, "*", "metadata.yml"))):
        folder = os.path.basename(os.path.dirname(meta))
        m = parse_metadata(meta)
        items.append((m.get("slug") or folder, m))
    items.sort(key=lambda t: (t[1].get("title") or t[0]).lower())
    return items


def money(low, high):
    def fmt(v):
        v = (str(v) if v is not None else "0").strip() or "0"
        try:
            return f"{int(v):,}"
        except ValueError:
            return v
    low, high = fmt(low), fmt(high)
    return f"${low}" if low == high else f"${low}-${high}"


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------- README markdown tables ----------------
def exp_row(slug, m):
    cost = money(m.get("cost_usd_low"), m.get("cost_usd_high"))
    status = STATUS_EMOJI.get((m.get("status") or "untested").strip(), m.get("status") or "")
    return (f"| [{m.get('title') or slug}](./experiments/{slug}/) | {m.get('question') or ''} "
            f"| {cost} | {m.get('difficulty') or ''} | {m.get('safety_level') or ''} | {status} |")


def res_row(slug, m):
    rel = m.get("related_experiment") or ""
    supports = f"[{rel}](./experiments/{rel}/)" if rel else "—"
    return (f"| [{m.get('title') or slug}](./resources/{slug}/) | {m.get('description') or ''} "
            f"| {supports} | {m.get('contributor') or '—'} |")


# ---------------- landing HTML cards ----------------
def _btns(primary_label, primary_href, ghost_label, ghost_href, has_page):
    if has_page:
        return (f'      <a class="btn solid" href="{primary_href}">{primary_label}</a>\n'
                f'      <a class="btn ghost" href="{ghost_href}">{ghost_label}</a>')
    # no hosted page yet: the GitHub link becomes the primary action
    return f'      <a class="btn solid" href="{ghost_href}">{ghost_label}</a>'


def exp_card(slug, m):
    status = (m.get("status") or "untested").strip()
    glyph = STATUS_GLYPH.get(status, "⬜")
    page = m.get("page") or ""
    btns = _btns("Open the experiment &rarr;", f"experiments/{slug}/{page}",
                 "Details, data &amp; BOM", f"{GH}/experiments/{slug}", bool(page))
    return (
        '  <div class="card">\n'
        f'    <h3>{esc(m.get("title") or slug)}</h3>\n'
        f'    <p class="claim">Question: <em>&ldquo;{esc(m.get("question") or "")}&rdquo;</em></p>\n'
        '    <div class="badges">\n'
        f'      <span class="badge"><b>{esc(money(m.get("cost_usd_low"), m.get("cost_usd_high")))}</b></span>\n'
        f'      <span class="badge">difficulty: <b>{esc(m.get("difficulty") or "")}</b></span>\n'
        f'      <span class="badge">safety: <b>{esc(m.get("safety_level") or "")}</b></span>\n'
        f'      <span class="badge status-{status}">{glyph} <b>{status}</b></span>\n'
        '    </div>\n'
        f'    <div class="btns">\n{btns}\n    </div>\n'
        '  </div>'
    )


def res_card(slug, m, exp_titles):
    rel = m.get("related_experiment") or ""
    supports = exp_titles.get(rel, rel)
    page = m.get("page") or ""
    btns = _btns("Open &rarr;", f"resources/{slug}/{page}",
                 "Source on GitHub", f"{GH}/resources/{slug}", bool(page))
    supports_badge = (f'\n      <span class="badge">supports: <b>{esc(supports)}</b></span>'
                      if supports else "")
    return (
        '  <div class="card">\n'
        f'    <h3>{esc(m.get("title") or slug)}</h3>\n'
        f'    <p class="claim">{esc(m.get("description") or "")}</p>\n'
        '    <div class="badges">\n'
        '      <span class="badge">type: <b>resource</b></span>'
        f'{supports_badge}\n'
        '    </div>\n'
        f'    <div class="btns">\n{btns}\n    </div>\n'
        '  </div>'
    )


def replace_block(text, start, end, block):
    if start not in text or end not in text:
        return text, False
    out = re.sub(re.escape(start) + r".*?" + re.escape(end),
                 lambda _: start + "\n" + block + "\n" + end, text, flags=re.S)
    return out, True


def main():
    exps = load_dir("experiments")
    ress = load_dir("resources")
    exp_titles = {slug: (m.get("title") or slug) for slug, m in exps}

    # ---- README tables ----
    exp_header = ("| Experiment | Question tested | Cost | Difficulty | Safety | Status |\n"
                  "|---|---|---|---|---|---|")
    res_header = "| Resource | What it is | Supports | Contributor |\n|---|---|---|---|"
    exp_table = "\n".join([exp_header] + [exp_row(s, m) for s, m in exps]) if exps else exp_header
    res_table = "\n".join([res_header] + [res_row(s, m) for s, m in ress]) if ress else res_header

    with open(README, encoding="utf-8") as f:
        text = f.read()
    text, ok = replace_block(text, "<!-- CATALOG:START -->", "<!-- CATALOG:END -->", exp_table)
    if not ok:
        sys.exit("ERROR: CATALOG markers not found in README.md")
    text, _ = replace_block(text, "<!-- RESOURCES:START -->", "<!-- RESOURCES:END -->", res_table)
    with open(README, "w", encoding="utf-8") as f:
        f.write(text)

    # ---- landing cards ----
    if os.path.exists(LANDING):
        exp_cards = "\n".join(exp_card(s, m) for s, m in exps)
        res_cards = "\n".join(res_card(s, m, exp_titles) for s, m in ress)
        with open(LANDING, encoding="utf-8") as f:
            html = f.read()
        html, _ = replace_block(html, "<!-- EXPERIMENT-CARDS:START -->", "<!-- EXPERIMENT-CARDS:END -->", exp_cards)
        html, _ = replace_block(html, "<!-- RESOURCE-CARDS:START -->", "<!-- RESOURCE-CARDS:END -->", res_cards)
        with open(LANDING, "w", encoding="utf-8") as f:
            f.write(html)

    print(f"Generated {len(exps)} experiment(s) + {len(ress)} resource(s) into README + landing.")


if __name__ == "__main__":
    main()
