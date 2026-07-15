"""
Classical information-theoretic analogue of the §2.5 decombination↔combination
symmetry.

The quantum Thread-2 result (predictions/multi_agent.py) showed: single-agent
reduced states are identical whether N agents are carved from one global
entangled state (top-down / decombination) or composed from independent parts
(bottom-up / combination), while the *joint* state differs by the entanglement.

Here the global object is a classical joint distribution P(X_1,...,X_N) over
discrete agent states instead of a quantum state. The dictionary:

    Hilbert space          -> joint distribution P
    entanglement entropy   -> total correlation  C(P) = Σ_i H(X_i) − H(X)
    partial trace          -> marginalization  P -> P(X_i)
    tensor product         -> product of marginals  ∏_i P(X_i)

This module proves computably the classical mirror:
  (a) single-agent marginals are IDENTICAL top-down vs bottom-up (TV distance 0);
  (b) D_KL(P ‖ ∏_i P(X_i)) = C(P), the total correlation (Watanabe 1960,
      10.1147/rd.41.0066).

So the symmetry, at the joint level, recovers total correlation — a known
quantity. Higher-order structure (synergy) is handled in emergence_detector.py.

All distributions are dense arrays over the joint state space {0,1}^N (or a
general alphabet), indexed by the integer encoding of the state tuple.
"""

from __future__ import annotations

import itertools
import numpy as np

LOG2 = np.log(2.0)


def _states(n: int, k: int = 2):
    """All joint states as tuples over alphabet of size k."""
    return list(itertools.product(range(k), repeat=n))


def entropy(p: np.ndarray) -> float:
    """Shannon entropy in bits of a (flattened) probability vector."""
    p = np.asarray(p, float).ravel()
    p = p[p > 0]
    return float(-np.sum(p * np.log(p)) / LOG2)


def marginal(P: np.ndarray, n: int, i: int, k: int = 2) -> np.ndarray:
    """Marginal distribution P(X_i) from the joint P (shape k**n)."""
    Pt = P.reshape([k] * n)
    axes = tuple(a for a in range(n) if a != i)
    return Pt.sum(axis=axes)


def all_marginals(P: np.ndarray, n: int, k: int = 2) -> list:
    return [marginal(P, n, i, k) for i in range(n)]


def product_of_marginals(P: np.ndarray, n: int, k: int = 2) -> np.ndarray:
    """Bottom-up joint: ∏_i P(X_i), flattened to shape k**n."""
    margs = all_marginals(P, n, k)
    out = np.array([1.0])
    for m in margs:
        out = np.kron(out, m)
    return out


def total_correlation(P: np.ndarray, n: int, k: int = 2) -> float:
    """C(P) = Σ_i H(X_i) − H(X_1..X_N)."""
    margs = all_marginals(P, n, k)
    return float(sum(entropy(m) for m in margs) - entropy(P))


def kl_divergence(P: np.ndarray, Q: np.ndarray) -> float:
    """D_KL(P ‖ Q) in bits."""
    P = np.asarray(P, float).ravel(); Q = np.asarray(Q, float).ravel()
    mask = P > 0
    return float(np.sum(P[mask] * (np.log(P[mask]) - np.log(Q[mask]))) / LOG2)


def total_variation(p: np.ndarray, q: np.ndarray) -> float:
    return float(0.5 * np.sum(np.abs(np.asarray(p, float) - np.asarray(q, float))))


def symmetry_report(P: np.ndarray, n: int, k: int = 2) -> dict:
    """Verify the classical mirror of the §2.5 symmetry on joint distribution P.

    top-down  : agents are the marginals of the correlated global P.
    bottom-up : agents are independent, marginals matched, joint = ∏ P(X_i).
    """
    P = np.asarray(P, float).ravel()
    P = P / P.sum()
    top_margs = all_marginals(P, n, k)
    Q = product_of_marginals(P, n, k)
    bot_margs = all_marginals(Q, n, k)

    # (a) single-perspective: marginals identical
    tv = [total_variation(a, b) for a, b in zip(top_margs, bot_margs)]

    # (b) joint distinguishability == total correlation
    C = total_correlation(P, n, k)
    Dkl = kl_divergence(P, Q)

    return {
        "n_agents": n,
        "single_perspective_TV_max": float(max(tv)),
        "single_perspective_identical": bool(max(tv) < 1e-12),
        "total_correlation_bits": C,
        "kl_P_vs_product_bits": Dkl,
        "kl_equals_total_correlation": bool(abs(C - Dkl) < 1e-10),
    }


if __name__ == "__main__":
    import json
    rng = np.random.default_rng(42)
    # a random correlated joint on 3 binary agents
    P = rng.random(2 ** 3); P /= P.sum()
    print(json.dumps(symmetry_report(P, 3), indent=1))
