# Benchmark: framework Φ vs canonical IIT Φ (PyPhi)

> **Note (2026-08-12 ordering audit):** the reference Φ values for the
> home-built XOR systems in this memo were computed before the TPM
> state-ordering fix at the PyPhi boundary and carry that convention. The
> memo's qualitative verdict — the framework heuristic is NOT an
> approximation of IIT Φ — is unaffected (the PyPhi-native anchor networks,
> including basic_network Φ = 2.3125, are ordering-clean), but individual
> XOR-system values here should not be quoted without rechecking against
> the audited pipeline (`reproducibility/phi_s/`).

**Roadmap item:** P3 — validate the integrated-information measure against a
reference implementation.

## Question
`predictions/iit_bridge.py::IntegratedInformation.compute_phi` is described in
its own docstring as a "simplified IIT 3.0-like measure." That phrasing implies
it approximates the integrated information Φ that IIT actually defines. This
benchmark tests that implication directly, against **PyPhi 1.2.0**, the reference
implementation of IIT 3.0 (Mayner et al., *PLOS Comput. Biol.* 2018,
DOI `10.1371/journal.pcbi.1006343`, verified via CrossRef).

## Method
- **Systems (24).** PyPhi's own canonical example networks (`basic_network`,
  `xor_network`) plus 22 small XOR-logic networks of 3–5 nodes at varying
  connectivity density. XOR gates are used because they are the canonical source
  of genuine integration in IIT (deterministic threshold gates collapse to
  fixed points with Φ = 0). Each system is a binary state-transition network
  with a **guaranteed-reachable state** (obtained by stepping a random state
  forward once, since PyPhi rejects unreachable states).
- **Reference Φ.** `pyphi.compute.sia(subsystem).phi`, computed in a dedicated
  Python 3.9 environment (PyPhi 1.2.0 imports `collections.Iterable`, removed in
  Python 3.10, so it cannot share the repo's Python ≥3.10 interpreter). The
  anchor `basic_network` reproduces the documented Φ = **2.3125** exactly,
  confirming the oracle is correctly configured.
- **Framework Φ.** `IntegratedInformation.compute_phi(W, state)` with `W` the
  system's binary adjacency matrix and the same state — computed in the repo's
  own environment.
- **Comparison.** Pearson and Spearman correlation over all systems, plus a
  binary "integration detection" confusion matrix (is Φ > 0?).

## Result — the two measures are unrelated

| metric | value |
|---|---|
| systems compared | 24 |
| Pearson r | **−0.012** (p = 0.96) |
| Spearman ρ | **+0.104** (p = 0.63) |
| integration-detection agreement | **58 %** (≈ chance) |
| classified oppositely | **10 of 24** (FP = 6, FN = 4) |
| framework Φ range | 0 – 0.693 |
| canonical Φ range | 0 – 6.375 |

Concrete disagreements:
- PyPhi's own `xor_network` has canonical **Φ = 1.875**, but the framework
  measure returns **0**.
- System `xor11` has canonical **Φ = 6.375** (the most integrated in the set),
  framework **Φ = 0**.
- System `xor21` has framework **Φ = 0.693** (its maximum), canonical **Φ = 0**.

The framework Φ does not track canonical IIT Φ either quantitatively (no
correlation) or qualitatively (it disagrees on which systems are integrated
almost as often as a coin flip). It also lives on a different scale (0–0.7 vs
0–6.4), consistent with it being a bespoke entropy-difference heuristic rather
than an approximation of IIT's minimum-information-partition Φ.

## Conclusion
The measure is an internally-defined heuristic, **not** an implementation or
approximation of IIT integrated information. Results elsewhere in the repository
that label this quantity "consciousness (Φ)" should be read accordingly: they
describe the framework's own scalar, not IIT Φ, and the two are not
interchangeable. This does not by itself refute anything the framework claims —
it bounds what the Φ symbol in the code is entitled to mean.

## Reproducibility
- `predictions/pyphi_benchmark.py` — system construction, both Φ maps, and the
  join/scoring logic.
- `tests/test_pyphi_benchmark.py` (5 tests) — runs without PyPhi against a
  checked-in fixture (`tests/fixtures/pyphi_benchmark_{framework,reference}.json`),
  so CI needs no PyPhi. Regenerating the reference fixture requires the Python
  3.9 + PyPhi environment (documented in the test docstring).
- Figure: `pyphi_benchmark.png`; joined data: `pyphi_benchmark.csv`.
- Seed 42; PyPhi 1.2.0; the anchor Φ = 2.3125 check guards oracle drift.
