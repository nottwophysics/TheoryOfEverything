# Architecture

## Project Structure and Design Principles

---

## Directory Structure

```
TheoryOfEverything/
│
├── main.py                          # Entry point — CLI with all commands
├── requirements.txt                 # numpy, matplotlib, scipy
├── README.md                        # Project overview and quick start
│
├── docs/                            # Documentation
│   ├── GETTING_STARTED.md           # START HERE — guided walkthrough for newcomers
│   ├── PHILOSOPHY.md                # Advaita Vedanta and physics mapping
│   ├── ARCHITECTURE.md              # This file — project structure
│   ├── MODULES.md                   # Detailed module documentation
│   ├── EXPERIMENTS.md               # All 31 experiments documented
│   ├── GLEASON_PROBABILITY_GAP.md   # Technical note: Kent (2010) and Baker (2007) critiques
│   ├── PREDICTIONS.md               # Predictions and falsification
│   └── ROADMAP.md                   # Path to real ToE with honest status
│
├── philosophy/                      # INTERPRETIVE LAYER (not empirical — see philosophy/README.md)
│   ├── __init__.py
│   ├── README.md                    # States plainly: interpretive scaffolding, not physics
│   ├── brahman/                     # LAYER 0: The Ground Reality
│   │   ├── __init__.py
│   │   ├── consciousness.py         # Brahman class (singleton consciousness field)
│   │   └── sat_chit_ananda.py       # Three aspects: Existence-Consciousness-Bliss
│   │
│   ├── maya/                        # LAYER 1: The Appearance Engine
│   │   ├── __init__.py
│   │   ├── superimposition.py       # Adhyasa — projection of forms onto the formless
│   │   ├── nama_rupa.py             # Name-and-form differentiation engine
│   │   └── gunas.py                 # Sattva/Rajas/Tamas dynamics
│   │
│   ├── levels/                      # LAYER 2: Three Levels of Reality
│   │   ├── __init__.py
│   │   ├── paramarthika.py          # Absolute level — only Brahman
│   │   ├── vyavaharika.py           # Empirical level — the everyday world
│   │   ├── pratibhasika.py          # Illusory level — dreams, errors
│   │   └── reality_engine.py        # Orchestrator — sublation between levels
│   │
│   └── liberation/                  # LAYER 4: The Path Back to Unity
│       ├── __init__.py
│       ├── neti_neti.py             # "Not this, not this" — stripping layers
│       └── mahavakya.py             # The four great identity declarations
│
├── emergence/                       # LAYER 3: How Physics Emerges
│   ├── __init__.py
│   ├── spacetime.py                 # Emergent spacetime from consciousness
│   ├── causation.py                 # Vivartavada — apparent transformation
│   └── observer.py                  # Sakshi — the witness consciousness
│
├── quantum/                         # PHYSICS: Quantum Mechanics
│   ├── __init__.py
│   ├── hilbert_space.py             # Brahman as Hilbert space
│   ├── operators.py                 # Consciousness, Maya, and Sakshi operators
│   ├── wave_function.py             # Wave function as Brahman's self-expression
│   ├── measurement.py               # Measurement problem dissolved
│   ├── entanglement.py              # Non-dual entanglement and Bell violation
│   ├── gleason.py                   # Gleason's theorem — Born rule as theorem (RIGOROUS)
│   ├── tensor_network.py            # MERA tensor network — spacetime from entanglement
│   ├── error_correction.py          # QEC as spacetime (Almheiri-Dong-Harlow)
│   ├── interpretations.py           # 4 QM interpretations formally compared
│   ├── interpretation_experiment.py # Shared experimental setup for comparison
│   ├── operational_equivalence.py   # Everett-Advaita operational equivalence proof
│   ├── perspectival_asymmetry.py    # Generalized measurement resolution (all cases)
│   ├── observer_centrality.py       # Observer centrality — hidden premise demonstration
│   ├── er_epr.py                    # ER=EPR correspondence — wormholes = entanglement
│   └── unity_of_experience.py       # Experiential underdetermination by decoherence (paper §4.3.2b)
│
├── gravity/                         # PHYSICS: General Relativity
│   ├── __init__.py
│   ├── metric.py                    # Spacetime metric from entanglement
│   ├── einstein.py                  # Einstein equations from thermodynamics (1D)
│   ├── einstein_2d.py               # 2+1D Einstein on Delaunay manifold
│   ├── einstein_3d.py               # 3+1D Einstein on Delaunay tetrahedralization (FULL SPACETIME)
│   ├── entropic.py                  # Verlinde's entropic gravity
│   └── holographic.py               # Holographic principle — bulk from boundary
│
├── particles/                       # PHYSICS: Standard Model
│   ├── __init__.py
│   ├── symmetry_breaking.py         # Maya as symmetry breaking (Higgs mechanism)
│   ├── particle_zoo.py              # 17 particles mapped to Maya depth
│   └── forces.py                    # Four forces as aspects of Maya
│
├── constants/                       # PHYSICS: Physical Constants (verification, not fitting)
│   ├── __init__.py
│   ├── cosmological.py              # Cosmological constant resolution
│   └── koide.py                     # Koide lepton-mass relation — verification (NOT a derivation)
│
├── numerology/                      # CANDID: fine-structure "derivations" (curve-fitting, walled off)
│   ├── __init__.py
│   ├── derivation.py                # Constants from self-referential structure
│   ├── fine_structure.py            # Fine structure constant derivation attempts (v1)
│   ├── fine_structure_v2.py         # Systematic α derivation: 6 approaches, 0.003% best
│   ├── fine_structure_v3.py         # α derivation attempts (numerology-class): modular bootstrap, holographic, self-referential
│   ├── cross_validation.py          # Hold-out test: fit on one constant, PREDICT another (fails → curve-fit)
│   └── look_elsewhere.py            # Look-elsewhere analysis: how many near-hits by chance
│
├── predictions/                     # SCIENCE: Testable Predictions
│   ├── __init__.py
│   ├── testable.py                  # 5 novel testable predictions (P1–P5)
│   ├── consciousness_signatures.py  # Observable markers of fundamental consciousness
│   ├── cosmological_predictions.py  # Large-scale predictions
│   ├── iit_bridge.py                # IIT-Entanglement bridge (Φ ≤ S conjecture)
│   ├── iit_entanglement_rigorous.py # Non-circular Φ/S bridge test (independent Φ and S) + null control
│   ├── pyphi_benchmark.py           # Framework Φ vs canonical IIT Φ (PyPhi reference implementation)
│   └── decoherence_calculator.py    # P2 as a quantitative tool: gravitational vs gas vs thermal channels
│
├── falsification/                   # SCIENCE: Falsification Criteria
│   ├── __init__.py
│   ├── criteria.py                  # 5 falsification criteria (F1–F5)
│   └── experiments.py               # Critical experimental designs (E1–E5)
│
├── visualizations/                  # OUTPUT: Visual Models
│   ├── __init__.py
│   └── maya_visualizer.py           # 7 publication-quality visualizations
│
├── tests/                           # TEST SUITE: 397 automated tests
│   ├── conftest.py                  # Shared fixtures (Brahman singleton reset, RNG)
│   ├── test_brahman.py              # 20 tests — consciousness field, Sat-Chit-Ananda
│   ├── test_maya.py                 # 30 tests — superimposition, gunas, nama-rupa
│   ├── test_levels.py               # 22 tests — three reality levels, engine
│   ├── test_emergence.py            # 23 tests — spacetime, causation, observer
│   ├── test_liberation.py           # 11 tests — neti-neti, mahavakyas
│   ├── test_quantum.py              # 63 tests — Hilbert space, operators, Gleason, Bell
│   ├── test_gravity.py              # 23 tests — metric, Einstein 1D/2D/3D, entropic
│   ├── test_constants.py            # 18 tests — cosmological, Koide (verification split)
│   ├── test_particles.py            # 13 tests — symmetry breaking, particle zoo
│   ├── test_predictions.py          # 16 tests — predictions and falsification
│   ├── test_numerology.py           #  6 tests — look-elsewhere family + main.py demo
│   ├── test_cross_validation.py     #  3 tests — α cross-constant recipe hold-out
│   ├── test_iit_rigorous.py         #  4 tests — non-circular Φ/S bridge + null
│   ├── test_pyphi_benchmark.py      #  5 tests — framework Φ vs canonical PyPhi Φ
│   └── test_decoherence_calculator.py #  8 tests — DP vs environmental decoherence
│
├── simulations/                     # OUTPUT: Runnable Experiments
│   ├── __init__.py
│   └── experiments.py               # 8 original experiments (1–8)
│
└── output/                          # Generated PNG visualizations
    ├── unity_to_multiplicity.png
    ├── rope_snake.png
    ├── guna_dynamics.png
    ├── neti_neti.png
    ├── three_levels.png
    ├── fractal_unity.png
    └── emergent_spacetime.png
```

