"""
Tests for the MEASURED content of quantum/unity_of_experience.py
(added 2026-08-15 with the structural-verdict removal).

Two groups:

  1. The genuinely measured claims — rho_SA's invariance under environment
     unitaries, and the factorization-dependence of the branch count. These
     must fail if the reductions are wrong, so each is also probed with a
     tolerance that MUST flip the flag.

  2. Regression locks on the honest relabelling — the four-interpretation
     catalogue is analytic, and this file pins the mechanism (three maps
     ignore rho_sa) so nobody can re-promote "30/30 trials" to a result.
"""

import numpy as np
import pytest

from quantum.unity_of_experience import UnityOfExperience


# ----------------------------------------------------------------------
# 1. MEASURED: rho_SA is blind to unitaries on the environment
# ----------------------------------------------------------------------

class TestEnvironmentUnitaryInvariance:
    def test_rho_SA_invariant_to_1e_14(self):
        u = UnityOfExperience(n_outcomes=3, seed=42)
        res = u.environment_unitary_invariance(n_trials=20, tol=1e-14)
        assert res["max_rho_SA_trace_norm_change"] < 1e-14
        assert res["rho_SA_invariant"] is True

    def test_environment_state_and_records_actually_change(self):
        # The invariance claim is only meaningful if the environment really moved.
        u = UnityOfExperience(n_outcomes=3, seed=42)
        res = u.environment_unitary_invariance(n_trials=20)
        assert res["min_rho_E_trace_norm_change"] > 1e-6
        assert res["environment_state_changed"] is True
        assert res["min_max_record_change"] > 1e-6
        assert res["environment_records_changed"] is True

    def test_invariance_flag_is_computed_not_hardcoded(self):
        # With an impossible tolerance the same data must report False.
        u = UnityOfExperience(n_outcomes=3, seed=42)
        strict = u.environment_unitary_invariance(n_trials=5, tol=0.0)
        assert strict["rho_SA_invariant"] is False

    def test_random_unitaries_are_unitary(self):
        u = UnityOfExperience(n_outcomes=4, seed=7)
        res = u.environment_unitary_invariance(n_trials=10)
        assert res["max_unitarity_error"] < 1e-10

    def test_holds_for_other_dimensions(self):
        for n in (2, 4, 5):
            u = UnityOfExperience(n_outcomes=n, seed=3)
            res = u.environment_unitary_invariance(n_trials=8, tol=1e-13)
            assert res["rho_SA_invariant"] is True
            assert res["environment_state_changed"] is True

    def test_manual_reproduction_of_the_invariance(self):
        # Independent re-derivation, not reading the module's own verdict.
        n = 3
        u = UnityOfExperience(n_outcomes=n, seed=11)
        bundle = u.post_measurement_state()
        psi = bundle["psi"]
        rng = np.random.default_rng(99)
        z = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
        q, r = np.linalg.qr(z)
        q = q @ np.diag(np.diag(r) / np.abs(np.diag(r)))

        t = psi.reshape(n, n, n)
        psi_p = np.einsum("fe,sae->saf", q, t).reshape(-1)

        rho = u._rho_SA_from_psi(psi, n)
        rho_p = u._rho_SA_from_psi(psi_p, n)
        assert np.sum(np.linalg.svd(rho - rho_p, compute_uv=False)) < 1e-14

        rho_e = u._rho_E_from_psi(psi, n)
        rho_e_p = u._rho_E_from_psi(psi_p, n)
        assert np.sum(np.linalg.svd(rho_e - rho_e_p, compute_uv=False)) > 1e-6


# ----------------------------------------------------------------------
# 2. MEASURED: the branch count depends on the S/A/E factorization
# ----------------------------------------------------------------------

