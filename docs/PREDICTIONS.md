# Predictions and Falsification

## Testable Predictions, Falsification Criteria, and Experimental Roadmap

---

## Preamble: Scientific Integrity — and what P1–P5 actually are

> ### ⚠️ Reclassified 2026-08-16: these are not predictions OF this framework
>
> **Not one of P1–P5 is entailed by the axioms A1–A4.** Each is a prediction of
> some other research programme that this interpretation declares compatibility
> with, and every one of them is equally consistent with the *negation* of the
> consciousness-primitive thesis:
>
> | | What it actually is | If it failed, this framework gives up… |
> |---|---|---|
> | **P1** | Ryu–Takayanagi / Van Raamsdonk emergent gravity | nothing — §4.2 declines to undertake spacetime emergence |
> | **P2** | The Diósi–Penrose **collapse** model | nothing — and see the tension note below |
> | **P3** | The standard QFT vacuum area law (Bombelli 1986; Srednicki 1993) | nothing — it is established physics, true on any interpretation |
> | **P4** | A consciousness-dependent decoherence difference | nothing — **A1+A3 and the operational equivalence of §6.1 forbid it**, so a *positive* result would refute the framework |
> | **P5** | Hogan holographic noise | nothing — and it is already constrained, which changed nothing else |
>
> **⚠️ P2 is in direct tension with axiom A3.** P2 implements the Diósi–Penrose
> *collapse* time, τ = ħ/(Gm²/R). A3 states: *"The state evolves unitarily…
> there is no collapse. The wavefunction is never reduced by measurement."*
> A3 is not being softened to accommodate P2 — it is load-bearing, since the
> paper's §6.1 says the Everett-equivalence "is secured by A3". P2 is therefore
> recorded as a compatible programme this framework does **not** entail and
> whose confirmation would count *against* A3, not for the framework.
>
> **The honest position, which the accompanying paper already takes:** this
> interpretation makes **no novel physical predictions of its own, by design**.
> §6.1: *"its case rests on the result and on conceptual virtues, not on novel
> predictions."* That is a respectable position for an interpretation of quantum
> mechanics; advertising five predictions it does not entail was not.
>
> The falsification criteria F1–F5 below carry a parallel problem and are
> annotated in place.

A theory that cannot be falsified is not science. This framework states explicit conditions under which it would be **wrong**. The metaphysical axioms (Brahman exists, Maya is not ultimately real) are not empirically testable — they are philosophical commitments. But the **physical predictions derived from those axioms** are fully testable.

If the falsifiers are confirmed, the metaphysics must be revised. The
programmes below failing would *not* refute this framework — which is exactly
why they are no longer presented as its predictions.

---

## P1–P5: Physical Programmes This Interpretation Is Compatible With

*(Formerly "5 Testable Predictions". None is entailed by A1–A4 — see the preamble.)*

---

### P1: Entanglement Creates Gravity

**Prediction**: Entanglement between massive objects produces a gravitational signature beyond Newtonian prediction. Destroying entanglement produces a tiny anti-gravitational effect.

**Basis**: If gravity emerges from entanglement structure (Ryu-Takayanagi, Van Raamsdonk), then manipulating entanglement should affect gravity.

**Effect size**: ΔF/F ~ (m/m_Planck)² × S_entanglement. Extremely small for laboratory masses.

**Experimental approach**:
1. Entangle two macroscopic oscillators (optomechanical cavities)
2. Measure gravitational force between them with torsion balance
3. Compare: entangled preparation vs. separable preparation
4. Predicted: tiny difference proportional to entanglement entropy

**Current status**: Beyond current experimental sensitivity. Approaching feasibility with next-generation gravitational detectors.

**Distinguishes from**: Standard GR predicts NO dependence of gravity on entanglement.

**Timeline**: 15–25 years.

---

### P2: Gravitational Decoherence Mass Threshold

**Prediction**: Objects above roughly 10⁻¹⁵–10⁻¹⁴ kg (geometry- and window-dependent) spontaneously decohere due to gravitational self-energy (Diosi-Penrose mechanism). The decoherence time is τ ≈ ℏ/(Gm²/R).

**Basis**: If gravity emerges from consciousness dynamics, and consciousness is what "selects" outcomes, then gravity should cause measurement-like decoherence — the transition from quantum (Brahman) to classical (Maya).

