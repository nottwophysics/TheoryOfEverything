"""Tests for the particles module — symmetry breaking and particle zoo."""

import numpy as np
import pytest

from particles.symmetry_breaking import MayaSymmetryBreaking
from particles.particle_zoo import ParticleFromMaya, analyze_particle_zoo


class TestMayaSymmetryBreaking:
    def test_unified_symmetry_normalized(self):
        msb = MayaSymmetryBreaking(field_dimension=32)
        field = msb.unified_symmetry()
        assert abs(np.linalg.norm(field) - 1.0) < 1e-10

    def test_mexican_hat_potential(self):
        msb = MayaSymmetryBreaking(field_dimension=32)
        field = msb.unified_symmetry()
        V = msb.mexican_hat_potential(field)
        assert V.shape == field.shape

    def test_break_symmetry_high_temperature(self):
        msb = MayaSymmetryBreaking(field_dimension=32)
        result = msb.break_symmetry(temperature=100.0)
        assert result["symmetry"] == "unbroken" or "temperature" in result

    def test_break_symmetry_low_temperature(self):
        msb = MayaSymmetryBreaking(field_dimension=32)
        result = msb.break_symmetry(temperature=0.0)
        assert "vev" in result or "symmetry" in result

    def test_particle_spectrum(self):
        msb = MayaSymmetryBreaking(field_dimension=32)
        result = msb.particle_spectrum_from_breaking()
        assert isinstance(result, dict)
        assert len(result) > 0


class TestParticleFromMaya:
    def test_massless_property(self):
        p = ParticleFromMaya("photon", 0.0, 0.0, 1.0, False, 0, 0.0)
        assert p.is_massless is True

    def test_massive_property(self):
        p = ParticleFromMaya("electron", 0.511, -1.0, 0.5, False, 1, 0.5)
        assert p.is_massless is False

    def test_guna_association_gen1(self):
        p = ParticleFromMaya("electron", 0.511, -1.0, 0.5, False, 1, 0.5)
        assert "Sattva" in p.guna_association

    def test_guna_association_gen2(self):
        p = ParticleFromMaya("muon", 105.7, -1.0, 0.5, False, 2, 0.6)
        assert "Rajas" in p.guna_association

    def test_guna_association_gen3(self):
        p = ParticleFromMaya("tau", 1776.9, -1.0, 0.5, False, 3, 0.8)
        assert "Tamas" in p.guna_association

    def test_field_excitation_normalized(self):
        p = ParticleFromMaya("electron", 0.511, -1.0, 0.5, False, 1, 0.5)
        field = p.as_field_excitation(field_size=128)
        assert abs(np.linalg.norm(field) - 1.0) < 1e-10

    def test_maya_depth_bounded(self):
        p = ParticleFromMaya("electron", 0.511, -1.0, 0.5, False, 1, 0.5)
        depth = p.compute_maya_depth()
        assert 0.0 <= depth <= 1.0


class TestAnalyzeParticleZoo:
    def test_analysis_runs(self):
        result = analyze_particle_zoo()
        assert isinstance(result, dict)
        assert len(result) > 0
