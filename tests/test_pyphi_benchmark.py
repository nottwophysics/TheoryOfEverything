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
        rows = {tuple(int(x) for x in row) for row in tpm}
        for _ in range(20):
            st = reachable_state(tpm, 2, rng)
            assert len(st) == 2 and all(b in (0, 1) for b in st)
            # The point of the helper: the state must actually BE a successor,
            # i.e. a row of the TPM. The old test only checked it was a bitstring.
            assert st in rows

    def test_framework_phi_runs(self):
        A = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
        phi = framework_phi(A, [1, 0, 0])
        assert isinstance(phi, float) and phi >= 0.0
        # A disconnected system has nothing to integrate: Phi must be 0.
        assert framework_phi(np.zeros((3, 3)), [1, 0, 0]) == 0.0


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

    def test_framework_phi_for_the_pyphi_example_networks_is_reproducible(self):
        """Recompute the framework Φ for the two rows that CAN be recomputed.

        HISTORY (2026-08-15): this test was called
        ``test_framework_side_matches_fixture`` and its docstring claimed "the
        stored framework Φ values must be reproducible from the code". It
        recomputed nothing — it opened one committed fixture and asserted that a
        key was present. Two rows are genuinely reproducible, because they are
        PyPhi's own published example networks: ``basic`` (connectivity matrix
        [[0,0,1],[1,0,1],[1,1,0]], state (1,0,0)) and ``xor`` (all-to-all XOR,
        state (0,0,0)). Those are recomputed here and matched against the
        fixture.

        The other 22 rows are the home-built XOR family whose adjacencies were
        never committed (see the ORDERING CAVEAT in
        ``predictions/pyphi_benchmark.py``); they CANNOT be regenerated and are
        deliberately not asserted as reproducible.
        """
        fw = {r["name"]: r for r in json.load(open(FW))}
        ref = {r["name"]: r for r in json.load(open(REF))}

        basic_cm = np.array([[0, 0, 1], [1, 0, 1], [1, 1, 0]], dtype=float)
        xor_cm = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]], dtype=float)

        basic_phi = framework_phi(basic_cm, [1, 0, 0])
        xor_phi = framework_phi(xor_cm, [0, 0, 0])
        assert abs(basic_phi - fw["basic"]["framework_phi"]) < 1e-6, (
            f"framework Phi for PyPhi's basic network drifted: recomputed "
            f"{basic_phi}, fixture {fw['basic']['framework_phi']}")
        assert abs(xor_phi - fw["xor"]["framework_phi"]) < 1e-6

        # The recomputed value is ln 2 — a closed form, not a stored number.
        assert abs(basic_phi - np.log(2)) < 1e-6
        assert xor_phi == 0.0

        # The headline finding, on the two convention-independent rows: the
        # framework measure is nowhere near canonical IIT Φ. PyPhi's own values
        # for these networks are 2.3125 and 1.875.
        assert abs(ref["basic"]["pyphi_phi"] - 2.3125) < 1e-9
        assert abs(ref["xor"]["pyphi_phi"] - 1.875) < 1e-9
        assert basic_phi < 0.5 * ref["basic"]["pyphi_phi"]
        assert xor_phi == 0.0 < ref["xor"]["pyphi_phi"]

    def test_fixture_pairing_contract(self):
        """CONTRACT ONLY — the two fixtures must stay row-aligned.

        This pins file structure, not physics; the 22 XOR-family rows cannot be
        recomputed (their adjacencies were never committed).
        """
        fw = json.load(open(FW))
        ref = json.load(open(REF))
        assert len(fw) == len(ref) >= 24
        assert [r["id"] for r in fw] == [r["id"] for r in ref]
        assert [r["name"] for r in fw] == [r["name"] for r in ref]
        assert all("framework_phi" in r for r in fw)
        assert any(r["framework_phi"] > 1e-6 for r in fw)
