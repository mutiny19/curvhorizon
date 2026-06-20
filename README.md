# ReplicationBench — Experiments

**We don't argue. We measure.**

This is the experiment catalog for ReplicationBench: a monorepo of accessible,
amateur-completable kits for replicating contested, counterintuitive, or famous
science experiments. Every experiment is built to one standard, costs almost
always **under $2,000**, and ships with the raw data from real runs — so you can
check the result yourself instead of taking anyone's word for it.

**Not a GitHub user?** The [landing page](https://replicationbench.github.io/RB/)
links straight to each experiment's interactive pages.

This repo is one half of a hybrid setup. The org profile, contribution guide,
issue/PR templates, and the [scope & safety policy](https://github.com/ReplicationBench/.github/blob/main/SCOPE.md)
live in the companion `.github` repo. The experiments live here.

---

## What belongs here

- **Replications anyone can check** — Earth's curvature, Earth's rotation, the
  gravitational constant, cosmic-ray muons, wave–particle duality.
- **Adversarial tests of popular claims**, blinded where perception matters —
  dowsing, homeopathy, "free energy" devices.

Each entry documents *method and data*, stated neutrally. The conclusion is left
to the reader and the measurement, not asserted by the maintainers. What's
explicitly **out of scope** (bio agents, energetic chemistry, radiation sources,
unisolated lethal voltage) is defined in the scope policy and enforced at review.

---

## Repository layout

```
experiments/<slug>/      one experiment, following the standard template
_template/               copy this to start a new experiment
scripts/build_index.py   regenerates the catalog table in this README
LICENSE                  GNU AGPL-3.0
COMMERCIAL-LICENSE.md    commercial / dual-license terms
.gitattributes           routes raw data + binaries through Git LFS
```

Every `experiments/<slug>/` folder has the same shape:

```
<slug>/
  README.md          the experiment, following the fixed schema
  metadata.yml       machine-readable record that feeds the catalog
  hardware/BOM.csv    priced bill of materials
  code/              firmware / control / DSP (omit if unused)
  analysis/          scripts that turn raw data into a result (optional)
  data/              raw runs, one subfolder per run: YYYY-MM-DD_contributor/
  results/           plots, photos, the narrative interpretation
```

---

## The standard every experiment meets

This consistency is the whole point — it's what makes the repo a catalog instead
of a pile of folders. Each experiment README hits the same beats:

1. **The claim**, stated neutrally, linked to its strongest version.
2. **Hypothesis & decision rule** — what measurement, beyond what threshold,
   decides it, *declared before building*. This is what separates a test from a vibe.
3. **Bill of materials**, fully priced, with a "checked on" date.
4. **Build** and **Procedure** — reproducible, blinded where human perception
   is involved.
5. **Reading the result** — the math, and a pointer to the analysis code.
6. **Results & replication log** — the recorded run, plus a running table of
   independent replications.
7. **Safety** — mandatory, even when the honest answer is "no special hazards."
8. **Sources** — cite, don't assert.

---

## The catalog is generated, not hand-written

The table below is produced from each experiment's `metadata.yml` by
`scripts/build_index.py` (pure standard library, no dependencies). Don't edit the
table by hand — edit the metadata and re-run the script.

<!-- CATALOG:START -->
| Experiment | Claim tested | Cost | Difficulty | Safety | Status |
|---|---|---|---|---|---|
| [Earth Curvature by Laser Over Water](./experiments/earth-curvature-laser/) | The Earth's surface is flat over long line-of-sight distances. | $50-$300 | medium | low | ⬜ untested |
<!-- CATALOG:END -->

`status` is one of `replicated` · `refuted` · `inconclusive` · `untested`, and it
must be supported by the data in `data/`, not by anyone's expectations.

### Metadata schema (`metadata.yml`)

```yaml
slug: ""                 # folder name, hyphenated
title: ""
claim: ""                # neutral one-liner
cost_usd_low: 0
cost_usd_high: 0
difficulty: ""           # easy | medium | hard
time: ""                 # e.g. "one weekend"
safety_level: ""         # none | low | medium | high
status: untested         # replicated | refuted | inconclusive | untested
tags: []                 # e.g. [astronomy, relativity, pseudoscience-test]
```

---

## Adding an experiment

```bash
cp -r _template experiments/your-slug
# fill in README.md, metadata.yml, hardware/BOM.csv
# add code/, analysis/, and at least one raw run under data/
python scripts/build_index.py    # refresh the catalog table
```

Open a **New Experiment Proposal** issue and get a 👍 before you build — it
catches duplicates and scope problems early. Full workflow and the review bar are
in the `.github` repo's `CONTRIBUTING.md`.

### Reporting a replication

The most valuable contribution here is running an existing experiment. Add your
run under that experiment's `data/`, namespaced by contributor and date, note the
outcome in its `results/README.md` log, and open a **Replication Report** issue. A
refuted or inconclusive result is a successful contribution — that's the project
working.

---

## Data & Git LFS

Raw data is a first-class artifact, not an afterthought. Common data and binary
formats (`.parquet`, `.h5`, `.wav`, `.mp4`, `.stl`, `.step`, and CSVs under
`data/`) are routed through Git LFS via `.gitattributes` so repository history
stays light. Run `git lfs install` once before your first push. If a single
experiment's dataset grows large enough to strain the monorepo, it can be split
into its own repo later — the structure here is designed to make that painless.

---

## License

Dual-licensed. By default this software is released under the **GNU Affero
General Public License v3.0** (see [`LICENSE`](LICENSE)) — free to use, study,
modify, and redistribute, with the AGPL's network-copyleft obligation (a hosted,
modified version must publish its source). A separate **commercial license** is
available for uses the AGPL does not permit; see
[`COMMERCIAL-LICENSE.md`](COMMERCIAL-LICENSE.md).
