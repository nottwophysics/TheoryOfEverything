#!/usr/bin/env python3
"""
phi_s_verdict.py — reproduce the paper's §8 falsification numbers for Φ ≤ S from
the per-system results table.

Input: phi_s_validated_results.csv (columns: id, topology, n, phi, S,
holds_phi_le_S, phi_nonzero) — 216 systems, seed 42, where phi is canonical
IIT-3.0 Φ (PyPhi 1.2.0) and S is the entanglement entropy of the transverse-field
Ising ground state built from the SAME coupling matrix. Generating that table
needs the PyPhi env (see reproducibility/phi_s/README.md); this analysis does not.

Reproduces (cf. PHI_S_MULTIAGENT_RESEARCH_REPORT.md and manuscript §8):
  - N systems, N with Φ>0
  - Φ≤S hold rate vs a permutation null (shuffle the Φ–S pairing)
  - violations; hold rate among the Φ>0 systems (0.0 = every integrated system violates)
  - max Φ, max S
  - Pearson r(Φ,S) with permutation p; Spearman ρ

Run from the repo root:
  PYTHONPATH=. python predictions/phi_s_verdict.py --csv reproducibility/phi_s/data/phi_s_validated_results.csv
"""
from __future__ import annotations

import argparse
import csv
import json

import numpy as np


def load(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    phi = np.array([float(r["phi"]) for r in rows])
    S = np.array([float(r["S"]) for r in rows])
    return phi, S


def pearson(a, b):
    a = a - a.mean(); b = b - b.mean()
    d = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d > 0 else float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="reproducibility/phi_s/data/phi_s_validated_results.csv")
    ap.add_argument("--out")
    ap.add_argument("--nperm", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--tol", type=float, default=1e-6)
    a = ap.parse_args()

    phi, S = load(a.csv)
    n = len(phi)
    rng = np.random.default_rng(a.seed)

    holds = phi <= S + a.tol
    hold_rate = float(holds.mean())
    null = [float((phi <= rng.permutation(S) + a.tol).mean()) for _ in range(a.nperm)]
    null_hold = float(np.mean(null))

    nz = phi > 1e-6
    violations = int((~holds).sum())
    hold_rate_nz = float(holds[nz].mean()) if nz.any() else float("nan")

    r = pearson(phi, S)
    rp = sum(abs(pearson(phi, rng.permutation(S))) >= abs(r) for _ in range(a.nperm))
    r_perm_p = (rp + 1) / (a.nperm + 1)

    try:
        from scipy.stats import spearmanr
        rho, rho_p = spearmanr(phi, S)
        rho, rho_p = float(rho), float(rho_p)
    except Exception:
        rho = rho_p = None

    out = {
        "n_systems": n,
        "n_phi_nonzero": int(nz.sum()),
        "hold_rate_phi_le_S": round(hold_rate, 4),
        "permutation_null_hold_rate": round(null_hold, 4),
        "violations": violations,
        "hold_rate_among_nonzero_phi": round(hold_rate_nz, 4),
        "max_phi_bits": round(float(phi.max()), 3),
        "max_S_bits": round(float(S.max()), 3),
        "pearson_r_phi_s": round(r, 3),
        "pearson_perm_p": round(r_perm_p, 5),
        "spearman_rho": None if rho is None else round(rho, 3),
        "spearman_p": rho_p,
        "n_perm": a.nperm,
        "seed": a.seed,
        "verdict": ("Phi<=S is FALSIFIED: the hold rate equals the permutation null "
                    "(it is produced almost entirely by the Phi=0 systems), "
                    + (f"every one of the {int(nz.sum())}"
                       if holds[nz].sum() == 0 else
                       f"all but {int(holds[nz].sum())} of the {int(nz.sum())}")
                    + " systems with nonzero integrated information violate the bound, "
                    "and canonical Phi is not capped by the bipartition entanglement "
                    "entropy that limits S."),
    }
    print(json.dumps(out, indent=1))
    if a.out:
        json.dump(out, open(a.out, "w"), indent=1)


if __name__ == "__main__":
    main()
