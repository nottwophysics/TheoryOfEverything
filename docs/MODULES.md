# Module Documentation

## Detailed Reference for Every Module and Class

---

## Metaphysical Foundation Modules

> These modules live under `philosophy/` and are the **interpretive layer** —
> Advaita scaffolding, not empirical physics. See [`philosophy/README.md`](../philosophy/README.md).

---

### `philosophy/brahman/consciousness.py` — The Singular Reality

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

### `philosophy/brahman/sat_chit_ananda.py` — Three Aspects of Brahman

**Class: `SatChitAnanda`**

Three orthogonal projections of the same field, each revealing a different aspect.

| Method | Returns | Advaita Meaning |
|--------|---------|-----------------|
| `.sat()` | Magnitude of the field (np.abs) | Existence — THAT anything IS |
| `.chit()` | Phase angles of the field (np.angle) | Consciousness — the knowing aspect |
| `.ananda()` | Coherence measure (float) | Bliss/Fullness — completeness |
| `.unity_check()` | Dict with reconstruction error | Proves Sat+Chit fully reconstruct the field |

---

### `philosophy/maya/superimposition.py` — Adhyasa

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

### `philosophy/maya/nama_rupa.py` — Name and Form

**Class: `NamaRupa`**

Differentiates a unified field into apparently distinct entities.

| Method | Description |
|--------|-------------|
| `.differentiate(field, num_entities, names)` | Carves the field into named forms. Returns list of `NamedForm`. |
| `.reunify(entities)` | Dissolves all forms back to the source field. |
| `.show_non_separation(entities)` | Proves all forms are made of the same substance. |

---

### `philosophy/maya/gunas.py` — Three Qualities

**Class: `Gunas`**

Models the three fundamental qualities of experience.

| Method | Description |
|--------|-------------|
| `.apply_to_field(field)` | Transform field according to current guna balance. Sattva clarifies, Rajas distorts, Tamas dampens. |
| `.evolve(dt, perturbation)` | Advance the guna balance one time step. |
| `.simulate_cycle(steps)` | Run many steps, returning history of proportions. |
| `.transcend()` | Returns `GunaState.TRANSCENDED` (Nirguna). |

---

### `philosophy/levels/reality_engine.py` — Three Levels of Reality

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

### `philosophy/liberation/neti_neti.py` — "Not This, Not This"

**Class: `NetiNeti`**

Systematic negation of false identifications.

| Method | Description |
|--------|-------------|
| `.inquire()` | Full inquiry — negates all 8 layers. Returns process + final teaching. |
| `.inquire_step_by_step()` | Generator yielding one negation at a time. |

8 layers negated: Physical Body → Vital Energy → Thoughts → Emotions → Memories → Intellect → Ego → Bliss of Deep Sleep. Remainder magnitude → 0.0.

---

### `philosophy/liberation/mahavakya.py` — The Four Great Sayings

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

### `quantum/tensor_network.py` — MERA Tensor Network

**Class: `MERATensorNetwork`**

Models spacetime as a Multiscale Entanglement Renormalization Ansatz where coarse-graining = Maya dissolving.

| Method | Description |
|--------|-------------|
| `MERATensorNetwork(num_sites, bond_dim)` | Build MERA with disentanglers and isometries. Sites must be power of 2. |
| `.coarse_grain(state)` | Full UV→IR coarse-graining. Returns entanglement at each layer. |
| `.entanglement_determines_distance()` | Distance ∝ 1/entanglement. Shows geometry from entanglement. |
| `.cut_entanglement_disconnects_space()` | Entangled state → space connected. Product state → space disconnected. |
| `.holographic_geometry()` | Maps layers to AdS radial slices. Metric factor = L²/z². |
| `.full_demonstration()` | Run all four demonstrations. |

---

### `quantum/error_correction.py` — QEC as Spacetime

**Class: `HolographicCode`**

Models spacetime as a quantum error-correcting code (Almheiri-Dong-Harlow).

