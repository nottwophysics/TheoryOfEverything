"""Tests for the cross-validation test of the fine-structure 'rule'."""
from numerology.cross_validation import CrossValidation


class TestCrossValidation:
    def setup_method(self):
        self.cv = CrossValidation()

    def test_alpha_recipe_recovers_163_26(self):
        # The recipe must recover the celebrated alpha tokens.
        rep = self.cv.full_report()
        assert rep["alpha_base_A"] == 163
        assert rep["alpha_string_dim_B"] == 26
        assert rep["recipe_fits"]["1/alpha"]["rel_error_pct"] < 0.01

    def test_alpha_base_does_not_generalize(self):
        # The load-bearing token (163) must NOT recur for other constants;
        # that non-recurrence IS the failure of cross-validation.
        rep = self.cv.full_report()
        assert rep["other_constants_reusing_alpha_base"] == 0

    def test_koide_holdout_predicts_tau(self):
        # The genuine cross-constant rule must pass where numerology fails.
        k = self.cv.koide_predict_tau()
        assert k["rel_error_pct"] < 0.05  # holds to well under 0.05%
        assert 1770 < k["m_tau_predicted_MeV"] < 1785
