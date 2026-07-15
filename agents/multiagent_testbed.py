"""
Multi-agent testbed with KNOWN ground-truth organization (seed 42).

Generates classical N-agent systems whose collective structure is known by
construction, so an emergence detector can be scored against truth. Each system
is returned as a sample of joint binary states (shape [n_samples, N]); the
empirical joint distribution is estimated downstream.

Four regimes:

  independent   : agents i.i.d. fair coins. Total correlation 0, no synergy.
                  GROUND TRUTH: no structure (null).
  redundant     : a shared latent bit L drives every agent (X_i = L w.p. 1-noise).
                  High total correlation, high pairwise correlation, POSITIVE
                  O-information. GROUND TRUTH: redundancy / common cause.
  synergistic   : N-1 agents are fair coins; the last is their parity (XOR),
                  optionally noisy. PAIRWISE correlations ~0 by construction; the
                  whole fixes a bit no proper subset reveals. NEGATIVE
                  O-information. GROUND TRUTH: synergy (genuine emergence).
  ising         : classical Ising agents on a ring at inverse-temperature beta;
                  a sweep of beta interpolates independent (beta=0) -> strongly
                  coordinated (large beta). GROUND TRUTH: graded coupling.
"""

from __future__ import annotations

import itertools
import numpy as np

SEED = 42


def independent(n: int, n_samples: int, rng) -> np.ndarray:
    return rng.integers(0, 2, size=(n_samples, n))


def redundant(n: int, n_samples: int, rng, noise: float = 0.1) -> np.ndarray:
    L = rng.integers(0, 2, size=(n_samples, 1))
    flips = rng.random((n_samples, n)) < noise
    X = np.repeat(L, n, axis=1).copy()
    X[flips] = 1 - X[flips]
    return X


def synergistic(n: int, n_samples: int, rng, noise: float = 0.0) -> np.ndarray:
    """N-1 free bits; last = parity of the others (optionally noisy)."""
    free = rng.integers(0, 2, size=(n_samples, n - 1))
    par = free.sum(axis=1) % 2
    if noise > 0:
        flip = rng.random(n_samples) < noise
        par = np.where(flip, 1 - par, par)
    return np.column_stack([free, par])


def ising_ring(n: int, n_samples: int, rng, beta: float = 0.5,
               burn: int = 200, thin: int = 5) -> np.ndarray:
    """Metropolis sampling of a classical Ising ring, spins in {0,1} (=-1/+1)."""
    spins = rng.integers(0, 2, size=n) * 2 - 1
    out = []
    steps = burn + thin * n_samples
    for t in range(steps):
        i = rng.integers(0, n)
        nb = spins[(i - 1) % n] + spins[(i + 1) % n]
        dE = 2 * spins[i] * nb  # J=1 ferromagnetic
        if dE <= 0 or rng.random() < np.exp(-beta * dE):
            spins[i] = -spins[i]
        if t >= burn and (t - burn) % thin == 0:
            out.append((spins > 0).astype(int).copy())
    return np.array(out[:n_samples])


def make_testbed(n: int = 4, n_samples: int = 20000, seed: int = SEED) -> dict:
    """Return {regime_label: {samples, ground_truth}} for the four fixed regimes
    plus an Ising beta-sweep."""
    rng = np.random.default_rng(seed)
    tb = {}
    tb["independent"] = {"samples": independent(n, n_samples, rng),
                         "ground_truth": "none"}
    tb["redundant"] = {"samples": redundant(n, n_samples, rng),
                       "ground_truth": "redundancy"}
    tb["synergistic"] = {"samples": synergistic(n, n_samples, rng),
                         "ground_truth": "synergy"}
    for beta in (0.0, 0.25, 0.5, 1.0, 2.0):
        tb[f"ising_b{beta}"] = {"samples": ising_ring(n, n_samples, rng, beta=beta),
                                "ground_truth": f"coupling_beta={beta}"}
    return tb


def empirical_joint(samples: np.ndarray, n: int, k: int = 2) -> np.ndarray:
    """Empirical joint distribution over k**n states, flattened."""
    idx = np.zeros(len(samples), dtype=int)
    for j in range(n):
        idx = idx * k + samples[:, j]
    counts = np.bincount(idx, minlength=k ** n).astype(float)
    return counts / counts.sum()


if __name__ == "__main__":
    import csv
    tb = make_testbed(n=4, n_samples=20000)
    rows = []
    for label, d in tb.items():
        s = d["samples"]
        rows.append({"regime": label, "N": s.shape[1], "n_samples": s.shape[0],
                     "ground_truth": d["ground_truth"],
                     "mean_state": f'{s.mean():.3f}'})
    with open("testbed_summary.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    for r in rows:
        print(r)
