# <Experiment title>

> One-sentence neutral summary of what this experiment measures.

Status: **untested** · Cost: **$0–$0** · Difficulty: **easy/medium/hard** · Time: **one weekend** · Safety: **none/low/medium/high**

<!-- Keep every section below. Delete a section only if you replace it with a
     clearly-labelled reason. State method and data; do not assert conclusions. -->

## 1. The claim

State the claim neutrally, in its strongest form, and link to where its
proponents make it. Do not strawman it.

## 2. Hypothesis & decision rule

**Declared before building.** What quantity will you measure, and beyond what
threshold does it decide the claim one way or the other? Name the predicted
value under each hypothesis, the instrument resolution, and what counts as a
clean run. A test without a pre-declared decision rule is a vibe, not a test.

- Prediction if the claim holds: …
- Prediction if it does not: …
- Decision rule: …
- What makes a run **inconclusive** rather than forced to a verdict: …

## 3. Bill of materials

Fully priced, with a "checked on" date. See [`hardware/BOM.csv`](hardware/BOM.csv).
Note any item a builder is likely to already own, and cheaper substitutions.

## 4. Build

How the apparatus goes together. Photos/diagrams in `results/`. Note calibration
and any controls that must pass before a real run counts.

## 5. Procedure

Step by step, reproducible by a stranger. **Blind the measurement wherever human
perception can bias it.** Say exactly what gets recorded and at what rate.

## 6. Reading the result

The math that turns the raw reading into a verdict, with the exact formula and a
pointer to [`analysis/`](analysis/) if code is involved. State the error budget.

## 7. Results & replication log

The recorded run(s) live in [`data/`](data/) (one subfolder per run,
`YYYY-MM-DD_contributor/`), with plots and the narrative interpretation in
[`results/`](results/). Keep a running table of independent replications there.
A **refuted** or **inconclusive** result is a successful contribution.

## 8. Safety

Mandatory — even if the honest answer is "no special hazards." List real hazards,
required PPE, and anything that would put a run out of scope (see the scope
policy in the org's `.github` repo).

## Sources

Cite, don't assert. Link the strongest version of every claim and every method.
