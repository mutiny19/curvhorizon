# The Genealogy of Knowledge

An interactive, zoomable sunburst tracing how the branches of philosophy became
the modern disciplines: from Philosophy at the core, out through five traditions,
down to specialized fields five levels deep.

**Live:** https://replicationbench.github.io/RB/resources/knowledge-genealogy/

## What it does

- **Click any wedge** to zoom into its lineage; **click the center** to zoom back out.
- **Hover any field** to light up its path back to Philosophy.
- **Dashed edges** mark interdisciplinary fields with more than one parent
  (e.g. biochemistry, cognitive science, computational linguistics). Hovering one
  draws a link across the core to its second parent, the relationship a strict
  tree cannot show.
- **Tooltips** carry each field's era, a short description, and where it emerged from.

## On accuracy

This is a genealogy, not a strict taxonomy, and a clean tree oversimplifies real
intellectual history. The in-app "On accuracy" panel documents the deliberate
simplifications: medicine predating biology, economics descending from moral
philosophy, the dual roots of psychology and neuroscience in physiology, and the
handling of interdisciplinary fields. Corrections via issues and PRs are welcome.

## Technical notes

- Single static HTML page. No build step. The hierarchy is embedded as JSON.
- Rendering by [D3](https://d3js.org/) v7.8.5, vendored locally in `vendor/`.
- Type set in Fraunces and IBM Plex, self-hosted in `fonts/` (both families are
  SIL Open Font License). No CDN requests, no analytics; the page phones home
  to nobody.

## License

Covered by this repository's license (see the repo root LICENSE). Fonts carry
their own SIL OFL terms.
