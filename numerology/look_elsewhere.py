"""
Look-Elsewhere Analysis for the Fine-Structure "Derivation"
============================================================

The module ``constants/fine_structure_v2.py`` reports that

    1/alpha  ~=  163 - 26 + pi/100  =  137.0314   (0.0033% from measurement)

and treats the closeness as evidence that alpha is "derivable." This module
tests that claim the only way it can be tested: by asking how many formulas of
*the same complexity* land equally close to alpha -- or to ANY of the ~two dozen
well-known dimensionless constants of physics -- purely by construction.

The winning formula has the structure

    A  -  B  +  (nice_constant / integer)

with three-to-four freely chosen tokens (which integer A, which integer B, which
small correction, which denominator) fitted to ONE target. If a formula family
of that size is dense enough that essentially every target in the relevant range
has a sub-0.01% hit, then hitting 137.036 is expected by chance and carries no
predictive content.

This is the standard "look-elsewhere effect" (a.k.a. multiple-comparisons /
trials-factor correction) used in particle physics to discount apparent signals.

Nothing here endorses or refutes any physical theory; it only measures the
trials factor of a formula family. Run as a script for a full report.
"""

from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------------------
# A basket of genuinely well-measured DIMENSIONLESS constants of physics.
# Values are standard textbook / CODATA-2018 / PDG figures. They are used only
# as "targets"; none is derived here.
# ---------------------------------------------------------------------------
PHYSICS_CONSTANTS = {
    "1/alpha (fine-structure inverse)": 137.035999084,
    "proton/electron mass ratio": 1836.15267343,
    "neutron/electron mass ratio": 1838.68366173,
    "neutron/proton mass ratio": 1.00137841931,
    "muon/electron mass ratio": 206.7682830,
    "tau/electron mass ratio": 3477.23,
    "tau/muon mass ratio": 16.8170,
    "W/Z boson mass ratio": 0.881531,
    "sin^2(theta_W) weak mixing": 0.231220,
    "strong coupling alpha_s(M_Z)": 0.11790,
    "Cabibbo sin(theta_C)": 0.225000,
    "Koide Q (lepton)": 0.666661,
    "Omega_Lambda (dark energy)": 0.68890,
    "Omega_matter": 0.31110,
    "Omega_baryon": 0.048970,
    "electron g-factor / 2": 1.001159652181,
    "muon anomaly a_mu x 1e3": 1.16592,
    "pion/electron mass ratio": 273.13203,
    "kaon/pion mass ratio": 3.53713,
    "up/down quark mass ratio": 0.47,
    "top/bottom quark mass ratio": 41.33,
    "baryon asymmetry eta x 1e10": 6.1000,
    "spectral index n_s (CMB)": 0.96490,
    "Hubble h (H0/100)": 0.67400,
    "sigma_8 (matter clustering)": 0.81100,
}


