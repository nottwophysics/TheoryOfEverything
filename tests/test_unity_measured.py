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
        # Independent re-derivation.  The reductions are rebuilt here by a
        # DIFFERENT route (form |Psi><Psi| and trace the blocks) and the
        # module's own reduction is then checked against them.  Calling
        # u._rho_SA_from_psi for both sides -- what this test used to do --
        # re-reads whatever the module does, so a broken reduction survived it:
        # verified 2026-08-21, stubbing _rho_SA_from_psi to a constant left
        # every test in this class green.
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

        def rho_sa(v):
            full = np.outer(v, v.conj()).reshape(n, n, n, n, n, n)
            return np.trace(full, axis1=2, axis2=5).reshape(n * n, n * n)

        def rho_e(v):
            full = np.outer(v, v.conj()).reshape(n, n, n, n, n, n)
            return np.trace(np.trace(full, axis1=0, axis2=3), axis1=0, axis2=2)

        assert np.sum(np.linalg.svd(rho_sa(psi) - rho_sa(psi_p),
                                    compute_uv=False)) < 1e-14
        assert np.sum(np.linalg.svd(rho_e(psi) - rho_e(psi_p),
                                    compute_uv=False)) > 1e-6

        # The module must agree with the independent construction.
        assert np.allclose(u._rho_SA_from_psi(psi, n), rho_sa(psi), atol=1e-12)
        assert np.allclose(u._rho_E_from_psi(psi, n), rho_e(psi), atol=1e-12)


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

    def test_operator_schmidt_rank_matches_an_independent_derivation(self):
        # The paper prints this value ("operator Schmidt rank 3 across the
        # A|E cut"), so it must be pinned, not merely bounded below.  The two
        # assertions above are the same assertion twice --
        # regrouping_is_product_across_A_E IS (rank == 1) -- so any wrong
        # value above 1 passes them.  Here the rank is re-derived from R's
        # definition by a different route (SVD of the reshaped operator, not
        # the module's matrix_rank call) and the module is checked against it.
        n = 3
        res = UnityOfExperience(n_outcomes=n, seed=42).factorization_dependence()

        def operator_schmidt_rank(op, dim_a, dim_e):
            t = op.reshape(dim_a, dim_e, dim_a, dim_e).transpose(0, 2, 1, 3)
            sv = np.linalg.svd(
                t.reshape(dim_a * dim_a, dim_e * dim_e), compute_uv=False
            )
            return int(np.sum(sv > 1e-10))

        r = np.zeros((n * n, n * n), dtype=np.complex128)
        for a in range(n):
            for e in range(n):
                r[a * n + ((e - a) % n), a * n + e] = 1.0

        assert operator_schmidt_rank(r, n, n) == n
        assert res["operator_schmidt_rank_across_A_E"] == n

        # Negative control: the same routine must return 1 on a genuine
        # product unitary.  Without this, an assertion that only ever sees
        # non-product operators cannot show it can discriminate -- and it is
        # what pins the (a',a),(e',e) reshape convention: dropping the
        # transpose returns 9 here, not 1.
        rng = np.random.default_rng(0)

        def haar(dim):
            x = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
            q, upper = np.linalg.qr(x)
            return q @ np.diag(np.diag(upper) / np.abs(np.diag(upper)))

        assert operator_schmidt_rank(np.kron(haar(n), haar(n)), n, n) == 1

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

    def test_ranks_match_an_independent_schmidt_derivation(self):
        """The two ranks s2.4 prints, re-derived by a route the module does not use.

        The module counts eigenvalues of rho_SA (``eigvalsh``). Here the same two
        numbers are obtained as Schmidt ranks across the S(x)A | E cut -- singular
        values of the reshaped state vector -- with the regrouping R rebuilt from
        its definition in the paper, R|a>|e> = |a>|(e-a) mod n>, rather than taken
        from the module.

        Scope, stated plainly: rank n before and 1 after are guaranteed by the
        construction, so this cannot catch a report layer that simply returns
        ``(n, 1)``; the module's own docstring says the drop is guaranteed rather
        than discovered. What it does catch is a broken reduction, a broken index
        convention, or a wrong R. The negative control is the part that carries
        weight -- a genuine U_A (x) U_E leaves the branch count alone, which is
        the claim s2.4 rests on when it says R is NOT of that form.
        """
        def schmidt_rank_SA_E(vec, n, tol=1e-10):
            m = vec.reshape(n * n, n)          # (S(x)A) x E
            return int(np.sum(np.linalg.svd(m, compute_uv=False) > tol))

        def regrouping(n):
            R = np.zeros((n * n, n * n), dtype=np.complex128)
            for a in range(n):
                for e in range(n):
                    R[a * n + ((e - a) % n), a * n + e] = 1.0
            return R

        for n in (2, 3, 4, 5):
            u = UnityOfExperience(n_outcomes=n, seed=42)
            psi = u.post_measurement_state()["psi"]
            psi_p = (psi.reshape(n, n * n) @ regrouping(n).T).reshape(-1)
            res = u.factorization_dependence()
            assert schmidt_rank_SA_E(psi, n) == res["rank_rho_SA_before"] == n
            assert schmidt_rank_SA_E(psi_p, n) == res["rank_rho_SA_after"] == 1

        # The pair (n, 1) above is guaranteed by the construction, so on its own
        # it cannot discriminate a report layer that returns those two constants
        # without computing them. This case can: with one amplitude set to zero
        # the true rank is n-1, and a hardcoded ``n`` disagrees.
        u = UnityOfExperience(n_outcomes=3, seed=42)
        weights = np.array([1.0, 1.0, 0.0])
        degenerate = u.factorization_dependence(amplitudes=weights)
        psi_d = u.post_measurement_state(weights)["psi"]
        assert schmidt_rank_SA_E(psi_d, 3) == degenerate["rank_rho_SA_before"] == 2
        assert degenerate["rank_rho_SA_after"] == 1

        # NEGATIVE CONTROL: a genuine product unitary on A (x) E redraws nothing.
        # Both factors are local to one side of the S(x)A | E cut, so the Schmidt
        # rank -- and hence the branch count -- must be untouched. Without this,
        # nothing in the suite distinguishes "the regrouping is non-product" from
        # "any unitary collapses the count".
        rng = np.random.default_rng(0)

        def haar(dim):
            x = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
            q, upper = np.linalg.qr(x)
            return q @ np.diag(np.diag(upper) / np.abs(np.diag(upper)))

        n = 3
        u = UnityOfExperience(n_outcomes=n, seed=42)
        psi = u.post_measurement_state()["psi"]
        product = np.kron(haar(n), haar(n))
        psi_q = (psi.reshape(n, n * n) @ product.T).reshape(-1)
        assert schmidt_rank_SA_E(psi_q, n) == n

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


