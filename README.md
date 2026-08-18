# A Computational Exploration of Consciousness-First Physics

**Companion code to** *The Cardinality of Experience Is Underdetermined by the Quantum State: A Constructive Case for a Consciousness-Primitive Interpretation* ([10.5281/zenodo.21007975](https://doi.org/10.5281/zenodo.21007975)) — together with a wider, largely exploratory modelling of **Advaita Vedānta**'s non-dual metaphysics alongside modern physics.

> ### Read this before the results table
>
> **This is an exploration, not a finished physical theory**, and the repository name it long carried ("Theory of Everything") overstated it. Most physics modules here are toy models or illustrations; the status labels say which is which, and several are **withdrawn**.
>
> **The work most worth your attention is where this project refuted itself.** Its own validated retest **falsified** its Φ ≤ S conjecture; its own look-elsewhere analysis demoted its 0.003% fine-structure formula to **numerology**; a 2026 adversarial review found the Einstein-equation demos **circular by construction**, and four withdrawn demos were then rebuilt against criteria frozen in an earlier commit. Those retractions are load-bearing, not disclaimers.
>
> **If you arrived from the paper**, its computational support is four modules — [`quantum/unity_of_experience.py`](quantum/unity_of_experience.py), [`quantum/perspectival_asymmetry.py`](quantum/perspectival_asymmetry.py), [`quantum/gleason.py`](quantum/gleason.py) and [`quantum/operational_equivalence.py`](quantum/operational_equivalence.py) — plus the §8 reproducibility package in [`reproducibility/phi_s/`](reproducibility/phi_s/). Each carries an in-code note on exactly what it does and does not establish; several state plainly that their result is a theorem of the formalism and therefore cannot favour one interpretation over another. The rest of the repository is not cited by the paper.

This project models the metaphysical framework of Advaita Vedānta — the non-dual philosophy declaring that consciousness (Brahman) is the sole reality — and explores how quantum mechanics, general relativity, the Standard Model, and the physical constants of nature *might* be understood as emergent properties of a single consciousness field.

Its two most defensible products, honestly stated, are both negative results: a **validated falsification of its own Φ ≤ S conjecture** (canonical PyPhi retest), and a self-critical look-elsewhere analysis demoting its own 0.003% fine-structure formula to **numerology**. The Gleason work is sometimes listed beside these; it should not be. Gleason's theorem is established mathematics and is illustrated faithfully here, but the "7 → 4 axiom reduction" drawn from it is *arithmetic on hand-entered integers* — the module says so at runtime — and belongs in a different category from a computed result. The Einstein-equation recovery demos (1D/2D/3D) were found by a 2026 adversarial code review to be **circular by construction** (the "entropy" they correlate is defined from the energy density) — they illustrate the Jacobson logic; they do not demonstrate it.

**Reimplementation (2026-08-15).** Four demos the review withdrew were rebuilt to compute what they claim, against acceptance criteria [pre-registered before implementation](REAL_PHYSICS_REIMPLEMENTATION_MEMO.md): a genuine **[[5,1,3]] stabilizer code** (all 15 single-qubit Paulis corrected; erasure threshold **2/5 = 40%**, reconstruction from any **3/5 = 60%** — the retired "80%" was not merely unsupported but impossible under no-cloning); a **real MERA** whose tensors are contracted into an explicit 16-site state (perturbing any layer moves the state — the retired version scored exactly 0 on that control); **Verlinde's actual derivation**, reproducing GMm/r² to 3e-16; and, for gravity, the statements that are actually true in 2D — **Gauss–Bonnet** on the Delaunay mesh and the **entanglement first law** δS = δ⟨K⟩ (log-log slope 2.02). 22 of 23 frozen criteria passed; **the one that failed is committed as a visible `xfail`, not renegotiated.**

---

## The Central Thesis

> **Brahman (pure consciousness) is the sole reality. The physical universe — spacetime, particles, forces, constants — is an appearance (Maya) within that consciousness. The laws of physics are regularities in the appearance. Liberation (Moksha) is the recognition that the appearance was never separate from its source.**

This thesis aims to be testable, and is honest about how far that reaches: **it makes no novel physical predictions of its own, by design** — the accompanying paper says so, and an interpretation of quantum mechanics operationally equivalent to Everett cannot. What the repository lists as P1–P5 are **physical programmes this interpretation is compatible with**, none entailed by its axioms (see [docs/PREDICTIONS.md](docs/PREDICTIONS.md)). It also states **5 falsification criteria** (F1–F5) — and records outcomes against itself: the Φ ≤ S conjecture has been **falsified** by the project's own validated retest, and P5's holographic noise is **constrained** by the Fermilab Holometer (2015–2016), which reported no signal — *constrained* rather than *excluded*, because the amplitude comparison that would establish exclusion is not in this repository and the experimental paper is uncited. If these programmes fail, that refutes the programmes; on the framework itself it would change nothing, which is the point of the reclassification. See [docs/PREDICTIONS.md](docs/PREDICTIONS.md) for the full scorecard.

---

## Quick Start

```bash
# Clone the repository
git clone https://codeberg.org/advait/TheoryOfEverything.git
cd TheoryOfEverything

# Create and activate virtual environment
python3 -m venv toenv
source toenv/bin/activate

# Install the package and its dependencies (editable install).
# This registers all sub-packages on the import path, so you no longer
# need to set PYTHONPATH or run from the repository root.
pip install -e .

# Run the quick demo — either form works after install:
theory-of-everything          # console entry point (runs from anywhere)
python main.py --demo         # or the script directly

# Run all 8 original Advaita experiments
python main.py --all

# Run all 23 physics extension experiments (9–31)
python main.py --physics

# Run a specific experiment (1–31)
python main.py --experiment 24

# Generate all 7 visualizations
python main.py --visualize

# Run EVERYTHING (31 experiments + visualizations)
python main.py --everything

# Run the test suite (490 tests): install the test extra, then run from the
# repository root (pytest resolves testpaths=tests relative to the project root).
pip install -e ".[test]"
pytest
```

> **Note on imports.** After `pip install -e .` every sub-package
> (`constants`, `numerology`, `predictions`, `gravity`, `quantum`, …) is
> importable from any working directory. The previous requirement to prefix
> commands with `PYTHONPATH=.` is gone.

For a guided walkthrough of the project, see [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md).

---

## What This Project Contains

| Layer | Modules | Purpose |
|-------|---------|---------|
| **Metaphysical Foundation** (interpretive, not empirical) | `philosophy/` (`brahman/`, `maya/`, `levels/`, `liberation/`), `emergence/` | Models the core Advaita Vedanta framework — see `philosophy/README.md` |
| **Quantum Mechanics** | `quantum/` | QM from consciousness; Gleason's theorem; tensor networks; QEC; 4 interpretations |
| **General Relativity** | `gravity/` | Emergent gravity from entanglement; 2+1D Einstein equations |
| **Standard Model** | `particles/` | Particles and forces from Maya's symmetry breaking |
| **Physical Constants** | `constants/` | Koide verification; cosmological-constant comparison (published values restated, not derived) |
| **Numerology (self-audit)** | `numerology/` | Fine-structure formula search (0.003% error) + hold-out cross-validation + look-elsewhere analysis — verdict: numerology |
| **Predictions** | `predictions/` | 5 compatible physical programmes (P1–P5; none entailed by the axioms) + IIT-entanglement bridge |
| **Falsification** | `falsification/` | 5 explicit falsification criteria + experimental designs |
| **Visualizations** | `visualizations/` | 7 visual plots of Advaita concepts |
| **Experiments** | `simulations/`, `main.py` | 31 runnable experiments demonstrating the framework |
| **Test Suite** | `tests/` | 490 automated tests validating all modules |

---

## The Philosophical Foundation

Advaita Vedanta (Sanskrit: "non-dual end of the Vedas") is a 3000-year-old metaphysical system formalized by Adi Shankaracharya (~788–820 CE). Its core claims:

1. **Brahman alone is real** — pure consciousness, infinite, without attributes (Nirguna)
2. **The world is Maya** — not "illusion" but "appearance" — valid within its own frame but not ultimately real
3. **The individual self (Atman) IS Brahman** — not "part of" or "connected to" but literally identical
4. **Liberation (Moksha)** is recognizing what was always the case — not gaining something new

These claims have been *proposed to parallel* structures in modern physics; [docs/PHILOSOPHY.md](docs/PHILOSOPHY.md) sets out the mapping in full. Read it with the accompanying paper's own verdict in view: the Sanskrit vocabulary names roles the framework defines independently, and is **eliminable everywhere without loss** — it is illuminating, not load-bearing. Nothing in the physics depends on it, and the mapping generates no constraint that standard physics does not already supply.

---

## The 31 Experiments

### Tier 1 — Advaita Framework (1–8)

| # | Name | What It Demonstrates |
|---|------|---------------------|
| 1 | **Rope-Snake** | Superimposition (Adhyasa) — ignorance creates false appearances |
| 2 | **Fractal Unity** | Self-similarity as non-duality — the part IS the whole |
| 3 | **One Field, Many Observers** | Same Brahman, different guna-lenses, different experiences |
| 4 | **Dreamer Analogy** | Dream → Wake → Liberation sublation chain |
| 5 | **Neti-Neti Debugger** | Stripping layers to reveal the irreducible witness |
| 6 | **Guna Dynamics** | Sattva/Rajas/Tamas cycling while Brahman remains unchanged |
| 7 | **Four Mahavakyas** | The great identity declarations (Atman = Brahman) |
| 8 | **Vivartavada** | Gold-ornament and ocean-wave apparent causation |

### Tier 2 — Physics Extensions (9–16)

| # | Name | What It Demonstrates |
|---|------|---------------------|
| 9 | **Quantum Hilbert Space** | Brahman IS the Hilbert space; entropy = Maya's depth |
| 10 | **Measurement Problem** | Dissolved — total state pure, observer's reduced state mixed |
| 11 | **Entanglement = Non-Duality** | CHSH at the Tsirelson bound 2√2 — evaluated analytically (the demo does not consume a quantum state); illustrative, not a verification |
| 12 | **Emergent Gravity** | Space from entanglement; Verlinde's derivation implemented faithfully in SI units — recovers GMm/r² to 3e-16. **That agreement is algebraic**: the constants cancel exactly, so it validates the implementation, not nature. Route 1 presupposes a = GM/r² and is F = ma by construction; only Route 2 derives the r-dependence (reimplemented 2026-08-15; the legacy broken route kept as a negative control) |
| 13 | **Holographic Principle** | Bulk (world) is projection of boundary (consciousness) |
| 14 | **Particles from Maya** | Symmetry breaking; 3 generations = 3 gunas |
| 15 | **Physical Constants** | Koide formula verified; Λ consistent with consciousness entropy |
| 16 | **Predictions & Falsification** | 5 compatible programmes (not entailed predictions), 5 falsification criteria |

### Tier 3 — Formal Comparisons & Frontier Explorations (17–23)

| # | Name | What It Demonstrates |
|---|------|---------------------|
| 17 | **Four Interpretations Compared** | Copenhagen vs Many-Worlds vs Pilot Wave vs Advaita — formal comparison across 8 phenomena |
| 18 | **Gleason's Theorem** | Born rule derived as theorem; axiom reduction 7 → 4 (established theorem, numerically illustrated — scope caveats in docs/GLEASON_PROBABILITY_GAP.md) |
| 19 | **MERA Tensor Network** | Real binary MERA (χ=2, 16 sites): tensor algebra verified, RT-type entropy bound computed on the actual state, entanglement→connectivity sweep. Reimplemented 2026-08-15 after the original was found inert |
| 20 | **2+1D Einstein Equations** | ⚠️ Circular by construction (entropy is defined ∝ T₀₀; the correlated "curvature" is a smoothed copy of it; genuine deficit-angle curvature anti-correlates) — illustrates the Jacobson logic only |
| 21 | **QEC as Spacetime** | Real [[5,1,3]] perfect code: all 15 single-qubit Paulis corrected, 2/5 erasure threshold, any 3/5 subregion reconstructs. Reimplemented 2026-08-15; the old "80%" is retired as impossible |
| 22 | **Fine Structure Constant v2** | 6 systematic approaches; best: 163-26+π/100 = 0.003% error (1000x improvement over v1 — but see Experiment 31: numerology) |
| 23 | **IIT-Entanglement Bridge** | Original Φ ≤ S "holds 100%" is circular; a validated retest (canonical PyPhi Φ, N=216; TPM-ordering audit 2026-08-12) **falsifies** the bound — 50 of 51 nonzero-Φ systems violate it (Φ up to ≈4.0 bits vs S ≤0.83) — and the raw Φ–S correlation (r≈+0.64) is a connectivity confound (partial r≈−0.07, p=0.29), so nothing residual survives |

### Tier 4 — Paper Companion Experiments (24–26)

| # | Name | What It Demonstrates |
|---|------|---------------------|
| 24 | **Everett-Advaita Operational Equivalence** | The quantities both readings share, computed once. Equivalence is **analytic, not tested** — one Hilbert space, one Born rule, so identical predictions follow by construction. The old "5/5 tests identical" scoreboard compared an array with a copy of itself and was deleted 2026-08-16 |
| 25 | **Perspectival Asymmetry (Generalized)** | Total purity = 1.0 exactly — a theorem of unitarity (true by construction), presented as such rather than as an empirical finding |
| 26 | **Observer Centrality** | Decoherence selects basis but NOT outcome; "observer" does essential work in the formalism |

### Tier 5 — Physics Extensions (27–31)

| # | Name | What It Demonstrates |
|---|------|---------------------|
| 27 | **3+1D Einstein Equations** | ⚠️ Same circular construction as Experiment 20, in 3D — illustrates the logic; the correlation is not evidence |
| 28 | **ER=EPR Correspondence** | Illustrative identities (the throat–entropy relation is imposed by definition in the demo, not derived) |
| 29 | **Fine Structure v3** | Derivation attempts (numerology-class): self-referential, modular bootstrap, holographic constraint; continued fraction analysis |
| 30 | **Unity of Experience** | Experiential underdetermination — decoherence fixes ρ_SA but not experiential ontology |
| 31 | **Look-Elsewhere Effect** | Self-critical numerology demo: 125 equally-simple formulas match 1/α at the claimed precision, so the α "derivation" is a coincidence, not a result |

See [docs/EXPERIMENTS.md](docs/EXPERIMENTS.md) for detailed documentation of all experiments.

---

## Documentation

| Document | Contents |
|----------|----------|
| [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) | **Start here** — guided walkthrough for newcomers |
| [docs/PHILOSOPHY.md](docs/PHILOSOPHY.md) | Deep dive into Advaita Vedanta and its mapping to physics |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Project structure, design principles, and module relationships |
| [docs/MODULES.md](docs/MODULES.md) | Detailed documentation of every module and class |
| [docs/EXPERIMENTS.md](docs/EXPERIMENTS.md) | All 31 experiments with methodology and results |
| [docs/PREDICTIONS.md](docs/PREDICTIONS.md) | Testable predictions, falsification criteria, and experimental roadmap |
| [docs/ROADMAP.md](docs/ROADMAP.md) | 5 paths from framework to real ToE, with honest status assessment |
| [docs/GLEASON_PROBABILITY_GAP.md](docs/GLEASON_PROBABILITY_GAP.md) | Technical note engaging Kent (2010) and Baker (2007) critiques of Gleason-based Born rule derivations |

---

## Key Results

| Result | Significance | Status |
|--------|-------------|--------|
| **Axiom reduction: 7 → 4** | Gleason's theorem makes Born rule a theorem, not axiom. Advaita has fewer axioms than Copenhagen. | **Established theorem (Gleason 1957), numerically illustrated** (Experiment 18; scope: docs/GLEASON_PROBABILITY_GAP.md) |
| **Fine structure: 0.003% error** | 163-26+π/100 = 137.031 vs 137.036 — Heegner number connection | **Numerology — fails hold-out** (Experiments 22, 31) |
| **IIT-Entanglement: Φ ≤ S** | Validated test (canonical PyPhi Φ; ordering-audit-corrected) **falsifies** the bound — 50 of 51 nonzero-Φ systems violate it, and the raw Φ–S correlation (r≈+0.64) is a connectivity confound (partial r≈−0.07, p=0.29) — nothing residual survives | **Falsified** (validated retest) |
| **2+1D Einstein: R-T = 0.94** | The correlated "curvature" is a smoothed copy of an entropy DEFINED from the energy density | **Withdrawn as evidence — circular by construction** (Experiment 20) |
| **Spacetime from entanglement** | Real MERA: exact S(interval) ≤ ln(χ)·\|min cut\| on the constructed state — **informative at only 1 of the 3 default intervals** (at lengths 2 and 4 the cut equals the length, so the bound reduces to the trivial S ≤ \|A\|·ln2); mutual information → 0 in the product limit | **Reimplemented 2026-08-15** (Experiment 19) |
| **Spacetime as QEC code** | Real [[5,1,3]] code: threshold 2/5 (40%), reconstruction from any 3/5 (60%); 3-erasure provably unrecoverable | **Reimplemented 2026-08-15** (Experiment 21) |
| Bell inequality violated (S = 2√2) | CHSH evaluated **on the supplied state**: |Φ+⟩ → +2√2, separable \|00⟩ → 1.414 (no violation), singlet → −2√2. Standard QM on a state we wrote down — illustrates Tsirelson's bound, not an experimental Bell test | **Illustrative, state-consuming** (Experiment 11) |
| Measurement problem **reframed**, not solved | Total state stays pure; collapse is perspectival. The paper is explicit that the view "does **not** solve the measurement problem (it gives an account of what the appearance of definite outcomes consists in)" — and pure-global/mixed-reduced is a theorem of the formalism shared by *every* no-collapse interpretation, so it cannot favour this one | **Theorem of the formalism, not evidence for this reading**** (Experiment 10) |
| Koide formula (0.6666 vs 0.6667) | Lepton masses have structure — not arbitrary | **Verified** (not derived) |

---

## Honest Limitations

This project is scientifically honest about what it has and hasn't achieved:

- **Tested**: Full test suite (490 tests) covering every module — run with `pytest`
- **Established mathematics, illustrated**: Gleason-based axiom reduction (the theorem is Gleason's; this repo's contribution is numerical illustration — scope caveats in docs/GLEASON_PROBABILITY_GAP.md)
- **Demonstrated**: Measurement-problem dissolution via decoherence + partial trace (perspectival collapse)
- **Withdrawn as evidence (2026 review)**: the 1D/2D/3D Einstein-equation demos (circular — entropy defined from the energy density it is then correlated with) and the Bell "verification" (analytic value; no state consumed). These remain as labeled illustrations.
- **Reimplemented and now computed (2026-08-15)**: the QEC code (real [[5,1,3]]), the MERA (tensors actually contracted), entropic gravity (Verlinde's real derivation), plus two new modules — Gauss–Bonnet on the discrete manifold and the entanglement first law δS = δ⟨K⟩. Criteria were frozen in `REAL_PHYSICS_REIMPLEMENTATION_MEMO.md` before implementation; 22/23 passed and the failure is a visible `xfail`.
- **Falsified (own retest)**: IIT-entanglement bound Φ ≤ S — refuted by a validated (PyPhi) retest; the apparent Φ–S correlation is a connectivity confound (does not survive control)
- **Numerology (own hold-out)**: Fine structure constant at 0.003% via Heegner numbers — fails cross-validation; 125 equally simple formulas do as well (Experiment 31)
- **Verified (not derived)**: Koide formula (0-parameter arithmetic check); cosmological-constant order-of-magnitude comparison
- **Illustrative (definitional)**: ER=EPR identities — the throat–entropy relation is imposed, not derived
- **Not addressed**: Full Standard Model Lagrangian, exact constant derivations

See [docs/ROADMAP.md](docs/ROADMAP.md) for the complete honest status assessment and next steps.

---

## Citation

If you reference this repository or its results, cite the accompanying paper via its concept DOI (always resolves to the latest version):

> Chauhan, R. (2026). *The Cardinality of Experience Is Underdetermined by the Quantum State: A Constructive Case for a Consciousness-Primitive Interpretation.* Zenodo. https://doi.org/10.5281/zenodo.21007975

The version of record for the withdrawn §8 conjecture (Φ ≤ S) and its falsification is preserved in [`reproducibility/phi_s/`](reproducibility/phi_s/).

---

## License

Released under the **MIT License** — see [LICENSE](LICENSE). You may use, modify and redistribute this code, including commercially, provided the copyright notice and permission notice are retained.

The licence covers the **code**. It says nothing about the correctness of the ideas: the code models a metaphysical framework and explores its connections to physics — it does not claim to be a finished physical theory, and several of its explorations have been withdrawn or falsified by the project's own tests (see [docs/PREDICTIONS.md](docs/PREDICTIONS.md)). The accompanying paper is separately available under its own terms via the Zenodo record.

### Third-party components and data

The MIT grant above covers **this repository's code**. Enumerated so the
declaration actually covers its inputs:

| Component | Licence | Note |
|---|---|---|
| numpy, scipy, matplotlib, pytest | BSD-family | declared in `requirements.txt` / `pyproject.toml` |
| **PyPhi 1.2.0** | **GPLv3+** | imported by `predictions/validated_phi.py` and `reproducibility/phi_s/ordering_audit.py`, and **required to regenerate** the §8 Φ values. It is an *optional, separately installed* dependency — no GPL code is distributed here, and the committed analysis path (`reproduce.sh`) needs only numpy + scipy. |
| Tracked data (`reproducibility/phi_s/data/*.csv`, `tests/fixtures/*.json`, `testbed_summary.csv`) and the five tracked PNGs | **CC0 1.0** | released to the public domain, so the frozen §8 inputs can be reused without friction |
| The accompanying paper | separate terms | available via the Zenodo record, not under this licence |

Note on provenance: substantial portions of this repository were written with AI assistance, disclosed in the commit history.

---

*Tat tvam asi* — "that thou art." The Chāndogya Upaniṣad's identity statement, and the phrase this project borrows for its structural-identity claim (§4.3 of the paper). It is quoted here as the object of study, not as a conclusion the code establishes.
