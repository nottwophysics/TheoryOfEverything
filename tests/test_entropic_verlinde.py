"""
Track C acceptance tests — faithful Verlinde entropic gravity (SI units).

Pre-registered criteria (REAL_PHYSICS_REIMPLEMENTATION_MEMO.md, 2026-08-15):
  C1  both routes (Unruh, screen-equipartition) equal Newton's GMm/r^2 to
      1e-12 relative across a lab-to-astronomical grid of M, m, r;
  C2  the legacy screen-area route is retained as screen_area_route_wrong()
      and demonstrably does NOT reproduce Newton (negative control);
  C3  programmatic dimensional bookkeeping over (kg, m, s, K) exponent
      tuples verifies F has dimensions kg·m·s^-2;
  C4  recover_newton() keeps its return keys and newton_recovered is
      computed (True because the derivation is faithful), with negative
      controls showing the verdict flips when the derivation is broken.
"""

import numpy as np
import pytest

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from gravity.entropic import (
    EntropicGravity,
    combine_dimensions,
    DIMENSIONS,
    C_LIGHT,
    G_NEWTON,
    HBAR,
    K_BOLTZMANN,
)

TOL = 1e-12

# Lab-to-astronomical grid (SI)
SOURCE_MASSES = [1.0, 5.972e24, 1.989e30]        # 1 kg, Earth, Sun
TEST_MASSES = [1e-3, 1.0, 1e3]                   # gram to tonne
RADII = [0.1, 1.0, 6.371e6, 1.496e11, 1e16]      # 10 cm to ~0.3 pc


class TestC1BothRoutesEqualNewton:
    def test_unruh_route_matches_newton_on_grid(self):
        eg = EntropicGravity()
        for M in SOURCE_MASSES:
            for m in TEST_MASSES:
                for r in RADII:
                    F = eg.force_unruh_route(M, m, r)
                    F_N = eg.newton_force(M, m, r)
                    assert abs(F / F_N - 1.0) < TOL, (M, m, r)

    def test_equipartition_route_matches_newton_on_grid(self):
        eg = EntropicGravity()
        for M in SOURCE_MASSES:
            for m in TEST_MASSES:
                for r in RADII:
                    F = eg.force_equipartition_route(M, m, r)
                    F_N = eg.newton_force(M, m, r)
                    assert abs(F / F_N - 1.0) < TOL, (M, m, r)

    def test_routes_agree_with_each_other(self):
        eg = EntropicGravity()
        for M in SOURCE_MASSES:
            for m in TEST_MASSES:
                for r in RADII:
                    F1 = eg.force_unruh_route(M, m, r)
                    F2 = eg.force_equipartition_route(M, m, r)
                    assert abs(F1 / F2 - 1.0) < TOL, (M, m, r)

    def test_entropic_force_wrapper_is_newton(self):
        eg = EntropicGravity()
        F = eg.entropic_force(5.972e24, 6.371e6, test_mass=1.0)
        # Surface gravity of Earth on 1 kg: ~9.82 N
        expected = G_NEWTON * 5.972e24 / 6.371e6 ** 2
        assert abs(F / expected - 1.0) < TOL

    def test_building_blocks_have_expected_values(self):
        eg = EntropicGravity()
        # dS/dx for m = 1 kg: 2π k_B c / ħ
        dS_dx = eg.displacement_entropy_gradient(1.0)
        expected = 2 * np.pi * K_BOLTZMANN * C_LIGHT / HBAR
        assert abs(dS_dx / expected - 1.0) < TOL
        # Unruh T at a = 9.81 m/s²: ħa/(2πck_B) ≈ 4e-20 K
        T = eg.unruh_temperature(9.81)
        expected_T = HBAR * 9.81 / (2 * np.pi * C_LIGHT * K_BOLTZMANN)
        assert abs(T / expected_T - 1.0) < TOL
        assert T < 1e-19  # Unruh temperatures at lab accelerations are tiny


class TestC2LegacyRouteNegativeControl:
    def test_legacy_route_does_not_reproduce_newton(self):
        eg = EntropicGravity()
        result = eg.screen_area_route_wrong(mass=1.0, test_mass=1.0)
        assert result["reproduces_newton"] is False
        assert result["ratio_varies_with_r"] is True

    def test_legacy_ratio_scales_linearly_with_r(self):
        # F_wrong/F_newton = c² r/(G m): spread across the radius grid must
        # match the grid's dynamic range (10^-2..10^12 m → spread 10^14).
        eg = EntropicGravity()
        result = eg.screen_area_route_wrong(mass=1.0, test_mass=1.0)
        assert result["linear_scaling_error"] < 1e-9
        expected_spread = eg.x[-1] / eg.x[0]
        assert abs(result["ratio_spread"] / expected_spread - 1.0) < 1e-9

    def test_legacy_route_has_no_test_mass_in_force(self):
        # The defect: F_wrong = Mc²/r is independent of the test mass, so
        # the ratio to Newton must scale as 1/m.
        eg = EntropicGravity()
        r1 = eg.screen_area_route_wrong(mass=1.0, test_mass=1.0)
        r2 = eg.screen_area_route_wrong(mass=1.0, test_mass=10.0)
        assert abs(r1["ratio_to_newton_max"] / r2["ratio_to_newton_max"]
                   - 10.0) < 1e-9


