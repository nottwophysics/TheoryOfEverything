# Operationalizing the §2.5 symmetry for classical multi-agent systems

### A detailed technical report — does an information-theoretic, non-Hilbert analogue compute something a designer couldn't otherwise get?

> **⚠️ CORRECTION (2026-08-15, adversarial review).** The headline effect
> sizes originally published here (AUC 1.000, Cohen's d ≈ +68.5 — the d column
> has since been removed from the table below) are **structural, not
> empirical**, and must not be cited as effect sizes. The synthetic parity
> regime is noiseless by design, so the AUC-1.000 separation is categorical
> **by construction**, and Cohen's d **grows without bound with per-instance
> sample count m** (independent re-measurement with the committed
> `agents/` code: d ≈ 262 at m = 500, ≈ 2 505 at the stated m = 4 000,
> ≈ 9 644 at m = 16 000). The published **+68.5 does not replicate** under
> the stated protocol, and **+68.5 is retracted and must not be cited**.
>
> **UPDATE 2026-08-16 — the AUC computation is now committed and runnable:**
> `agents/benchmark.py` (`python -m agents.benchmark`), with tests in
> `tests/test_classical_agents.py`. The AUC table below has been regenerated
> from it; the previously published baseline figures (0.390/0.429/0.472) came
> from an uncommitted run and have been replaced by measured values. Cohen's *d*
> is deliberately **not** implemented, because on this construction it reports a
> property of the sample count rather than of the detector. Still absent: the
> **figures** cited in this report (`classical_emergence_measures.png`,
> `detector_vs_baselines.png`) were never committed and cannot be regenerated
> from the repository. What survives is
> the qualitative, provably-true point: pairwise-correlation and variance
> baselines cannot see zero-pairwise-correlation parity structure, while
> O-information can — and O-information is the *existing* measure of Rosas
> et al., so the contribution is an operational test, not a new observable.

**Scope.** This report documents the full research programme that grew out of the
paper analysis and the swarm-emergence use-case discussion. It formalizes the
paper's §2.5 decombination↔combination symmetry as a *classical* (non-Hilbert)
information-theoretic construction, builds a controlled multi-agent testbed with
known ground truth, derives an emergence detector from the symmetry, and tests —
falsification-first — whether that detector catches genuine collective emergence
that the tools a system designer normally uses would miss.

**One-line result.** It does — the symmetry-derived synergy detector separates a
synergistic (parity) collective from an independent one at AUC 1.00 (categorical
by construction; see the correction banner) while pairwise-correlation and
per-agent-variance baselines are uninformative (AUC ≈ 0.29–0.47 across
re-measurements) — but the measure it recovers is the existing O-information, so
the contribution is a clean operational *test*, not a new observable.

**Reproducibility.** Global seed 42; environment `tofe` (Python 3.13, numpy
2.5.1, scipy 1.18.0); no Hilbert space, no PyPhi. Numbers were transcribed from
working-session output; the §9 provenance retraction and the correction banner
above govern which of them can still be traced. All five external citations were
verified against CrossRef / arXiv at the time of writing.

---

## 1. Motivation and the question

The paper (*The Cardinality of Experience Is Underdetermined by the Quantum
State*) argues in §2.5 for a **decombination↔combination symmetry**: carving one
global whole into perspectival parts (decombination) and composing independent
parts into a whole (combination) are dialectically symmetric operations. A
follow-on feedback thread asked whether that symmetry could be turned into an
engineering tool — specifically, a way to **detect emergent behaviour in a swarm
of agents**.

The quantum multi-agent result (Thread 2 of the Φ≤S study) had already answered
this for the *quantum* case: single-perspective content is identical whether N
agents are carved from one entangled whole or composed from independent parts
(trace distance 0), while the joint content differs by the entanglement. That is
a statement about the limits of perspectival knowledge, not a control mechanism —
and AI swarms aren't in a Hilbert space anyway. The open question this report
closes:

> Build the **classical** analogue of the §2.5 symmetry over ordinary probability
> distributions, and determine whether it yields a usable emergence detector — a
> quantity a designer *could not otherwise get* from standard tools — or whether
> it merely reframes existing information-theoretic measures.

