"""
Entanglement as Non-Duality — The Quantum Residue of Advaita

Entanglement: two particles are correlated in a way that
cannot be explained by any local hidden variable theory.

In Advaita: entanglement is the NATURAL state. Separation
is the illusion. When Maya is removed, everything is seen
as non-separate (a-dvaita = not-two).

Bell's theorem proves that reality is non-local.
Advaita has said this for 3000 years: there is only One,
appearing as many. The 'many' are never truly separate.

WHAT THE CHSH DEMO COMPUTES (rewritten 2026-08-15):
``bell_inequality_violation()`` now measures the state it is handed.  It
builds the analyzer observable A(θ) = cos2θ·σ_z + sin2θ·σ_x, forms
A(a) ⊗ A(b), and evaluates ⟨ψ|A(a)⊗A(b)|ψ⟩ on the supplied two-qubit vector;
it then draws ``num_trials`` outcomes from the exact projective-measurement
distribution of that same state and re-estimates S from the counts.  Both
arguments are consumed.  Two controls run through the identical code path and
come out differently — the separable state |00⟩ gives S = √2 (no violation)
and the singlet |Ψ−⟩ gives S = −2√2 — which is the mechanical proof that the
result depends on the state.  Non-numeric or wrong-dimension input now raises
instead of returning a violation.

HISTORY: before 2026-08-15 this method ignored BOTH of its arguments.  It
evaluated the closed-form singlet correlator E = −cos(2(a−b)) and returned
CHSH = −2.828 with violates_classical=True for any input whatsoever,
including inputs that were not quantum states (the string "banana" returned a
Bell violation).  Docs of that era were right to label it "analytic value, no
state consumed"; that caveat NO LONGER APPLIES to this module and should be
retired wherever it appears.  Note a sign change in the default: |Φ+⟩ with
these angles gives S = +2√2.  The old −2√2 came from applying the singlet
formula to |Φ+⟩; |S| is unchanged at the Tsirelson bound, and −2√2 is still
what |Ψ−⟩ returns.  Scope, unchanged: this is a standard-QM calculation on a
state we wrote down, i.e. an illustration of Tsirelson's bound, not an
experimental test of local realism.
"""

import numpy as np

# Pauli matrices used by the CHSH analyzers.
_SIGMA_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)
_SIGMA_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128)


