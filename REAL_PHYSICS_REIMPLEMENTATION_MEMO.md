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

---

# RESULTS (2026-08-15, recorded after implementation against the frozen criteria above)

Four independent implementer tracks, each adversarially verified by a separate
reviewer that re-derived the numbers rather than trusting the implementer.
**All four verifiers returned PASS. 22 of 23 frozen criteria pass; 1 fails and
is recorded as a failure, not renegotiated.**

## Track A — [[5,1,3]] stabilizer code: 5/5 PASS
- A1 max |⟨S_i⟩−1| = 2.2e-16 (4 logical states × 4 stabilizers).
- A2 all 15 single-qubit Paulis corrected, worst fidelity 1.0 over 60 cases; 16 distinct syndromes.
- A3 all 10 two-erasure patterns recovered, worst fidelity 1.0 over 760 cases.
- A4 (negative control) 3-erasure: trace distance between logical states on the
  survivors = 0.0 for **all 10** patterns (memo asked for one) — information
  genuinely absent, as no-cloning requires.
- A5 every 3-of-5 subregion reconstructs the logical qubit (trace distance 1.0).
- **Headline change: "80% boundary erasure" → erasure threshold 2/5 (40%),
  reconstruction from any 3/5 (60%).** The old figure was not merely
  unsupported; >50% erasure recovery is impossible.
- Independent verifier rebuilt the code from its own stabilizer projector with a
  random fiducial state and confirmed the same code space (residual < 4e-16),
  distance exactly 3, and every acceptance number.

## Track B — real binary MERA: 5/5 PASS
- B1 max |U†U−I| = 2.2e-15, |W†W−I| = 2.0e-15 over 15 disentanglers/15 isometries.
- B2 (the old defect inverted) replacing any single layer moves the state:
  ‖Δψ‖ = 1.31, 1.28, 1.46, 1.42 by layer; phase-invariant distances 1.05–1.41,
  so a global-phase no-op cannot pass. **The retired implementation scored 0 here.**
- B3 exact S(interval) ≤ ln(χ)·|min cut| for lengths 2/4/8 (saturation
  0.874 / 0.691 / 0.613), cut computed by max-flow on the real contraction graph.
  (Corrected 2026-08-15: the length-8 figure was first recorded as 0.581; the
  committed code returns 0.6133. Re-derived at correction time.)
- B4 I(L:R) = 5.10 → 4.80 → 3.06 → 1.73 → 0.66 → 0.0 over six λ values, → 0 exactly at λ=0.
  **Scope limit found by the verifier: monotonicity is a property of this grid;
  I(λ) is not globally monotone near λ=1. The docs must say "on this grid".**
- B5 the log-shaped minimal cut is labeled by-construction, not as a result.

## Track C — faithful Verlinde derivation: 4/4 PASS
- C1 |F/(GMm/r²) − 1| ≤ 3.3e-16 for both routes across M ∈ [1, 2e30] kg,
  m ∈ [1e-3, 1e3] kg, r ∈ [0.1, 1.5e11] m.
- C2 legacy screen-area route retained and still fails Newton (ratio spread 1e14).
- C3 computed dimension tuples: both routes give (1,1,−2,0) = kg·m·s⁻².
- C4 `newton_recovered` now computed True because the derivation is faithful.
- **Honesty notes added post-verification:** Route 1 takes a = GM/r² as input, so
  it is F = ma by construction and is NOT an independent derivation; only Route 2
  (holographic screen + equipartition) derives the r-dependence. And the
  machine-precision agreement is ALGEBRAIC — it confirms the implementation, not
  nature. Whether entropic gravity is correct physics remains open.

## Track D — discrete geometry + entanglement thermodynamics: 8/9 (one honest FAIL)
- D1 Gauss–Bonnet residual 5.3e-15 (χ computed from the mesh as V−E+F, not
  hardcoded); topology negative control shifts the sum by exactly 2π when χ: 1→0.
  Module states plainly that the 2D Einstein tensor vanishes identically.
- D2 entanglement first law δS = δ⟨K_A⟩ on a free-fermion chain: log-log slope
  **2.0178** (criterion 2 ± 0.2), mismatch 1.6e-10 at ε=1e-4 (criterion 1e-6);
  wrong-modular-Hamiltonian control gives slope 1.01 and ~5000× the mismatch.
- D3 criticality: Spearman ρ(|i−j|, I) = **−0.9891** (criterion < −0.9).
- **D3 paramagnet criterion FAILS: max I = 1.41e-2 at g = 8.0, against the frozen
  threshold of 1e-2.** Confirmed by two independent reduced-density-matrix
  implementations and consistent with perturbation theory (amplitude J/4g = 1/32).
  The threshold is met only for g ≳ 10. **The criterion was NOT weakened to
  manufacture a pass** — the test is committed as an `xfail` carrying this
  explanation, so the failure stays visible in every future test run.

## Integration performed (PARTIAL — see the gap recorded below)
`main.py` Experiments 19 and 21 rewritten against the real APIs (both previously
crashed on retired signatures); Experiment 12's "fails honestly" banner removed
since the derivation now succeeds; two obsolete shared tests in
`tests/test_gravity.py` replaced — `test_unruh_temperature` now checks the SI
formula and linearity in acceleration, and the old
`test_recover_newton_honestly_reports_failure` is superseded by
`test_recover_newton` plus a retained negative control asserting the legacy route
still fails. Suite: **396 passed, 1 xfailed** on the PUBLIC tree (490 collected).
(Corrected 2026-08-15: 404 counted the private, gitignored
`tests/test_integration_pkg.py`, which is not part of the public suite.)

**✅ INTEGRATION GAP — found by the post-reimplementation deep scan, now CLOSED
(2026-08-16).** The gap was real: the plan above states "Exp 20 → D1 + D2", but
Track D had not been wired into `main.py` — `gauss_bonnet_check()`,
`entanglement_first_law.py` and `entanglement_geometry.py` were referenced by no
experiment, so the three genuinely-computed Track-D results were unreachable from
the documented interface while Experiments 20 and 27 still printed the withdrawn
constructions with "Passes: True".

**Resolution.** Experiment 20 was restructured so the computed results lead:
Part 1 discrete Gauss-Bonnet (residual 1.07e-14, χ = V−E+F = 1 computed from the
mesh, plus the topology-puncture negative control shifting the sum by exactly
2π when χ: 1→0), Part 2 the entanglement first law with its
wrong-modular-Hamiltonian control, Part 3 the mutual-information geometry with
its shuffle control (including the honest note that the frozen g = 8.0 threshold
is not met), and Part 4 the legacy R-T correlation explicitly labelled WITHDRAWN
with its pass/fail flag suppressed. Experiment 27 likewise no longer prints a
verdict for the 3D legacy channel. Tracks A, B and C were already integrated
(Experiments 21, 19, 12).

Note the suite figures in this section are as of the reimplementation commit;
the suite has since grown to 423 passed / 1 xfailed (490 collected) as the
vacuous legacy tests were converted.
