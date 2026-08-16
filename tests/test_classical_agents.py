"""Tests for the classical multi-agent §2.5 symmetry analogue and emergence detector."""
import numpy as np

from agents.classical_symmetry import (
    entropy, total_correlation, kl_divergence, product_of_marginals,
    symmetry_report, all_marginals, total_variation,
)
from agents.multiagent_testbed import (
    independent, redundant, synergistic, make_testbed,
)
from agents.emergence_detector import measures, permutation_null, classify


class TestSymmetryRecovery:
    def test_marginals_identical_topdown_bottomup(self):
        rng = np.random.default_rng(42)
        for n in (2, 3, 4):
            P = rng.random(2 ** n); P /= P.sum()
            r = symmetry_report(P, n)
            assert r["single_perspective_identical"]

    def test_kl_equals_total_correlation(self):
        rng = np.random.default_rng(1)
        for n in (2, 3, 4):
            P = rng.random(2 ** n); P /= P.sum()
            assert abs(total_correlation(P, n) - kl_divergence(P, product_of_marginals(P, n))) < 1e-10

    def test_independent_zero_redundant_max(self):
        # independent product -> C=0
        p = np.array([0.5, 0.5]); P = np.kron(np.kron(p, p), p)
        assert total_correlation(P, 3) < 1e-12
        # perfectly correlated 000/111 -> C = 2 bits (N-1)
        P2 = np.zeros(8); P2[0] = P2[7] = 0.5
        assert abs(total_correlation(P2, 3) - 2.0) < 1e-9


class TestTestbedGroundTruth:
    def test_independent_no_structure(self):
        rng = np.random.default_rng(42)
        m = measures(independent(4, 20000, rng))
        assert abs(m["total_correlation"]) < 0.02
        assert abs(m["o_information"]) < 0.02

    def test_redundant_positive_o(self):
        rng = np.random.default_rng(42)
        m = measures(redundant(4, 20000, rng, noise=0.1))
        assert m["total_correlation"] > 0.5
        assert m["o_information"] > 0.05          # redundancy-dominated

    def test_synergistic_negative_o(self):
        rng = np.random.default_rng(42)
        m = measures(synergistic(4, 20000, rng, noise=0.0))
        assert m["o_information"] < -0.5          # synergy-dominated
        assert classify(synergistic(4, 20000, rng)) == "synergy"

    def test_synergy_has_no_pairwise_signal(self):
        # the whole point: parity is invisible to pairwise correlation
        rng = np.random.default_rng(42)
        s = synergistic(4, 20000, rng, noise=0.0)
        C = np.corrcoef(s.T)
        off = C[~np.eye(4, dtype=bool)]
        assert np.nanmax(np.abs(off)) < 0.1       # near-zero pairwise corr


class TestNull:
    def test_permutation_null_independent_nonsignificant(self):
        rng = np.random.default_rng(42)
        res = permutation_null(independent(4, 8000, rng), n_perm=200, seed=42)
        assert res["p_value"]["total_correlation"] > 0.05

    def test_permutation_null_synergy_significant(self):
        rng = np.random.default_rng(42)
        res = permutation_null(synergistic(4, 8000, rng), n_perm=200, seed=42)
        assert res["p_value"]["o_information"] < 0.05


class TestBeatTheBaselinesBenchmark:
    """
    The benchmark both classical reports called "the decisive test".

    Until 2026-08-16 no AUC, ROC or Cohen's-d computation existed anywhere in
    the tree, so the table positioning Omega against the designer baselines was
    unrunnable by any reader. These tests exercise the committed version.
    """

    def test_auc_helper_matches_known_values(self):
        from agents.benchmark import _auc
        assert _auc([3, 4, 5], [0, 1, 2]) == 1.0          # perfect separation
        assert _auc([0, 1, 2], [3, 4, 5]) == 0.0          # perfectly reversed
        assert _auc([1, 2], [1, 2]) == 0.5                # identical -> chance
        assert _auc([1, 1], [1, 1]) == 0.5                # all ties -> chance

    def test_benchmark_separates_and_baselines_do_not(self):
        from agents.benchmark import run_benchmark
        r = run_benchmark(n_instances=25, n_samples=1500, seed=7)
        auc = r["auc"]
        assert auc["abs_o_information"] == 1.0
        # Measured across seeds {7,42,101} x n_samples {1500,4000}: the detector
        # is 1.000 in every configuration; the baselines range 0.26-0.66. So the
        # honest assertion is that no baseline APPROACHES separation, not that
        # each sits at some tidy value.
        for k in ("max_abs_pairwise_corr", "mean_abs_pairwise_corr",
                  "max_per_agent_variance"):
            assert auc[k] < 0.75, f"{k} = {auc[k]} unexpectedly separates"
        # max|pairwise correlation| is consistently BELOW chance, and that is
        # explicable rather than noise: the parity construction has exactly zero
        # pairwise correlation, while independent bits show small sample
        # correlations -- so a designer reading pairwise coupling ranks the
        # synergistic regime as LESS coupled than independent noise.
        assert auc["max_abs_pairwise_corr"] < 0.5

    def test_total_correlation_also_separates_and_this_is_disclosed(self):
        """Omega is NOT distinguished from TC on this task. Must not be hidden."""
        from agents.benchmark import run_benchmark
        r = run_benchmark(n_instances=25, n_samples=1500, seed=7)
        assert r["auc"]["total_correlation"] == 1.0
        assert r["total_correlation_also_separates"] is True
        assert r["separation_is_by_construction"] is True

    def test_cohens_d_is_not_reported(self):
        """d ~ 68 was a sample-count artifact; it must not come back."""
        from agents.benchmark import run_benchmark
        r = run_benchmark(n_instances=10, n_samples=800, seed=3)
        flat = repr(r).lower()
        assert "cohen" not in flat.replace("cohens_d_not_computed", "")
        assert not any(k.startswith("d_") or k == "d" for k in r.get("auc", {}))

    def test_sign_separates_where_total_correlation_is_at_chance(self):
        """
        The real differentiator, on a fair comparison: hold TC fixed, and
        Omega's sign still separates synergy from redundancy.
        """
        from agents.benchmark import sign_separation
        s = sign_separation(n_instances=20, n_samples=2000, seed=11)
        # TC must be genuinely uninformative here, or the test proves nothing.
        assert s["tc_distributions_overlap"] is True
        assert abs(s["tc_auc_synergy_vs_redundancy"] - 0.5) < 0.25
        # ...and the sign still works.
        assert s["omega_synergistic_all_negative"] is True
        assert s["omega_redundant_all_positive"] is True
        assert s["mean_omega_synergistic"] < 0 < s["mean_omega_redundant"]

    def test_tc_matched_noise_is_findable(self):
        from agents.benchmark import find_tc_matched_noise, TC_MATCHED_NOISE
        found = find_tc_matched_noise(n_samples=2000, reps=6, iters=12)
        assert abs(found - TC_MATCHED_NOISE) < 0.05, (
            f"pinned TC_MATCHED_NOISE={TC_MATCHED_NOISE} but bisection found {found}")
