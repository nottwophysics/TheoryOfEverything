"""
Track A acceptance tests — the real [[5,1,3]] five-qubit stabilizer code.

Pre-registered criteria (REAL_PHYSICS_REIMPLEMENTATION_MEMO.md, 2026-08-15):
  A1  encoded states are +1 eigenstates of all 4 stabilizers
      (|<S_i> - 1| < 1e-10);
  A2  all 15 single-qubit Pauli errors corrected by syndrome lookup:
      post-correction logical fidelity > 1 - 1e-10, for >= 3 distinct
      logical states;
  A3  any 2-of-5 known-location erasure (all 10 patterns) recovered exactly
      under random Pauli noise on the erased pair, decoding restricted to
      the erased support, fidelity > 1 - 1e-10;
  A4  (negative control) 3-erasure is UNRECOVERABLE: reduced states of
      logical |0> and |1> on the surviving 2 qubits are identical
      (trace distance < 1e-10) — the information is genuinely absent;
  A5  any 3-of-5 subregion reconstructs the logical qubit: reduced states
      of the logical basis states on every 3-qubit subset are perfectly
      distinguishable (trace distance 1 within 1e-10).

Plus mechanical no-hardcoding checks: the same machinery must produce
FAILING verdicts on inputs where the physics says it should fail (a
non-codeword, an uncorrected error, a wrong correction, a >2 erasure),
so no reported flag can be a constant.
"""

import itertools
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from quantum.error_correction import (
    DIM,
    N_QUBITS,
    STABILIZER_STRINGS,
    FiveQubitCode,
    HolographicCode,
    SubsystemCode,
    pauli_string_operator,
    reduced_density_matrix,
    syndrome_of_pauli,
    trace_distance,
)

TOL = 1e-10


def _code():
    return FiveQubitCode()


# ---------------------------------------------------------------------------
# A1 — codewords are +1 eigenstates of all four stabilizers
# ---------------------------------------------------------------------------


class TestA1StabilizerEigenstates:
    def test_encoded_states_are_plus_one_eigenstates(self):
        code = _code()
        states = code.reference_logical_states()
        assert len(states) >= 3  # memo: >= 3 distinct logical states
        for name, psi in states.items():
            assert abs(np.linalg.norm(psi) - 1.0) < TOL
            for s in STABILIZER_STRINGS:
                op = pauli_string_operator(s)
                exp = np.real(np.vdot(psi, op @ psi))
                assert abs(exp - 1.0) < TOL, (name, s, exp)

    def test_report_flag_matches_independent_recomputation(self):
        code = _code()
        report = code.codeword_stabilizer_check()
        assert report["all_plus_one_eigenstates"] is True
        assert report["max_eigenvalue_deviation"] < TOL

    def test_negative_control_non_codeword_fails_check(self):
        """|00000> is NOT a codeword; the same expectation machinery must
        detect that (guards against a check that ignores its input)."""
        code = _code()
        product = np.zeros(DIM, dtype=np.complex128)
        product[0] = 1.0
        exps = code.stabilizer_expectations(product)
        max_dev = max(abs(e - 1.0) for e in exps)
        assert max_dev > 0.5  # <00000|XZZXI|00000> = 0, far from +1

    def test_codewords_orthonormal_and_logical_z_acts(self):
        code = _code()
        assert abs(np.vdot(code.logical_zero, code.logical_one)) < TOL
        z_bar = pauli_string_operator("ZZZZZ")
        assert np.allclose(z_bar @ code.logical_zero, code.logical_zero, atol=TOL)
        assert np.allclose(z_bar @ code.logical_one, -code.logical_one, atol=TOL)


# ---------------------------------------------------------------------------
# A2 — all 15 single-qubit Pauli errors corrected by syndrome lookup
# ---------------------------------------------------------------------------


