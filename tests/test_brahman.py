"""Tests for the brahman module — consciousness field and Sat-Chit-Ananda."""

import numpy as np
import pytest

from brahman.consciousness import Brahman
from brahman.sat_chit_ananda import SatChitAnanda


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
    def test_sat_returns_magnitudes(self, brahman):
        sca = SatChitAnanda(brahman)
        sat = sca.sat()
        np.testing.assert_allclose(sat, np.abs(brahman.field))

    def test_chit_returns_phases(self, brahman):
        sca = SatChitAnanda(brahman)
        chit = sca.chit()
        np.testing.assert_allclose(chit, np.angle(brahman.field))

    def test_ananda_equals_coherence(self, brahman):
        sca = SatChitAnanda(brahman)
        assert abs(sca.ananda() - brahman.coherence()) < 1e-10

    def test_unity_check_reconstruction(self, brahman):
        sca = SatChitAnanda(brahman)
        result = sca.unity_check()
        assert result["is_unified"] == True
        assert result["reconstruction_error"] < 1e-10

    def test_unity_check_keys(self, brahman):
        sca = SatChitAnanda(brahman)
        result = sca.unity_check()
        assert "sat_mean" in result
        assert "chit_range" in result
        assert "ananda" in result

    def test_repr_format(self, brahman):
        sca = SatChitAnanda(brahman)
        r = repr(sca)
        assert "SatChitAnanda" in r
        assert "unified" in r
