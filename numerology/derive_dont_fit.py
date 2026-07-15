"""
The derive-don't-fit standard for α (roadmap item 20)
=====================================================

The framework claims the fine-structure constant α is *determined* by structure.
The roadmap fixes the standard such a claim must meet:

    zero free parameters, fixed by axioms, predicts α AND a second constant,
    agrees with CODATA.

Until that bar is cleared the work is a *search*, not a derivation. This module
makes the standard explicit and MECHANICALLY CHECKABLE: it scores any candidate
α formula on four independent criteria, and — the honest interim goal the
roadmap names — asks whether the framework's axioms constrain α to any range at
all from first principles (spoiler: as implemented, they do not).

The four criteria (each a hard pass/fail):
  1. ZERO FREE PARAMETERS — the recipe introduces no integer/real chosen to hit
     the target. A formula like ``163 - 26 + π/100`` fails: 163, 26 and the
     denominator 100 are all selected because they land near 137.
  2. FIXED BY AXIOMS — every ingredient is forced by a stated axiom of the
     framework, not imported from unrelated mathematics (Heegner numbers,
     bosonic-string critical dimension) purely because the number is convenient.
  3. PREDICTS A SECOND CONSTANT — the SAME parameter-free recipe, with nothing
     re-chosen, also lands a different measured constant. (This is what a real
     relation does — cf. Koide predicting m_τ from m_e, m_μ.)
  4. AGREES WITH CODATA — matches the recommended value within its uncertainty,
     not merely "to 0.003 %".

A candidate is a DERIVATION only if it passes all four. Anything short is a
SEARCH, and should be labelled as one.

CODATA 2022 recommended value:
    α⁻¹ = 137.035999177(21)   (relative uncertainty ~1.5e-10)
    (Mohr, Newell, Taylor & Tiesinga, "CODATA recommended values of the
     fundamental physical constants: 2022", Rev. Mod. Phys. 97, 025002 (2025),
     DOI 10.1103/RevModPhys.97.025002 — DOI verified via CrossRef.)
"""

from __future__ import annotations

import numpy as np

ALPHA_INV_CODATA = 137.035999177
ALPHA_INV_CODATA_UNC = 0.000000021
CODATA_DOI = "10.1103/RevModPhys.97.025002"


class Criterion:
    """One pass/fail check with a recorded justification."""

    def __init__(self, name: str, passed: bool, detail: str):
        self.name = name
        self.passed = passed
        self.detail = detail

    def as_dict(self) -> dict:
        return {"criterion": self.name, "passed": self.passed, "detail": self.detail}


def score_candidate(name: str, value: float, n_free_parameters: int,
                    ingredients_forced_by_axioms: bool,
                    predicts_second_constant: bool,
                    second_constant_detail: str = "") -> dict:
    """Score an α candidate against the four derive-don't-fit criteria.

    ``value`` is the predicted α⁻¹. The CODATA-agreement criterion is computed
    (matches within CODATA uncertainty); the other three are supplied by the
    caller because they are facts about the *construction*, not the number.
    """
    within_codata = abs(value - ALPHA_INV_CODATA) <= ALPHA_INV_CODATA_UNC
    rel_err = abs(value - ALPHA_INV_CODATA) / ALPHA_INV_CODATA

    crits = [
        Criterion("zero_free_parameters", n_free_parameters == 0,
                  f"{n_free_parameters} free parameter(s) in the recipe"),
        Criterion("fixed_by_axioms", ingredients_forced_by_axioms,
                  "all ingredients forced by a stated axiom"
                  if ingredients_forced_by_axioms else
                  "ingredients imported for numerical convenience, not from axioms"),
        Criterion("predicts_second_constant", predicts_second_constant,
                  second_constant_detail or
                  ("same recipe lands a second measured constant"
                   if predicts_second_constant else
                   "no second constant predicted by the same parameter-free recipe")),
        Criterion("agrees_with_codata", within_codata,
                  f"predicts {value:.6f}, CODATA {ALPHA_INV_CODATA:.6f} "
                  f"± {ALPHA_INV_CODATA_UNC:.0e} (rel. err {rel_err:.2e}, "
                  f"{'within' if within_codata else 'OUTSIDE'} uncertainty)"),
    ]
    is_derivation = all(c.passed for c in crits)
    return {
        "name": name,
        "predicted_alpha_inv": value,
        "relative_error": rel_err,
        "criteria": [c.as_dict() for c in crits],
        "n_criteria_passed": sum(c.passed for c in crits),
        "verdict": "DERIVATION" if is_derivation else "SEARCH",
    }