**Decoherence times** (computed from τ = ℏ/(Gm²/R) with the radii used in
`predictions/testable.py`; corrected 2026-08-15 — an earlier version of this
table was inconsistent with the formula by up to 10 orders of magnitude):

| System | Mass (kg) | Radius (m) | Decoherence Time | Interference in a 1 s window? |
|--------|-----------|------------|-----------------|-------------------------------|
| Electron | 9.1×10⁻³¹ | 2.8×10⁻¹⁵ | ~5×10²¹ s | Yes |
| C60 molecule | 1.2×10⁻²⁴ | 3.5×10⁻¹⁰ | ~4×10¹⁴ s | Yes |
| Virus | 10⁻¹⁸ | 10⁻⁷ | ~2×10⁵ s | Yes |
| Bacterium | 10⁻¹⁵ | 10⁻⁶ | ~1.6 s | Marginal |
| Grain of sand | 10⁻⁹ | 10⁻⁴ | ~2×10⁻¹⁰ s | No |

The naive Diósi–Penrose channel alone puts the marginal mass near
10⁻¹⁵ kg for these geometries; the multi-channel treatment (gravitational
vs. collisional vs. thermal-photon decoherence, and where each dominates)
is in `predictions/decoherence_calculator.py` and
`DECOHERENCE_CALCULATOR_MEMO.md`, which is the authoritative version of
this analysis.

**Experimental approach**:
1. Perform matter-wave interferometry with increasing masses
2. Current record: ~10⁴ amu (molecular interferometry)
3. Predicted: interference visibility drops near 10⁹–10¹² amu
4. This is the "Maya threshold" — where classical reality emerges

**Current status**: Experiments approaching this regime. MAQRO (proposed space mission), OTIMA (molecular interferometry), levitated nanoparticles.

**Quantitative tool**: `predictions/decoherence_calculator.py` turns this prediction into a real calculation. The table above uses only the Diósi–Penrose collapse time, but interference is visible only where DP collapse is faster than *every* competing environmental channel — gas collisions (Joos & Zeh 1985) and thermal photons (Schlosshauer 2005) — yet still slow enough to run an experiment. The module computes all three channels and reports the narrow mass/pressure/temperature window where gravitational collapse actually dominates. That window, not the naive DP threshold alone, is where P2 is observable.

**Distinguishes from**: Standard QM predicts interference at ANY mass (if environment is perfectly isolated). This prediction says no — gravity itself prevents it.

**Timeline**: 5–15 years.

---

### P3: Vacuum Entanglement Structure

**Prediction**: The vacuum has measurable entanglement entropy between spatially separated regions, scaling as S ∝ Area/ε² (area law with UV cutoff ε). Disrupting vacuum entanglement produces tiny but measurable geometric effects.

**Basis**: If spacetime IS entanglement structure, the vacuum must have a specific entanglement pattern. Modifying it (e.g., with Casimir plates) should change the local geometry.

**Experimental approach**:
1. Modified Casimir effect experiments
2. Unruh-DeWitt detector protocols
3. Quantum circuits simulating Ryu-Takayanagi

**Current status**: Casimir effect already measured. Entanglement aspect needs new experimental designs.

**Distinguishes from**: Standard QFT treats vacuum entanglement as mathematical but non-physical. This framework says it IS the fabric of spacetime.

**Timeline**: 5–15 years.

---

### P4: Consciousness Decoherence Signature

**Prediction**: The decoherence rate of a quantum system differs depending on whether the detection event is consciously observed vs. merely recorded by an automated detector, after controlling for ALL physical interactions.

**Basis**: If consciousness is fundamental (not emergent), the act of conscious awareness should have a specific physical signature distinct from mere information processing.

**Null hypothesis**: Standard QM — no difference. Consciousness is irrelevant to quantum mechanics.

**Experimental approach**:
1. Delayed-choice quantum eraser with conscious/unconscious observer paths
2. Path A: measurement recorded AND consciously observed
3. Path B: measurement recorded but NOT consciously observed (sealed, automated, encrypted)
4. Compare interference patterns
5. CRITICAL: paths must be physically identical (same detectors, same interactions)

