"""Tests for the levels module — three reality levels and engine.

HONESTY NOTE (2026-08-15 test-suite audit)
------------------------------------------
16 of the 22 tests in this file asserted either a doctrinal string literal
(``view["reality"] == "Brahman alone"``, ``dream_substance == "dreamer's own
mind"``) or a boolean that is written as a constant in the module
(``substrate_unchanged``, ``reality_changed``, ``dream_objects_remain``,
``dreamer_remains``, ``physics_valid``, ``is_real``). None of those could fail.

Each has been converted to the *checkable* content of the same claim — the
invariant that would break if the code were wrong — or, where the claim really
is interpretive prose with nothing to compute, renamed ``*_contract`` so it can
never be cited as a result.
"""

import numpy as np
import pytest

from philosophy.levels.paramarthika import Paramarthika
from philosophy.levels.vyavaharika import Vyavaharika
from philosophy.levels.pratibhasika import Pratibhasika
from philosophy.levels.reality_engine import RealityEngine
from philosophy.brahman.consciousness import Brahman
from philosophy.maya.gunas import GunaBalance


class TestParamarthika:
    def test_non_dual_flag_tracks_the_field_and_can_be_false(self):
        """`non_dual` and `field_coherence` are computed; prove it by breaking
        the field and watching both flip. (Was: `assert view["non_dual"] == True`
        plus a doctrinal string, neither of which could fail.)"""
        p = Paramarthika()
        view = p.view()
        assert bool(view["non_dual"]) is True
        # Uniform field: coherence = 1 - std/mean = 1 exactly.
        assert abs(view["field_coherence"] - 1.0) < 1e-12

        # Differentiate the field — the same two keys must now report otherwise.
        p.brahman._field = p.brahman._field.copy()
        p.brahman._field[0] *= 3.0
        p.brahman._field /= np.linalg.norm(p.brahman._field)
        broken = p.view()
        assert bool(broken["non_dual"]) is False
        assert broken["field_coherence"] < 1.0

    def test_pure_awareness_is_a_normalized_copy_of_the_field(self):
        p = Paramarthika()
        field = p.pure_awareness()
        np.testing.assert_allclose(field, p.brahman.field)
        assert abs(np.linalg.norm(field) - 1.0) < 1e-12
        # Handing out the live array would let a caller mutate Brahman.
        field[0] = 99.0
        assert abs(np.linalg.norm(p.brahman.field) - 1.0) < 1e-12

    def test_sublate_contract(self):
        """CONTRACT ONLY — sublation returns the lower view verbatim plus prose.

        The one checkable thing is that the lower-level view is passed through
        by identity (not copied, not summarised), which the engine relies on.
        """
        p = Paramarthika()
        lower = {"some": "view"}
        result = p.sublate(lower)
        assert result["sublated"] is lower
        assert "revealed" in result


class TestVyavaharika:
    def test_simulate_reports_its_own_state(self):
        v = Vyavaharika()
        result = v.simulate(steps=1)
        # Reported energy must be the norm^2 of the state actually stored.
        assert abs(result["field_energy"]
                   - float(np.sum(np.abs(v.get_state()) ** 2))) < 1e-12
        assert result["time_step"] == 1
        assert result["guna_state"] == v.gunas.balance.dominant.value
        # The guna weights reported must be the ones the object holds.
        assert result["sattva"] == v.gunas.balance.sattva
        assert result["rajas"] == v.gunas.balance.rajas
        assert result["tamas"] == v.gunas.balance.tamas

    def test_time_step_increments(self):
        v = Vyavaharika()
        v.simulate(steps=3)
        assert v.time_step == 3

    def test_get_state_simulates_lazily(self):
        v = Vyavaharika()
        assert v.time_step == 0
        state = v.get_state()
        assert isinstance(state, np.ndarray)
        assert v.time_step == 1                      # it had to run a step
        assert len(state) == v.brahman.resolution

    def test_physics_laws_contract(self):
        """CONTRACT ONLY — this method returns five prose strings.

        Nothing is computed, so nothing is asserted beyond the key set.
        """
        v = Vyavaharika()
        laws = v.physics_laws()
        assert set(laws) == {"conservation", "causation", "locality",
                             "symmetry", "note"}

    def test_entropy_saturates_the_uniform_field_bound(self):
        v = Vyavaharika()
        result = v.simulate()
        n = v.brahman.resolution
        # Shannon entropy of a distribution over n outcomes is bounded by
        # log2(n), with equality iff uniform. The guna transform rescales the
        # uniform Brahman field without reshaping it, so the bound is saturated.
        assert 0.0 <= result["field_entropy"] <= np.log2(n) + 1e-9
        assert abs(result["field_entropy"] - np.log2(n)) < 1e-9

    def test_dominant_guna_follows_the_supplied_balance(self):
        # Was: `assert "guna_state" in result` — true for any dict.
        sattvic = Vyavaharika(guna_balance=GunaBalance(0.8, 0.1, 0.1)).simulate()
        assert sattvic["guna_state"] == "sattva_dominant"
        Brahman.reset()
        tamasic = Vyavaharika(guna_balance=GunaBalance(0.1, 0.1, 0.8)).simulate()
        assert tamasic["guna_state"] == "tamas_dominant"

    def test_count_entities_small_field(self):
        assert Vyavaharika._count_entities(np.array([1, 2])) == 0
        assert Vyavaharika._count_entities(np.array([1, 3, 1])) == 1
        # A wrong peak-finder would miscount these too.
        assert Vyavaharika._count_entities(np.array([1, 3, 1, 4, 1])) == 2
        assert Vyavaharika._count_entities(np.array([1, 1, 1, 1])) == 0


