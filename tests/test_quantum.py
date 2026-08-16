"""Tests for the quantum module — Hilbert space, operators, wave function, measurement, entanglement, Gleason.

HONESTY NOTE (2026-08-15 test-suite audit)
------------------------------------------
Several assertions here used to read a key whose value is a source literal and
compare it to the same literal restated in the test (``er_equals_epr == True``,
``non_traversable is True``, ``collapsed is False``, ``sakshi_modified is
False``, ``axiom_counts["copenhagen"] == 7``). Those cannot fail for any input
and are not evidence of anything. They have been replaced by recomputations
against closed forms, or — where the value really is editorial bookkeeping —
kept but renamed so the test reads as a contract, not as a result.
"""

import numpy as np
import pytest

from quantum.hilbert_space import BrahmanHilbertSpace
from quantum.operators import ConsciousnessOperator, MayaOperator, SakshiProjector
from quantum.wave_function import BrahmanWaveFunction
from quantum.measurement import AdvaiticMeasurement
from quantum.entanglement import NonDualEntanglement
from quantum.gleason import GleasonVerification
from quantum.er_epr import EREqualsEPR
from quantum.unity_of_experience import UnityOfExperience


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

    def test_witness_does_not_modify_the_state(self):
        # Replaces `assert result["sakshi_modified"] is False` (a source
        # literal). The checkable content of "the witness never changes what it
        # witnesses" is that the input array survives the call untouched, and
        # that what comes back is the Born distribution.
        sp = SakshiProjector(dimension=8)
        psi = np.ones(8, dtype=np.complex128) / np.sqrt(8)
        before = psi.copy()
        result = sp.witness(psi)
        np.testing.assert_array_equal(psi, before)
        np.testing.assert_allclose(result["probabilities"], np.abs(before) ** 2, atol=1e-12)
        assert abs(np.sum(result["probabilities"]) - 1.0) < 1e-10
        # Uniform superposition over 8 modes: Shannon entropy = ln 8.
        assert abs(result["entropy"] - np.log(8)) < 1e-10
        assert result["num_active_modes"] == 8

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
        # `classically_forbidden` IS computed (k0^2/2 < barrier); check it
        # against the energies the method itself reports.
        assert result["particle_energy"] < result["barrier_height"]
        assert result["classically_forbidden"] is True
        T = result["transmission_probability"]
        R = result["reflection_probability"]
        # CAVEAT (2026-08-15): these two are unnormalised region integrals of
        # |psi|^2 (they sum to ~12.7 here), so despite the key names they are
        # NOT probabilities. Only their ratio is meaningful, so that is what is
        # asserted: sub-barrier tunnelling reflects far more than it transmits.
        assert T > 0 and R > 0
        assert R > T
        assert 0.0 < T / (T + R) < 0.5

    def test_ground_state_saturates_uncertainty_bound(self):
        wf = BrahmanWaveFunction(dimension=256)
        result = wf.uncertainty_as_maya()
        assert result["delta_x"] > 0
        assert result["delta_p"] > 0
        # Consistency: the reported product is the product it says it is.
        assert abs(result["product"] - result["delta_x"] * result["delta_p"]) < 1e-12
        # Physics, independent of the module: a Gaussian ground state is a
        # minimum-uncertainty state, so dx*dp = hbar/2 = 0.5 in natural units.
        # It must sit ON the bound, not merely above it.
        assert result["product"] >= 0.5 - 0.01
        assert abs(result["product"] - 0.5) < 0.1
        assert result["satisfies_uncertainty"] == True


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
        # Independent recomputation of the purity from the state itself.
        rho = np.outer(total, total.conj())
        purity_indep = float(np.real(np.trace(rho @ rho)))
        assert abs(view["purity"] - purity_indep) < 1e-12
        assert abs(view["purity"] - 1.0) < 1e-6
        # `collapsed: False` is a source literal in measurement.py and is not
        # asserted. Its checkable content is that the global state is still
        # pure, i.e. its von Neumann entropy vanishes.
        eigs = np.linalg.eigvalsh(rho).real
        eigs = eigs[eigs > 1e-12]
        assert abs(-np.sum(eigs * np.log(eigs))) < 1e-9

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

    def test_verify_conditions_contract(self):
        """CONTRACT ONLY — these four checks cannot fail, and the module says so.

        C2 is automatic for any density matrix, C3 is linearity of the trace,
        C4 is true by construction, C1 is a dimension comparison. Passing them
        is not evidence for anything; this test only pins that the four keys are
        still computed and still reported honestly.
        """
        gv = GleasonVerification(dimension=4)
        result = gv.verify_conditions()
        assert result["all_conditions_satisfied"] is True
        for key in ("C1_dimension_ge_3", "C2_non_negativity",
                    "C3_additivity", "C4_normalization"):
            assert result[key]["satisfied"] is True
        # The flag must be the AND of the four, not an independent literal.
        assert result["all_conditions_satisfied"] == all(
            result[k]["satisfied"] for k in
            ("C1_dimension_ge_3", "C2_non_negativity", "C3_additivity", "C4_normalization"))

    def test_born_additivity_holds_and_non_born_rules_fail(self):
        """The Born flag is only meaningful next to rules that make it False."""
        gv = GleasonVerification(dimension=4)
        result = gv.demonstrate_uniqueness()
        born = result["born_rule"]["additivity"]
        assert born["satisfies_additivity"] is True
        assert born["violations"] == 0
        assert born["max_violation"] < 1e-12
        # Negative controls: the sampled non-Born ray rules must VIOLATE
        # additivity on the same tests. Without these the Born flag would be
        # unfalsifiable.
        for alt in ("alternative_amplitude", "alternative_quartic"):
            bad = result[alt]["additivity"]
            assert bad["satisfies_additivity"] is False
            assert bad["violations"] == bad["tests"]
            assert bad["max_violation"] > 1e-3
        # The module must keep saying this is not a uniqueness proof.
        assert "NOT a uniqueness proof" in result["scope"]

    def test_dim2_exception(self):
        gv = GleasonVerification(dimension=4)
        result = gv.demonstrate_dim2_exception()
        assert result["dim_2"]["dispersion_free_works"] is True
        # The dim-3 side is a COMPUTED refutation: the assignment must fail on a
        # substantial fraction of random bases, and the flag must follow the
        # measured rate rather than standing alone.
        d3 = result["dim_3"]
        assert d3["total_tests"] >= 100
        assert 0.0 < d3["failure_rate"] <= 1.0
        assert d3["dispersion_free_fails"] == (d3["failure_rate"] > 0)

    def test_axiom_count_bookkeeping_is_editorial_not_a_proof(self):
        """CONTRACT ONLY — the axiom counts are hand-entered integers.

        Renamed 2026-08-15 from ``test_axiom_reduction``, which asserted
        ``copenhagen == 7`` and ``advaita_independent == 4`` — the same literals
        the module assigns, so it could not fail. What IS checkable is that the
        arithmetic is self-consistent and that the provenance caveat survives.
        """
        gv = GleasonVerification(dimension=4)
        result = gv.axiom_reduction_proof()
        counts = result["axiom_counts"]
        cop, stated, indep = (counts["copenhagen"], counts["advaita_stated"],
                              counts["advaita_independent"])
        assert cop > stated > indep >= 1
        # The advertised reduction must be the arithmetic difference.
        assert f"{cop} → {indep}" in counts["reduction"]
        assert f"({cop - indep} fewer axioms)" in counts["reduction"]
        # Exactly one axiom (the Born rule) is claimed to be absorbed by Gleason.
        assert stated - indep == 1
        # The honesty caveats must not be quietly dropped.
        assert "not computed" in counts["provenance"]
        assert "Nothing here is proved" in result["status"]
        # The three genuinely computed checks it reports:
        assert result["check_1_conditions_consistent"] is True
        assert result["check_2_born_additivity_holds"] is True
        assert result["check_3_dispersion_free_fails_in_dim3"] is True


