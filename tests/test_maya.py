"""Tests for the maya module — superimposition, gunas, nama-rupa."""

import numpy as np
import pytest

from maya.superimposition import Adhyasa, SuperimposedObject
from maya.gunas import Gunas, GunaBalance, GunaState
from maya.nama_rupa import NamaRupa, NamedForm


class TestSuperimposedObject:
    def test_is_never_real(self):
        obj = SuperimposedObject(
            apparent=np.array([1.0, 2.0]),
            actual=np.array([1.0, 1.0]),
            ignorance_level=0.5,
            projection_pattern="test",
        )
        assert obj.is_real is False

    def test_error_magnitude(self):
        actual = np.array([1.0, 0.0])
        apparent = np.array([0.0, 1.0])
        obj = SuperimposedObject(apparent, actual, 0.5, "test")
        assert obj.error_magnitude > 0

    def test_recognize_returns_actual(self):
        actual = np.array([1.0, 2.0, 3.0])
        obj = SuperimposedObject(np.zeros(3), actual, 0.8, "test")
        np.testing.assert_array_equal(obj.recognize(), actual)


class TestAdhyasa:
    def test_default_patterns_exist(self):
        a = Adhyasa()
        assert "snake" in a.memory_patterns
        assert "water" in a.memory_patterns
        assert len(a.memory_patterns) == 5

    def test_ignorance_clipped(self):
        a = Adhyasa()
        substrate = np.ones(256)
        result = a.superimpose(substrate, ignorance_level=1.5)
        assert result.ignorance_level == 1.0

    def test_clear_seeing_no_superimposition(self):
        a = Adhyasa()
        substrate = np.ones(256)
        result = a.superimpose(substrate, ignorance_level=0.1)
        assert result.projection_pattern == "none (clear seeing)"
        np.testing.assert_array_equal(result.apparent, substrate)

    def test_high_ignorance_produces_error(self):
        a = Adhyasa()
        substrate = np.ones(256)
        result = a.superimpose(substrate, ignorance_level=0.9, pattern_name="snake")
        assert result.error_magnitude > 0

    def test_rope_snake_demo_returns_all_levels(self):
        a = Adhyasa()
        results = a.rope_snake_demo()
        assert len(results) == 6
        for key in results:
            assert "error" in results[key]
            assert "is_real" in results[key]

    def test_rope_snake_error_decreases_with_clarity(self):
        a = Adhyasa()
        results = a.rope_snake_demo()
        high_ign = results["ignorance_0.95"]["error"]
        low_ign = results["ignorance_0.05"]["error"]
        assert low_ign < high_ign


class TestGunaBalance:
    def test_normalization(self):
        g = GunaBalance(2.0, 3.0, 5.0)
        assert abs(g.sattva + g.rajas + g.tamas - 1.0) < 1e-10

    def test_dominant_sattvic(self):
        g = GunaBalance(0.7, 0.2, 0.1)
        assert g.dominant == GunaState.SATTVIC

    def test_dominant_rajasic(self):
        g = GunaBalance(0.1, 0.8, 0.1)
        assert g.dominant == GunaState.RAJASIC

    def test_dominant_tamasic(self):
        g = GunaBalance(0.1, 0.1, 0.8)
        assert g.dominant == GunaState.TAMASIC

    def test_balanced_when_no_clear_dominant(self):
        g = GunaBalance(0.34, 0.33, 0.33)
        assert g.dominant == GunaState.BALANCED

    def test_as_array(self):
        g = GunaBalance(1, 1, 1)
        arr = g.as_array()
        assert len(arr) == 3
        np.testing.assert_allclose(arr, [1/3, 1/3, 1/3], atol=1e-10)


class TestGunas:
    def test_default_balance(self):
        g = Gunas()
        assert abs(g.balance.sattva - 1/3) < 1e-10

    def test_evolve_changes_balance(self):
        g = Gunas()
        old = g.balance.as_array().copy()
        g.evolve(dt=0.1)
        new = g.balance.as_array()
        assert not np.allclose(old, new)

    def test_evolve_stays_normalized(self):
        g = Gunas()
        g.evolve(dt=0.5)
        total = g.balance.sattva + g.balance.rajas + g.balance.tamas
        assert abs(total - 1.0) < 1e-10

    def test_history_tracks_evolution(self):
        g = Gunas()
        g.evolve()
        g.evolve()
        assert len(g.history) == 3  # initial + 2 evolves

    def test_simulate_cycle_length(self):
        g = Gunas()
        history = g.simulate_cycle(steps=50)
        assert len(history) == 50
        assert "dominant" in history[0]

    def test_transcend(self):
        g = Gunas()
        assert g.transcend() == GunaState.TRANSCENDED

    def test_apply_to_field_shape(self):
        g = Gunas()
        field = np.ones(100)
        result = g.apply_to_field(field)
        assert result.shape == field.shape


class TestNamaRupa:
    def test_differentiate_count(self):
        nr = NamaRupa()
        field = np.ones(100)
        entities = nr.differentiate(field, num_entities=5)
        assert len(entities) == 5

    def test_entities_are_named_forms(self):
        nr = NamaRupa()
        field = np.ones(100)
        entities = nr.differentiate(field, num_entities=3)
        for e in entities:
            assert isinstance(e, NamedForm)

    def test_named_forms_never_separate(self):
        nr = NamaRupa()
        field = np.ones(100)
        entities = nr.differentiate(field, num_entities=3)
        for e in entities:
            assert e.is_separate is False

    def test_dissolve_returns_source(self):
        nr = NamaRupa()
        field = np.ones(100)
        entities = nr.differentiate(field, num_entities=3)
        np.testing.assert_array_equal(entities[0].dissolve(), field)

    def test_reunify_returns_source(self):
        nr = NamaRupa()
        field = np.ones(100)
        entities = nr.differentiate(field, num_entities=3)
        source = nr.reunify(entities)
        np.testing.assert_array_equal(source, field)

    def test_reunify_empty(self):
        nr = NamaRupa()
        result = nr.reunify([])
        assert len(result) == 0

    def test_custom_names(self):
        nr = NamaRupa()
        field = np.ones(100)
        entities = nr.differentiate(field, num_entities=2, names=["alpha", "beta"])
        assert entities[0].nama == "alpha"
        assert entities[1].nama == "beta"

    def test_show_non_separation(self):
        nr = NamaRupa()
        field = np.ones(100) + np.sin(np.linspace(0, 4 * np.pi, 100))
        entities = nr.differentiate(field, num_entities=3)
        result = nr.show_non_separation(entities)
        for name in result:
            assert result[name]["actually_separate"] is False
            assert result[name]["substance"] == "Brahman"
