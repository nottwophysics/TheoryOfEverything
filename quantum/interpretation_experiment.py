"""
The Shared Experiment — A Single Quantum Scenario Run Under All Interpretations

We define ONE physical setup — a Stern-Gerlach-like measurement of a
spin-1/2 particle prepared in a superposition — and ask each interpretation
to account for the same set of phenomena:

    1. Pre-measurement: particle in superposition |ψ⟩ = α|↑⟩ + β|↓⟩
    2. Measurement: particle interacts with apparatus
    3. Outcome: a definite result is observed (↑ or ↓)
    4. Statistics: over many trials, Born rule probabilities emerge
    5. Entanglement: two particles in Bell state show non-local correlations
    6. Delayed choice: measurement basis chosen after particle is in flight
    7. Wigner's friend: observer inside a sealed lab measures; outside observer describes lab as superposition
    8. Consciousness: why does measurement produce a subjective experience of ONE outcome?

Each interpretation must answer ALL eight phenomena.
The comparison is then: how many axioms, how much explanatory scope,
and what novel predictions (if any).
"""

import numpy as np
from dataclasses import dataclass, field


# ============================================================
# The Physical Setup
# ============================================================

@dataclass
class QuantumSetup:
    """The shared physical scenario all interpretations must explain."""

    # Spin-1/2 system
    spin_up: np.ndarray = field(default_factory=lambda: np.array([1, 0], dtype=np.complex128))
    spin_down: np.ndarray = field(default_factory=lambda: np.array([0, 1], dtype=np.complex128))

    # Prepared state: superposition
    alpha: complex = np.sqrt(0.7) + 0j
    beta: complex = np.sqrt(0.3) + 0j

    def prepared_state(self) -> np.ndarray:
        """α|↑⟩ + β|↓⟩"""
        return self.alpha * self.spin_up + self.beta * self.spin_down

    def probabilities(self) -> dict:
        """Born rule predictions."""
        return {
            "P(up)": float(abs(self.alpha) ** 2),
            "P(down)": float(abs(self.beta) ** 2),
        }

    def bell_state(self) -> np.ndarray:
        """Entangled Bell state |Φ+⟩ = (|↑↑⟩ + |↓↓⟩)/√2"""
        uu = np.kron(self.spin_up, self.spin_up)
        dd = np.kron(self.spin_down, self.spin_down)
        return (uu + dd) / np.sqrt(2)

    def density_matrix(self, state: np.ndarray) -> np.ndarray:
        return np.outer(state, state.conj())

    def run_many_trials(self, num_trials: int = 10000, seed: int = 42) -> dict:
        """Run the experiment many times and collect statistics."""
        rng = np.random.RandomState(seed)
        p_up = float(abs(self.alpha) ** 2)
        outcomes = rng.choice(["up", "down"], size=num_trials, p=[p_up, 1 - p_up])
        n_up = np.sum(outcomes == "up")
        n_down = num_trials - n_up

        return {
            "num_trials": num_trials,
            "n_up": int(n_up),
            "n_down": int(n_down),
            "freq_up": n_up / num_trials,
            "freq_down": n_down / num_trials,
            "born_rule_up": p_up,
            "born_rule_down": 1 - p_up,
            "deviation": abs(n_up / num_trials - p_up),
        }


# ============================================================
# The Eight Phenomena Every Interpretation Must Address
# ============================================================

PHENOMENA = {
    "P1_superposition": {
        "question": "What IS the superposition α|↑⟩ + β|↓⟩ before measurement?",
        "observable": "Interference patterns confirm superposition is real, not classical mixture",
    },
    "P2_measurement": {
        "question": "What physically happens during measurement?",
        "observable": "A definite outcome (↑ or ↓) is always obtained",
    },
    "P3_born_rule": {
        "question": "Why does P(outcome) = |amplitude|²?",
        "observable": "Statistical frequencies match Born rule over many trials",
    },
    "P4_entanglement": {
        "question": "How do entangled particles show non-local correlations?",
        "observable": "Bell inequality violated (S = 2√2), ruling out local hidden variables",
    },
    "P5_delayed_choice": {
        "question": "How can a future measurement choice affect past behavior?",
        "observable": "Wheeler's delayed-choice experiment confirms retrocausal-like effects",
    },
    "P6_wigners_friend": {
        "question": "If a friend measures inside a sealed lab, is the lab in superposition for you?",
        "observable": "No consensus — this is where interpretations diverge most sharply",
    },
    "P7_preferred_basis": {
        "question": "Why does measurement happen in the position/momentum basis and not some arbitrary basis?",
        "observable": "Decoherence selects a preferred basis via environment interaction",
    },
    "P8_consciousness": {
        "question": "Why does measurement produce a subjective experience of ONE outcome?",
        "observable": "Every observer reports experiencing exactly one definite outcome",
    },
}
