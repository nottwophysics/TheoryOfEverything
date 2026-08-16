"""Tests for the gravity module — metric, einstein 1D/2D, entropic gravity."""

import numpy as np
import pytest

from gravity.metric import ConsciousnessMetric
from gravity.einstein import EmergentEinstein
from gravity.einstein_2d import EmergentEinstein2D
from gravity.einstein_3d import EmergentEinstein3D
from gravity.entropic import EntropicGravity


class TestConsciousnessMetric:
    def test_entanglement_structure_symmetric(self):
        cm = ConsciousnessMetric(num_points=10)
        C = cm.build_entanglement_structure(maya_depth=0.5)
        np.testing.assert_allclose(C, C.T, atol=1e-10)

    def test_distance_from_entanglement(self):
        cm = ConsciousnessMetric(num_points=10)
        C = cm.build_entanglement_structure(maya_depth=0.5)
        d = cm.entanglement_to_distance(C)
        # Diagonal should be zero (self-distance)
        np.testing.assert_allclose(np.diag(d), 0.0, atol=1e-10)
        # All distances non-negative
        assert np.all(d >= -1e-10)

    def test_derive_metric(self):
        cm = ConsciousnessMetric(num_points=10, dimension=2)
        result = cm.derive_metric(maya_depth=0.5)
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_space_from_entanglement_sweep(self):
        cm = ConsciousnessMetric(num_points=10, dimension=2)
        result = cm.demonstrate_space_from_entanglement()
        assert any(k.startswith("maya_") for k in result), (
            "expected per-maya-depth entries in the sweep result")


class TestEmergentEinstein:
    def test_entropy_non_negative(self):
        ee = EmergentEinstein(grid_size=10)
        region = np.ones(10)
        assert ee.consciousness_entropy(region) >= 0

    def test_temperature_increases_with_acceleration(self):
        ee = EmergentEinstein(grid_size=10)
        t1 = ee.maya_temperature(1.0)
        t2 = ee.maya_temperature(2.0)
        assert t2 > t1

    def test_gravity_from_consciousness(self):
        ee = EmergentEinstein(grid_size=20)
        result = ee.demonstrate_gravity_from_consciousness()
        assert "einstein_equations" in result
        corr = result["einstein_equations"]["correlation_G_T"]
        assert -1.0 <= corr <= 1.0
        # Documented honest state (review 2026-08-15): the toy construction
        # anti-correlates — a positive Einstein-like correlation is NOT achieved.
        assert corr < 0


class TestEmergentEinstein2D:
    def test_geometry_built(self):
        ee2d = EmergentEinstein2D(num_points=20, seed=42)
        assert ee2d.points is not None
        assert ee2d.triangulation is not None

    def test_energy_density(self):
        ee2d = EmergentEinstein2D(num_points=20, seed=42)
        mass_pos = np.array([[0.5, 0.5]])
        mass_val = np.array([1.0])
        T = ee2d.consciousness_energy_density(mass_pos, mass_val)
        assert len(T) == 20
        assert np.all(T >= 0)

    def test_entropy_channel_is_circular_not_an_einstein_test(self):
        """The 2D counterpart of the honest-assertion fix already applied to the
        1D test (2026-08-15). The old assertion was ``test["passes"] == True``,
        where ``passes = abs(correlation) > 0.7`` and the line above it already
        asserted the correlation — the flag added nothing and read as evidence.

        The module's own note says the entropy channel is circular: S is DEFINED
        from T_00 and R_entropy is a local average of S. That circularity is
        what this test now measures, rather than dressing it up as a field
        equation being satisfied.
        """
        ee2d = EmergentEinstein2D(num_points=30, seed=42)
        mass_pos = np.array([[0.5, 0.5]])
        mass_val = np.array([5.0])

        # Demonstrate the circularity directly: the entropy field is very nearly
        # an affine image of the energy density it was built from.
        T = ee2d.consciousness_energy_density(mass_pos, mass_val)
        S = ee2d.entanglement_entropy_field(T)
        assert np.corrcoef(S, T)[0, 1] > 0.9, (
            "if S ever decoupled from T_00 the 'Einstein test' below would "
            "become meaningful — and this assertion is how we would find out")

        result = ee2d.derive_einstein_equations(mass_pos, mass_val)
        test = result["einstein_equation_test"]
        assert test["R_entropy_T_correlation"] > 0
        # The flag must track the threshold it documents — not stand alone.
        assert test["passes"] == (abs(test["R_entropy_T_correlation"])
                                 > test["correlation_threshold"])
        # NEGATIVE CONTROL: with no mass there is nothing to correlate and the
        # same flag must come out False. Without this, `passes == True` could be
        # a constant.
        empty = ee2d.derive_einstein_equations(np.zeros((0, 2)), np.zeros(0))
        assert empty["einstein_equation_test"]["passes"] is False
        # The module must keep saying the entropy channel is not evidence.
        assert "not independent evidence" in result["improvement_over_1d"]

    def test_mass_curves_space(self):
        ee2d = EmergentEinstein2D(num_points=30, seed=42)
        result = ee2d.demonstrate_mass_curves_space()
        assert {"no_mass", "one_mass", "two_masses"} <= set(result)


