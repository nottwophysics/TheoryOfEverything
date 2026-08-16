"""Tests for the particles module — symmetry breaking and particle zoo.

HONESTY NOTE (2026-08-15 test-suite audit)
------------------------------------------
Two assertions were disjunctions whose second branch is always true
(``result["symmetry"] == "unbroken" or "temperature" in result`` and
``"vev" in result or "symmetry" in result``). Both keys are always present, so
the tests passed no matter what the physics did — and the first branch was in
fact WRONG (the module reports ``"intact"``, never ``"unbroken"``), which the
always-true second branch hid. They now check the mexican-hat closed forms.
"""

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
        # Closed form for the module's mu^2 = -1, lambda = 0.5 potential:
        # T_c = sqrt(-mu^2/lambda) = sqrt(2).
        assert abs(result["critical_temperature"] - np.sqrt(2.0)) < 1e-12
        assert result["temperature"] > result["critical_temperature"]
        # Above T_c the symmetry is restored: no VEV, no Higgs mass, no
        # Goldstone modes.
        assert result["symmetry"] == "intact"
        assert result["vev"] == 0.0
        assert result["higgs_mass"] == 0.0
        assert result["num_goldstone_bosons"] == 0

    def test_break_symmetry_low_temperature(self):
        msb = MayaSymmetryBreaking(field_dimension=32)
        result = msb.break_symmetry(temperature=0.0)
        assert result["temperature"] < result["critical_temperature"]
        assert result["symmetry"] == "broken"
        # v = sqrt(-mu^2 / 2 lambda) = 1, m_higgs = sqrt(-2 mu^2) = sqrt(2).
        assert abs(result["vev"] - 1.0) < 1e-12
        assert abs(result["higgs_mass"] - np.sqrt(2.0)) < 1e-12
        # Goldstone's theorem for a broken continuous symmetry on this toy:
        # one massive radial mode, dim-1 massless tangential modes.
        assert result["num_goldstone_bosons"] == 32 - 1

    def test_particle_spectrum_carries_standard_model_masses(self):
        msb = MayaSymmetryBreaking(field_dimension=32)
        result = msb.particle_spectrum_from_breaking()
        # The spectrum must be built on a genuinely broken vacuum...
        assert result["symmetry_breaking"]["symmetry"] == "broken"
        spec = result["particle_spectrum"]
        # ...and quote PDG masses (MeV/GeV as labelled in the module) to ~1%.
        assert spec["gauge_bosons"]["photon"]["mass"] == 0
        assert spec["gauge_bosons"]["gluon"]["mass"] == 0
        assert abs(spec["gauge_bosons"]["W_boson"]["mass"] - 80.4) < 1.0
        assert abs(spec["gauge_bosons"]["Z_boson"]["mass"] - 91.19) < 1.0
        assert abs(spec["higgs"]["mass"] - 125.25) < 1.5
        # The mass hierarchy across the three generations must be strict.
        f = spec["fermions"]
        assert f["electron"]["mass"] < f["muon"]["mass"] < f["tau"]["mass"]
        assert [f[k]["generation"] for k in ("electron", "muon", "tau")] == [1, 2, 3]


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
    def test_zoo_orders_particles_by_mass_and_maya_depth(self):
        """Was `assert isinstance(result, dict)` — a literal stub dict passed it.

        The analysis has real orderings in it, so check those: the mass
        hierarchy must be ascending, the "closest to Brahman" list must be the
        shallowest maya depths, and the generation averages must increase.
        """
        result = analyze_particle_zoo()
        assert result["total_particles"] > 10

        masses = [m for _, m in result["mass_hierarchy"]]
        assert masses == sorted(masses)
        # Neutrinos and the photon are the light end; the photon is massless.
        assert result["closest_to_brahman"][0][0] == "photon"
        assert result["closest_to_brahman"][0][1] == 0.0

        shallow = [d for _, d in result["closest_to_brahman"]]
        deep = [d for _, d in result["deepest_in_maya"]]
        assert shallow == sorted(shallow)
        assert deep == sorted(deep)
        assert max(shallow) < min(deep)
        assert all(0.0 <= d <= 1.0 for d in shallow + deep)

        # Generation averages must climb monotonically (the mass hierarchy the
        # module maps onto the three gunas).
        gen = result["generation_avg_mass"]
        assert gen[1] < gen[2] < gen[3]
