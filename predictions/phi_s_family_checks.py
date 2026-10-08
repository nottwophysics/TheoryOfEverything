#!/usr/bin/env python3
"""
phi_s_family_checks.py — the two Φ ≤ S figures that come from the system
family itself rather than from the per-system results table.

1. Distinct dynamics.  The threshold rule in ``threshold_tpm`` is exactly
   scale-invariant, so many of the 216 coupling matrices induce the same
   transition probability matrix.  This counts the distinct TPMs (per n).
   Φ can therefore take at most that many distinct values.

2. Entropy across transverse-field strengths.  S is reported at h = H_FIELD
   (1.0).  This sweeps h over an explicit grid and reports the largest S in the
   family, with the spectral gap E1 − E0 at that point.  The family maximum
   rises as h falls (0.34 at h = 2, 0.83 at h = 1, 0.99 at h = 0.5) and
   saturates at ≈ 1 bit, the cat-state limit, for h ≲ 0.2.  The digits beyond
   1 bit (1.0003 at h = 0.03 on the default grid) appear only where the ground
   state is near-degenerate (gap ~1e-4) and depend on the grid, so read the
   figure as "≈ 1 bit", not as a bound.  A four-node half/half cut allows at
   most 2 bits, which this family never approaches at any h.

No PyPhi needed.  Run from the repo root:
  PYTHONPATH=. python predictions/phi_s_family_checks.py
"""
from __future__ import annotations

import argparse
import json

import numpy as np

from predictions.entanglement_entropy import S_of_W, ising_hamiltonian
from predictions.phi_s_systems import H_FIELD, make_family, threshold_tpm


def distinct_dynamics(family) -> dict:
    keys = {(s["n"], threshold_tpm(np.array(s["W"])).astype(int).tobytes())
            for s in family}
    by_n = {n: sum(1 for k in keys if k[0] == n)
            for n in sorted({s["n"] for s in family})}
    return {"n_systems": len(family), "distinct_dynamics": len(keys),
            "distinct_dynamics_by_n": by_n}


def entropy_sweep(family, h_min: float, h_max: float, h_step: float) -> dict:
    grid = np.round(np.arange(h_min, h_max + h_step / 2, h_step), 6)
    best_S, best_h, best_id = -1.0, None, None
    for h in grid:
        for s in family:
            S = S_of_W(np.array(s["W"]), float(h))
            if S > best_S:
                best_S, best_h, best_id = S, float(h), s["id"]
    W = np.array(family[best_id]["W"])
    E = np.linalg.eigvalsh(ising_hamiltonian(W, best_h))
    return {
        "max_S_at_reported_h": round(max(S_of_W(np.array(s["W"]), H_FIELD)
                                         for s in family), 4),
        "reported_h": H_FIELD,
        "grid": {"h_min": h_min, "h_max": h_max, "h_step": h_step,
                 "points": int(len(grid))},
        "max_S_over_grid": round(best_S, 4),
        "argmax_h": best_h,
        "argmax_system_id": best_id,
        "spectral_gap_at_argmax": float(f"{E[1] - E[0]:.3e}"),
        "at_grid_edge": bool(np.isclose(best_h, grid[0])),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--h-min", type=float, default=0.01)
    ap.add_argument("--h-max", type=float, default=2.0)
    ap.add_argument("--h-step", type=float, default=0.01)
    ap.add_argument("--out")
    a = ap.parse_args()
    fam = make_family()
    out = {**distinct_dynamics(fam),
           **entropy_sweep(fam, a.h_min, a.h_max, a.h_step)}
    print(json.dumps(out, indent=1))
    if a.out:
        json.dump(out, open(a.out, "w"), indent=1)


if __name__ == "__main__":
    main()
