"""
Quantum Error Correction as Spacetime Structure — the real [[5,1,3]] code.

History: this module was found defective by the 2026-08-15 adversarial review
(its advertised "80% erasure threshold" was the scan's loop bound at
near-chance fidelity — and recovery from >50% erasure is impossible by
no-cloning) and was reimplemented the same day as a genuine [[5,1,3]]
five-qubit stabilizer code per REAL_PHYSICS_REIMPLEMENTATION_MEMO.md Track A.

WHAT IS COMPUTED (all on explicit 32-dimensional statevectors):
- The five-qubit perfect code (Laflamme-Miquel-Paz-Zurek 1996):
  stabilizer generators XZZXI, IXZZX, XIXZZ, ZXIXZ (cyclic shifts of XZZXI),
  logical X̄ = XXXXX, Z̄ = ZZZZZ; codewords built by projecting |00000⟩ with
  Π(I + S_i)/2 and applying X̄.
- Syndrome table for all 15 single-qubit Pauli errors (16 distinct syndromes
  including the trivial one — the code is perfect), and syndrome-lookup
  correction of every single-qubit error.
- Known-location erasure decoding: for erased qubits at known positions,
  search the Pauli group restricted to the erased support for an operator
  matching the measured syndrome. Any 2-of-5 erasure is corrected exactly.
- Information-theoretic (un)recoverability via partial traces: the reduced
  states of logical |0̄⟩ and |1̄⟩ on any 2 qubits are IDENTICAL (trace
  distance 0 — a 3-erasure destroys the information; this is no-cloning at
  work, since 2 + 3 = 5 and two disjoint recoverable regions would clone the
  qubit), while on any 3 qubits they are PERFECTLY distinguishable (trace
  distance 1 — the entanglement-wedge/complementary-recovery structure of
  Almheiri-Dong-Harlow 2015 in its smallest exact instance).

  ARGUMENT SCOPE (2026-08-16): trace distance 1 between the marginals of |0̄⟩
  and |1̄⟩ certifies that the two LOGICAL BASIS STATES are perfectly
  distinguishable on that subregion. That is the diagonal half of the
  Knill-Laflamme condition, and it is NOT by itself reconstruction of an
  arbitrary logical state. The reconstruction claim is carried by the
  complement-erasure decoder implemented below, which recovers the full
  logical qubit; the result is right, the trace-distance argument alone was
  not sufficient to establish it.

Honest headline: erasure threshold 2/5 (40%); reconstruction from any
3/5 (60%) subregion. NOT 80% — that figure is retired.

SCOPE (2026-08-16). Two caveats the headline does not carry:
  * "Any 2-of-5 erasure is corrected exactly" is demonstrated for PAULI
    errors; the decoder raises rather than decoding for anything else.
  * 2/5 and 3/5 are not measured thresholds. They are d-1 and n-(d-1) for
    the [[5,1,3]] stabiliser set hardcoded here, i.e. textbook properties of
    any [[5,1,3]] code — only changing the code changes them. What the run
    establishes is that THIS implementation is faithful to that code, which
    is worth checking and is what the criteria asked for.

WHAT IS INTERPRETATION (not computed): the Advaita reading. Bulk/logical =
Brahman (protected information); boundary/physical = Maya (corruptible
surface); erasure = partial ignorance (Avidya); complementary recovery =
the same truth reachable from different perspectives. These are labeled
mappings onto the computed structure, not results.
"""

import itertools

import numpy as np

# ---------------------------------------------------------------------------
# Pauli algebra helpers
# ---------------------------------------------------------------------------

_PAULI = {
    "I": np.eye(2, dtype=np.complex128),
    "X": np.array([[0, 1], [1, 0]], dtype=np.complex128),
    "Y": np.array([[0, -1j], [1j, 0]], dtype=np.complex128),
    "Z": np.array([[1, 0], [0, -1]], dtype=np.complex128),
}

N_QUBITS = 5
DIM = 2 ** N_QUBITS  # 32

# Stabilizer generators: XZZXI and its cyclic shifts (the 5th shift is the
# product of these four, hence dependent and omitted).
STABILIZER_STRINGS = ("XZZXI", "IXZZX", "XIXZZ", "ZXIXZ")
LOGICAL_X_STRING = "XXXXX"
LOGICAL_Z_STRING = "ZZZZZ"


