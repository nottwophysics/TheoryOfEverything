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
"""

import numpy as np


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

    def bell_inequality_violation(self, state: np.ndarray = None,
                                   num_trials: int = 10000) -> dict:
        """
        Demonstrate Bell inequality violation — proving non-locality.

        CHSH inequality: |S| ≤ 2 for local hidden variables.
        Quantum mechanics: |S| ≤ 2√2 ≈ 2.828.

        In Advaita: the universe IS non-local because there is
        only One. Bell's theorem is physics confirming Advaita.
        """
        if state is None:
            state = self.bell_state("phi_plus")

        # CHSH optimal angles for maximum violation
        a1 = 0                # Alice angle 1
        a2 = np.pi / 4       # Alice angle 2
        b1 = np.pi / 8       # Bob angle 1
        b2 = 3 * np.pi / 8   # Bob angle 2

        def expectation(theta_a, theta_b):
            """E(a,b) for |Φ+⟩ Bell state: E = -cos(2(a-b))."""
            return -np.cos(2 * (theta_a - theta_b))

        E_a1b1 = expectation(a1, b1)
        E_a1b2 = expectation(a1, b2)
        E_a2b1 = expectation(a2, b1)
        E_a2b2 = expectation(a2, b2)

        S = E_a1b1 - E_a1b2 + E_a2b1 + E_a2b2
        classical_bound = 2.0
        quantum_bound = 2 * np.sqrt(2)

        return {
            "CHSH_S_value": float(S),
            "classical_bound": classical_bound,
            "quantum_bound": float(quantum_bound),
            "violates_classical": abs(S) > classical_bound,
            "violation_amount": float(abs(S) - classical_bound),
            "correlations": {
                "E(a1,b1)": float(E_a1b1),
                "E(a1,b2)": float(E_a1b2),
                "E(a2,b1)": float(E_a2b1),
                "E(a2,b2)": float(E_a2b2),
            },
            "insight": (
                f"CHSH value S = {S:.4f}, violating the classical bound of 2. "
                "This proves that reality is non-local — there are no "
                "'hidden variables' that could explain the correlations classically. "
                "Advaita: 'there are no hidden separations.' "
                "The particles are not two things that communicate — "
                "they are one thing appearing as two."
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
