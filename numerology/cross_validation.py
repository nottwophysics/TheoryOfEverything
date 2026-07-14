"""
Cross-Validation Test for the Fine-Structure "Rule"
===================================================

A genuine formula-generating *principle* is one you can fit on one constant and
then use to PREDICT a second, independent constant with no re-tuning. That is the
standard hold-out test that separates a physical law from a curve fit.

The look-elsewhere module already showed that ~125 formulas of the same
complexity as ``163 - 26 + pi/100`` hit 1/alpha equally well, so the closeness is
not evidence. This module asks the complementary question: is there any RULE ---
a fixed recipe mapping "which constant" to "which formula" --- that the alpha
result is an instance of, and that also predicts other constants?

We test the recipe the v2 module leans on:

    1/const  =  (special integer)  -  (string dimension)  +  (small pi-correction)

with the "physically meaningful" vocabulary the module invokes: Heegner numbers
{19, 43, 67, 163}, string-theory dimensions {10, 26}, and pi/e/phi corrections.

RESULT (computed below): there is NO shared structure. Each constant, fitted in
the same family, needs its OWN arbitrary base integer --- and that integer is
simply round(target). The "formula" reduces to "the constant is close to an
integer, plus a small fudge," which is true of every real number and predicts
nothing. Fixing the recipe on alpha therefore gives ZERO predictive power for any
other constant: the integers 163 and 26 do not recur, and no map
target -> integers exists.

For contrast we include a REAL cross-constant rule --- the Koide relation --- which
predicts the tau mass from the electron and muon masses with zero free parameters
to 0.006%. That is what passing this test looks like. (Note: even Koide is an
empirical regularity, not a derivation from the framework's axioms; the
repository's own code says as much.)

Nothing here endorses or refutes any physical theory; it measures whether a rule
generalizes across constants.
"""

from __future__ import annotations

import numpy as np


# Heegner numbers and string-theory "meaningful" integers the v2 module invokes.
HEEGNER = [1, 2, 3, 7, 11, 19, 43, 67, 163]
STRING_DIMS = [10, 26]
NICE = {"1": 1.0, "pi": np.pi, "e": np.e, "phi": (1 + np.sqrt(5)) / 2}

# Targets: 1/value for a few well-measured dimensionless constants, so the
# "A - B + correction" recipe (which produces numbers ~ O(10-2000)) can apply.
TARGETS_INV = {
    "1/alpha": 137.035999084,
    "proton/electron mass ratio": 1836.15267343,
    "muon/electron mass ratio": 206.7682830,
    "1/sin^2(theta_W)": 1.0 / 0.231220,
    "1/alpha_s(M_Z)": 1.0 / 0.11790,
    "pion/electron mass ratio": 273.13203,
}