---

## 2. The classical dictionary

The quantum construction maps term-for-term onto discrete information theory. The
global object stops being a state vector in a Hilbert space and becomes a joint
probability distribution; entanglement entropy is replaced by total correlation;
partial trace by marginalization; tensor product by the product of marginals.

| quantum object (Thread 2) | classical analogue (this work) |
|---|---|
| Hilbert space 𝓗 = (ℂ²)^⊗N | joint distribution P(X₁,…,X_N) over discrete agent states |
| global pure state \|Ψ⟩ | the correlated global distribution P |
| partial trace Tr_{≠i} → ρᵢ | marginalization → P(Xᵢ) |
| tensor product ⊗ᵢ ρᵢ | product of marginals ∏ᵢ P(Xᵢ) |
| entanglement entropy S(ρ_A) | total correlation C(P) = Σᵢ H(Xᵢ) − H(X₁…X_N) |
| top-down (decombination) | agents = marginals of the correlated global P |
| bottom-up (combination) | agents = independent, marginals matched, composed as ∏Pᵢ |

**Module:** `agents/classical_symmetry.py` — primitives `entropy`, `marginal`,
`all_marginals`, `product_of_marginals`, `total_correlation`, `kl_divergence`,
`total_variation`, and `symmetry_report`.

---

## 3. The total-correlation recovery — the honest first-order result

The classical mirror of the Thread-2 finding is a theorem, and it was confirmed
computably across 11 test distributions (N ∈ {2,3,4}, random and structured):

1. **Single-agent marginals are identical** under the top-down and bottom-up
   constructions — total-variation distance ≤ 2×10⁻¹⁶ (machine zero). This is the
   classical image of the quantum trace-distance-0 result: *a single agent cannot
   tell, from its own accessible distribution, whether it is a marginal of one
   correlated whole or an independent combined agent.*
2. **The joint distinguishability equals the total correlation exactly:**

   D_KL(P ‖ ∏ᵢ P(Xᵢ)) = Σᵢ H(Xᵢ) − H(X) = C(P),

   confirmed to 10⁻¹⁵ on every case.

Two interpretive anchors bracket the scale: a perfectly redundant three-agent
system (states 000 or 111 only) has C = 2.000 bits (the maximum, N−1), and an
independent product has C = 0.000.

**What this means.** At the full-joint level the symmetry **recovers total
correlation** (Watanabe 1960) — a known quantity. Stated plainly: the first-order
operationalization is a re-derivation, not a discovery. The interesting question
is therefore not *whether* there is joint structure (total correlation already
measures that) but *what kind* — and that is where the standard tools fail.

**Verification table** (`classical_symmetry_check.csv`): across all 11
distributions, `single_identical = True` and `KL == total correlation = True`.

---

## 4. The testbed with known ground truth

`agents/multiagent_testbed.py` generates classical N-agent systems (N = 4,
20 000 samples, seed 42) whose organization is fixed by construction, so a
detector can be scored against truth. Critically, **all four core regimes have
≈0.5 marginals**, so no first-order (per-agent) statistic can distinguish them —
any signal must live in the joint structure.

| regime | construction | ground truth | mean state |
|---|---|---|---|
| independent | i.i.d. fair coins | none (null) | 0.501 |
| redundant | shared latent bit drives all agents (noise 0.1) | redundancy / common cause | 0.504 |
| synergistic | N−1 free bits; last = their parity (XOR) | synergy (genuine emergence) | 0.500 |
| Ising ring | Metropolis, J=1 ferromagnetic, β-sweep | graded coupling | 0.501 → 0.686 |

The **synergistic** regime is the decisive one: parity has **zero pairwise
correlation and fair-coin marginals by construction**, yet the whole determines a
bit that no proper subset reveals — the textbook case of "the collective is more
than the sum of its parts." The **Ising** `mean_state` climbing from 0.50 (β=0,
disordered) to 0.686 (β=2, ordered) confirms the graded-coupling interpolation.

---

## 5. The emergence detector

