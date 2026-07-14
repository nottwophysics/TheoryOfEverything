"""Tests for the liberation module — neti-neti and mahavakyas."""

import numpy as np
import pytest

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

    def test_inquire_process(self):
        nn = NetiNeti(field_size=64)
        result = nn.inquire(verbose=False)
        assert len(result["process"]) == 8
        assert "remainder" in result
        assert "final_teaching" in result

    def test_remainder_near_zero(self):
        nn = NetiNeti(field_size=64)
        result = nn.inquire(verbose=False)
        assert result["remainder"]["is_zero"] is True

    def test_step_by_step_generator(self):
        nn = NetiNeti(field_size=64)
        steps = list(nn.inquire_step_by_step())
        assert len(steps) == 9  # 8 layers + final
        assert steps[-1].get("complete") is True

    def test_reset(self):
        nn = NetiNeti(field_size=64)
        nn.inquire(verbose=False)
        assert len(nn._negated) == 8
        nn.reset()
        assert len(nn._negated) == 0


class TestMahavakya:
    def test_prajnanam_brahma(self):
        m = Mahavakya()
        result = m.prajnanam_brahma()
        assert result["mahavakya"] == "Prajnanam Brahma"
        assert result["demonstration"]["field_is_awareness"] is True

    def test_aham_brahmasmi_high_overlap(self):
        m = Mahavakya()
        result = m.aham_brahmasmi()
        overlap = result["demonstration"]["individual_brahman_overlap"]
        assert overlap > 0.9

    def test_tat_tvam_asi_structure(self):
        m = Mahavakya()
        result = m.tat_tvam_asi()
        demo = result["demonstration"]
        assert "tat" in demo
        assert "tvam" in demo
        assert "asi" in demo
        assert result["mahavakya"] == "Tat Tvam Asi"

    def test_ayam_atma_brahma_four_states(self):
        m = Mahavakya()
        result = m.ayam_atma_brahma()
        states = result["four_states"]
        assert "vaishvanara" in states
        assert "taijasa" in states
        assert "prajna" in states
        assert "turiya" in states

    def test_all_mahavakyas_returns_four(self):
        m = Mahavakya()
        result = m.all_mahavakyas()
        assert "prajnanam_brahma" in result
        assert "aham_brahmasmi" in result
        assert "tat_tvam_asi" in result
        assert "ayam_atma_brahma" in result
        assert "unity" in result
