# Water-Surface Shape by Laser

> Level a laser over open water, never aim it at a target, and measure whether the
> water holds a constant height under the beam (flat) or falls away from it
> (curved) — with refraction measured on the night, not assumed.

**Status:** ⬜ untested · **Cost:** $50–$300 · **Difficulty:** medium · **Time:** one weekend · **Safety:** low

**Interactive references**
- ▶ **[The field protocol](laser-experiment.html)** — full build, setup diagrams, procedure, refraction handling, equipment options, and a live run simulator embedded in it.
- ▶ **[Curvature & horizon simulator](../../resources/surface-shape-simulator/simulator.html)** — to-scale model of curvature, horizon dip, hidden height, and refraction.

*(Browsing on GitHub? Those are HTML pages — open them via the
[live site](https://replicationbench.github.io/RB/experiments/laser-experiment/laser-experiment.html).)*

---

## 1. The claim

In its strongest form, the flat position is that **a gravity-levelled line of
sight stays a constant height above open water out to the horizon and beyond** —
that over miles of calm water the surface does not fall away, so a level laser
should keep the same clearance the whole way. The experiment is built to test
that neutrally; it presupposes neither outcome.

## 2. Hypothesis & decision rule

*Declared before building, and signed by both sides before any number is taken.*

A laser is levelled to local gravity where it stands, locked on both axes, and
**never aimed at the far end**. A drone (or, in the entry build, three
equal-height markers) reports the height of the surface relative to that level
line as a function of distance.

- **If the surface is flat:** the height under the beam is constant — the water
  stays parallel to the level line. The implied curvature is zero.
- **If the surface is a sphere of radius R:** the water falls below the level
  line by **R(1 − cos θ)** with θ = d/R — the exact, trigonometric drop, which
  over these distances equals the familiar **d²/2R** to better than a part in a
  thousand. At 3 mi ≈ 6 ft; at 5 mi ≈ 17 ft.
- **Decision rule:** fit the measured height-vs-distance profile to a level line
  (flat) and to a parabola (sphere). The radius the run *implies*,
  R = d²/(2·drop), is an **output of the readings**, not an input. Report which
  prediction the data land on, with its error.
- **Inconclusive (also a result):** the predicted drop sits inside the
  instrument noise at the chosen distance, refraction was never measured, the air
  shifted so no single shape fits, or the cross-checks disagree. Then say so and
  run again — do not force a verdict.

## 3. Bill of materials

Priced list with a checked-on date: **[`hardware/BOM.csv`](hardware/BOM.csv)**.
The $50–$300 entry assumes you already own a tripod, a camera, and an
inclinometer. The fuller **drone-profile** build (downward lidar logging tens of
thousands of height readings) costs more — its tiered, linked component options
are in the protocol's [Equipment section](laser-experiment.html#equipment).

## 4. Build

Fire from a height over open water (a bluff or sea cliff) so the beam rides clear
of the worst near-surface air. Level the beam against an independent reference,
then **clamp both axes**. Either fly a drone that follows the beam centroid and
logs its height above the water, or set three equal-height markers (origin,
midpoint, far end) and photograph the midpoint against the chord. Full diagrams,
sensor layout, and a known-flat **control** run are in the
[protocol](laser-experiment.html).

## 5. Procedure

Level at the origin → lock → record predictions (both sides) → run, logging
height against distance (and against the clock, the axis nobody disputes) →
measure refraction on the night (two colours and/or a vertical-gradient column)
→ read the end depression and, where set, the midpoint figure. Blind/witness what
can bias it, and publish the raw logs. Step-by-step:
[Procedure](laser-experiment.html#procedure).

## 6. Reading the result

The surface drop is recovered **globe-free**: measured height + measured beam sag
→ surface drop in metres, owing nothing to any radius; only then does R enter, as
the output R = d²/(2·drop) compared against 6,371 km. Refraction is taken out as
a *measured* bend (the two-colour dispersion returns it with no shape assumed),
not an assumed coefficient. The math, the small-angle-vs-exact note, and the
effective-radius treatment are in
[Reading the results](laser-experiment.html#measurements) and the embedded
[simulator](../../resources/surface-shape-simulator/simulator.html); analysis scripts go in [`analysis/`](analysis/).

## 7. Results & replication log

No clean runs are logged yet, so the status is **untested**. Recorded runs and
the replication table live in [`results/`](results/); raw runs go under
[`data/`](data/), one folder per run. A refuted or inconclusive result is a
successful contribution.

## 8. Safety

- **532 nm laser is an eye hazard.** Everyone on the crew wears **OD 4+ 532 nm
  goggles**; keep the beam **above head height** once lit; never sweep it toward
  people, roads, boats, or aircraft. Higher-power (>5 mW) units carry real injury
  risk and, in some places, permits.
- **On/near water:** standard boating and shore safety; a chase boat for any
  drone run beyond easy reach.
- Drone flights follow local airspace rules (in the US, visual line of sight for
  recreational flight, or a Part 107 + waiver beyond it).

## Sources

- Wallace, A. R. (1908). *My Life* — Bedford Level, 1870.
- Oldham, H. Y. (1901). Experimental demonstration of the curvature of the earth's surface. *Report of the British Association*.
- Hirt, C., et al. (2010). Monitoring of the refraction coefficient in the lower atmosphere. *JGR Atmospheres*, 115(D21). https://doi.org/10.1029/2010JD014067
- Friedli, E., Presl, R., & Wieser, A. (2019). Influence of atmospheric refraction on terrestrial laser scanning at long range. *JISDM/FIG*. https://www.fig.net/resources/proceedings/2019/04_JISDM2019/18.pdf
- FECORE (Szekely & Cavanaugh, 2018) and the Metabunk analysis (Rodoxag, 2021) — prior laser-over-water attempts the protocol is built against.
- Soundly / Lake Pontchartrain (West, 2017, Metabunk) — three-point geometry in the field.

Full citations are in the protocol's [References](laser-experiment.html#references).
