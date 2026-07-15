"""Tests for the multi-agent §2.5 symmetry formalization (Φ ≤ S research)."""
import numpy as np

from predictions.multi_agent import (
    ghz_interpolation, reduced_density_matrix, trace_distance,
    global_product_of_marginals, analyze,
)


class TestGHZInterpolation:
    def test_product_limit_lambda0(self):
        psi = ghz_interpolation(3, 0.0)
        # |000>, a product state -> reduced state is pure
        rho = reduced_density_matrix(psi, 3, 0)
        assert abs(np.trace(rho @ rho) - 1.0) < 1e-9

    def test_ghz_limit_lambda1(self):
        psi = ghz_interpolation(3, 1.0)
        # maximally entangled -> reduced state maximally mixed (purity 0.5)
        rho = reduced_density_matrix(psi, 3, 0)
        assert abs(np.trace(rho @ rho) - 0.5) < 1e-9

    def test_state_normalized(self):
        for lam in (0.0, 0.3, 0.7, 1.0):
            psi = ghz_interpolation(3, lam)
            assert abs(np.vdot(psi, psi) - 1.0) < 1e-9


class TestSymmetry:
    def test_single_perspective_indistinguishable(self):
        # Bottom-up matches marginals by construction: trace distance 0 for all λ.
        res = analyze(n=3)
        assert all(r["single_perspective_trace_dist"] < 1e-9 for r in res)

    def test_joint_distinguishable_scales_with_entanglement(self):
        res = analyze(n=3)
        js = [r["joint_trace_dist"] for r in res]
        assert js[0] < 1e-9            # product limit: indistinguishable jointly too
        assert js[-1] > 0.5           # GHZ limit: strongly distinguishable jointly
        assert all(a <= b + 1e-9 for a, b in zip(js, js[1:]))  # monotone in λ

    def test_topdown_perfectly_correlated(self):
        res = analyze(n=3)
        # for λ>0, top-down cross-correlation ~1, bottom-up ~0
        nonzero = [r for r in res if r["lambda"] > 0.05]
        assert all(r["topdown_cross_corr"] > 0.95 for r in nonzero)
        assert all(abs(r["bottomup_cross_corr"]) < 0.2 for r in nonzero)

    def test_trace_distance_properties(self):
        psi = ghz_interpolation(3, 0.6)
        rho = reduced_density_matrix(psi, 3, 0)
        assert trace_distance(rho, rho) < 1e-12       # identity
        other = reduced_density_matrix(ghz_interpolation(3, 0.2), 3, 0)
        assert trace_distance(rho, other) >= 0.0      # non-negative
