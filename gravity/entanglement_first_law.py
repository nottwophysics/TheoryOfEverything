"""
First law of entanglement for a free-fermion chain — exact, from the
correlation matrix.

Setup (all computed; no fits, no proxies):
    H = -Σ_i t_i (c†_i c_{i+1} + h.c.),  N = 100 sites, open ends,
    half filling (N_f = 50).
    Ground-state correlation matrix C_ij = <c†_i c_j> = Σ over the N_f
    lowest single-particle modes (Peschel 2003, arXiv:cond-mat/0212631).
    For a region A of L = 20 contiguous sites the reduced density matrix is
    Gaussian and fully determined by C_A = C restricted to A:

        S(A) = -Σ_l [ ν_l ln ν_l + (1-ν_l) ln(1-ν_l) ],   ν_l = eig(C_A)
        K_A  = Σ_ij k_ij c†_i c_j + const,   k = ln((1-C_A)/C_A)

    (k is the exact modular Hamiltonian kernel for a Gaussian state; the
    eigenvalues are clipped to [1e-12, 1-1e-12] before any log — numerical
    hygiene, not physics.)

The first law of entanglement: for ANY perturbation of the global state,

        δS(A) = δ<K_A>          to first order,

with the exact deficit δ<K_A> − δS(A) = S(ρ_A ‖ ρ_A⁰) ≥ 0 (a relative
entropy), which is second order in the perturbation.  The perturbation
family here is a smooth bond-strength modulation t_i = 1 + ε cos(2πi/N)
of the ground state, and this module verifies:
  - |δS − δ<K_A>| scales as ε² — log-log slope 2 ± 0.2 over ε ∈ [1e-3, 1e-1]
    — and is < 1e-6 at ε = 1e-4;
  - the deficit is non-negative at every ε (relative-entropy positivity);
  - negative control: replacing k by a WRONG generator (the subregion
    Hamiltonian h_A) breaks the first-order equality — the mismatch then
    scales as ε¹, not ε².

Why a BOND perturbation and not a site potential: at half filling the
hopping chain is particle-hole symmetric, and the linear response of S(A)
to ANY site potential vanishes identically (the first-order δC_A lives on
the same-sublattice matrix elements, while k lives on the opposite-
sublattice ones, so Tr(k δC_A) = 0 at first order).  With a site potential
both δS and δ<K_A> start at ε², the slope-2 check becomes degenerate, and
the negative control stops discriminating.  A hopping modulation has
genuine first-order response, so slope 2 here is a real statement about
first-order agreement.

Context, honestly stated: δS = δ<K_A> is the computable kernel behind
"gravity from entanglement" programs — Faulkner, Guica, Hartman, Myers and
Van Raamsdonk (arXiv:1312.7856) obtain linearized Einstein equations from
it in holographic CFTs, and Jacobson (arXiv:1505.04753) posits it as an
entanglement-equilibrium principle.  This module verifies the first law
for a 1D lattice chain ONLY: it derives no gravitational equation, and no
consciousness claim is made — any such connection is interpretation, not
computation.

HISTORY: the demonstration this replaces ("Einstein equations recovered"
from an entropy defined out of T_00) was found defective by the 2026-08-15
adversarial review; reimplemented the same day per
REAL_PHYSICS_REIMPLEMENTATION_MEMO.md Track D (D2).
"""

import numpy as np

CLIP = 1e-12  # keep correlation eigenvalues away from 0/1 before logs