class TestEmergentEinstein3D:
    def test_geometry_built(self):
        ee3d = EmergentEinstein3D(num_points=30, seed=42)
        assert ee3d.points is not None
        assert ee3d.points.shape == (30, 3)
        assert ee3d.triangulation is not None

    def test_tetra_volumes_positive(self):
        ee3d = EmergentEinstein3D(num_points=30, seed=42)
        assert np.all(ee3d.tetra_volumes >= 0)

    def test_vertex_volumes_positive(self):
        ee3d = EmergentEinstein3D(num_points=30, seed=42)
        assert np.all(ee3d.vertex_volumes >= 0)

    def test_energy_density(self):
        ee3d = EmergentEinstein3D(num_points=30, seed=42)
        mass_pos = [np.array([0.0, 0.0, 0.0])]
        mass_val = [5.0]
        T = ee3d.consciousness_energy_density(mass_pos, mass_val)
        assert len(T) == 30
        assert np.all(T >= 0)

    def test_entropy_channel_is_circular_and_geometry_is_hull_only(self):
        """3D counterpart of the same fix. ``result["dimensions"] == 3`` was a
        source literal compared to itself; the correlation assertion measured a
        quantity the module itself marks WITHDRAWN AS EVIDENCE.

        Two things here are real and are what the test now checks: the entropy
        field is an image of T_00 (the circularity), and the solid-angle deficit
        on a flat point cloud can only live on the convex hull — an invariant a
        broken curvature routine would violate.
        """
        ee3d = EmergentEinstein3D(num_points=50, seed=42)
        source = [np.array([0.0, 0.0, 0.0])]
        T = ee3d.consciousness_energy_density(source, [5.0])
        S = ee3d.entanglement_entropy_field(T)
        assert np.corrcoef(S, T)[0, 1] > 0.9      # S is defined from T_00

        result = ee3d.derive_einstein_equations(source, [5.0])
        test = result["einstein_equation_test"]
        assert "WITHDRAWN AS EVIDENCE" in test["status"]
        assert test["correlation_exceeds_threshold"] == (
            abs(test["R_entropy_T_correlation"]) > test["correlation_threshold"])

        # Flat embedding: every vertex carrying a solid-angle deficit must be a
        # hull vertex, and the off-hull deficit must be numerical zero.
        diag = result["geometric_diagnostic"]
        assert diag["num_vertices_carrying_deficit"] == diag["num_hull_vertices"]
        assert diag["max_abs_R_geometric_off_hull"] <= diag["deficit_tolerance"]
        assert diag["deficit_confined_to_hull"] is True

        # NEGATIVE CONTROL: no mass, no correlation, flag False.
        empty = ee3d.derive_einstein_equations([], [])
        assert empty["einstein_equation_test"]["correlation_exceeds_threshold"] is False

    def test_mass_curves_3d_space(self):
        ee3d = EmergentEinstein3D(num_points=40, seed=42)
        result = ee3d.demonstrate_mass_curves_3d_space()
        assert "single_mass" in result
        assert "binary_system" in result
        assert "mass_shell" in result

    def test_gravitational_wave_signature_is_a_static_difference_field(self):
        """Renamed 2026-08-15. The method computes the difference between two
        STATIC source placements — there is no time coordinate, no wave equation
        and no retarded propagation — and the module says so. Asserting
        ``propagates == True`` invited the opposite reading.
        """
        ee3d = EmergentEinstein3D(num_points=40, seed=42)
        gw = ee3d.gravitational_wave_signature()
        assert "WITHDRAWN AS EVIDENCE" in gw["status"]
        assert gw["wave_amplitude"] > 0
        # The legacy flags must be the computed comparisons they claim to be.
        assert gw["propagates"] == (gw["far_field_amplitude"] > 0)
        assert gw["falls_off_with_distance"] == (
            gw["near_field_amplitude"] > gw["far_field_amplitude"])
        # Honest content: both sources sit near the origin, so the difference
        # field is a Gaussian bump there — larger near than far. That is the
        # profile of the INPUT, not a 1/r radiation law.
        assert gw["near_field_amplitude"] > gw["far_field_amplitude"]
        assert 0 < gw["points_affected"] <= gw["total_points"]
        assert "NOT about anything moving" in gw["propagates_means"]


class TestEntropicGravity:
    def test_entropy_scales_with_radius(self):
        eg = EntropicGravity()
        s1 = eg.holographic_screen_entropy(1.0, 1.0)
        s2 = eg.holographic_screen_entropy(2.0, 1.0)
        assert s2 > s1

    def test_unruh_temperature(self):
        # SI units since the 2026-08-15 Verlinde reimplementation:
        # T = hbar*a/(2*pi*c*k_B). For a = 1 m/s^2 this is ~4.06e-21 K.
        eg = EntropicGravity()
        T = eg.unruh_temperature(1.0)
        assert T > 0
        expected = eg.hbar * 1.0 / (2 * np.pi * eg.c * eg.k_B)
        assert abs(T / expected - 1.0) < 1e-12
        # Unruh temperature is linear in acceleration.
        assert abs(eg.unruh_temperature(2.0) / T - 2.0) < 1e-12

    def test_entropic_force_positive(self):
        eg = EntropicGravity()
        F = eg.entropic_force(1.0, 1.0)
        assert F > 0

    def test_recover_newton(self):
        # Superseded the old honest-failure test on 2026-08-15: the module now
        # implements Verlinde's actual derivation (displaced-test-mass entropy
        # gradient, not the screen-area gradient), so Newton IS recovered.
        eg = EntropicGravity()
        result = eg.recover_newton(mass=1.0)
        assert result["newton_recovered"] is True
        assert abs(result["newton_correlation"] - 1.0) < 1e-9
        assert abs(result["avg_ratio_entropic_newton"] - 1.0) < 1e-9

    def test_legacy_screen_area_route_still_fails_newton(self):
        # Negative control: the retired route must keep failing, so a
        # regression to it cannot pass unnoticed.
        eg = EntropicGravity()
        wrong = eg.screen_area_route_wrong()
        assert wrong["reproduces_newton"] is False

    def test_black_hole_properties(self):
        eg = EntropicGravity()
        result = eg.black_hole_as_maximum_maya(mass=10.0)
        assert "schwarzschild_radius" in result
        assert result["schwarzschild_radius"] > 0
