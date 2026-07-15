"""Tests for the derive-don't-fit standard for alpha (roadmap item 20)."""
import numpy as np

from numerology.derive_dont_fit import (
    score_candidate, audit_framework_candidates, first_principles_constraint,
    ALPHA_INV_CODATA, ALPHA_INV_CODATA_UNC,
)


class TestScoring:
    def test_perfect_derivation_would_pass_all(self):
        # A hypothetical ideal: exact CODATA value, no free params, axiom-forced,
        # predicts a second constant.
        r = score_candidate("ideal", ALPHA_INV_CODATA, 0, True, True)
        assert r["verdict"] == "DERIVATION"
        assert r["n_criteria_passed"] == 4

    def test_free_parameters_force_search_verdict(self):
        r = score_candidate("fit", ALPHA_INV_CODATA, 3, False, False)
        assert r["verdict"] == "SEARCH"

    def test_codata_criterion_uses_uncertainty(self):
        # A value off by more than CODATA uncertainty must fail criterion 4.
        off = ALPHA_INV_CODATA + 1e-3
        r = score_candidate("close", off, 0, True, True)
        codata_crit = [c for c in r["criteria"] if c["criterion"] == "agrees_with_codata"][0]
        assert codata_crit["passed"] is False


class TestFrameworkAudit:
    def test_no_framework_candidate_is_a_derivation(self):
        results = audit_framework_candidates()
        assert len(results) >= 3
        assert all(r["verdict"] == "SEARCH" for r in results)

    def test_v2_formula_fails_all_four(self):
        results = audit_framework_candidates()
        v2 = [r for r in results if r["name"].startswith("v2")][0]
        assert v2["n_criteria_passed"] == 0

    def test_feigenbaum_attempts_miss_badly(self):
        results = audit_framework_candidates()
        feig = [r for r in results if "self-referential" in r["name"]]
        assert feig and all(r["relative_error"] > 0.3 for r in feig)

    def test_axioms_do_not_constrain_alpha(self):
        fp = first_principles_constraint()
        assert fp["answer"] is False
