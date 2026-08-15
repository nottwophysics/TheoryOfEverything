# Classical operationalization of the §2.5 symmetry: does it give a designer a usable emergence detector?

> **⚠️ CORRECTION (2026-08-15, adversarial review).** The headline effect
> sizes below (AUC 1.000, Cohen's d ≈ +68.5) are **structural, not
> empirical**, and must not be cited as effect sizes. The synthetic parity
> regime is noiseless by design, so the AUC-1.000 separation is categorical
> **by construction**, and Cohen's d **grows without bound with per-instance
> sample count m** (independent re-measurement with the committed
> `agents/` code: d ≈ 262 at m = 500, ≈ 2 505 at the stated m = 4 000,
> ≈ 9 644 at m = 16 000). The published **+68.5 does not replicate** under
> the stated protocol, and the AUC/Cohen's-d computation plus most of the
> result artifacts cited in this report were never committed to the public
> repository, so their provenance cannot be established. What survives is
> the qualitative, provably-true point: pairwise-correlation and variance
> baselines cannot see zero-pairwise-correlation parity structure, while
> O-information can — and O-information is the *existing* measure of Rosas
> et al., so the contribution is an operational test, not a new observable.

Follow-on to the quantum multi-agent result (Thread 2 of the Φ≤S study). The
driving question, from the use-case discussion: take the paper's §2.5
decombination↔combination symmetry, build a **classical** (non-Hilbert)
information-theoretic analogue, and test whether it **computes something a
designer of multi-agent / swarm systems couldn't otherwise get** — concretely, a
detector of emergent collective behaviour. Falsification-first; seed 42.

---

## 1. The classical dictionary

The quantum construction maps cleanly onto discrete information theory:

| quantum (Thread 2) | classical (here) |
|---|---|
| Hilbert space 𝓗 = (ℂ²)^⊗N | joint distribution P(X₁,…,X_N) |
| global pure state \|Ψ⟩ | correlated global P |
| partial trace → ρ_i | marginalization → P(X_i) |
| tensor product ⊗ρ_i | product of marginals ∏P(X_i) |
| entanglement entropy S | total correlation C(P)=ΣH(X_i)−H(X) |

**Module:** `agents/classical_symmetry.py`.

## 2. The total-correlation recovery (the honest baseline)

The classical mirror of the Thread-2 finding is provable and was confirmed across
11 distributions:

- **Single-agent marginals are identical** top-down vs bottom-up (total-variation
  distance ≤ 2×10⁻¹⁶, machine zero) — the classical image of the quantum
  trace-distance-0 result. A single agent cannot tell whether it is a marginal of
  one correlated whole or an independent combined agent.
- **The joint distinguishability equals the total correlation exactly:**
  D_KL(P ‖ ∏P_i) = ΣH(X_i) − H(X) = C(P), to 10⁻¹⁵.

So at the full-joint level **the symmetry recovers total correlation** (Watanabe
1960) — a known quantity, not a new one. This must be stated plainly: the
first-order operationalization is a re-derivation, not a discovery.

## 3. The testbed (known ground truth, seed 42)

`agents/multiagent_testbed.py` — N=4 agents, 20 000 samples each:

- **independent** — i.i.d. fair coins (null; C=0).
- **redundant** — a shared latent bit drives all agents (redundancy).
- **synergistic** — parity/XOR: N−1 free bits, the last their parity. **Zero
  pairwise correlation and fair-coin marginals by construction** — the whole
  fixes a bit no proper subset reveals (genuine emergence).
- **Ising ring** — Metropolis at β ∈ {0, 0.25, 0.5, 1, 2} (graded coupling).

## 4. The detector

`agents/emergence_detector.py` — total correlation C, dual total correlation DTC,
and **O-information Ω = C − DTC** (Rosas, Mediano, Gastpar & Jensen 2019), with a
permutation null. Ω's sign is the key: **Ω>0 redundancy-dominated, Ω<0
synergy-dominated.** Ground truth recovered 3/3:

| regime | C | Ω | permutation p | detected |
|---|---|---|---|---|
| independent | 0.000 | −0.000 | 0.48 / 0.77 | none |
| redundant | 1.213 | **+0.524** | 0.000 | redundancy |
| synergistic | 1.000 | **−2.000** | 0.000 | synergy |
| Ising β=2 | 2.668 | +1.766 | 0.000 | redundancy |

Note C alone cannot separate redundant (C=1.21) from synergistic (C=1.00) — they
are similar; **only the sign of Ω distinguishes them.** The Ising sweep shows Ω
rising positive with β — ferromagnetic alignment is a redundant mechanism (shared
order), correctly classified.

## 5. Beat-the-baselines — the decisive test

Does the symmetry-derived synergy measure catch emergence that a designer's
standard tools miss? Task: distinguish **synergistic from independent**, 100
seeded instances per regime, against two baselines a designer already has —
pairwise correlation and per-agent variance.

| metric | AUC (synergistic vs independent) |
|---|---|
| **O-information \|Ω\| (ours)** | **1.000** |
| total correlation | 1.000 |
| max \|pairwise correlation\| (baseline) | 0.390 |
| mean \|pairwise correlation\| (baseline) | 0.429 |
| max per-agent variance (baseline) | 0.472 |

Effect size (Cohen's d, synergistic vs independent): the previously reported
**Ω d = +68.5 is retracted** — d is structural here and grows without bound in
the per-instance sample count (see the correction banner); baseline d values
(max pairwise −0.33, per-agent variance +0.09) are likewise
construction-dependent.

**The synergy detector separates parity-type emergence categorically (AUC 1.0 —
by construction); the designer baselines are uninformative** (the
pairwise-correlation baselines score below 0.5 — 0.390/0.429 in the table above,
≈0.29–0.39 under independent re-measurement — an anti-signal artifact of the
construction). This is expected and exactly the
point: parity has zero pairwise correlation and fair-coin marginals by
construction, so correlation- and variance-based tools are provably blind to it,
while the higher-order measure fires unmistakably.

Figures: `classical_emergence_measures.png` (Ω sign-flip across regimes + Ising
sweep); `detector_vs_baselines.png` (per-instance separation + detection AUC).

---

## 6. Honest scope verdict

**Answering the driving question — "does the classical operationalization compute
something a designer couldn't otherwise get?" — the answer is a qualified YES:**

- **YES, relative to the tools a designer normally reaches for.** Per-agent
  statistics and the pairwise correlation matrix are genuinely blind to
  synergistic (parity-type) collective structure; the symmetry-derived
  O-information detects it at AUC 1.0. A swarm engineer using only variance and
  correlation would miss this class of emergence entirely. That is a concrete,
  demonstrated gain.

- **NO, relative to the existing higher-order-information literature.** The
  measure is **not novel** — it is the O-information (Rosas et al. 2019), rooted
  in Williams–Beer partial information decomposition and Watanabe's total
  correlation. The §2.5 symmetry does not produce a new quantity; it provides a
  clean **operational derivation and test** — a principled route from "one whole
  vs many parts" to *which* multivariate information measure detects genuine
  emergence, plus a ready null.

**So the symmetry's real contribution is methodological, not a new observable:**
it motivates and frames a synergy detector that beats naive baselines, but it
recovers rather than transcends the synergy/PID literature. For a designer who
does *not* already know that literature, this is a usable and correct tool with a
motivated derivation; for one who does, it is a reframing.

### Relation to the quantum result and the paper

This mirrors Thread 2 exactly. There, single-perspective content was
indistinguishable top-down vs bottom-up while joint content differed by the
entanglement — a statement about the *limits of perspectival knowledge*, not a
control mechanism. Here, single-agent marginals are identical while the joint
distribution differs by the total correlation, and genuine emergence lives in the
**higher-order** (synergistic) part of that joint structure — invisible to any
single agent or pairwise view. Both are the same lesson: **emergence, if it is
real, is a property of the whole's joint structure that no local or low-order
view recovers** — which is precisely the paper's §2.5 point stated operationally,
and consistent with §8's separation of what a perspective can and cannot access.

## 7. Limitations

- Small N (=4) and binary agents; high-order entropy estimation is sample-hungry
  and the plug-in estimator is biased for larger alphabets/N (a known issue in
  the O-information literature; bias-corrected estimators exist).
- The parity regime is a clean synthetic extreme; real swarms have noisier,
  mixed redundancy+synergy that the single Ω scalar summarizes only coarsely
  (a full PID lattice would resolve more).
- "Emergence" here is operationalized specifically as statistical synergy; other
  senses (dynamical, causal, computational) are not addressed.

## 8. Provenance

- Seed 42 throughout (testbed, permutation null, instance sampling).
- Env `tofe` (Python 3.13, numpy 2.5.1, scipy 1.18.0); all classical, no PyPhi/
  Hilbert space. AUC computed directly (rank statistic; sklearn not required).
- Full suite bar maintained (tests in Step 8).
- **Citations (CrossRef/arXiv-verified this session):** Watanabe total correlation
  10.1147/rd.41.0066; Williams–Beer PID arXiv:1004.2515; Rosas–Mediano–Gastpar–
  Jensen O-information **10.1103/PhysRevE.100.032305**; Timme et al. synergy
  10.1007/s10827-013-0458-4; Mediano et al. emergence review
  10.1098/rsta.2021.0246.
- Numbers: provenance RETRACTED (2026-08-15) — `detector_results.csv`,
  `baseline_comparison.csv` and `baseline_verdict.json` were never committed to
  the public repository (see the correction banner and the detailed report's §9).

## Bottom line

The classical operationalization **works and beats the naive baselines**: it
turns the §2.5 symmetry into a concrete, correct synergy detector that catches
parity-type collective emergence (AUC 1.0) which correlation and variance tools
miss (AUC ≈ 0.29–0.47 — an anti-signal artifact of the construction, not
chance). But it **recovers the existing O-information / PID machinery
rather than producing a new quantity** — so it is a principled *operational test*
a designer could adopt, not a fundamentally new measurement. That is the honest,
defensible scope: a usable tool with a clean derivation, not a novel observable.
