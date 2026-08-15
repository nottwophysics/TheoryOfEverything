"""
Mutual-information geometry of an exact TFIM ground state (dense ED).

What is COMPUTED:
    Transverse-field Ising chain, H = -J Σ σz_i σz_{i+1} - g Σ σx_i,
    N = 10 spins, open ends, full dense diagonalization (dim 1024).
    From the exact ground state: two-site mutual information
    I(i,j) = S(i) + S(j) - S(ij) for all pairs (von Neumann entropies of
    exact reduced density matrices; eigenvalues clipped at 1e-15 before
    logs).  Then:
      - at criticality (g = J = 1): I decays monotonically with separation
        — Spearman ρ(|i-j|, I) over all pairs, acceptance ρ < -0.9;
      - deep in the paramagnet: the state is near-product, so I collapses;
      - negative control: shuffling the I values across pairs destroys the
        distance-separation monotonicity (|ρ_shuffled| small).

What is INTERPRETATION:
    The derived "distance" d(i,j) = -ln(I(i,j)/I_max) is a DEFINITION — an
    information-metric ansatz in the spirit of Van Raamsdonk
    (arXiv:1005.3035, "building up spacetime with quantum entanglement") —
    not derived geometry.  The computed results are the MI decay and the
    near-product collapse; calling -ln(I/I_max) a distance is the
    interpretive step, and it is labeled as such.

MEASURED LIMIT AT THE FROZEN PARAMAGNET POINT (recorded, not hidden):
    The memo froze "max I < 1e-2 in the paramagnet" at g = 8.0.  The exact
    value at g = 8.0 is max I = 1.41e-2 (adjacent interior pair; consistent
    with perturbation theory, bond amplitude J/4g = 1/32), so the frozen
    criterion FAILS at g = 8.0 as written.  max I crosses below 1e-2 only
    at g ≈ 10 (9.59e-3 at g = 10, 6.98e-3 at g = 12).  Per the memo's
    ground rules the threshold is not weakened here: the returned
    `near_product` flag at g = 8.0 is computed and comes out False, and a
    deeper supplementary point (g = 12) is reported separately, clearly
    labeled, where the near-product criterion does hold.

HISTORY: the "space from entanglement" demonstration this replaces used a
fabricated correlation matrix rather than a physical state and was
withdrawn by the 2026-08-15 adversarial review; reimplemented the same day
on a REAL state per REAL_PHYSICS_REIMPLEMENTATION_MEMO.md Track D (D3).
"""

import numpy as np
from scipy.stats import spearmanr

EIG_CLIP = 1e-15  # clip RDM eigenvalues before logs

_SX = np.array([[0.0, 1.0], [1.0, 0.0]])
_SZ = np.array([[1.0, 0.0], [0.0, -1.0]])