class TestPratibhasika:
    def test_dream_is_built_from_the_dreamer_s_own_field(self):
        """Replaces `assert result["dream_substance"] == "dreamer's own mind"`.

        The checkable content of "the dream is made of the dreamer's mind" is
        that every frame lives in the dreamer's own space and stays on the unit
        sphere — the walk never leaves the state space it started in.
        """
        p = Pratibhasika()
        mind = np.ones(64) / np.sqrt(64)
        result = p.generate_dream(dreamer_mind=mind, duration=10)
        assert result["num_frames"] == 10 == result["duration"]
        assert len(p._dream_state) == 10
        for frame in p._dream_state:
            assert frame.shape == mind.shape
            assert abs(np.linalg.norm(frame) - 1.0) < 1e-12
        # It is a walk, not a copy: successive frames differ.
        assert not np.allclose(p._dream_state[0], p._dream_state[-1])

    def test_dream_stores_state(self):
        p = Pratibhasika()
        p.generate_dream(duration=5)
        assert p._dream_state is not None
        assert len(p._dream_state) == 5

    def test_mirage_leaves_the_substrate_untouched(self):
        """Replaces `assert result["substrate_unchanged"] is True` (a literal).

        The claim "the desert is real, the water is projected" is checkable as:
        the input array is not mutated by the call.
        """
        p = Pratibhasika()
        field = np.random.RandomState(0).randn(100)
        before = field.copy()
        result = p.mirage(field)
        np.testing.assert_array_equal(field, before)
        assert result["actual"].startswith("desert")

    def test_rope_snake_interpretation_follows_illumination(self):
        p = Pratibhasika()
        rope = np.ones(50)
        before = rope.copy()
        # All three branches of the threshold logic, including the boundaries.
        assert "snake" in p.rope_snake(rope, darkness_level=0.9)["perceived_as"]
        assert "snake" in p.rope_snake(rope, darkness_level=0.71)["perceived_as"]
        assert "ambiguous" in p.rope_snake(rope, darkness_level=0.7)["perceived_as"]
        assert "ambiguous" in p.rope_snake(rope, darkness_level=0.31)["perceived_as"]
        assert "rope" in p.rope_snake(rope, darkness_level=0.3)["perceived_as"]
        assert "rope" in p.rope_snake(rope, darkness_level=0.1)["perceived_as"]
        # "reality_changed: False" is a source literal; what is checkable is
        # that the rope array itself survives every perception unchanged.
        np.testing.assert_array_equal(rope, before)

    def test_wake_up_clears_the_dream_and_is_idempotent(self):
        """Replaces assertions on `dream_objects_remain` / `dreamer_remains`,
        both source literals. The checkable content: the dream state is gone,
        waking again is harmless, and the dreamer can still dream."""
        p = Pratibhasika()
        p.generate_dream(duration=5)
        p.wake_up()
        assert p._dream_state is None
        p.wake_up()                       # idempotent — no dream to clear
        assert p._dream_state is None
        again = p.generate_dream(duration=3)
        assert again["num_frames"] == 3   # the dreamer survived the waking


class TestRealityEngine:
    def test_observe_waking_routes_to_vyavaharika(self):
        engine = RealityEngine()
        result = engine.observe("waking")
        assert result["level"] == "Vyavaharika"
        # The view must be a real Vyavaharika step, not a canned dict.
        assert result["view"]["time_step"] == 1
        assert result["view"]["field_energy"] > 0

    def test_observe_liberated_returns_the_actual_brahman_field(self):
        engine = RealityEngine()
        result = engine.observe("liberated")
        assert result["level"] == "Paramarthika"
        np.testing.assert_allclose(result["field"], engine.brahman.field)
        assert abs(np.linalg.norm(result["field"]) - 1.0) < 1e-12

    def test_observe_dreaming_routes_to_pratibhasika(self):
        engine = RealityEngine()
        result = engine.observe("dreaming")
        assert result["level"] == "Pratibhasika"
        # A real dream was generated and retained (default duration 50).
        assert result["view"]["num_frames"] == 50
        assert len(engine.pratibhasika._dream_state) == 50

    def test_observe_invalid_raises(self):
        engine = RealityEngine()
        with pytest.raises(ValueError):
            engine.observe("invalid_state")

    def test_sublation_chain_is_actually_wired_together(self):
        """The three steps must reference each other's real outputs.

        Step 3 sublates the SAME empirical dict that step 2 produced — checked
        by identity, which a hand-written summary dict would fail.
        """
        engine = RealityEngine()
        result = engine.demonstrate_sublation()
        empirical = result["step_2_waking"]["empirical_view"]
        assert result["step_3_liberation"]["empirical_sublated"]["sublated"] is empirical
        assert empirical["time_step"] >= 1
        assert result["step_1_dreaming"]["experience"]["num_frames"] == 50
        # Waking really cleared the dream state.
        assert engine.pratibhasika._dream_state is None

    def test_compare_levels_contract(self):
        """CONTRACT ONLY — a 3x4 table of prose. Nothing here is computed."""
        engine = RealityEngine()
        result = engine.compare_levels()
        assert set(result) == {"paramarthika", "vyavaharika", "pratibhasika"}
        for level in result.values():
            assert set(level) == {"ontology", "epistemology", "sublated_by", "analogy"}