| Method | Description |
|--------|-------------|
| `HolographicCode(n_physical, k_logical)` | Build holographic code with random isometric encoding. |
| `.encode(logical_state)` | Encode logical (Brahman) state into physical (Maya) space. |
| `.erase_qubits(physical_state, qubits)` | Erase specific qubits — model partial ignorance (Avidya). |
| `.recover_logical(rho_physical)` | Attempt to recover bulk from (corrupted) boundary. |
| `.test_error_correction(logical_state)` | Test recovery at increasing erasure levels. |
| `.demonstrate_spacetime_as_code()` | Full demo: error correction + distinguishability + entanglement. |

**Class: `SubsystemCode`**

| Method | Description |
|--------|-------------|
| `.reconstruct_from_subregion(qubits)` | Try recovering bulk from a boundary subregion. |
| `.demonstrate_multiple_reconstructions()` | Same bulk from left/right/even/odd boundary — multiple paths to Brahman. |

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

**Status**: 1D proof-of-concept. See `gravity/einstein_2d.py` for the 2+1D upgrade.

---

### `gravity/einstein_2d.py` — 2+1D Einstein Equations (Upgraded)

**Class: `EmergentEinstein2D`**

Jacobson's thermodynamic derivation on a proper 2D discrete manifold (Delaunay triangulation). **Major upgrade from the 1D model.**

| Method | Description |
|--------|-------------|
| `EmergentEinstein2D(num_points, seed)` | Build discrete 2D manifold via Delaunay triangulation. |
| `.consciousness_energy_density(positions, values)` | Gaussian mass distributions on the manifold. |
| `.entanglement_entropy_field(T_00)` | Bekenstein-bound entropy + neighbor entanglement. |
| `.discrete_ricci_scalar(S)` | Deficit angle (geometric) + integrated entropy (Jacobson) curvature. |
| `.derive_einstein_equations(positions, values)` | Full derivation: T_μν → S → R → test R ∝ T. |
| `.demonstrate_mass_curves_space()` | 0, 1, and 2 mass comparisons. |

**Key result**: R_entropy vs T_00 correlation = **0.94** (two masses) on 80-point manifold with 149 triangles.

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

## Numerology Modules (candidly walled off)

> The `numerology/` package holds the fine-structure "derivations." They are
> **numerical curve-fitting presented honestly as such**, not physics — moved out
> of `constants/` and renamed so they can be judged on their own terms. The two
> hold-out modules below (`cross_validation.py`, `look_elsewhere.py`) exist
> precisely to show why: a genuine law predicts a *second* constant with no
> re-tuning, and survives a look-elsewhere correction. These do not.

---

### `numerology/derivation.py` — Physical Constants from Consciousness

**Class: `ConstantsFromConsciousness`**

| Method | Description |
|--------|-------------|
| `.self_reference_fixed_point()` | φ, e, π from fixed-point iterations of self-referential functions. |
| `.information_theoretic_constants()` | log(2), log(3), holographic bound from consciousness information theory. |
| `.consciousness_geometry_constants()` | Feigenbaum constants, fine structure attempts, Mandelbrot dimension. |
| `.attempt_mass_ratios()` | Koide formula: (m_e+m_μ+m_τ)/(√m_e+√m_μ+√m_τ)² = 0.6666 ≈ 2/3. |

---

### `numerology/fine_structure.py` — The Fine Structure Constant

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

### `numerology/fine_structure_v2.py` — Fine Structure Constant (v2, Systematic)

**Classes**: `FineStructureFromMERA`, `FineStructureFromTopology`, `FineStructureFromSelfReference`, `FineStructureFromModular`, `FineStructureV2`

Systematic exploration of 6 approaches to derive α ≈ 1/137.036.

