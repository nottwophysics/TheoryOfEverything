"""Tests for the levels module — three reality levels and engine."""

import numpy as np
import pytest

from philosophy.levels.paramarthika import Paramarthika
from philosophy.levels.vyavaharika import Vyavaharika
from philosophy.levels.pratibhasika import Pratibhasika
from philosophy.levels.reality_engine import RealityEngine
from philosophy.brahman.consciousness import Brahman
from philosophy.maya.gunas import GunaBalance


class TestParamarthika:
    def test_view_is_non_dual(self):
        p = Paramarthika()
        view = p.view()
        assert view["non_dual"] == True
        assert view["reality"] == "Brahman alone"

    def test_pure_awareness_is_brahman_field(self):
        p = Paramarthika()
        field = p.pure_awareness()
        np.testing.assert_allclose(field, p.brahman.field)

    def test_sublate_structure(self):
        p = Paramarthika()
        lower = {"some": "view"}
        result = p.sublate(lower)
        assert "sublated" in result
        assert "revealed" in result
        assert result["sublated"] is lower


class TestVyavaharika:
    def test_simulate_returns_expected_keys(self):
        v = Vyavaharika()
        result = v.simulate(steps=1)
        assert "time_step" in result
        assert "guna_state" in result
        assert "field_energy" in result
        assert "field_entropy" in result

    def test_time_step_increments(self):
        v = Vyavaharika()
        v.simulate(steps=3)
        assert v.time_step == 3

    def test_get_state_returns_array(self):
        v = Vyavaharika()
        state = v.get_state()
        assert isinstance(state, np.ndarray)

    def test_physics_laws_has_keys(self):
        v = Vyavaharika()
        laws = v.physics_laws()
        assert "conservation" in laws
        assert "causation" in laws
        assert "locality" in laws

    def test_entropy_non_negative(self):
        v = Vyavaharika()
        result = v.simulate()
        assert result["field_entropy"] >= 0

    def test_custom_guna_balance(self):
        v = Vyavaharika(guna_balance=GunaBalance(0.8, 0.1, 0.1))
        result = v.simulate()
        assert "guna_state" in result

    def test_count_entities_small_field(self):
        assert Vyavaharika._count_entities(np.array([1, 2])) == 0
        assert Vyavaharika._count_entities(np.array([1, 3, 1])) == 1


class TestPratibhasika:
    def test_generate_dream_structure(self):
        p = Pratibhasika()
        result = p.generate_dream(duration=10)
        assert result["num_frames"] == 10
        assert result["dream_substance"] == "dreamer's own mind"

    def test_dream_stores_state(self):
        p = Pratibhasika()
        p.generate_dream(duration=5)
        assert p._dream_state is not None
        assert len(p._dream_state) == 5

    def test_mirage_structure(self):
        p = Pratibhasika()
        field = np.random.randn(100)
        result = p.mirage(field)
        assert result["substrate_unchanged"] is True
        assert "actual" in result

    def test_rope_snake_high_darkness(self):
        p = Pratibhasika()
        rope = np.ones(50)
        result = p.rope_snake(rope, darkness_level=0.9)
        assert "snake" in result["perceived_as"]
        assert result["reality_changed"] is False

    def test_rope_snake_low_darkness(self):
        p = Pratibhasika()
        rope = np.ones(50)
        result = p.rope_snake(rope, darkness_level=0.1)
        assert "rope" in result["perceived_as"]

    def test_wake_up_clears_dream(self):
        p = Pratibhasika()
        p.generate_dream(duration=5)
        result = p.wake_up()
        assert p._dream_state is None
        assert result["dream_objects_remain"] is False
        assert result["dreamer_remains"] is True


class TestRealityEngine:
    def test_observe_waking(self):
        engine = RealityEngine()
        result = engine.observe("waking")
        assert result["level"] == "Vyavaharika"
        assert result["physics_valid"] is True

    def test_observe_liberated(self):
        engine = RealityEngine()
        result = engine.observe("liberated")
        assert result["level"] == "Paramarthika"
        assert "field" in result

    def test_observe_dreaming(self):
        engine = RealityEngine()
        result = engine.observe("dreaming")
        assert result["level"] == "Pratibhasika"
        assert result["is_real"] is False

    def test_observe_invalid_raises(self):
        engine = RealityEngine()
        with pytest.raises(ValueError):
            engine.observe("invalid_state")

    def test_sublation_chain(self):
        engine = RealityEngine()
        result = engine.demonstrate_sublation()
        assert "step_1_dreaming" in result
        assert "step_2_waking" in result
        assert "step_3_liberation" in result
        assert "teaching" in result

    def test_compare_levels_has_all_three(self):
        engine = RealityEngine()
        result = engine.compare_levels()
        assert "paramarthika" in result
        assert "vyavaharika" in result
        assert "pratibhasika" in result
        for level in result.values():
            assert "ontology" in level
            assert "epistemology" in level
