# Module Documentation

## Detailed Reference for Every Module and Class

---

## Metaphysical Foundation Modules

---

### `brahman/consciousness.py` — The Singular Reality

**Class: `Brahman`**

The non-dual ground of all existence. Implemented as a singleton — there can only be one.

| Property/Method | Description |
|----------------|-------------|
| `Brahman(resolution=256)` | Creates (or returns existing) Brahman instance. Resolution controls field granularity. |
| `.field` | Returns a copy of the undifferentiated field — uniform complex vector normalized to 1. |
| `.awareness()` | Returns `self` — consciousness aware of itself. The self-referential loop. |
| `.manifest(maya_lens)` | Brahman "seen through" a Maya operator. Returns the projected field. |
| `.coherence()` | 0.0–1.0 measure of field uniformity. 1.0 = perfect unity. |
| `.is_non_dual()` | Boolean: is the field still undifferentiated? |
| `.reset()` | Class method. Resets the singleton (for test isolation). |

**Key design choice**: Brahman's `__eq__` always returns `True` for another Brahman instance — because Atman IS Brahman, not merely equal to it.

---

### `brahman/sat_chit_ananda.py` — Three Aspects of Brahman

**Class: `SatChitAnanda`**

Three orthogonal projections of the same field, each revealing a different aspect.

| Method | Returns | Advaita Meaning |
|--------|---------|-----------------|
| `.sat()` | Magnitude of the field (np.abs) | Existence — THAT anything IS |
| `.chit()` | Phase angles of the field (np.angle) | Consciousness — the knowing aspect |
| `.ananda()` | Coherence measure (float) | Bliss/Fullness — completeness |
| `.unity_check()` | Dict with reconstruction error | Proves Sat+Chit fully reconstruct the field |

---

### `maya/superimposition.py` — Adhyasa

**Class: `Adhyasa`**

The core mechanism of Maya — projecting familiar patterns onto ambiguous perception.

| Method | Description |
|--------|-------------|
| `.superimpose(substrate, ignorance_level, pattern_name)` | Apply superimposition. Returns `SuperimposedObject`. |
| `.rope_snake_demo(rope_length)` | Classic example at multiple ignorance levels. |

**Class: `SuperimposedObject`**

| Property | Type | Description |
|----------|------|-------------|
| `.apparent` | np.ndarray | What is perceived (snake) |
| `.actual` | np.ndarray | What is really there (rope) |
| `.is_real` | bool | Always `False` — superimposed objects are never real |
| `.error_magnitude` | float | Distance between appearance and reality |
| `.recognize()` | np.ndarray | Sublation — returns `.actual` |

---

### `maya/nama_rupa.py` — Name and Form

**Class: `NamaRupa`**

Differentiates a unified field into apparently distinct entities.

| Method | Description |
|--------|-------------|
| `.differentiate(field, num_entities, names)` | Carves the field into named forms. Returns list of `NamedForm`. |
| `.reunify(entities)` | Dissolves all forms back to the source field. |
| `.show_non_separation(entities)` | Proves all forms are made of the same substance. |

---

### `maya/gunas.py` — Three Qualities

**Class: `Gunas`**

Models the three fundamental qualities of experience.

| Method | Description |
|--------|-------------|
| `.apply_to_field(field)` | Transform field according to current guna balance. Sattva clarifies, Rajas distorts, Tamas dampens. |
| `.evolve(dt, perturbation)` | Advance the guna balance one time step. |
| `.simulate_cycle(steps)` | Run many steps, returning history of proportions. |
| `.transcend()` | Returns `GunaState.TRANSCENDED` (Nirguna). |

---

### `levels/reality_engine.py` — Three Levels of Reality

**Class: `RealityEngine`**

Orchestrates the three levels and demonstrates sublation.

| Method | Description |
|--------|-------------|
| `.observe(observer_state)` | Returns what is seen from "liberated", "waking", or "dreaming" perspective. |
| `.demonstrate_sublation()` | Walks through Dream → Waking → Liberation, showing each level sublating the previous. |
| `.compare_levels()` | Side-by-side comparison of all three levels. |

---

### `emergence/spacetime.py` — Emergent Space and Time

**Class: `ConsciousnessField`**

Generates spatial dimensions through self-referential differentiation.

| Method | Description |
|--------|-------------|
| `.differentiate(num_dimensions)` | Each self-referential step creates a new spatial dimension. |
| `.collapse_to_unity()` | Moksha — all dimensions fold back to a single point. |

**Class: `EmergentSpacetime`**

Generates spatial points and metric from the awareness field.

| Method | Description |
|--------|-------------|
| `.generate_from_awareness(awareness_field)` | Produces spatial coordinates determined by the field's structure. |
| `.curvature_proxy()` | Estimates curvature from the emergent geometry. |

