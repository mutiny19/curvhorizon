# Contributing to ReplicationBench

There are two ways to take part: **report a run** (you went out and measured
something) and **shape the design** (you have a control, a correction, or an
argument). Both are below. Everything here keeps to one rule: the experiment
presupposes nothing. Flat is a result, curved is a result, and a run that does
not resolve is a result. None is the goal.

> Heads up: all of these need a free GitHub account. The issue forms are guided
> web forms — you do **not** need to know git to file one.

---

## Report a run

1. Open **[Report a run](https://github.com/ReplicationBench/RB/issues/new?template=submit-run.yml)**
   and fill the form: site, distance, instruments, conditions, how you measured
   refraction, the outcome, and a link to the raw readings.
2. **Publish the raw data**, not just the summary — a number nobody can re-check
   can't go in the log. Small CSVs and photos can be attached to the issue; large
   logs go in a pull request to `data/`, or an external archive (e.g. a Zenodo or
   OSF deposit, which also gives the dataset a citable DOI) linked from the issue.
3. A maintainer (or you, by pull request) then commits the run:

   ```
   experiments/laser-experiment/
     data/2026-06-19_yourhandle/      # raw logs, photos, instrument exports
     results/                          # plots, narrative, and the replication-log row
   ```

   The run is added as a row in the experiment's replication log, and the
   experiment `status` (`untested → replicated | refuted | inconclusive`) is only
   ever moved to match the rows in that log — never anyone's expectations.

A refuted or inconclusive run is a successful contribution. Report it the same way.

---

## Shape the design

| You have… | Use |
|---|---|
| An open-ended question, an argument, a site report, a "what about…" | **[Discussions](https://github.com/ReplicationBench/RB/discussions)** |
| A concrete control, correction, or clarification | **[Propose a change](https://github.com/ReplicationBench/RB/issues/new?template=propose-change.yml)** |
| An actual edit to the protocol or data | **A pull request** |

The design is meant to be built *with* the people who expect the opposite result.
The sharpest objection is a gift — it's usually a control the design didn't have
yet. Proposals that close a way the result could later be explained away are the
most valuable thing you can file.

---

## Editing files directly (pull requests)

- The protocol is a single hand-maintained page:
  `experiments/laser-experiment/laser-experiment.html`. Edit it directly.
- The **landing page and the README catalog are generated** — don't hand-edit the
  cards or tables. Edit the experiment's `metadata.yml` (or add a new
  `experiments/<slug>/` or `resources/<slug>/` folder from `_template/`) and run:

  ```
  python scripts/build_index.py
  ```

  That rewrites the cards in `index.html` and the tables in `README.md` from the
  metadata. The build is pure standard library — no dependencies.

---

## Licensing

By contributing you agree your work is licensed under the repository's terms:
documentation and data under **CC BY-SA 4.0**, code under **AGPL-3.0** (see
[`LICENSE`](LICENSE) and [`COMMERCIAL-LICENSE.md`](COMMERCIAL-LICENSE.md)). You
keep the credit; the measurement stays open for anyone to re-check.

---

## For maintainers: enabling Discussions

Discussions has to be turned on once, by hand:

1. Repo **Settings → General → Features → tick *Discussions***.
2. Suggested categories (replace the defaults):
   - **Methodology** — how the experiment should work; refraction, controls, geometry.
   - **Results & runs** — discussion of reported runs and their data.
   - **Site & equipment** — venues, builds, cheaper/available parts.
   - **Q&A** — questions (answerable format).
   - **General** — everything else.
3. Pin a welcome post:

   > **We don't argue. We measure.** This is the room for the open part —
   > questions, objections, site reports, and ideas that aren't a concrete change
   > yet. When a suggestion becomes specific, turn it into a
   > [design proposal](https://github.com/ReplicationBench/RB/issues/new?template=propose-change.yml);
   > when you've gone out and measured, file a
   > [run report](https://github.com/ReplicationBench/RB/issues/new?template=submit-run.yml).
   > Flat, curved, and inconclusive are all welcome here, and all treated the same.

The `result` and `design` issue labels referenced by the forms are created the
first time you apply them (or add them under **Issues → Labels**).