class TestC3DimensionalBookkeeping:
    def test_force_dimensions_are_newtons(self):
        eg = EntropicGravity()
        dims = eg.dimensional_check()
        assert dims["force_dimensions_ok"] is True
        assert dims["dim_force_unruh_route"] == (1, 1, -2, 0)  # kg·m·s⁻²
        assert dims["dim_force_equipartition_route"] == (1, 1, -2, 0)

    def test_intermediate_dimensions(self):
        eg = EntropicGravity()
        dims = eg.dimensional_check()
        assert dims["dim_T_unruh_is_kelvin"] is True
        assert dims["dim_T_equip_is_kelvin"] is True
        assert dims["dim_N_dimensionless"] is True
        assert dims["dim_dS_dx_ok"] is True
        # dS/dx = entropy/length = kg·m·s⁻²·K⁻¹
        assert dims["dim_dS_dx"] == (1, 1, -2, -1)

    def test_combine_dimensions_helper(self):
        # G·M/r² must come out as acceleration
        dim_a = combine_dimensions(("G", 1), ("mass", 1), ("length", -2))
        assert dim_a == DIMENSIONS["acceleration"]
        # k_B·T must come out as energy
        dim_E = combine_dimensions(("k_B", 1), ("temperature", 1))
        assert dim_E == DIMENSIONS["energy"]


class TestC4RecoverNewton:
    REQUIRED_KEYS = [
        "test_mass", "radii_range", "newton_correlation",
        "avg_ratio_entropic_newton", "newton_recovered",
        "derivation", "insight",
    ]

    def test_return_keys_preserved(self):
        eg = EntropicGravity()
        result = eg.recover_newton(mass=1.0)
        for key in self.REQUIRED_KEYS:
            assert key in result, key

    def test_newton_genuinely_recovered(self):
        eg = EntropicGravity()
        result = eg.recover_newton(mass=1.0)
        assert result["newton_recovered"] is True
        assert result["max_rel_deviation_unruh_route"] < TOL
        assert result["max_rel_deviation_equipartition_route"] < TOL
        assert result["routes_agree"] is True
        assert abs(result["avg_ratio_entropic_newton"] - 1.0) < TOL
        assert result["newton_correlation"] > 0.999999

    def test_recovery_holds_for_astronomical_source(self):
        eg = EntropicGravity()
        result = eg.recover_newton(mass=1.989e30, test_mass=5.972e24)
        assert result["newton_recovered"] is True
        assert abs(result["avg_ratio_entropic_newton"] - 1.0) < TOL

    def test_negative_control_wrong_gradient_flips_verdict(self):
        # Mechanical check A: the verdict must be able to come out
        # differently. Breaking the entropy gradient by a factor of 3
        # must flip newton_recovered to False (not hardcoded).
        eg = EntropicGravity()
        eg.displacement_entropy_gradient = (
            lambda m: 3.0 * 2 * np.pi * eg.k_B * m * eg.c / eg.hbar)
        result = eg.recover_newton(mass=1.0)
        assert result["newton_recovered"] is False
        assert abs(result["avg_ratio_entropic_newton"] - 3.0) < 1e-9

    def test_negative_control_correlation_alone_would_lie(self):
        # The legacy criterion (correlation > 0.99) cannot distinguish
        # GMm/r² from 3·GMm/r² — with the broken gradient the correlation
        # stays ~1 but the computed verdict is still False. This is why
        # newton_recovered uses the ratio criterion, not correlation.
        eg = EntropicGravity()
        eg.displacement_entropy_gradient = (
            lambda m: 3.0 * 2 * np.pi * eg.k_B * m * eg.c / eg.hbar)
        result = eg.recover_newton(mass=1.0)
        assert result["newton_correlation"] > 0.999999
        assert result["newton_recovered"] is False

    def test_negative_control_perturbed_screen_dof_breaks_equipartition(self):
        # Doubling the screen degrees of freedom halves the equipartition
        # temperature → that route drops to GMm/(2r²) and the routes
        # disagree: both computed flags must flip.
        eg = EntropicGravity()
        original = eg.screen_dof
        eg.screen_dof = lambda r: 2.0 * original(r)
        result = eg.recover_newton(mass=1.0)
        assert result["routes_agree"] is False
        assert result["newton_recovered"] is False


class TestBlackHoleSI:
    def test_bekenstein_saturation_is_computed(self):
        eg = EntropicGravity()
        result = eg.black_hole_as_maximum_maya(mass=10.0)
        assert result["is_maximum_entropy"] is True
        assert abs(result["bekenstein_saturation_ratio"] - 1.0) < TOL
        assert result["schwarzschild_radius"] > 0

    def test_solar_mass_black_hole_values(self):
        eg = EntropicGravity()
        result = eg.black_hole_as_maximum_maya(mass=1.989e30)
        # r_s(Sun) ≈ 2.95 km; T_H ≈ 6.2e-8 K (standard references)
        assert abs(result["schwarzschild_radius"] - 2953.0) < 5.0
        assert abs(result["hawking_temperature"] / 6.17e-8 - 1.0) < 0.01
