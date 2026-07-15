# A validated-Φ test of Φ ≤ S, and the §2.5 multi-agent symmetry — research report

Follow-on to the paper analysis (`PAPER_ANALYSIS_AND_UPDATES.md`), which flagged
two threads worth developing properly: (1) the paper's §8 **Φ ≤ S** conjecture,
which the repo previously "confirmed" only through a circular construction, now
retested with a Φ **validated against canonical IIT**; and (2) the §2.5
decombination↔combination **symmetry**, formalized as a computable
operational-indistinguishability test. Falsification-first throughout: a negative
result is a result. Global seed 42.

---

## Thread 1 — Φ ≤ S with a validated Φ

### The problem with the old result

The paper's §8 cites `predictions/iit_bridge.py`, which computes both Φ and S
inside one construction so the inequality holds by definition. The earlier PyPhi
benchmark (`predictions/pyphi_benchmark.py`) had already shown that module's
bespoke "Φ" is **not** integrated information: correlation with canonical PyPhi Φ
was r = −0.012 across 24 systems. So neither the bound's holding nor any Φ–S
relationship it implied could be trusted.

### Method — the commensurability bridge

To test Φ ≤ S honestly, Φ and S must live on the **same object** but be computed
by **independent** routes. Each of 216 test systems is fixed by one symmetric
zero-diagonal coupling matrix W (topology swept: disconnected, chain, ring, star,
fully-connected, random; N ∈ {3,4}; seed 42). From the *same* W:

- **Φ (classical route).** A deterministic threshold-logic transition-probability
  matrix → **PyPhi 1.2.0** `compute.sia(subsystem).phi`. This is canonical IIT Φ
  (Oizumi, Albantakis & Tononi 2014; Mayner et al. 2018).
- **S (quantum route).** A transverse-field Ising Hamiltonian
  H(W) = −Σ Wᵢⱼ ZᵢZⱼ − h Σ Xᵢ (h=1) → ground state → von Neumann entanglement
  entropy across a site bipartition.

The two share only W. Modules: `predictions/phi_s_systems.py` (shared family),
`predictions/validated_phi.py` (PyPhi env, Python 3.9),
`predictions/entanglement_entropy.py` (tofe env, Python 3.13).

**Φ validation (required before trusting any number):** PyPhi reproduced
`basic_network` Φ = **2.3125** exactly and `xor_network` Φ = 1.875. Table in
`validated_phi_check.csv`.

### Result — the bound is *falsified*, not confirmed

| quantity | value |
|---|---|
| systems | 216 (power ≈ 1.00 for the observed effect) |
| apparent Φ≤S hold rate | 0.8935 (193/216) |
| permutation-null hold rate | 0.8939 (Δ = **−0.0004**) |
| violations | **23** |
| hold rate among the 23 Φ>0 systems | **0.000** |
| max Φ | 2.384 bits |
| max S | 0.833 bits (bipartition ceiling) |
| Pearson r (Φ,S) | **+0.65**, permutation p < 2×10⁻⁴ |
| Spearman ρ | +0.45, p = 3×10⁻¹² |

Two findings, which must be kept separate:

1. **The bound Φ ≤ S is false in the regime that matters.** The 89% "hold rate"
   is *identical to the permutation null* — it is entirely produced by the 193
   systems with Φ = 0 (0 ≤ S trivially). **Every one of the 23 systems with
   nonzero integrated information violates the bound.** The reason is structural:
   canonical Φ reaches 2.38 bits while S is capped by the bipartition at 0.83
   bits, so any genuinely integrated system has Φ > S. This is the opposite of
   the paper's "holds without violation."

2. **Φ and S are nonetheless genuinely correlated** (Pearson +0.65, permutation
   p < 2×10⁻⁴) — because both increase with network connectivity. This is a
   *real* relationship that the framework's bespoke Φ entirely lacked (r = −0.012
   vs PyPhi). So the validated analysis simultaneously rescues a weak-but-real
   Φ–S association and refutes the specific inequality claimed.

Figure `phi_s_validated.png`: (a) Φ-vs-S scatter with the y=x bound line — the 23
violators sit near the Φ ≈ 2.4 ceiling, far above the S ceiling; (b) the observed
hold rate falling exactly on the permutation-null distribution.

### What this means for the paper's §8

The paper-analysis memo recommended softening §8 to "holds ~99.5% but
indistinguishable from a shuffled null." **This result is stronger and should
replace that recommendation:** with a Φ validated against canonical IIT, the
bound does not merely lack evidence — it is **falsified**, and falsified exactly
where integrated information is nonzero. The honest §8 revision is:

