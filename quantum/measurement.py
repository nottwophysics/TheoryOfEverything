"""
The Measurement Problem — Dissolved by Advaita

The measurement problem asks: why does superposition collapse?

Advaita answer: it doesn't. The total system (Brahman) stays
in superposition. The *appearance* of collapse arises because
the observer (jiva) is entangled with the system, creating a
reduced perspective where only one outcome is seen.

Collapse = Maya's partial view of a non-dual whole.
"""

import numpy as np


class AdvaiticMeasurement:
    """
    Measurement as entanglement + partial tracing.

    No collapse postulate needed. Decoherence + the Advaitic
    framework explains the appearance of definite outcomes.
    """

    def __init__(self, system_dim: int = 4, environment_dim: int = 16):
        self.system_dim = system_dim
        self.env_dim = environment_dim
        self.total_dim = system_dim * environment_dim

    def create_superposition(self) -> np.ndarray:
        """System in equal superposition — Brahman state."""
        psi = np.ones(self.system_dim, dtype=np.complex128)
        return psi / np.linalg.norm(psi)

    def entangle_with_environment(self, system_state: np.ndarray) -> np.ndarray:
        """
        Decoherence: system entangles with environment (Maya).

        |ψ⟩_sys |0⟩_env → Σ cᵢ |i⟩_sys |εᵢ⟩_env

        The environment plays the role of Maya: by interacting
        with everything, it creates the appearance of classicality.
        """
        total = np.zeros(self.total_dim, dtype=np.complex128)

        for i in range(self.system_dim):
            # Each system basis state correlates with a distinct env state
            env_state = np.zeros(self.env_dim, dtype=np.complex128)
            # Orthogonal environment states (decoherence condition)
            env_state[i % self.env_dim] = 1.0

            sys_basis = np.zeros(self.system_dim, dtype=np.complex128)
            sys_basis[i] = 1.0

            total += system_state[i] * np.kron(sys_basis, env_state)

        norm = np.linalg.norm(total)
        if norm > 0:
            total /= norm
        return total

    def brahman_view(self, total_state: np.ndarray) -> dict:
        """
        What Brahman 'sees': the total state — pure, non-dual.
        No collapse. Full superposition intact.
        """
        rho = np.outer(total_state, total_state.conj())
        purity = float(np.real(np.trace(rho @ rho)))

        return {
            "perspective": "Paramarthika (Absolute)",
            "state": "pure superposition",
            "purity": purity,
            "collapsed": False,
            "insight": "From the absolute view, all possibilities coexist. "
                       "There is no measurement problem because there is no collapse.",
        }

    def jiva_view(self, total_state: np.ndarray) -> dict:
        """
        What the individual observer (jiva) sees:
        trace out the environment → reduced density matrix → classical probabilities.

        This IS the 'collapse' — not a physical event, but a
        consequence of limited perspective.
        """
        rho_total = np.outer(total_state, total_state.conj())

        # Partial trace over environment
        rho_system = np.zeros(
            (self.system_dim, self.system_dim), dtype=np.complex128
        )
        for i in range(self.env_dim):
            # Extract the block corresponding to env state |i>
            start = 0
            block = np.zeros((self.system_dim, self.system_dim), dtype=np.complex128)
            for a in range(self.system_dim):
                for b in range(self.system_dim):
                    block[a, b] = rho_total[
                        a * self.env_dim + i,
                        b * self.env_dim + i
                    ]
            rho_system += block

        purity = float(np.real(np.trace(rho_system @ rho_system)))
        probabilities = np.real(np.diag(rho_system)).tolist()

        # Off-diagonal elements (coherence) — should be near zero after decoherence
        off_diag_sum = float(np.sum(np.abs(rho_system - np.diag(np.diag(rho_system)))))

        return {
            "perspective": "Vyavaharika (Empirical)",
            "state": "mixed / classical",
            "purity": purity,
            "probabilities": probabilities,
            "coherence_remaining": off_diag_sum,
            "appears_collapsed": off_diag_sum < 0.01,
            "insight": "The jiva sees classical probabilities — no interference. "
                       "This LOOKS like collapse but is just partial information.",
        }

    def demonstrate_measurement_problem_resolved(self) -> dict:
        """
        Full demonstration: same state, two perspectives.

        Brahman sees: pure superposition (no problem).
        Jiva sees: classical mixture (apparent collapse).

        No new physics needed — just two levels of description
        (Paramarthika vs Vyavaharika).
        """
        system = self.create_superposition()
        total = self.entangle_with_environment(system)

        brahman = self.brahman_view(total)
        jiva = self.jiva_view(total)

        return {
            "system_state": "equal superposition of all basis states",
            "after_decoherence": {
                "brahman_sees": brahman,
                "jiva_sees": jiva,
            },
            "resolution": (
                "The measurement problem assumes collapse is real. "
                "Advaita says: collapse is perspectival. "
                f"Total state purity: {brahman['purity']:.6f} (pure). "
                f"Reduced state purity: {jiva['purity']:.6f} (mixed). "
                "Same reality, two views. No new postulate needed."
            ),
        }