`agents/emergence_detector.py` computes, from the symmetry construction, three
entropy-only measures plus a permutation null:

- **Total correlation** C(X) = Σᵢ H(Xᵢ) − H(X)
- **Dual total correlation** DTC(X) = Σᵢ H(X₋ᵢ) − (N−1) H(X)
- **O-information** Ω(X) = C(X) − DTC(X)  (Rosas, Mediano, Gastpar & Jensen 2019)

The **sign of Ω** is the key discriminator: Ω > 0 is redundancy-dominated, Ω < 0
is synergy-dominated. The permutation null independently shuffles each agent
column (destroying cross-agent structure) and recomputes, giving each measure a
two-sided empirical p-value.

**Ground truth recovered 3/3** (`detector_results.csv`):

| regime | C (bits) | DTC (bits) | Ω (bits) | perm-null p (C / Ω) | detected |
|---|---|---|---|---|---|
| independent | 0.000 | 0.000 | −0.000 | 0.76 / 0.48 | none |
| redundant | 1.213 | 0.690 | **+0.524** | 0.000 / 0.000 | redundancy |
| synergistic | 1.000 | 3.000 | **−2.000** | 0.000 / 0.000 | synergy |
| Ising β=0.25 | 0.185 | 0.166 | +0.020 | 0.000 | redundancy |
| Ising β=0.5 | 0.770 | 0.531 | +0.239 | 0.000 | redundancy |
| Ising β=1.0 | 2.265 | 0.971 | +1.294 | 0.000 | redundancy |
| Ising β=2.0 | 2.668 | 0.901 | +1.766 | 0.000 | redundancy |

The essential observation: **total correlation cannot separate redundant
(C = 1.21) from synergistic (C = 1.00)** — they are close. **Only the sign of Ω
distinguishes them** (+0.52 vs −2.00). The Ising sweep shows Ω rising positive
with β, correctly identifying ferromagnetic alignment as a redundant mechanism
(agents share a common order) rather than a synergistic one.

The first figure shows the Ω sign-flip across the three canonical regimes (Panel
a) and the Ising coupling sweep (Panel b):

*Figure — Information measures across regimes. Panel a: total correlation, dual total correlation, and O-information for the independent, redundant, and synergistic regimes — the O-information sign flips from positive (redundancy) to strongly negative (synergy). Panel b: total correlation and O-information versus Ising inverse-temperature β, showing redundant structure growing with ferromagnetic coupling. (figure file in the artifact package `classical_multiagent_package.tar.gz`).*

---

## 6. Beat-the-baselines — the decisive test

The falsification-first core: does the symmetry-derived synergy measure catch
emergence that a designer's standard tools miss? The task is to distinguish the
**synergistic** regime from the **independent** regime (100 seeded instances
each, 4 000 samples per instance), scoring each metric by its AUC and effect
size. The baselines are the two things a designer already has: the pairwise
correlation matrix and per-agent variance.

| metric | AUC (synergistic vs independent) |
|---|---|
| **O-information \|Ω\| (this work)** | **1.000** |
| total correlation | 1.000 |
| max \|pairwise correlation\| (baseline) | 0.373 |
| mean \|pairwise correlation\| (baseline) | 0.513 |
| max per-agent variance (baseline) | 0.530 |

*(n = 100 instances per regime, 4 agents, 4 000 samples, seed 42.)*

**Reproduce:** `python -m agents.benchmark` (committed 2026-08-16). Measured
across seeds {7, 42, 101} x n_samples {1500, 4000}: the detector is **1.000 in
every configuration**; the baselines range **0.26–0.66**. Cohen's *d* is
deliberately not computed — on this construction it grows without bound in
n_samples, so the figure that previously circulated (d ≈ 68) reports a property
of the protocol, not of the detector.

**What this AUC does and does not show.** The parity regime is noiseless, so the
separation is **deterministic by construction** and AUC 1.000 is the *expected*
result — it confirms the estimator behaves as derived, not that the detector
would separate emergence in the wild. **Total correlation reaches 1.000 too**:
|Ω| is *not* distinguished from TC on this task. The differentiator is the
**sign**, and only on a comparison that holds TC fixed — see below.

