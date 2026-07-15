"""
Emergence detector — total correlation, dual total correlation, and
O-information, derived from the §2.5 symmetry construction.

The classical_symmetry module showed the joint distinguishability top-down vs
bottom-up equals the total correlation C(X). But C (like pairwise correlation)
cannot separate a REDUNDANT collective (shared cause) from a SYNERGISTIC one
(the whole fixes information no subset reveals). The measure that does is the
O-information (Rosas, Mediano, Gastpar & Jensen 2019, 10.1103/PhysRevE.100.032305):

    C(X)   = Σ_i H(X_i) − H(X)                      (total correlation)
    DTC(X) = Σ_i H(X_{-i}) − (N−1) H(X)             (dual total correlation)
    Ω(X)   = C(X) − DTC(X)                           (O-information)

Ω > 0  → redundancy-dominated;  Ω < 0  → synergy-dominated. Synergy (Ω<0) is the
signature of genuine collective emergence that per-agent and pairwise-correlation
statistics miss (parity has zero pairwise correlation yet strong synergy).

Entropies are plug-in estimates from the empirical joint distribution over
{0,1}^N. A permutation null (independently shuffle each agent column to destroy
cross-agent structure) gives each measure a significance test.
"""

from __future__ import annotations

import numpy as np

from agents.classical_symmetry import entropy
from agents.multiagent_testbed import empirical_joint

LOG2 = np.log(2.0)


def _joint_entropy_from_samples(samples: np.ndarray, n: int) -> float:
    P = empirical_joint(samples, n)
    return entropy(P)


def _subset_entropy(samples: np.ndarray, cols) -> float:
    """Entropy of the marginal over a subset of agent columns."""
    cols = list(cols)
    idx = np.zeros(len(samples), dtype=int)
    for j in cols:
        idx = idx * 2 + samples[:, j]
    counts = np.bincount(idx, minlength=2 ** len(cols)).astype(float)
    p = counts / counts.sum()
    return entropy(p)


def measures(samples: np.ndarray) -> dict:
    """Total correlation, dual total correlation, O-information (bits)."""
    n = samples.shape[1]
    H_all = _subset_entropy(samples, range(n))
    H_i = [_subset_entropy(samples, [i]) for i in range(n)]
    H_not_i = [_subset_entropy(samples, [j for j in range(n) if j != i]) for i in range(n)]
    C = sum(H_i) - H_all
    DTC = sum(H_not_i) - (n - 1) * H_all
    O = C - DTC
    return {"total_correlation": float(C),
            "dual_total_correlation": float(DTC),
            "o_information": float(O),
            "n_agents": n}


def permutation_null(samples: np.ndarray, n_perm: int = 500, seed: int = 42) -> dict:
    """Shuffle each column independently to break cross-agent structure; recompute
    the three measures. Returns null means and two-sided empirical p-values for
    the observed values (|obs| vs |null|)."""
    rng = np.random.default_rng(seed)
    obs = measures(samples)
    keys = ["total_correlation", "dual_total_correlation", "o_information"]
    null = {k: np.empty(n_perm) for k in keys}
    N = samples.shape[1]
    for t in range(n_perm):
        sh = np.column_stack([rng.permutation(samples[:, j]) for j in range(N)])
        m = measures(sh)
        for k in keys:
            null[k][t] = m[k]
    out = {"observed": obs, "null_mean": {}, "p_value": {}}
    for k in keys:
        out["null_mean"][k] = float(null[k].mean())
        out["p_value"][k] = float((np.abs(null[k]) >= abs(obs[k])).mean())
    return out


def classify(samples: np.ndarray, o_tol: float = 1e-3) -> str:
    """Ground-truth-style label from the measures alone."""
    m = measures(samples)
    if m["total_correlation"] < 1e-2:
        return "none"
    return "synergy" if m["o_information"] < -o_tol else "redundancy"


if __name__ == "__main__":
    import json
    from agents.multiagent_testbed import make_testbed
    tb = make_testbed(n=4, n_samples=20000)
    for label, d in tb.items():
        m = measures(d["samples"])
        print(f"{label:16s} gt={d['ground_truth']:20s} "
              f"C={m['total_correlation']:+.4f} DTC={m['dual_total_correlation']:+.4f} "
              f"O={m['o_information']:+.4f} -> {classify(d['samples'])}")
