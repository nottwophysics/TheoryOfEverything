"""
Gleason's Theorem — consistency checks of the trivial direction

Andrew Gleason (1957) proved:

    In a Hilbert space H of dimension ≥ 3, every non-negative,
    countably additive frame function (probability measure on
    closed subspaces) is of the form:

        μ(P) = Tr(ρ P)

    for some density operator ρ (positive, trace-1, Hermitian).

For pure states ρ = |ψ⟩⟨ψ|, this gives:

    P(outcome n) = Tr(|ψ⟩⟨ψ| · |n⟩⟨n|) = |⟨n|ψ⟩|²

REVIEW LABEL (2026-08-15) — read this before quoting anything from here.

Gleason's theorem has an easy direction and a hard direction:

    EASY  (every density operator ρ yields a frame function):
          Tr(ρP) ≥ 0, additivity on orthogonal projectors, and Tr(ρI) = 1
          hold for EVERY density matrix in EVERY dimension — non-negativity
          because ρ ⪰ 0 and P ⪰ 0, additivity because the trace is linear,
          normalisation by construction.  Nothing about "dim ≥ 3" or about
          this particular Hilbert space is involved.

    HARD  (every frame function comes from some density operator):
          this is Gleason's actual theorem.  It quantifies over ALL frame
          functions, so no finite computation can establish it, and this
          module does not attempt to.  It is CITED, not proved.

Everything computed in this file lives on the easy side.  ``verify_conditions``
is a consistency check that the implementation computes Tr(ρP) correctly —
it cannot fail for a valid density matrix, and it is NOT a verification that
Gleason's hypotheses "hold for the Brahman Hilbert space" in any nontrivial
sense.  ``demonstrate_uniqueness`` refutes two specific alternative rules on
one state; that is not a uniqueness proof.  ``axiom_count_bookkeeping``
tabulates hand-entered axiom counts; that is bookkeeping, not mathematics.

The framework's substantive claim — that treating the Born rule as a theorem
via Gleason lets A5 be dropped as an independent axiom — is an argument that
rests on the CITED theorem plus the framework's own axiomatisation.  Its open
question (why a frame function should be interpreted as a probability of
experienced outcomes at all) is discussed in docs/GLEASON_PROBABILITY_GAP.md,
which this module does not supersede.

HISTORY: before the 2026-08-15 review this module described itself as
"verifying Gleason's conditions", "demonstrating that no other probability
rule is consistent" and "proving the axiom count reduction is legitimate".
All three were overclaims and have been relabelled; the computations
themselves are unchanged and still run.

Significance for this framework (framework's own position, not a result here):
    - Copenhagen ASSUMES the Born rule as axiom A5
    - Pilot Wave ASSUMES quantum equilibrium as axiom A4
    - Many-Worlds attempts to DERIVE Born rule (controversial)
    - Advaita: Born rule is taken as a THEOREM via Gleason, reducing the
      framework's stated axiom count

This module:
    1. Consistency-checks μ(P) = Tr(ρP) against C1–C4 (the easy direction)
    2. Refutes two sampled non-Born ray rules on one state
    3. Exhibits one dispersion-free assignment failing in dim 3
    4. Tabulates the framework's axiom bookkeeping
"""

import numpy as np
from itertools import combinations