| Class | Method | Best Result |
|-------|--------|-------------|
| `FineStructureFromMERA` | `.rg_fixed_point_ratio()` | RG ratio → 1/α (high error) |
| `FineStructureFromTopology` | `.chern_weil_approach()` | n=69 → 1/α=138 (0.70% error) |
| `FineStructureFromSelfReference` | `.logistic_map_approach()` | Feigenbaum constants |
| `FineStructureFromSelfReference` | `.continued_fraction_approach()` | CF analysis of 1/α |
| `FineStructureFromSelfReference` | `.golden_ratio_approach()` | φ-based formulas |
| `FineStructureFromModular` | `.dedekind_eta_approach()` | **163-26+π/100 → 0.003% error** |

**Class: `FineStructureV2`** — Orchestrator

| Method | Description |
|--------|-------------|
| `.run_all_approaches()` | Run all 6 approaches, rank by accuracy, report best result. |

**Key result**: 1/α ≈ 163 - 26 + π/100 = 137.031 (0.003% error). Connects Heegner number 163, bosonic string dimension 26, and Monster group.

---

### `numerology/fine_structure_v3.py` — Fine Structure Constant (v3, Rigorous)

**Classes**: `ModularBootstrap`, `HolographicAlpha`, `SelfReferentialAlpha`, `FineStructureV3`

The most careful of the three attempts: modular-bootstrap, holographic, and
self-referential routes to α ≈ 1/137.036, each reporting its own error honestly.

| Method | Description |
|--------|-------------|
| `.run_all_approaches()` | Run every v3 route, rank by accuracy, and report the residual error of each. |

**Framing**: v3 tightens the arithmetic but does not change the verdict — see the
two hold-out tests below, which are the actual arbiters of whether any of this is
physics or coincidence.

---

### `numerology/cross_validation.py` — Hold-Out Cross-Validation

**Class: `CrossValidation`**

A genuine formula-generating *principle* can be fixed on one constant and then
**predict a second, independent constant with no re-tuning**. This module runs
that standard hold-out test on the fine-structure "rule."

| Method | Description |
|--------|-------------|
| `.fit_on(constant)` | Tune the recipe's free integers on a single target constant. |
| `.predict_held_out(recipe)` | Apply the fitted recipe, unchanged, to a different constant. |
| `.run()` | Full fit → predict → report. Reports the held-out error (large → curve-fit). |

**Key result**: the recipe fitted on 1/α does **not** transfer — the held-out
prediction is off by orders of magnitude more than the in-sample "hit." Produces
`alpha_cross_validation.png`.

---

### `numerology/look_elsewhere.py` — Look-Elsewhere Analysis

**Class: `LookElsewhere`**

Counts how many equally-simple integer/π/e expressions land within the same
tolerance of 1/α by chance, quantifying the multiple-comparisons ("look-elsewhere")
penalty behind the `163 - 26 + π/100` coincidence.

| Method | Description |
|--------|-------------|
| `.enumerate_expressions(depth)` | Generate the space of comparably-simple candidate formulas. |
| `.count_near_hits(tolerance)` | How many land as close as the reported "derivation." |
| `.run()` | Full sweep + report of the effective trials factor. |

**Key result**: many independent simple expressions hit 1/α to the same
precision, so the near-match carries little evidential weight. Produces
`alpha_look_elsewhere.png`.

---

### `constants/koide.py` — Koide Relation (Verification, NOT Derivation)

**Class: `KoideRelation`**

The Koide relation is an empirical near-coincidence among the charged-lepton
masses: Q = (mₑ+m_μ+m_τ)/(√mₑ+√m_μ+√m_τ)² ≈ 2/3. This module **verifies** it
against measured masses and states plainly that the framework does not *derive*
it. (Split out of the old `constants/derivation.py` so verification is not
mistaken for derivation.)

| Method | Description |
|--------|-------------|
| `.compute_Q(masses)` | Evaluate Q from the three measured lepton masses (with uncertainties). |
| `.distance_from_two_thirds()` | How close Q sits to 2/3, in σ. |
| `.verify()` | Full report: value, error bars, and an explicit "not derived here" note. |

---

### `predictions/iit_bridge.py` — IIT-Entanglement Bridge

**Classes**: `IntegratedInformation`, `EntanglementEntropy`, `IITEntanglementBridge`