class EntanglementGeometry:
    """
    Exact-diagonalization TFIM ground states and their mutual-information
    structure.  Deterministic; every returned flag is computed.
    """

    def __init__(self, num_spins: int = 10, J: float = 1.0):
        self.num_spins = int(num_spins)
        self.J = float(J)

    # -- exact ground state ----------------------------------------------

    def _op_at(self, op: np.ndarray, site: int) -> np.ndarray:
        """Embed a single-site operator at `site` (tensor-axis convention)."""
        out = np.array([[1.0]])
        for s in range(self.num_spins):
            out = np.kron(out, op if s == site else np.eye(2))
        return out

    def tfim_hamiltonian(self, g: float) -> np.ndarray:
        """Dense H = -J Σ σz σz - g Σ σx on an open chain."""
        n = self.num_spins
        dim = 2 ** n
        H = np.zeros((dim, dim))
        for i in range(n - 1):
            H -= self.J * (self._op_at(_SZ, i) @ self._op_at(_SZ, i + 1))
        for i in range(n):
            H -= g * self._op_at(_SX, i)
        return H

    def ground_state(self, g: float) -> np.ndarray:
        """Exact ground state by dense diagonalization (deterministic)."""
        _, evecs = np.linalg.eigh(self.tfim_hamiltonian(g))
        return evecs[:, 0]

    # -- entropies and mutual information --------------------------------

    @staticmethod
    def _von_neumann(rho: np.ndarray) -> float:
        w = np.clip(np.linalg.eigvalsh(rho), EIG_CLIP, 1.0)
        return float(-np.sum(w * np.log(w)))

    def _rdm_single(self, psi: np.ndarray, i: int) -> np.ndarray:
        T = np.moveaxis(psi.reshape([2] * self.num_spins), i, 0).reshape(2, -1)
        return T @ T.conj().T

    def _rdm_pair(self, psi: np.ndarray, i: int, j: int) -> np.ndarray:
        T = np.moveaxis(psi.reshape([2] * self.num_spins), [i, j], [0, 1])
        M = T.reshape(4, -1)
        return M @ M.conj().T

    def mutual_information_matrix(self, psi: np.ndarray) -> np.ndarray:
        """I(i,j) = S(i) + S(j) - S(ij) for all pairs, from exact RDMs.

        Tiny negative values from float roundoff are floored at 0
        (I is non-negative by subadditivity).
        """
        n = self.num_spins
        S1 = [self._von_neumann(self._rdm_single(psi, i)) for i in range(n)]
        I = np.zeros((n, n))
        for i in range(n):
            for j in range(i + 1, n):
                Sij = self._von_neumann(self._rdm_pair(psi, i, j))
                I[i, j] = I[j, i] = max(S1[i] + S1[j] - Sij, 0.0)
        return I

    @staticmethod
    def distance_matrix(I: np.ndarray) -> np.ndarray:
        """d(i,j) = -ln(I(i,j)/I_max): the interpretive information-distance.

        Pairs with I = 0 get d = inf (no mutual information = infinitely
        far in this ansatz).  This is a definition, not derived geometry.
        """
        I_max = float(np.max(I))
        n = I.shape[0]
        d = np.full((n, n), np.inf)
        np.fill_diagonal(d, 0.0)
        nz = I > 0
        with np.errstate(divide="ignore"):
            d[nz] = -np.log(I[nz] / I_max)
        return d

    # -- analyses ---------------------------------------------------------

    def analyze(self, g: float) -> dict:
        """MI decay statistics for the exact ground state at field g."""
        n = self.num_spins
        psi = self.ground_state(g)
        I = self.mutual_information_matrix(psi)
        d = self.distance_matrix(I)

        separations, mi_values = [], []
        for i in range(n):
            for j in range(i + 1, n):
                separations.append(abs(i - j))
                mi_values.append(I[i, j])
        rho, _ = spearmanr(separations, mi_values)

        mean_I_by_sep = []
        mean_d_by_sep = []
        for sep in range(1, n):
            vals = [I[i, i + sep] for i in range(n - sep)]
            dvals = [d[i, i + sep] for i in range(n - sep)]
            mean_I_by_sep.append(float(np.mean(vals)))
            mean_d_by_sep.append(float(np.mean(dvals)))

        mono_d = bool(all(
            mean_d_by_sep[k + 1] > mean_d_by_sep[k]
            for k in range(len(mean_d_by_sep) - 1)
        ))

        return {
            "g": float(g),
            "J": self.J,
            "spearman_rho_sep_vs_I": float(rho),
            "monotone_decay": bool(rho < -0.9),
            "max_I": float(np.max(I)),
            "mean_I_by_separation": mean_I_by_sep,
            "mean_distance_by_separation": mean_d_by_sep,
            "distance_monotone_increasing": mono_d,
            "separations": separations,
            "mi_values": [float(v) for v in mi_values],
        }

    def shuffle_control(self, analysis: dict, seed: int = 0) -> dict:
        """Negative control: shuffle I across pairs; monotonicity must die."""
        rng = np.random.default_rng(seed)
        shuffled = np.array(analysis["mi_values"], dtype=float)
        rng.shuffle(shuffled)
        rho, _ = spearmanr(analysis["separations"], shuffled)
        return {
            "seed": int(seed),
            "spearman_rho_shuffled": float(rho),
            "monotonicity_destroyed": bool(rho > -0.9),
        }

    def demonstrate_entanglement_geometry(self,
                                          g_critical: float = 1.0,
                                          g_paramagnet: float = 8.0,
                                          g_paramagnet_deeper: float = 12.0
                                          ) -> dict:
        """
        Full Track D3 run: critical decay + paramagnet collapse + shuffle
        control.  `g_paramagnet = 8.0` is the memo's frozen point; the
        `near_product` flag there is computed honestly (it comes out False —
        max I = 1.41e-2 > 1e-2; see module docstring).  The deeper point is
        supplementary and clearly labeled — it does not replace the frozen
        criterion.
        """
        critical = self.analyze(g_critical)
        para = self.analyze(g_paramagnet)
        para_deep = self.analyze(g_paramagnet_deeper)
        shuffle = self.shuffle_control(critical, seed=0)

        threshold = 1e-2
        return {
            "num_spins": self.num_spins,
            "J": self.J,
            "critical": critical,
            "paramagnet": {
                **{k: para[k] for k in (
                    "g", "spearman_rho_sep_vs_I", "max_I",
                    "mean_I_by_separation")},
                "near_product_threshold": threshold,
                "near_product": bool(para["max_I"] < threshold),
            },
            "paramagnet_deeper_supplementary": {
                "g": para_deep["g"],
                "max_I": para_deep["max_I"],
                "near_product_threshold": threshold,
                "near_product": bool(para_deep["max_I"] < threshold),
                "label": (
                    "supplementary point, NOT the frozen g=8.0 criterion; "
                    "shows the near-product limit is reached by g ~ 10-12"
                ),
            },
            "shuffle_control": shuffle,
            "interpretation": (
                "Computed: at criticality mutual information decays "
                "monotonically with separation, and deep in the paramagnet "
                "it collapses toward a product state. Interpretive: reading "
                "-ln(I/I_max) as a distance (Van Raamsdonk arXiv:1005.3035) "
                "is an ansatz, not derived geometry. The frozen g=8.0 "
                "near-product threshold is NOT met (max I = 1.41e-2 vs "
                "1e-2); recorded honestly rather than moved."
            ),
        }
