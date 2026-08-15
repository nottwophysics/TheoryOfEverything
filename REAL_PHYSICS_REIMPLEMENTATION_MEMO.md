# Design memo — reimplementing the withdrawn demos as real computations

**Date:** 2026-08-15 (pre-registered before implementation; acceptance criteria
frozen here). Follow-up to the 2026-08-15 adversarial review, which withdrew
four headline demonstrations as circular, inert, or overstated. This memo
specifies what the replacements must ACTUALLY compute, with negative controls
that would catch a regression to the old defects. A claim ships only if its
acceptance test passes; a track that cannot meet its criteria reports failure
honestly rather than shipping a weaker construction under the same label.

Ground rules for every track:
- No hardcoded verdict booleans: every flag in a return dict is computed.
- Every headline number must be able to come out differently (mechanical
  check A), be computed inside the loop that varies its inputs (check B),
  and consume its inputs (check C).
- Each track adds its own new test file; shared test files are not edited by
  implementers (integration reconciles them).
- Deterministic seeds; each module's demo runs in seconds, not minutes.

---

## Track A — `quantum/error_correction.py`: a real [[5,1,3]] stabilizer code

Replaces: the "80% boundary erasure" claim (loop-bound artifact, near-chance
fidelity). Note the old claim was not merely overstated — recovering from >50%
erasure is impossible by no-cloning.

Implement the five-qubit perfect code with explicit statevectors (dim 32):
stabilizers XZZXI and cyclic shifts; logical X̄ = XXXXX, Z̄ = ZZZZZ.

Acceptance (tests in `tests/test_qec_stabilizer.py`):
- **A1** Encoded states are +1 eigenstates of all 4 stabilizers (|⟨S_i⟩−1| < 1e-10).
- **A2** All 15 single-qubit Pauli errors corrected by syndrome lookup:
  post-correction logical fidelity 1 − 1e-10, for ≥3 distinct logical states.
- **A3** Any 2-of-5 erasure (all 10 patterns) recovered exactly: apply random
  Pauli noise on the erased pair (known locations), decode restricted to the
  erased support, fidelity 1 − 1e-10.
- **A4 (negative control)** 3-erasure is UNRECOVERABLE: for some 3-erasure
  pattern, the reduced states of logical |0̄⟩ and |1̄⟩ on the surviving 2 qubits
  are identical (trace distance < 1e-10) — information genuinely absent.
- **A5** Any 3-of-5 subregion reconstructs the logical qubit: reduced states of
  |0̄⟩ vs |1̄⟩ on every 3-qubit subset are perfectly distinguishable (trace
  distance 1 within 1e-10).

Honest headline: erasure threshold **2/5 (40%)**, reconstruction from any
**3/5 (60%)** — replacing "80%".

## Track B — `quantum/tensor_network.py`: a MERA whose tensors act

Replaces: coarse-graining applied as a global phase (physical no-op).

Binary MERA, N = 16 sites, χ = 2: layers of 2-site disentanglers (4×4
unitaries) and 2→1 isometries (4×2, W†W = I), built by QR from seeded
Gaussians, with an entangling-strength parameter λ (λ=1 generic, λ=0
identity/product limit). The boundary state (dim 65536) is constructed
explicitly by descending from a top state, so all claims are computed on an
actual state.

Acceptance (tests in `tests/test_mera_real.py`):
- **B1** Tensor algebra: every U†U = I and W†W = I to 1e-10.
- **B2 (negative control — the old defect inverted)** Replacing any single
  layer's tensors with different random ones changes the boundary state
  (‖Δψ‖ > 0.01). Zeroing tensors must NOT leave the state unchanged.
- **B3 (RT-type bound, computed)** For intervals of length 2, 4, 8: exact
  S(interval) from the state obeys S ≤ ln(χ)·|minimal cut| + 1e-9, with the
  minimal cut counted on the actual network graph. Saturation ratios reported.
- **B4 (disconnection, computed)** As λ → 0, I(left half : right half)
  decreases monotonically over ≥5 values to < 1e-8, and the derived distance
  −ln(I/I₀) grows accordingly.