Formally bridges Tononi's IIT (consciousness measure Φ) with quantum entanglement entropy (S).

**Class: `IntegratedInformation`**

| Method | Description |
|--------|-------------|
| `.compute_phi(connectivity, state)` | Compute Φ by finding the Minimum Information Partition. |

**Class: `EntanglementEntropy`**

| Method | Description |
|--------|-------------|
| `.von_neumann_entropy(rho)` | S(ρ) = -Tr(ρ log ρ). |
| `.entanglement_entropy(state, partition)` | S for a bipartition via partial trace. |
| `.total_entanglement(state)` | Average S over all bipartitions. |

**Class: `IITEntanglementBridge`**

| Method | Description |
|--------|-------------|
| `.test_conjecture(num_trials)` | Test Φ ≤ S across random systems. Returns hold rate, correlation, ratio. |
| `.demonstrate_extremes()` | Disconnected (Φ=0,S=0), half (Φ=0,S=0.32), full (Φ=0.03,S=0.69). |
| `.mera_consciousness_profile()` | Compute Φ at each MERA layer. Prediction: Φ increases toward IR (Brahman). |
| `.full_demonstration()` | Run all tests + generate testable predictions. |

**Key result (superseded — circular).** This module reports Φ ≤ S holding in 100%
of 50 trials with Φ rising toward the MERA IR. That result is an artifact.

> **⚠️ The bound is falsified by a validated test.** The original test is
> *circular* — it draws both Φ and S from the same scalar (total connectivity of
> one random matrix), and `compute_phi` is a "simplified IIT-like" measure, not
> canonical IIT Φ (`pyphi_benchmark.py` finds them uncorrelated, r ≈ −0.01).
> `iit_entanglement_rigorous.py` removes the circularity; the **validated** rebuild
> (`phi_s_systems.py` + `validated_phi.py` + `entanglement_entropy.py`: canonical
> PyPhi Φ vs. transverse-field Ising ground-state entanglement from the same
> couplings, N = 216, seed 42; numbers per the 2026-08-12 TPM-ordering audit)
> **refutes Φ ≤ S** — the 77% hold rate is almost entirely the trivial Φ = 0
> systems and equals the permutation null (0.7685 vs 0.7789), while **50 of the
> 51 nonzero-Φ systems violate the bound** (canonical Φ up to ≈ 4.0 bits is not
> capped by the bipartition entropy that limits S at ≈ 0.83 bits). The raw Φ–S
> correlation (r ≈ +0.64) is a **connectivity confound**: controlling for
> connectivity collapses it to r ≈ −0.07 (p = 0.29; with system size, +0.06,
> p = 0.38), so **no residual Φ–S association survives** — §8 retains no claim.

---

### `predictions/iit_entanglement_rigorous.py` — Non-Circular Φ/S Bridge

**Class: `RigorousIITEntanglementBridge`**

Re-runs the Φ ≤ S test **without the circularity**: Φ is computed from a system's
causal structure and S from an *independently prepared* quantum state, so a
correlation (if any) is not built in by construction. Includes a null control.

| Method | Description |
|--------|-------------|
| `.independent_phi_and_S(trials)` | Draw Φ and S from separate sources; record both. |
| `.null_control(trials)` | Shuffle the pairing to establish the chance baseline. |
| `.test_conjecture(trials)` | Compare observed Φ–S relationship against the null. |

**Purpose**: tells apart a real Φ ≤ S regularity from an artifact of sharing one
random scalar between the two quantities.

---

### `predictions/pyphi_benchmark.py` — Framework Φ vs Canonical IIT Φ

**Class: `PyPhiBenchmark`**

Tests the implicit claim that `iit_bridge.compute_phi` approximates the Φ that
IIT actually defines, by comparing it system-for-system against **PyPhi 1.2.0**
(Mayner et al., *PLOS Comput. Biol.* 2018, `10.1371/journal.pcbi.1006343`), the
reference IIT 3.0 implementation. Runs offline against checked-in fixtures
(`tests/fixtures/pyphi_benchmark_{framework,reference}.json`) so PyPhi need not be
installed to reproduce the comparison.

