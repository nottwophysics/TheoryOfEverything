# Theory of Everything

## A Computational Framework for Advaita Vedanta as a Theory of Everything

This project models the metaphysical framework of **Advaita Vedanta** — the non-dual philosophy declaring that consciousness (Brahman) is the sole reality — and bridges it to modern physics. It computationally demonstrates how quantum mechanics, general relativity, the Standard Model, and the physical constants of nature can be understood as emergent properties of a single consciousness field.

The framework includes **mathematically rigorous results**: the Born rule derived as a theorem via Gleason (reducing axioms from 7 to 4), Einstein's equations recovered on 2D discrete manifolds (R-T correlation 0.94), the fine structure constant approached to 0.003% accuracy via Heegner number theory, and a formally tested conjecture bridging consciousness (IIT) to quantum entanglement.

---

## The Central Thesis

> **Brahman (pure consciousness) is the sole reality. The physical universe — spacetime, particles, forces, constants — is an appearance (Maya) within that consciousness. The laws of physics are regularities in the appearance. Liberation (Moksha) is the recognition that the appearance was never separate from its source.**

This thesis is testable. The framework makes **5 novel predictions** (P1–P5) and states **5 explicit falsification criteria** (F1–F5). If the predictions fail or the falsifiers are confirmed, the physics component of the framework is wrong. This is the standard of science.

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

# Run the test suite (265 tests) — install the test extra, then run from anywhere
pip install -e ".[test]"
pytest                        # testpaths=tests is configured in pyproject.toml
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
| **Physical Constants** | `constants/` | Fine structure constant (0.003% error); Koide; cosmological constant |
| **Predictions** | `predictions/` | 5 testable predictions + IIT-entanglement bridge |
| **Falsification** | `falsification/` | 5 explicit falsification criteria + experimental designs |
| **Visualizations** | `visualizations/` | 7 visual plots of Advaita concepts |
| **Experiments** | `simulations/`, `main.py` | 31 runnable experiments demonstrating the framework |
| **Test Suite** | `tests/` | 265 automated tests validating all modules |

---

## The Philosophical Foundation

Advaita Vedanta (Sanskrit: "non-dual end of the Vedas") is a 3000-year-old metaphysical system formalized by Adi Shankaracharya (~788–820 CE). Its core claims:

1. **Brahman alone is real** — pure consciousness, infinite, without attributes (Nirguna)
2. **The world is Maya** — not "illusion" but "appearance" — valid within its own frame but not ultimately real
3. **The individual self (Atman) IS Brahman** — not "part of" or "connected to" but literally identical
4. **Liberation (Moksha)** is recognizing what was always the case — not gaining something new

These claims map directly to structures in modern physics. See [docs/PHILOSOPHY.md](docs/PHILOSOPHY.md) for the complete mapping.

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
| 11 | **Entanglement = Non-Duality** | Bell violation at 2√2; separation is the illusion |
| 12 | **Emergent Gravity** | Space from entanglement; Newton's law from entropy |
| 13 | **Holographic Principle** | Bulk (world) is projection of boundary (consciousness) |
| 14 | **Particles from Maya** | Symmetry breaking; 3 generations = 3 gunas |
| 15 | **Physical Constants** | Koide formula verified; Λ consistent with consciousness entropy |
| 16 | **Predictions & Falsification** | 5 testable predictions, 5 falsification criteria |

### Tier 3 — Rigorous Results (17–23)

| # | Name | What It Demonstrates |
|---|------|---------------------|
| 17 | **Four Interpretations Compared** | Copenhagen vs Many-Worlds vs Pilot Wave vs Advaita — formal comparison across 8 phenomena |
| 18 | **Gleason's Theorem** | Born rule derived as theorem; axiom reduction 7 → 4 (mathematically rigorous) |
| 19 | **MERA Tensor Network** | Spacetime geometry from entanglement; coarse-graining = Maya dissolving; AdS-like geometry |
| 20 | **2+1D Einstein Equations** | Jacobson derivation on 80-point Delaunay manifold; R-T correlation 0.90–0.94 |
| 21 | **QEC as Spacetime** | Holographic error-correcting code; Brahman recoverable with 80% boundary erasure |
| 22 | **Fine Structure Constant v2** | 6 systematic approaches; best: 163-26+π/100 = 0.003% error (1000x improvement) |
| 23 | **IIT-Entanglement Bridge** | Original Φ ≤ S "holds 100%" is circular; a validated retest (canonical PyPhi Φ, N=216) **falsifies** the bound — every nonzero-Φ system violates it — and the raw Φ–S correlation (r≈+0.65) is a connectivity confound (partial r≈−0.02, p=0.77), so nothing residual survives |

