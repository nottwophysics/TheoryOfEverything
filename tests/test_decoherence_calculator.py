"""Tests for the decoherence-threshold calculator."""
import numpy as np
from predictions.decoherence_calculator import (
    DecoherenceCalculator, sphere_radius, dp_energy_difference,
    tau_diosi_penrose, tau_collisional, tau_thermal_photon, REFERENCES,
)


class TestPhysicsLimits:
    def test_dp_energy_zero_at_zero_separation(self):
        m, R = 1e-14, sphere_radius(1e-14, 2000)
        assert abs(dp_energy_difference(m, R, 1e-18)) < 1e-30

    def test_dp_energy_saturates_at_2R(self):
        # ΔE(2R) should equal (12/5 - 2*(1/2))·Gm²/R = (7/5)·Gm²/R
        m = 1e-14; R = sphere_radius(m, 2000)
        G = 6.67430e-11
        val = dp_energy_difference(m, R, 2 * R)
        assert abs(val - 1.4 * G * m * m / R) / (G * m * m / R) < 1e-9

    def test_dp_time_scale_osmium(self):
        # A 10 pg osmium sphere (1e-14 kg) has τ_DP on the millisecond scale.
        m = 1e-14; R = sphere_radius(m, 22600)
        tau = tau_diosi_penrose(m, R)
        assert 1e-4 < tau < 1e-1

    def test_thermal_photon_matches_joos_zeh_table(self):
        # 10 µm grain at 300 K, Δx = radius: τ ~ 1e-16 s (Joos–Zeh 1985 table).
        a = 1e-5
        tau = tau_thermal_photon(a, 300.0, separation_m=a)
        assert 1e-17 < tau < 1e-14

    def test_collisional_decreases_with_pressure(self):
        R = sphere_radius(1e-14, 2000)
        assert tau_collisional(R, 1e-8) < tau_collisional(R, 1e-12)


class TestChannelComparison:
    def test_room_temperature_is_photon_limited_for_nanosphere(self):
        calc = DecoherenceCalculator(2000)
        r = calc.evaluate(1e-14, 1e-10 * 100, temperature_k=300)
        assert r["limiting_channel"] == "thermal_photon"
        assert not r["gravity_is_dominant"]

    def test_cryogenic_opens_a_DP_window(self):
        calc = DecoherenceCalculator(2000)
        grid = np.logspace(-16, -9, 200)
        warm = calc.discriminating_window(grid, 1e-13 * 100, temperature_k=300)
        cold = calc.discriminating_window(grid, 1e-13 * 100, temperature_k=4.0)
        assert warm["n_testable_masses"] == 0
        assert cold["n_testable_masses"] > 0
        assert cold["mass_max_kg"] is not None

    def test_references_are_dois(self):
        assert all("/" in d for d in REFERENCES.values())
        assert REFERENCES["diosi_1989"] == "10.1103/PhysRevA.40.1165"
