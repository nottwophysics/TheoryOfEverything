# Deeper P4 research items 19 & 20 — honest verdicts

These two roadmap items are research questions, not cleanups. The
falsification-first ethos of this review means the deliverable is to *attempt*
each derivation and report truthfully whether the framework's axioms deliver —
not to manufacture a positive result.

---

## Item 19 — develop the one framework-unique prediction (P4)

**Module:** `predictions/consciousness_decoherence_bound.py`
**Tests:** `tests/test_p4_bounded_conjecture.py` (8)

P4 (consciousness-dependent decoherence) is the framework's only non-borrowed
claim. As written in `predictions/testable.py` it is *qualitative* ("the rate
differs") and leans on the discredited PEAR / Global Consciousness Project
results. The roadmap: derive a quantitative effect size from the axioms, or drop
it.

**Honest finding.** The framework's consciousness axioms
(`philosophy/brahman/consciousness.py`) contain **no parameter with physical
units** — Brahman is a normalized field whose only scalar invariant is a
dimensionless "coherence" in [0, 1], and the consciousness signatures use
dimensionless IIT Φ. **No effect size can be derived**, because nothing in the
axioms sets a magnitude. Pretending otherwise would be dishonest.

**What was done instead — make it sharp and falsifiable.** P4 is developed as a
quantitative **bounded conjecture**:

- **Operational coupling.** In a which-path / quantum-eraser interferometer,
  complementarity fixes fringe visibility via V² + D² ≤ 1 (Englert 1996), with
  no role for consciousness. Add one dimensionless coupling ε ≥ 0:
  `V_conscious = V_physical·(1 − ε)`, everything physical held identical. Then
  **ε = (V_auto − V_conscious)/V_auto** is directly measurable. ε = 0 is standard
  QM (all interpretations agree); ε > 0 is the framework-unique claim.
- **Current bound.** No which-path / eraser experiment (Walborn 2002, Kim 2000,
  Jacques 2007, reviewed in Ma–Kofler–Zeilinger 2016) has ever reported an
  observer-consciousness dependence; all agree with QM. A null at 1% visibility
  precision bounds **ε < 0.02 (2σ)**.
- **Powered protocol.** Detecting ε = 0.01 at per-trial visibility noise 0.05
  requires **N ≈ 197 blinded, pre-registered trials** (α = 0.05, power = 0.8),
  randomizing conscious-vs-automated readout with all physical confounds matched.

**Recommendation baked into the module:** reclassify P4 from "prediction" to
"bounded conjecture", retire the PEAR/GCP citations, and state the current
experimental upper bound plus the protocol that would tighten it.

All five references CrossRef-verified: Englert `10.1103/PhysRevLett.77.2154`,
Walborn `10.1103/PhysRevA.65.033818`, Kim `10.1103/PhysRevLett.84.1`,
Jacques `10.1126/science.1136303`, Ma–Kofler–Zeilinger `10.1103/RevModPhys.88.015005`.

---

## Item 20 — derive-don't-fit for α

**Module:** `numerology/derive_dont_fit.py`
**Tests:** `tests/test_derive_dont_fit.py` (7)

The roadmap fixes the standard a "derivation" of α must meet: **zero free
parameters, fixed by axioms, predicts α AND a second constant, agrees with
CODATA.** This module makes that standard **mechanically checkable** — four
hard pass/fail criteria — and audits the framework's own α attempts against it,
using values computed live from its modules.

**Result: every candidate is a SEARCH, not a DERIVATION.**

| candidate | 1/α predicted | rel. err | criteria passed |
|---|---|---|---|
| v2: `163 − 26 + π/100` (Heegner + bosonic dim) | 137.0314 | 3.3e-5 | **0 / 4** |
| v3 Feigenbaum δ × (2π)² | 184.33 | 0.35 | 1 / 4 |
| v3 r∞ × δ × α_F × e/π | 36.10 | 0.74 | 1 / 4 |
| v3 4π × n_eff × α_F | 36.85 | 0.73 | 1 / 4 |

- The celebrated **v2 formula fails all four**: 163, 26 and the denominator 100
  are each chosen to land near 137 (3 free parameters); they are imported from
  unrelated mathematics, not forced by any axiom; the base 163 recurs in **0 of
  5** other constants (per `numerology/cross_validation.py`); and 137.0314 is
  **outside** the CODATA uncertainty (CODATA 2022: 137.035999177 ± 2.1e-8).
- The **parameter-free Feigenbaum attempts** pass criterion 1 (genuinely not
  tuned) but miss α by **35–74%** and predict no second constant.

**First-principles constraint?** The honest interim goal was to show the axioms
*constrain* α to any range, even loosely. They do not: the only parameter-free
scalar the axioms fix is dimensionless coherence in [0, 1], and no axiom maps it
to α or bounds α to a sub-range. **The framework does not constrain α at all** —
every α value is equally compatible with the stated axioms. The α work is a
numerical search over convenient constants, correctly housed in `numerology/`.

CODATA 2022 reference CrossRef-verified: Mohr, Newell, Taylor & Tiesinga,
Rev. Mod. Phys. 97, 025002 (2025), `10.1103/RevModPhys.97.025002`.

---

## Bottom line

Both items resolve the same way: the framework's two most ambitious claims —
consciousness-dependent decoherence and an α derivation — **cannot be derived
from its stated axioms**. Item 19 converts P4 into a genuinely falsifiable,
currently-bounded conjecture with a powered protocol. Item 20 provides a
mechanical standard that classifies every α attempt as a search. Neither is a
failure of the review; a truthful "not derivable, here is what would be needed"
is the correct scientific outcome.

Figure: `p4_alpha_research.png`. Full suite after these additions: **280 tests**.
