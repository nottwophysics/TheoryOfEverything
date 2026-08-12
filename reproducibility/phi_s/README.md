# §8 (Φ ≤ S) reproducibility package

Reproduces every number in the paper's **§8 (Empirical Purchase)** — the
falsification of the Φ ≤ S conjecture, and the connectivity-confound analysis of
the Φ–S correlation. The paper (*The Cardinality of Experience Is Underdetermined
by the Quantum State*) withdraws the Φ ≤ S bound on the strength of these results.

## TL;DR — verify in one command (no PyPhi needed)

From the repository root:

```bash
bash reproducibility/phi_s/reproduce.sh
```

This runs the two analysis scripts against the frozen per-system table
`data/phi_s_validated_results.csv` (216 systems, seed 42) and prints the §8
numbers. Needs only `numpy` + `scipy` (the `toenv`/`tofe` env).

## What each §8 statement maps to

> **⚠️ ORDERING AUDIT (2026-08-12) — the numbers below SUPERSEDE the ones in the
> published v2 manuscript (Zenodo 10.5281/zenodo.21380318) and in the frozen
> `*_SUPERSEDED_big_endian.*` files.** `threshold_tpm` enumerates TPM rows
> big-endian while PyPhi 1.2.0 reads them little-endian, so PyPhi previously
> analyzed convention-scrambled systems. The fix converts at the PyPhi boundary
> (`phi_s_systems.to_little_endian`, called by `validated_phi.phi_of_tpm`) and
> is guarded by an ordering self-test in `validated_phi.validate()` plus
> `tests/test_tpm_ordering.py`. The audit script is `ordering_audit.py` (PyPhi
> env). **Every qualitative §8 conclusion survives — and strengthens**: more
> systems are genuinely integrated (51 vs 23), the Φ-vs-S gap widens (4.01 vs
> 0.83 bits), the hold rate still equals the permutation null, and the Φ–S
> correlation remains a connectivity confound.

| §8 statement (corrected) | value | superseded (big-endian) | produced by |
|---|---|---|---|
| 216 systems, seed 42 | 216 | 216 | `predictions/phi_s_systems.py::make_family` |
| apparent Φ≤S hold rate ≈ permutation null | 0.7685 ≈ 0.7789 | 0.8935 ≈ 0.8939 | `phi_s_verdict.py` |
| nonzero-Φ systems violating the bound | **50 of 51** (hold-rate among Φ>0 = 0.0196) | 23 of 23 | `phi_s_verdict.py` |
| Φ reaches ≈4.0 bits; S ≤ ≈0.8 bits | max Φ = 4.012, max S = 0.833 | 2.384 / 0.833 | `phi_s_verdict.py` |
| Pearson r(Φ,S) ≈ +0.64 | +0.643 (perm p ≈ 1e-4) | +0.65 | `phi_s_verdict.py` |
| partial r(Φ,S \| Σ\|W\|) ≈ −0.07, p = 0.29 | −0.074 | −0.02 (p 0.77) | `partial_corr_phi_s.py` |
| partial r(Φ,S \| Σ\|W\|, n) ≈ +0.06, p = 0.38 | +0.062 | +0.09 (p 0.17) | `partial_corr_phi_s.py` |

`data/phi_s_partial_correlation.json` is the reference output for the second row
pair, for a byte-level cross-check.

## Data

- **`data/phi_s_validated_results.csv`** — the per-system table (216 rows):
  `id, topology, n, phi, S, holds_phi_le_S, phi_nonzero`, where
  - `phi` = canonical IIT-3.0 Φ (PyPhi 1.2.0) of the induced threshold-logic dynamics,
  - `S` = entanglement entropy across a bipartition of the transverse-field Ising
    ground state (h = 1) built from the **same** coupling matrix W.
- **`data/phi_s_partial_correlation.json`** — the partial-correlation result.
- **`data/validated_phi_check.csv`** — the PyPhi **validation anchor**: `basic_network`
  Φ = 2.3125 (computed) = 2.3125 (reference), plus `xor_network`, plus the
  **ordering self-test** (little-endian encoding matches PyPhi's reading) —
  confirming the Φ pipeline computes canonical IIT Φ, in the correct
  convention, before the 216-system family is processed.
- **`data/*_SUPERSEDED_big_endian.*`** — the pre-audit results (the ones the
  published v2 manuscript cites), frozen for provenance. Do not use.
- **`ordering_audit.py`** — the audit that found the convention bug (runs in the
  PyPhi env; empirically determines PyPhi's convention, then recomputes Φ both
  ways on the load-bearing systems).

## Regenerating Φ and S from scratch (upstream — requires the PyPhi env)

Φ (canonical IIT) needs **PyPhi 1.2.0 on Python 3.9 with parallelism OFF** — the
parallel evaluators deadlock otherwise; `validated_phi.py` sets the flags:

```bash
# PyPhi env (Python 3.9, pyphi==1.2.0):
python predictions/validated_phi.py          # -> /tmp/phi_s/phi.json  (+ validated_phi_check.csv)

# tofe env (Python 3.13, numpy/scipy):
PYTHONPATH=. python predictions/entanglement_entropy.py   # -> /tmp/phi_s/S.json
```

Then join `phi.json` + `S.json` by `id` into the CSV schema above (add
`holds_phi_le_S = phi <= S`, `phi_nonzero = phi > 1e-6`) and re-run the two
analysis scripts on the regenerated CSV. **Validation anchor:** PyPhi reproduces
`basic_network` Φ = 2.3125 exactly (checked by `validated_phi.validate()` before
the family is processed).

## Environment

| stage | interpreter | key packages |
|---|---|---|
| analysis (`phi_s_verdict.py`, `partial_corr_phi_s.py`) | Python 3.13 (`toenv`/`tofe`) | numpy 2.5.1, scipy 1.18.0 — **no PyPhi** |
| upstream Φ (`validated_phi.py`) | Python 3.9 (`tofe-pyphi39`) | PyPhi 1.2.0 (Mayner et al. 2018, doi:10.1371/journal.pcbi.1006343), parallelism OFF |
| upstream S (`entanglement_entropy.py`) | Python 3.13 | numpy, scipy |

Global seed **42** throughout; permutation tests use 10 000 resamples.
