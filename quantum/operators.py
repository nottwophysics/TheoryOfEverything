"""
Quantum Operators as Aspects of Maya and Consciousness

    Consciousness Operator  → Generates awareness (Chit aspect)
    Maya Operator           → Projects infinite into finite
    Sakshi Projector        → The measurement/witness operator
    Creation/Annihilation   → Nama-Rupa (name-form manifestation)
"""

import numpy as np
from scipy.linalg import expm


class ConsciousnessOperator:
    """
    The fundamental operator — consciousness acting on itself.

    In QM: every observable is a Hermitian operator.
    In Advaita: every experience is consciousness knowing itself
    through a particular mode (operator).

    Consciousness IS the operator, the operand, and the result.
    """

    def __init__(self, dimension: int = 64):
        self.dimension = dimension

    def identity(self) -> np.ndarray:
        """
        The identity operator — Brahman as pure being.
        Acts on everything, changes nothing.
        The 'do-nothing' operator IS the ground of all doing.
        """
        return np.eye(self.dimension, dtype=np.complex128)

    def awareness_operator(self) -> np.ndarray:
        """
        The Chit operator — consciousness aware of itself.

        Modeled as a Hermitian matrix whose eigenstates are
        the 'modes of knowing.' Self-adjoint because the knower
        and the known are the same.
        """
        H = np.zeros((self.dimension, self.dimension), dtype=np.complex128)
        for i in range(self.dimension):
            H[i, i] = i + 1  # Energy levels = degrees of differentiation
            if i + 1 < self.dimension:
                coupling = np.sqrt(i + 1) * 0.1
                H[i, i + 1] = coupling
                H[i + 1, i] = coupling  # Hermitian
        return H

    def creation_operator(self) -> np.ndarray:
        """
        a† — Creation operator.

        In Advaita: Srishti (creation/manifestation).
        Each application adds one quantum of nama-rupa
        (one more distinction in the field).
        """
        a_dag = np.zeros((self.dimension, self.dimension), dtype=np.complex128)
        for i in range(self.dimension - 1):
            a_dag[i + 1, i] = np.sqrt(i + 1)
        return a_dag

    def annihilation_operator(self) -> np.ndarray:
        """
        a — Annihilation operator.

        In Advaita: Laya (dissolution).
        Each application removes one quantum of nama-rupa
        (one less distinction — moving toward unity).
        """
        a = np.zeros((self.dimension, self.dimension), dtype=np.complex128)
        for i in range(self.dimension - 1):
            a[i, i + 1] = np.sqrt(i + 1)
        return a

    def number_operator(self) -> np.ndarray:
        """
        N = a†a — The number operator.

        Counts the degree of manifestation.
        N=0: vacuum (unmanifest Brahman)
        N=large: highly manifested (deep Maya)
        """
        a_dag = self.creation_operator()
        a = self.annihilation_operator()
        return a_dag @ a

    def hamiltonian(self, coupling_strength: float = 0.1) -> np.ndarray:
        """
        The Hamiltonian — generator of time evolution.

        In Advaita: Maya's dynamics. The rules by which
        the appearance evolves. Brahman itself is timeless,
        but the Hamiltonian governs the appearance of change.
        """
        N = self.number_operator()
        a = self.annihilation_operator()
        a_dag = self.creation_operator()

        # Harmonic oscillator + self-interaction
        # Self-interaction models Maya's self-reinforcing nature
        H = N + 0.5 * self.identity()
        H += coupling_strength * (a_dag @ a_dag @ a @ a)  # Self-interaction
        return H