def pauli_string_operator(s: str) -> np.ndarray:
    """Dense operator for a Pauli string; char i acts on qubit i (qubit 0 =
    leftmost tensor factor = most significant bit of the state index)."""
    op = _PAULI[s[0]]
    for ch in s[1:]:
        op = np.kron(op, _PAULI[ch])
    return op


def strings_anticommute(p: str, q: str) -> bool:
    """Two Pauli strings anticommute iff they differ (both non-identity) on an
    odd number of positions — pure symplectic bookkeeping, no matrices."""
    count = sum(1 for a, b in zip(p, q) if a != "I" and b != "I" and a != b)
    return count % 2 == 1


def syndrome_of_pauli(error: str) -> tuple:
    """Syndrome bits of a Pauli string: bit i = 1 iff it anticommutes with
    stabilizer generator S_i."""
    return tuple(int(strings_anticommute(error, s)) for s in STABILIZER_STRINGS)


def reduced_density_matrix(state: np.ndarray, keep: list) -> np.ndarray:
    """Partial trace of |state⟩⟨state| keeping the qubits in `keep`
    (genuine partial trace via tensor reshape — not a matrix block)."""
    keep = sorted(keep)
    traced = [q for q in range(N_QUBITS) if q not in keep]
    psi = state.reshape([2] * N_QUBITS)
    psi = np.transpose(psi, keep + traced).reshape(2 ** len(keep), -1)
    return psi @ psi.conj().T


def trace_distance(rho: np.ndarray, sigma: np.ndarray) -> float:
    """T(ρ,σ) = ½‖ρ−σ‖₁ via eigenvalues of the Hermitian difference."""
    eigs = np.linalg.eigvalsh(rho - sigma)
    return float(0.5 * np.sum(np.abs(eigs)))


def von_neumann_entropy_bits(rho: np.ndarray) -> float:
    """Von Neumann entropy in bits (log base 2)."""
    eigs = np.real(np.linalg.eigvalsh(rho))
    eigs = eigs[eigs > 1e-15]
    return float(-np.sum(eigs * np.log2(eigs)))


# ---------------------------------------------------------------------------
# The [[5,1,3]] five-qubit perfect code
# ---------------------------------------------------------------------------