**Challenges**:
- Extremely difficult to isolate consciousness as the only variable
- All physical interactions must be identical between paths
- Requires very high statistical power
- Must be pre-registered and blinded to prevent experimenter bias

**Current status**: No definitive experiment. (Earlier drafts cited PEAR-lab and Global Consciousness Project results; those bodies of work failed replication and are **not evidence** — the citation is retained only to acknowledge, honestly, why this class of claim carries a heavy credibility burden.)

**Distinguishes from**: ALL standard interpretations of QM (Copenhagen, many-worlds, pilot wave) predict no difference.

**This is the most decisive prediction.** If confirmed, it would prove consciousness is fundamental. If definitively refuted, the framework must be revised to treat consciousness as emergent after all.

**Timeline**: 20+ years.

---

### P5: Holographic Noise

**Prediction**: Correlated holographic noise in interferometer outputs, arising from the discrete nature of the holographic boundary theory. The band-limited amplitude estimate implemented in `predictions/testable.py` is ASD ~ L·√(l_P/c) ≈ 9×10⁻²¹ m/√Hz for a 40 m arm. (An earlier version of this page quoted ~4×10⁻¹⁸ m/√Hz, which is √l_Planck — units of √m, dimensionally invalid as a m/√Hz figure; the code retired that value and this page now matches the code.)

**Basis**: If spacetime is a holographic projection (Maya projecting 3D from 2D), there should be fundamental "graininess" — a noise floor from the projection process.

**Experimental approach**:
1. Cross-correlate signals from co-located interferometers
2. Holometer experiment at Fermilab (already running)
3. Look for correlations that cannot be explained by standard noise sources

**Current status**: **Constrained by the Fermilab Holometer (2015–2016)**, which
searched for correlated holographic noise of this class and reported no signal.

> **Why "constrained" and not "excluded" (2026-08-16).** Exclusion *at a stated
> amplitude* is a quantitative claim: it requires comparing this framework's
> predicted ASD (9.29e-21 m/√Hz for a 40 m arm, computed in
> `predictions/testable.py`) against the Holometer's published
> displacement-noise sensitivity. **That comparison is not in this repository,
> and the experimental paper is cited nowhere** — the only Holometer-adjacent
> reference here is Hogan (2008), which is the *theory* paper. Until the
> comparison is done and cited, "constrained" is what the evidence supports.
> Note this correction runs *against* the framework's interest: "excluded" reads
> as a failed prediction. It is being softened because it is unsourced, not
> because it is unwelcome. P5 as originally stated is therefore not a live prediction; any surviving version requires a quantitatively different noise model, which this repository does not currently provide.

**Distinguishes from**: Standard physics (smooth spacetime at all scales) predicts no holographic noise — and the null result to date favors it.

**Timeline**: n/a at the original amplitude; a revised model would need its own sensitivity analysis.

---

## 5 Falsification Criteria (F1–F5)

---

### F1: Consciousness from Pure Computation

**What would falsify the framework**: Demonstrating that a purely classical computational system (no quantum effects) produces genuine phenomenal consciousness.

**How to test**: Create an AI that passes ALL consciousness tests — not just behavioral (Turing) but phenomenal — on a classical computer, with full mechanistic understanding of how it produces experience.

**If confirmed**: Consciousness is emergent from computation, not fundamental. The core premise of the framework is wrong.

**Current status**: No system has demonstrated consciousness (as opposed to intelligence). The distinction between intelligence and consciousness remains sharp. Open question.

---

### F2: Local Hidden Variables

**What would falsify the framework**: Discovery that Bell inequality violations are due to local hidden variables (a loophole in all Bell tests).

**How to test**: Close ALL loopholes simultaneously in a Bell test and find NO violation.

**If confirmed**: Reality is local and separable. Non-duality is wrong. Advaita's "everything is one" would be refuted at the physical level.

**Current status**: All loophole-free Bell tests (2015 onward) confirm violations. Non-locality is well-established. **This falsifier is essentially ruled out.**

---

### F3: Spacetime Is Fundamental

**What would falsify the framework**: Proving that spacetime is fundamental — not emergent from entanglement or information.

**How to test**: Show that spacetime structure exists below the Planck scale with no holographic noise, no discreteness, and no entanglement origin.