class TestFactorizationDependence:
    def test_regrouping_is_a_non_product_unitary(self):
        u = UnityOfExperience(n_outcomes=3, seed=42)
        res = u.factorization_dependence()
        assert res["regrouping_is_unitary"] is True
        assert res["regrouping_unitarity_error"] < 1e-10
        # If it were a product U_A (x) U_E the demonstration would be empty.
        assert res["operator_schmidt_rank_across_A_E"] > 1
        assert res["regrouping_is_product_across_A_E"] is False

    def test_branch_count_changes_while_rho_S_does_not(self):
        u = UnityOfExperience(n_outcomes=3, seed=42)
        res = u.factorization_dependence()
        assert res["rank_rho_SA_before"] == 3
        assert res["rank_rho_SA_after"] == 1
        assert res["branch_count_changed"] is True
        assert res["rho_S_trace_norm_change"] < 1e-12
        assert res["rho_S_invariant"] is True

    def test_nothing_was_lost_global_state_still_pure(self):
        u = UnityOfExperience(n_outcomes=4, seed=5)
        res = u.factorization_dependence()
        assert res["global_state_still_pure"] is True
        assert abs(res["global_state_norm_after"] - 1.0) < 1e-10

    def test_rank_before_tracks_n_outcomes(self):
        # rank(rho_SA) before the regrouping must follow the data, not a constant.
        for n in (2, 3, 5):
            u = UnityOfExperience(n_outcomes=n, seed=13)
            res = u.factorization_dependence()
            assert res["rank_rho_SA_before"] == n
            assert res["rank_rho_SA_after"] == 1

    def test_rho_S_invariance_flag_is_computed(self):
        u = UnityOfExperience(n_outcomes=3, seed=42)
        strict = u.factorization_dependence(tol=0.0)
        # rho_S really is bit-identical here, so an exact-zero tolerance is the
        # one case that must still be reported honestly:
        assert strict["rho_S_trace_norm_change"] == 0.0
        assert strict["rho_S_invariant"] is False  # 0.0 < 0.0 is False

    def test_rho_SA_really_moved(self):
        u = UnityOfExperience(n_outcomes=3, seed=42)
        res = u.factorization_dependence()
        assert res["rho_SA_trace_norm_change"] > 0.5


# ----------------------------------------------------------------------
# 3. Regression locks on the honest relabelling
# ----------------------------------------------------------------------

class TestCatalogueIsAnalyticNotEmpirical:
    def test_three_maps_ignore_rho_sa(self):
        # Feed each map a matrix that is not a density matrix at all.
        u = UnityOfExperience(n_outcomes=3, seed=42)
        garbage = np.full((9, 9), 7.0 + 1j, dtype=np.complex128)
        assert u.everett_superposed_map(garbage, 3)["n_unified_experiences"] == 0
        assert u.copenhagen_classical_map(garbage, 3)["n_unified_experiences"] == 1
        assert u.subject_modes_map(garbage, 3)["n_unified_experiences"] == 1

    def test_definitional_sources_are_labelled(self):
        u = UnityOfExperience(n_outcomes=3, seed=42)
        result = u.underdetermination_test()
        assert result["definitional_cardinality_count"] == 3
        sources = [m["cardinality_source"] for m in result["interpretations"]]
        assert sum(s.startswith("definitional") for s in sources) == 3
        assert "ANALYTIC" in result["verdict_status"]

    def test_verdict_survives_an_undecohered_rank_1_state(self):
        # The point of the relabelling: the verdict cannot come out False.
        u = UnityOfExperience(n_outcomes=3, seed=42)
        bundle = u.post_measurement_state(amplitudes=[1.0, 0.0, 0.0])
        rho = u.reduced_SA(bundle)
        assert u.einselection_diagnostic(rho)["rank"] == 1
        result = u.underdetermination_test(bundle)
        assert result["decoherence_underdetermines_experience"] is True

    def test_sweep_reports_structural_invariance_with_control(self):
        u = UnityOfExperience(n_outcomes=3, seed=42)
        res = u.sweep_robustness(n_trials=10)
        assert res["control_rho_SA_rank"] == 1
        assert res["control_verdict_true"] is True
        assert res["structurally_invariant"] is True
        assert "NOT EVIDENCE" in res["interpretation"]

    def test_run_all_carries_the_measured_results(self):
        u = UnityOfExperience(n_outcomes=3, seed=42)
        report = u.run_all()
        assert "environment_unitary_invariance" in report
        assert "factorization_dependence" in report
        assert report["environment_unitary_invariance"]["rho_SA_invariant"] is True
        assert report["factorization_dependence"]["branch_count_changed"] is True
        # The old headline must no longer read as a robustness finding.
        assert "ANALYTIC" in report["paper_claim_supported"]


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-v"])
