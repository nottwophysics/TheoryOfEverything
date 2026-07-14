"""Tests for predictions and falsification modules."""

import numpy as np
import pytest

from predictions.testable import TestablePredictions
from predictions.consciousness_signatures import ConsciousnessSignatures
from falsification.criteria import FalsificationCriteria
from falsification.experiments import CriticalExperiments


class TestTestablePredictions:
    def test_all_predictions(self):
        tp = TestablePredictions()
        result = tp.all_predictions()
        assert isinstance(result, dict)
        assert len(result) >= 5

    def test_prediction_1(self):
        tp = TestablePredictions()
        result = tp.prediction_1_entanglement_gravity()
        assert isinstance(result, dict)

    def test_prediction_2_decoherence(self):
        tp = TestablePredictions()
        result = tp.prediction_2_decoherence_mass_threshold()
        assert isinstance(result, dict)
        # Threshold must be a derived, physically sensible mass, and must be
        # consistent with the per-object table (objects below it can show
        # interference; objects far above it cannot).
        m_thr = result["threshold_mass_kg"]
        assert 1e-18 < m_thr < 1e-6, f"threshold mass unphysical: {m_thr}"
        cases = result["test_cases"]
        assert cases["cat"]["can_show_interference"] is False
        assert cases["electron"]["can_show_interference"] is True

    def test_prediction_3(self):
        tp = TestablePredictions()
        result = tp.prediction_3_vacuum_entanglement_structure()
        assert isinstance(result, dict)

    def test_prediction_4(self):
        tp = TestablePredictions()
        result = tp.prediction_4_consciousness_decoherence_rate()
        assert isinstance(result, dict)

    def test_prediction_5(self):
        tp = TestablePredictions()
        result = tp.prediction_5_holographic_noise()
        assert isinstance(result, dict)
        # RMS displacement must be a physical length, bounded below by the
        # Planck length and above by the interferometer arm length. (Guards the
        # earlier sqrt(l_planck) dimensional bug, which had units of sqrt(m).)
        rms = result["rms_displacement_m"]
        assert result["planck_length"] < rms < result["arm_length_m"], (
            f"holographic RMS displacement not lengthlike: {rms}")
        assert result["noise_asd_m_per_sqrtHz"] > 0


class TestConsciousnessSignatures:
    def test_integrated_information(self):
        cs = ConsciousnessSignatures()
        result = cs.integrated_information()
        assert isinstance(result, dict)

    def test_neural_quantum_correlates(self):
        cs = ConsciousnessSignatures()
        result = cs.neural_quantum_correlates()
        assert isinstance(result, dict)

    def test_cosmological_signatures(self):
        cs = ConsciousnessSignatures()
        result = cs.cosmological_signatures()
        assert isinstance(result, dict)


class TestFalsificationCriteria:
    def test_core_falsifiers(self):
        fc = FalsificationCriteria()
        result = fc.core_falsifiers()
        assert isinstance(result, dict)
        assert len(result) >= 5

    def test_partial_falsifiers(self):
        fc = FalsificationCriteria()
        result = fc.partial_falsifiers()
        assert isinstance(result, dict)

    def test_non_falsifiable(self):
        fc = FalsificationCriteria()
        result = fc.what_cannot_be_falsified()
        assert isinstance(result, dict)

    def test_full_report(self):
        fc = FalsificationCriteria()
        result = fc.full_report()
        assert isinstance(result, dict)


class TestCriticalExperiments:
    def test_all_experiments(self):
        ce = CriticalExperiments()
        result = ce.all_experiments()
        assert isinstance(result, dict)

    def test_experiment_1(self):
        ce = CriticalExperiments()
        result = ce.experiment_1_macroscopic_superposition()
        assert isinstance(result, dict)

    def test_experiment_2(self):
        ce = CriticalExperiments()
        result = ce.experiment_2_entanglement_gravity_coupling()
        assert isinstance(result, dict)