# ----------------------------------------------------------------------
# 3. MEASURED: rho_S is computed from the state, not assumed
# ----------------------------------------------------------------------

class TestRhoSIsComputedNotAssumed:
    """
    §2.4 reports that a regrouping unitary on A (x) E leaves rho_S unchanged
    ("trace-norm change 0.0").  That assertion has no teeth on its own: a
    reduction that ignores psi and returns a constant reproduces the 0.0
    exactly.  Verified 2026-08-21 — stubbing _rho_S_from_psi to eye(n)/n left
    all 490 tests passing.  These three pin the reduction itself.
    """

    def test_rho_S_equals_the_born_weights(self):
        """|Psi> = sum_k c_k |k>|k>|k>  =>  rho_S = diag(|c_k|^2)."""
        u = UnityOfExperience(n_outcomes=3, seed=42)
        amps = np.array([0.8, 0.5, 0.2])
        amps = amps / np.linalg.norm(amps)
        psi = u.post_measurement_state(amplitudes=amps)["psi"]
        rho_s = UnityOfExperience._rho_S_from_psi(psi, 3)
        np.testing.assert_allclose(np.real(np.diag(rho_s)), amps**2, atol=1e-12)

    def test_rho_S_depends_on_the_state(self):
        """Two states with different Born weights must give different rho_S."""
        u = UnityOfExperience(n_outcomes=3, seed=42)
        a = u.post_measurement_state(amplitudes=np.array([0.9, 0.3, 0.1]))["psi"]
        b = u.post_measurement_state(amplitudes=np.array([0.1, 0.3, 0.9]))["psi"]
        ra = UnityOfExperience._rho_S_from_psi(a, 3)
        rb = UnityOfExperience._rho_S_from_psi(b, 3)
        assert np.linalg.norm(ra - rb) > 0.1

    def test_the_invariance_claim_is_not_vacuous(self):
        """
        rho_S_trace_norm_change == 0 is only informative if rho_S is a
        non-trivial state.  A constant reduction would satisfy the
        invariance while carrying no information about the physics.
        """
        u = UnityOfExperience(n_outcomes=3, seed=42)
        res = u.factorization_dependence()
        assert res["rho_S_trace_norm_change"] < 1e-12
        rho_s = UnityOfExperience._rho_S_from_psi(
            u.post_measurement_state()["psi"], 3
        )
        assert np.linalg.norm(rho_s - np.eye(3) / 3) > 0.05
