"""
Brahman as Hilbert Space — The Quantum Substrate

In standard QM, the Hilbert space is an abstract mathematical arena.
In this framework, the Hilbert space IS Brahman — consciousness itself
is the space in which all quantum states exist.

Key mapping:
    Brahman          → Infinite-dimensional Hilbert space H
    Maya             → Projection operators that reduce H to finite subspaces
    Superposition    → Non-dual nature (all possibilities coexist before Maya)
    Measurement      → Sakshi (witness) collapsing potentiality to actuality
    Entanglement     → Non-separation (Advaita = "not-two")
"""

import numpy as np
from scipy.linalg import expm
from typing import Optional


class BrahmanHilbertSpace:
    """
    The fundamental Hilbert space — consciousness as quantum arena.

    This is not a space *within* which consciousness exists.
    This IS consciousness — the arena and the content are one.
    """

    def __init__(self, dimension: int = 64):
        """
        In principle, Brahman is infinite-dimensional.
        We work with a finite truncation for computation.
        """
        self.dimension = dimension
        # The vacuum state: pure undifferentiated potential
        # In Advaita: Brahman prior to any Maya
        self._vacuum = np.zeros(dimension, dtype=np.complex128)
        self._vacuum[0] = 1.0  # Ground state

        # The full-superposition state: all basis states equally weighted
        # In Advaita: Brahman as infinite potentiality
        self._brahman_state = np.ones(dimension, dtype=np.complex128) / np.sqrt(dimension)

    @property
    def vacuum(self) -> np.ndarray:
        """The ground state — Brahman in 'deep sleep' (Sushupti)."""
        return self._vacuum.copy()

    @property
    def brahman_state(self) -> np.ndarray:
        """Full superposition — Brahman as pure potentiality."""
        return self._brahman_state.copy()

    def inner_product(self, psi: np.ndarray, phi: np.ndarray) -> complex:
        """
        <psi|phi> — the overlap between two states.

        In Advaita: the degree to which two apparently separate
        entities share the same consciousness-substrate.
        Atman-Brahman identity → <atman|brahman> ≈ 1
        """
        return complex(np.dot(np.conj(psi), phi))

    def norm(self, psi: np.ndarray) -> float:
        """The 'reality-measure' of a state."""
        return float(np.sqrt(np.abs(self.inner_product(psi, psi))))

    def normalize(self, psi: np.ndarray) -> np.ndarray:
        """Normalize a state vector."""
        n = self.norm(psi)
        if n > 0:
            return psi / n
        return psi

    def tensor_product(self, psi: np.ndarray, phi: np.ndarray) -> np.ndarray:
        """
        |psi> ⊗ |phi> — combining two systems.

        In Advaita: Maya creating the appearance of two separate
        systems from one Brahman. The tensor product structure
        is what allows entanglement (non-separation).
        """
        return np.kron(psi, phi)

    def partial_trace(self, rho: np.ndarray, dim_a: int, dim_b: int,
                      trace_over: str = "B") -> np.ndarray:
        """
        Trace out subsystem B (or A) from a bipartite density matrix.

        In Advaita: ignoring part of reality (Maya's concealment).
        The reduced state of a subsystem looks mixed even when
        the whole is pure — apparent ignorance from partial seeing.
        """
        rho_reshaped = rho.reshape(dim_a, dim_b, dim_a, dim_b)
        if trace_over == "B":
            return np.trace(rho_reshaped, axis1=1, axis2=3)
        else:
            return np.trace(rho_reshaped, axis1=0, axis2=2)

    def density_matrix(self, psi: np.ndarray) -> np.ndarray:
        """
        |psi><psi| — the density matrix (pure state).

        Brahman in its fullness: a pure state.
        Maya introduces mixedness through partial tracing.
        """
        psi = psi.reshape(-1, 1)
        return psi @ psi.conj().T

    def von_neumann_entropy(self, rho: np.ndarray) -> float:
        """
        S(rho) = -Tr(rho ln rho)

        The entropy of a quantum state.
        Pure states (Brahman) have S=0.
        Mixed states (Maya's partial view) have S>0.

        In Advaita: entropy measures the degree of Maya's concealment.
        Full knowledge (S=0) = seeing Brahman.
        Maximum ignorance (S=log(d)) = maximum Maya.
        """
        eigenvalues = np.real(np.linalg.eigvalsh(rho))
        eigenvalues = eigenvalues[eigenvalues > 1e-15]
        return float(-np.sum(eigenvalues * np.log(eigenvalues)))

    def superposition(self, states: list, amplitudes: list = None) -> np.ndarray:
        """
        Create a superposition — multiple possibilities coexisting.

        In Advaita: Brahman holds all possibilities simultaneously.
        This is not uncertainty about reality — it IS reality
        prior to Maya's differentiation.
        """
        if amplitudes is None:
            amplitudes = [1.0 / np.sqrt(len(states))] * len(states)

        result = np.zeros(self.dimension, dtype=np.complex128)
        for state, amp in zip(states, amplitudes):
            result += amp * state
        return self.normalize(result)

    def create_basis_state(self, n: int) -> np.ndarray:
        """Create the nth basis state |n>."""
        state = np.zeros(self.dimension, dtype=np.complex128)
        state[n % self.dimension] = 1.0
        return state

    def evolve(self, psi: np.ndarray, hamiltonian: np.ndarray,
               time: float = 1.0) -> np.ndarray:
        """
        Time evolution: |psi(t)> = exp(-iHt)|psi(0)>

        In Advaita: Brahman doesn't evolve (it's timeless).
        But the *appearance* evolves through Maya's dynamics.
        The Hamiltonian encodes Maya's rules of transformation.
        """
        U = expm(-1j * hamiltonian * time)
        return self.normalize(U @ psi)

    def demonstrate_quantum_advaita(self) -> dict:
        """
        Demonstrate key quantum-Advaita correspondences.
        """
        brahman = self.brahman_state
        rho_brahman = self.density_matrix(brahman)
        entropy_brahman = self.von_neumann_entropy(rho_brahman)

        # Create an entangled state (Bell state analogue)
        dim_sub = int(np.sqrt(self.dimension))
        psi_entangled = np.zeros(dim_sub * dim_sub, dtype=np.complex128)
        for i in range(dim_sub):
            psi_entangled[i * dim_sub + i] = 1.0 / np.sqrt(dim_sub)

        rho_entangled = self.density_matrix(psi_entangled)
        rho_reduced = self.partial_trace(rho_entangled, dim_sub, dim_sub)
        entropy_reduced = self.von_neumann_entropy(rho_reduced)

        return {
            "brahman_entropy": entropy_brahman,
            "brahman_is_pure": entropy_brahman < 1e-10,
            "insight_1": "Brahman (the whole) is a pure state — zero entropy, "
                         "complete knowledge, nothing hidden",
            "entangled_subsystem_entropy": entropy_reduced,
            "subsystem_appears_mixed": entropy_reduced > 0.1,
            "insight_2": "When you look at only PART of an entangled whole, "
                         "it appears mixed/random — this IS Maya. "
                         "Ignorance = looking at the part, not the whole.",
            "resolution": "See the whole → entropy vanishes → Maya dissolves → Moksha",
        }