---

### `emergence/causation.py` — Vivartavada

**Class: `Vivartavada`**

Models apparent transformation — the cause appears as the effect without undergoing real change.

| Method | Description |
|--------|-------------|
| `.apparent_transformation(substrate, form_function)` | Apply a form to the substrate. Returns `CausalEvent`. |
| `.gold_ornament_demo()` | Same gold → ring, necklace, bracelet. Substance preserved >94%. |
| `.ocean_wave_demo()` | Waves on ocean. Each wave IS ocean. Correlation >92%. |

---

### `emergence/observer.py` — Sakshi (The Witness)

**Class: `Sakshi`**

The unchanging witness of all experience.

| Method | Description |
|--------|-------------|
| `.witness(experience)` | Witness an experience. `sakshi_changed` is always `False`. |
| `.witness_state_transition(from_state, to_state)` | Shows the witness persists through state changes. |
| `.demonstrate_five_sheaths()` | Pancha Kosha — each sheath is witnessed, therefore not-self. |
| `.mirror_analogy()` | Mirror reflects fire but is not burned. |

---

### `liberation/neti_neti.py` — "Not This, Not This"

**Class: `NetiNeti`**

Systematic negation of false identifications.

| Method | Description |
|--------|-------------|
| `.inquire()` | Full inquiry — negates all 8 layers. Returns process + final teaching. |
| `.inquire_step_by_step()` | Generator yielding one negation at a time. |

8 layers negated: Physical Body → Vital Energy → Thoughts → Emotions → Memories → Intellect → Ego → Bliss of Deep Sleep. Remainder magnitude → 0.0.

---

### `liberation/mahavakya.py` — The Four Great Sayings

**Class: `Mahavakya`**

Computational demonstrations of the four identity declarations.

| Method | Mahavakya | Key Metric |
|--------|-----------|-----------|
| `.prajnanam_brahma()` | "Consciousness is Brahman" | `awareness is brahman: True` |
| `.aham_brahmasmi()` | "I am Brahman" | Individual-Brahman overlap: 0.999944 |
| `.tat_tvam_asi()` | "That Thou Art" | Identity after removing upadhi: 0.787 |
| `.ayam_atma_brahma()` | "This Self is Brahman" | AUM analysis across 4 states |

---

## Physics Extension Modules

---

### `quantum/hilbert_space.py` — Brahman as Hilbert Space

**Class: `BrahmanHilbertSpace`**

Derives Hilbert space axioms from Sat-Chit-Ananda.

| Method | Description |
|--------|-------------|
| `.inner_product(psi, phi)` | Chit as ⟨ψ\|φ⟩ — the degree of mutual recognition. |
| `.norm(psi)` | Sat as \|\|ψ\|\| — the measure of existence. |
| `.von_neumann_entropy(rho)` | S(ρ) = -Tr(ρ ln ρ). Pure states (Brahman) have S=0. Mixed states (Maya) have S>0. |
| `.partial_trace(rho, dim_a, dim_b)` | Maya's concealment — ignoring part of the whole creates apparent mixedness. |
| `.demonstrate_quantum_advaita()` | Shows: Brahman is pure (S=0); subsystem of entangled state appears mixed (S>0). |

---

### `quantum/operators.py` — Consciousness, Maya, and Witness Operators

**Class: `ConsciousnessOperator`**

| Method | Description |
|--------|-------------|
| `.identity()` | Brahman as pure being — the do-nothing operator. |
| `.awareness_operator()` | Hermitian (self-adjoint = self-aware) matrix. |
| `.creation_operator()` | a† — Srishti (creation/manifestation). |
| `.annihilation_operator()` | a — Laya (dissolution). |
| `.hamiltonian(coupling)` | Generator of Maya's time evolution. |

**Class: `MayaOperator`**

| Method | Description |
|--------|-------------|
| `.avarana(depth)` | Concealing projection — hides dimensions of the field. |
| `.vikshepa(seed)` | Projecting transformation — reshuffles visible subspace. |
| `.full_maya(depth, seed)` | Avarana + Vikshepa combined. |
| `.measure_maya_depth(operator)` | 0.0 (no Maya) to 1.0 (total concealment). |

**Class: `SakshiProjector`**

| Method | Description |
|--------|-------------|
| `.witness(psi)` | Sees all probabilities WITHOUT collapsing. Sakshi never changes. |
| `.ego_measurement(psi)` | Collapses to one outcome — the ego identifies with a result. |

---

### `quantum/wave_function.py` — The Wave Function

**Class: `BrahmanWaveFunction`**

