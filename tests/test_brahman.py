"""Tests for the brahman module — consciousness field and Sat-Chit-Ananda.

HONESTY NOTE (2026-08-15 test-suite audit)
------------------------------------------
The SatChitAnanda tests asserted each function against its own definition
(``sat() == np.abs(field)``, ``chit() == np.angle(field)``,
``ananda() == coherence()``). Restating an implementation cannot detect a wrong
implementation. They now check closed-form values for the known uniform field
and the transformation properties a wrong decomposition would violate, and the
``is_unified`` flag is exercised with a control that makes it False.
"""

import numpy as np
import pytest

from philosophy.brahman.consciousness import Brahman
from philosophy.brahman.sat_chit_ananda import SatChitAnanda


class TestBrahmanSingleton:
    def test_singleton_returns_same_instance(self):
        a = Brahman(64)
        b = Brahman(64)
        assert a is b

    def test_reset_clears_singleton(self):
        a = Brahman(64)
        Brahman.reset()
        b = Brahman(32)
        assert a is not b
        assert b.resolution == 32

    def test_equality_always_true_for_brahman(self):
        a = Brahman(64)
        Brahman.reset()
        b = Brahman(32)
        assert a == b

    def test_equality_not_implemented_for_other(self):
        b = Brahman(64)
        assert b.__eq__("not brahman") is NotImplemented


class TestBrahmanField:
    def test_field_is_normalized(self, brahman):
        assert abs(np.linalg.norm(brahman.field) - 1.0) < 1e-10

    def test_field_returns_copy(self, brahman):
        f1 = brahman.field
        f2 = brahman.field
        assert f1 is not f2
        np.testing.assert_array_equal(f1, f2)

    def test_field_has_correct_resolution(self, brahman):
        assert len(brahman.field) == 64

    def test_field_is_complex(self, brahman):
        assert brahman.field.dtype == np.complex128

    def test_field_is_uniform(self, brahman):
        magnitudes = np.abs(brahman.field)
        assert np.std(magnitudes) < 1e-10


class TestBrahmanProperties:
    def test_is_non_dual_initially(self, brahman):
        assert brahman.is_non_dual() == True

    def test_coherence_is_one_for_uniform_field(self, brahman):
        assert abs(brahman.coherence() - 1.0) < 1e-10

    def test_awareness_returns_self(self, brahman):
        assert brahman.awareness() is brahman

    def test_resolution_property(self, brahman):
        assert brahman.resolution == 64

    def test_repr_contains_key_info(self, brahman):
        r = repr(brahman)
        assert "Brahman" in r
        assert "coherence" in r
        assert "non_dual" in r


class TestSatChitAnanda:
    def test_sat_is_the_closed_form_amplitude_and_is_phase_invariant(self, brahman):
        """The uniform normalized field of resolution n has |psi_k| = 1/sqrt(n)
        for every k, and amplitudes must be unchanged by a global phase."""
        sca = SatChitAnanda(brahman)
        sat = sca.sat()
        n = brahman.resolution
        np.testing.assert_allclose(sat, 1.0 / np.sqrt(n), atol=1e-12)
        assert abs(float(np.sum(sat ** 2)) - 1.0) < 1e-12   # Born normalization

        # Rotating the whole field by e^{i theta} must leave Sat untouched.
        # (Brahman is a singleton, so this mutates the one instance in place;
        # the autouse `reset_brahman` fixture restores it after the test.)
        brahman._field = brahman.field * np.exp(1j * 0.7)
        np.testing.assert_allclose(SatChitAnanda(brahman).sat(), sat, atol=1e-12)

    def test_chit_is_a_phase_and_shifts_with_a_global_rotation(self, brahman):
        """A wrong "phase" extractor (e.g. returning the real part) would pass a
        definitional test but fail both properties checked here."""
        sca = SatChitAnanda(brahman)
        chit = sca.chit()
        assert np.all(chit >= -np.pi - 1e-12) and np.all(chit <= np.pi + 1e-12)
        # The reference field is real and positive, so every phase is 0.
        np.testing.assert_allclose(chit, 0.0, atol=1e-12)

        theta = 0.7
        brahman._field = brahman.field * np.exp(1j * theta)   # singleton, reset by fixture
        np.testing.assert_allclose(SatChitAnanda(brahman).chit(), chit + theta,
                                   atol=1e-12)

    def test_ananda_is_one_for_a_unified_field_and_falls_when_it_is_not(self, brahman):
        sca = SatChitAnanda(brahman)
        # Uniform magnitudes: coherence = 1 - std/mean = 1 exactly.
        assert abs(sca.ananda() - 1.0) < 1e-12

        # Control: differentiate the field and Ananda must drop below 1.
        f = brahman.field
        f[0] *= 4.0
        brahman._field = f / np.linalg.norm(f)   # singleton, reset by fixture
        assert SatChitAnanda(brahman).ananda() < 1.0

    def test_unity_check_reconstruction(self, brahman):
        sca = SatChitAnanda(brahman)
        result = sca.unity_check()
        # Independent reconstruction: |psi| * exp(i arg psi) must return psi.
        rebuilt = sca.sat() * np.exp(1j * sca.chit())
        np.testing.assert_allclose(rebuilt, brahman.field, atol=1e-12)
        assert result["reconstruction_error"] < 1e-10
        assert result["is_unified"] == True
        assert abs(result["sat_mean"] - 1.0 / np.sqrt(brahman.resolution)) < 1e-12
        assert result["chit_range"] == (pytest.approx(0.0), pytest.approx(0.0))
        assert abs(result["ananda"] - 1.0) < 1e-12

    def test_unity_check_fails_when_the_aspects_disagree(self, brahman):
        """`is_unified` must be a computed comparison, not a constant: a broken
        Sat aspect has to make it False."""
        class BrokenSat(SatChitAnanda):
            def sat(self):
                return np.abs(self._field) + 0.5

        result = BrokenSat(brahman).unity_check()
        assert result["reconstruction_error"] > 0.1
        assert result["is_unified"] == False

    def test_repr_format(self, brahman):
        sca = SatChitAnanda(brahman)
        r = repr(sca)
        assert "SatChitAnanda" in r
        assert "unified" in r