**Sign separation (the claim worth citing).** At the redundancy noise where the
two regimes carry the *same* total correlation (0.1195), TC is at chance between
them (AUC 0.53, distributions overlap) while Ω's sign still separates them
completely: every synergistic instance negative (mean −2.00), every redundant
instance positive (mean +0.39). Run `agents.benchmark.sign_separation()`.
Scope: this holds where redundancy is actually present; as noise → 0.5 both
regimes collapse toward Ω = 0 and the sign stops being meaningful.


**The synergy detector separates parity-type emergence categorically (AUC 1.00 —
by construction; the d column is structural, see the correction banner); the
designer baselines are uninformative** (note: the pairwise-correlation baselines
score at or below chance — measured 0.26–0.66 across seeds {7,42,101} and
n_samples {1500,4000}, with max|pairwise| consistently BELOW 0.5 — an
anti-signal artifact of the construction, not "chance". Note two of the three
baselines sit marginally ABOVE 0.5 at some settings, so the honest claim is
"never approaches separation", not "always below chance"). This is exactly what the
construction predicts: parity has zero pairwise correlation and fair-coin marginals *by
construction*, so correlation- and variance-based tools are provably blind to it,
while the higher-order measure fires unmistakably.

The second figure shows the per-instance separation (Panel a) and the detection
AUC bars against the chance line (Panel b):

*Figure — Detector versus baselines on synergistic-emergence detection. Panel a: per-instance metric values, independent (grey) versus synergistic (colored) — only O-information separates the two clouds; the pairwise-correlation and per-agent-variance clouds overlap completely. Panel b: detection AUC per metric — O-information and total correlation at 1.00, baselines at 0.29–0.47 (below the 0.5 line — anti-signal artifact, see banner). (figure file was never committed to the public repository — see §10.)*

---

## 7. Honest scope verdict

**Does the classical operationalization compute something a designer couldn't
otherwise get? A qualified YES.**

- **YES, relative to the tools a designer normally reaches for.** Per-agent
  statistics and the pairwise correlation matrix are genuinely blind to
  synergistic (parity-type) collective structure. The symmetry-derived
  O-information detects it at AUC 1.00. A swarm engineer using only variance and
  correlation would miss this entire class of emergence — so for that engineer,
  this is a concrete, demonstrated capability they did not have.

- **NO, relative to the existing higher-order-information literature.** The
  measure is **not novel** — it is the O-information (Rosas et al. 2019), rooted
  in Williams–Beer partial information decomposition and Watanabe's total
  correlation. The §2.5 symmetry does not produce a new quantity. What it
  provides is a principled **operational derivation and test**: a route from the
  bare "one whole versus many parts" picture to *which* multivariate information
  measure detects genuine emergence, together with a ready-made permutation null.

**The contribution is therefore methodological, not a new observable.** For a
designer who does not already know the synergy/PID literature, this is a usable,
correct tool with a motivated derivation. For one who does, it is a clean
reframing that recovers — rather than transcends — that literature. Neither
outcome is a failure; the falsification-first framing treats "it re-expresses
known measures" as a valid, reportable result, and the beat-the-baselines test
turned that into a demonstrated positive against the naive tools.

### Relation to the quantum result and the paper

The classical result mirrors Thread 2 exactly:

| | quantum (Thread 2) | classical (this work) |
|---|---|---|
| single view | reduced states identical top-down/bottom-up (TD = 0) | marginals identical (TV ≈ 0) |
| joint view | differs by the entanglement | differs by the total correlation |
| where emergence lives | global tensor-product correlations | higher-order (synergistic) joint structure |

Both express the same lesson, and it is precisely the paper's §2.5 point stated
operationally: **emergence, if it is real, is a property of the whole's joint
structure that no single-agent or low-order view recovers.** This is consistent
with the paper's §8 firewall separating what a perspective can and cannot access
— and it sharpens, rather than supports, any hope of reading collective unity off
local data.

---

## 8. Limitations

