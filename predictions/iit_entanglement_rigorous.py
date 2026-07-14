"""
Rigorous IIT–Entanglement Bridge Test (non-circular)
====================================================

The original test (`predictions/iit_bridge.py::IITEntanglementBridge.
test_conjecture`) is circular: for each trial it computes both Φ and the
entanglement entropy S from the *same* scalar — the total connectivity ΣW of one
random matrix. Φ comes from `compute_phi(W)`, and S comes from a quantum state
built by a linear interpolation keyed to `ΣW / n²`. Two deterministic functions
of one variable are trivially perfectly (anti-)correlated, so the reported
"100% hold rate" and Φ–S correlation of −1.0 are artifacts of construction, not
evidence for any conjecture Φ ≤ S.

This module rebuilds the test so it can actually fail:

1. **Independent, structured mapping.** The quantum state is the ground state of
   a transverse-field Ising Hamiltonian whose couplings are the FULL off-diagonal
   structure of W (every pair W_ij), not just its sum:

       H(W) = - Σ_{i<j} W_ij Z_i Z_j  -  h Σ_i X_i

   Φ(W) uses W's partition structure (the minimum-information partition); S uses
   W's coupling geometry via a distinct nonlinear map (ground-state
   entanglement). Neither is a function of ΣW alone, so a correlation between
   them — if any — is a real finding, not a tautology.

2. **A null model.** We permute the Φ–S pairing (pair Φ(W_k) with S from a
   *different* trial's network) and recompute. If the conjecture "holds" and the
   correlation look the same under the null, the result is uninformative. Only a
   real signal survives the permutation test.

3. **An independent-draw baseline.** Φ from one random W, S from the ground state
   of an *independently* drawn W'. This is what genuine "no relationship" looks
   like and calibrates the reader's expectation.

Nothing here endorses IIT, the consciousness-first framework, or the conjecture;
it only replaces a circular test with one that has the power to reject it.
"""

from __future__ import annotations

from itertools import combinations

import numpy as np

from predictions.iit_bridge import IntegratedInformation, EntanglementEntropy


# --- single-qubit Pauli matrices ------------------------------------------
_I2 = np.eye(2, dtype=np.complex128)
_X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
_Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)


def _op_on(site: int, op: np.ndarray, n: int) -> np.ndarray:
    """Embed a single-site operator into the n-qubit Hilbert space."""
    mats = [op if k == site else _I2 for k in range(n)]
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out


def _op_on_pair(i: int, j: int, op: np.ndarray, n: int) -> np.ndarray:
    """Embed op⊗op acting on sites i and j into the n-qubit space."""
    mats = [op if (k == i or k == j) else _I2 for k in range(n)]
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out


