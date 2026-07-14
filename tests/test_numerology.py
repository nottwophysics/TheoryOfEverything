"""Tests for the look-elsewhere analysis of the fine-structure 'derivation'."""
import numpy as np
from numerology.look_elsewhere import LookElsewhereAnalysis, PHYSICS_CONSTANTS


class TestLookElsewhere:
    def setup_method(self):
        self.la = LookElsewhereAnalysis()

    def test_family_reproduces_claimed_formula(self):
        # 163 - 26 + pi/100 must be a member of the enumerated family.
        alpha = PHYSICS_CONSTANTS["1/alpha (fine-structure inverse)"]
        claim = 163 - 26 + np.pi / 100
        vals = self.la.values_in_range(claim - 1e-9, claim + 1e-9)
        assert np.min(np.abs(vals - claim)) < 1e-9

    def test_many_formulas_match_alpha(self):
        # The whole point: the claimed 0.003% hit is NOT unique.
        alpha = PHYSICS_CONSTANTS["1/alpha (fine-structure inverse)"]
        claim_err = abs((163 - 26 + np.pi / 100) - alpha) / alpha
        n = self.la.hits_for_target(alpha, claim_err)
        assert n >= 50, f"expected many equally-good formulas, got {n}"

    def test_coverage_near_alpha_is_saturated(self):
        # Family can hit essentially any target near 137 at 0.01%.
        cov = self.la.coverage(130, 145, 1e-4)
        assert cov > 0.99, f"coverage {cov} not saturated"

    def test_closest_beats_the_claim(self):
        # A better 'derivation' than the celebrated one exists in the family.
        alpha = PHYSICS_CONSTANTS["1/alpha (fine-structure inverse)"]
        best = self.la.closest_value(alpha)
        claim_err = abs((163 - 26 + np.pi / 100) - alpha) / alpha
        best_err = abs(best - alpha) / alpha
        assert best_err < claim_err


class TestLookElsewhereExperiment:
    """The main.py teaching demo (experiment 31) that wraps LookElsewhereAnalysis."""

    def test_experiment_runs_and_reports_completed(self, capsys):
        import main
        result = main.look_elsewhere_experiment()
        assert result["status"] == "completed"
        assert result["experiment"] == 31
        out = capsys.readouterr().out
        # the demo must actually surface the look-elsewhere message
        assert "LOOK-ELSEWHERE" in out.upper()
        assert "163 - 26 + pi/100" in out

    def test_registered_in_experiments_map(self):
        # experiment 31 must be reachable via the CLI dispatch table
        import inspect
        import main
        src = inspect.getsource(main.main)
        assert "31: look_elsewhere_experiment" in src