class FiveQubitCode:
    """The [[5,1,3]] five-qubit perfect code on explicit 32-dim statevectors.

    Encodes 1 logical qubit in 5 physical qubits with distance 3: corrects
    any single-qubit Pauli error (syndrome lookup) and any 2 erasures at
    known locations; any 3-qubit subregion carries the full logical qubit,
    any 2-qubit subregion carries none of it. All flags returned by the
    report methods are computed from the states — nothing is hardcoded.
    """

    def __init__(self):
        self.stabilizer_ops = [pauli_string_operator(s) for s in STABILIZER_STRINGS]
        self.logical_x = pauli_string_operator(LOGICAL_X_STRING)
        self.logical_z = pauli_string_operator(LOGICAL_Z_STRING)

        # |0̄⟩ ∝ Π (I + S_i)/2 |00000⟩ ; |1̄⟩ = X̄|0̄⟩
        ket0 = np.zeros(DIM, dtype=np.complex128)
        ket0[0] = 1.0
        for s_op in self.stabilizer_ops:
            ket0 = 0.5 * (ket0 + s_op @ ket0)
        self.logical_zero = ket0 / np.linalg.norm(ket0)
        self.logical_one = self.logical_x @ self.logical_zero

        # Syndrome table over the 15 single-qubit Paulis (+ identity),
        # built symbolically from anticommutation.
        self.single_qubit_errors = [
            "".join("I" if j != q else p for j in range(N_QUBITS))
            for q in range(N_QUBITS)
            for p in "XYZ"
        ]
        self.syndrome_table = {(0, 0, 0, 0): "IIIII"}
        for err in self.single_qubit_errors:
            self.syndrome_table[syndrome_of_pauli(err)] = err
        # Computed (not asserted-by-fiat): perfect code ⇒ 16 distinct syndromes.
        self.syndromes_all_distinct = len(self.syndrome_table) == 16

    # -- encoding ----------------------------------------------------------

    def encode(self, alpha: complex, beta: complex) -> np.ndarray:
        """Encode the logical state α|0̄⟩ + β|1̄⟩ (normalized)."""
        psi = alpha * self.logical_zero + beta * self.logical_one
        return psi / np.linalg.norm(psi)

    def reference_logical_states(self) -> dict:
        """Distinct encoded states used across the acceptance checks."""
        s = 1 / np.sqrt(2)
        return {
            "zero": self.encode(1.0, 0.0),
            "one": self.encode(0.0, 1.0),
            "plus": self.encode(s, s),
            "plus_i": self.encode(s, 1j * s),
        }

    # -- syndromes and correction ------------------------------------------

    def stabilizer_expectations(self, state: np.ndarray) -> list:
        """⟨ψ|S_i|ψ⟩ for the four generators (real parts)."""
        return [float(np.real(np.vdot(state, op @ state)))
                for op in self.stabilizer_ops]

    def measure_syndrome(self, state: np.ndarray) -> tuple:
        """Syndrome of a state that is a Pauli error applied to a codeword
        (each stabilizer expectation is then exactly ±1)."""
        bits = []
        for exp in self.stabilizer_expectations(state):
            if abs(exp - 1.0) < 1e-8:
                bits.append(0)
            elif abs(exp + 1.0) < 1e-8:
                bits.append(1)
            else:
                raise ValueError(
                    f"stabilizer expectation {exp:.6f} is not ±1; state is not "
                    "a definite syndrome eigenstate (non-Pauli noise?)"
                )
        return tuple(bits)

    def apply_pauli(self, state: np.ndarray, pauli_string: str) -> np.ndarray:
        return pauli_string_operator(pauli_string) @ state

    def correct(self, state: np.ndarray) -> dict:
        """Syndrome-lookup correction for (at most) a single-qubit Pauli error.

        Measures the syndrome, looks up the unique single-qubit Pauli with
        that syndrome, and applies it (Paulis are involutions).
        """
        syndrome = self.measure_syndrome(state)
        error = self.syndrome_table.get(syndrome)
        if error is None:  # unreachable for a perfect code, kept for honesty
            return {"syndrome": syndrome, "error_identified": None,
                    "corrected_state": state, "correction_applied": False}
        corrected = self.apply_pauli(state, error)
        return {
            "syndrome": syndrome,
            "error_identified": error,
            "corrected_state": corrected,
            "correction_applied": True,
        }

    def decode_erasure(self, state: np.ndarray, erased: tuple) -> dict:
        """Known-location erasure decoding, restricted to the erased support.

        Searches the 4^|erased| Pauli operators supported on the erased qubits
        for one matching the measured syndrome. For |erased| ≤ 2 the match is
        unique up to a stabilizer (distance 3 ⇒ no nontrivial logical of
        weight ≤ 2 ⇒ candidates with equal syndrome act identically on the
        codespace), so decoding is exact.
        """
        syndrome = self.measure_syndrome(state)
        erased = tuple(sorted(erased))
        for letters in itertools.product("IXYZ", repeat=len(erased)):
            candidate = ["I"] * N_QUBITS
            for pos, letter in zip(erased, letters):
                candidate[pos] = letter
            candidate = "".join(candidate)
            if syndrome_of_pauli(candidate) == syndrome:
                return {
                    "syndrome": syndrome,
                    "correction": candidate,
                    "corrected_state": self.apply_pauli(state, candidate),
                    "decoded": True,
                }
        return {"syndrome": syndrome, "correction": None,
                "corrected_state": state, "decoded": False}

    @staticmethod
    def fidelity(psi: np.ndarray, phi: np.ndarray) -> float:
        """|⟨ψ|φ⟩|² for pure states (global-phase insensitive)."""
        return float(abs(np.vdot(psi, phi)) ** 2)

    # -- acceptance-criterion computations (A1–A5) --------------------------

    def codeword_stabilizer_check(self) -> dict:
        """A1: encoded states are +1 eigenstates of all four stabilizers."""
        max_dev = 0.0
        for psi in self.reference_logical_states().values():
            for exp in self.stabilizer_expectations(psi):
                max_dev = max(max_dev, abs(exp - 1.0))
        return {
            "max_eigenvalue_deviation": max_dev,
            "all_plus_one_eigenstates": max_dev < 1e-10,
        }

    def single_error_correction_report(self) -> dict:
        """A2: every single-qubit Pauli error is corrected by syndrome lookup,
        for several distinct logical states."""
        min_fid = 1.0
        n_cases = 0
        for psi in self.reference_logical_states().values():
            for err in self.single_qubit_errors:
                noisy = self.apply_pauli(psi, err)
                result = self.correct(noisy)
                min_fid = min(min_fid, self.fidelity(psi, result["corrected_state"]))
                n_cases += 1
        return {
            "n_cases": n_cases,
            "min_fidelity": min_fid,
            "all_corrected": min_fid > 1.0 - 1e-10,
            "syndromes_all_distinct": self.syndromes_all_distinct,
        }

    def two_erasure_report(self, seed: int = 42, n_random_draws: int = 3) -> dict:
        """A3: every 2-of-5 known-location erasure is recovered exactly.

        Exhausts all 16 Pauli noise operators on each of the 10 erased pairs
        (which covers any random Pauli draw) and additionally decodes seeded
        random draws, per the memo's wording.
        """
        rng = np.random.default_rng(seed)
        pairs = list(itertools.combinations(range(N_QUBITS), 2))
        states = self.reference_logical_states()
        min_fid = 1.0
        n_cases = 0
        for name, psi in states.items():
            for pair in pairs:
                # Exhaustive over the pair-supported Pauli group.
                for letters in itertools.product("IXYZ", repeat=2):
                    noise = ["I"] * N_QUBITS
                    noise[pair[0]], noise[pair[1]] = letters
                    noisy = self.apply_pauli(psi, "".join(noise))
                    out = self.decode_erasure(noisy, pair)
                    min_fid = min(min_fid, self.fidelity(psi, out["corrected_state"]))
                    n_cases += 1
                # Seeded random draws (memo wording: random Pauli noise).
                for _ in range(n_random_draws):
                    letters = rng.choice(list("IXYZ"), size=2)
                    noise = ["I"] * N_QUBITS
                    noise[pair[0]], noise[pair[1]] = letters
                    noisy = self.apply_pauli(psi, "".join(noise))
                    out = self.decode_erasure(noisy, pair)
                    min_fid = min(min_fid, self.fidelity(psi, out["corrected_state"]))
                    n_cases += 1
        return {
            "n_patterns": len(pairs),
            "n_cases": n_cases,
            "min_fidelity": min_fid,
            "all_recovered": min_fid > 1.0 - 1e-10,
        }

    def three_erasure_negative_control(self) -> dict:
        """A4 (negative control): a 3-erasure is UNRECOVERABLE — the reduced
        states of |0̄⟩ and |1̄⟩ on the surviving 2 qubits are identical for
        every 3-erasure pattern. Recovery here would violate no-cloning
        (2 survivors + 3 erased = 5; two disjoint recoverable regions would
        clone the logical qubit)."""
        max_td = 0.0
        patterns = list(itertools.combinations(range(N_QUBITS), 3))
        for erased in patterns:
            survivors = [q for q in range(N_QUBITS) if q not in erased]
            rho0 = reduced_density_matrix(self.logical_zero, survivors)
            rho1 = reduced_density_matrix(self.logical_one, survivors)
            max_td = max(max_td, trace_distance(rho0, rho1))
        return {
            "n_patterns": len(patterns),
            "max_trace_distance_on_survivors": max_td,
            "information_absent": max_td < 1e-10,
        }

    def subregion_reconstruction_report(self) -> dict:
        """A5: every 3-of-5 subregion carries the full logical qubit — the
        reduced states of |0̄⟩ and |1̄⟩ on each 3-qubit subset are perfectly
        distinguishable (trace distance 1)."""
        min_td = 1.0
        subsets = list(itertools.combinations(range(N_QUBITS), 3))
        for keep in subsets:
            rho0 = reduced_density_matrix(self.logical_zero, list(keep))
            rho1 = reduced_density_matrix(self.logical_one, list(keep))
            min_td = min(min_td, trace_distance(rho0, rho1))
        return {
            "n_subsets": len(subsets),
            "min_trace_distance": min_td,
            "all_reconstructable": abs(min_td - 1.0) < 1e-10,
        }

    def erasure_threshold(self) -> dict:
        """Computed erasure threshold: the largest k such that EVERY
        k-erasure pattern leaves the survivors with full distinguishability
        (trace distance 1) between the logical basis states. Necessity is
        information-theoretic; sufficiency for k ≤ 2 is demonstrated
        constructively by `two_erasure_report`."""
        threshold = 0
        per_k = {}
        for k in range(1, N_QUBITS):
            min_td = 1.0
            for erased in itertools.combinations(range(N_QUBITS), k):
                survivors = [q for q in range(N_QUBITS) if q not in erased]
                rho0 = reduced_density_matrix(self.logical_zero, survivors)
                rho1 = reduced_density_matrix(self.logical_one, survivors)
                min_td = min(min_td, trace_distance(rho0, rho1))
            recoverable = abs(min_td - 1.0) < 1e-10
            per_k[k] = {"min_trace_distance_on_survivors": min_td,
                        "recoverable": recoverable}
            if recoverable:
                threshold = k
        return {
            "per_erasure_count": per_k,
            "threshold_qubits": threshold,
            "threshold_fraction": threshold / N_QUBITS,
        }

    def run_full_analysis(self) -> dict:
        """All five acceptance computations plus the honest headline."""
        a1 = self.codeword_stabilizer_check()
        a2 = self.single_error_correction_report()
        a3 = self.two_erasure_report()
        a4 = self.three_erasure_negative_control()
        a5 = self.subregion_reconstruction_report()
        thr = self.erasure_threshold()
        return {
            "A1_stabilizer_eigenstates": a1,
            "A2_single_qubit_errors": a2,
            "A3_two_erasure": a3,
            "A4_three_erasure_negative_control": a4,
            "A5_subregion_reconstruction": a5,
            "erasure_threshold": thr,
            "headline": (
                f"[[5,1,3]] code: erasure threshold "
                f"{thr['threshold_qubits']}/{N_QUBITS} "
                f"({thr['threshold_fraction']:.0%}); logical qubit "
                f"reconstructable from any 3/5 (60%) subregion. "
                f"The former '80%' figure is retired."
            ),
        }


