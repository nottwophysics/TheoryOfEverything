"""
Vyavaharika — The Empirical Level of Reality

The everyday world of experience. This is where:
- Physics operates (laws of nature, cause and effect)
- Individual selves (jivas) exist and interact
- God (Ishvara) governs the cosmos
- Karma and dharma have meaning
- Science, ethics, and daily life are valid

This level is not "false" — it is valid within its own frame.
It is only sublated from the Paramarthika (absolute) perspective.

Analogy: dream objects are real within the dream.
"""

import numpy as np
from brahman.consciousness import Brahman
from maya.gunas import Gunas, GunaBalance


class Vyavaharika:
    """
    The empirical world — reality as experienced by embodied beings.

    This is the level at which a 'Theory of Everything' in physics
    would operate. It describes the patterns and regularities within
    the appearance, not the ultimate nature of what appears.
    """

    def __init__(self, brahman: Brahman = None, guna_balance: GunaBalance = None):
        self.brahman = brahman or Brahman()
        self.gunas = Gunas(guna_balance or GunaBalance(0.5, 0.3, 0.2))
        self.time_step = 0
        self._state = None

    def simulate(self, steps: int = 1) -> dict:
        """
        Run one or more steps of the empirical world simulation.

        The empirical world evolves — things change, causes produce effects,
        entities interact. All of this is valid at this level.
        """
        field = self.brahman.field

        for _ in range(steps):
            # Gunas evolve — the experiential quality shifts
            self.gunas.evolve(dt=0.1)

            # Apply guna transformation to the field
            self._state = self.gunas.apply_to_field(field)
            self.time_step += 1

        return {
            "time_step": self.time_step,
            "guna_state": self.gunas.balance.dominant.value,
            "sattva": self.gunas.balance.sattva,
            "rajas": self.gunas.balance.rajas,
            "tamas": self.gunas.balance.tamas,
            "field_energy": float(np.sum(np.abs(self._state) ** 2)),
            "field_entropy": self._entropy(self._state),
            "num_apparent_entities": self._count_entities(self._state),
        }

    def get_state(self) -> np.ndarray:
        """Current state of the empirical world."""
        if self._state is None:
            self.simulate(1)
        return self._state

    def physics_laws(self) -> dict:
        """
        The laws that govern this level.
        These are the regularities that physics discovers.
        """
        return {
            "conservation": "Energy is conserved (field norm is constant)",
            "causation": "Events have causes (guna dynamics are deterministic given state)",
            "locality": "Nearby regions interact more strongly",
            "symmetry": "The underlying field has translational symmetry",
            "note": "These laws are valid here but are patterns within Maya, "
                    "not absolute truths about Brahman",
        }

    @staticmethod
    def _entropy(field: np.ndarray) -> float:
        """Shannon entropy of the field's probability distribution."""
        probs = np.abs(field) ** 2
        total = np.sum(probs)
        if total == 0:
            return 0.0
        probs = probs / total
        probs = probs[probs > 0]
        return float(-np.sum(probs * np.log2(probs)))

    @staticmethod
    def _count_entities(field: np.ndarray) -> int:
        """Count apparent distinct entities (peaks in the field)."""
        if len(field) < 3:
            return 0
        # Find local maxima
        peaks = 0
        for i in range(1, len(field) - 1):
            if field[i] > field[i - 1] and field[i] > field[i + 1]:
                peaks += 1
        return peaks