def audit_framework_candidates() -> list:
    """Apply the standard to the framework's own α attempts, using values
    computed live from its modules where possible."""
    out = []

    # 1. The celebrated v2 formula: 163 - 26 + pi/100.
    v2 = 163 - 26 + np.pi / 100
    out.append(score_candidate(
        "v2: 163 - 26 + pi/100 (Heegner + bosonic dim)",
        value=v2, n_free_parameters=3,  # 163, 26, and denom 100 all chosen
        ingredients_forced_by_axioms=False,
        predicts_second_constant=False,
        second_constant_detail="163 (Heegner) recurs in 0 of 5 other constants "
                               "(see numerology/cross_validation.py)"))

    # 2-4. The v3 'first-principles' attempts (Feigenbaum self-reference).
    from numerology.fine_structure_v3 import FineStructureV3
    v3 = FineStructureV3().run_all_approaches()
    for attempt in v3["self_referential"]["attempts"]:
        out.append(score_candidate(
            f"v3 self-referential: {attempt['method']}",
            value=attempt["alpha_inv"], n_free_parameters=0,
            # ingredients are universal constants (Feigenbaum) — genuinely not
            # tuned — but they are not forced by any *stated* axiom either.
            ingredients_forced_by_axioms=False,
            predicts_second_constant=False,
            second_constant_detail="misses alpha by "
                                   f"{attempt['error_pct']:.0f}% — no second "
                                   "constant attempted"))
    return out


def first_principles_constraint() -> dict:
    """The honest interim goal: do the axioms constrain α to ANY range from
    first principles, with zero free parameters?

    We look for any parameter-free quantity the framework's axioms fix that has
    the dimension of (or bounds) a coupling. The consciousness field is a
    normalized complex array; its only scalar invariant is the dimensionless
    'coherence' in [0, 1]. No axiom maps that to α, and no axiom bounds α to a
    sub-range of (0, ∞). The framework therefore does not constrain α at all —
    every α value is equally compatible with the stated axioms."""
    return {
        "question": "Do the axioms constrain alpha to any range from first principles?",
        "answer": False,
        "what_would_count": (
            "A parameter-free inequality derived from the axioms, e.g. "
            "'the coherence functional is stationary only for 1/alpha in [a, b]'. "
            "No such inequality exists in the framework as implemented."
        ),
        "only_axiom_scalar": "coherence in [0, 1] (dimensionless; not mapped to alpha)",
        "conclusion": (
            "The framework does not constrain alpha, even loosely. The alpha "
            "work is a numerical SEARCH over convenient constants, correctly "
            "housed in numerology/. Calling it a derivation is unsupported."
        ),
    }


def _main() -> None:
    print("DERIVE-DON'T-FIT STANDARD FOR alpha")
    print("=" * 60)
    print(f"CODATA 2022: 1/alpha = {ALPHA_INV_CODATA} +/- {ALPHA_INV_CODATA_UNC}")
    print("\nAudit of the framework's own candidates:")
    for r in audit_framework_candidates():
        passed = r["n_criteria_passed"]
        print(f"\n  {r['name']}")
        print(f"    predicts 1/alpha = {r['predicted_alpha_inv']:.4f} "
              f"(rel err {r['relative_error']:.2e})")
        print(f"    criteria passed: {passed}/4  ->  {r['verdict']}")
        for c in r["criteria"]:
            mark = "PASS" if c["passed"] else "FAIL"
            print(f"      [{mark}] {c['criterion']}: {c['detail']}")
    print("\n" + "=" * 60)
    fp = first_principles_constraint()
    print(f"First-principles constraint on alpha? {fp['answer']}")
    print(f"  {fp['conclusion']}")


if __name__ == "__main__":
    _main()