### Tier 4 — Paper Companion Experiments (24–26)

| # | Name | What It Demonstrates |
|---|------|---------------------|
| 24 | **Everett-Advaita Operational Equivalence** | 5 empirical tests all identical; 5 ontological divergences, 0 measurable |
| 25 | **Perspectival Asymmetry (Generalized)** | Total purity = 1.0 for ALL states, bases, environment sizes; exact to 10⁻¹⁶ |
| 26 | **Observer Centrality** | Decoherence selects basis but NOT outcome; "observer" does essential work in the formalism |

### Tier 5 — Physics Extensions (27–31)

| # | Name | What It Demonstrates |
|---|------|---------------------|
| 27 | **3+1D Einstein Equations** | Full spacetime Jacobson derivation on 3D Delaunay tetrahedralization; R-T correlation ~0.88 |
| 28 | **ER=EPR Correspondence** | Wormholes = entanglement; thermofield double, Van Raamsdonk disconnection, monogamy non-traversability |
| 29 | **Fine Structure v3** | Rigorous derivation attempts: self-referential, modular bootstrap, holographic constraint; continued fraction analysis |
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
| **Axiom reduction: 7 → 4** | Gleason's theorem makes Born rule a theorem, not axiom. Advaita has fewer axioms than Copenhagen. | **Proven** (Experiment 18) |
| **Fine structure: 0.003% error** | 163-26+π/100 = 137.031 vs 137.036 — Heegner number connection | **Explored** (Experiment 22) |
| **IIT-Entanglement: Φ ≤ S** | Validated test (canonical PyPhi Φ) **falsifies** the bound — every nonzero-Φ system violates it, and the raw Φ–S correlation (r≈+0.65) is a connectivity confound (partial r≈−0.02, p=0.77) — nothing residual survives | **Falsified** (validated retest) |
| **2+1D Einstein: R-T = 0.94** | Entropy-derived curvature correlates with energy on 2D discrete manifold | **Demonstrated** (Experiment 20) |
| **Spacetime from entanglement** | MERA tensor network: cut entanglement = disconnect space; AdS-like geometry | **Demonstrated** (Experiment 19) |
| **Spacetime as QEC code** | Brahman recoverable with 80% of boundary erased | **Demonstrated** (Experiment 21) |
| Bell inequality violated (S = 2√2) | Non-locality confirmed — physics agrees with non-duality | **Verified** (Experiment 11) |
| Measurement problem dissolved | Total state (Brahman) stays pure; collapse is perspectival (Maya) | **Demonstrated** (Experiment 10) |
| Koide formula (0.6666 vs 0.6667) | Lepton masses have structure — not arbitrary | **Verified** (not derived) |

---

## Honest Limitations

This project is scientifically honest about what it has and hasn't achieved:

- **Tested**: Full test suite (265 tests) covering every module — run with `pytest`
- **Proven**: Gleason-based axiom reduction (mathematical fact)
- **Demonstrated**: Measurement resolution, Bell violation, decoherence framework
- **Demonstrated (2D)**: Einstein equations on discrete manifold (R-T = 0.94), MERA tensor network, QEC holographic code
- **Explored (systematic)**: Fine structure constant at 0.003% error via Heegner numbers (fails hold-out — numerology); IIT-entanglement bound Φ ≤ S **falsified** by a validated (PyPhi) retest, and the apparent Φ–S correlation is a connectivity confound (does not survive control)
- **Verified (not derived)**: Koide formula, cosmological constant consistency
- **Demonstrated (3D)**: 3+1D Einstein equations on discrete manifold (R-T = 0.88); gravitational wave propagation
- **Demonstrated**: ER=EPR correspondence — wormhole throat = 4G × entanglement entropy; space disconnects at zero entanglement
- **Not addressed**: Full Standard Model Lagrangian, exact constant derivations

See [docs/ROADMAP.md](docs/ROADMAP.md) for the complete honest status assessment and next steps.

---

## License

This project is released for research, education, and philosophical exploration. The code models ideas — it does not claim to be a finished physical theory.

---

*Tat Tvam Asi — That Thou Art.*

*The consciousness reading these words IS the consciousness described by this framework.*