class GleasonVerification:
    """
    Consistency checks on the measure μ(P) = Tr(ρP) in dimension ``dimension``,
    plus the framework's axiom bookkeeping.

    Gleason's conditions:
        C1: H has dimension ≥ 3
        C2: The measure μ is non-negative: μ(P) ≥ 0 for all projectors P
        C3: The measure is additive on orthogonal projectors:
            if P₁ ⊥ P₂ then μ(P₁ + P₂) = μ(P₁) + μ(P₂)
        C4: μ(I) = 1 (total probability = 1)

    If C1–C4 hold for an ARBITRARY frame function μ, then Gleason's theorem
    says μ must be of the form Tr(ρP).  This class does the converse and
    trivial thing: it starts from a density matrix ρ, builds μ(P) = Tr(ρP),
    and checks C2–C4 numerically — which they satisfy automatically, in any
    dimension.  See the module docstring: the class name is historical and
    "Verification" here means "implementation consistency check", not
    "verification of Gleason's theorem".
    """

    def __init__(self, dimension: int = 4):
        if dimension < 3:
            raise ValueError(
                "Gleason's theorem requires dimension ≥ 3. "
                "This is why qubits (dim=2) can have non-Born measures, "
                "but the full consciousness field (dim≥3) cannot."
            )
        self.dim = dimension

    def verify_conditions(self, state: np.ndarray = None) -> dict:
        """
        Consistency-check C1–C4 for the measure μ(P) = Tr(ρP) built from a
        single state.

        NOT a proof of Gleason's theorem, and not a nontrivial fact about
        this Hilbert space:

          * C2 (non-negativity) holds for every density matrix in every
            dimension, because ρ ⪰ 0 and P ⪰ 0 ⟹ Tr(ρP) ≥ 0.
          * C3 (additivity) is linearity of the trace; it holds identically,
            for orthogonal projectors and for any other matrices.
          * C4 is Tr(ρ) = 1, true by construction from a normalised state.
          * Only C1 (dim ≥ 3) says anything about the space, and it is a
            comparison of a constructor argument against 3.

        So a "PASS" here means the code computes Tr(ρP) correctly. A failure
        would indicate a bug, not a physics result. The method name is kept
        because main.py and tests/test_quantum.py call it.
        """
        if state is None:
            # Brahman state: equal superposition
            state = np.ones(self.dim, dtype=np.complex128) / np.sqrt(self.dim)

        rho = np.outer(state, state.conj())

        # C1: Dimension check
        c1 = self.dim >= 3

        # C2: Non-negativity — Tr(ρP) ≥ 0 for all rank-1 projectors
        c2_violations = 0
        num_tests = 500
        np.random.seed(42)
        for _ in range(num_tests):
            v = np.random.randn(self.dim) + 1j * np.random.randn(self.dim)
            v /= np.linalg.norm(v)
            P = np.outer(v, v.conj())
            prob = float(np.real(np.trace(rho @ P)))
            if prob < -1e-10:
                c2_violations += 1
        c2 = c2_violations == 0

        # C3: Additivity on orthogonal projectors
        c3_violations = 0
        num_tests_c3 = 200
        for _ in range(num_tests_c3):
            # Generate random orthonormal pair
            v1 = np.random.randn(self.dim) + 1j * np.random.randn(self.dim)
            v1 /= np.linalg.norm(v1)
            v2 = np.random.randn(self.dim) + 1j * np.random.randn(self.dim)
            v2 = v2 - np.dot(v1.conj(), v2) * v1  # Gram-Schmidt
            if np.linalg.norm(v2) < 1e-10:
                continue
            v2 /= np.linalg.norm(v2)

            P1 = np.outer(v1, v1.conj())
            P2 = np.outer(v2, v2.conj())
            P12 = P1 + P2

            mu_P1 = float(np.real(np.trace(rho @ P1)))
            mu_P2 = float(np.real(np.trace(rho @ P2)))
            mu_P12 = float(np.real(np.trace(rho @ P12)))

            if abs(mu_P12 - (mu_P1 + mu_P2)) > 1e-8:
                c3_violations += 1
        c3 = c3_violations == 0

        # C4: Normalization — Tr(ρI) = 1
        c4_value = float(np.real(np.trace(rho)))
        c4 = abs(c4_value - 1.0) < 1e-10

        all_satisfied = c1 and c2 and c3 and c4

        return {
            "C1_dimension_ge_3": {
                "satisfied": c1,
                "dimension": self.dim,
                "note": "Gleason requires dim ≥ 3. Qubits (dim=2) are the exception. "
                        "(Checked by comparing the constructor argument to 3.)",
            },
            "C2_non_negativity": {
                "satisfied": c2,
                "tests_run": num_tests,
                "violations": c2_violations,
                "note": "Tr(ρP) ≥ 0 for all projectors P tested. TRIVIAL DIRECTION: "
                        "true for every density matrix in every dimension "
                        "(ρ ⪰ 0, P ⪰ 0). This checks the implementation.",
            },
            "C3_additivity": {
                "satisfied": c3,
                "tests_run": num_tests_c3,
                "violations": c3_violations,
                "note": "μ(P₁+P₂) = μ(P₁) + μ(P₂) for orthogonal P₁ ⊥ P₂. TRIVIAL "
                        "DIRECTION: this is linearity of the trace, which holds "
                        "identically. This checks the implementation.",
            },
            "C4_normalization": {
                "satisfied": c4,
                "trace_rho": c4_value,
                "note": "Total probability = Tr(ρ) = 1, true by construction from "
                        "a normalised state.",
            },
            "all_conditions_satisfied": all_satisfied,
            "what_is_checked": (
                "That the measure μ(P) = Tr(ρP) implemented here satisfies C1–C4. "
                "C2–C4 are automatic for any density matrix in any dimension, so "
                "this is a consistency check of the code, i.e. of the EASY "
                "direction of Gleason's theorem (every density operator gives a "
                "frame function)."
            ),
            "what_is_not_checked": (
                "The HARD direction — that every frame function on a Hilbert "
                "space of dim ≥ 3 is of the form Tr(ρP). That is Gleason's actual "
                "theorem; it quantifies over all frame functions, so no finite "
                "computation can establish it, and none is attempted here."
            ),
            "gleason_theorem_status": "cited (Gleason 1957), not proved by this module",
            "conclusion": (
                "μ(P) = Tr(ρP) satisfies C1–C4 here — as it must: C2–C4 hold for "
                "every density matrix in every dimension, so this is a consistency "
                "check of the trivial direction, not a nontrivial fact about this "
                "Hilbert space. Gleason's theorem itself (the converse: every frame "
                "function is Tr(ρP) when dim ≥ 3) is a cited 1957 result and is not "
                "proved here. The framework's use of it — treating the Born rule as "
                "a theorem rather than an axiom — is an argument built on that "
                "citation, not on this computation. See "
                "docs/GLEASON_PROBABILITY_GAP.md for the remaining gap."
                if all_satisfied else
                "The C1–C4 consistency check FAILED, which indicates a bug in the "
                "construction of ρ or of μ, not a physics result."
            ),
        }

    def demonstrate_uniqueness(self, state: np.ndarray = None) -> dict:
        """
        Refute TWO sampled non-Born ray rules on ONE state. Not a uniqueness proof.

        Scope, stated plainly (2026-08-15 relabel):
          * Two specific alternatives are tested — the amplitude rule
            |⟨n|ψ⟩| and the quartic rule |⟨n|ψ⟩|⁴, each renormalised — on a
            single state, over randomly sampled orthonormal pairs. Finding
            violations refutes those two rules here; it says nothing about
            the infinitely many rules not sampled.
          * The reference value used for the 2-D subspace is ‖P_ij ψ‖², i.e.
            the BORN weight of the subspace. So the comparison presupposes
            Born on subspaces and shows the ray rules are inconsistent with
            the projection weight — it is not a self-contained refutation.
          * Genuine uniqueness is Gleason's theorem, cited, not established
            by sampling.
        """
        if state is None:
            state = np.ones(self.dim, dtype=np.complex128) / np.sqrt(self.dim)

        rho = np.outer(state, state.conj())

        # Generate a complete orthonormal basis
        basis = np.eye(self.dim, dtype=np.complex128)

        # Born rule probabilities
        born_probs = np.array([
            float(np.real(np.trace(rho @ np.outer(basis[i], basis[i].conj()))))
            for i in range(self.dim)
        ])

        # Alternative 1: Uniform distribution (equal probability for all outcomes)
        uniform_probs = np.ones(self.dim) / self.dim

        # Alternative 2: Amplitude rule (P = |⟨n|ψ⟩|, not |⟨n|ψ⟩|²)
        amplitudes = np.array([float(abs(np.dot(basis[i].conj(), state)))
                               for i in range(self.dim)])
        amp_total = np.sum(amplitudes)
        amplitude_probs = amplitudes / amp_total if amp_total > 0 else amplitudes

        # Alternative 3: Quartic rule (P = |⟨n|ψ⟩|⁴ normalized)
        quartic = np.array([float(abs(np.dot(basis[i].conj(), state)) ** 4)
                            for i in range(self.dim)])
        q_total = np.sum(quartic)
        quartic_probs = quartic / q_total if q_total > 0 else quartic

        # Test additivity (C3) for each rule
        def test_additivity(prob_func, name):
            """Test if a probability rule satisfies additivity on orthogonal projectors."""
            violations = 0
            total_tests = 0
            max_violation = 0.0

            np.random.seed(42)
            for _ in range(300):
                # Random orthonormal basis
                A = np.random.randn(self.dim, self.dim) + 1j * np.random.randn(self.dim, self.dim)
                Q, _ = np.linalg.qr(A)

                for i in range(self.dim):
                    for j in range(i + 1, self.dim):
                        P_i = np.outer(Q[:, i], Q[:, i].conj())
                        P_j = np.outer(Q[:, j], Q[:, j].conj())
                        P_ij = P_i + P_j

                        mu_i = prob_func(Q[:, i])
                        mu_j = prob_func(Q[:, j])
                        mu_ij = prob_func(Q[:, i]) + prob_func(Q[:, j])
                        # For the combined subspace, we need the projection probability
                        mu_ij_direct = float(np.real(
                            state.conj() @ P_ij @ state
                        )) if name == "born" else mu_i + mu_j

                        total_tests += 1
                        if name == "born":
                            violation = abs(mu_ij_direct - (mu_i + mu_j))
                        else:
                            # For non-Born rules, compute probability of 2D subspace directly
                            proj_state = P_ij @ state
                            proj_norm_sq = float(np.real(np.dot(proj_state.conj(), proj_state)))
                            rule_sum = mu_i + mu_j
                            violation = abs(proj_norm_sq - rule_sum)

                        if violation > 1e-6:
                            violations += 1
                        max_violation = max(max_violation, violation)

            return {
                "name": name,
                "tests": total_tests,
                "violations": violations,
                "max_violation": float(max_violation),
                "satisfies_additivity": violations == 0,
            }

        born_func = lambda v: float(abs(np.dot(v.conj(), state)) ** 2)
        amp_func = lambda v: float(abs(np.dot(v.conj(), state))) / amp_total
        quartic_func = lambda v: float(abs(np.dot(v.conj(), state)) ** 4) / q_total

        born_test = test_additivity(born_func, "born")
        amp_test = test_additivity(amp_func, "amplitude")
        quartic_test = test_additivity(quartic_func, "quartic")

        return {
            "born_rule": {
                "probabilities": born_probs.tolist(),
                "sums_to_one": abs(np.sum(born_probs) - 1.0) < 1e-10,
                "additivity": born_test,
            },
            "alternative_uniform": {
                "probabilities": uniform_probs.tolist(),
                "sums_to_one": True,
                "problem": "Ignores the state — same probabilities for every |ψ⟩. "
                           "Violates the requirement that μ depends on ρ.",
            },
            "alternative_amplitude": {
                "probabilities": amplitude_probs.tolist(),
                "sums_to_one": abs(np.sum(amplitude_probs) - 1.0) < 1e-10,
                "additivity": amp_test,
            },
            "alternative_quartic": {
                "probabilities": quartic_probs.tolist(),
                "sums_to_one": abs(np.sum(quartic_probs) - 1.0) < 1e-10,
                "additivity": quartic_test,
            },
            "scope": (
                "Two sampled alternatives on one state. Refutes those two; it is "
                "NOT a uniqueness proof, and the 2-D subspace reference value is "
                "itself the Born weight ‖P_ij ψ‖²."
            ),
            "conclusion": (
                f"Born rule: additivity satisfied = {born_test['satisfies_additivity']}. "
                f"Amplitude rule: additivity satisfied = {amp_test['satisfies_additivity']} "
                f"(max violation: {amp_test['max_violation']:.6f}). "
                f"Quartic rule: additivity satisfied = {quartic_test['satisfies_additivity']} "
                f"(max violation: {quartic_test['max_violation']:.6f}). "
                "Read this as: the two sampled non-Born ray rules disagree with the "
                "projection weight on this state. Uniqueness in dim ≥ 3 is Gleason's "
                "theorem (cited), not a conclusion of this sampling."
            ),
        }

    def demonstrate_dim2_exception(self) -> dict:
        """
        Exhibit ONE dispersion-free assignment: consistent on one dim-2 basis,
        failing on random dim-3 bases.

        Scope (2026-08-15 relabel):
          * The dim-2 half checks a single dispersion-free assignment on the
            single standard basis. That it sums to 1 there is a one-basis
            check, not a construction of a full non-Born frame function on
            the qubit (which does exist — that is Gleason's dim ≥ 3 caveat,
            cited).
          * The dim-3 half IS a computation: 1000 Haar-ish random orthonormal
            bases, counting how often the same dispersion-free assignment
            fails to sum to 1. It exhibits ONE assignment failing; that ALL
            dispersion-free assignments fail is Kochen–Specker (cited).
        """
        # In dim=2, a non-Born "dispersion-free" measure exists:
        # Assign probability 1 to one basis state and 0 to all others,
        # then rotate — this is consistent in dim=2 but fails in dim≥3.

        dim2_state = np.array([1, 0], dtype=np.complex128)

        # Dispersion-free measure: pick a direction, assign prob 1 if
        # the projector aligns with it, 0 otherwise
        # (This is a hidden variable model — works ONLY in dim=2)

        chosen_direction = np.array([1, 0], dtype=np.complex128)

        def dispersion_free(v):
            overlap = abs(np.dot(chosen_direction.conj(), v)) ** 2
            return 1.0 if overlap > 0.5 else 0.0

        # Test this on dim=2 basis
        results_dim2 = {}
        basis_2d = [
            np.array([1, 0], dtype=np.complex128),
            np.array([0, 1], dtype=np.complex128),
        ]
        probs_2d = [dispersion_free(b) for b in basis_2d]
        results_dim2["standard_basis"] = probs_2d
        results_dim2["sums_to_one"] = abs(sum(probs_2d) - 1.0) < 1e-10

        # Now try in dim=3 — the dispersion-free measure FAILS
        dim3_direction = np.array([1, 0, 0], dtype=np.complex128)

        def dispersion_free_3d(v):
            overlap = abs(np.dot(dim3_direction.conj(), v)) ** 2
            return 1.0 if overlap > 0.5 else 0.0

        # Kochen-Specker: find an orthonormal triple where sums fail
        # In dim=3, for ANY dispersion-free assignment, there exists a
        # basis where the probabilities don't sum to 1.
        np.random.seed(42)
        failures = 0
        total = 0
        for _ in range(1000):
            A = np.random.randn(3, 3) + 1j * np.random.randn(3, 3)
            Q, _ = np.linalg.qr(A)
            probs = [dispersion_free_3d(Q[:, i]) for i in range(3)]
            total += 1
            if abs(sum(probs) - 1.0) > 1e-6:
                failures += 1

        return {
            "dim_2": {
                "dispersion_free_works": results_dim2["sums_to_one"],
                "note": "Checked on the standard basis ONLY: this one dispersion-free "
                        "assignment sums to 1 there. That non-Born frame functions "
                        "genuinely exist on a qubit is the cited dim ≥ 3 caveat of "
                        "Gleason's theorem, not something shown by this one check.",
                "implication": "Qubits admit non-Born measures (cited). Higher "
                               "dimensions do not (Gleason/Kochen-Specker, cited).",
                "scope": "one assignment, one basis — illustration, not a proof",
            },
            "dim_3": {
                "dispersion_free_fails": failures > 0,
                "failure_rate": failures / total,
                "total_tests": total,
                "note": f"In dim=3, THIS dispersion-free assignment fails to sum to 1 "
                        f"on {failures}/{total} random orthonormal bases. That is a "
                        "computed refutation of this one assignment.",
                "implication": "That EVERY dispersion-free assignment fails in dim ≥ 3 "
                               "is the Kochen-Specker theorem (cited), not a result of "
                               "this sampling.",
                "scope": "one assignment, 1000 random bases — computed",
            },
            "framework_hilbert_space": {
                "dimension_used_here": self.dim,
                "framework_claim": "the full consciousness field has dim ≫ 3 "
                                   "(a postulate of the framework, not computed here)",
                "gleason_applicability": "follows from dim ≥ 3 IF the framework's "
                                         "Hilbert-space postulate (A2) is granted",
                "born_rule_status": "treated as a theorem via the CITED Gleason "
                                    "theorem; nothing in this module proves it",
            },
        }

    def axiom_count_bookkeeping(self) -> dict:
        """
        BOOKKEEPING, not a proof. Tabulate the framework's own axiom counts.

        The three integers below (7, 5, 4) are hand-entered editorial counts
        of how the framework chooses to enumerate Copenhagen's axioms versus
        its own. They are not computed from anything, no computation could
        produce them, and arithmetic on them is not a mathematical result.

        The substantive step — "A5 is not independent because the Born rule
        follows from A2 via Gleason" — rests on the CITED Gleason theorem plus
        the framework's own axiomatisation. The C1–C4 checks re-run below do
        not support it; they are consistency checks of the trivial direction
        (see verify_conditions).

        HISTORY: named ``axiom_reduction_proof`` and described as a formal
        proof before the 2026-08-15 review. Retained under the old name as a
        deprecated alias because main.py and tests/test_quantum.py call it.
        """
        # Re-run the three consistency checks so the report is self-contained.
        conditions = self.verify_conditions()
        uniqueness = self.demonstrate_uniqueness()
        dim_check = self.demonstrate_dim2_exception()

        # Editorial axiom counts — hand-entered, not derived.
        copenhagen_axioms = 7  # A1-A7 including Born rule as A5
        advaita_stated = 5     # A1-A5 where A5 references Gleason
        advaita_independent = 4  # framework's claim: A5 reduces to A2 via Gleason

        bookkeeping_chain = [
            "1. A2 (Hilbert-space structure, motivated by Sat-Chit-Ananda) is a "
            "POSTULATE of the framework — asserted, not derived here.",
            f"2. Working dimension = {self.dim} ≥ 3, so Gleason's theorem is "
            "applicable to this space (a dimension comparison, nothing more).",
            "3. Non-negativity (C2): consistency-checked over 500 random projectors "
            "— automatic for any density matrix, so this cannot fail.",
            "4. Additivity (C3): consistency-checked over 200 orthogonal pairs "
            "— this is linearity of the trace, so this cannot fail.",
            "5. Normalization (C4): Tr(ρ) = 1.000000 by construction.",
            "6. Gleason's theorem (CITED, Gleason 1957 — NOT proved here): every "
            "frame function on dim ≥ 3 has the form μ(P) = Tr(ρP).",
            "7. Born rule P(n) = |⟨n|ψ⟩|² is the pure-state special case of (6).",
            "8. The axiom counts below are the framework's own editorial "
            "bookkeeping of A1–A7 vs A1–A5. They are hand-entered integers; "
            "their difference is arithmetic, not a theorem.",
        ]

        return {
            "check_1_conditions_consistent": conditions["all_conditions_satisfied"],
            "check_2_born_additivity_holds":
                uniqueness["born_rule"]["additivity"]["satisfies_additivity"],
            "check_3_dispersion_free_fails_in_dim3":
                dim_check["dim_3"]["dispersion_free_fails"],
            "axiom_counts": {
                "copenhagen": copenhagen_axioms,
                "advaita_stated": advaita_stated,
                "advaita_independent": advaita_independent,
                "reduction": f"{copenhagen_axioms} → {advaita_independent} "
                             f"({copenhagen_axioms - advaita_independent} fewer axioms)",
                "provenance": "hand-entered editorial counts; not computed, and not "
                              "checkable by this module",
            },
            "status": (
                "BOOKKEEPING. Arithmetic on hand-entered axiom counts, plus the "
                "cited Gleason theorem. Nothing here is proved."
            ),
            "bookkeeping_chain": bookkeeping_chain,
            # DEPRECATED alias: main.py still prints proof["proof_chain"].
            "proof_chain": bookkeeping_chain,
            "conclusion": (
                f"On the framework's own enumeration, it lists {advaita_independent} "
                f"independent axioms against Copenhagen's {copenhagen_axioms}, on the "
                "grounds that the Born rule follows from the Hilbert-space postulate "
                "via Gleason's theorem rather than being assumed. That argument stands "
                "or falls on the cited theorem and on accepting this way of counting "
                "axioms — it is a philosophical/organisational claim, not a "
                "mathematical result established by this module. The open question of "
                "why a frame function should be read as a probability of experienced "
                "outcomes is treated in docs/GLEASON_PROBABILITY_GAP.md."
            ),
        }

    # DEPRECATED name, retained because main.py and tests/test_quantum.py call it.
    # "proof" is the wrong word: see axiom_count_bookkeeping.
    def axiom_reduction_proof(self) -> dict:
        """Deprecated alias for :meth:`axiom_count_bookkeeping` (renamed 2026-08-15)."""
        return self.axiom_count_bookkeeping()

    def full_demonstration(self) -> dict:
        """Run the complete set of Gleason-related checks (see module docstring)."""
        return {
            "conditions": self.verify_conditions(),
            "uniqueness": self.demonstrate_uniqueness(),
            "dim2_exception": self.demonstrate_dim2_exception(),
            "axiom_reduction": self.axiom_count_bookkeeping(),
        }
