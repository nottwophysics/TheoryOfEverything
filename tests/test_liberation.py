"""Tests for the liberation module — neti-neti and mahavakyas.

HONESTY NOTE (2026-08-15 test-suite audit)
------------------------------------------
Four assertions here compared a doctrinal string in the module against the same
string retyped in the test (``result["mahavakya"] == "Prajnanam Brahma"`` and
three siblings), and two more asserted booleans that were true by construction.
They are replaced below by recomputations and by POSITIVE/NEGATIVE control pairs,
so that every flag asserted True is one this suite has also seen come out False.

One honest finding surfaced while doing this and is now pinned: the DEFAULT
``tat_tvam_asi`` demonstration does not clear its own 0.9 identity threshold
(it reaches 0.7865), so ``upadhi_removed`` is False there. The old test never
looked.
"""

import numpy as np
import pytest

from philosophy.brahman.consciousness import Brahman
from philosophy.liberation.neti_neti import NetiNeti, Layer
from philosophy.liberation.mahavakya import Mahavakya


class TestLayer:
    def test_layer_creation(self):
        layer = Layer("test", "desc", np.ones(10), 0.5)
        assert layer.name == "test"
        assert layer.attachment_strength == 0.5


class TestNetiNeti:
    def test_default_layers(self):
        nn = NetiNeti(field_size=64)
        assert len(nn.layers) == 8
        # Every layer must carry a field of the requested size and a bounded
        # attachment weight — a stub list of names would fail this.
        for layer in nn.layers:
            assert layer.content.shape == (64,)
            assert 0.0 < layer.attachment_strength <= 1.0

    def test_inquire_negates_each_layer_in_turn(self):
        nn = NetiNeti(field_size=64)
        total = np.zeros(64)
        for layer in nn.layers:
            total += layer.content
        result = nn.inquire(verbose=False)
        assert len(result["process"]) == 8

        # Independent recomputation of the running remainder: after k negations
        # the remainder is total minus the first k layer fields.
        remainder = total.copy()
        for step, layer in zip(result["process"], nn.layers):
            remainder = remainder - layer.content
            assert abs(step["remainder_energy"] - float(np.sum(remainder ** 2))) < 1e-9
            assert step["attachment_released"] == layer.attachment_strength

    def test_remainder_vanishes_because_the_layers_are_exhaustive(self):
        nn = NetiNeti(field_size=64)
        result = nn.inquire(verbose=False)
        # Subtracting every summand from the sum must leave zero to float
        # precision; `is_zero` is the computed comparison, not a constant.
        assert result["remainder"]["energy"] < 1e-20
        assert result["remainder"]["is_zero"] is True

    def test_step_by_step_generator(self):
        nn = NetiNeti(field_size=64)
        steps = list(nn.inquire_step_by_step())
        assert len(steps) == 9  # 8 layers + final
        assert steps[-1].get("complete") is True
        # The remainder magnitude must fall to ~0 by the last negation.
        assert steps[-2]["remainder_magnitude"] < 1e-9
        assert steps[0]["remainder_magnitude"] > 1.0

    def test_reset(self):
        nn = NetiNeti(field_size=64)
        nn.inquire(verbose=False)
        assert len(nn._negated) == 8
        nn.reset()
        assert len(nn._negated) == 0