class RigorousIITEntanglementBridge:
    """Non-circular test of the conjecture Φ ≤ S_entanglement."""

    def __init__(self, num_nodes: int = 4, transverse_field: float = 1.0):
        self.n = num_nodes
        self.h = transverse_field
        self.iit = IntegratedInformation(num_nodes)
        self.ent = EntanglementEntropy(num_nodes)

    # -- physical channel: W -> quantum ground state -----------------------

    def ground_state(self, W: np.ndarray) -> np.ndarray:
        """
        Ground state of the transverse-field Ising Hamiltonian with couplings
        given by the full symmetric off-diagonal structure of W.

            H = - Σ_{i<j} W_ij Z_i Z_j - h Σ_i X_i

        Uses every pairwise coupling, so the resulting entanglement depends on
        W's geometry, not merely on ΣW.
        """
        n = self.n
        dim = 2 ** n
        H = np.zeros((dim, dim), dtype=np.complex128)
        for i in range(n):
            for j in range(i + 1, n):
                if W[i, j] != 0:
                    H -= W[i, j] * _op_on_pair(i, j, _Z, n)
        for i in range(n):
            H -= self.h * _op_on(i, _X, n)
        evals, evecs = np.linalg.eigh(H)
        return evecs[:, 0]  # ground state (lowest eigenvalue)

    # -- one trial ---------------------------------------------------------

    def _phi_and_S(self, W: np.ndarray) -> tuple[float, float]:
        phi = self.iit.compute_phi(W)["phi"]
        S = self.ent.total_entanglement(self.ground_state(W))
        return float(phi), float(S)

    # -- the full experiment ----------------------------------------------

    def run(self, num_trials: int = 200, seed: int = 42,
            n_perm: int = 2000) -> dict:
        """
        Returns real, null, and independent-draw statistics.

        Real:        (Φ_k, S_k) both from the SAME network W_k.
        Null:        S values permuted across trials (pairing broken).
        Independent: Φ from W_k, S from an independently drawn W'_k.
        """
        rng = np.random.default_rng(seed)

        phis, Ss, Ss_indep = [], [], []
        for _ in range(num_trials):
            W = self._random_network(rng)
            phi, S = self._phi_and_S(W)
            phis.append(phi)
            Ss.append(S)
            # independent-draw baseline: S from a different, unrelated network
            W2 = self._random_network(rng)
            Ss_indep.append(self._phi_and_S(W2)[1])

        phis = np.array(phis)
        Ss = np.array(Ss)
        Ss_indep = np.array(Ss_indep)

        real = self._pair_stats(phis, Ss)
        indep = self._pair_stats(phis, Ss_indep)

        # permutation null: shuffle S against Φ many times
        null_corr = np.empty(n_perm)
        null_hold = np.empty(n_perm)
        for p in range(n_perm):
            perm = rng.permutation(Ss)
            null_corr[p] = self._safe_corr(phis, perm)
            null_hold[p] = np.mean(phis <= perm + 1e-9)

        # empirical two-sided p for the real correlation against the null
        obs = real["pearson"]
        p_corr = float((np.sum(np.abs(null_corr) >= abs(obs)) + 1) / (n_perm + 1))

        return {
            "conjecture": "Phi <= S_entanglement",
            "num_trials": num_trials,
            "transverse_field_h": self.h,
            "real": real,
            "independent_draw": indep,
            "null_pairing": {
                "mean_correlation": float(np.mean(null_corr)),
                "std_correlation": float(np.std(null_corr)),
                "mean_hold_rate": float(np.mean(null_hold)),
            },
            "permutation_test": {
                "n_perm": n_perm,
                "observed_pearson": float(obs),
                "p_value_two_sided": p_corr,
                "significant_at_0.05": bool(p_corr < 0.05),
            },
            "verdict": self._verdict(
                real, null_corr, p_corr,
                indep_hold=indep["hold_rate"],
                null_hold=float(np.mean(null_hold))),
        }

    # -- helpers -----------------------------------------------------------

    @staticmethod
    def _random_network(rng) -> np.ndarray:
        n = 4
        W = rng.random((n, n)) * 0.5
        W = (W + W.T) / 2.0  # symmetric couplings
        np.fill_diagonal(W, 0.0)
        return W

    @staticmethod
    def _safe_corr(a: np.ndarray, b: np.ndarray) -> float:
        if np.std(a) < 1e-12 or np.std(b) < 1e-12:
            return 0.0
        return float(np.corrcoef(a, b)[0, 1])

    def _pair_stats(self, phis: np.ndarray, Ss: np.ndarray) -> dict:
        from scipy.stats import spearmanr
        hold = float(np.mean(phis <= Ss + 1e-9))
        margin = Ss - phis
        sp = spearmanr(phis, Ss)
        return {
            "hold_rate": hold,
            "pearson": self._safe_corr(phis, Ss),
            "spearman": float(sp.statistic) if np.std(phis) > 1e-12 else 0.0,
            "mean_phi": float(np.mean(phis)),
            "mean_S": float(np.mean(Ss)),
            "mean_margin_S_minus_phi": float(np.mean(margin)),
            "min_margin": float(np.min(margin)),
        }

    @staticmethod
    def _verdict(real: dict, null_corr: np.ndarray, p_corr: float,
                 indep_hold: float, null_hold: float) -> str:
        parts = [f"Phi <= S holds in {real['hold_rate']*100:.1f}% of trials"]
        # The hold rate is uninformative if it is essentially unchanged when the
        # pairing is broken (independent draw) or shuffled (null). This is a
        # threshold-free control comparison, not a hand-picked cutoff on the Φ/S
        # ratio: if all three hold rates agree, "Φ ≤ S holds" carries no evidence
        # about a Φ–S relationship.
        spread = max(abs(real["hold_rate"] - indep_hold),
                     abs(real["hold_rate"] - null_hold))
        if spread < 0.02:
            parts.append(
                "but this carries NO evidence for a Φ–S link: the same hold rate "
                f"appears when the pairing is broken (independent draw "
                f"{indep_hold*100:.1f}%) or shuffled (null {null_hold*100:.1f}%), "
                f"within {spread*100:.1f} pp of the real pairing — the inequality "
                "just reflects that this Φ estimator is numerically smaller than S")
        if p_corr < 0.05:
            parts.append(
                f"the Φ–S correlation ({real['pearson']:+.3f}) IS significant "
                f"vs the permutation null (p={p_corr:.3f}) — a real, if modest, "
                "structural relationship survives")
        else:
            parts.append(
                f"the Φ–S correlation ({real['pearson']:+.3f}) is NOT "
                f"distinguishable from the permutation null (p={p_corr:.3f}) — "
                "no relationship beyond chance")
        return "; ".join(parts) + "."


def _main() -> None:
    br = RigorousIITEntanglementBridge(num_nodes=4, transverse_field=1.0)
    r = br.run(num_trials=200, seed=42, n_perm=2000)
    print("=" * 70)
    print("RIGOROUS IIT–ENTANGLEMENT BRIDGE TEST (non-circular)")
    print("=" * 70)
    print(f"conjecture: {r['conjecture']}   (n_trials={r['num_trials']}, "
          f"h={r['transverse_field_h']})")
    print()
    for key in ("real", "independent_draw"):
        s = r[key]
        print(f"[{key}]")
        print(f"  hold rate Φ≤S : {s['hold_rate']*100:5.1f}%")
        print(f"  Pearson r     : {s['pearson']:+.3f}    "
              f"Spearman : {s['spearman']:+.3f}")
        print(f"  mean Φ={s['mean_phi']:.4f}  mean S={s['mean_S']:.4f}  "
              f"mean margin(S−Φ)={s['mean_margin_S_minus_phi']:.4f}")
        print()
    n = r["null_pairing"]
    print("[null pairing (Φ–S shuffled)]")
    print(f"  mean correlation : {n['mean_correlation']:+.3f} "
          f"± {n['std_correlation']:.3f}")
    print(f"  mean hold rate   : {n['mean_hold_rate']*100:5.1f}%")
    print()
    pt = r["permutation_test"]
    print(f"[permutation test]  observed r={pt['observed_pearson']:+.3f}  "
          f"p={pt['p_value_two_sided']:.4f}  "
          f"significant={pt['significant_at_0.05']}")
    print()
    print("VERDICT:", r["verdict"])


if __name__ == "__main__":
    _main()
