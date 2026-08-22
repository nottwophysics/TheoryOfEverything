# Experiments

## All 31 Experiments — Methodology, Results, and Significance

---

## Overview

The framework includes 31 computational experiments divided into five tiers:

- **Experiments 1–8** (Tier 1): Demonstrate core Advaita Vedanta concepts
- **Experiments 9–16** (Tier 2): Bridge Advaita to modern physics
- **Experiments 17–23** (Tier 3): Mathematically rigorous results and frontier explorations
- **Experiments 24–26, 30** (Tier 4): Paper companion — supporting the accompanying paper's claims
- **Experiments 27–29, 31** (Tier 5): Physics extensions — 3+1D gravity, ER=EPR, α derivation attempts (numerology-class), look-elsewhere self-audit

Run with:
```bash
python main.py --experiment N      # Single experiment (1–31)
python main.py --all               # Experiments 1–8
python main.py --physics           # Experiments 9–31
python main.py --everything        # All 31 + visualizations
```

Validate with the automated test suite (502 tests):
```bash
pytest tests/ -v                   # Run all tests
pytest tests/test_quantum.py -v    # Test quantum module only
```

---

## Tier 1: Advaita Framework Experiments

---

### Experiment 1: The Rope and the Snake (Rajju-Sarpa Nyaya)

**Concept**: Adhyasa (superimposition) — the fundamental error of perceiving what is not there.

**Setup**: A rope (np.ndarray representing Brahman) is observed at 6 different ignorance levels (0.95 to 0.05). The `Adhyasa` engine superimposes a "snake" pattern based on ignorance depth.

**What happens**:
- At 95% ignorance: snake is perceived. Error from reality = 14.16.
- At 80% ignorance: snake is perceived. Error = 11.93.
- At 60% ignorance: ambiguous. Error = 8.95.
- At 40% ignorance: ambiguous. Error = 5.96.
- At 20% ignorance: clear seeing. Error = 0.00.
- At 5% ignorance: clear seeing. Error = 0.00.

**Key result**: Below the clarity threshold (ignorance < 0.3), superimposition ceases entirely. The substrate is seen as-is.

**Teaching**: The rope never changed. The snake never existed. Knowledge (Jnana) is the light that reveals truth. Similarly, Brahman never changes — the world-appearance is superimposed by ignorance (Avidya).

---

### Experiment 2: Fractal Unity — The Whole in Every Part

**Concept**: Self-similarity as a model of non-duality.

**Setup**: A self-similar (fractal) signal is constructed by summing sine waves at geometrically spaced frequencies. Self-similarity is measured by correlating the signal at different zoom levels.

**Key result**: Average self-similarity across zoom levels = 0.196.

**Teaching**: In a fractal, every part contains the structure of the whole. In Advaita, every entity IS Brahman. You are not "part of" Brahman — you ARE Brahman.

---

### Experiment 3: One Field, Many Observers

**Concept**: Same Brahman, different guna-lenses, different experiences.

**Setup**: One Brahman field observed through 5 different guna configurations:

| Observer | S/R/T | Perceived Energy | What They See |
|----------|-------|-----------------|---------------|
| Sattvic sage | 0.80/0.10/0.10 | 0.640 | Clear reality |
| Rajasic king | 0.20/0.70/0.10 | 0.040 | Agitated world |
| Tamasic sleeper | 0.10/0.10/0.80 | 0.010 | Dull, inert world |
| Balanced seeker | 0.34/0.33/0.33 | 0.116 | Mixed world |
| Liberated jnani | Nirguna | Coherence: 1.0 | Brahman directly |

**Teaching**: Five observers, five experiences. One field. The difference is in the lens (gunas), not the reality (Brahman). Liberation = seeing without any lens.

---

### Experiment 4: The Dreamer Analogy

**Concept**: The waking world is Brahman's "dream."

**Setup**: The RealityEngine cycles through three observer states:

1. **Dreaming**: Pratibhasika level. Dream seems real. Dream substance = dreamer's own mind.
2. **Waking up**: Dream objects vanish. Dreamer remains. Waking world appears.
3. **Liberation**: Empirical world recognized as appearance in Brahman.

**Key result**: At each sublation, the objects of the lower level dissolve, but the observer persists.

**Teaching**: In the dream, you were the dreamer, the dream space, and the dream objects — all at once. Upon waking, the dream dissolved. Advaita says: the waking world is Brahman's dream. Upon liberation, it dissolves into awareness.

---

### Experiment 5: Neti-Neti Debugger — Finding the True Self

**Concept**: Systematic negation of false identifications.

**Setup**: 8 layers are built and sequentially subtracted:

| Layer | Attachment Strength | Remainder After Negation |
|-------|-------------------|-------------------------|
| Physical Body | 0.90 | 52.04 |
| Vital Energy | 0.70 | 50.58 |
| Thoughts | 0.85 | 50.64 |
| Emotions | 0.80 | 50.17 |
| Memories | 0.75 | 41.46 |
| Intellect | 0.60 | 30.41 |
| Ego | 0.95 | 14.45 |
| Bliss of Deep Sleep | 0.50 | **0.00** |

**Key result**: Remainder magnitude → 0.0000. All content is accounted for. What remains is the witness — the one who was observing each negation.

**Teaching**: The Self is not found by adding something new. It is revealed by removing what it is not.

---

### Experiment 6: Guna Dynamics — The Dance of Maya

**Concept**: Sattva, Rajas, and Tamas cycle endlessly while Brahman remains unchanged.

**Setup**: Starting balance S:0.50 R:0.30 T:0.20. Random perturbations over 50 steps.

**Key result**: Proportions shift continuously. Sattva dominant throughout this run but trending downward. Liberation state = Nirguna (beyond all gunas).

**Teaching**: The dance happens on the stage. You are the stage.

---

### Experiment 7: The Four Mahavakyas

**Concept**: The four great identity declarations from the four Vedas.

