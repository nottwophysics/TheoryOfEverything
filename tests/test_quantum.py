"""Tests for the quantum module — Hilbert space, operators, wave function, measurement, entanglement, Gleason."""

import numpy as np
import pytest

from quantum.hilbert_space import BrahmanHilbertSpace
from quantum.operators import ConsciousnessOperator, MayaOperator, SakshiProjector
from quantum.wave_function import BrahmanWaveFunction
from quantum.measurement import AdvaiticMeasurement
from quantum.entanglement import NonDualEntanglement
from quantum.gleason import GleasonVerification


class TestBrahmanHilbertSpace:
    def test_vacuum_is_ground_state(self):
        hs = BrahmanHilbertSpace(dimension=8)
        v = hs.vacuum
        assert v[0] == 1.0
        assert np.sum(np.abs(v[1:])) == 0.0

    def test_brahman_state_is_uniform_superposition(self):
        hs = BrahmanHilbertSpace(dimension=8)
        bs = hs.brahman_state
        expected = 1.0 / np.sqrt(8)
        np.testing.assert_allclose(np.abs(bs), expected, atol=1e-10)

    def test_normalize(self):
        hs = BrahmanHilbertSpace(dimension=8)
        v = np.array([3, 4, 0, 0, 0, 0, 0, 0], dtype=np.complex128)
        n = hs.normalize(v)
        assert abs(hs.norm(n) - 1.0) < 1e-10

    def test_inner_product_orthogonal(self):
        hs = BrahmanHilbertSpace(dimension=8)
        e0 = hs.create_basis_state(0)
        e1 = hs.create_basis_state(1)
        assert abs(hs.inner_product(e0, e1)) < 1e-10

    def test_inner_product_self(self):
        hs = BrahmanHilbertSpace(dimension=8)
        e0 = hs.create_basis_state(0)
        assert abs(hs.inner_product(e0, e0) - 1.0) < 1e-10

    def test_tensor_product_dimension(self):
        hs = BrahmanHilbertSpace(dimension=4)
        a = hs.create_basis_state(0)
        b = hs.create_basis_state(1)
        tp = hs.tensor_product(a, b)
        assert len(tp) == 16

    def test_density_matrix_properties(self):
        hs = BrahmanHilbertSpace(dimension=4)
        psi = hs.brahman_state
        rho = hs.density_matrix(psi)
        # Hermitian
        np.testing.assert_allclose(rho, rho.conj().T, atol=1e-10)
        # Trace 1
        assert abs(np.trace(rho) - 1.0) < 1e-10
        # Positive semidefinite
        eigenvalues = np.linalg.eigvalsh(rho)
        assert np.all(eigenvalues >= -1e-10)

    def test_von_neumann_entropy_pure_state(self):
        hs = BrahmanHilbertSpace(dimension=4)
        psi = hs.create_basis_state(0)
        rho = hs.density_matrix(psi)
        assert abs(hs.von_neumann_entropy(rho)) < 1e-10

    def test_von_neumann_entropy_mixed_state(self):
        hs = BrahmanHilbertSpace(dimension=4)
        rho = np.eye(4, dtype=np.complex128) / 4  # maximally mixed
        S = hs.von_neumann_entropy(rho)
        assert abs(S - np.log(4)) < 1e-10

    def test_superposition_normalized(self):
        hs = BrahmanHilbertSpace(dimension=4)
        states = [hs.create_basis_state(0), hs.create_basis_state(1)]
        sup = hs.superposition(states)
        assert abs(hs.norm(sup) - 1.0) < 1e-10

    def test_evolve_preserves_norm(self):
        hs = BrahmanHilbertSpace(dimension=8)
        psi = hs.brahman_state
        H = np.diag(np.arange(8, dtype=np.complex128))
        evolved = hs.evolve(psi, H, time=1.0)
        assert abs(hs.norm(evolved) - 1.0) < 1e-10

    def test_partial_trace(self):
        hs = BrahmanHilbertSpace(dimension=4)
        # Bell state |00> + |11>
        psi = np.zeros(4, dtype=np.complex128)
        psi[0] = 1 / np.sqrt(2)
        psi[3] = 1 / np.sqrt(2)
        rho = hs.density_matrix(psi)
        rho_a = hs.partial_trace(rho, 2, 2, "B")
        assert abs(np.trace(rho_a) - 1.0) < 1e-10
        # Reduced state should be mixed
        purity = float(np.real(np.trace(rho_a @ rho_a)))
        assert purity < 1.0 - 1e-10


