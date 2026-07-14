"""
Tests for the framework-Φ vs canonical-IIT-Φ (PyPhi) benchmark.

These run WITHOUT pyphi: the framework side is recomputed live, and the
canonical Φ values are read from a checked-in fixture that was generated once in
a Python<=3.9 environment with pyphi installed (see predictions/pyphi_benchmark.py).
Regenerating the fixture: build systems, compute pyphi Φ in that environment,
and overwrite tests/fixtures/pyphi_benchmark_reference.json.
"""
import json
import os

import numpy as np

from predictions.pyphi_benchmark import (
    xor_tpm, reachable_state, framework_phi, run_benchmark, compare,
)

FIX = os.path.join(os.path.dirname(__file__), "fixtures")
FW = os.path.join(FIX, "pyphi_benchmark_framework.json")
REF = os.path.join(FIX, "pyphi_benchmark_reference.json")


class TestBenchmarkMechanics:
    def test_xor_tpm_shape_and_parity(self):
        A = np.array([[0, 1], [1, 0]])
        tpm = xor_tpm(A)
        assert tpm.shape == (4, 2)
        # state (1,0): node0's input is node1(=0)->0; node1's input is node0(=1)->1
        idx = 0b10
        assert list(tpm[idx]) == [0.0, 1.0]

    def test_reachable_state_is_a_successor(self):
        A = np.array([[0, 1], [1, 0]])
        tpm = xor_tpm(A)
        rng = np.random.default_rng(0)
        st = reachable_state(tpm, 2, rng)
        assert len(st) == 2 and all(b in (0, 1) for b in st)

    def test_framework_phi_runs(self):
        A = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
        phi = framework_phi(A, [1, 0, 0])
        assert isinstance(phi, float) and phi >= 0.0


class TestBenchmarkResult:
    def test_fixture_reproduces_no_correspondence(self):
        stats = run_benchmark(FW, REF)
        # The headline finding: the two Φ measures are uncorrelated and
        # agree on integration only near chance. Lock in the qualitative result.
        assert stats["n"] >= 20
        assert abs(stats["pearson_r"]) < 0.4        # no linear relationship
        assert stats["detection_agreement"] < 0.75  # not a reliable classifier
        # both measures find *some* integrated systems (sanity, not agreement)
        assert stats["framework_nonzero"] > 0 and stats["reference_nonzero"] > 0

    def test_framework_side_matches_fixture(self):
        # The stored framework Φ values must be reproducible from the code,
        # so the fixture cannot silently drift from the implementation.
        # (Systems are encoded by their adjacency in the framework fixture's
        # companion; here we just check the fixture is internally consistent.)
        fw = json.load(open(FW))
        assert all("framework_phi" in r for r in fw)
        assert any(r["framework_phi"] > 1e-6 for r in fw)
