"""
Shared system-family generator for the validated Φ ≤ S test.

Both the Φ pipeline (`validated_phi.py`, PyPhi env) and the S pipeline
(`entanglement_entropy.py`, tofe env) import THIS module so they build the
*identical* family of systems from seed 42. Each system is fixed by one
symmetric zero-diagonal coupling matrix W; that single W drives two independent
computations downstream:

    W  ──(threshold-logic TPM)──►  PyPhi  ──►  Φ   (validated_phi.py)
    W  ──(transverse-field Ising H)──►  ground state  ──►  S   (entanglement_entropy.py)

Keeping the generator in one place guarantees commensurability: system k on the
Φ side and system k on the S side are the same physical object.
"""

from __future__ import annotations

import itertools
import numpy as np

SEED = 42
H_FIELD = 1.0  # transverse-field strength for the Ising Hamiltonian (S side)


def _sym_zero_diag(W: np.ndarray) -> np.ndarray:
    W = (W + W.T) / 2.0
    np.fill_diagonal(W, 0.0)
    return W


def make_family(seed: int = SEED):
    """Deterministic family of test systems spanning a topology sweep.

    Returns a list of dicts: {id, topology, n, W (list-of-lists)}.
    """
    rng = np.random.default_rng(seed)
    systems = []
    sid = 0

    def add(topology, W):
        nonlocal sid
        systems.append({"id": sid, "topology": topology,
                        "n": int(W.shape[0]),
                        "W": _sym_zero_diag(np.asarray(W, float)).tolist()})
        sid += 1

    # Coupling-strength draws per structural class, N in {3,4}.
    for n in (3, 4):
        for _ in range(18):
            g = rng.uniform(0.3, 1.0)  # global coupling scale

            # disconnected
            add("disconnected", np.zeros((n, n)))

            # chain (nearest neighbour)
            Wc = np.zeros((n, n))
            for i in range(n - 1):
                Wc[i, i + 1] = g * rng.uniform(0.5, 1.0)
            add("chain", Wc)

            # ring (chain + wraparound)
            Wr = Wc.copy()
            Wr[0, n - 1] = g * rng.uniform(0.5, 1.0)
            add("ring", Wr)

            # star / half-connected (hub = node 0)
            Ws = np.zeros((n, n))
            for i in range(1, n):
                Ws[0, i] = g * rng.uniform(0.5, 1.0)
            add("star", Ws)

            # fully connected
            Wf = g * rng.uniform(0.5, 1.0, (n, n))
            add("fully_connected", Wf)

            # random Bernoulli-masked
            mask = (rng.random((n, n)) < 0.6).astype(float)
            Wrand = mask * rng.uniform(0.2, 1.0, (n, n)) * g
            add("random", Wrand)

    return systems


def threshold_tpm(W: np.ndarray) -> np.ndarray:
    """Deterministic threshold-logic state-by-node TPM (2**n x n) from W.

    Node i is on at t+1 iff the weighted input from currently-on nodes exceeds
    half its total possible in-weight. This is the CLASSICAL route → Φ.
    """
    W = np.asarray(W, float)
    n = W.shape[0]
    tpm = np.zeros((2 ** n, n))
    thr = 0.5 * W.sum(axis=0)
    for idx, state in enumerate(itertools.product([0, 1], repeat=n)):
        s = np.array(state, float)
        inp = W.T @ s
        tpm[idx] = (inp > thr).astype(float)
    return tpm


if __name__ == "__main__":
    fam = make_family()
    from collections import Counter
    print("total systems:", len(fam))
    print("by topology:", dict(Counter(s["topology"] for s in fam)))
    print("by n:", dict(Counter(s["n"] for s in fam)))
    # sanity: disconnected TPM is all-zeros-input -> node off unless thr<0
    W0 = np.array(fam[0]["W"])
    print("system0 topology:", fam[0]["topology"], "| TPM sum:", threshold_tpm(W0).sum())
