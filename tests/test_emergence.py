"""Tests for the emergence module — spacetime, causation, observer."""

import numpy as np
import pytest

from emergence.spacetime import ConsciousnessField, EmergentSpacetime
from emergence.causation import Vivartavada, CausalEvent
from emergence.observer import Sakshi, Experience


class TestConsciousnessField:
    def test_initial_state(self):
        cf = ConsciousnessField()
        assert cf.dimensions == 0
        assert len(cf.awareness) == 1

    def test_differentiate_increases_dimensions(self):
        cf = ConsciousnessField(resolution=32)
        cf.differentiate(num_dimensions=3)
        assert cf.dimensions == 3

    def test_differentiate_returns_normalized(self):
        cf = ConsciousnessField(resolution=32)
        field = cf.differentiate(num_dimensions=2)
        assert abs(np.linalg.norm(field) - 1.0) < 1e-10

    def test_collapse_to_unity(self):
        cf = ConsciousnessField(resolution=32)
        cf.differentiate(num_dimensions=3)
        result = cf.collapse_to_unity()
        assert len(result) == 1
        assert cf.dimensions == 0

    def test_history_tracked(self):
        cf = ConsciousnessField(resolution=32)
        cf.differentiate(num_dimensions=3)
        assert len(cf.get_history()) == 3


class TestEmergentSpacetime:
    def test_generate_from_awareness(self):
        es = EmergentSpacetime(num_points=20, dimensions=3)
        field = np.ones(100, dtype=np.complex128) / 10
        result = es.generate_from_awareness(field)
        assert result["num_points"] == 20
        assert result["dimensions"] == 3
        assert result["metric_shape"] == (20, 20)

    def test_metric_diagonal_is_zero(self):
        es = EmergentSpacetime(num_points=20, dimensions=3)
        field = np.ones(100, dtype=np.complex128) / 10
        es.generate_from_awareness(field)
        np.testing.assert_allclose(np.diag(es.metric), 0.0, atol=1e-10)

    def test_metric_is_symmetric(self):
        es = EmergentSpacetime(num_points=20, dimensions=3)
        field = np.ones(100, dtype=np.complex128) / 10
        es.generate_from_awareness(field)
        np.testing.assert_allclose(es.metric, es.metric.T, atol=1e-10)

    def test_curvature_proxy_without_metric(self):
        es = EmergentSpacetime()
        assert es.curvature_proxy() == 0.0

    def test_curvature_proxy_bounded(self):
        es = EmergentSpacetime(num_points=20, dimensions=3)
        field = np.ones(100, dtype=np.complex128) / 10
        es.generate_from_awareness(field)
        c = es.curvature_proxy()
        assert 0.0 <= c <= 1.0


class TestCausalEvent:
    def test_substrate_preserved(self):
        cause = np.array([1.0, 0.0, 0.0])
        effect = np.array([0.9, 0.1, 0.0])
        event = CausalEvent(cause, effect, "apparent", False)
        assert 0.0 <= event.substrate_preserved <= 1.0

    def test_substrate_preserved_identical(self):
        cause = np.array([1.0, 2.0, 3.0])
        event = CausalEvent(cause, cause.copy(), "apparent", False)
        assert abs(event.substrate_preserved - 1.0) < 1e-10


class TestVivartavada:
    def test_apparent_transformation(self):
        v = Vivartavada()
        substrate = np.ones(100) * 0.5
        event = v.apparent_transformation(substrate)
        assert event.transformation_type == "apparent (vivarta)"
        assert event.substrate_changed is False

    def test_causal_chain_tracked(self):
        v = Vivartavada()
        substrate = np.ones(100)
        v.apparent_transformation(substrate)
        v.apparent_transformation(substrate)
        assert len(v.causal_chain) == 2

    def test_gold_ornament_demo(self):
        v = Vivartavada()
        result = v.gold_ornament_demo()
        assert "ring" in result
        assert "necklace" in result
        assert result["ring"]["real_change"] is False
        assert result["ring"]["gold_preserved"] > 0.9

    def test_ocean_wave_demo(self):
        v = Vivartavada()
        result = v.ocean_wave_demo()
        assert result["num_waves"] == 5
        assert result["each_wave_is_ocean"] is True
        for corr in result["ocean_correlation"]:
            assert corr > 0.9


class TestExperience:
    def test_is_always_witnessed(self):
        e = Experience("thought", np.array([1.0]), "thought")
        assert e.is_witnessed is True

    def test_is_never_self(self):
        e = Experience("ego", np.array([1.0]), "ego")
        assert e.is_self is False


class TestSakshi:
    def test_witness_does_not_change(self):
        s = Sakshi()
        e = Experience("pain", np.array([1.0]), "body")
        result = s.witness(e)
        assert result["sakshi_changed"] is False
        assert result["sakshi_affected"] is False

    def test_witness_log(self):
        s = Sakshi()
        s.witness(Experience("thought", np.array([1.0]), "thought"))
        s.witness(Experience("feeling", np.array([2.0]), "emotion"))
        log = s.get_witness_log()
        assert len(log) == 2
        assert log[0]["name"] == "thought"

    def test_state_transition(self):
        s = Sakshi()
        result = s.witness_state_transition("waking", "dreaming")
        assert result["states_changed"] is True
        assert result["witness_changed"] is False

    def test_five_sheaths(self):
        s = Sakshi()
        result = s.demonstrate_five_sheaths()
        assert "Annamaya Kosha" in result
        assert "Anandamaya Kosha" in result
        assert "what_remains" in result

    def test_mirror_analogy(self):
        s = Sakshi()
        result = s.mirror_analogy()
        assert "fire" in result["reflections"]
        assert "death" in result["reflections"]
        assert len(result["reflections"]) == 7
