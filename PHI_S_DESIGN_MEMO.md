# Design memo — a validated-Φ test of Φ ≤ S, and the multi-agent symmetry

> **OUTCOME (recorded 2026-08-15):** the test this memo designs was run.
> **Φ ≤ S was FALSIFIED** (50 of 51 nonzero-Φ systems violate it;
> ordering-audit-corrected 2026-08-12) and the raw Φ–S correlation proved a
> connectivity confound. See `PHI_S_MULTIAGENT_RESEARCH_REPORT.md` and
> `reproducibility/phi_s/`. This memo is the dated pre-registration record.

Scope: operationalize the paper's §8 conjecture **Φ ≤ S** with a Φ that is
*canonical IIT* (computed by PyPhi), not the bespoke heuristic the earlier
benchmark showed is uncorrelated with IIT Φ (r = −0.012). And formalize the §2.5
decombination↔combination symmetry as a computable operational-indistinguishability
test. Falsification-first: a negative result ("Φ does not track S", "the symmetry
is a metaphor not a mechanism") is a valid outcome and will be reported as such.
Global seed 42 throughout.

## The commensurability problem, and the bridge

Φ (integrated information) is defined by IIT on a **classical** system — a
transition-probability matrix (TPM) over discrete node states. S (entanglement
entropy) is a **quantum** quantity — von Neumann entropy of a reduced density
matrix. To test Φ ≤ S honestly they must be computed on the **same object**, yet
by **independent** routes (no shared intermediate — that independence is exactly
what the circular `iit_bridge.py` lacked).

**The bridge: one weight matrix W drives both.** For each test system we draw a
symmetric zero-diagonal coupling matrix W (topology varied — see family below).
From the *same* W:

- **Classical route → Φ.** Build a deterministic threshold-logic TPM: node *i*
  turns on next step iff its weighted input from currently-on nodes exceeds half
  its total in-weight (`tpm[state] = (Wᵀ s > 0.5·W.sum(0))`). Feed the TPM to
  PyPhi; Φ = `pyphi.compute.sia(subsystem).phi`. This is the *validated* Φ.
- **Quantum route → S.** Build a transverse-field Ising Hamiltonian
  `H(W) = −Σᵢⱼ Wᵢⱼ ZᵢZⱼ − h Σᵢ Xᵢ` (h = 1.0), find its ground state |ψ⟩, and
  compute the entanglement entropy S = −Tr(ρ_A log₂ ρ_A) across a bipartition of
  the sites, with ρ_A = Tr_B|ψ⟩⟨ψ|. This reuses the Hamiltonian construction the
  non-circular IIT rebuild already validated this session.

The two quantities share only W — the physical specification of the system — and
nothing in their computation. So Φ ≤ S becomes a genuine empirical question:
does canonical integrated information of the classical dynamics stay below the
entanglement of the quantum ground state of the same couplings?

## System family (seed 42)

N = 3–4 sites (PyPhi Φ is super-exponential; N≤4 keeps each Φ ≈ 0.1 s with
parallelism disabled). Topology sweep, each with several coupling-strength draws:

| class | W structure | expected S | expected Φ |
|---|---|---|---|
| disconnected | W = 0 (or block-diagonal isolated sites) | S = 0 | Φ = 0 (paper's limiting case) |
| chain | nearest-neighbour couplings only | low–moderate | low |
| ring | chain + wraparound | moderate | moderate |
| star / half-connected | one hub | moderate | variable |
| fully-connected | all pairs coupled | high | high (paper's limiting case) |
| random | Bernoulli(0.6) mask × U(0.2,1.0), symmetrized | spread | spread |

Target ≥ 200 systems total across classes and coupling draws.

## The test (pre-registered)

1. **Bound hold rate:** fraction with Φ ≤ S.
2. **Permutation/shuffle null (decisive control):** break the Φ–S pairing by
   permuting S against Φ; recompute hold rate. If the shuffled hold rate ≈ the
   real hold rate, "Φ ≤ S holds" carries no evidence of a Φ–S relationship — it
   is a scale accident (this is exactly what sank the circular version).
3. **Correlation:** Pearson and Spearman Φ–S with permutation p-values.
4. **Bound tightness:** distribution of (S − Φ).
5. **Power analysis:** N systems needed to detect a correlation of given size at
   α = 0.05, power = 0.8.

**Verdict rule (fixed in advance, not tuned):** the bound is *evidentially
meaningful* only if the real hold rate exceeds the shuffled hold rate by a
margin that itself beats the null spread, AND the Φ–S correlation is
distinguishable from its permutation null. Otherwise the honest verdict is
"Φ ≤ S holds numerically but reflects scale, not a Φ–S law." Either outcome is
reported.

## Multi-agent thread (§2.5 symmetry)

Formalize decombination↔combination as **operational indistinguishability**.
Construct N localized agents two ways from the same Hilbert space:

- **top-down**: agents = perspectival reductions (partial traces) of ONE global
  entangled state;
- **bottom-up**: agents = independent local states later composed.

Test whether the two constructions can yield the **same operational content O**
(each agent's reduced state, cross-agent correlations, decision statistics on a
task) while differing in "cardinality" (one subject-in-modes vs. many combined
subjects). Distinguishability metric: trace distance between the accessible
observables' outcomes under the two constructions (seed 42). The §2.5 claim
predicts they can be made operationally indistinguishable. **Honest scope
question, decided by the result:** does this yield a usable *design principle*
(top-down global constraints computably reproducing bottom-up multi-agent
behaviour) or does it remain an evocative analogy with no engineering purchase?

## Toolchain / environments

- **Φ (PyPhi 1.2.0):** env `tofe-pyphi39` (Python 3.9). **Critical:** set
  `PARALLEL_CONCEPT_EVALUATION=False`, `PARALLEL_CUT_EVALUATION=False`,
  `PROGRESS_BARS=False`, `WELCOME_OFF=True` — the parallel evaluators deadlock in
  the sandbox (confirmed: with them off, basic_network Φ=2.3125 in 0.1 s; with
  them on, the call hangs > 13 min). Validation anchor: basic_network Φ = 2.3125
  exact, xor_network as second fixture.
- **S, analysis, figures, multi-agent:** env `tofe` (Python 3.13). Handoff
  between envs via JSON files (kernels share the filesystem, not memory).

## Citations (all verified via CrossRef this session)

| ref | DOI | verified |
|---|---|---|
| Tononi, IIT provisional manifesto (2008) | 10.2307/25470707 | ✓ |
| Tononi, information integration theory (2004) | 10.1186/1471-2202-5-42 | ✓ |
| Oizumi, Albantakis & Tononi, IIT 3.0 (2014) | 10.1371/journal.pcbi.1003588 | ✓ |
| Mayner et al., PyPhi (2018) | 10.1371/journal.pcbi.1006343 | ✓ |
| Eisert, Cramer & Plenio, area laws (2010) | 10.1103/RevModPhys.82.277 | ✓ |