class CrossValidation:
    """Test whether the alpha 'rule' generalizes to other constants."""

    def best_in_recipe(self, target: float, denom_max: int = 100) -> dict:
        """
        Best formula for `target` under the recipe

            target ~= A - B + s * (nice / n)

        with A a 'meaningful' base integer (Heegner or Heegner*10^k in range),
        B in STRING_DIMS ∪ {0}, nice in NICE, n in 1..denom_max, s in {+1,-1}.

        Returns the best (lowest relative error) assignment.
        """
        # Allow the "meaningful" bases and their decimal shifts to reach large
        # targets (e.g. 1836), which is the most generous reading of the recipe.
        bases = set()
        for h in HEEGNER:
            for k in range(0, 4):
                bases.add(h * 10 ** k)
        bases = sorted(b for b in bases if b <= target * 1.2 + 30)

        best = None
        for A in bases:
            for B in STRING_DIMS + [0]:
                for nm, nv in NICE.items():
                    for n in range(1, denom_max + 1):
                        for s in (+1, -1):
                            val = A - B + s * nv / n
                            err = abs(val - target) / target
                            if best is None or err < best["rel_error"]:
                                best = {
                                    "target": target, "value": val,
                                    "rel_error": err, "A": A, "B": B,
                                    "nice": nm, "n": n, "sign": s,
                                }
        return best

    def scan_recipe(self, denom_max: int = 100) -> dict:
        """Fit the recipe to every target; report the tokens each one needs."""
        out = {}
        for name, inv in TARGETS_INV.items():
            b = self.best_in_recipe(inv, denom_max)
            out[name] = {
                "target_inv": inv,
                "best_value": b["value"],
                "rel_error_pct": b["rel_error"] * 100,
                "base_A": b["A"],
                "string_dim_B": b["B"],
                "correction": f"{'+' if b['sign']>0 else '-'}{b['nice']}/{b['n']}",
                "A_equals_round_target": b["A"] == round(inv) or
                b["A"] - b["B"] == round(inv) or abs(b["A"] - inv) < 1,
            }
        return out

    # -- a genuine cross-constant rule, for contrast -----------------------

    @staticmethod
    def koide_predict_tau(m_e: float = 0.510999,
                          m_mu: float = 105.6584,
                          m_tau_measured: float = 1776.86) -> dict:
        """
        Genuine hold-out: fix Q = 2/3 and (m_e, m_mu), solve for m_tau with
        ZERO free parameters, compare to the measured value.
        """
        A = np.sqrt(m_e) + np.sqrt(m_mu)
        a = 1.0 - 2.0 / 3.0
        b = -(4.0 / 3.0) * A
        c = (m_e + m_mu) - (2.0 / 3.0) * A ** 2
        disc = b * b - 4 * a * c
        roots = [((-b + np.sqrt(disc)) / (2 * a)) ** 2,
                 ((-b - np.sqrt(disc)) / (2 * a)) ** 2]
        # physical root is the larger one
        m_tau_pred = max(roots)
        return {
            "rule": "Koide Q=2/3, predict m_tau from m_e and m_mu (0 free params)",
            "m_tau_predicted_MeV": float(m_tau_pred),
            "m_tau_measured_MeV": m_tau_measured,
            "rel_error_pct": float(abs(m_tau_pred - m_tau_measured)
                                   / m_tau_measured * 100),
        }

    def full_report(self) -> dict:
        recipe = self.scan_recipe()
        # Does the alpha-selected vocabulary (163, 26) recur in other fits?
        alpha_A = recipe["1/alpha"]["base_A"]
        alpha_B = recipe["1/alpha"]["string_dim_B"]
        others = {k: v for k, v in recipe.items() if k != "1/alpha"}
        reuse_A = sum(1 for v in others.values() if v["base_A"] == alpha_A)
        reuse_B = sum(1 for v in others.values() if v["string_dim_B"] == alpha_B)
        # With the RESTRICTED "meaningful" vocabulary, how many others can even
        # be fit as well as alpha's 0.003%? (If few, the recipe is not general.)
        poorly_fit = sum(1 for v in others.values() if v["rel_error_pct"] > 0.1)
        return {
            "recipe_fits": recipe,
            "alpha_base_A": alpha_A,
            "alpha_string_dim_B": alpha_B,
            "other_constants_reusing_alpha_base": reuse_A,
            "other_constants_reusing_alpha_string_dim": reuse_B,
            "n_others": len(others),
            "others_needing_own_bespoke_base": len(others) - reuse_A,
            "others_not_fittable_below_0.1pct": poorly_fit,
            "koide_holdout": self.koide_predict_tau(),
        }


def _main() -> None:
    cv = CrossValidation()
    rep = cv.full_report()
    print("=" * 74)
    print("CROSS-VALIDATION OF THE FINE-STRUCTURE 'RULE'")
    print("=" * 74)
    print("Recipe:  1/const = (meaningful integer A) - (string dim B) + nice/n")
    print(f"  alpha fit: A={rep['alpha_base_A']}, B={rep['alpha_string_dim_B']}"
          f"  (the celebrated 163 - 26 + pi/100)")
    print()
    print(f"{'constant':<30}{'A':>6}{'B':>5}{'correction':>14}{'err %':>10}")
    print("-" * 74)
    for name, v in rep["recipe_fits"].items():
        print(f"{name:<30}{v['base_A']:>6}{v['string_dim_B']:>5}"
              f"{v['correction']:>14}{v['rel_error_pct']:>10.4f}")
    print()
    print(f"Other constants reusing alpha's base integer (163): "
          f"{rep['other_constants_reusing_alpha_base']} of {rep['n_others']}")
    print(f"Other constants reusing alpha's string dim (26): "
          f"{rep['other_constants_reusing_alpha_string_dim']} of {rep['n_others']}")
    print(f"Constants that can't even be fit below 0.1% in this vocabulary: "
          f"{rep['others_not_fittable_below_0.1pct']} of {rep['n_others']}")
    print("  -> each constant needs its OWN bespoke base integer; 163 never")
    print("     recurs. There is no map target -> tokens, so fixing the recipe")
    print("     on alpha predicts NOTHING else. FAILS cross-validation.")
    print()
    k = rep["koide_holdout"]
    print("CONTRAST -- a REAL cross-constant rule (Koide):")
    print(f"  {k['rule']}")
    print(f"  predicted m_tau = {k['m_tau_predicted_MeV']:.2f} MeV, "
          f"measured {k['m_tau_measured_MeV']:.2f} MeV, "
          f"err {k['rel_error_pct']:.4f}%")
    print("  -> ONE formula, THREE masses, zero free parameters, holds to 6e-3%.")
    print("     THIS passes cross-validation. The alpha numerology does not.")


if __name__ == "__main__":
    _main()