class NonDualEntanglement:
    """
    Entanglement as the quantum signature of non-duality.
    """

    def __init__(self, dimension: int = 2):
        self.dim = dimension

    def bell_state(self, which: str = "phi_plus") -> np.ndarray:
        """
        Create a Bell state — maximum entanglement between two qubits.

        |Φ+⟩ = (|00⟩ + |11⟩)/√2  — "We are the same"
        |Φ-⟩ = (|00⟩ - |11⟩)/√2  — "We are the same (with phase)"
        |Ψ+⟩ = (|01⟩ + |10⟩)/√2  — "We are complementary"
        |Ψ-⟩ = (|01⟩ - |10⟩)/√2  — "We are complementary (with phase)"

        In Advaita: these are four ways two apparently separate
        entities can express their underlying unity.
        """
        dim2 = self.dim ** 2
        psi = np.zeros(dim2, dtype=np.complex128)

        if which == "phi_plus":
            psi[0] = 1 / np.sqrt(2)   # |00⟩
            psi[dim2 - 1] = 1 / np.sqrt(2)  # |11⟩
        elif which == "phi_minus":
            psi[0] = 1 / np.sqrt(2)
            psi[dim2 - 1] = -1 / np.sqrt(2)
        elif which == "psi_plus":
            psi[1] = 1 / np.sqrt(2)   # |01⟩
            psi[self.dim] = 1 / np.sqrt(2)  # |10⟩
        elif which == "psi_minus":
            psi[1] = 1 / np.sqrt(2)
            psi[self.dim] = -1 / np.sqrt(2)

        return psi

    def entanglement_entropy(self, bipartite_state: np.ndarray,
                              dim_a: int = None, dim_b: int = None) -> float:
        """
        Von Neumann entropy of the reduced state — measures entanglement.

        S = 0: separable (Maya says "these are separate")
        S = log(d): maximally entangled (reality says "these are one")

        In Advaita: high entanglement entropy = reality is non-dual.
        Low entropy = Maya has successfully created the appearance
        of separation.
        """
        if dim_a is None:
            dim_a = self.dim
        if dim_b is None:
            dim_b = len(bipartite_state) // dim_a

        rho = np.outer(bipartite_state, bipartite_state.conj())
        rho_reshaped = rho.reshape(dim_a, dim_b, dim_a, dim_b)
        rho_a = np.trace(rho_reshaped, axis1=1, axis2=3)

        eigenvalues = np.real(np.linalg.eigvalsh(rho_a))
        eigenvalues = eigenvalues[eigenvalues > 1e-15]
        entropy = -np.sum(eigenvalues * np.log(eigenvalues))

        return float(entropy)

    # ------------------------------------------------------------------
    # CHSH — measured on the supplied state (rewritten 2026-08-15)
    # ------------------------------------------------------------------

    CHSH_ANGLES = (0.0, np.pi / 4, np.pi / 8, 3 * np.pi / 8)  # a1, a2, b1, b2

    @staticmethod
    def analyzer_observable(theta: float) -> np.ndarray:
        """
        A(θ) = cos(2θ)·σ_z + sin(2θ)·σ_x — a ±1-valued analyzer at angle θ.

        Hermitian with eigenvalues ±1, eigenvectors (cosθ, sinθ) for +1 and
        (−sinθ, cosθ) for −1.
        """
        return np.cos(2 * theta) * _SIGMA_Z + np.sin(2 * theta) * _SIGMA_X

    @staticmethod
    def _analyzer_eigenvectors(theta: float):
        """(+1, −1) eigenvectors of ``analyzer_observable(theta)``."""
        plus = np.array([np.cos(theta), np.sin(theta)], dtype=np.complex128)
        minus = np.array([-np.sin(theta), np.cos(theta)], dtype=np.complex128)
        return plus, minus

    @classmethod
    def _chsh_exact(cls, psi: np.ndarray) -> tuple:
        """Exact ⟨A(a)⊗A(b)⟩ for the four CHSH settings, on THIS state."""
        a1, a2, b1, b2 = cls.CHSH_ANGLES

        def E(theta_a, theta_b):
            M = np.kron(cls.analyzer_observable(theta_a),
                        cls.analyzer_observable(theta_b))
            return float(np.real(np.vdot(psi, M @ psi)))

        E11, E12, E21, E22 = E(a1, b1), E(a1, b2), E(a2, b1), E(a2, b2)
        S = E11 - E12 + E21 + E22
        return float(S), (E11, E12, E21, E22)

    @classmethod
    def _chsh_sampled(cls, psi: np.ndarray, num_trials: int, seed: int):
        """
        Re-estimate S by sampling projective outcomes from THIS state.

        For each setting pair the four joint outcome probabilities are
        |⟨s_a ⊗ t_b|ψ⟩|²; counts are drawn multinomially and
        Ê = (n₊₊ + n₋₋ − n₊₋ − n₋₊)/N.
        """
        rng = np.random.default_rng(seed)
        a1, a2, b1, b2 = cls.CHSH_ANGLES
        max_norm_error = 0.0
        estimates = []
        for theta_a, theta_b in ((a1, b1), (a1, b2), (a2, b1), (a2, b2)):
            ap, am = cls._analyzer_eigenvectors(theta_a)
            bp, bm = cls._analyzer_eigenvectors(theta_b)
            signs, probs = [], []
            for sa, va in ((1, ap), (-1, am)):
                for sb, vb in ((1, bp), (-1, bm)):
                    amp = np.vdot(np.kron(va, vb), psi)
                    signs.append(sa * sb)
                    probs.append(float(abs(amp) ** 2))
            max_norm_error = max(max_norm_error, abs(sum(probs) - 1.0))
            probs = np.clip(np.asarray(probs), 0.0, None)
            probs = probs / probs.sum()
            counts = rng.multinomial(num_trials, probs)
            estimates.append(float(np.dot(signs, counts) / num_trials))
        E11, E12, E21, E22 = estimates
        return E11 - E12 + E21 + E22, max_norm_error

    def _as_two_qubit_state(self, state) -> tuple:
        """Validate and normalize an input state; return (psi, input_norm)."""
        try:
            psi = np.asarray(state, dtype=np.complex128).reshape(-1)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "bell_inequality_violation needs a numeric two-qubit state "
                f"vector; got {state!r}"
            ) from exc
        if psi.size != 4:
            raise ValueError(
                "CHSH as implemented here is a two-qubit protocol: expected a "
                f"4-component state vector, got size {psi.size}"
            )
        norm = float(np.linalg.norm(psi))
        if norm < 1e-12:
            raise ValueError("state vector has (essentially) zero norm")
        return psi / norm, norm

    def bell_inequality_violation(self, state: np.ndarray = None,
                                   num_trials: int = 10000,
                                   seed: int = 0) -> dict:
        """
        Measure the CHSH combination ON THE SUPPLIED STATE.

        CHSH inequality: |S| ≤ 2 for local hidden variables.
        Quantum mechanics: |S| ≤ 2√2 ≈ 2.828 (Tsirelson).

        Both arguments are consumed.  ``state`` (default |Φ+⟩; any normalizable
        4-vector accepted, non-numeric or wrong-size input raises) is measured
        with A(θ) = cos2θ·σ_z + sin2θ·σ_x at the four optimal settings, giving
        the exact S; ``num_trials`` outcomes are then sampled from that state's
        own measurement distribution and S is re-estimated from the counts
        (``seed`` makes the sampling deterministic; ``num_trials=0`` skips it).

        Two controls run the same code on other states and land elsewhere —
        |00⟩ at S = √2 (no violation), the singlet |Ψ−⟩ at S = −2√2 — so
        ``violates_classical`` is a computed flag, not a constant.

        Scope: this is standard QM evaluated on a state we wrote down. It
        illustrates Tsirelson's bound; it is not an experimental Bell test and
        rules out nothing on its own. (See the module docstring for what this
        replaced.)

        In Advaita: the universe IS non-local because there is
        only One. Bell's theorem is physics confirming Advaita.
        """
        if state is None:
            state = self.bell_state("phi_plus")
        psi, input_norm = self._as_two_qubit_state(state)

        S, (E11, E12, E21, E22) = self._chsh_exact(psi)
        classical_bound = 2.0
        quantum_bound = 2 * np.sqrt(2)

        # Controls: the same measurement code on states with known, DIFFERENT
        # answers. If these ever matched the main result, the demo would have
        # stopped consuming its input.
        control_states = {
            "separable_|00>": np.array([1, 0, 0, 0], dtype=np.complex128),
            "singlet_|psi_minus>": np.array(
                [0, 1, -1, 0], dtype=np.complex128) / np.sqrt(2),
        }
        controls = {}
        for label, vec in control_states.items():
            S_c, _ = self._chsh_exact(vec)
            controls[label] = {
                "CHSH_S_value": S_c,
                "violates_classical": bool(abs(S_c) > classical_bound),
            }
        # Regression detector: if the code ever went back to returning a
        # closed-form constant, these two control states would return the
        # SAME S and this gap would collapse to 0.
        control_values = [c["CHSH_S_value"] for c in controls.values()]
        state_dependence_gap = float(max(control_values) - min(control_values))

        sampling = {"num_trials": int(num_trials), "seed": int(seed)}
        if num_trials and num_trials > 0:
            S_hat, prob_norm_error = self._chsh_sampled(psi, int(num_trials),
                                                        int(seed))
            tolerance = 10.0 / np.sqrt(int(num_trials))  # ~5 sigma on S
            sampling.update({
                "sampled_CHSH_S": float(S_hat),
                "probability_normalization_error": float(prob_norm_error),
                "tolerance": float(tolerance),
                "sampled_matches_exact": bool(abs(S_hat - S) <= tolerance),
            })
        else:
            sampling["sampled_CHSH_S"] = None
            sampling["sampled_matches_exact"] = None

        return {
            "CHSH_S_value": float(S),
            "classical_bound": classical_bound,
            "quantum_bound": float(quantum_bound),
            "violates_classical": bool(abs(S) > classical_bound),
            "violation_amount": float(abs(S) - classical_bound),
            "state_dimension": int(psi.size),
            "input_norm": input_norm,
            "control_S_spread": state_dependence_gap,
            "output_depends_on_state": bool(state_dependence_gap > 1e-9),
            "correlations": {
                "E(a1,b1)": float(E11),
                "E(a1,b2)": float(E12),
                "E(a2,b1)": float(E21),
                "E(a2,b2)": float(E22),
            },
            "sampling": sampling,
            "state_dependence_controls": controls,
            "insight": (
                f"CHSH value S = {S:.4f}, computed as <psi|A(a)xA(b)|psi> on "
                f"the supplied state (|S| {'>' if abs(S) > classical_bound else '<='} "
                "2, the local-hidden-variable bound). The same code gives "
                f"S = {controls['separable_|00>']['CHSH_S_value']:.4f} on the "
                f"separable state |00> and "
                f"S = {controls['singlet_|psi_minus>']['CHSH_S_value']:.4f} on "
                "the singlet, so the number tracks the state rather than the "
                "formula. Standard QM, not an experimental test: real Bell "
                "experiments are what rule out local hidden variables. "
                "Advaita reads the correlations as 'there are no hidden "
                "separations' — the particles are not two things that "
                "communicate, but one thing appearing as two."
            ),
        }

    def monogamy_of_entanglement(self) -> dict:
        """
        Entanglement monogamy: if A is maximally entangled with B,
        A cannot be entangled with C at all.

        In Advaita: this maps to the teaching that liberation
        requires total identification with Brahman. Partial
        identification (entanglement with Maya) prevents full
        realization.

        You cannot be fully identified with both Brahman and the body.
        """
        # A maximally entangled with B
        psi_AB = self.bell_state("phi_plus")
        S_AB = self.entanglement_entropy(psi_AB)

        # A in a GHZ-like state with B and C
        dim3 = self.dim ** 3
        psi_ABC = np.zeros(dim3, dtype=np.complex128)
        psi_ABC[0] = 1 / np.sqrt(2)         # |000⟩
        psi_ABC[dim3 - 1] = 1 / np.sqrt(2)  # |111⟩

        # Entanglement of A with B (tracing out C)
        rho_ABC = np.outer(psi_ABC, psi_ABC.conj())
        rho_ABC_r = rho_ABC.reshape(self.dim, self.dim, self.dim,
                                     self.dim, self.dim, self.dim)
        rho_AB = np.trace(rho_ABC_r, axis1=2, axis2=5)
        rho_AB_flat = rho_AB.reshape(self.dim ** 2, self.dim ** 2)

        # Entanglement of A with B in the three-party state
        rho_A_from_AB = np.trace(rho_AB_flat.reshape(self.dim, self.dim,
                                                       self.dim, self.dim),
                                  axis1=1, axis2=3)
        eigs = np.real(np.linalg.eigvalsh(rho_A_from_AB))
        eigs = eigs[eigs > 1e-15]
        S_A_given_BC = -np.sum(eigs * np.log(eigs))

        return {
            "bell_pair_entanglement": float(S_AB),
            "ghz_state_A_entanglement": float(S_A_given_BC),
            "monogamy_principle": "More entanglement with B → less available for C",
            "advaita_parallel": (
                "Total identification with Brahman (S_max with the Absolute) "
                "requires releasing identification with Maya. "
                "You cannot be 100% identified with both the infinite and the finite. "
                "This is why Vairagya (dispassion) is prerequisite to Jnana (knowledge)."
            ),
        }

    def non_duality_demonstration(self) -> dict:
        """
        Show that entanglement = non-duality at the quantum level.
        """
        # Product state: two 'separate' entities (Maya's view)
        psi_separate = np.zeros(self.dim ** 2, dtype=np.complex128)
        a = np.array([1, 0], dtype=np.complex128)
        b = np.array([0, 1], dtype=np.complex128)
        psi_separate = np.kron(a, b)
        S_separate = self.entanglement_entropy(psi_separate)

        # Bell state: non-dual (Brahman's view)
        psi_entangled = self.bell_state("phi_plus")
        S_entangled = self.entanglement_entropy(psi_entangled)

        return {
            "separable_state_entropy": float(S_separate),
            "entangled_state_entropy": float(S_entangled),
            "max_entropy": float(np.log(self.dim)),
            "separation_is_illusion": S_entangled > S_separate,
            "insight": (
                f"Separable state entropy: {S_separate:.6f} (Maya: 'these are two'). "
                f"Entangled state entropy: {S_entangled:.6f} (Brahman: 'these are one'). "
                "Bell's theorem proves the entangled view is correct. "
                "Separation is the illusion. Non-duality is the reality."
            ),
        }