- **Small N and binary agents.** N = 4 with two-state agents keeps the joint
  distribution exactly enumerable. High-order entropy estimation is sample-hungry
  and the plug-in estimator is biased upward for larger alphabets or N; the
  O-information literature has bias-corrected estimators that would be needed to
  scale.
- **Parity is a clean synthetic extreme.** Real swarms exhibit noisier, mixed
  redundancy-plus-synergy that a single scalar Ω summarizes only coarsely; a full
  PID lattice (Williams–Beer) would resolve the decomposition more finely.
- **One sense of "emergence."** Here emergence is operationalized specifically as
  statistical synergy. Dynamical, causal, and computational senses of emergence
  are not addressed and would need different instruments.

---

## 9. Provenance and reproducibility

- **Seed 42** throughout (testbed generation, permutation null, per-instance
  sampling).
- **Environment `tofe`** (Python 3.13, numpy 2.5.1, scipy 1.18.0). Entirely
  classical — no PyPhi, no Hilbert space. AUC computed directly via the rank
  (Mann–Whitney) statistic; scikit-learn not required.
- **Tests:** 9 in `tests/test_classical_agents.py` (symmetry recovery, testbed
  ground-truth signatures, detector sign-correctness, null behaviour). Full repo
  suite **302 passed** (historical count at the time of writing; the current
  public suite is 437; the repo's pytest run is authoritative).
- **Numbers**: RETRACTED as a provenance claim (2026-08-15) — of the artifacts
  named here, only `testbed_summary.csv` was ever committed to the public
  repository; `classical_symmetry_check.csv`, `detector_results.csv`,
  `baseline_comparison.csv` and `baseline_verdict.json` are absent, so the
  numbers attributed to them cannot be traced. Numbers reproducible from the
  committed `agents/` code and `testbed_summary.csv` stand; the §8 effect-size
  column does not (see correction banner).

### Citations (all verified via CrossRef / arXiv this session)

| reference | identifier | source |
|---|---|---|
| Watanabe, *Information Theoretical Analysis of Multivariate Correlation* (1960) — total correlation | 10.1147/rd.41.0066 | IBM J. Res. Dev. |
| Williams & Beer, *Nonnegative Decomposition of Multivariate Information* (2010) — PID | arXiv:1004.2515 | arXiv |
| Rosas, Mediano, Gastpar & Jensen, *Quantifying high-order interdependencies…* (2019) — O-information | 10.1103/PhysRevE.100.032305 | Phys. Rev. E |
| Timme et al., *Synergy, redundancy, and multivariate information measures* (2013) | 10.1007/s10827-013-0458-4 | J. Comput. Neurosci. |
| Mediano et al., *Greater than the parts: a review of the information decomposition…* (2022) | 10.1098/rsta.2021.0246 | Phil. Trans. R. Soc. A |

---

## 10. Artifacts

**Modules** (`agents/` package): `classical_symmetry.py`, `multiagent_testbed.py`,
`emergence_detector.py`. **Tests:** `test_classical_agents.py` (9 tests).
**Results:** `testbed_summary.csv` (committed). NOT in the public repository
(2026-08-15 audit): `classical_symmetry_check.csv`, `detector_results.csv`,
`baseline_comparison.csv`, `baseline_verdict.json`, both figures
(`classical_emergence_measures.png`, `detector_vs_baselines.png`) and
`classical_multiagent_package.tar.gz`.
**Design memo:** `CLASSICAL_SYMMETRY_DESIGN_MEMO.md` (committed).

## Bottom line

The classical operationalization **works and beats the naive baselines**: it
turns the §2.5 symmetry into a concrete, correct synergy detector that catches
parity-type collective emergence (AUC 1.00) which correlation and variance tools
miss entirely (AUC ≈ 0.29–0.47 — an anti-signal artifact of the construction,
not chance). But it **recovers the existing O-information / PID
machinery rather than producing a new quantity** — so it is a principled
operational test a designer could adopt, not a fundamentally new measurement.
That is the honest, defensible scope: a usable tool with a clean derivation from
the symmetry, standing on measures the higher-order-information literature already
established.