class TestEREqualsEPR:
    def test_thermofield_double_entropy_matches_closed_form(self):
        er = EREqualsEPR(dimension=4)
        beta = 1.0
        tfd = er.thermofield_double(beta=beta)
        assert tfd["total_state_pure"] == True
        # Independent closed form: weights w_n ∝ exp(-beta*n/2), normalised so
        # sum w_n^2 = 1; the reduced state is diag(w_n^2) and
        # S = -sum w_n^2 ln w_n^2.
        e = np.arange(4, dtype=float)
        w = np.exp(-beta * e / 2)
        w = w / np.linalg.norm(w)
        p = w ** 2
        s_indep = float(-np.sum(p * np.log(p)))
        assert abs(tfd["entanglement_entropy"] - s_indep) < 1e-12
        assert abs(tfd["max_entropy"] - np.log(4)) < 1e-12
        assert abs(tfd["entanglement_fraction"] - s_indep / np.log(4)) < 1e-12
        # NOT asserted as a finding: `er_epr_identity`. The module's own
        # docstring states S_thermal is SET EQUAL to S_entanglement, so that
        # flag is definitional. Pin the definition instead of the "identity".
        assert tfd["thermal_entropy"] == tfd["entanglement_entropy"]

    def test_thermofield_high_temperature_high_entanglement(self):
        er = EREqualsEPR(dimension=4)
        hot = er.thermofield_double(beta=0.1)
        cold = er.thermofield_double(beta=5.0)
        assert hot["entanglement_entropy"] > cold["entanglement_entropy"]

    def test_wormhole_from_entanglement(self):
        er = EREqualsEPR(dimension=2)
        wh = er.wormhole_from_entanglement(1.0)
        assert wh["wormhole_exists"] == True
        # Closed form: |psi> = cos(t)|00> + sin(t)|11> with t = s*pi/4, so
        # S = -c^2 ln c^2 - s^2 ln s^2 and (Ryu-Takayanagi, G=1) A = 4S.
        t = 1.0 * np.pi / 4
        p = np.array([np.cos(t) ** 2, np.sin(t) ** 2])
        s_indep = float(-np.sum(p[p > 0] * np.log(p[p > 0])))
        assert abs(wh["entanglement_entropy"] - s_indep) < 1e-12
        assert abs(s_indep - np.log(2)) < 1e-12      # maximally entangled qubit
        assert abs(wh["wormhole_throat_area"] - 4 * s_indep) < 1e-12

    def test_no_entanglement_no_wormhole(self):
        er = EREqualsEPR(dimension=2)
        wh = er.wormhole_from_entanglement(0.0)
        assert wh["wormhole_exists"] == False

    def test_throat_area_increases_with_entanglement(self):
        er = EREqualsEPR(dimension=2)
        wh_low = er.wormhole_from_entanglement(0.3)
        wh_high = er.wormhole_from_entanglement(1.0)
        assert wh_high["wormhole_throat_area"] > wh_low["wormhole_throat_area"]

    def test_cutting_entanglement_disconnects(self):
        er = EREqualsEPR(dimension=2)
        result = er.cutting_entanglement_destroys_geometry()
        assert result["connected_at_zero"] == False
        assert result["connected_at_max"] == True

    def test_monogamy_dilutes_bipartite_entanglement(self):
        """Replaces an assertion on `non_traversable`, which is a source literal.

        The computed content of the monogamy argument is that A's entanglement
        is strictly smaller once a third party is present.
        """
        er = EREqualsEPR(dimension=4)
        result = er.non_traversability_from_monogamy()
        s_ab = result["max_entanglement_AB"]
        s_abc = result["entanglement_A_in_tripartite"]
        assert s_ab > 0
        assert s_abc < s_ab                       # monogamy: strictly diluted
        assert result["entanglement_diluted"] is True
        assert abs(result["dilution_ratio"] - s_abc / s_ab) < 1e-12
        assert 0.0 <= result["dilution_ratio"] < 1.0
        # A maximally entangled pair in dim 4 saturates at ln 4.
        assert abs(s_ab - np.log(4)) < 1e-9

    def test_full_demonstration_carries_the_computed_trends(self):
        """Replaces `summary["er_equals_epr"] == True` (a source literal) with
        the three monotonic trends the demonstration actually computes."""
        er = EREqualsEPR(dimension=2)
        result = er.full_demonstration()
        tfd = result["thermofield_double"]
        assert (tfd["high_temperature"]["entanglement_entropy"]
                > tfd["medium_temperature"]["entanglement_entropy"]
                > tfd["low_temperature"]["entanglement_entropy"])
        geo = result["wormhole_geometry"]
        assert (geo["max_entanglement"]["wormhole_throat_area"]
                > geo["half_entanglement"]["wormhole_throat_area"]
                > geo["no_entanglement"]["wormhole_throat_area"])
        assert geo["no_entanglement"]["wormhole_exists"] is False
        assert result["van_raamsdonk"]["connected_at_max"] is True
        assert result["van_raamsdonk"]["connected_at_zero"] is False