# ---------------------------------------------------------------------------
# Backward-compatible interfaces (names imported by quantum/__init__ and
# main.py). Same class names and return keys, now backed by the real code.
# ---------------------------------------------------------------------------


class HolographicCode(FiveQubitCode):
    """Holographic-code interface backed by the real [[5,1,3]] code.

    Almheiri-Dong-Harlow (2015): the holographic dictionary has the structure
    of a quantum error-correcting code — bulk operators = logical qubits,
    boundary operators = physical qubits, and the bulk is robust against
    boundary erasure. The five-qubit code is the smallest exact model of
    that structure. The Advaita mapping (Brahman = bulk/logical, Maya =
    boundary/physical, Avidya = erasure) is interpretation layered on the
    computed results, and is labeled as such in the returned dicts.
    """

    def __init__(self, n_physical: int = 5, k_logical: int = 1):
        if (n_physical, k_logical) != (5, 1):
            raise ValueError(
                "HolographicCode now implements the exact [[5,1,3]] code; "
                f"only n_physical=5, k_logical=1 is supported "
                f"(got n_physical={n_physical}, k_logical={k_logical})."
            )
        super().__init__()
        self.n = 5
        self.k = 1
        self.code_distance = 3  # actual distance of the [[5,1,3]] code
        self.max_erasure = 2    # known-location erasures correctable (= d − 1)

    def test_error_correction(self, logical_state: np.ndarray = None,
                              seed: int = 42) -> dict:
        """Erasure analysis at every erasure level 0..4.

        For ≤ 2 erasures: constructive syndrome decoding of seeded random
        Pauli noise on the erased qubits (fidelity computed against the
        original encoded state). For ≥ 3 erasures no decoder exists; the
        reported figure is the optimal probability of even distinguishing
        |0̄⟩ from |1̄⟩ using the survivors, (1 + T)/2 with T the computed
        trace distance — 0.5 means chance.
        """
        if logical_state is None:
            logical_state = np.array([1.0, 1.0], dtype=np.complex128) / np.sqrt(2)
        logical_state = np.asarray(logical_state, dtype=np.complex128)
        psi = self.encode(logical_state[0], logical_state[1])
        rng = np.random.default_rng(seed)

        results = []
        for num_erase in range(N_QUBITS):
            erased = tuple(range(num_erase))
            survivors = [q for q in range(N_QUBITS) if q not in erased]
            rho0 = reduced_density_matrix(self.logical_zero, survivors)
            rho1 = reduced_density_matrix(self.logical_one, survivors)
            td = trace_distance(rho0, rho1)

            if num_erase <= self.max_erasure:
                # Constructive recovery under random Pauli noise on the
                # erased qubits (worst case over several seeded draws).
                fid = 1.0
                draws = 5 if num_erase > 0 else 1
                for _ in range(draws):
                    noise = ["I"] * N_QUBITS
                    for q in erased:
                        noise[q] = str(rng.choice(list("IXYZ")))
                    noisy = self.apply_pauli(psi, "".join(noise))
                    out = self.decode_erasure(noisy, erased)
                    fid = min(fid, self.fidelity(psi, out["corrected_state"]))
                mode = "syndrome decoding (constructive)"
            else:
                # No decoder: best distinguishing probability from survivors.
                fid = 0.5 * (1.0 + td)
                mode = "optimal distinguishability bound (1 + T)/2"

            results.append({
                "qubits_erased": num_erase,
                "fraction_erased": num_erase / N_QUBITS,
                "recovery_fidelity": fid,
                "recovery_mode": mode,
                "survivor_trace_distance": td,
                "is_recoverable": fid > 1.0 - 1e-9,
                "maya_interpretation": (
                    "No ignorance" if num_erase == 0 else
                    f"Partial ignorance ({num_erase}/{N_QUBITS} of Maya erased)"
                ),
            })

        threshold = 0
        for r in results:
            if r["is_recoverable"]:
                threshold = r["qubits_erased"]

        return {
            "code_parameters": {
                "n_physical": self.n,
                "k_logical": self.k,
                "code_distance": self.code_distance,
                "max_correctable_erasure": self.max_erasure,
            },
            "erasure_tests": results,
            "error_correction_threshold": threshold,
            "threshold_fraction": threshold / self.n,
            "insight": (
                f"The [[5,1,3]] code protects {self.k} logical qubit in "
                f"{self.n} physical qubits. Recovery is exact for up to "
                f"{threshold}/{self.n} ({threshold / self.n:.0%}) erased "
                f"qubits at known locations; at 3+ erasures the surviving "
                f"qubits' reduced states for |0̄⟩ and |1̄⟩ coincide (trace "
                f"distance 0), so the information is genuinely absent — "
                f"no-cloning forbids doing better. Interpretation: the bulk "
                f"(Brahman) is protected from limited boundary ignorance "
                f"(Maya/Avidya), but the protection has a hard threshold."
            ),
        }

    def demonstrate_spacetime_as_code(self) -> dict:
        """Distinguishability and entanglement structure of the codewords,
        computed via genuine partial traces on the 32-dim codewords."""
        ec_test = self.test_error_correction()

        # Orthogonal codewords stay perfectly distinguishable after a
        # single-qubit erasure (trace distance on the 4 survivors).
        overlap = float(abs(np.vdot(self.logical_zero, self.logical_one)))
        survivors = [1, 2, 3, 4]  # qubit 0 erased
        rho0 = reduced_density_matrix(self.logical_zero, survivors)
        rho1 = reduced_density_matrix(self.logical_one, survivors)
        td_after = trace_distance(rho0, rho1)
        overlap_after = float(np.real(np.trace(rho0 @ rho1)))

        # Codeword entanglement: every 2-qubit reduced state of a codeword is
        # maximally mixed (2 bits) — the same fact that makes 2 qubits
        # carry zero logical information.
        rho_2q = reduced_density_matrix(self.logical_zero, [0, 1])
        ent_bits = von_neumann_entropy_bits(rho_2q)

        return {
            "error_correction": ec_test,
            "distinguishability": {
                "logical_overlap": overlap,
                "physical_overlap_after_erasure": overlap_after,
                "survivor_trace_distance": td_after,
                "states_still_distinguishable": abs(td_after - 1.0) < 1e-10,
            },
            "entanglement_structure": {
                "codeword_entanglement": ent_bits,  # bits, 2-qubit marginal
                "highly_entangled": ent_bits > 1.9,
                "note": (
                    "Every 2-qubit marginal of a codeword is exactly "
                    "maximally mixed (2.0 bits) — this computed fact is "
                    "simultaneously why the code corrects errors and why "
                    "small regions carry no logical information. "
                    "Interpretation: entanglement (non-duality) is the "
                    "mechanism of robustness."
                ),
            },
            "advaita_mapping": {
                "bulk_brahman": "Logical qubit — the protected information "
                                "(interpretive label)",
                "boundary_maya": "Physical qubits — the accessible, "
                                 "corruptible surface (interpretive label)",
                "error_correction": "Recovery despite ≤ 2/5 erasure — "
                                    "computed above",
                "entanglement": "Maximally mixed small marginals — computed "
                                "above; 'non-duality = robustness' is the "
                                "interpretation",
                "threshold": (
                    f"{ec_test['threshold_fraction']:.0%} of the boundary is "
                    "erasable with exact recovery; beyond that the "
                    "information is provably absent (no-cloning)."
                ),
            },
            "physics_significance": (
                "The [[5,1,3]] code is the smallest exact instance of the "
                "Almheiri-Dong-Harlow observation that bulk information can "
                "be protected against boundary erasure, with complementary "
                "recovery from any 3/5 subregion. Whether real spacetime "
                "works this way is a conjecture of the holographic program, "
                "not something this module demonstrates."
            ),
        }


