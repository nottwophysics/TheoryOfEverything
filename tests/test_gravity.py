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

    def test_einstein_equations_correlation(self):
        ee2d = EmergentEinstein2D(num_points=30, seed=42)
        mass_pos = np.array([[0.5, 0.5]])
        mass_val = np.array([5.0])
        result = ee2d.derive_einstein_equations(mass_pos, mass_val)
        test = result["einstein_equation_test"]
        assert test["R_entropy_T_correlation"] > 0
        assert test["passes"] == True

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

    def test_einstein_equations_correlation(self):
        ee3d = EmergentEinstein3D(num_points=50, seed=42)
        result = ee3d.derive_einstein_equations(
            [np.array([0.0, 0.0, 0.0])], [5.0]
        )
        test = result["einstein_equation_test"]
        assert test["R_entropy_T_correlation"] > 0.5
        assert result["dimensions"] == 3

    def test_mass_curves_3d_space(self):
        ee3d = EmergentEinstein3D(num_points=40, seed=42)
        result = ee3d.demonstrate_mass_curves_3d_space()
        assert "single_mass" in result
        assert "binary_system" in result
        assert "mass_shell" in result

    def test_gravitational_wave(self):
        ee3d = EmergentEinstein3D(num_points=40, seed=42)
        gw = ee3d.gravitational_wave_signature()
        assert gw["wave_amplitude"] > 0
        assert gw["propagates"] == True


class TestEntropicGravity:
    def test_entropy_scales_with_radius(self):
        eg = EntropicGravity()
        s1 = eg.holographic_screen_entropy(1.0, 1.0)
        s2 = eg.holographic_screen_entropy(2.0, 1.0)
        assert s2 > s1

    def test_unruh_temperature(self):
        eg = EntropicGravity()
        T = eg.unruh_temperature(1.0)
        assert T > 0
        expected = 1.0 / (2 * np.pi)
        assert abs(T - expected) < 1e-10

    def test_entropic_force_positive(self):
        eg = EntropicGravity()
        F = eg.entropic_force(1.0, 1.0)
        assert F > 0

    def test_recover_newton_honestly_reports_failure(self):
        eg = EntropicGravity()
        result = eg.recover_newton(mass=1.0)
        # The 0.93 correlation is 1/r-vs-1/r^2 shape similarity, NOT Newton
        # recovery; the module itself must keep reporting that honestly.
        assert 0.9 < result["newton_correlation"] < 0.99
        assert result["newton_recovered"] is False

    def test_black_hole_properties(self):
        eg = EntropicGravity()
        result = eg.black_hole_as_maximum_maya(mass=10.0)
        assert "schwarzschild_radius" in result
        assert result["schwarzschild_radius"] > 0