class MayaOperator:
    """
    Maya as a quantum operator — projecting the infinite into the finite.

    Maya is not a unitary operator (information is 'lost' / concealed).
    It is a projection operator: P² = P (idempotent).
    Applying Maya twice doesn't double the illusion.
    """

    def __init__(self, dimension: int = 64):
        self.dimension = dimension

    def avarana(self, concealment_depth: int = None) -> np.ndarray:
        """
        Avarana Shakti — the concealing power of Maya.

        Projects the full Hilbert space onto a subspace,
        hiding the rest. The concealed dimensions don't
        cease to exist — they just become invisible.
        """
        if concealment_depth is None:
            concealment_depth = self.dimension // 2

        P = np.zeros((self.dimension, self.dimension), dtype=np.complex128)
        visible = min(concealment_depth, self.dimension)
        for i in range(visible):
            P[i, i] = 1.0

        return P

    def vikshepa(self, projection_seed: int = 42) -> np.ndarray:
        """
        Vikshepa Shakti — the projecting power of Maya.

        After concealment, the mind projects patterns onto
        the reduced space. This is a non-trivial transformation
        within the visible subspace.
        """
        rng = np.random.RandomState(projection_seed)
        # Random unitary in the visible subspace
        A = rng.randn(self.dimension, self.dimension) + \
            1j * rng.randn(self.dimension, self.dimension)
        Q, _ = np.linalg.qr(A)
        return Q

    def full_maya(self, concealment_depth: int = None,
                  projection_seed: int = 42) -> np.ndarray:
        """
        Full Maya = Avarana (conceal) + Vikshepa (project).

        First hide the totality, then project forms onto what remains.
        """
        P = self.avarana(concealment_depth)
        U = self.vikshepa(projection_seed)
        return P @ U

    def measure_maya_depth(self, operator: np.ndarray) -> float:
        """
        How much Maya is active? Measured by rank deficiency.

        rank(M) / dimension:
            1.0 = no Maya (full rank, nothing concealed)
            0.0 = total Maya (everything concealed)
        """
        rank = np.linalg.matrix_rank(operator)
        return 1.0 - rank / self.dimension


class SakshiProjector:
    """
    The Witness as a measurement operator.

    In QM: measurement projects a superposition onto an eigenstate.
    In Advaita: the Sakshi illuminates without choosing.

    Key difference from standard QM:
    - Standard QM: measurement disturbs the system
    - Advaita: the witness illuminates without disturbance
    - Resolution: what's disturbed is the ego's interpretation,
      not consciousness itself
    """

    def __init__(self, dimension: int = 64):
        self.dimension = dimension

    def projector(self, basis_index: int) -> np.ndarray:
        """
        |n><n| — Project onto a specific basis state.

        This is what 'measurement' does: collapses the superposition
        to a definite outcome.
        """
        state = np.zeros(self.dimension, dtype=np.complex128)
        state[basis_index % self.dimension] = 1.0
        return np.outer(state, state.conj())

    def witness(self, psi: np.ndarray) -> dict:
        """
        The Sakshi witnesses all possibilities without collapsing them.

        Returns the probability distribution over all outcomes
        WITHOUT performing a collapse. This is pure awareness
        seeing the full picture.
        """
        probabilities = np.abs(psi) ** 2
        entropy = -np.sum(probabilities[probabilities > 0] *
                         np.log(probabilities[probabilities > 0]))

        return {
            "probabilities": probabilities,
            "entropy": float(entropy),
            "num_active_modes": int(np.sum(probabilities > 1e-10)),
            "most_probable": int(np.argmax(probabilities)),
            "sakshi_modified": False,  # Witness never changes
            "insight": "The witness sees all possibilities simultaneously. "
                       "Only ego-identification collapses to one.",
        }

    def ego_measurement(self, psi: np.ndarray, seed: int = None) -> dict:
        """
        Ego-based measurement — collapses the superposition.

        Unlike the Sakshi, the ego identifies with a particular
        outcome. This is the 'measurement problem' — and in Advaita,
        it IS the fundamental problem of bondage.
        """
        probabilities = np.abs(psi) ** 2
        probabilities = probabilities / np.sum(probabilities)

        rng = np.random.RandomState(seed)
        outcome = rng.choice(self.dimension, p=probabilities)

        collapsed = np.zeros(self.dimension, dtype=np.complex128)
        collapsed[outcome] = 1.0

        return {
            "outcome": int(outcome),
            "collapsed_state": collapsed,
            "probability": float(probabilities[outcome]),
            "information_lost": True,
            "insight": "The ego 'measures' = identifies with one possibility. "
                       "All other possibilities seem to vanish. "
                       "But they only vanish FOR THE EGO, not for the Sakshi.",
        }