class EntanglementFirstLaw:
    """
    Exact first-law-of-entanglement check on a tight-binding chain.

    Everything is deterministic (fixed lattice, fixed smooth bond
    modulation); returned flags are computed from the numbers, never set.
    """

    def __init__(self, num_sites: int = 100, region_size: int = 20):
        self.num_sites = int(num_sites)
        self.region_size = int(region_size)
        start = (self.num_sites - self.region_size) // 2
        self.region = np.arange(start, start + self.region_size)
        self.num_filled = self.num_sites // 2  # half filling
        # Smooth deterministic bond modulation (see module docstring for
        # why a bond — not site — perturbation is required at half filling).
        bonds = np.arange(self.num_sites - 1)
        self.bond_modulation = np.cos(2 * np.pi * bonds / self.num_sites)

    # -- single-particle building blocks ---------------------------------

    def single_particle_hamiltonian(self, epsilon: float = 0.0) -> np.ndarray:
        """h_ij for H = -Σ t_i (c†_i c_{i+1} + h.c.), t_i = 1 + ε·cos(2πi/N)."""
        n = self.num_sites
        t = 1.0 + epsilon * self.bond_modulation
        h = np.zeros((n, n))
        for i in range(n - 1):
            h[i, i + 1] = h[i + 1, i] = -t[i]
        return h

    def correlation_matrix(self, epsilon: float = 0.0) -> np.ndarray:
        """C_ij = <c†_i c_j> in the many-body ground state at half filling.

        Exact for free fermions: fill the N/2 lowest single-particle modes,
        C = Φ_occ Φ_occ† (Slater determinant → correlation matrix).
        """
        h = self.single_particle_hamiltonian(epsilon)
        _, evecs = np.linalg.eigh(h)
        occ = evecs[:, : self.num_filled]
        return occ @ occ.T

    def region_correlation(self, epsilon: float = 0.0) -> np.ndarray:
        """C_A: the correlation matrix restricted to region A."""
        C = self.correlation_matrix(epsilon)
        return C[np.ix_(self.region, self.region)]

    # -- entanglement quantities (exact for Gaussian states) -------------

    @staticmethod
    def entanglement_entropy(C_A: np.ndarray) -> float:
        """S(A) = -Σ [ν ln ν + (1-ν) ln(1-ν)] over eigenvalues ν of C_A."""
        nu = np.clip(np.linalg.eigvalsh(C_A), CLIP, 1.0 - CLIP)
        return float(-np.sum(nu * np.log(nu) + (1.0 - nu) * np.log(1.0 - nu)))

    @staticmethod
    def modular_hamiltonian(C_A: np.ndarray) -> np.ndarray:
        """Single-particle modular kernel k = ln((1-C_A)/C_A).

        Computed as a matrix function via the eigendecomposition of C_A,
        with eigenvalues clipped away from 0/1 before the log.
        ρ_A ∝ exp(-Σ_ij k_ij c†_i c_j) reproduces C_A exactly.
        """
        nu, U = np.linalg.eigh(C_A)
        nu = np.clip(nu, CLIP, 1.0 - CLIP)
        return U @ np.diag(np.log((1.0 - nu) / nu)) @ U.T

    # -- the first-law check ---------------------------------------------

    def first_law_check(self, eps_grid: np.ndarray = None,
                        eps_small: float = 1e-4) -> dict:
        """
        Verify δS(A) = δ<K_A> to first order along the bond-modulation
        family, with the wrong-generator negative control.

        For each ε:
            δS  = S(C_A(ε)) − S(C_A(0))                (exact entropies)
            δK  = Tr[k · (C_A(ε) − C_A(0))]            (k from the ε=0 state)
            δK' = Tr[h_A · (C_A(ε) − C_A(0))]          (WRONG generator:
                                                        subregion Hamiltonian)
        The first law predicts |δS − δK| = O(ε²) (it equals the relative
        entropy S(ρ_A‖ρ_A⁰) ≥ 0), while |δS − δK'| = O(ε) because h_A is
        NOT the modular Hamiltonian.
        """
        if eps_grid is None:
            eps_grid = np.logspace(-3, -1, 7)  # memo range [1e-3, 1e-1]

        C_A0 = self.region_correlation(0.0)
        S0 = self.entanglement_entropy(C_A0)
        k0 = self.modular_hamiltonian(C_A0)
        h_A = self.single_particle_hamiltonian(0.0)[
            np.ix_(self.region, self.region)]

        def deltas(eps):
            C_A = self.region_correlation(eps)
            dC = C_A - C_A0
            dS = self.entanglement_entropy(C_A) - S0
            dK = float(np.trace(k0 @ dC))
            dK_wrong = float(np.trace(h_A @ dC))
            return dS, dK, dK_wrong

        mismatch, mismatch_wrong, deficit_signed = [], [], []
        for eps in eps_grid:
            dS, dK, dKw = deltas(eps)
            mismatch.append(abs(dS - dK))
            mismatch_wrong.append(abs(dS - dKw))
            deficit_signed.append(dK - dS)  # = S(ρ_A(ε) ‖ ρ_A(0)) ≥ 0

        log_eps = np.log(np.asarray(eps_grid))
        slope = float(np.polyfit(log_eps, np.log(mismatch), 1)[0])
        slope_wrong = float(np.polyfit(log_eps, np.log(mismatch_wrong), 1)[0])

        dS_s, dK_s, dKw_s = deltas(eps_small)
        mismatch_small = abs(dS_s - dK_s)
        mismatch_wrong_small = abs(dS_s - dKw_s)

        slope_ok = bool(abs(slope - 2.0) <= 0.2)
        small_ok = bool(mismatch_small < 1e-6)
        rel_ent_ok = bool(min(deficit_signed) >= -1e-12)
        wrong_breaks = bool(
            slope_wrong < 1.5
            and mismatch_wrong_small > 100.0 * mismatch_small
        )

        return {
            "num_sites": self.num_sites,
            "region": [int(self.region[0]), int(self.region[-1]) + 1],
            "num_filled": self.num_filled,
            "S_region": float(S0),
            "epsilons": [float(e) for e in eps_grid],
            "mismatch": [float(m) for m in mismatch],
            "mismatch_wrong_K": [float(m) for m in mismatch_wrong],
            "deficit_signed": [float(d) for d in deficit_signed],
            "loglog_slope": slope,
            "loglog_slope_wrong_K": slope_wrong,
            "eps_small": float(eps_small),
            "mismatch_at_eps_small": float(mismatch_small),
            "wrong_mismatch_at_eps_small": float(mismatch_wrong_small),
            "slope_within_2_pm_0.2": slope_ok,
            "small_eps_below_1e-6": small_ok,
            "relative_entropy_nonnegative": rel_ent_ok,
            "first_law_holds": bool(slope_ok and small_ok),
            "wrong_K_breaks_first_order": wrong_breaks,
            "interpretation": (
                "delta S = delta <K_A> verified to first order for a free-"
                "fermion chain; the deficit is the (non-negative) relative "
                "entropy, second order in epsilon. This is the computable "
                "kernel of entanglement-thermodynamics programs (Faulkner et "
                "al. arXiv:1312.7856; Jacobson arXiv:1505.04753); it is NOT "
                "a derivation of the Einstein equations."
            ),
        }

    def demonstrate_first_law(self) -> dict:
        """Convenience wrapper used by experiments: run the default check."""
        return self.first_law_check()