class TestUnityOfExperience:
    def test_invalid_n_outcomes_raises(self):
        with pytest.raises(ValueError):
            UnityOfExperience(n_outcomes=1)

    def test_post_measurement_state_is_pure(self):
        u = UnityOfExperience(n_outcomes=3)
        sb = u.post_measurement_state()
        assert abs(sb["total_purity"] - 1.0) < 1e-10

    def test_reduced_state_is_diagonal_in_pointer_basis(self):
        u = UnityOfExperience(n_outcomes=3)
        sb = u.post_measurement_state()
        rho_sa = u.reduced_SA(sb)
        einsel = u.einselection_diagnostic(rho_sa)
        assert einsel["is_diagonal_pointer_basis"] is True
        assert einsel["off_diagonal_norm"] < 1e-10

    def test_reduced_state_trace_one(self):
        u = UnityOfExperience(n_outcomes=4)
        sb = u.post_measurement_state()
        rho_sa = u.reduced_SA(sb)
        assert abs(float(np.real(np.trace(rho_sa))) - 1.0) < 1e-10

    def test_reduced_state_is_mixed(self):
        u = UnityOfExperience(n_outcomes=3)
        sb = u.post_measurement_state()
        rho_sa = u.reduced_SA(sb)
        purity = float(np.real(np.trace(rho_sa @ rho_sa)))
        assert purity < 1.0 - 1e-6

    def test_distinct_cardinalities_across_interpretations(self):
        u = UnityOfExperience(n_outcomes=3)
        result = u.underdetermination_test()
        assert result["distinct_cardinalities_count"] >= 2

    def test_decoherence_underdetermines_experience(self):
        u = UnityOfExperience(n_outcomes=3)
        result = u.underdetermination_test()
        assert result["decoherence_underdetermines_experience"] is True

    def test_all_interpretations_consistent_with_rho(self):
        u = UnityOfExperience(n_outcomes=3)
        result = u.underdetermination_test()
        for interp in result["interpretations"]:
            assert interp["consistent_with_rho_sa"] is True
            assert interp["justification_by_decoherence"] is False

    def test_sweep_is_structurally_invariant_not_robustness_evidence(self):
        """Renamed 2026-08-15 from ``test_robustness_all_trials_pass``.

        A 100% "success rate" here is guaranteed before the first trial runs —
        three of the four interpretation maps never read rho_SA. The only
        assertion with content is the DEGENERATE NEGATIVE CONTROL: an
        undecohered rank-1 rho_SA must still return the same verdict, which is
        what proves the verdict is insensitive to the data.
        """
        u = UnityOfExperience(n_outcomes=3)
        sweep = u.sweep_robustness(n_trials=20)
        assert sweep["trials"] == 20
        assert sweep["verdict_true_count"] == 20
        # Negative control: amplitudes (1,0,0) give a product state — nothing has
        # decohered — so rho_SA has rank exactly 1.
        assert sweep["control_rho_SA_rank"] == 1
        assert sweep["control_verdict_true"] is True, (
            "the control is the whole point: the verdict survives a state in "
            "which no decoherence has occurred")
        assert sweep["structurally_invariant"] is True
        assert "NOT EVIDENCE" in sweep["interpretation"]
        # The deprecated aliases must still agree with the honest keys.
        assert sweep["success_rate"] == sweep["verdict_true_rate"] == 1.0

    def test_run_all_orchestrator(self):
        u = UnityOfExperience(n_outcomes=3)
        result = u.run_all()
        assert "main_result" in result
        assert "robustness" in result
        assert result["main_result"]["decoherence_underdetermines_experience"] is True


