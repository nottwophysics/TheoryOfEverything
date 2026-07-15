"""Tests for P4 developed as a quantitative bounded conjecture (roadmap item 19)."""
import numpy as np

from predictions.consciousness_decoherence_bound import (
    ConsciousnessDecoherenceBound, epsilon_from_visibilities,
    upper_bound_from_null, trials_needed, REFERENCES,
    EPSILON_IS_DERIVABLE_FROM_AXIOMS,
)


class TestEpsilonMechanics:
    def test_epsilon_zero_when_visibilities_equal(self):
        assert epsilon_from_visibilities(0.9, 0.9) == 0.0

    def test_epsilon_positive_when_conscious_lower(self):
        eps = epsilon_from_visibilities(0.9, 0.81)
        assert abs(eps - 0.1) < 1e-12

    def test_upper_bound_scales_with_precision(self):
        assert upper_bound_from_null(0.02) > upper_bound_from_null(0.01)

    def test_trials_grow_as_target_shrinks(self):
        assert trials_needed(0.005, 0.05) > trials_needed(0.02, 0.05)


class TestBoundedConjecture:
    def test_null_result_bounds_epsilon(self):
        m = ConsciousnessDecoherenceBound()
        r = m.analyze_experiment(v_auto=0.90, v_conscious=0.90, sigma_V=0.01)
        assert r["consistent_with_standard_QM"] is True
        assert r["epsilon_measured"] == 0.0
        assert r["epsilon_upper_bound"] > 0.0

    def test_design_returns_positive_sample_size(self):
        m = ConsciousnessDecoherenceBound()
        d = m.design_test(epsilon_target=0.01, sigma_V_single=0.05)
        assert d["trials_required"] > 0
        assert "distinguishes_from" in d

    def test_honest_status_not_a_derivation(self):
        # The whole point: the framework CANNOT predict epsilon.
        assert EPSILON_IS_DERIVABLE_FROM_AXIOMS is False
        st = ConsciousnessDecoherenceBound().status()
        assert st["epsilon_derivable_from_axioms"] is False
        assert "conjecture" in st["classification"].lower()

    def test_references_are_dois(self):
        assert all("/" in d for d in REFERENCES.values())
        assert REFERENCES["englert_1996"] == "10.1103/PhysRevLett.77.2154"