class SubsystemCode:
    """Complementary recovery from boundary subregions, on the real code.

    Entanglement-wedge-style statement made exact: any 3-of-5 subregion of
    the [[5,1,3]] code determines the logical qubit completely (survivor
    trace distance 1 between |0̄⟩ and |1̄⟩, and the complement — being ≤ 2
    qubits — is a correctable erasure, which is the operational meaning of
    'the subregion suffices'); any ≤ 2-qubit subregion determines nothing.
    The Advaita reading (many perspectives, one truth) is interpretation.
    """

    def __init__(self, n_boundary: int = 5, n_bulk: int = 1):
        if (n_boundary, n_bulk) != (5, 1):
            raise ValueError(
                "SubsystemCode now demonstrates subregion reconstruction on "
                "the exact [[5,1,3]] code; only n_boundary=5, n_bulk=1 is "
                f"supported (got n_boundary={n_boundary}, n_bulk={n_bulk})."
            )
        self.n_boundary = 5
        self.n_bulk = 1
        self.code = FiveQubitCode()

    def reconstruct_from_subregion(self, subregion_qubits: list) -> dict:
        """Computed reconstructability of the logical qubit from a subregion.

        - trace_distance: T between the reduced states of |0̄⟩ and |1̄⟩ on
          the subregion (1 = perfectly distinguishable, 0 = no information).
        - recovery_fidelity: if the complement is a correctable erasure
          (≤ 2 qubits), the worst-case constructive decode fidelity over ALL
          Pauli noise on the complement (exact recovery ⇒ 1.0); otherwise
          the optimal distinguishing probability (1 + T)/2 (0.5 = chance).
        """
        subregion = sorted(set(subregion_qubits))
        complement = [q for q in range(N_QUBITS) if q not in subregion]
        rho0 = reduced_density_matrix(self.code.logical_zero, subregion)
        rho1 = reduced_density_matrix(self.code.logical_one, subregion)
        td = trace_distance(rho0, rho1)

        if len(complement) <= 2:
            fid = 1.0
            for psi in self.code.reference_logical_states().values():
                for letters in itertools.product("IXYZ", repeat=len(complement)):
                    noise = ["I"] * N_QUBITS
                    for pos, letter in zip(complement, letters):
                        noise[pos] = letter
                    noisy = self.code.apply_pauli(psi, "".join(noise))
                    out = self.code.decode_erasure(noisy, tuple(complement))
                    fid = min(fid, self.code.fidelity(psi, out["corrected_state"]))
            mode = "complement-erasure decoding (constructive)"
        else:
            fid = 0.5 * (1.0 + td)
            mode = "optimal distinguishability bound (1 + T)/2"

        return {
            "subregion": subregion,
            "subregion_fraction": len(subregion) / self.n_boundary,
            "trace_distance": td,
            "recovery_fidelity": fid,
            "recovery_mode": mode,
            "is_recoverable": fid > 1.0 - 1e-9,
        }

    def demonstrate_multiple_reconstructions(self) -> dict:
        """The same logical qubit reconstructed from several distinct 3-qubit
        subregions — and NOT from a 2-qubit one (computed contrast)."""
        results = {
            "left_half": self.reconstruct_from_subregion([0, 1, 2]),
            "right_half": self.reconstruct_from_subregion([2, 3, 4]),
            "even_qubits": self.reconstruct_from_subregion([0, 2, 4]),
            "odd_qubits": self.reconstruct_from_subregion([1, 3]),
        }
        results["insight"] = (
            "Any 3-of-5 subregion reconstructs the logical qubit exactly "
            "(complement is a correctable 2-erasure); the 2-qubit subregion "
            "carries strictly zero logical information (trace distance 0) — "
            "both facts computed above. Interpretation: the same bulk truth "
            "(Brahman) is reachable from many boundary perspectives, but a "
            "perspective can also be too narrow to reach it at all."
        )
        return results
