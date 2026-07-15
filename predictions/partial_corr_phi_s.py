#!/usr/bin/env python3
"""
R3 for §8 v2 — partial correlation of Phi and S controlling for connectivity.

Answers the reviewers' A2/T1 objection: the raw Phi-S correlation (r ~ +0.65)
may be a common-cause effect of connectivity (both Phi and S rise with it).
This computes the correlation of Phi and S AFTER removing the linear effect of
connectivity (and, in a second variant, system size n), with a permutation
p-value. If the partial correlation stays clearly nonzero, a residual Phi-S
association survives; if it collapses to ~0, the raw correlation is a confound.

INPUT (whichever you have; connectivity is always rebuilt from the shared family):
  * merged CSV  (durable store artifact, e.g. phi_s_validated_results.csv) with
    per-system columns including an id, a Phi column, and an S column; OR
  * the two raw JSONs written by the committed pipelines:
      phi.json  = list of {id, topology, n, phi}   (predictions/validated_phi.py)
      S.json    = list of {id, topology, n, S}      (predictions/entanglement_entropy.py)

Numpy only — no PyPhi. Run from the repo root:
  PYTHONPATH=. python predictions/partial_corr_phi_s.py --csv phi_s_validated_results.csv
  # or:
  PYTHONPATH=. python predictions/partial_corr_phi_s.py --phi phi.json --S S.json
"""
from __future__ import annotations

import argparse
import csv
import json

import numpy as np

from predictions.phi_s_systems import make_family


# ---------- input loading -------------------------------------------------

def _find_col(header, *cands):
    low = {h.lower().strip(): h for h in header}
    for c in cands:                       # exact (case-insensitive) first
        if c in low:
            return low[c]
    for c in cands:                       # then substring
        for k, v in low.items():
            if c in k:
                return v
    return None


def load_csv(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    header = rows[0].keys()
    id_c = _find_col(header, "id", "system", "sid")
    phi_c = _find_col(header, "phi")
    s_c = _find_col(header, "s", "s_entanglement", "entanglement", "entropy")
    if phi_c is None or s_c is None:
        raise SystemExit(f"Could not find Phi/S columns in {list(header)}")
    out = {}
    for k, r in enumerate(rows):
        i = int(float(r[id_c])) if id_c else k
        phi = r[phi_c].strip()
        out[i] = {"phi": None if phi in ("", "None", "nan") else float(phi),
                  "S": float(r[s_c])}
    return out


def load_json_pair(phi_path, s_path):
    phi = {r["id"]: r for r in json.load(open(phi_path))}
    Sd = {r["id"]: r for r in json.load(open(s_path))}
    out = {}
    for i in set(phi) & set(Sd):
        out[i] = {"phi": phi[i]["phi"], "S": float(Sd[i]["S"])}
    return out


# ---------- statistics ----------------------------------------------------

def pearson(a, b):
    a = a - a.mean(); b = b - b.mean()
    d = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d > 0 else float("nan")


def residuals(y, X):
    """Residuals of y regressed on [1, X] (X is (m,k))."""
    A = np.column_stack([np.ones(len(y)), X])
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    return y - A @ beta


def partial_corr(P, S, Z, n_perm, seed):
    """Partial Pearson r(P,S | Z) via residual correlation, with a permutation
    p-value (shuffle one residual vector)."""
    rP, rS = residuals(P, Z), residuals(S, Z)
    r = pearson(rP, rS)
    rng = np.random.default_rng(seed)
    hits = sum(abs(pearson(rP, rng.permutation(rS))) >= abs(r) for _ in range(n_perm))
    return r, (hits + 1) / (n_perm + 1)


# ---------- main ----------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv")
    ap.add_argument("--phi")
    ap.add_argument("--S", dest="s")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--nperm", type=int, default=10000)
    args = ap.parse_args()

    if args.csv:
        data = load_csv(args.csv)
    elif args.phi and args.s:
        data = load_json_pair(args.phi, args.s)
    else:
        raise SystemExit("give either --csv FILE or both --phi FILE --S FILE")

    fam = {s["id"]: s for s in make_family(args.seed)}

    P, S, C, N = [], [], [], []
    dropped = 0
    for i in sorted(set(data) & set(fam)):
        phi = data[i]["phi"]
        if phi is None:
            dropped += 1
            continue
        W = np.abs(np.asarray(fam[i]["W"], float))
        P.append(float(phi))
        S.append(float(data[i]["S"]))
        C.append(float(np.triu(W, 1).sum()))   # connectivity = sum|W| (upper tri)
        N.append(float(fam[i]["n"]))
    P, S, C, N = map(np.asarray, (P, S, C, N))

    print(f"systems used: {len(P)}   (dropped phi=None: {dropped})")
    print(f"raw    Pearson r(Phi, S)          = {pearson(P, S):+.3f}   "
          f"[should reproduce ~+0.65]")
    r1, p1 = partial_corr(P, S, C.reshape(-1, 1), args.nperm, args.seed)
    print(f"partial r(Phi, S | sum|W|)        = {r1:+.3f}   perm p = {p1:.4f}")
    r2, p2 = partial_corr(P, S, np.column_stack([C, N]), args.nperm, args.seed)
    print(f"partial r(Phi, S | sum|W|, n)     = {r2:+.3f}   perm p = {p2:.4f}")

    nz = P > 1e-6
    if nz.sum() >= 4:
        print(f"[nonzero-Phi subset, N={int(nz.sum())}] raw r(Phi,S) = "
              f"{pearson(P[nz], S[nz]):+.3f}")

    print("\n--> paste r(Phi,S | sum|W|, n) and its perm p into the v2 placeholder;")
    print("    if |r| is small and p is large -> confound (raw corr does not survive);")
    print("    if |r| stays clear and p is small -> a residual Phi-S association survives.")


if __name__ == "__main__":
    main()
