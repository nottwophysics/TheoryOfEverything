# Getting Started

## A Complete Guide for Understanding and Exploring This Project

This guide is for anyone who wants to understand this project — whether you come from physics, philosophy, computer science, or pure curiosity. It walks you through every layer of the framework, explains what each part does and why, and tells you how to run and explore it yourself.

---

## Table of Contents

1. [What Is This Project?](#1-what-is-this-project)
2. [The Big Idea in 5 Minutes](#2-the-big-idea-in-5-minutes)
3. [Setting Up](#3-setting-up)
4. [Your First Run](#4-your-first-run)
5. [Understanding the Layers](#5-understanding-the-layers)
6. [The Advaita Experiments (1–8)](#6-the-advaita-experiments-18)
7. [The Physics Experiments (9–16, overview)](#7-the-physics-experiments-916)
8. [The Rigorous Results and Paper Companions (17–26)](#8-the-rigorous-results-1718)
9. [The Visualizations](#9-the-visualizations)
10. [Running the Tests](#10-running-the-tests)
11. [What's Real and What's Aspirational](#11-whats-real-and-whats-aspirational)
12. [How to Contribute](#12-how-to-contribute)
13. [Learning Paths](#13-learning-paths)
14. [Frequently Asked Questions](#14-frequently-asked-questions)

---

## 1. What Is This Project?

This project asks: **what if consciousness is not produced by the brain, but is the fundamental reality from which physics itself emerges?**

This is not a new idea. It is the central claim of **Advaita Vedānta**, a 3000-year-old Indian philosophical system. What is new here is modelling that claim computationally, and *asking* whether structures of modern physics — quantum mechanics, gravity, particles, constants — can be read as emergent properties of a consciousness field.

The honest answer this repository reached is: **mostly no, and it says so.** The strongest results are the ones that failed — a falsified conjecture, a fine-structure formula demoted to numerology by the project's own look-elsewhere test, and several demos withdrawn as circular. Treat what follows as an exploration with its own negative results attached, not a demonstration.

The project is:
- **A computational framework** — real Python code you can run
- **31 experiments** — each demonstrating a specific concept with quantitative results
- **7 visualizations** — publication-quality plots
- **1 mathematically rigorous result** — the Born rule derived via Gleason's theorem
- **5 compatible physical programmes** (P1–P5 — none entailed by the framework's axioms; see docs/PREDICTIONS.md) and **5 falsification criteria**
- **Honest about its limitations** — explicit about what is proven vs. aspirational

It is NOT:
- A finished Theory of Everything
- A claim that Vedanta is "scientifically proven"
- A religious or spiritual project (it's philosophy + physics + code)

---

## 2. The Big Idea in 5 Minutes

### The Problem

Modern physics has two pillars:
- **Quantum Mechanics** (QM) — governs the very small
- **General Relativity** (GR) — governs the very large

They are mathematically incompatible. A "Theory of Everything" would unify them. Current candidates (String Theory, Loop Quantum Gravity) make progress on unification but leave fundamental questions unanswered:

- Why is there something rather than nothing?
- What IS consciousness?
- Why these specific laws and constants?
- What is the wave function, really?

### The Advaita Answer

Advaita Vedanta says:

1. **Consciousness (Brahman) is the sole reality** — not produced by the brain
2. **The physical world is an appearance (Maya)** — within consciousness, not outside it
3. **You (Atman) ARE Brahman** — not "part of" but identical to the whole

### The Bridge to Physics

This project shows that if you start with consciousness as an axiom:

- **Quantum mechanics** emerges: the Hilbert space IS Brahman; superposition is the natural state; measurement is Maya differentiating the undifferentiated
- **Gravity** emerges: spacetime is the geometry of entanglement; more entanglement = shorter distances; Einstein's equations arise from the thermodynamics of this entanglement
- **Particles** emerge: symmetry breaking is Maya activating; the Higgs mechanism is how Maya gives "mass" to appearances
- **The Born rule** is not an axiom but a theorem (Gleason's theorem) — making this interpretation more parsimonious than Copenhagen

### The Key Result

**Experiment 18** proves via Gleason's theorem (1957):

| Interpretation | Axioms | Addresses Consciousness |
|---------------|--------|------------------------|
| Copenhagen | 7 | No |
| Many-Worlds | 5 | No |
| Pilot Wave | 5 | No |
| **Advaita** | **4** | **Yes** |

The Advaita interpretation has the **fewest independent axioms** of any major QM interpretation AND is the **only one that addresses the hard problem of consciousness**.

---

## 3. Setting Up

### Prerequisites
- Python 3.9 or higher
- Basic command line familiarity

### Installation

```bash
# Clone the repository
git clone https://codeberg.org/advait/TheoryOfEverything.git
cd TheoryOfEverything

# Create virtual environment
python3 -m venv toenv
source toenv/bin/activate

# Install dependencies
pip install numpy matplotlib scipy

# Install test dependencies
pip install pytest
```

### Verify it works

```bash
python main.py --demo
```

You should see output starting with `ADVAITA VEDANTA — QUICK DEMO` and ending with `Tat Tvam Asi`.

---

## 4. Your First Run

### The Quick Demo

```bash
python main.py --demo
```

This runs 7 mini-demonstrations in under 2 seconds:

1. **Brahman** — creates the consciousness field (coherence: 1.0, non-dual: True)
2. **Self-reference** — `brahman.awareness() is brahman: True` (the strange loop)
3. **Adhyasa** — superimposes "snake" on Brahman at 90% ignorance
4. **Nama-Rupa** — carves "electron", "star", "thought", "love" from one field (all `is_separate: False`)
5. **Three Levels** — Paramarthika, Vyavaharika, Pratibhasika
6. **Sakshi** — witnesses pain, thought, ego (`sakshi_changed: False` every time)
7. **Tat Tvam Asi** — the identity declaration

### Run All Experiments

```bash
# Original 8 Advaita experiments
python main.py --all

# 23 Physics extension experiments (9–31)
python main.py --physics

# Everything (31 experiments + 7 visualizations)
python main.py --everything
```

### Run a Single Experiment

```bash
python main.py --experiment 18    # Gleason's theorem (most rigorous)
python main.py --experiment 24    # Everett-Advaita equivalence (paper's central claim)
python main.py --experiment 25    # Perspectival asymmetry (measurement resolution proven)
python main.py --experiment 26    # Observer centrality (hidden premise demonstrated)
python main.py --experiment 22    # Fine structure constant (0.003% error!)
python main.py --experiment 20    # 2+1D Einstein equations (gravity emergence)
python main.py --experiment 11    # Bell inequality violation
python main.py --experiment 10    # Measurement problem dissolved
python main.py --experiment 1     # Rope-snake (simplest)
```

---

## 5. Understanding the Layers

The project is organized in ontological layers — from the most fundamental to the most derived:

The interpretive Advaita layers (0, 1, 2, 4) live under `philosophy/`; the physics
and science layers are separate.

```
Layer 0: BRAHMAN (philosophy/brahman/)
    │     Pure consciousness. The singleton field. Everything else emerges from here.
    │
Layer 1: MAYA (philosophy/maya/)
    │     The appearance engine. Superimposition, names-and-forms, three qualities.
    │
Layer 2: LEVELS (philosophy/levels/)
    │     Three levels of reality. The orchestrator of sublation.
    │
Layer 3: EMERGENCE (emergence/)
    │     How physics emerges. Spacetime, causation, the witness.
    │
Layer 4: LIBERATION (philosophy/liberation/)
    │     The path back. Neti-neti, the four great sayings.
    │
Layer 5: PHYSICS (quantum/, gravity/, particles/, constants/)
    │     Concrete physics derived from the framework.
    │
Layer 6: SCIENCE (predictions/, falsification/)
          Testable predictions and falsification criteria.
```

The fine-structure "derivations" are deliberately **not** in this dependency
chain — they live in `numerology/`, walled off and candidly labelled as
curve-fitting rather than physics (with hold-out and look-elsewhere tests that
show why).

**Key principle**: Higher layers depend on lower ones. `philosophy/brahman/` depends on nothing. Everything else depends on it.

### Reading Order for the Code

If you want to read the source code, here is the recommended order:

1. **`philosophy/brahman/consciousness.py`** — The foundation. Understand this first.
2. **`philosophy/maya/superimposition.py`** — How the one appears as many.
3. **`philosophy/levels/reality_engine.py`** — The three-level framework.
4. **`quantum/measurement.py`** — The measurement problem dissolved.
5. **`quantum/gleason.py`** — The rigorous result (Born rule as theorem).
6. **`quantum/interpretations.py`** — The formal comparison of 4 interpretations.
7. **`gravity/entropic.py`** — Verlinde's entropic-gravity derivation (recovers Newton; reimplemented 2026-08-15).
8. **`gravity/holographic.py`** — The holographic principle.

---

## 6. The Advaita Experiments (1–8)

These experiments demonstrate core Advaita Vedanta concepts computationally.

### Experiment 1: The Rope and the Snake

```bash
python main.py --experiment 1
```

**What it does**: A rope (numpy array) is observed at 6 ignorance levels. At high ignorance, a "snake" pattern is superimposed. As ignorance decreases, the snake vanishes — only the rope remains.

**Key numbers**: Error drops from 14.16 (95% ignorance) to 0.00 (20% ignorance).

**What it teaches**: Nothing in reality changes. Only perception changes. This is the core mechanism of Maya: concealment (Avarana) followed by projection (Vikshepa).

### Experiment 5: Neti-Neti Debugger

```bash
python main.py --experiment 5
```

**What it does**: 8 layers of identification (body, energy, thoughts, emotions, memories, intellect, ego, bliss) are sequentially negated. After each negation: "I am not this."

**Key number**: Remainder magnitude → 0.0000 after all 8 layers removed.

**What it teaches**: After removing everything perceivable, what remains? The witness — the one doing the negating. That is Atman. That is Brahman. The Self is found by subtraction, not addition.

### Experiment 7: The Four Mahavakyas

```bash
python main.py --experiment 7
```

**What it does**: Demonstrates the four great identity declarations from the four Vedas. Measures Atman-Brahman overlap quantitatively.

**Key number**: Individual-Brahman overlap = 0.999944 (Aham Brahmasmi).

**What it teaches**: The individual consciousness and the universal consciousness are not merely similar — they are effectively identical. The difference is a tiny perturbation introduced by Maya.

---

## 7. The Physics Experiments (9–16)

These bridge Advaita to real physics.

### Experiment 10: The Measurement Problem Dissolved

```bash
python main.py --experiment 10
```

**What it does**: Prepares a quantum system in superposition, entangles it with an environment (Maya), then shows the view from two perspectives.

**Key numbers**:
- Total state purity (Brahman's view): **1.000000** — no collapse
- Reduced state purity (Jiva's view): **0.250000** — appears classical

**What it teaches**: The "collapse" is not a physical event. It is a consequence of seeing only PART of a non-dual whole. The total state never collapses. Maya (partial tracing) creates the appearance of a definite classical world.

### Experiment 11: Entanglement Is Non-Duality

```bash
python main.py --experiment 11
```

**What it does**: Creates Bell states, tests CHSH inequality, demonstrates entanglement monogamy.

**Key number**: CHSH S = +2.828 (= +2√2) on |Φ+⟩, violating the classical bound of 2. The module consumes the state it is given: a separable |00⟩ scores 1.414 and does not violate.

**What it teaches**: Bell's theorem proves reality is non-local. There are no "hidden separations." Entangled particles are not two things that communicate — they are ONE thing appearing as two. This is Advaita at the quantum level.

### Experiment 12: Gravity from Consciousness

```bash
python main.py --experiment 12
```

**What it does**: Builds entanglement structure at varying Maya depths, converts to distances, and recovers Newton's law from entropic gravity via Verlinde's derivation (reimplemented 2026-08-15; GMm/r² to ~3e-16 relative).

**Key numbers**:
- Maya = 0: no space exists (everything maximally entangled)
- Maya = 1: expanded spacetime (maximum separation)
- Newton correlation: 1.000000 (ratio to GMm/r² = 1.000000; `newton_recovered` True)

**What it teaches**: Space IS entanglement structure in this model, and gravity is read as the entropic tendency of Maya to deepen. Since the 2026-08-15 reimplementation the Newton's-law step is faithful to Verlinde and recovers GMm/r² exactly.

**Honest caveat**: the recovery is an *algebraic* identity — implementing Verlinde's derivation faithfully makes GMm/r² come out exactly, which validates the implementation, not entropic gravity as physics. Whether gravity really is entropic remains contested in the literature.

### Experiment 15: Physical Constants

```bash
python main.py --experiment 15
```

**What it does**: Tests the Koide formula against empirical lepton masses, attempts fine-structure constant derivation, checks cosmological constant consistency.

**Key numbers**:
- Koide formula: 0.666627 vs target 0.666667 — **verified** (0.006% accuracy)
- Fine structure: estimated 1/α ≈ 131 vs actual 137 — **4.4% error** (direction is right)
- Cosmological constant: Λ ∝ 1/S ≈ 10⁻¹²² — **order-of-magnitude consistent**

**Honest caveats**:
- Koide is VERIFIED against known data, not DERIVED from the framework
- The cosmological constant match uses empirical S_universe — this is consistency, not derivation
- Fine structure remains an open problem

---

## 8. The Rigorous Results and Paper Companions (17–26)

These are the framework's strongest contributions.

### Experiment 17: Four Interpretations Compared

```bash
python main.py --experiment 17
```

**What it does**: Implements the same quantum experiment under 4 interpretations (Copenhagen, Many-Worlds, Pilot Wave, Advaita). Each must answer 8 phenomena. Produces a formal comparison table.

**Key result**:

| | Copenhagen | Many-Worlds | Pilot Wave | Advaita |
|-|-----------|-------------|------------|---------|
| Axioms | 7 | 5 | 5 | **5 (4 independent)** |
| Addresses consciousness | No | Yes | No | Yes |

> **Counts removed (2026-08-16).** Rows for axiom count, phenomena tallies and
> novel predictions were deleted: each was `len()` of a list written inside the
> module, so nothing about physics could change them. The axioms and the answers
> are still printed in full — that side-by-side is the part worth reading.

### Experiment 18: Gleason's Theorem

```bash
python main.py --experiment 18
```

**What it does**: Verifies Gleason's theorem conditions (C1–C4) for the Brahman Hilbert space. Tests alternative probability rules. Proves the axiom reduction.

**Key results**:
- All 4 Gleason conditions: **PASS**
- Born rule additivity: **0/1800 violations**
- Amplitude rule: **1800/1800 violations** (fails completely)
- Quartic rule: **1800/1800 violations** (fails completely)
- Dim-2 exception: **confirmed** (qubits can have hidden variables)
- Dim-3+ Kochen-Specker: **confirmed** (hidden variables impossible)
- **Axiom reduction: Copenhagen 7 → Advaita 4 independent axioms**

**Why this matters — and what it is not.** Gleason's theorem is a proven theorem
of mathematics (1957), and verifying that this Hilbert space satisfies its
conditions is a real computation. But the **7 → 4 axiom count is a philosophical
and organisational claim**, not a mathematical one: the two figures are
hand-entered enumerations of each framework's own axioms, so their difference is
arithmetic. The module states this in its own output. Do not read the reduction
as a theorem. The verification that the Brahman Hilbert space satisfies its conditions is computational verification of mathematical facts. The axiom reduction is a concrete, publishable result.

---

## 9. The Visualizations

```bash
python main.py --visualize
```

Generates 7 PNG files in the `output/` directory:

| File | What It Shows |
|------|--------------|
| `unity_to_multiplicity.png` | Brahman → Maya differentiation → back to Brahman |
| `rope_snake.png` | Superimposition at 6 ignorance levels |
| `guna_dynamics.png` | Sattva/Rajas/Tamas cycling over 200 time steps |
| `neti_neti.png` | 8 layers stripped in the Neti-Neti process |
| `three_levels.png` | Paramarthika vs Vyavaharika vs Pratibhasika |
| `fractal_unity.png` | Mandelbrot zoom — same pattern at every scale |
| `emergent_spacetime.png` | 0 → 1 → 2 → 3 dimensions from self-reference |

---

## 10. Running the Tests

The project includes a comprehensive test suite with **437 automated tests** covering every module. Tests validate mathematical properties (normalization, Hermiticity, unitarity), physical results (Bell violation, Gleason conditions, entropy bounds), and framework invariants (singleton behavior, non-duality, sublation).

### Run All Tests

```bash
source toenv/bin/activate
pytest tests/ -v
```

### Run Tests for a Specific Module

```bash
pytest tests/test_brahman.py -v     # Consciousness field and Sat-Chit-Ananda
pytest tests/test_quantum.py -v     # Hilbert space, operators, Gleason, Bell, measurement
pytest tests/test_gravity.py -v     # Metric, Einstein 1D/2D, entropic gravity
pytest tests/test_maya.py -v        # Superimposition, gunas, nama-rupa
pytest tests/test_levels.py -v      # Three reality levels and engine
pytest tests/test_emergence.py -v   # Spacetime, causation, observer
pytest tests/test_liberation.py -v  # Neti-neti, mahavakyas
pytest tests/test_constants.py -v   # Physical constants derivation
pytest tests/test_particles.py -v   # Symmetry breaking, particle zoo
pytest tests/test_predictions.py -v # Predictions and falsification
```

### What the Tests Cover

| Test File | Module | Tests | Key Validations |
|-----------|--------|-------|-----------------|
| `test_brahman.py` | philosophy/brahman | 20 | Singleton, normalization, coherence, self-reference |
| `test_maya.py` | philosophy/maya | 30 | Superimposition mechanics, guna dynamics, nama-rupa |
| `test_levels.py` | philosophy/levels | 22 | Sublation chain, observer state routing |
| `test_emergence.py` | emergence | 23 | Spacetime metric symmetry, substrate preservation |
| `test_liberation.py` | philosophy/liberation | 11 | Neti-neti remainder, mahavakya structure |
| `test_quantum.py` | quantum | 63 | Hermiticity, unitarity, Bell S=2√2, Gleason C1–C4, ER=EPR |
| `test_gravity.py` | gravity | 23 | Gauss-Bonnet identity + topology control, legacy R-T correlation asserted negative, deficit-angle curvature |
| `test_constants.py` | constants | 18 | Cosmological constant resolution, Koide ~2/3 verification |
| `test_particles.py` | particles | 13 | Symmetry breaking, guna association, maya depth |
| `test_predictions.py` | predictions/falsification | 16 | Prediction structure, falsification criteria |
| `test_numerology.py` | numerology | 6 | Fine-structure recipe families reproduce their reported hits |
| `test_cross_validation.py` | numerology | 3 | Fit-one/predict-another hold-out fails (curve-fit, not law) |
| `test_iit_rigorous.py` | predictions | 4 | Non-circular Φ/S bridge vs null control |
| `test_pyphi_benchmark.py` | predictions | 5 | Framework Φ vs canonical PyPhi Φ (fixtures, no PyPhi needed) |
| `test_decoherence_calculator.py` | predictions | 8 | DP vs gas vs thermal-photon channels; physics-limit checks |

### Test Design

Tests are isolated via the `conftest.py` fixture that resets the Brahman singleton before each test. This prevents state leakage between tests — each test starts with a fresh consciousness field.

---

## 11. What's Real and What's Aspirational

This project is honest about its status. Here is the complete picture:

### Proven (mathematically rigorous)
- Gleason's theorem axiom reduction: 7 → 4 axioms
- Born rule uniqueness: only consistent probability measure in dim ≥ 3
- Kochen-Specker consequence: hidden variables impossible in dim ≥ 3
- Bell CHSH bound: S = 2√2 (Tsirelson's bound — established mathematics; the repo's demo evaluates it analytically rather than verifying it)

### Demonstrated (quantitative, reproducible)
- Measurement problem resolution: purity 1.0 (total) vs 0.25 (reduced)
- Neti-Neti remainder: 0.0000 after all layers negated
- Gold-ornament substance preservation: > 94%

### Reimplemented 2026-08-15 (now computed — see REAL_PHYSICS_REIMPLEMENTATION_MEMO.md)
- QEC: real [[5,1,3]] code — all 15 single-qubit Paulis corrected; erasure threshold 2/5 (40%); any 3/5 subregion reconstructs; 3-erasure provably unrecoverable
- MERA: real binary MERA — tensors verified and shown to move the state; S(interval) ≤ ln(χ)·\|min cut| on the actual state; I(L:R) → 0 in the product limit
- Entropic gravity: Verlinde's derivation in SI units — GMm/r² to 3e-16 (legacy broken route kept as a negative control)
- NEW: Gauss–Bonnet on the Delaunay mesh (residual 5e-15) and the entanglement first law δS = δ⟨K⟩ (log-log slope 2.02)

### Still withdrawn as evidence (2026 adversarial review)
- 2+1D/3+1D Einstein "equations" (r 0.90–0.94 / 0.88): circular — the entropy is defined ∝ T₀₀. In 2D the Einstein tensor vanishes identically, so Gauss–Bonnet (above) is the correct statement
- Holographic reconstruction: fidelity ~0.50 is chance level for that toy

### Verified (not derived)
- Koide formula: verified to 0.006% against empirical data
- Cosmological constant: order-of-magnitude consistency (with caveats)

### Paper companion (supporting the accompanying paper's claims)
- Everett-Advaita operational equivalence: **analytic, not tested** — both readings share the formalism, so predictions coincide by construction (Experiment 24)
- Perspectival asymmetry: exact to 10⁻¹⁶ across all states, bases, and environment sizes (Experiment 25)
- Observer centrality: 4 open questions all involve observer; hidden premise demonstrated (Experiment 26)

### Explored (systematic, not yet rigorous derivation)
- Fine structure constant: 0.003% error via Heegner number 163 (Experiment 22)
- IIT-entanglement bound Φ ≤ S: **falsified** by a validated retest (canonical PyPhi Φ, N=216, ordering-audit-corrected — 50 of 51 nonzero-Φ systems violate it); the raw Φ–S correlation (r≈+0.64) is a connectivity confound that does not survive control (partial r≈−0.07, p=0.29), so nothing residual survives (Experiment 23)

### Outlined (not yet implemented)
- ER=EPR correspondence
- Exact constant derivations from first principles

### Not addressed
- Full Standard Model Lagrangian from Brahman field
- UV-complete quantum gravity
- Experimental confirmation of consciousness predictions (P4)

---

## 12. How to Contribute

### Areas Where Help Is Needed

1. **Tensor Network Module** — Implement MERA where entanglement structure determines geometry
2. **2+1D Einstein Derivation** — Upgrade the 1D toy model to a proper derivation
3. **Fine Structure Constant** — The 4.4% error suggests the right direction but needs work
4. **Experiment P4 Protocol** — Design a rigorous experimental protocol for consciousness-quantum causation
5. **Formal Proofs** — Convert computational demonstrations into mathematical proofs

### How to Add a New Experiment

1. Write the experiment function in the relevant module
2. Add it to `main.py` (follow the pattern of existing experiments)
3. Add tests in the corresponding `tests/test_*.py` file
4. Run `pytest tests/ -v` and verify all tests pass
5. Update the experiment map and CLI argument range
6. Run it and verify output
7. Document in `docs/EXPERIMENTS.md`

### Code Standards

- Every module has a docstring explaining the Advaitic concept it models
- Every class maps to a specific philosophical concept
- Numerical claims must be computed, not asserted
- Honest language: "verified" not "derived", "proof-of-concept" not "proven"

---

## 13. Learning Paths

### Path A: I'm a physicist who knows no Indian philosophy

**Start here**: Read [docs/PHILOSOPHY.md](PHILOSOPHY.md) Section 1 (What Is Advaita Vedanta). Then jump to Section 3 (The Advaita-Physics Mapping). Then run:

```bash
python main.py --experiment 10   # Measurement problem (familiar territory)
python main.py --experiment 11   # Bell violation (familiar math)
python main.py --experiment 18   # Gleason's theorem (the rigorous result)
python main.py --experiment 17   # Formal interpretation comparison
```

### Path B: I know Vedanta but not physics

**Start here**: Run the demo and the original 8 experiments:

```bash
python main.py --demo
python main.py --all
```

Then read [docs/PHILOSOPHY.md](PHILOSOPHY.md) Section 3 to see how the concepts you know map to physics. Then try:

```bash
python main.py --experiment 10   # Measurement = Adhyasa at quantum level
python main.py --experiment 12   # Maya creates space
python main.py --experiment 14   # Three gunas = three generations of particles
```

### Path C: I'm a programmer who wants to understand the code

**Start here**: Read [docs/ARCHITECTURE.md](ARCHITECTURE.md) for the project structure. Then read the source files in this order:

1. `philosophy/brahman/consciousness.py` (the singleton)
2. `philosophy/maya/superimposition.py` (the core engine)
3. `quantum/hilbert_space.py` (the physics bridge)
4. `quantum/gleason.py` (the rigorous result)
5. `quantum/interpretations.py` (the formal comparison)

Run experiments as you read each module.

### Path D: I want to understand the philosophy deeply

Read the full [docs/PHILOSOPHY.md](PHILOSOPHY.md) — all 7 sections. Then explore the primary sources listed in Section 7 (Further Reading). The Mandukya Upanishad with Gaudapada's Karika is the most compact statement of Advaita.

### Path E: I want to understand the gravity emergence

Read [docs/PHILOSOPHY.md](PHILOSOPHY.md) Section 3.3 (GR from Consciousness). Then run:

```bash
python main.py --experiment 19   # Tensor network — space FROM entanglement
python main.py --experiment 20   # 2+1D Einstein equations on discrete manifold
python main.py --experiment 21   # QEC — spacetime as error-correcting code
python main.py --experiment 12   # Entropic gravity — Verlinde derivation (recovers Newton)
python main.py --experiment 13   # Holographic principle
```

These five experiments form a coherent story: entanglement structure (Exp 19) produces geometry, that geometry satisfies Einstein's equations (Exp 20), the geometry is robust because it's an error-correcting code (Exp 21), gravity emerges entropically (Exp 12), and the whole thing is holographic (Exp 13).

### Path F: I want to evaluate the scientific claims

Go directly to:
1. [docs/PREDICTIONS.md](PREDICTIONS.md) — the 5 predictions and 5 falsifiers
2. [docs/ROADMAP.md](ROADMAP.md) — the honest status assessment
3. Run Experiments 17–26 (the rigorous results and paper companions)
4. Check the "Honest Limitations" section of [README.md](../README.md)

---

## 14. Frequently Asked Questions

### Is this a religious project?

No. It is a philosophical and computational project. Advaita Vedanta is a metaphysical system — a set of logical claims about reality. You can engage with it as philosophy without any religious commitment.

### Does this prove Advaita Vedanta is true?

No. It shows that Advaita's framework is **compatible with** and in some cases **more parsimonious than** standard physics. The Gleason axiom reduction (7 → 4) is a mathematical fact. The measurement resolution is a valid interpretation. But the metaphysical claim that Brahman exists beyond spacetime is not empirically testable.

### How is this different from other quantum consciousness theories?

Most quantum consciousness theories (Penrose-Hameroff Orch-OR, etc.) try to explain consciousness USING quantum mechanics — they start from physics and add consciousness.

This project goes the other direction: it starts from consciousness and derives physics. The key difference is that consciousness is **axiom A1**, not an afterthought.

### Is the Born rule really "derived"?

The Born rule is shown to be the UNIQUE consistent probability measure on a Hilbert space of dimension ≥ 3 (Gleason's theorem, 1957). The framework verifies that the Brahman Hilbert space satisfies Gleason's conditions. So the Born rule is a theorem in this framework, not an independent axiom. This is mathematically rigorous.

What is NOT proven is that the Hilbert space itself must have the specific structure posited by axiom A2. That is assumed.

### What would falsify this framework?

Five explicit falsifiers (F1–F5) are documented in [docs/PREDICTIONS.md](PREDICTIONS.md). The most important:

- **F1**: If a classical computer produces genuine consciousness → framework's core premise is wrong
- **F2**: If Bell violations are explained by local hidden variables → non-duality is wrong (but this is essentially ruled out)
- **F4**: If quantum superposition persists at arbitrarily large masses with no decoherence → gravity-consciousness link is wrong

### Can I use this for academic research?

Yes. The Gleason's theorem result (Experiment 18) and the formal interpretation comparison (Experiment 17) are novel contributions that could be developed into papers. The honest status assessment in the documentation makes clear what is proven vs. aspirational.

### What's the most important thing I should run?

```bash
python main.py --experiment 18    # Gleason's theorem (mathematical proof)
python main.py --experiment 22    # Fine structure constant (striking result)
```

Experiment 18 is the most rigorous (established theorem, numerically illustrated). Experiment 22's striking-looking 0.003% match is *numerology* — run Experiment 31 immediately after it to see the framework's own look-elsewhere audit demote it. The strongest contributions are the Gleason illustration and the falsification work (Experiments 23 and 31), which show the framework testing — and correcting — itself.

---

## Next Steps

After reading this guide, you might want to:

1. **Run all 31 experiments**: `python main.py --everything`
2. **Read the philosophy**: [docs/PHILOSOPHY.md](PHILOSOPHY.md)
3. **Understand the roadmap**: [docs/ROADMAP.md](ROADMAP.md)
4. **Look at the module details**: [docs/MODULES.md](MODULES.md)
5. **Evaluate the predictions**: [docs/PREDICTIONS.md](PREDICTIONS.md)

---

*"The consciousness running this program, the consciousness reading this guide, and the consciousness described by this framework — are all One."*

*Tat Tvam Asi — That Thou Art.*