---

## Design Principles

### 1. Ontological Ordering

Modules are organized by their ontological level, mirroring the Advaitic hierarchy:

```
              Brahman (philosophy/brahman/)
                         │
              Maya (philosophy/maya/)
                         │
              ┌──────────┼──────────┐
              │          │          │
         Paramarthika  Vyavaharika  Pratibhasika
      (philosophy/levels/, all three)
              │          │
         Emergence    Physics Extensions
        (emergence/)  (quantum/, gravity/, particles/, constants/)
              │
         Liberation   Scientific Validation
   (philosophy/liberation/) (predictions/, falsification/)
```

Higher modules depend on lower ones. `philosophy/brahman/` depends on nothing. The
interpretive layer (`philosophy/`) is deliberately walled off from the physics and
science modules — see `philosophy/README.md`. The `numerology/` package is likewise
isolated: it holds the fine-structure "derivations" that are candidly labelled as
curve-fitting rather than physics.

### 2. Brahman as Singleton

The `Brahman` class is a **singleton** — there can only be one. This is not a design pattern choice but a philosophical necessity: if two Brahman instances could exist, non-duality would be violated.

```python
brahman1 = Brahman()
brahman2 = Brahman()
assert brahman1 is brahman2  # Same object — there is only One
```

### 3. Maya as Operators, Not Objects