class TestScoreboardsStayDeleted:
    """
    Regression guard for the 2026-08-16 deletion of the Experiment 17 and 24
    scoreboards.

    Both experiments used to report figures that were ``len()`` of lists
    written inside the modules themselves -- axiom counts, phenomena tallies,
    a novel-predictions ranking, a parsimony ordering, and a count of
    "ontological divergences". Nothing about physics could change any of them.
    Experiment 24 additionally reported an ``all_empirically_identical`` flag
    that was True for every possible input, because it compared one array
    against a copy of itself.

    These tests fail if any of that returns.
    """

    BANNED_17 = {"axiom_count", "ranking_by_parsimony", "num_predictions",
                 "phenomena_addressed", "phenomena_with_problems",
                 "phenomena_clean", "novel_predictions"}

    def test_interpretation_comparison_reports_no_counts_or_rankings(self):
        from quantum.interpretations import InterpretationComparison
        comp = InterpretationComparison()

        axioms = comp.axiom_comparison()
        assert "ranking_by_parsimony" not in axioms
        for entry in axioms.values():
            assert "axiom_count" not in entry
            assert entry["axioms"], "the axioms themselves must be kept"

        scope = comp.explanatory_scope()
        for entry in scope.values():
            assert self.BANNED_17.isdisjoint(entry), (
                f"a deleted count returned in explanatory_scope: {entry}")
            assert isinstance(entry["phenomena_flagging_a_residual_problem"], list)

        assert not hasattr(comp, "novel_predictions_comparison"), (
            "novel_predictions_comparison scored interpretations by the length "
            "of lists written for them here; it must stay deleted")

        for row in comp.summary_table().values():
            assert self.BANNED_17.isdisjoint(row), f"deleted count in summary_table: {row}"

        assert "novel_predictions" not in comp.full_comparison()

    def test_empirical_agreement_declares_it_is_by_construction(self):
        from quantum.interpretations import InterpretationComparison
        agreement = InterpretationComparison().empirical_agreement()
        # The agreement is real but structural: all four inherit one
        # compute_predictions(). It must not be presented as a test result.
        assert agreement["agreement_is_by_construction"] is True

    def test_operational_equivalence_reaches_no_verdict(self):
        from quantum.operational_equivalence import OperationalEquivalence
        oe = OperationalEquivalence(dimension=4)

        assert not hasattr(oe, "full_equivalence_test"), (
            "full_equivalence_test() returned a cannot-fail verdict; "
            "full_report() replaces it")

        report = oe.full_report()
        flat = repr(report)
        for banned in ("all_empirically_identical", "empirical_tests_passed",
                       "ontological_divergences\": 5", "measurable_divergences",
                       "numbers_identical"):
            assert banned not in flat, f"deleted verdict field returned: {banned}"

        assert "ANALYTIC" in report["equivalence_status"]
        # The shared quantities must still be computed, not stubbed.
        probs = report["shared_quantities"]["probabilities"]["probabilities"]
        assert abs(sum(probs) - 1.0) < 1e-12

    def test_no_arm_is_a_copy_of_another_arm(self):
        """
        The specific defect: two 'interpretations' that were one array copied
        twice, so their difference was identically zero.

        Searched against EXECUTABLE code only. The module's HISTORY docstring
        deliberately quotes the removed lines so the record survives, and a
        naive source search matches that quotation -- which is exactly the
        false positive this strips out.
        """
        import ast, inspect
        from quantum import operational_equivalence as oe_mod

        tree = ast.parse(inspect.getsource(oe_mod))
        for node in ast.walk(tree):
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) \
                    and isinstance(node.value.value, str):
                node.value.value = ""          # blank every docstring/string literal
        code = ast.unparse(tree)

        for banned in ("everett_probs", "advaita_probs", "everett_state",
                       "advaita_state", "everett_outcomes", "advaita_outcomes"):
            assert banned not in code, (
                f"{banned} is live code again: the two-arm comparison was a copy "
                f"of one array, and must not return")