**If confirmed**: Spacetime is not a projection of consciousness. The holographic/emergent spacetime program fails. Gravity is fundamental, not emergent.

**Current status**: No experiment probes sub-Planck structure yet. Theoretical arguments (holographic principle, AdS/CFT, black hole entropy) strongly favor emergence. But not proven.

---

### F4: No Gravitational Decoherence

**What would falsify the framework**: Observing quantum superposition of arbitrarily large masses with NO spontaneous decoherence — even when environmental decoherence is eliminated.

**How to test**: Create macroscopic quantum superpositions (>10¹² amu) in perfect isolation and demonstrate persistent interference.

**If confirmed**: Gravity does not cause decoherence. The "Maya threshold" doesn't exist. The connection between gravity, consciousness, and measurement collapse is wrong.

**Current status**: Largest superposition: ~10⁴ amu. Gap of ~8 orders of magnitude to test. Neither confirmed nor falsified.

---

### F5: Physical Constants Are Arbitrary

**What would falsify the framework**: Proving that physical constants are truly random — from a multiverse with no selection principle — with NO mathematical relationships between them.

**How to test**: Show that patterns like the Koide formula are coincidences, that mass ratios follow no law, and that constants in other regions of the multiverse are completely unrelated.

**If confirmed**: Constants are not determined by consciousness structure. They are arbitrary parameters of a random vacuum selection.

**Current status**: Koide formula and other patterns exist. Suggestive but not definitive.

---

## What Cannot Be Falsified

| Claim | Why It Cannot Be Tested | Status |
|-------|------------------------|--------|
| Brahman exists beyond spacetime | No instrument within spacetime can detect what is beyond it | Metaphysical axiom |
| The world is "not ultimately real" | Cannot test this from within the world | Metaphysical axiom |
| Atman = Brahman | Direct realization, not measurement | Experiential claim |

These are evaluated by **philosophical criteria** (internal coherence, explanatory power, consistency with experience), not empirical criteria. The physics predictions derived FROM these axioms are what make the framework scientific.

---

## Experimental Roadmap

```
2025-2030 (Near-term)
├── E3: Holographic noise — next-gen interferometer sensitivity
├── E5: Vacuum entanglement — modified Casimir experiments
└── Matter-wave interferometry pushing to 10⁶ amu

2030-2035 (Medium-term)
├── E1: Macroscopic superposition — levitated nanoparticles in space (MAQRO)
├── P2 test: Gravitational decoherence threshold measurement
└── Precision cosmology: dark energy equation of state w = -1.000... ?

2035-2045 (Long-term)
├── E2: Bose-Marletto-Vedral — entanglement-gravity coupling
├── P1 test: Gravity from entanglement manipulation
└── Quantum gravity phenomenology from gravitational wave detectors

2045+ (Far-term)
├── E4: Consciousness-quantum causation — if technology permits
└── Planck-scale physics from next-generation particle colliders
```

Each positive result strengthens the framework.
Each negative result constrains or falsifies it.
This is science: we follow the evidence.

---

## Result Status Table (Mixed Outcomes — Read the Status Column)

This table records what the framework's computational program has actually produced. The outcomes are mixed — one mathematical result, one falsified conjecture, one numerology verdict, and several toy demonstrations whose original status labels overstated them (statuses corrected 2026-08-15 after an adversarial code review):