class TestA2SingleErrorCorrection:
    def test_all_15_errors_corrected_for_multiple_logical_states(self):
        code = _code()
        states = code.reference_logical_states()
        assert len(states) >= 3
        assert len(code.single_qubit_errors) == 15
        for psi in states.values():
            for err in code.single_qubit_errors:
                noisy = code.apply_pauli(psi, err)
                out = code.correct(noisy)
                fid = code.fidelity(psi, out["corrected_state"])
                assert fid > 1.0 - TOL, (err, fid)
                assert out["correction_applied"] is True

    def test_sixteen_distinct_syndromes(self):
        """Perfect code: 15 single-qubit Paulis + identity give 16 distinct
        syndromes (computed symbolically, not asserted by fiat)."""
        code = _code()
        syndromes = {syndrome_of_pauli(e) for e in code.single_qubit_errors}
        syndromes.add((0, 0, 0, 0))
        assert len(syndromes) == 16
        assert code.syndromes_all_distinct is True

    def test_report_flags_computed(self):
        code = _code()
        report = code.single_error_correction_report()
        assert report["n_cases"] >= 45  # >= 3 states x 15 errors
        assert report["min_fidelity"] > 1.0 - TOL
        assert report["all_corrected"] is True

    def test_negative_control_uncorrected_error_is_orthogonal(self):
        """Before correction, a nontrivial Pauli error takes the codeword to
        an ORTHOGONAL state (fidelity 0) — guards against a fidelity
        function that always reports success."""
        code = _code()
        psi = code.encode(1.0, 0.0)
        noisy = code.apply_pauli(psi, "XIIII")
        assert code.fidelity(psi, noisy) < TOL

    def test_negative_control_wrong_correction_fails(self):
        """Applying the WRONG single-qubit correction must not restore the
        state (the verdict genuinely depends on the syndrome lookup)."""
        code = _code()
        psi = code.encode(1.0, 0.0)
        noisy = code.apply_pauli(psi, "XIIII")
        wrongly_corrected = code.apply_pauli(noisy, "IIIIZ")
        assert code.fidelity(psi, wrongly_corrected) < 0.5


# ---------------------------------------------------------------------------
# A3 — any 2-of-5 known-location erasure recovered exactly
# ---------------------------------------------------------------------------


class TestA3TwoErasureRecovery:
    def test_all_10_patterns_recovered_exactly(self):
        code = _code()
        report = code.two_erasure_report(seed=42)
        assert report["n_patterns"] == 10
        assert report["min_fidelity"] > 1.0 - TOL
        assert report["all_recovered"] is True

    def test_exhaustive_pauli_noise_on_each_pair(self):
        """Direct exhaustive check independent of the report method: every
        Pauli on every erased pair, decoded restricted to that support."""
        code = _code()
        psi = code.encode(0.6, 0.8)
        for pair in itertools.combinations(range(N_QUBITS), 2):
            for letters in itertools.product("IXYZ", repeat=2):
                noise = ["I"] * N_QUBITS
                noise[pair[0]], noise[pair[1]] = letters
                noisy = code.apply_pauli(psi, "".join(noise))
                out = code.decode_erasure(noisy, pair)
                assert out["decoded"] is True
                fid = code.fidelity(psi, out["corrected_state"])
                assert fid > 1.0 - TOL, (pair, letters, fid)

    def test_correction_restricted_to_erased_support(self):
        """The decoder must only touch the erased qubits (known locations)."""
        code = _code()
        psi = code.encode(1.0, 1.0)
        pair = (1, 3)
        noisy = code.apply_pauli(psi, "IYIZI")
        out = code.decode_erasure(noisy, pair)
        correction = out["correction"]
        for q in range(N_QUBITS):
            if q not in pair:
                assert correction[q] == "I"


# ---------------------------------------------------------------------------
# A4 (negative control) — 3-erasure is information-theoretically unrecoverable
# ---------------------------------------------------------------------------


class TestA4ThreeErasureNegativeControl:
    def test_survivor_reduced_states_identical_for_every_3_erasure(self):
        """For every 3-erasure pattern (memo requires 'some'; all hold), the
        2 surviving qubits carry ZERO logical information: the reduced
        states of |0_L> and |1_L> coincide (no-cloning: 2 + 3 = 5, so a
        recoverable 2-qubit remnant would allow cloning)."""
        code = _code()
        for erased in itertools.combinations(range(N_QUBITS), 3):
            survivors = [q for q in range(N_QUBITS) if q not in erased]
            rho0 = reduced_density_matrix(code.logical_zero, survivors)
            rho1 = reduced_density_matrix(code.logical_one, survivors)
            assert trace_distance(rho0, rho1) < TOL, erased

    def test_report_flag_computed(self):
        code = _code()
        report = code.three_erasure_negative_control()
        assert report["n_patterns"] == 10
        assert report["max_trace_distance_on_survivors"] < TOL
        assert report["information_absent"] is True

    def test_threshold_verdict_varies_with_erasure_count(self):
        """Mechanical no-hardcoding check: the recoverable flag must flip
        within the loop that varies the erasure count (True at k <= 2,
        False at k >= 3), so the 2/5 threshold is computed, not asserted."""
        code = _code()
        thr = code.erasure_threshold()
        assert thr["per_erasure_count"][1]["recoverable"] is True
        assert thr["per_erasure_count"][2]["recoverable"] is True
        assert thr["per_erasure_count"][3]["recoverable"] is False
        assert thr["per_erasure_count"][4]["recoverable"] is False
        assert thr["threshold_qubits"] == 2
        assert abs(thr["threshold_fraction"] - 0.4) < 1e-15


