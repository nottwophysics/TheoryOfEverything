"""
Unity of Experience — what rho_SA does and does not fix

The accompanying paper claims (section 4.3.2b):

    "Everett faces the 'preferred basis problem' at the level of experience:
     why does each branch-copy of you experience a *unified* world rather
     than a superposition? Decoherence answers this formally (pointer states),
     but the question of why pointer states correspond to *unified experiences*
     is not addressed."

REVIEW LABEL (2026-08-15) — read this before quoting any number from here.

Two different things live in this module, and they are NOT the same kind of
claim:

  (A) MEASURED.  Two computations whose outcome depends on the state and
      could come out the other way:

      * ``environment_unitary_invariance()`` — apply a Haar-random unitary
        to the environment factor alone (I_S (x) I_A (x) U_E).  rho_SA is
        unchanged to ~1e-16 in trace norm while the environment's own
        state rho_E and the individual records |E_n> demonstrably change.
        So rho_SA does not fix the environment record: information that
        exists in the global state is simply absent from rho_SA.

      * ``factorization_dependence()`` — apply a global unitary that is a
        product across the S | (A (x) E) cut but NOT a product across
        S (x) A (x) E (a regrouping/erasure permutation on A (x) E, operator
        Schmidt rank > 1 across A|E, checked here).  rho_S is invariant to
        ~1e-16, yet rank(rho_SA) drops from n to 1.  So the "number of
        branches" read off rho_SA is a property of the chosen S/A/E split,
        not of the global state.

      Both are honest, falsifiable statements about what rho_SA leaves open.

  (B) ANALYTIC BOOKKEEPING, NOT EVIDENCE.  ``underdetermination_test()``
      catalogues four experiential interpretations and reports that they
      disagree on the cardinality of unified experience.  Three of the four
      maps (``everett_superposed_map``, ``copenhagen_classical_map``,
      ``subject_modes_map``) return their cardinality BY DEFINITION — they
      accept rho_sa and never read it.  The verdict
      ``decoherence_underdetermines_experience`` is therefore True for every
      input, including a rank-1 rho_SA in which nothing has decohered.  It
      restates the definitions of the four positions; it does not test them.
      ``sweep_robustness()`` documents exactly that invariance (with a
      rank-1 negative control) instead of reporting it as a 30/30 finding.

HISTORY: before the 2026-08-15 review this module reported "30/30 trials
confirm underdetermination" as a robustness result.  That framing was
withdrawn: the sweep is structurally invariant, so 30/30 was guaranteed
before any trial ran.  The measured content in (A) was added at the same
time, because it is the part of the paper's claim that IS computable.

STATUS: Supports paper section 4.3.2(b) via (A).  (B) is a taxonomy.
"""

import numpy as np