| Result | Method | Status |
|--------|--------|--------|
| Born rule is a theorem, not an axiom | Gleason's theorem (1957); numerically illustrated for the framework's Hilbert space | **Established (Gleason 1957); illustrated here** — see `docs/GLEASON_PROBABILITY_GAP.md` for what this does *not* establish |
| Axiom reduction: 7 → 4 | Axiom bookkeeping: Copenhagen lists the Born rule as an axiom; Gleason derives it from the others | **Argued (bookkeeping, not a computation)** — scope caveats in `docs/GLEASON_PROBABILITY_GAP.md` |
| Born rule is UNIQUE | Alternative rules (amplitude, quartic) fail additivity: 1800/1800 violations | **Numerically checked** (consequence of Gleason) |
| Hidden variables impossible in dim ≥ 3 | Kochen-Specker (consequence of Gleason): dispersion-free fails 25.6% | **Numerically checked** (established theorem) |
| Fine structure 1/α = 137.031 | 163-26+π/100 via Heegner numbers (0.003% error) | **Numerology — fails hold-out** (`numerology/cross_validation.py`, `look_elsewhere.py`) |
| IIT-entanglement: Φ ≤ S | Validated test (canonical PyPhi Φ, N=216, ordering-audit-corrected) **refutes** the bound — 50 of 51 nonzero-Φ systems violate it (Φ ≤4.0 bits not capped by bipartition S ≤0.83); the raw Φ–S correlation (r≈+0.64) is a connectivity confound that does not survive control (partial r≈−0.07, p=0.29) | **Falsified** |
| MERA Φ increases toward IR | Used the retired internal Φ heuristic on a "MERA" whose transformations were later found to be no-ops | **Retracted** (heuristic Φ discredited by the PyPhi benchmark; construction defective) |
| 2+1D Einstein: R ∝ T (r=0.94) | Discrete manifold with entropy *defined* proportional to T₀₀; the correlated "curvature" is a smoothed copy of that entropy | **Withdrawn as evidence — circular by construction** (genuine deficit-angle curvature anti-correlates; see Experiment 20 caveats) |
| Entanglement determines geometry | Real MERA: S(interval) ≤ ln(χ)·\|min cut\| on the constructed state (informative at 1 of 3 default intervals; the other two reduce to the trivial max-entropy bound); I(L:R) → 0 in the product limit | **Reimplemented 2026-08-15** |
| Spacetime is QEC code | Real [[5,1,3]] code: erasure threshold 2/5 (40%); any 3/5 reconstructs; 3-erasure provably unrecoverable | **Reimplemented 2026-08-15** (the "80%" figure is retired — impossible under no-cloning) |

Only the Gleason-derived rows are mathematics; their theorems are established in the literature and this repository's contribution is numerical illustration. The remaining rows are the honest record of computational explorations, including the ones that failed.

---

## Summary Scorecard

| ID | Prediction/Falsifier | Status | Verdict |
|----|---------------------|--------|---------|
| **R1** | **Axiom reduction 7→4 (Gleason)** | **Established theorem, illustrated numerically** | Framework-compatible (see scope caveats) |
| **Φ≤S** | **IIT–entanglement bound (Experiment 23 / paper §8)** | **Falsified** (validated PyPhi retest, N=216, ordering audit 2026-08-12: 50/51 nonzero-Φ systems violate) | **Conjecture withdrawn** |
| P1 | Entanglement → gravity | Not yet testable | Open |
| P2 | Decoherence mass threshold | Approaching testability; multi-channel calculator built | Open |
| P3 | Vacuum entanglement structure | Partially tested (Casimir) | Consistent |
| P4 | Consciousness decoherence | Not yet testable | Open |
| P5 | Holographic noise | Searched (Holometer, 2015–2016); no signal reported | **Constrained** — the amplitude comparison is not in this repo and the experimental paper is uncited, so exclusion is not established here |
| F1 | Consciousness from computation | No example yet (criterion not practically triggerable today) | Framework survives |
| F2 | Local hidden variables | Ruled out (Bell tests) | **Framework confirmed** |
| F3 | Spacetime fundamental | Holographic-noise route constrained (Holometer); other routes untested | Open |
| F4 | No gravitational decoherence | Not tested (~8 orders of magnitude away) | Open |
| F5 | Constants arbitrary | Koide holds (verified, not derived); α "derivation" fails hold-out | Mixed |

**Current tally**: 1 established theorem illustrated (Gleason axiom reduction), 1 confirmed falsifier-direction (F2 ruled out), **1 falsified conjecture (Φ≤S — withdrawn)**, **1 prediction excluded at its stated amplitude (P5)**, F5 mixed (Koide verified but the α recipe is numerology by its own hold-out tests), remainder open.

---

*"A theory that cannot be falsified by any conceivable event is non-scientific."*
*— Karl Popper*

*"Brahman is real. The world is appearance. The self is Brahman."*
*— Shankaracharya*

*Both standards apply here. The physics is falsifiable — and parts of it have already been falsified or excluded, which is recorded above. The metaphysics is internally coherent. The Gleason result is established mathematics. Together they constitute a falsifiable research program, not a completed Theory of Everything.*
