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
