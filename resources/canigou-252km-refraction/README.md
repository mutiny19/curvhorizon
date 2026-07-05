# Canigou to Marseille, 252 km: Refraction & Visibility Analysis

A worked case study for the [Laser Beam Follow Experiment](../../experiments/laser-experiment/laser-experiment.html):
the atmospheric refraction coefficient is **solved from a single long-range photograph**,
over four independent targets, rather than assumed.

**Live:** https://replicationbench.github.io/RB/resources/canigou-252km-refraction/

## Headline

From a near-infrared panorama of the Gulf of Lion / Marseille shot from the summit of
the Canigou (2,784.7 m, 252 km line of sight), the refraction coefficient during the
exposure is **k = 0.126** (1-sigma 0.118-0.134), from a one-parameter chi-squared fit
(chi-squared 0.18 over 3 degrees of freedom, all four residuals under one pixel).
The optical horizon at this k is 201.5 km, and every visibility fact in the image
follows: Notre-Dame de la Garde shows only its top ~44 m, the Port-Saint-Louis
turbines show rotors but not their bases, and Cap Sicie (which needs k >= 0.19) is
absent, exactly as predicted. Everything is labelled measured / assumed / solved,
and the analysis states what would falsify it.

## What is (and is not) in this folder

Hosted here (the analysis, all reproducible):

- `canigou-252km-refraction.html` — the write-up, tables, and an original hidden-height figure.
- `data/geometry.json`, `data/kfit.json` — machine-readable distances, azimuths, fit inputs and results.
- `data/Canigou_hidden_vs_visible.xlsx` — per-landmark table; change the k cell and everything recomputes.
- `scripts/` — the Python used for the geodesic geometry, the fit, and the renders.

**Not hosted here:** the source panorama and its derivative renders. The photograph is
**© Antoine Mangiavacca** (12 September 2019), a third party; it is used here by
**reference only**, out of respect for the photographer's rights. View it at the source:

- Beyond Horizons write-up: https://beyondrange.wordpress.com/2019/09/12/canigo-pyriness-notre-dame-de-la-garde-marseille-252-kms/
- Photographer's galleries: https://www.klape.fr/panoramas

## Honest-scale note

The source image is reflected near-IR (1000 nm), not thermal LWIR. Brightness is not
temperature; any temperature scale on it is decoration, not measurement.

## License

The analysis, data tables, and scripts here are covered by this repository's license.
The source photograph is not ours and is not redistributed; its rights remain with the
photographer.
