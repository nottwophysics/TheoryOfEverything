"""
Independent entanglement-entropy pipeline for the Φ ≤ S test.

Computes the von Neumann entanglement entropy S of the transverse-field Ising
ground state of each system in the shared family (`phi_s_systems`, seed 42),
across a site bipartition. This is computed with NOTHING shared with the Φ
pipeline except the coupling matrix W — the independence that makes the Φ ≤ S
test non-circular.

    H(W) = − Σ_{i<j} W_ij Z_i Z_j − h Σ_i X_i        (h = H_FIELD = 1.0)

S = − Tr(ρ_A log₂ ρ_A),  ρ_A = Tr_B |gs⟩⟨gs|,  A = first ⌈n/2⌉ sites.

Reference for entanglement entropy / area laws: Eisert, Cramer & Plenio,
Rev. Mod. Phys. 82, 277 (2010), DOI 10.1103/RevModPhys.82.277.
"""

from __future__ import annotations

import numpy as np

from predictions.phi_s_systems import make_family, H_FIELD

# single-qubit Paulis
_I = np.eye(2)
_X = np.array([[0.0, 1.0], [1.0, 0.0]])
_Z = np.array([[1.0, 0.0], [0.0, -1.0]])


def _op_on(op: np.ndarray, site: int, n: int) -> np.ndarray:
    """Embed single-site operator on `site` into the n-qubit space."""
    mats = [op if k == site else _I for k in range(n)]
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out


def ising_hamiltonian(W: np.ndarray, h: float = H_FIELD) -> np.ndarray:
    """Transverse-field Ising Hamiltonian for coupling matrix W."""
    W = np.asarray(W, float)
    n = W.shape[0]
    dim = 2 ** n
    H = np.zeros((dim, dim))
    for i in range(n):
        for j in range(i + 1, n):
            if W[i, j] != 0.0:
                H -= W[i, j] * _op_on(_Z, i, n) @ _op_on(_Z, j, n)
    for i in range(n):
        H -= h * _op_on(_X, i, n)
    return H


def ground_state(W: np.ndarray, h: float = H_FIELD) -> np.ndarray:
    H = ising_hamiltonian(W, h)
    vals, vecs = np.linalg.eigh(H)
    return vecs[:, 0]  # lowest eigenvalue


def entanglement_entropy(psi: np.ndarray, n: int, cut: int = None) -> float:
    """Von Neumann entropy (base 2) across bipartition A=[0..cut), B=[cut..n)."""
    if cut is None:
        cut = (n + 1) // 2
    dimA, dimB = 2 ** cut, 2 ** (n - cut)
    psi_mat = psi.reshape(dimA, dimB)
    # reduced density matrix on A via SVD (numerically stable)
    s = np.linalg.svd(psi_mat, compute_uv=False)
    p = s ** 2
    p = p[p > 1e-15]
    p = p / p.sum()
    return float(-np.sum(p * np.log2(p)))


def S_of_W(W: np.ndarray, h: float = H_FIELD) -> float:
    W = np.asarray(W, float)
    n = W.shape[0]
    return entanglement_entropy(ground_state(W, h), n)


def run(out_json: str) -> dict:
    import json
    fam = make_family()
    results = []
    for sysd in fam:
        W = np.array(sysd["W"], float)
        S = S_of_W(W)
        results.append({"id": sysd["id"], "topology": sysd["topology"],
                        "n": sysd["n"], "S": S})
    json.dump(results, open(out_json, "w"))
    Ss = [r["S"] for r in results]
    return {"n_systems": len(results),
            "S_range": [min(Ss), max(Ss)],
            "S_zero_count": sum(1 for s in Ss if s < 1e-9)}


if __name__ == "__main__":
    summary = run("/tmp/phi_s/S.json")
    import json
    print(json.dumps(summary, indent=1))