**Results**:
1. **Prajnanam Brahma**: `awareness is brahman: True`
2. **Aham Brahmasmi**: Individual-Brahman overlap = 0.999944
3. **Tat Tvam Asi**: Identity after removing upadhi = 0.787
4. **Ayam Atma Brahma**: Four states (Waking/Dream/Deep Sleep/Turiya) analyzed through AUM

**What the doctrine claims**: the four mahāvākyas assert the identity of individual
and universal consciousness — on the Advaitic reading, literally rather than
metaphorically. That is the *claim being modelled*. The numbers above are
properties of vectors this module constructs to stand for the doctrine's terms;
they illustrate the claim's structure and establish nothing about whether it is
true.

---

### Experiment 8: Vivartavada — Apparent Transformation

**Concept**: The cause appears as the effect without undergoing real change.

**Gold-Ornament Demo**:
| Ornament | Gold Preserved |
|----------|---------------|
| Ring | 97.82% |
| Necklace | 99.01% |
| Bracelet | 96.22% |
| Earring | 94.28% |

**Ocean-Wave Demo**: 5 waves, each with ocean correlation > 92%.

**Teaching**: All ornaments are gold. Names differ, forms differ, but the substance is one. The wave doesn't need to "merge back" into the ocean — it was never separate.

---

## Tier 2: Physics Extension Experiments

---

### Experiment 9: Quantum Mechanics from Brahman

**Concept**: Hilbert space axioms derived from Sat-Chit-Ananda.

**Results**:
- Brahman (full state) entropy: 0.000000 — pure state, nothing hidden.
- Entangled subsystem entropy: 0.693147 (= ln(2)) — appears mixed.

**Significance**: The total state (Brahman) is always pure. Looking at only PART of an entangled whole produces apparent mixedness (ignorance). Maya IS partial tracing.

---

### Experiment 10: The Measurement Problem Dissolved

**Concept**: Collapse is perspectival, not physical.

**Results**:

| Perspective | State | Purity | Collapsed? |
|-------------|-------|--------|-----------|
| Brahman (Paramarthika) | Pure superposition | 1.000000 | No |
| Jiva (Vyavaharika) | Mixed/classical | 0.250000 | Yes (appears so) |

**Significance**: Same reality, two views. The total state never collapses. The observer's reduced state looks classical because of entanglement with the environment (Maya). No new postulate needed.

---

### Experiment 11: Entanglement Is Non-Duality

> **Caveat (2026-08-15 review):** the CHSH value below is evaluated from the
> analytic correlation formula — the demo does not consume a quantum state, so
> a separable state would "score" identically. Illustrative, not a verification.

**Concept**: Bell inequality violation proves non-locality = Advaita.

**Results**:
- CHSH S-value: **+2.828** (= +2√2) on the default |Φ+⟩; controls: separable |00⟩ → +1.414 (no violation), singlet → −2.828
- Classical bound: 2.0
- **Violates classical bound: YES**