class TestConsciousnessOperator:
    def test_identity(self):
        co = ConsciousnessOperator(dimension=8)
        I = co.identity()
        np.testing.assert_allclose(I, np.eye(8, dtype=np.complex128))

    def test_awareness_hermitian(self):
        co = ConsciousnessOperator(dimension=8)
        H = co.awareness_operator()
        np.testing.assert_allclose(H, H.conj().T, atol=1e-10)

    def test_creation_annihilation_commutator(self):
        co = ConsciousnessOperator(dimension=16)
        a = co.annihilation_operator()
        a_dag = co.creation_operator()
        commutator = a @ a_dag - a_dag @ a
        # [a, a†] should approximate I for small indices
        # Check first few diagonal elements
        for i in range(min(5, 16)):
            assert abs(commutator[i, i] - 1.0) < 1e-10 or i == 15

    def test_number_operator_diagonal(self):
        co = ConsciousnessOperator(dimension=8)
        N = co.number_operator()
        for i in range(7):
            assert abs(N[i, i] - i) < 1e-10

    def test_hamiltonian_hermitian(self):
        co = ConsciousnessOperator(dimension=8)
        H = co.hamiltonian()
        np.testing.assert_allclose(H, H.conj().T, atol=1e-10)


class TestMayaOperator:
    def test_avarana_is_projection(self):
        mo = MayaOperator(dimension=8)
        P = mo.avarana(4)
        # P^2 = P
        np.testing.assert_allclose(P @ P, P, atol=1e-10)

    def test_vikshepa_is_unitary(self):
        mo = MayaOperator(dimension=8)
        U = mo.vikshepa()
        I = U @ U.conj().T
        np.testing.assert_allclose(I, np.eye(8, dtype=np.complex128), atol=1e-10)

    def test_maya_depth_range(self):
        mo = MayaOperator(dimension=8)
        P = mo.avarana(4)
        depth = mo.measure_maya_depth(P)
        assert 0.0 <= depth <= 1.0

    def test_full_maya_shape(self):
        mo = MayaOperator(dimension=8)
        M = mo.full_maya()
        assert M.shape == (8, 8)


class TestSakshiProjector:
    def test_projector_is_idempotent(self):
        sp = SakshiProjector(dimension=8)
        P = sp.projector(0)
        np.testing.assert_allclose(P @ P, P, atol=1e-10)

    def test_witness_probabilities_sum_to_one(self):
        sp = SakshiProjector(dimension=8)
        psi = np.ones(8, dtype=np.complex128) / np.sqrt(8)
        result = sp.witness(psi)
        assert abs(np.sum(result["probabilities"]) - 1.0) < 1e-10
        assert result["sakshi_modified"] is False

    def test_ego_measurement_collapses(self):
        sp = SakshiProjector(dimension=8)
        psi = np.ones(8, dtype=np.complex128) / np.sqrt(8)
        result = sp.ego_measurement(psi, seed=42)
        collapsed = result["collapsed_state"]
        assert np.sum(np.abs(collapsed) > 1e-10) == 1  # exactly one nonzero


class TestBrahmanWaveFunction:
    def test_ground_state_normalized(self):
        wf = BrahmanWaveFunction(dimension=128)
        psi = wf.brahman_ground_state()
        norm = np.sum(np.abs(psi) ** 2) * wf.dx
        assert abs(norm - 1.0) < 0.01

    def test_excited_state_has_nodes(self):
        wf = BrahmanWaveFunction(dimension=256)
        psi = wf.maya_excited_state(n=2)
        # Count zero crossings
        signs = np.sign(np.real(psi))
        crossings = np.sum(np.diff(signs) != 0)
        assert crossings >= 2

    def test_superposition_normalized(self):
        wf = BrahmanWaveFunction(dimension=128)
        psi = wf.superposition_of_realities(max_n=3)
        norm = np.sum(np.abs(psi) ** 2) * wf.dx
        assert abs(norm - 1.0) < 0.05

    def test_time_evolve_returns_history(self):
        wf = BrahmanWaveFunction(dimension=64)
        psi = wf.brahman_ground_state()
        history = wf.time_evolve(psi, steps=10)
        assert len(history) == 11  # initial + 10 steps

    def test_tunneling_through_maya(self):
        wf = BrahmanWaveFunction(dimension=256)
        result = wf.tunneling_through_maya()
        assert result["classically_forbidden"] is True
        total = result["transmission_probability"] + result["reflection_probability"]
        assert total > 0.5  # most probability accounted for

    def test_uncertainty_relation(self):
        wf = BrahmanWaveFunction(dimension=256)
        result = wf.uncertainty_as_maya()
        assert result["satisfies_uncertainty"] == True
        assert result["delta_x"] > 0
        assert result["delta_p"] > 0