| Method | Description |
|--------|-------------|
| `.canonical_networks()` | PyPhi's own example networks + small XOR-logic systems (3–5 nodes). |
| `.compare(system)` | Framework Φ vs PyPhi Φ for a single system with a reachable state. |
| `.run(regenerate=False)` | Full benchmark; by default reads fixtures, optionally recomputes. |

**Purpose**: quantifies how far the "simplified IIT-like" measure sits from
canonical Φ, so the docstring's implied equivalence can be judged.

---

### `predictions/decoherence_calculator.py` — Decoherence-Threshold Calculator

**Class: `DecoherenceCalculator`**

Turns prediction **P2** into a real quantitative tool. Interference is visible
only where gravitational (Diósi–Penrose) collapse is faster than *every*
environmental decoherence channel, yet still slow enough to run an experiment.
This computes all three channels and finds that window.

| Channel | Formula | Reference |
|---------|---------|-----------|
| Gravitational (DP) | τ = ħ / ΔE_grav (uniform-sphere self-energy) | Diósi 1989 `10.1103/PhysRevA.40.1165`; Penrose 1996 `10.1007/BF02105068` |
| Gas collisions | τ = 1/(n v̄ σ) | Joos & Zeh 1985 `10.1007/BF01725541` |
| Thermal photons | τ = 1/(Λ Δx²), Λ = 8.55 ζ(9) c R⁶ (k_BT/ħc)⁹ | Schlosshauer 2005 `10.1103/RevModPhys.76.1267` |

| Method | Description |
|--------|-------------|
| `.dp_time(radius, delta_x)` | Gravitational collapse time for a sphere superposed at separation Δx. |
| `.gas_time(radius, pressure, T)` | Collisional decoherence time. |
| `.photon_time(radius, delta_x, T)` | Thermal-photon decoherence time. |
| `.observable_window(...)` | Mass/pressure/temperature region where DP collapse wins. Produces `decoherence_envelopes.png`. |

---

### `quantum/gleason.py` — Gleason's Theorem (Born Rule as Theorem)

**Class: `GleasonVerification`**

The framework's most rigorous module. Verifies Gleason's theorem applies to the Brahman Hilbert space and proves the Born rule is the unique consistent probability measure.

| Method | Description |
|--------|-------------|
| `GleasonVerification(dimension)` | Initialize with dimension ≥ 3 (raises error for dim < 3). |
| `.verify_conditions(state)` | Verify all 4 Gleason conditions: C1 (dim≥3), C2 (non-negativity, 500 tests), C3 (additivity, 200 tests), C4 (normalization). |
| `.demonstrate_uniqueness(state)` | Test Born rule vs alternatives (amplitude, quartic). Born: 0/1800 violations. Alternatives: 1800/1800 violations. |
| `.demonstrate_dim2_exception()` | Show dim=2 allows non-Born measures (qubits CAN have hidden variables). Dim≥3: Kochen-Specker fails 25.6%. |
| `.axiom_reduction_proof()` | Full proof chain: Sat-Chit-Ananda → Hilbert space → Gleason → Born rule → axiom reduction 7→4. |
| `.full_demonstration()` | Run all four demonstrations. |

**Key result**: Copenhagen has 7 axioms. Advaita has 4 independent axioms (Born rule is a theorem, not an axiom).

---

### `quantum/interpretations.py` — Four QM Interpretations Compared

**Classes**: `Copenhagen`, `ManyWorlds`, `PilotWave`, `AdvaitaInterpretation`, `InterpretationComparison`

Each interpretation class defines:
- Axioms (with count)
- Answers to 8 phenomena (with mechanisms, advantages, problems)
- What it cannot explain
- Novel predictions

**Class: `InterpretationComparison`**