# ---------------------------------------------------------------------------
# A5 — any 3-of-5 subregion reconstructs the logical qubit
# ---------------------------------------------------------------------------


class TestA5SubregionReconstruction:
    def test_every_3_subset_perfectly_distinguishes_logical_states(self):
        code = _code()
        subsets = list(itertools.combinations(range(N_QUBITS), 3))
        assert len(subsets) == 10
        for keep in subsets:
            rho0 = reduced_density_matrix(code.logical_zero, list(keep))
            rho1 = reduced_density_matrix(code.logical_one, list(keep))
            td = trace_distance(rho0, rho1)
            assert abs(td - 1.0) < TOL, (keep, td)

    def test_report_flag_computed(self):
        code = _code()
        report = code.subregion_reconstruction_report()
        assert report["n_subsets"] == 10
        assert abs(report["min_trace_distance"] - 1.0) < TOL
        assert report["all_reconstructable"] is True

    def test_contrast_2_subsets_carry_nothing(self):
        """Complementary contrast (consumes A4's physics): every 2-qubit
        subregion is informationless, so 3/5 is sharp, not slack."""
        code = _code()
        for keep in itertools.combinations(range(N_QUBITS), 2):
            rho0 = reduced_density_matrix(code.logical_zero, list(keep))
            rho1 = reduced_density_matrix(code.logical_one, list(keep))
            assert trace_distance(rho0, rho1) < TOL, keep


# ---------------------------------------------------------------------------
# Backward-compatible interfaces (HolographicCode / SubsystemCode)
# ---------------------------------------------------------------------------


class TestCompatInterfaces:
    def test_package_level_imports(self):
        from quantum import HolographicCode as HC, SubsystemCode as SC

        assert HC is HolographicCode
        assert SC is SubsystemCode

    def test_holographic_code_threshold_is_computed_2_of_5(self):
        hc = HolographicCode(n_physical=5, k_logical=1)
        result = hc.test_error_correction(seed=42)
        assert result["error_correction_threshold"] == 2
        assert abs(result["threshold_fraction"] - 0.4) < 1e-15
        by_count = {r["qubits_erased"]: r for r in result["erasure_tests"]}
        for k in (0, 1, 2):
            assert by_count[k]["is_recoverable"] is True
            assert by_count[k]["recovery_fidelity"] > 1.0 - 1e-9
        for k in (3, 4):
            assert by_count[k]["is_recoverable"] is False
            # (1 + T)/2 with T = 0: chance-level distinguishability.
            assert abs(by_count[k]["recovery_fidelity"] - 0.5) < TOL

    def test_holographic_code_rejects_fictional_parameters(self):
        """The old free-parameter constructor is gone: only the exact
        [[5,1,3]] code is claimed."""
        try:
            HolographicCode(n_physical=7, k_logical=1)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for n_physical=7")

    def test_subsystem_code_multiple_reconstructions(self):
        sc = SubsystemCode(n_boundary=5, n_bulk=1)
        result = sc.demonstrate_multiple_reconstructions()
        for region in ("left_half", "right_half", "even_qubits"):
            assert result[region]["is_recoverable"] is True
            assert result[region]["recovery_fidelity"] > 1.0 - 1e-9
            assert abs(result[region]["trace_distance"] - 1.0) < TOL
        # The 2-qubit region carries strictly zero logical information.
        assert result["odd_qubits"]["is_recoverable"] is False
        assert result["odd_qubits"]["trace_distance"] < TOL
        assert abs(result["odd_qubits"]["recovery_fidelity"] - 0.5) < TOL

    def test_full_analysis_headline_numbers_are_derived(self):
        """The headline string must carry the computed 2/5 threshold — and
        the computation, not the string, is what the tests trust."""
        code = _code()
        analysis = code.run_full_analysis()
        thr = analysis["erasure_threshold"]
        assert thr["threshold_qubits"] == 2
        assert f"{thr['threshold_qubits']}/{N_QUBITS}" in analysis["headline"]
        assert analysis["A2_single_qubit_errors"]["all_corrected"] is True
        assert analysis["A3_two_erasure"]["all_recovered"] is True
        assert analysis["A4_three_erasure_negative_control"]["information_absent"] is True
        assert analysis["A5_subregion_reconstruction"]["all_reconstructable"] is True