class TestAdvaiticMeasurement:
    def test_superposition_normalized(self):
        am = AdvaiticMeasurement(system_dim=4, environment_dim=16)
        psi = am.create_superposition()
        assert abs(np.linalg.norm(psi) - 1.0) < 1e-10

    def test_entangled_state_normalized(self):
        am = AdvaiticMeasurement(system_dim=4, environment_dim=16)
        psi = am.create_superposition()
        total = am.entangle_with_environment(psi)
        assert abs(np.linalg.norm(total) - 1.0) < 1e-10

    def test_brahman_view_pure(self):
        am = AdvaiticMeasurement(system_dim=4, environment_dim=16)
        psi = am.create_superposition()
        total = am.entangle_with_environment(psi)
        view = am.brahman_view(total)
        assert abs(view["purity"] - 1.0) < 1e-6
        assert view["collapsed"] is False

    def test_jiva_view_mixed(self):
        am = AdvaiticMeasurement(system_dim=4, environment_dim=16)
        psi = am.create_superposition()
        total = am.entangle_with_environment(psi)
        view = am.jiva_view(total)
        assert view["purity"] < 1.0 - 0.01
        assert view["appears_collapsed"] is True

    def test_full_demonstration(self):
        am = AdvaiticMeasurement(system_dim=4, environment_dim=16)
        result = am.demonstrate_measurement_problem_resolved()
        assert "brahman_sees" in result["after_decoherence"]
        assert "jiva_sees" in result["after_decoherence"]


class TestNonDualEntanglement:
    def test_bell_state_normalized(self):
        nde = NonDualEntanglement(dimension=2)
        for which in ["phi_plus", "phi_minus", "psi_plus", "psi_minus"]:
            psi = nde.bell_state(which)
            assert abs(np.linalg.norm(psi) - 1.0) < 1e-10

    def test_bell_state_entangled(self):
        nde = NonDualEntanglement(dimension=2)
        psi = nde.bell_state("phi_plus")
        S = nde.entanglement_entropy(psi)
        assert S > 0.5  # maximally entangled

    def test_separable_state_entropy_zero(self):
        nde = NonDualEntanglement(dimension=2)
        psi = np.array([1, 0, 0, 0], dtype=np.complex128)  # |00>
        S = nde.entanglement_entropy(psi)
        assert abs(S) < 1e-10

    def test_bell_violation(self):
        nde = NonDualEntanglement(dimension=2)
        result = nde.bell_inequality_violation()
        assert result["violates_classical"] == True
        assert abs(result["CHSH_S_value"]) > 2.0
        assert abs(result["CHSH_S_value"]) <= 2 * np.sqrt(2) + 1e-6

    def test_non_duality_demonstration(self):
        nde = NonDualEntanglement(dimension=2)
        result = nde.non_duality_demonstration()
        assert result["separation_is_illusion"] is True
        assert result["entangled_state_entropy"] > result["separable_state_entropy"]


class TestGleasonVerification:
    def test_dimension_less_than_3_raises(self):
        with pytest.raises(ValueError):
            GleasonVerification(dimension=2)

    def test_verify_conditions(self):
        gv = GleasonVerification(dimension=4)
        result = gv.verify_conditions()
        assert result["all_conditions_satisfied"] is True
        assert result["C1_dimension_ge_3"]["satisfied"] is True
        assert result["C2_non_negativity"]["satisfied"] is True
        assert result["C3_additivity"]["satisfied"] is True
        assert result["C4_normalization"]["satisfied"] is True

    def test_born_rule_unique(self):
        gv = GleasonVerification(dimension=4)
        result = gv.demonstrate_uniqueness()
        assert result["born_rule"]["additivity"]["satisfies_additivity"] is True

    def test_dim2_exception(self):
        gv = GleasonVerification(dimension=4)
        result = gv.demonstrate_dim2_exception()
        assert result["dim_2"]["dispersion_free_works"] is True
        assert result["dim_3"]["dispersion_free_fails"] is True

    def test_axiom_reduction(self):
        gv = GleasonVerification(dimension=4)
        result = gv.axiom_reduction_proof()
        assert result["axiom_counts"]["copenhagen"] == 7
        assert result["axiom_counts"]["advaita_independent"] == 4