| Method | Description |
|--------|-------------|
| `.axiom_comparison()` | Compare axiom counts. Ranking by Occam's razor. |
| `.explanatory_scope()` | Count phenomena addressed, with/without problems. |
| `.novel_predictions_comparison()` | Compare unique predictions per interpretation. |
| `.consciousness_comparison()` | Who addresses the hard problem? |
| `.empirical_agreement()` | Verify all 4 agree on observables (P(up), P(down)). |
| `.advaita_measurement_demo()` | Quantitative measurement resolution: purity 1.0 vs 0.58. |
| `.summary_table()` | The final comparison table across all criteria. |

---

### `quantum/interpretation_experiment.py` — Shared Experimental Setup

**Class: `QuantumSetup`** — The physical scenario all interpretations must explain (spin-1/2, α²=0.7, β²=0.3, Bell state).

**Dictionary: `PHENOMENA`** — 8 phenomena (P1–P8) with questions and observables that every interpretation must address.

---

### `quantum/operational_equivalence.py` — Everett-Advaita Equivalence Proof

**Class: `OperationalEquivalence`**

Proves the paper's central claim: Everett and Advaita make identical empirical predictions.

| Method | Description |
|--------|-------------|
| `.test_probabilities()` | Born rule probabilities identical under both interpretations. |
| `.test_time_evolution()` | Unitary evolution at 5 time steps — identical states. |
| `.test_measurement_statistics(num_trials)` | 10,000 measurement outcomes — identical distributions. |
| `.test_entanglement_correlations()` | Bell CHSH = -2.83, entanglement entropy — identical. |
| `.test_decoherence()` | Total purity, reduced purity, pointer states — identical. |
| `.test_where_they_diverge()` | Documents 5 ontological divergences with 0 measurable consequences. |
| `.full_equivalence_test()` | Run all 6 tests. Summary: 5/5 empirical identical, 5 ontological divergences. |

---

### `quantum/perspectival_asymmetry.py` — Generalized Measurement Resolution

**Class: `PerspectivalAsymmetry`**

Proves that "total pure, reduced mixed" holds for ALL quantum scenarios, not just one example.

| Method | Description |
|--------|-------------|
| `.test_varying_states(num_states)` | 20 states (equal, biased, random, basis) — all total pure. |
| `.test_varying_environment_size()` | Environment dim 3–64 — total purity 1.0 for all. |
| `.test_varying_basis()` | 5 random measurement bases — perspectival asymmetry in every basis. |
| `.test_asymmetry_is_exact()` | 100 random states — max deviation from purity 1.0: 8.88×10⁻¹⁶. |
| `.full_test()` | Run all 4 tests. Summary: perspectival asymmetry is exact. |

---

### `quantum/observer_centrality.py` — Hidden Premise Demonstration

**Class: `ObserverCentrality`**

Demonstrates the paper's hidden premise: observer ontology is part of the interpretive burden.

| Method | Description |
|--------|-------------|
| `.step1_decoherence_selects_basis()` | Standard physics: pointer states selected, coherence = 0. |
| `.step2_decoherence_does_not_select_outcome()` | Gap: P(↑)=0.5, P(↓)=0.5, but which is experienced? Undefined. |
| `.step3_observer_required_for_outcomes()` | All 4 interpretations invoke "observer" — only Advaita analyzes it. |
| `.step4_unanalyzed_observer_is_a_gap()` | Formalism determines 5 things, leaves 4 open — all involving observer. |
| `.full_demonstration()` | Run all 4 steps. Argument chain → observer ontology is not optional. |

---

### `quantum/unity_of_experience.py` — Experiential Underdetermination

**Class: `UnityOfExperience`**

Quantitatively supports the paper's §4.3.2(b) claim: decoherence fixes the reduced density matrix ρ_SA but does NOT fix experiential ontology. Multiple, pairwise-incompatible interpretations — Everett-unified, Everett-superposed, Copenhagen-classical, consciousness-primitive — all map to the same ρ_SA while disagreeing on the cardinality of unified experience.