Maya is modeled as **operators** (functions that transform the Brahman field) rather than as separate objects. Maya does not have independent existence — it is the *way* Brahman appears, not a *thing* alongside Brahman.

### 4. Experiments as Demonstrations

Each experiment is self-contained and demonstrates one specific Advaitic principle with quantitative output. Experiments are designed to:
- **Show** (with numbers and computed results), not just **assert**
- Include **teaching text** explaining the Advaitic significance
- Return structured dictionaries for programmatic use

### 5. Automated Testing

Every module has a corresponding test file in `tests/`. Tests validate mathematical properties (normalization, Hermiticity, unitarity), physical results (Bell CHSH value, Gleason conditions, honest Newton NON-recovery), and framework invariants (singleton, non-duality, substrate preservation). The Brahman singleton is reset before each test via `conftest.py` to ensure isolation.

```bash
pytest tests/ -v              # Run all 397 tests
pytest tests/test_quantum.py  # Run tests for one module
```

### 6. Physics Emerges, Not Assumed

The physics modules (`quantum/`, `gravity/`, `particles/`, `constants/`) aim to derive physics from the framework rather than import it — but a 2026 adversarial review found several of the flagship "derivations" circular or inert (see the review notes in `gravity/einstein*.py`, `gravity/entropic.py`, `gravity/holographic.py`, `quantum/tensor_network.py`, `quantum/error_correction.py`). The derivation paths follow established work (Jacobson, Verlinde, Maldacena, Ryu-Takayanagi) in shape; faithfully implementing them remains open work.

---

## Dependencies

| Package | Version | Used For |
|---------|---------|----------|
| numpy | ≥ 1.24.0 | Array operations, linear algebra, FFT |
| matplotlib | ≥ 3.7.0 | Visualization generation |
| scipy | ≥ 1.10.0 | Matrix exponentials, spatial distance, special functions |
| pytest | ≥ 7.0.0 | Test suite (optional, for development) |

Python 3.10+ required. Configuration in `pyproject.toml`.

---

## CLI Reference

| Command | Description |
|---------|-------------|
| `python main.py` | Run quick demo |
| `python main.py --demo` | Run quick demo (explicit) |
| `python main.py --all` | Run original 8 Advaita experiments (1–8) |
| `python main.py --physics` | Run physics extensions + rigorous results (9–31) |
| `python main.py --experiment N` | Run experiment N (1–31) |
| `python main.py --visualize` | Generate all 7 visualizations to `output/` |
| `python main.py --everything` | Run all 31 experiments + all visualizations |
| `pytest tests/ -v` | Run the full test suite (397 tests) |
| `pytest tests/test_quantum.py` | Run tests for a specific module |