class UnityOfExperience:
    """
    Separate what decoherence fixes (rho_SA, and what rho_SA is invariant
    under) from what it does not fix (experiential ontology).
    """

    def __init__(self, n_outcomes: int = 3, seed: int = 42):
        if n_outcomes < 2:
            raise ValueError("n_outcomes must be at least 2.")
        self.n = n_outcomes
        self.seed = seed

    # ------------------------------------------------------------
    # State preparation and decoherence
    # ------------------------------------------------------------

    def post_measurement_state(self, amplitudes: np.ndarray = None) -> dict:
        """
        Construct |Psi> = sum_n c_n |n>_S |n>_A |E_n> with orthogonal E_n.

        Returns the joint pure state and the per-subsystem dimensions.
        """
        if amplitudes is None:
            rng = np.random.default_rng(self.seed)
            c = rng.normal(size=self.n) + 1j * rng.normal(size=self.n)
            amplitudes = c / np.linalg.norm(c)
        else:
            amplitudes = np.array(amplitudes, dtype=np.complex128)
            amplitudes = amplitudes / np.linalg.norm(amplitudes)

        n = self.n
        dim = n * n * n  # S x A x E
        psi = np.zeros(dim, dtype=np.complex128)

        # Index convention: (s, a, e) -> s*(n*n) + a*n + e
        for k in range(n):
            idx = k * (n * n) + k * n + k
            psi[idx] = amplitudes[k]

        return {
            "psi": psi,
            "amplitudes": amplitudes,
            "dim_S": n,
            "dim_A": n,
            "dim_E": n,
            "n_outcomes": n,
            "total_purity": float(np.real(np.vdot(psi, psi))),
        }

    def reduced_SA(self, state_bundle: dict) -> np.ndarray:
        """Trace out E to obtain rho_SA."""
        psi = state_bundle["psi"]
        n = state_bundle["n_outcomes"]
        # Index convention: (s, a, e) -> s*n^2 + a*n + e
        rho_sa = np.zeros((n * n, n * n), dtype=np.complex128)
        for s in range(n):
            for a in range(n):
                for sp in range(n):
                    for ap in range(n):
                        acc = 0.0 + 0.0j
                        for e in range(n):
                            i_left = s * (n * n) + a * n + e
                            i_right = sp * (n * n) + ap * n + e
                            acc += psi[i_left] * psi[i_right].conj()
                        rho_sa[s * n + a, sp * n + ap] = acc
        return rho_sa

    # ------------------------------------------------------------
    # Reduction helpers used by the measured tests below
    # ------------------------------------------------------------

    @staticmethod
    def _rho_SA_from_psi(psi: np.ndarray, n: int) -> np.ndarray:
        """rho_SA = Tr_E |Psi><Psi|, vectorised (same convention as reduced_SA)."""
        t = psi.reshape(n, n, n)
        return np.einsum("sae,tbe->satb", t, t.conj()).reshape(n * n, n * n)

    @staticmethod
    def _rho_S_from_psi(psi: np.ndarray, n: int) -> np.ndarray:
        """rho_S = Tr_AE |Psi><Psi|."""
        t = psi.reshape(n, n, n)
        return np.einsum("sae,tae->st", t, t.conj())

    @staticmethod
    def _rho_E_from_psi(psi: np.ndarray, n: int) -> np.ndarray:
        """rho_E = Tr_SA |Psi><Psi|."""
        t = psi.reshape(n, n, n)
        return np.einsum("sae,saf->ef", t, t.conj())

    @staticmethod
    def _trace_norm(m: np.ndarray) -> float:
        """||m||_1 = sum of singular values (Schatten-1 norm)."""
        return float(np.sum(np.linalg.svd(m, compute_uv=False)))

    @staticmethod
    def _haar_unitary(dim: int, rng: np.random.Generator) -> np.ndarray:
        """Haar-random unitary via QR with the standard phase correction."""
        z = (rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))) / np.sqrt(2.0)
        q, r = np.linalg.qr(z)
        d = np.diag(r)
        return q @ np.diag(d / np.abs(d))

    # ------------------------------------------------------------
    # Einselection check
    # ------------------------------------------------------------

    def einselection_diagnostic(self, rho_sa: np.ndarray) -> dict:
        """
        Check whether rho_SA is diagonal in the measurement/pointer basis.
        Reports off-diagonal weight and spectrum.  Everything here is read
        off the supplied matrix.
        """
        diag = np.diag(np.diag(rho_sa))
        off_diag_norm = float(np.linalg.norm(rho_sa - diag))
        diag_weights = np.real(np.diag(rho_sa))

        eigvals = np.sort(np.real(np.linalg.eigvalsh(rho_sa)))[::-1]
        # Only non-trivial eigenvalues
        significant = eigvals[eigvals > 1e-12]

        return {
            "off_diagonal_norm": off_diag_norm,
            "diagonal_weights": [float(x) for x in diag_weights if x > 1e-12],
            "eigenvalues": [float(x) for x in significant],
            "is_diagonal_pointer_basis": bool(off_diag_norm < 1e-10),
            "rank": int(np.sum(eigvals > 1e-10)),
        }

    # ------------------------------------------------------------
    # (A) MEASURED: what rho_SA is invariant under
    # ------------------------------------------------------------

    def environment_unitary_invariance(self, n_trials: int = 20,
                                       tol: float = 1e-14) -> dict:
        """
        MEASURED.  rho_SA is blind to unitaries on the environment.

        Apply I_S (x) I_A (x) U_E for Haar-random U_E and measure:

            * ||rho_SA - rho'_SA||_1   (expected ~1e-16, must be < tol)
            * ||rho_E  - rho'_E ||_1   (expected O(0.1): the environment's
              own state genuinely changed)
            * per-record change 1 - |<E_k|U_E|E_k>|^2 (the pointer records
              themselves are rotated into different environment states)

        The conclusion is a statement about what rho_SA does NOT fix: the
        environment record is not recoverable from rho_SA, so any account
        that reads an experiential fact off rho_SA is reading off an object
        that has already discarded that information.

        Every flag returned is a comparison of measured floats against the
        stated tolerance; a bug that made rho_SA move, or a U_E that failed
        to move rho_E, would flip them.
        """
        n = self.n
        rng = np.random.default_rng(self.seed + 1)
        bundle = self.post_measurement_state()
        psi = bundle["psi"]

        rho_sa = self._rho_SA_from_psi(psi, n)
        rho_e = self._rho_E_from_psi(psi, n)

        sa_distances = []
        e_distances = []
        record_changes = []
        unitarity_errors = []

        for _ in range(n_trials):
            u = self._haar_unitary(n, rng)
            unitarity_errors.append(
                float(np.linalg.norm(u.conj().T @ u - np.eye(n)))
            )

            t = psi.reshape(n, n, n)
            psi_p = np.einsum("fe,sae->saf", u, t).reshape(-1)

            rho_sa_p = self._rho_SA_from_psi(psi_p, n)
            rho_e_p = self._rho_E_from_psi(psi_p, n)

            sa_distances.append(self._trace_norm(rho_sa - rho_sa_p))
            e_distances.append(self._trace_norm(rho_e - rho_e_p))
            # |<E_k|U|E_k>|^2 = |U_kk|^2 in the record basis.
            record_changes.append(
                float(np.max(1.0 - np.abs(np.diag(u)) ** 2))
            )

        max_sa = float(np.max(sa_distances))
        min_e = float(np.min(e_distances))
        min_record = float(np.min(record_changes))
        max_unitarity_err = float(np.max(unitarity_errors))

        return {
            "trials": int(n_trials),
            "n_outcomes": n,
            "tolerance": float(tol),
            "max_rho_SA_trace_norm_change": max_sa,
            "mean_rho_SA_trace_norm_change": float(np.mean(sa_distances)),
            "min_rho_E_trace_norm_change": min_e,
            "mean_rho_E_trace_norm_change": float(np.mean(e_distances)),
            "min_max_record_change": min_record,
            "max_unitarity_error": max_unitarity_err,
            "rho_SA_invariant": bool(max_sa < tol),
            "environment_state_changed": bool(min_e > 1e-6),
            "environment_records_changed": bool(min_record > 1e-6),
            "measured_claim": (
                f"Over {n_trials} Haar-random environment unitaries, rho_SA moved "
                f"by at most {max_sa:.2e} in trace norm (tolerance {tol:.0e}) while "
                f"rho_E moved by at least {min_e:.3f} and at least one environment "
                f"record was rotated by at least {min_record:.3f}. rho_SA therefore "
                "does not fix the environment record. This is measured, not assumed: "
                "the flags are float comparisons that a broken reduction would fail."
            ),
        }

    def factorization_dependence(self, tol: float = 1e-12) -> dict:
        """
        MEASURED.  The branch count read off rho_SA depends on the S/A/E split.

        Apply the regrouping permutation R on A (x) E defined by

            R |a>_A |e>_E = |a>_A |(e - a) mod n>_E

        which is unitary (checked) and has operator Schmidt rank n > 1 across
        the A|E cut (checked) — i.e. it is NOT of the form U_A (x) U_E, so it
        redraws the A/E boundary without touching S.

        On |Psi> = sum_k c_k |k>_S |k>_A |E_k> it produces
        sum_k c_k |k>_S |k>_A |E_0>, so:

            * rho_S is unchanged (trace norm change ~1e-16), and the global
              state stays pure — nothing was lost;
            * rank(rho_SA) drops from n to 1: the "N branches" become one.

        Hence "how many branches there are" is not a property of the global
        state; it is a property of the factorization chosen when the
        environment was named.  Everything below is computed from the two
        states; nothing is asserted.
        """
        n = self.n
        bundle = self.post_measurement_state()
        psi = bundle["psi"]

        # Build R explicitly on the A (x) E space (index a*n + e).
        dim_ae = n * n
        r_mat = np.zeros((dim_ae, dim_ae), dtype=np.complex128)
        for a in range(n):
            for e in range(n):
                r_mat[a * n + ((e - a) % n), a * n + e] = 1.0
        unitarity_error = float(
            np.linalg.norm(r_mat.conj().T @ r_mat - np.eye(dim_ae))
        )

        # Operator Schmidt rank of R across A|E: reshape (a',e',a,e) -> ((a',a),(e',e)).
        r_t = r_mat.reshape(n, n, n, n).transpose(0, 2, 1, 3).reshape(n * n, n * n)
        operator_schmidt_rank = int(np.linalg.matrix_rank(r_t, tol=1e-10))

        # Apply I_S (x) R.
        t = psi.reshape(n, dim_ae)
        psi_p = (t @ r_mat.T).reshape(-1)

        rho_sa = self._rho_SA_from_psi(psi, n)
        rho_sa_p = self._rho_SA_from_psi(psi_p, n)
        rho_s = self._rho_S_from_psi(psi, n)
        rho_s_p = self._rho_S_from_psi(psi_p, n)

        rank_before = int(np.sum(np.real(np.linalg.eigvalsh(rho_sa)) > 1e-10))
        rank_after = int(np.sum(np.real(np.linalg.eigvalsh(rho_sa_p)) > 1e-10))

        rho_s_change = self._trace_norm(rho_s - rho_s_p)
        rho_sa_change = self._trace_norm(rho_sa - rho_sa_p)
        purity_after = float(np.real(np.vdot(psi_p, psi_p)))

        return {
            "n_outcomes": n,
            "tolerance": float(tol),
            "regrouping_unitarity_error": unitarity_error,
            "regrouping_is_unitary": bool(unitarity_error < 1e-10),
            "operator_schmidt_rank_across_A_E": operator_schmidt_rank,
            "regrouping_is_product_across_A_E": bool(operator_schmidt_rank == 1),
            "rank_rho_SA_before": rank_before,
            "rank_rho_SA_after": rank_after,
            "branch_count_changed": bool(rank_after != rank_before),
            "rho_S_trace_norm_change": rho_s_change,
            "rho_S_invariant": bool(rho_s_change < tol),
            "rho_SA_trace_norm_change": rho_sa_change,
            "global_state_norm_after": purity_after,
            "global_state_still_pure": bool(abs(purity_after - 1.0) < 1e-10),
            "measured_claim": (
                f"A unitary acting only on A (x) E (operator Schmidt rank "
                f"{operator_schmidt_rank} across A|E, so not a product U_A (x) U_E) "
                f"leaves rho_S unchanged to {rho_s_change:.2e} in trace norm and "
                f"keeps the global state pure, yet rank(rho_SA) goes "
                f"{rank_before} -> {rank_after}. The branch count is therefore a "
                "property of the chosen S/A/E factorization, not of the state."
            ),
        }

    # ------------------------------------------------------------
    # (B) Four experiential interpretations — a taxonomy, not a test
    # ------------------------------------------------------------

    def everett_unified_map(self, rho_sa: np.ndarray, n: int) -> dict:
        """
        I1: Each pointer-basis component is a unified experience.
        Cardinality of unified experiencers = rank of rho_SA.

        This is the ONE map whose cardinality is read from rho_sa.

        This interpretation asserts a postulate BEYOND decoherence:
        'pointer state <=> unified experience'. The einselection argument
        (Zurek 2003) justifies stability of pointer states, not their
        identification with experiences.
        """
        eigvals = np.linalg.eigvalsh(rho_sa)
        eigvals = np.real(eigvals[eigvals > 1e-12])
        return {
            "name": "Everett (unified branches)",
            "n_unified_experiences": int(len(eigvals)),
            "cardinality_source": "computed from rho_sa (its rank)",
            "extra_postulate": "Pointer states are identified with unified experiences.",
            "justification_by_decoherence": False,
            "consistent_with_rho_sa": True,
        }

    def everett_superposed_map(self, rho_sa: np.ndarray, n: int) -> dict:
        """
        I2: A single experience over a SUPERPOSITION of outcomes.
        This is what the paper's section 4.3.2(b) highlights: decoherence
        does not rule this out — it only makes pointer states robust. A
        hypothetical 'non-unified observer' would experience superposition.

        NOTE (2026-08-15 review): the cardinality 0 is part of the DEFINITION
        of this position, not a measurement. rho_sa is accepted for a uniform
        signature and is deliberately not read.
        """
        return {
            "name": "Everett (non-unified, superposed experience)",
            "n_unified_experiences": 0,
            "cardinality_source": "definitional (rho_sa is not read)",
            "extra_postulate": "Experience tracks the superposed subsystem state (no unity).",
            "justification_by_decoherence": False,
            "consistent_with_rho_sa": True,
        }

    def copenhagen_classical_map(self, rho_sa: np.ndarray, n: int) -> dict:
        """
        I3: One classical outcome is realized; rho_SA is a probabilistic
        description of the classical ensemble. Requires collapse.

        NOTE (2026-08-15 review): the cardinality 1 is definitional. Only the
        classical probabilities below are read from rho_sa.
        """
        diag = np.real(np.diag(rho_sa))
        diag = diag[diag > 1e-12]
        return {
            "name": "Copenhagen (collapse + classical outcome)",
            "n_unified_experiences": 1,
            "cardinality_source": "definitional (one outcome is realized, by hypothesis)",
            "extra_postulate": "A collapse mechanism selects one classical outcome.",
            "justification_by_decoherence": False,
            "consistent_with_rho_sa": True,
            "classical_probabilities": [float(x) for x in diag],
        }

    def subject_modes_map(self, rho_sa: np.ndarray, n: int) -> dict:
        """
        I4: One universal subject, whose modes of self-relation correspond
        to perspectives. Unity is intrinsic to the subject; pointer states
        are the structural form of locally-unified perspectives. The
        postulate is metaphysical (A1 of the paper), not an add-on to
        decoherence.

        NOTE (2026-08-15 review): the cardinality 1 is definitional (there is
        one subject by hypothesis). Only n_perspective_modes is read from rho_sa.
        """
        eigvals = np.linalg.eigvalsh(rho_sa)
        eigvals = np.real(eigvals[eigvals > 1e-12])
        return {
            "name": "Consciousness-primitive (subject with modes)",
            "n_unified_experiences": 1,  # ONE subject — by hypothesis, not measured
            "n_perspective_modes": int(len(eigvals)),
            "cardinality_source": "definitional (one subject); modes computed from rho_sa",
            "extra_postulate": "Unity is intrinsic to the universal subject (axiom A1).",
            "justification_by_decoherence": False,
            "consistent_with_rho_sa": True,
            "distinction": (
                "Unlike Everett, unity is not asserted for each branch. "
                "Unity is a feature of the one subject, and perspectives "
                "are its modes. Decoherence creates the mode structure; "
                "unity is grounded in the primitive."
            ),
        }

    # ------------------------------------------------------------
    # The interpretation catalogue (analytic, not empirical)
    # ------------------------------------------------------------

    def underdetermination_test(self, state_bundle: dict = None) -> dict:
        """
        ANALYTIC BOOKKEEPING — not a test, despite the historical name.

        Catalogues four experiential interpretations and reports that they
        disagree on the cardinality of unified experience while all being
        consistent with the same rho_SA.

        Why this is not evidence: three of the four cardinalities (0, 1, 1)
        are definitional — those maps never read rho_sa. So
        ``distinct_cardinalities_count >= 2`` holds for EVERY input,
        including a rank-1 rho_SA in which nothing has decohered. The
        returned flag ``decoherence_underdetermines_experience`` is therefore
        an analytic consequence of how the four positions are defined, and
        the honest reading of it is: "the four positions, as defined,
        disagree" — not "decoherence was shown to underdetermine anything".

        The measurable content of the paper's claim lives in
        ``environment_unitary_invariance()`` and ``factorization_dependence()``.

        HISTORY: named ``underdetermination_test`` and reported as a result
        before the 2026-08-15 review; kept under that name only because
        main.py and tests/test_quantum.py call it.
        """
        if state_bundle is None:
            state_bundle = self.post_measurement_state()
        rho_sa = self.reduced_SA(state_bundle)
        einsel = self.einselection_diagnostic(rho_sa)
        n = state_bundle["n_outcomes"]

        maps = [
            self.everett_unified_map(rho_sa, n),
            self.everett_superposed_map(rho_sa, n),
            self.copenhagen_classical_map(rho_sa, n),
            self.subject_modes_map(rho_sa, n),
        ]

        cardinalities = {m["name"]: m["n_unified_experiences"] for m in maps}
        unique_cardinalities = sorted(set(cardinalities.values()))

        # NOTE: `underdetermined` is computed from the four maps, but three of
        # them supply their cardinality by definition, so it cannot come out
        # False. See the docstring and sweep_robustness()'s rank-1 control.
        underdetermined = len(unique_cardinalities) >= 2
        all_consistent = all(m["consistent_with_rho_sa"] for m in maps)

        n_definitional = sum(
            1 for m in maps if m["cardinality_source"].startswith("definitional")
        )

        return {
            "rho_SA_trace": float(np.real(np.trace(rho_sa))),
            "rho_SA_purity": float(np.real(np.trace(rho_sa @ rho_sa))),
            "einselection": einsel,
            "interpretations": maps,
            "cardinalities": cardinalities,
            "distinct_cardinalities_count": len(unique_cardinalities),
            "definitional_cardinality_count": int(n_definitional),
            "verdict_status": (
                "ANALYTIC — not empirical. "
                f"{n_definitional} of {len(maps)} cardinalities are definitional "
                "(those maps do not read rho_sa), so the verdict below is True "
                "for every input, including an undecohered rank-1 rho_SA."
            ),
            "decoherence_underdetermines_experience": bool(
                underdetermined and all_consistent
            ),
            "conclusion": (
                "Bookkeeping, not a measurement: four interpretations that "
                f"differ by definition are catalogued, and {len(unique_cardinalities)} "
                "distinct cardinalities of unified experience result. Since three "
                "of the four cardinalities are fixed by the definition of the "
                "position rather than read from rho_SA, this restates the "
                "positions; it does not test them. The measured version of the "
                "paper's claim is in environment_unitary_invariance() and "
                "factorization_dependence(): rho_SA is provably blind to "
                "environment unitaries, and the branch count it exhibits changes "
                "under a regrouping of the A/E cut."
            ),
        }

    # ------------------------------------------------------------
    # Structural-invariance documentation (formerly "robustness")
    # ------------------------------------------------------------

    def sweep_robustness(self, n_trials: int = 30) -> dict:
        """
        Document that ``underdetermination_test``'s verdict is structurally
        invariant — it is NOT a robustness result.

        HISTORY: this method previously reported "30/30 trials confirm
        underdetermination" as evidence. Withdrawn 2026-08-15: the verdict
        cannot come out False for any input, so 30/30 was guaranteed before
        the first trial ran.

        What is actually computed here:
          * the verdict over ``n_trials`` random amplitude profiles, and
          * a DEGENERATE NEGATIVE CONTROL: amplitudes (1, 0, ..., 0), giving a
            rank-1 rho_SA — a product state in which no decoherence has
            occurred at all. If the verdict is still True there, the verdict
            is insensitive to the data by construction.

        ``structurally_invariant`` is True exactly when the verdict held on
        every random trial AND on the undecohered control; if a future change
        made any map read rho_sa, the control would flip and this would become
        False.
        """
        rng = np.random.default_rng(self.seed)
        outcomes = []

        for _ in range(n_trials):
            c = rng.normal(size=self.n) + 1j * rng.normal(size=self.n)
            c = c / np.linalg.norm(c)
            sb = self.post_measurement_state(amplitudes=c)
            result = self.underdetermination_test(sb)
            outcomes.append(result["decoherence_underdetermines_experience"])

        verdict_rate = sum(outcomes) / len(outcomes)

        # Negative control: no decoherence at all (rank-1 rho_SA).
        degenerate = np.zeros(self.n, dtype=np.complex128)
        degenerate[0] = 1.0
        ctrl_bundle = self.post_measurement_state(amplitudes=degenerate)
        ctrl_rho = self.reduced_SA(ctrl_bundle)
        ctrl_result = self.underdetermination_test(ctrl_bundle)
        ctrl_rank = self.einselection_diagnostic(ctrl_rho)["rank"]
        ctrl_verdict = bool(ctrl_result["decoherence_underdetermines_experience"])

        structurally_invariant = bool(verdict_rate == 1.0 and ctrl_verdict)

        return {
            "trials": n_trials,
            "n_outcomes_per_trial": self.n,
            "verdict_true_count": int(sum(outcomes)),
            "verdict_true_rate": float(verdict_rate),
            "control_rho_SA_rank": int(ctrl_rank),
            "control_verdict_true": ctrl_verdict,
            "structurally_invariant": structurally_invariant,
            # DEPRECATED aliases: main.py and tests/test_quantum.py still read
            # these names. They are the same numbers; the words "success" and
            # "robust" are misleading and should not be quoted. See notes.
            "success_count": int(sum(outcomes)),
            "success_rate": float(verdict_rate),
            "robust": bool(verdict_rate == 1.0),
            "interpretation": (
                f"NOT EVIDENCE. The verdict was True on {int(sum(outcomes))}/{n_trials} "
                f"random amplitude profiles AND on the rank-{int(ctrl_rank)} control in "
                "which nothing has decohered. Agreement across trials therefore "
                "measures nothing: three of the four interpretation maps supply their "
                "cardinality by definition and never read rho_SA. This sweep is "
                "reported only to document that invariance."
            ),
        }

    # ------------------------------------------------------------
    # Orchestrator
    # ------------------------------------------------------------

    def run_all(self) -> dict:
        """Run everything and return a consolidated report."""
        sb = self.post_measurement_state()
        rho_sa = self.reduced_SA(sb)
        main = self.underdetermination_test(sb)
        robust = self.sweep_robustness()
        env_inv = self.environment_unitary_invariance()
        factorization = self.factorization_dependence()

        return {
            "state": {
                "n_outcomes": sb["n_outcomes"],
                "amplitudes_abs": [float(abs(a)) for a in sb["amplitudes"]],
                "total_state_purity": sb["total_purity"],
            },
            "reduced_SA_trace": float(np.real(np.trace(rho_sa))),
            "main_result": main,
            "robustness": robust,
            "environment_unitary_invariance": env_inv,
            "factorization_dependence": factorization,
            "measured_support": (
                "Paper section 4.3.2(b), measured part: rho_SA is invariant "
                f"(<= {env_inv['max_rho_SA_trace_norm_change']:.2e} in trace norm) under "
                f"{env_inv['trials']} random environment unitaries that move rho_E by "
                f">= {env_inv['min_rho_E_trace_norm_change']:.3f}; and a regrouping of the "
                f"A/E cut that leaves rho_S fixed to "
                f"{factorization['rho_S_trace_norm_change']:.2e} changes rank(rho_SA) "
                f"{factorization['rank_rho_SA_before']} -> {factorization['rank_rho_SA_after']}. "
                "So rho_SA fixes neither the environment record nor the branch count."
            ),
            "paper_claim_supported": (
                "Paper section 4.3.2(b): decoherence formalism does not address "
                "why pointer states correspond to unified experiences. The "
                "four-interpretation catalogue below is ANALYTIC (three of the "
                "four cardinalities are definitional, so it is True for every "
                "input, including an undecohered rank-1 state) and is not "
                "offered as evidence; the evidential content is the measured "
                "invariance results above."
            ),
        }