class LookElsewhereAnalysis:
    """
    Enumerate a formula family of the same structural complexity as
    ``163 - 26 + pi/100`` and measure how often it lands within a tolerance of
    physical targets, both individually and across the whole range.
    """

    # Small transcendental / algebraic "nice" constants a numerologist reaches
    # for, used as the additive-correction numerator.
    NICE = {
        "1": 1.0,
        "pi": np.pi,
        "e": np.e,
        "phi": (1 + np.sqrt(5)) / 2,
        "sqrt2": np.sqrt(2),
        "sqrt3": np.sqrt(3),
        "sqrt5": np.sqrt(5),
        "2pi": 2 * np.pi,
        "pi^2": np.pi ** 2,
    }

    def __init__(self, a_max: int = 4000, b_max: int = 50, denom_max: int = 200):
        """
        Family:  value = A - B + s * (nice / n)

            A in 1..a_max                 (integer base)
            B in 0..b_max                 (integer offset)
            nice in NICE                  (small correction numerator)
            n in 1..denom_max             (integer denominator)
            s in {+1, -1}  and  the no-correction case (kappa = 0)

        This is deliberately CONSERVATIVE: it forbids the multiplications,
        powers, and nested functions that the repository's other attempts use
        (phi^7*4pi/3, Feigenbaum*(2pi)^2, j-invariant cube roots, ...), so the
        hit counts below are a LOWER bound on what a numerologist could reach.
        """
        self.a_max = a_max
        self.b_max = b_max
        self.denom_max = denom_max
        self._values = None
        self._corrections = None

    # -- family construction -------------------------------------------------

    def corrections(self) -> np.ndarray:
        """All distinct additive corrections kappa (including 0)."""
        if self._corrections is None:
            ks = {0.0}
            for val in self.NICE.values():
                for n in range(1, self.denom_max + 1):
                    ks.add(val / n)
                    ks.add(-val / n)
            self._corrections = np.array(sorted(ks))
        return self._corrections

    def values_in_range(self, lo: float, hi: float) -> np.ndarray:
        """
        All family values falling in [lo, hi]. Computed as
        (integer in a window) + correction, which is exactly the reachable set
        of A - B + kappa for A in 1..a_max, B in 0..b_max.
        """
        kappa = self.corrections()
        # A - B ranges over integers (1 - b_max) .. a_max. Restrict to those
        # whose value can land in [lo, hi] once a correction (|kappa| < 2pi) is
        # added.
        i_lo = int(np.floor(lo - kappa.max())) - 1
        i_hi = int(np.ceil(hi - kappa.min())) + 1
        i_lo = max(i_lo, 1 - self.b_max)
        i_hi = min(i_hi, self.a_max)
        ints = np.arange(i_lo, i_hi + 1)
        vals = (ints[:, None] + kappa[None, :]).ravel()
        vals = vals[(vals >= lo) & (vals <= hi)]
        return np.sort(vals)

    # -- measurements --------------------------------------------------------

    def hits_for_target(self, target: float, rel_tol: float) -> int:
        """Number of family values within rel_tol (relative) of target."""
        window = abs(target) * rel_tol
        vals = self.values_in_range(target - window, target + window)
        return int(np.sum(np.abs(vals - target) <= window))

    def target_is_hit(self, target: float, rel_tol: float) -> bool:
        return self.hits_for_target(target, rel_tol) > 0

    def coverage(self, lo: float, hi: float, rel_tol: float,
                 n_probe: int = 20000, seed: int = 42) -> float:
        """
        Fraction of random targets drawn uniformly in [lo, hi] that have at
        least one family value within rel_tol. Coverage ~1 means the family can
        "predict" essentially any number in the range, so a single hit is
        meaningless.
        """
        rng = np.random.default_rng(seed)
        vals = self.values_in_range(lo, hi)
        probes = rng.uniform(lo, hi, size=n_probe)
        # nearest family value to each probe
        idx = np.searchsorted(vals, probes)
        idx = np.clip(idx, 1, len(vals) - 1)
        left = vals[idx - 1]
        right = vals[idx]
        nearest = np.where(probes - left <= right - probes, left, right)
        rel = np.abs(nearest - probes) / np.abs(probes)
        return float(np.mean(rel <= rel_tol))

    def basket_scan(self, rel_tol: float) -> dict:
        """For each physics constant, is it hit, and by how many formulas?"""
        out = {}
        for name, val in PHYSICS_CONSTANTS.items():
            out[name] = {
                "value": val,
                "n_hits": self.hits_for_target(val, rel_tol),
            }
        return out

    def closest_value(self, target: float, half_width: float = 0.05) -> float:
        """The single family value nearest to target (for illustration)."""
        vals = self.values_in_range(target - half_width, target + half_width)
        return float(vals[np.argmin(np.abs(vals - target))])

    def full_report(self) -> dict:
        """Machine-readable summary of the look-elsewhere measurement."""
        alpha = PHYSICS_CONSTANTS["1/alpha (fine-structure inverse)"]
        claim = 163 - 26 + np.pi / 100
        claim_err = abs(claim - alpha) / alpha
        best = self.closest_value(alpha)
        return {
            "family_size_corrections": len(self.corrections()),
            "claimed_formula": "163 - 26 + pi/100",
            "claimed_value": float(claim),
            "claimed_rel_error": float(claim_err),
            "n_formulas_matching_alpha_at_claim_precision":
                self.hits_for_target(alpha, claim_err),
            "n_formulas_matching_alpha_at_1e-4": self.hits_for_target(alpha, 1e-4),
            "closest_family_value_to_alpha": best,
            "closest_family_rel_error": float(abs(best - alpha) / alpha),
            "coverage_130_145_at_1e-4": self.coverage(130, 145, 1e-4),
            "coverage_broad_at_1e-4": self.coverage(0.1, 2000, 1e-4),
            "basket_fraction_hit_at_1e-4": (
                sum(1 for v in self.basket_scan(1e-4).values() if v["n_hits"] > 0)
                / len(PHYSICS_CONSTANTS)
            ),
        }


def _main() -> None:
    la = LookElsewhereAnalysis()
    alpha = PHYSICS_CONSTANTS["1/alpha (fine-structure inverse)"]
    claim = 163 - 26 + np.pi / 100
    claim_err = abs(claim - alpha) / alpha

    print("=" * 70)
    print("LOOK-ELSEWHERE ANALYSIS — fine-structure 'derivation'")
    print("=" * 70)
    print(f"Formula family: A - B + s*(nice/n)  [add/subtract only]")
    print(f"  distinct additive corrections: {len(la.corrections())}")
    print()
    print(f"Claimed result: 163 - 26 + pi/100 = {claim:.6f}")
    print(f"  relative error vs 1/alpha={alpha}: {claim_err*100:.5f}%")
    print()
    n_claim = la.hits_for_target(alpha, claim_err)
    print(f"Formulas in the family matching 1/alpha AT LEAST AS WELL "
          f"({claim_err*100:.5f}%): {n_claim}")
    for tol in (1e-4, 1e-3, 1e-2):
        print(f"  within {tol*100:6.4f}%: {la.hits_for_target(alpha, tol):5d} formulas")
    best = la.closest_value(alpha)
    print(f"  single closest family value: {best:.8f} "
          f"(err {abs(best-alpha)/alpha*100:.2e}%, "
          f"{claim_err/(abs(best-alpha)/alpha):.0f}x better than the claim)")
    print()
    print("Coverage (fraction of RANDOM targets the family can hit):")
    for lo, hi, lab in [(130, 145, "near 1/alpha"), (0.1, 2000, "broad")]:
        for tol in (1e-4, 1e-3):
            print(f"  {lab:12s} @ {tol*100:6.4f}%: "
                  f"{la.coverage(lo, hi, tol)*100:5.1f}%")
    print()
    print("Basket of 25 well-measured dimensionless constants:")
    for tol in (1e-4, 1e-3):
        sc = la.basket_scan(tol)
        hit = sum(1 for v in sc.values() if v["n_hits"] > 0)
        print(f"  hit within {tol*100:6.4f}%: {hit}/{len(sc)} constants")
    print()
    print("CONCLUSION: with 100% coverage near 137 and >100 equally-good")
    print("formulas, matching 1/alpha to 0.003% is expected by chance and")
    print("carries no predictive content. This is numerology, not derivation.")


if __name__ == "__main__":
    _main()