> *A validated test (canonical IIT Φ via PyPhi, entanglement entropy from the
> independent quantum ground state of the same couplings, N=216, seed 42) refutes
> Φ ≤ S: the inequality holds only for the trivial Φ=0 systems (its 89% hold rate
> equals the permutation null), while every system with nonzero integrated
> information violates it, because Φ is unbounded by the bipartition entropy that
> caps S. Φ and S are, however, positively correlated (r≈+0.65) as both track
> connectivity. The §8 conjecture as stated is therefore false; a defensible
> residual claim is only the weaker correlation.*

This does not touch §2–§7 — the paper's own firewall ("if §8 fails, §2–§7 are
untouched") holds.

---

## Thread 2 — the §2.5 symmetry as an operational-indistinguishability test

### Method

`predictions/multi_agent.py` builds N agents two ways from the same Hilbert
space, using a GHZ-interpolation global state
|Ψ(λ)⟩ = cos θ|0…0⟩ + sin θ|1…1⟩ (θ = λπ/4, λ: product → GHZ):

- **top-down** (decombination): agent i = perspectival reduction (partial trace)
  of the one global state;
- **bottom-up** (combination): independent local states, marginals matched to the
  top-down reductions, composed as a product.

Distinguishability is measured by trace distance at two access levels:
single-perspective (one agent's reduced state) and joint (the global state vs the
product of marginals), plus the cross-agent outcome correlation.

### Result

| λ | single-perspective TD | joint TD | top-down corr | bottom-up corr |
|---|---|---|---|---|
| 0.0 | 0.000 | 0.000 | 0.00 | 0.00 |
| 0.5 | 0.000 | 0.544 | 1.00 | ≈0 |
| 1.0 | 0.000 | 0.875 | 1.00 | ≈0 |

- **Single-perspective content is identical under both constructions at every λ**
  (trace distance ≡ 0). An agent cannot tell from its own accessible state
  whether it is a mode of one global whole or an independent combined agent. This
  is the paper's underdetermination (claim E) — **confirmed computably**, and it
  is exactly the operational-symmetry the §2.5 argument asserts.
- **Joint content distinguishes them, scaling with entanglement** (joint trace
  distance 0 → 0.875 as λ: 0 → 1; top-down outcomes perfectly correlated,
  bottom-up independent). The distinction exists but is accessible only to a
  global/coordinated protocol, never to a single perspective.

Figure `multi_agent_symmetry.png`.

### Honest scope verdict: design principle, or analogy?

**It is a real, computable indistinguishability — but not a design principle.**
The feedback note that prompted this work hoped the symmetry could let engineers
build "scale-free cognitive architectures where the global field state dictates
localized agent behaviour." The computation shows why that does not follow: the
two constructions **agree locally and differ only globally**, so "the global
field dictates local behaviour" has no operational purchase a single agent could
exploit — local behaviour is *identical* whether or not a global whole exists.
The symmetry is genuine and now demonstrable, but it is a statement about the
**limits of perspectival knowledge**, not a top-down control mechanism. This is
the §2.5 result stated operationally, and it confirms the paper's own modesty:
the symmetry is dialectical, not a route to new engineering.

---

## Provenance & reproducibility

- **Seed 42** everywhere (system family, permutation null, decision sampling).
- **Environments:** Φ in `tofe-pyphi39` (Python 3.9, PyPhi 1.2.0 —
  `PARALLEL_CONCEPT_EVALUATION`/`PARALLEL_CUT_EVALUATION`/`PROGRESS_BARS` OFF, or
  it deadlocks in-sandbox). S, analysis, multi-agent, figures in `tofe`
  (Python 3.13, numpy 2.5.1, scipy 1.18.0). Cross-env handoff via JSON.
- **Tests:** 13 new (`test_entanglement_entropy.py` 6, `test_multi_agent.py` 7);
  full suite **293 passed**. `validated_phi.py` runs only in the PyPhi env and is
  not collected by the tofe suite.
- **Citations (all CrossRef-verified this session):** Tononi IIT 2004
  (10.1186/1471-2202-5-42) & 2008 (10.2307/25470707); Oizumi–Albantakis–Tononi
  IIT 3.0 (10.1371/journal.pcbi.1003588); Mayner et al. PyPhi
  (10.1371/journal.pcbi.1006343); Eisert–Cramer–Plenio area laws
  (10.1103/RevModPhys.82.277).
- **Numbers** copied from executed output (`phi_s_verdict.json`,
  `phi_s_validated_results.csv`, `multi_agent_results.csv`), not recalled.

## Bottom line

The validated analysis delivers a clean, publishable pair of results: **Φ ≤ S is
false** (once Φ is real IIT integrated information, it exceeds the entanglement
ceiling exactly when a system is integrated), though **Φ and S do correlate**
through shared dependence on connectivity; and the **§2.5 symmetry is a genuine
perspective-level indistinguishability but not an engineering design principle.**
Both sharpen, rather than support, the strong claims — the same direction this
whole review has moved the codebase.