- **B5** The log-shaped minimal cut is stated as a property of the network
  BY CONSTRUCTION; only B3's inequality on the actual state is claimed as a
  computed result.

## Track C — `gravity/entropic.py`: Verlinde's derivation, faithfully

Replaces: screen-area entropy gradient yielding F = M/r ("not Newton").

Implement the actual chain in SI units: displacement entropy
ΔS = 2π k_B (mc/ħ) Δx; Unruh T = ħa/(2π c k_B); holographic screen
N = A c³/(G ħ), equipartition E = ½ N k_B T = M c². Two independent routes to
F (Unruh-temperature route and screen-equipartition route) must agree and
equal Newton.

Acceptance (tests in `tests/test_entropic_verlinde.py`):
- **C1** |F/(GMm/r²) − 1| < 1e-12 across a grid of M, m, r spanning lab to
  astronomical scales, both routes.
- **C2 (negative control)** The legacy screen-area route is retained as
  `screen_area_route_wrong()` and demonstrably does NOT reproduce Newton
  (ratio varies with r).
- **C3** Programmatic dimensional bookkeeping (exponent tuples over kg, m, s,
  K) verifies F has dimensions kg·m·s⁻².
- **C4** `recover_newton()` keeps its return keys; `newton_recovered` is now
  computed and True because the derivation is faithful, not because the
  criterion moved.

Scope honesty: this makes the code faithful to Verlinde (2011); whether
entropic gravity is correct physics remains open in the literature.

## Track D — discrete geometry and entanglement thermodynamics

Replaces: "Einstein equations recovered" via entropy defined from T₀₀.

- **D1** `gravity/einstein_2d.py` gains `gauss_bonnet_check()`: genuine
  deficit-angle curvature on the Delaunay manifold satisfies
  Σ interior deficits + Σ boundary exterior angles = 2πχ to 1e-9, and the
  module states plainly that the 2D Einstein tensor vanishes identically —
  Gauss–Bonnet is the correct 2D statement. Negative control: removing a
  triangle (changing topology/boundary) shifts the sum as χ dictates.
- **D2** NEW `gravity/entanglement_first_law.py`: free-fermion chain (N≈100,
  half filling), region A (L≈20): exact S(A) from correlation-matrix
  eigenvalues; exact modular Hamiltonian k = ln((1−C_A)/C_A); verify the
  first law of entanglement δS = δ⟨K_A⟩: the mismatch scales as ε²
  (log-log slope 2 ± 0.2 over ε ∈ [1e-3, 1e-1]) and is < 1e-6 at ε = 1e-4.
  Negative control: a deliberately wrong modular Hamiltonian breaks the
  first-order equality. This is the entanglement-thermodynamics kernel behind
  "gravity from entanglement" programs (Faulkner et al. 2013; Jacobson 2015
  entanglement equilibrium) — the honest, computable piece.
- **D3** NEW `gravity/entanglement_geometry.py`: exact TFIM ground state
  (N = 10, dense ED) at criticality and deep in the paramagnet: mutual
  information I(i,j) → distance −ln(I/I_max). Acceptance: I decays
  monotonically with separation at criticality (Spearman ρ(|i−j|, I) < −0.9);
  the near-product state has max I < 1e-2 (no entanglement → no connectivity),
  with a REAL state this time. Negative control: shuffling I destroys the
  distance-separation monotonicity.

Out of scope this round (recorded): einstein_3d.py beyond its existing honest
caveats; variationally optimized MERA; graviton-level claims.

## Integration plan

Experiments keep their numbers (no 31→32 churn): Exp 12 gains D3's real-state
space-from-entanglement + Track C; Exp 19 → Track B; Exp 20 → D1 + D2; Exp 21
→ Track A. Docs statuses move from "withdrawn as evidence" to "reimplemented
(2026-08-15)" ONLY where the acceptance tests pass, with the retraction
history preserved. Test counts in docs updated after the suite stabilizes.
