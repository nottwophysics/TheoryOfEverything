# Design memo — classical information-theoretic analogue of the §2.5 symmetry

**Driving question (from the use-case thread):** operationalize the paper's §2.5
decombination↔combination symmetry for *classical* multi-agent systems (no
Hilbert space) and test whether it computes **something a designer couldn't
otherwise get** — specifically, whether it yields a usable detector of emergent
collective behaviour.

This is the classical mirror of Thread-2 (the quantum multi-agent result). There
the finding was: single-perspective content is identical top-down vs bottom-up
(trace distance 0), while joint content differs by the entanglement. We now ask
what the same construction gives when the global object is a classical joint
probability distribution instead of a quantum state.

## The classical dictionary (quantum → classical)

| quantum object (Thread 2) | classical analogue (this work) |
|---|---|
| Hilbert space 𝓗 = (ℂ²)^⊗N | joint distribution P(X₁,…,X_N) over discrete agent states |
| global pure state \|Ψ⟩ | the correlated global distribution P |
| partial trace Tr_{≠i} → ρ_i | marginalization → P(X_i) |
| tensor product ⊗_i ρ_i | product of marginals ∏_i P(X_i) |
| entanglement entropy S(ρ_A) | **total correlation** C(P) = Σ_i H(X_i) − H(X₁…X_N) |
| top-down (decombination) | agents = marginals of the correlated global P |
| bottom-up (combination) | agents = independent draws, marginals matched, composed as ∏P_i |
| single-perspective indistinguishability | marginals identical either way (TV distance 0) |
| joint distinguishability grows with entanglement | D(P ‖ ∏P_i) = C(P), the total correlation |

**Provable classical mirror (Step 2 will confirm computably):**
- (a) single-agent marginals are IDENTICAL under top-down and bottom-up
  construction — TV distance 0, by construction;
- (b) the joint distinguishability, in KL divergence, equals the total
  correlation exactly: D_KL(P ‖ ∏_i P_i) = Σ_i H(X_i) − H(X) = C(P).

So the symmetry, at the full-joint level, **recovers a known quantity** (total
correlation, Watanabe 1960). That is the honest baseline and must be stated
plainly: the first-order operationalization does not conjure a new measure.

## The real question — beyond total correlation

Total correlation (and ordinary pairwise correlation) cannot distinguish two
very different collectives:

- **Redundant / common-cause:** a shared latent drives every agent. High total
  correlation, high pairwise correlation — but nothing "emergent"; any one agent
  already carries the shared signal.
- **Synergistic:** a global constraint (e.g. parity/XOR) means the *whole*
  determines information that **no proper subset reveals**. This is the genuine
  "the collective is more than its parts." Parity has **zero pairwise
  correlation** by construction, so a designer's standard tools (per-agent
  variance, correlation matrix) see nothing.

The candidate "quantity a designer couldn't otherwise get" is therefore a
**synergy / higher-order** measure that the symmetry construction motivates:
- **O-information** Ω(X) = C(X) − DTC(X) (Rosas et al. 2019): sign distinguishes
  redundancy-dominated (Ω>0) from synergy-dominated (Ω<0) systems, where DTC is
  the dual total correlation.

## Pre-registered test (fixed before running)

- **Testbed (seed 42), four regimes with known ground truth:** independent (null);
  redundant/common-cause; synergistic (parity); graded classical Ising (coupling
  sweep, independent → coordinated).
- **Detector:** total correlation, dual total correlation, O-information, each
  with a permutation null (independently permute each agent column; recompute).
- **Baselines a designer already has:** (1) per-agent variance/entropy; (2)
  pairwise correlation matrix (max and mean |corr|).
- **Decisive case:** the SYNERGISTIC regime — baselines should see ≈0 structure
  while the synergy detector (O-information < 0, negative) fires.
- **Verdict rule (not tuned):** the operationalization "gives something a designer
  couldn't otherwise get" ONLY if the synergy detector separates the synergistic
  regime from independent with an effect the pairwise+per-agent baselines do not
  achieve, across many seeded instances. Otherwise the honest verdict is
  "reframes/unifies the known synergy literature and contributes a clean
  operational test, but not a new quantity." Both outcomes reported.

## Citations (all verified via CrossRef / arXiv this session)

| ref | id | verified |
|---|---|---|
| Watanabe, total correlation (1960) | 10.1147/rd.41.0066 | ✓ IBM J. Res. Dev. |
| Williams & Beer, PID (2010) | arXiv:1004.2515 | ✓ "Nonnegative Decomposition of Multivariate Information" |
| Rosas, Mediano, Gastpar & Jensen, O-information (2019) | 10.1103/PhysRevE.100.032305 | ✓ Phys. Rev. E (corrected from a transposed DOI) |
| Timme et al., synergy/redundancy measures (2013) | 10.1007/s10827-013-0458-4 | ✓ J. Comput. Neurosci. |
| Mediano et al., emergence review (2022) | 10.1098/rsta.2021.0246 | ✓ Phil. Trans. R. Soc. A |

## Environment

All classical (discrete distributions, numpy/scipy) — env `tofe` (Python 3.13).
No Hilbert space, no PyPhi. Optional cross-check of information measures with the
`dit` library if installable.