| Method | Description |
|--------|-------------|
| `.post_measurement_state(amplitudes)` | Build entangled S+A+E pure state with orthogonal pointer environment. |
| `.reduced_SA(state_bundle)` | Trace out the environment to obtain ρ_SA. |
| `.einselection_diagnostic(rho_sa)` | Verify pointer-basis diagonality (off-diagonal norm < 10⁻¹⁰). |
| `.everett_unified_map(...)` | Branches-as-unified-experiences interpretation; cardinality = N. |
| `.everett_superposed_map(...)` | Non-unified-experience interpretation; cardinality = 0. |
| `.copenhagen_classical_map(...)` | Collapse-to-one-classical-outcome; cardinality = 1. |
| `.subject_modes_map(...)` | One subject, N perspective-modes; cardinality = 1. |
| `.underdetermination_test()` | Confirm 4 interpretations consistent with same ρ_SA, distinct cardinalities. |
| `.sweep_robustness(n_trials)` | Repeat across random amplitude profiles (default 30/30 pass). |
| `.run_all()` | Orchestrator. Returns full report supporting paper §4.3.2(b). |

Companion technical note: [`docs/GLEASON_PROBABILITY_GAP.md`](GLEASON_PROBABILITY_GAP.md) addresses the related Kent (2010) and Baker (2007) critiques of Gleason-based Born rule derivations.

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

---

## Test Suite

---

### `tests/` — 306 Automated Tests

Every module above has a corresponding test file. Tests validate mathematical properties, physical results, and framework invariants. Run with `pytest tests/ -v`.

| Test File | Module(s) Tested | Tests | Key Validations |
|-----------|-----------------|-------|-----------------|
| `test_brahman.py` | philosophy/brahman/ | 20 | Singleton pattern, field normalization, coherence = 1.0, self-reference, Atman=Brahman equality |
| `test_maya.py` | philosophy/maya/ | 30 | Superimposition at varying ignorance, clarity threshold, guna normalization/evolution, nama-rupa non-separation |
| `test_levels.py` | philosophy/levels/ | 22 | Three-level routing, sublation chain, entropy non-negativity, entity counting, invalid state raises |
| `test_emergence.py` | emergence/ | 23 | Metric symmetry, diagonal=0, curvature bounds, substrate preservation, witness immutability |
| `test_liberation.py` | philosophy/liberation/ | 11 | 8-layer negation, remainder→0, step-by-step generator, mahavakya structure and overlap |
| `test_quantum.py` | quantum/ | 63 | Normalization, orthogonality, Hermiticity, [a,a†]=I, Gleason C1–C4, Born uniqueness, Bell S=2√2, decoherence, ER=EPR, **experiential underdetermination (Exp 30)** |
| `test_gravity.py` | gravity/ | 23 | Correlation matrix symmetry, distance properties, R-T correlation, Newton recovery (r>0.9), 2+1D & 3+1D deficit-angle curvature |
| `test_constants.py` | constants/ | 18 | Cosmological constant resolution, Koide ~2/3 verification with error bars |
| `test_particles.py` | particles/ | 13 | Unified symmetry normalization, guna-generation mapping, maya depth bounds |
| `test_predictions.py` | predictions/, falsification/ | 16 | Prediction structure, falsifier completeness, experiment designs |
| `test_numerology.py` | numerology/ | 6 | Fine-structure recipe families reproduce their reported hits; main.py demo runs |
| `test_cross_validation.py` | numerology/ | 3 | Fit-on-one / predict-another hold-out fails as expected (curve-fit, not law) |
| `test_iit_rigorous.py` | predictions/ | 4 | Non-circular Φ/S bridge behaves vs. null control |
| `test_pyphi_benchmark.py` | predictions/ | 5 | Framework Φ vs canonical PyPhi Φ against checked-in fixtures (no PyPhi needed) |
| `test_decoherence_calculator.py` | predictions/ | 8 | DP vs gas vs thermal-photon channels; physics-limit sanity checks |

**Test isolation**: The `conftest.py` fixture resets the Brahman singleton before each test, preventing state leakage.

**Configuration**: `pyproject.toml` defines pytest settings (test paths, naming conventions, verbose output).