| Method | Description |
|--------|-------------|
| `.brahman_ground_state()` | Gaussian — maximum clarity, minimum uncertainty. |
| `.maya_excited_state(n)` | nth Hermite-Gaussian. Higher n = more differentiation = deeper Maya. |
| `.time_evolve(psi, potential, dt, steps)` | Split-operator Schrödinger solver. |
| `.tunneling_through_maya()` | Quantum tunneling as penetrating Maya's barrier. Transmission ≈ grace. |
| `.uncertainty_as_maya()` | ΔxΔp ≥ ℏ/2. Ground state saturates the bound. Uncertainty is a property of Maya. |

---

### `quantum/measurement.py` — The Measurement Problem Dissolved

**Class: `AdvaiticMeasurement`**

| Method | Description |
|--------|-------------|
| `.create_superposition()` | System in Brahman state (equal superposition). |
| `.entangle_with_environment(system)` | Decoherence: system entangles with Maya (environment). |
| `.brahman_view(total)` | Paramarthika perspective — total state is pure, purity ≈ 1.0. |
| `.jiva_view(total)` | Vyavaharika perspective — reduced state is mixed, appears classical. |
| `.demonstrate_measurement_problem_resolved()` | Full demo: same state, two views, no collapse. |

---

### `quantum/entanglement.py` — Non-Dual Entanglement

**Class: `NonDualEntanglement`**

| Method | Description |
|--------|-------------|
| `.bell_state(which)` | Create Bell states: Φ+, Φ-, Ψ+, Ψ-. |
| `.entanglement_entropy(state)` | Von Neumann entropy of reduced state. S=0: separable. S=log(d): maximally entangled. |
| `.bell_inequality_violation()` | CHSH test. S = -2.828 (= -2√2), violating classical bound of 2. |
| `.monogamy_of_entanglement()` | More entanglement with B → less with C. Liberation requires full identification with Brahman. |
| `.non_duality_demonstration()` | Separable entropy vs. entangled entropy proves non-duality. |

---

### `gravity/metric.py` — Spacetime Metric from Entanglement

**Class: `ConsciousnessMetric`**

| Method | Description |
|--------|-------------|
| `.build_entanglement_structure(maya_depth)` | Correlation matrix between spatial points. maya=0: all connected. maya=1: all separate. |
| `.entanglement_to_distance(C)` | d(i,j) = -log(C(i,j)). Ryu-Takayanagi prescription. |
| `.derive_metric(maya_depth)` | Full metric tensor via MDS embedding + local Jacobian. |
| `.demonstrate_space_from_entanglement()` | Shows: maya=0 → no space. maya=1 → expanded spacetime. |

---

### `gravity/einstein.py` — Emergent Einstein Equations

**Class: `EmergentEinstein`**