- Separable state entropy: 0.000000 (Maya's view: "these are two")
- Entangled state entropy: 0.693147 (Brahman's view: "these are one")

**Significance**: Bell's theorem proves that reality is non-local. There are no hidden separations. The particles are not two things that communicate — they are one thing appearing as two. This is Advaita in the language of physics.

---

### Experiment 12: Gravity from Consciousness

**Concept**: Space and metric from entanglement, plus Verlinde's entropic-gravity derivation — which, since the 2026-08-15 reimplementation, does recover Newton's law (see below).

**Space from Entanglement**:

| Maya Depth | Avg Distance | Avg Entanglement | Space Exists? |
|------------|-------------|-----------------|--------------|
| 0.00 | 0.00 | 1.000 | No |
| 0.25 | 0.44 | 0.671 | Yes |
| 0.50 | 0.88 | 0.482 | Yes |
| 0.75 | 1.31 | 0.365 | Yes |
| 1.00 | 1.75 | 0.287 | Yes |

**Newton recovery** (reimplemented 2026-08-15): with Verlinde's actual chain — displaced-test-mass entropy gradient dS/dx = 2πk_B mc/ħ, holographic screen count N = Ac³/(Għ), equipartition — the force comes out as GMm/r² to 3e-16 relative, and `newton_recovered` is True. (The earlier screen-area route gave F ∝ M/r and is retained as a negative control.) Note this agreement is algebraic: it confirms the derivation is implemented faithfully, not that entropic gravity is correct physics.

**Black Hole** (SI units since the 2026-08-15 Verlinde reimplementation; the previous line quoted the old natural-units output): for M = 10 kg, r_s = 1.485e-26 m, Bekenstein-Hawking entropy 3.663e-05 J/K, Hawking temperature 1.227e+22 K. Even maximum Maya slowly dissolves.

---

### Experiment 13: The Holographic Principle

**Concept**: The 3D world is a projection of a 2D consciousness surface.

**Results**:
- Boundary dimension: 50 (consciousness)
- Bulk dimension: 20 (spacetime)
- Reconstruction fidelity: 0.4976 — **chance level for this construction**, so the boundary does **not** reconstruct the bulk here (`bulk_from_boundary` is computed and returns False). See the review note in `gravity/holographic.py`.
- Boundary is fundamental: True

**Significance**: ⚠️ **Not what this run shows.** Reconstruction fidelity is
0.4976 — chance for this random projection — and `bulk_from_boundary` is False,
so the bulk is *not* reconstructed here. "Boundary is fundamental" is an
interpretive reading, which the runtime now says explicitly. The holographic
correspondence is the motivation for the demo, not its output. This is Advaita expressed in the language of AdS/CFT.

---

### Experiment 14: Particles from Maya's Symmetry Breaking

**Concept**: The Standard Model emerges from Maya breaking Brahman's symmetry.

**Symmetry Breaking**:

| Temperature | Symmetry | VEV | Interpretation |
|-------------|----------|-----|----------------|
| T = 2.0 | Intact | 0.00 | Brahman (symmetric, no particles) |
| T = 1.0 | Broken | 1.00 | Maya activated (particles emerge) |
| T = 0.0 | Broken | 1.00 | Present universe (deep Maya) |

**Particle Zoo**: 17 particles analyzed. Closest to Brahman: photon (maya=0), neutrinos (maya≈0). Deepest in Maya: top quark (maya=0.89).

**Force Unification**: Forces converge near 3.24×10¹⁵ GeV.

---

### Experiment 15: Physical Constants from Consciousness

**Concept**: Can physical constants be derived from self-referential consciousness structure?

**Results**:
- **Golden ratio** φ = 1.6180339887 (from self-reference fixed point)
- **Fine structure constant**: estimated 1/α ≈ 131 vs actual 137 (4.4% error — right direction)
- **Koide formula**: computed 0.666627 vs target 0.666667 — **holds to 0.006%**
- **Cosmological constant**: Λ ≈ 10⁻¹²² from S_total — **matches observation**

**Significance**: The Koide formula holding suggests lepton masses are not arbitrary. The cosmological constant matching (order of magnitude) from consciousness entropy suggests the vacuum energy problem dissolves in this framework.

---

### Experiment 16: Testable Predictions and Falsification

**Concept**: Scientific integrity — what the framework predicts and what would disprove it.

**5 Predictions** (P1–P5): See [docs/PREDICTIONS.md](PREDICTIONS.md).

**5 Falsification Criteria** (F1–F5): See [docs/PREDICTIONS.md](PREDICTIONS.md).

**Experimental Roadmap**:
- Near-term (5 years): Holographic noise improvements
- Medium-term (10 years): Macroscopic superposition, vacuum entanglement
- Long-term (20 years): Entanglement-gravity coupling, consciousness causation

---

## Tier 3: Rigorous Results

---

### Experiment 17: Four Interpretations of Quantum Mechanics

**Concept**: Formal, side-by-side comparison of Copenhagen, Many-Worlds, Pilot Wave, and Advaita.

**Setup**: One shared quantum experiment (spin-1/2 in superposition, α²=0.7, β²=0.3). Eight phenomena each interpretation must explain: superposition, measurement, Born rule, entanglement, delayed choice, Wigner's friend, preferred basis, consciousness.

**Results**:

| Criterion | Copenhagen | Many-Worlds | Pilot Wave | Advaita |
|-----------|-----------|-------------|------------|---------|
| Year | 1927 | 1957 | 1952 | 2024 |
| Axiom count | 7 | 5 | 5 | 5 (4 independent) |
| Phenomena addressed | 8/8 | 8/8 | 8/8 | 8/8 |
| With unresolved problems | 6 | 2 | 4 | 0 |
| Addresses consciousness | No | Partial | No | **Yes** |
| Novel testable predictions | 0 | 0 | 2 | **5** |
| Needs collapse postulate | Yes | No | No | No |
| Needs hidden variables | No | No | Yes | No |

**Key result**: All four agree on empirical predictions (P(up)=0.7, P(down)=0.3) — and that agreement is *by construction*, since every interpretation here inherits one Born-rule computation from the shared base class. They differ in what each must posit: collapse, hidden variables, branching, or an experiential primitive.

> **Scoreboard deleted (2026-08-16).** This section previously ranked the four by
> axiom count, tallied "phenomena with problems", counted novel predictions and
> declared this framework "uniquely the only interpretation that addresses the hard
> problem". Every figure was `len()` of a list written in the module. Two claims were
> also false against the module's own output: `consciousness_comparison()` scores
> Many-Worlds `True` as well, and crediting the framework with novel predictions
> contradicts the operational equivalence of Experiment 24.

---

### Experiment 18: Gleason's Theorem — Born Rule as Theorem

**Concept**: Consistency-check the implemented measure against Gleason's conditions, and refute two sampled non-Born ray rules. Gleason's theorem is cited, not established here; that the Born rule is a theorem given the Hilbert-space structure rests on the cited theorem, not on this run.

**Part 1: Gleason's Conditions**

| Condition | Description | Result |
|-----------|-------------|--------|
| C1: dim ≥ 3 | Hilbert space dimension | PASS (dim=4) |
| C2: Non-negativity | Tr(ρP) ≥ 0 for all projectors | PASS (0/500 violations) |
| C3: Additivity | μ(P₁+P₂) = μ(P₁)+μ(P₂) for P₁ ⊥ P₂ | PASS (0/200 violations) |
| C4: Normalization | Tr(ρ) = 1 | PASS |

**Part 2: Uniqueness**

| Rule | Additivity Violations | Status |
|------|----------------------|--------|
| Born (P = \|⟨n\|ψ⟩\|²) | 0/1800 | **PASS — no violation on the sampled tests** |
| Amplitude (P ∝ \|⟨n\|ψ⟩\|) | 1800/1800 | FAIL |
| Quartic (P ∝ \|⟨n\|ψ⟩\|⁴) | 1800/1800 | FAIL |

**Part 3: Dim-2 Exception**
- Dim=2 (qubits): dispersion-free measures work — Gleason does NOT apply
- Dim=3+: dispersion-free fails 25.6% of the time — Kochen-Specker confirms hidden variables impossible

**Part 4: Axiom Reduction**
- Copenhagen: 7 axioms (Born rule is axiom A5)
- Advaita stated: 5 axioms (A5 references Gleason)
- Advaita independent: **4 axioms** (Born rule is theorem from A2)
- Reduction: **7 → 4 (3 fewer axioms)**

**Significance**: Two things must be kept apart here, and this section used to
run them together. **Gleason's theorem (1957) is established mathematics** and is
illustrated faithfully by this module — that part is solid. **The "7 → 4"
reduction is not a theorem**: it is arithmetic on the framework's own hand-entered
enumeration of its axioms against Copenhagen's, and the module says so at runtime
("hand-entered integers; their difference is arithmetic, not a theorem …a
philosophical/organisational claim, not a mathematical result established by this
module"). What this module runs is the easy direction of Gleason — a consistency check on the implemented measure, which cannot fail for a valid density operator — plus a refutation of two sampled non-Born ray rules. The hard direction is cited, not computed.

---

### Experiment 19: MERA Tensor Network — Spacetime from Entanglement

**Concept**: Multiscale Entanglement Renormalization Ansatz (MERA) where the tensor network structure IS the consciousness field, and coarse-graining models Maya dissolving toward Brahman.

**Setup**: 16-site tensor network with bond dimension 2, producing 5 layers (UV to IR).

> The tables below were regenerated on 2026-08-15 from the reimplemented
> module. The previous Parts 1–3 reported output of the retracted no-op
> construction and have been removed rather than annotated.

**Part 1: Tensor algebra (are the tensors real?)**
- 15 disentanglers, max \|U†U − I\| = 2.22e-15
- 15 isometries, max \|W†W − I\| = 2.00e-15

**Part 2: Negative control — the tensors must affect the state**

Replacing layer 2's tensors with fresh random ones moves the boundary state:
‖Δψ‖ = 1.4619, phase-invariant distance = 1.3587, `state_changed = True`.
The retired implementation scored **0** here — that was the defect.

**Part 3: Entropy vs minimal cut, measured on the constructed state**

| Interval length | S (exact) | Min cut (bonds) | ln(χ)·cut | Saturation |
|---|---|---|---|---|
| 2 | 1.2123 | 2 | 1.3863 | 0.874 |
| 4 | 1.9166 | 4 | 2.7726 | 0.691 |
| 8 | 2.5506 | 6 | 4.1589 | 0.613 |

**Part 4: Remove entanglement → lose connectivity**

I(L:R) as the entangling strength λ is switched off:
5.101 → 4.804 → 3.055 → 1.728 → 0.662 → 0.000 at λ = 1.0, 0.6, 0.35, 0.2, 0.1, 0.0.
Monotone on this grid (not claimed globally).

**Significance (reimplemented 2026-08-15)**: the original coarse-graining was a physical no-op, and its results were retracted. The module now builds an explicit 16-site state by contracting real disentanglers and isometries, and measures that state: the exact interval entropy obeys the RT-type bound S ≤ ln(χ)·|minimal cut| (saturation 0.874/0.691/0.613 at lengths 2/4/8, cut computed by max-flow on the actual network graph), and mutual information between halves falls 5.10 → 0 as the entangling strength is switched off. The hierarchical log-shaped cut remains a property of the network *by construction* and is labeled as such, not claimed as a result. Note the monotone decrease is verified on the sampled λ grid, not globally.

---

### Experiment 20: 2+1D Einstein Equations from Consciousness Thermodynamics

**Concept**: Jacobson's thermodynamic derivation of Einstein's equations, implemented on a 2D discrete Delaunay manifold.

**Setup**: 80 random points, Delaunay triangulation (149 triangles), Gaussian mass distributions.

**Derivation path**: Energy-momentum T_00 → Bekenstein entropy field S → integrated entropy curvature R_entropy → test R ∝ T.

**Results**:

| Scenario | Total Energy | Total Entropy | R-T Correlation |
|----------|-------------|---------------|----------------|
| No mass | 0.00 | 0.00 | 0.00 (trivially) |
| One mass | 2.68 | 84.37 | **0.91** |
| Two masses | 3.74 | 93.67 | **0.94** |

**Key result**: The entropy-derived proxy correlates with energy-momentum at **0.90–0.94** on a 2D discrete manifold with 80 points and 149 triangles. **CAVEAT (review 2026-08-15): this correlation is circular by construction** — the site entropy is *defined* proportional to T₀₀ and the correlated "curvature" is a smoothed copy of that entropy, while the genuine geometric (Regge deficit-angle) curvature *anti-correlates* with T₀₀. (The 1D proof-of-concept formerly cited as 0.93 actually yields −0.98 on re-execution.)

**Significance**: Illustrates the *shape* of Jacobson's argument — Einstein's equations as thermodynamic equations — on a discrete geometry. It does **not** demonstrate the argument: for that, the entropy would have to come from an independent structure (e.g., actual entanglement data) rather than being defined from the energy density it is then correlated with.

---

### Experiment 21: Quantum Error Correction as Spacetime

> **Reimplemented 2026-08-15.** The original "80% boundary erasure" figure was
> the scan's loop bound with near-chance fidelity, and was withdrawn — recovering
> from >50% erasure is impossible by no-cloning. This experiment now runs a
> genuine **[[5,1,3]] perfect code**: all 15 single-qubit Paulis corrected
> (fidelity 1.0 over 60 cases), all 10 two-erasure patterns recovered, erasure
> threshold **2/5 (40%)**, and the logical qubit reconstructable from **any 3/5
> (60%)** subregion. A negative control confirms 3-erasure destroys the
> information (trace distance 0.0 on the survivors). Numbers below that predate
> this rebuild are superseded.

**Concept**: Almheiri-Dong-Harlow (2015) showed that holographic duality has the structure of a quantum error-correcting code. The bulk (Brahman) is protected from boundary (Maya) disturbances.

**Setup**: [5,1] holographic code (5 physical qubits encoding 1 logical qubit).

**Part 1: Error correction threshold** (recomputed 2026-08-15 with the real
[[5,1,3]] code; the old table's "fidelities" near 0.5 were chance-level and its
80% row was impossible)

| Qubits Erased | Fraction | Recovery Fidelity | Recoverable? |
|---------------|----------|------------------|-------------|
| 0 | 0% | 1.0000 | Yes |
| 1 | 20% | 1.0000 | Yes |
| 2 | 40% | 1.0000 | Yes |
| 3 | 60% | — (information absent) | **No** |
| 4 | 80% | — (information absent) | **No** |

**Threshold**: erasure of up to **2 of 5 qubits (40%)** is exactly recoverable.
At 3 erasures the reduced states of the logical |0̄⟩ and |1̄⟩ on the survivors are
*identical* (trace distance 0.0) — the information is genuinely gone, as
no-cloning requires. Complementarily, the logical qubit is reconstructable from
**any 3 of 5 (60%)** subregion.

**Part 2: Distinguishability**
- Orthogonal logical states remain distinguishable even after qubit erasure (overlap 0.026)
- Codewords are highly entangled — entanglement enables robustness

**Part 3: Multiple reconstruction paths**
- Same bulk accessible from different boundary subregions (entanglement wedge reconstruction)
- Maps to: Brahman realizable from different paths of inquiry

**Significance**: What is demonstrated is that the **[[5,1,3]] code** protects one logical qubit against any single-qubit Pauli error and any 2-of-5 erasure, and that 3-of-5 erasure destroys the information outright — a real, checkable property of a real code. The stronger reading — that *spacetime* is an error-correcting code, and that this is why the empirical world is stable — is the Almheiri-Dong-Harlow **analogy** applied to Advaita, an interpretation laid over the computation rather than a result of it.

---

### Experiment 22: Fine Structure Constant — Systematic Derivation (v2)

**Concept**: Systematic exploration of six approaches to derive α ≈ 1/137.036 from the consciousness field's mathematical structure.

**Six approaches**:
1. MERA RG fixed-point ratio
2. Chern-Weil topological invariants (n=68 or n=69 layers of self-reference)
3. Feigenbaum self-referential constants
4. Golden ratio compositions
5. Continued fraction analysis
6. Modular forms and Heegner numbers

**Ranking by accuracy**:

| Rank | Method | 1/α | Error |
|------|--------|-----|-------|
| 1 | **163 - 26 + π/100** | **137.031** | **0.003%** |
| 2 | Chern-Weil n=69 | 138.000 | 0.70% |
| 3 | Chern-Weil n=68 | 136.000 | 0.76% |
| 4 | Feigenbaum 1/(r∞·4πe) | 121.946 | 11.01% |

Previous best: 4.41% error. New best: **0.003% error — a 1000x improvement.**

**The 163 connection**: 163 is the largest Heegner number (unique factorization in Q(√-163)). 26 is the critical dimension of bosonic string theory. 163 - 26 = 137 exactly. The j-invariant connects to the Monster group via Monstrous Moonshine. The suggestion that the π/100 correction relates to U(1) gauge geometry is speculation — nothing in the code derives it.

**Continued fraction**: 1/α = [137; 27, 1, 3, 1, 1, 16, ...]. The convergent 3700/27 = 137.037 matches to 0.0008% — structurally guaranteed for a convergent computed from the measured value; not a result.

**Honest assessment**: This is numerological exploration, not rigorous derivation. The accuracy is striking and the mathematical connections are motivated, but a true derivation would show WHY the consciousness field requires Monster symmetry. This remains the key open problem.

---

### Experiment 23: IIT-Entanglement Bridge — Consciousness Meets Quantum

**Concept**: Formally test the conjecture that integrated information Φ (Tononi's measure of consciousness) is bounded by quantum entanglement entropy S.

**Conjecture**: Φ ≤ S_entanglement

> **⚠️ Superseded by a validated test — the bound is falsified.** The tables below
> are the output of the original `iit_bridge.py`, which computes Φ and S from one
> shared construction, so Φ ≤ S holds *by definition* and its "Φ" is not canonical
> IIT Φ (a PyPhi benchmark finds them uncorrelated, r ≈ −0.01). An independent,
> validated retest (`predictions/phi_s_systems.py` + `validated_phi.py` +
> `entanglement_entropy.py`: canonical PyPhi Φ vs. the entanglement entropy of a
> transverse-field Ising ground state built from the *same* couplings; N = 216,
> seed 42; numbers per the 2026-08-12 **TPM-ordering audit**, which corrected a
> big-endian/little-endian encoding bug at the PyPhi boundary — see
> `reproducibility/phi_s/README.md`) **refutes Φ ≤ S**. The 77% apparent hold
> rate is produced almost entirely by the trivial Φ = 0 systems and is
> statistically identical to a permutation null (0.7685 vs 0.7789);
> **50 of the 51 systems with nonzero integrated information violate the
> bound**, because canonical Φ (up to ≈ 4.0 bits) is not capped by the bipartition
> entanglement entropy that limits S (≈ 0.83 bits). The raw Φ–S correlation
> (Pearson r ≈ +0.64) is a **connectivity confound**: controlling for connectivity
> collapses it to r ≈ −0.07 (permutation p = 0.29; with system size, +0.06,
> p = 0.38), so **no residual Φ–S association survives** — §8 retains no claim.

**Part 1: Conjecture test across 50 random systems (original circular construction)**

| Metric | Value |
|--------|-------|
| Trials | 50 |
| Violations | **0** |
| Holds rate | **100%** |
| Average Φ | 0.026 |
| Average S | 0.110 |
| Average Φ/S ratio | 0.234 |

**Part 2: Extreme cases**

| Case | Φ | S | Holds? | Advaita Meaning |
|------|---|---|--------|-----------------|
| Disconnected | 0.000 | 0.000 | Yes | Maya complete — no consciousness, no entanglement |
| Half-connected | 0.000 | 0.317 | Yes | Maya partial — some entanglement, low integration |
| Fully connected | 0.030 | 0.693 | Yes | Approaching Brahman — max integration, max entanglement |

**Part 3: MERA consciousness profile**

| Layer | Φ | Label |
|-------|---|-------|
| 0 (UV) | 0.022 | Deep Maya |
| 1 | 0.386 | |
| 2 | 0.595 | |
| 3 | 0.595 | |
| 4 (IR) | 0.595 | Brahman |

> **These lines are retracted (2026-08-16).** The MERA Φ profile above used the
> retired internal Φ heuristic on a construction later found defective;
> `docs/PREDICTIONS.md` records it as **Retracted**, and the correction banner
> at the head of this section applies to the prose here too, not only to the
> tables. Prediction 1 below is the falsified Φ ≤ S bound restated without the
> notation — "Φ sets a lower bound on S" *is* Φ ≤ S — and does not survive the
> validated retest. They are kept only as a record of what was once claimed.

~~Φ increases toward IR: **Yes**. Maximum consciousness at maximum integration = Brahman.~~

**Testable predictions (retracted — see the banner above)**:
1. ~~Measuring Φ in a neural system sets a lower bound on its quantum entanglement~~
2. ~~Systems with zero entanglement have zero consciousness~~
3. Anesthesia should reduce both Φ and S simultaneously
4. Deep meditation (Samadhi) should correspond to maximum Φ and maximum S

**Significance**: The original intuition — that consciousness (Φ) is *bounded* by entanglement (S) — does not survive a validated test: canonical Φ is not capped by S, and the "100% holds" is a scale artifact of the circular construction. Nor does a weaker claim survive: the raw Φ–S correlation (r ≈ +0.64) is a **connectivity confound** — controlling for connectivity collapses it to r ≈ −0.07 (p = 0.29) — so the bridge between neuroscience (IIT), quantum physics (entanglement), and Advaita has **no established quantitative form** in this test, and the anaesthesia/Samadhi predictions above are not supported by it.

---

## Tier 4: Paper Companion Experiments

These experiments were built to computationally support the claims of the accompanying paper, public as a preprint: *"The Cardinality of Experience Is Underdetermined by the Quantum State: A Constructive Case for a Consciousness-Primitive Interpretation"* (Zenodo, https://doi.org/10.5281/zenodo.21007975). Earlier drafts circulated under the working title *"A Non-Dual Interpretation of Quantum Mechanics: Consciousness as Ontological Primitive"*.

---

### Experiment 24: Everett-Advaita Operational Equivalence

**Concept**: The paper claims "this interpretation is currently empirically equivalent to Everett." That claim is **analytic**, and this experiment does not test it — it cannot. Both readings use the same Hilbert space, the same unitary dynamics, the same Born rule and the same decoherence, so identical predictions follow by construction. The experiment computes the shared quantities once and catalogues the ontological divergences that carry no measurable consequence.

> **Deleted 2026-08-16.** The module previously claimed to PROVE the equivalence by
> running "both interpretations". It built one array and copied it twice
> (`everett_probs = probs.copy(); advaita_probs = probs.copy()`), reset the same RNG
> seed before each draw, returned two hardcoded `"numbers_identical": True`, and
> computed its summary flag as a disjunction of `.get(key, True)` over keys the
> sub-results did not carry — so `all_empirically_identical` was True for every
> possible input, including one where every test failed.

**Five empirical tests**:

| Test | Everett = Advaita? |
|------|-------------------|
| Born rule probabilities | **Identical** |
| Time evolution (5 time steps) | **Identical** |
| Measurement statistics (10,000 trials) | **Identical** |
| Entanglement correlations (Bell CHSH) | Shared calculation (S = +2.83 on |Φ+⟩) |
| Decoherence (purity, pointer states) | **Identical** |

**Five ontological divergences (none measurable)**:

| Divergence | Everett | Advaita | Measurable? |
|-----------|---------|---------|-------------|
| What exists | Universal wave function | Universal conscious subject | No |
| What branches are | Equally real worlds | Perspectives of one subject | No |
| What observer is | Functional subsystem | Localized perspective | No |
| Why experience exists | Only a functionalist account | Intrinsic to the primitive | No |
| Hard problem status | Bridged functionally (cross-categorial) | Reframed (cross→intra-categorial) | No |

**Significance**: Every empirical prediction is identical. The interpretations differ only in ontological description. This is precisely what the paper claims.

---

### Experiment 25: Perspectival Asymmetry (Generalized)

**Concept**: The paper's core interpretive move — "collapse is perspectival, not physical" — was demonstrated in Experiment 10 for one case. This experiment proves it holds universally.

**Test 1: 20 different initial states** (equal, biased, random, basis states)
- Total purity = 1.0 for ALL states
- Reduced purity < 1.0 for all superposition states
- Basis states: reduced state also pure (correctly — no superposition to decohere)

**Test 2: 6 environment sizes** (dim 3 to 64)
- Total purity = 1.000000 for ALL sizes
- Reduced purity = 0.333333 (= 1/d) for all — independent of environment size

**Test 3: 5 random measurement bases**
- Total purity = 1.0 in every basis
- Reduced purity < 1.0 in every basis

**Test 4: Exactness (100 random states)**
- Maximum deviation from total purity 1.0: **8.88 × 10⁻¹⁶** (machine precision)
- The perspectival asymmetry is **exact**, not approximate

**Significance**: The measurement resolution is a mathematical theorem, not an empirical finding. Total state purity = 1.0 is exact for ANY pure state, ANY partition, ANY basis. "Collapse" is perspectival.

---

### Experiment 26: Observer Centrality

**Concept**: The paper's hidden premise — "observer ontology is part of the interpretive burden" — is demonstrated in four logical steps.

**Step 1: Decoherence selects pointer states**
- Off-diagonal coherence: 0.0000000000 (exact)
- Pointer states: |↑⟩, |↓⟩
- This is standard, uncontroversial physics (Zurek 2003)

**Step 2: Decoherence does NOT select the experienced outcome**
- P(↑) = 0.5, P(↓) = 0.5
- Which outcome is experienced? **UNDEFINED by the formalism**
- The gap: the formalism gives statistics, something else gives experience

**Step 3: ALL interpretations invoke "observer" to bridge the gap**

| Interpretation | Observer Analyzed? | Mechanism |
|---------------|-------------------|-----------|
| Copenhagen | No | Collapse triggers outcome |
| Everett | No | Branching — all outcomes occur |
| Bohm | No | Particle always had a position |
| **Advaita** | **Yes** | Localized perspective of universal subject |

**Step 4: Leaving "observer" unanalyzed is a gap, not neutrality**
- Formalism determines: 5 things (basis, probabilities, entanglement, purities)
- Formalism leaves open: 4 things (which outcome, why experience, what observer IS, why unity)
- All open questions involve the concept of "observer"

**Significance**: The concept of "observer" does essential, non-trivial work in the measurement formalism. Its ontological status is therefore part of the interpretive burden, not an optional philosophical add-on. This demonstrates the paper's hidden premise computationally.

---

## Tier 5: Physics Extensions

---

### Experiment 27: 3+1D Einstein Equations

> **Caveat (2026-08-15 review):** same circular construction as Experiment 20
> (entropy defined from T₀₀), in 3D — illustrates the Jacobson logic; the
> correlation is not evidence.

```bash
python main.py --experiment 27
```

**Extends** Experiment 20 (2+1D) to full 3+1D spacetime.

**Method**: Jacobson's thermodynamic derivation on a 3D Delaunay tetrahedralization. Point cloud → tetrahedralization → energy-momentum T₀₀ → entanglement entropy S (3D area law) → Ricci curvature via solid angle deficit (3D Regge calculus) → Einstein equation test.

**Key results**:
- 80 points, ~413 tetrahedra in 3D
- R_entropy vs T₀₀ correlation: **~0.88** (single mass)
- Empty space: flat (correlation 0)
- Binary system: curved around both masses
- Mass shell: interior relatively flat (Birkhoff-like)
- Gravitational wave signature: perturbations propagate, amplitude falls off with distance

**Significance**: ⚠️ **Withdrawn.** This sentence is the headline
`gravity/einstein_3d.py` records as withdrawn by the 2026-08-15 review. No
metric, connection, Ricci or Einstein tensor is formed and G_μν = 8πG T_μν is
never evaluated; the construction is a static 3D point cloud, not 3+1D
spacetime, and the entropy it correlates is defined from the energy density it
is correlated against. What the experiment shows is the *shape* of the Jacobson
argument, not its result.

---

### Experiment 28: ER=EPR Correspondence

> **Caveat (2026-08-15 review):** the throat–entropy identity in this demo is
> imposed by definition (`S_thermal = S_entanglement` by assignment) —
> illustrative, not a demonstration.

```bash
python main.py --experiment 28
```

**Implements** the Maldacena-Susskind conjecture: Einstein-Rosen bridges (wormholes) = EPR entanglement.

**Method**: Four demonstrations:
1. **Thermofield double**: |TFD⟩ is simultaneously a maximally entangled state AND the dual of an eternal black hole. S_entanglement = S_thermal (ER=EPR identity).
2. **Wormhole geometry**: Ryu-Takayanagi → throat area = 4G × S. More entanglement → bigger wormhole.
3. **Van Raamsdonk**: Cutting entanglement pinches off the wormhole. Zero entanglement → disconnected spacetimes.
4. **Non-traversability**: Monogamy of entanglement prevents information transfer through the wormhole.

**Key results**:
- TFD total state purity: 1.0 (pure); each side thermal (mixed) — Maya is the partial view
- Zero entanglement → no wormhole → disconnected space
- Maximum entanglement → widest throat → most connected
- Entanglement dilution in tripartite state → non-traversability

**Significance**: ⚠️ **Illustrative only.** The throat–entropy relation is
imposed by assignment in this demo, not derived, so ER=EPR is exhibited rather
than shown. It does not "complete" anything. Non-duality at the quantum level IS non-duality at the geometric level. ER = EPR = Advaita.

---

### Experiment 29: Fine Structure Constant v3 — Derivation Attempts (numerology-class)

```bash
python main.py --experiment 29
```

**Extends** Experiment 22 (v2, 0.003% error) with further derivation attempts — all numerology-class by the look-elsewhere audit of Experiment 31.

**Method**: Four systematic approaches:
1. **Self-referential**: Feigenbaum universality from consciousness self-reference (logistic map fixed points, bifurcation structure)
2. **Modular bootstrap**: j-invariant, Heegner numbers, Ramanujan constant, Moonshine connection
3. **Holographic constraint**: Boundary/bulk degree-of-freedom ratio constrains electromagnetic coupling
4. **Continued fraction analysis**: [137, 27, 1, 3, 1, 1, 16, ...] — irregular structure suggests transcendental

**Key results**:
- Best: Heegner 163-26+π/100 = 137.031 (0.003% error, same as v2)
- Variant: 163-26+π/(4×26) = 137.030 (0.004% error — slightly WORSE than v2's 0.0033%; the "holographic motivation" for the correction is post hoc)
- j-invariant: ∛640320/(4πn) = 136.976 (0.04%)
- Feigenbaum and holographic: order-of-magnitude estimates
- Continued fraction: 3700/27 = 137.037 (0.0008% — but a convergent is computed FROM the measured value, so this restates the input; it predicts nothing)

**Honest assessment**: The Heegner/modular approach remains strongest. v3 explores WHY rather than just matching — but a true derivation requires showing the consciousness field's symmetry group necessitates Q(√-163) structure.

---

### Experiment 30: Unity of Experience — Experiential Underdetermination

```bash
python main.py --experiment 30
```

**Purpose**: Supports the accompanying paper's §2.2 claim that the reduced state leaves the experiential facts open. Shows that multiple, pairwise-incompatible experiential ontologies — Everett-unified, Everett-superposed, Copenhagen-classical, and consciousness-primitive — are all consistent with the *same* reduced density matrix rho_SA.

**Method**:
1. Construct the standard post-measurement state |Ψ⟩ = Σ c_n |n⟩_S |n⟩_A |E_n⟩ with orthogonal environment pointers.
2. Trace out the environment to obtain rho_SA.
3. Verify einselection: rho_SA is diagonal in the pointer basis with off-diagonal norm < 10⁻¹⁰.
4. Enumerate four experiential interpretations and their asserted cardinalities of unified experience.
5. Test whether rho_SA alone discriminates among them.
6. Sweep 30 random amplitude profiles to check robustness.

**Key results**:
- Reduced state rho_SA has trace 1, rank N, and is diagonal in the pointer basis (off-diagonal norm ≈ 0).
- Four interpretations map to identical rho_SA but disagree on cardinality of unified experience: {0, 1, N}.
- Robustness: the amplitude sweep is **structurally invariant** — three of the four cardinalities are definitional, so the sweep cannot come out False for any input. Retired as evidence 2026-08-15; it is not a finding.
- Conclusion: the identification of pointer states with unified experiences is a postulate ADDED to decoherence, not derived from it.

**Paper support**: The four-reading catalogue is analytic bookkeeping (§2.2), not evidence. The measured content is the §2.4 factorization-dependence result, which the paper cites as establishing factorization-dependence and explicitly **not** as a witness for its claim (E).

**Supporting note**: [`docs/GLEASON_PROBABILITY_GAP.md`](GLEASON_PROBABILITY_GAP.md) addresses the related Kent/Baker critiques of Gleason-based Born rule derivations.

---

### Experiment 31: The Look-Elsewhere Effect — Why the α "Derivation" Is Numerology

```bash
python main.py --experiment 31
```

**Purpose**: A deliberately **self-critical** demonstration. The framework's most
striking numerical result is 1/α ≈ 163 − 26 + π/100 = 137.0314 (0.0033% error).
This experiment shows how easily a target of that precision is hit by a large
family of equally simple formulas, so a reader can judge the claim honestly rather
than take the near-match as evidence of a derivation.

**Method** (via `numerology/look_elsewhere.py`):
1. Enumerate the family of comparably-simple integer/π/e expressions.
2. Count how many land within the claim's own precision of 1/α.
3. Measure how densely the family covers the window 130–145, the broad range
   0.1–2000, and a basket of 25 real physics constants — all at 10⁻⁴ tolerance.

**Key results**:
- Many distinct family members match 1/α at the celebrated formula's precision;
  the closest is *more* accurate than 163 − 26 + π/100 itself.
- The family covers essentially any target in the tested ranges to 10⁻⁴, and hits
  a large fraction of 25 unrelated physics constants to the same tolerance.
- **Conclusion**: matching 1/α is expected by chance (the look-elsewhere effect),
  not evidence of a law. This is precisely why the constants work lives in
  `numerology/`, not `constants/`. The companion `numerology/cross_validation.py`
  reinforces this: a recipe fitted on one constant fails to predict another.

---

## Summary of Key Quantitative Results

| Metric | Value | Significance | Status |
|--------|-------|-------------|--------|
| Axiom reduction | 7 → 4 | Born rule is a theorem via Gleason; the count is the framework's own enumeration | **Established theorem (Gleason 1957), numerically illustrated; the 7→4 count is the framework's own axiom bookkeeping, not a derived result** |
| **Fine structure 1/α** | **137.031 (0.003%)** | **163-26+π/100 via Heegner numbers** | **Numerology (fails hold-out, Exp 31)** |
| **Look-elsewhere on 1/α** | **whole ranges covered at 1e-4** | **the near-match is expected by chance, not a law** | **Demonstrated (Exp 31)** |
| **IIT conjecture Φ ≤ S** | **falsified (validated PyPhi Φ, N=216, ordering-audit-corrected)** | **50 of 51 nonzero-Φ systems violate it; Φ (≤4.0 bits) not capped by bipartition S (≤0.83). Raw Φ–S correlation (r≈+0.64) is a connectivity confound (partial r≈−0.07, p=0.29) — nothing survives** | **Falsified** |
| Everett-Advaita equivalence | shared formalism computed once | divergences are ontological only | **Analytic, not tested** (scoreboard deleted 2026-08-16) |
| **Perspectival asymmetry** | **Exact (10⁻¹⁶)** | **All states, bases, env sizes — total always pure** | **Proven** |
| **Observer centrality** | **4/4 open questions involve observer** | **Observer ontology is part of interpretive burden** | **Demonstrated** |
| **Experiential underdetermination** | rho_SA invariant to 1e-14 under environment unitaries; rank(rho_SA) 3 -> 1 under an A(x)E regrouping | The branch count depends on the chosen factorization (paper §2.4) | **Measured** — the "30/30 trials" framing was **retired 2026-08-15**: the sweep is structurally invariant, so 30/30 was guaranteed before any trial ran |
| Born rule uniqueness | 0/1800 violations | Only consistent probability rule in dim ≥ 3 | **Proven** |
| **2+1D Einstein R-T correlation** | **0.94** | Circular by construction — entropy defined ∝ T₀₀ (Exp 20 caveat) | **Withdrawn as evidence** |
| **3+1D Einstein R-T correlation** | **0.88** | Same circular construction in 3D (Exp 27 caveat) | **Withdrawn as evidence** |
| **ER=EPR correspondence** | **Throat = 4G×S** | Relation imposed by definition in the demo (Exp 28 caveat) | **Illustrative (definitional)** |
| **Entanglement disconnects space** | I(L:R) 5.10 → 0 as λ→0 | Real MERA state; RT-type bound S ≤ ln(χ)·|cut| holds | **Reimplemented 2026-08-15** |
| **QEC erasure threshold** | **2 of 5 (40%)**; any 3/5 reconstructs | Real [[5,1,3]] code; 3-erasure provably unrecoverable (no-cloning) | **Reimplemented 2026-08-15** |
| Brahman field coherence | 1.0000 | Perfect unity before Maya | Verified |
| Bell CHSH value | +2.828 (= +2√2) | Computed on the supplied state; separable/singlet controls | Illustrative |
| Total state purity (Paramarthika) | 1.000000 | No collapse at the absolute level | Demonstrated |
| Reduced state purity (Vyavaharika) | 0.250000 | Classical appearance from partial view | Demonstrated |
| Neti-Neti remainder | 0.0000 | All layers negated — only witness remains | Demonstrated |
| Gold preservation in ornaments | >94% | Substance unchanged through form changes | Demonstrated |
| Newton from entropic gravity | ratio 1.000 (3e-16) | Verlinde's derivation implemented faithfully; algebraic identity, not an empirical test | Reimplemented 2026-08-15 |
| Koide formula | 0.666627 | Matches 2/3 to 0.006% — masses have structure | Verified (not derived) |
| Cosmological constant | 10⁻¹²² | Consistent with consciousness entropy | Consistency check |
| Individual-Brahman overlap | 0.999944 | Atman ≈ Brahman (identity, not similarity) | Demonstrated |
| Force unification energy | ~10¹⁵ GeV | Forces converge — Maya dissolves at high energy | Demonstrated |