class TestMahavakya:
    def test_prajnanam_brahma_awareness_is_the_strange_loop(self):
        """`field_is_awareness` is `awareness() is self.brahman` — a real
        identity check. (Was: an assertion on the Sanskrit title string.)"""
        m = Mahavakya()
        result = m.prajnanam_brahma()
        assert m.brahman.awareness() is m.brahman
        assert result["demonstration"]["field_is_awareness"] is True

    def test_aham_brahmasmi_overlap_has_a_working_negative_control(self):
        m = Mahavakya()
        # Positive: the default individual differs from Brahman only by small
        # random phases, so |<i|b>| stays near 1.
        result = m.aham_brahmasmi()
        overlap = result["demonstration"]["individual_brahman_overlap"]
        assert overlap > 0.9
        assert result["demonstration"]["identity"] is True

        # Negative control: a state orthogonal to the uniform field must give
        # overlap 0 and flip `identity` to False. Without this the flag would be
        # unfalsifiable.
        n = m.brahman.resolution
        orthogonal = np.zeros(n, dtype=np.complex128)
        orthogonal[0] = 1 / np.sqrt(2)
        orthogonal[1] = -1 / np.sqrt(2)
        control = m.aham_brahmasmi(individual_field=orthogonal)
        assert control["demonstration"]["individual_brahman_overlap"] < 1e-12
        assert control["demonstration"]["identity"] is False

    def test_tat_tvam_asi_default_upadhi_removal_does_not_reach_identity(self):
        """HONEST FINDING (2026-08-15): the default Gaussian upadhi leaves the
        magnitude profiles only 0.79 aligned, below the module's own 0.9
        threshold, so `upadhi_removed` is False. The previous test asserted only
        that three dict keys existed and never noticed."""
        m = Mahavakya()
        result = m.tat_tvam_asi()
        demo = result["demonstration"]
        identity = float(demo["asi"].split(": ")[1].rstrip(")"))
        assert 0.75 < identity < 0.9
        assert demo["upadhi_removed"] is False

        # Positive control: a jiva that differs from Brahman only by phase has
        # the same magnitude profile, so the flag CAN be True.
        n = m.brahman.resolution
        phased = m.brahman.field * np.exp(1j * np.linspace(0, 1, n))
        good = m.tat_tvam_asi(jiva_field=phased)
        assert good["demonstration"]["upadhi_removed"] is True

        # Negative control: a jiva localised on one mode is maximally unlike it.
        localized = np.zeros(n, dtype=np.complex128)
        localized[0] = 1.0
        bad = m.tat_tvam_asi(jiva_field=localized)
        assert bad["demonstration"]["upadhi_removed"] is False

    def test_ayam_atma_brahma_state_energies_match_closed_forms(self):
        """The four Mandukya "states" are modulations of the normalized field;
        their energies follow from mean(cos^2) = mean(sin^2) = 1/2."""
        m = Mahavakya()
        result = m.ayam_atma_brahma()
        states = result["four_states"]
        assert set(states) == {"vaishvanara", "taijasa", "prajna", "turiya"}

        # Turiya is Brahman as-is: a unit-norm field, so energy = 1 exactly.
        assert abs(states["turiya"]["field_energy"] - 1.0) < 1e-12
        # Prajna is the uniform field at the mean magnitude: n * (1/sqrt(n))^2 = 1.
        assert abs(states["prajna"]["field_energy"] - 1.0) < 1e-12
        # Waking = |field| * cos(...) over whole periods -> 1/2.
        assert abs(states["vaishvanara"]["field_energy"] - 0.5) < 0.02
        # Dreaming = the same with sin(...) * 0.5 -> 0.25 * 1/2 = 0.125.
        assert abs(states["taijasa"]["field_energy"] - 0.125) < 0.02
        assert (states["turiya"]["field_energy"]
                > states["vaishvanara"]["field_energy"]
                > states["taijasa"]["field_energy"])

    def test_all_mahavakyas_delegates_to_the_four_methods(self):
        """Orchestrator contract: the aggregate must carry the same numbers the
        individual methods produce (a summary literal would not)."""
        m = Mahavakya()
        result = m.all_mahavakyas()
        assert set(result) == {"prajnanam_brahma", "aham_brahmasmi",
                               "tat_tvam_asi", "ayam_atma_brahma", "unity"}
        assert (result["tat_tvam_asi"]["demonstration"]["asi"]
                == m.tat_tvam_asi()["demonstration"]["asi"])
        assert (result["ayam_atma_brahma"]["four_states"]["turiya"]["field_energy"]
                == m.ayam_atma_brahma()["four_states"]["turiya"]["field_energy"])