| Method | Description |
|--------|-------------|
| `.consciousness_entropy(region)` | Entanglement entropy of a region (Maya's depth). |
| `.maya_temperature(acceleration)` | Unruh temperature T = a/(2π). Acceleration = deeper identification = more Maya. |
| `.clausius_to_einstein(energy, entropy)` | δQ = TdS → G_μν = 8πG T_μν. Returns correlation between curvature and energy. |
| `.demonstrate_gravity_from_consciousness()` | Full pipeline: field → entropy → curvature → Einstein equations. |

---

### `gravity/entropic.py` — Verlinde's Entropic Gravity

**Class: `EntropicGravity`**

| Method | Description |
|--------|-------------|
| `.entropic_force(mass, radius)` | F = T × dS/dr. Gravity as entropy gradient. |
| `.recover_newton(mass)` | Shows F_entropic recovers F = GMm/r². Newton correlation > 0.93. |
| `.black_hole_as_maximum_maya(mass)` | Schwarzschild radius, Bekenstein-Hawking entropy, Hawking temperature. Even maximum Maya eventually dissolves. |

---

### `gravity/holographic.py` — The Holographic Principle

**Class: `HolographicBoundary`**

| Method | Description |
|--------|-------------|
| `.boundary_state(complexity)` | The boundary state — pure consciousness (Brahman). No gravity, no spacetime. |
| `.holographic_projection(boundary)` | Project boundary → bulk. Maya creating spacetime from consciousness. |
| `.ryu_takayanagi(boundary)` | S(A) = Area(γ_A)/(4G). Entanglement entropy = area of minimal surface. |
| `.demonstrate_holographic_principle()` | Full demo: boundary → bulk projection → reconstruction fidelity. |

---

### `particles/symmetry_breaking.py` — Maya as Symmetry Breaking

**Class: `MayaSymmetryBreaking`**

| Method | Description |
|--------|-------------|
| `.unified_symmetry()` | Fully symmetric state — Brahman before Maya. |
| `.mexican_hat_potential(field)` | V(φ) = μ²\|φ\|² + λ\|φ\|⁴. The potential driving differentiation. |
| `.break_symmetry(temperature)` | Phase transition: T > T_c (Brahman, symmetric) → T < T_c (Maya, broken). |
| `.particle_spectrum_from_breaking()` | Maps Standard Model particles to symmetry breaking modes. |

---

### `particles/particle_zoo.py` — Particles as Nama-Rupa

**Class: `ParticleFromMaya`** (dataclass)

17 Standard Model particles, each with:

| Field | Description |
|-------|-------------|
| `mass_MeV` | Mass in MeV — how much Maya "weighs it down" |
| `charge` | Electromagnetic charge — how it interacts with Maya's illumination |
| `spin` | Intrinsic rotational symmetry |
| `color_charge` | Strong force charge — confinement by Maya |
| `generation` | 1 (Sattva), 2 (Rajas), or 3 (Tamas) |
| `maya_depth` | Computed: 0.0 (Brahman) to 1.0 (deep Maya) |

**Function: `analyze_particle_zoo()`** — Returns sorted analysis: closest to Brahman (neutrinos) vs. deepest in Maya (top quarks).

---

### `particles/forces.py` — Four Forces as Maya's Aspects

**Class: `FundamentalForces`**

| Method | Description |
|--------|-------------|
| `.coupling_running(energy)` | RG running of coupling constants. Forces converge at high energy. |
| `.demonstrate_unification()` | Shows convergence near 10¹⁵ GeV. |
| `.force_as_maya_aspect()` | Maps each force to a specific Maya function (geometry, illumination, transformation, binding). |

---

### `constants/derivation.py` — Physical Constants from Consciousness

**Class: `ConstantsFromConsciousness`**

| Method | Description |
|--------|-------------|
| `.self_reference_fixed_point()` | φ, e, π from fixed-point iterations of self-referential functions. |
| `.information_theoretic_constants()` | log(2), log(3), holographic bound from consciousness information theory. |
| `.consciousness_geometry_constants()` | Feigenbaum constants, fine structure attempts, Mandelbrot dimension. |
| `.attempt_mass_ratios()` | Koide formula: (m_e+m_μ+m_τ)/(√m_e+√m_μ+√m_τ)² = 0.6666 ≈ 2/3. |

---

### `constants/fine_structure.py` — The Fine Structure Constant

**Class: `FineStructureDerivation`**

| Method | Description |
|--------|-------------|
| `.attempt_geometric()` | Multiple geometric approaches to deriving α ≈ 1/137. |
| `.attempt_information_theoretic()` | 7 bits + self-reference corrections → 1/α ≈ 131 (4.4% error). |
| `.demonstrate_alpha_significance()` | What α controls and what would change if it differed. |

---

### `constants/cosmological.py` — The Cosmological Constant

**Class: `CosmologicalConstant`**

| Method | Description |
|--------|-------------|
| `.vacuum_energy_problem()` | The 10¹²⁰ discrepancy between QFT and observation. |
| `.consciousness_resolution()` | Λ ∝ 1/S_total ≈ 10⁻¹²² — matches observation. |
| `.dark_energy_as_residual_maya()` | 68.3% dark energy = Avarana Shakti at cosmic scale. |

---

### `predictions/testable.py` — 5 Testable Predictions

**Class: `TestablePredictions`**

See [docs/PREDICTIONS.md](PREDICTIONS.md) for full details on P1–P5.

---

### `falsification/criteria.py` — 5 Falsification Criteria

**Class: `FalsificationCriteria`**

See [docs/PREDICTIONS.md](PREDICTIONS.md) for full details on F1–F5.

---

### `falsification/experiments.py` — Critical Experimental Designs

**Class: `CriticalExperiments`**

5 experimental designs (E1–E5) with protocols, timelines, and feasibility assessments.

---

### `visualizations/maya_visualizer.py` — 7 Visual Models

**Class: `MayaVisualizer`**

| Method | Output File | What It Shows |
|--------|------------|---------------|
| `.plot_unity_to_multiplicity()` | `unity_to_multiplicity.png` | Brahman → Maya differentiation → back to unity |
| `.plot_rope_snake()` | `rope_snake.png` | Superimposition at 6 ignorance levels |
| `.plot_guna_dynamics()` | `guna_dynamics.png` | Sattva/Rajas/Tamas cycling over 200 steps |
| `.plot_neti_neti()` | `neti_neti.png` | 8 layers stripped in Neti-Neti process |
| `.plot_three_levels()` | `three_levels.png` | Paramarthika vs. Vyavaharika vs. Pratibhasika |
| `.plot_fractal_unity()` | `fractal_unity.png` | Mandelbrot zoom — same pattern at every scale |
| `.plot_emergent_spacetime()` | `emergent_spacetime.png` | 0→1→2→3 dimensions from self-reference |
