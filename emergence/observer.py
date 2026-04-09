"""
Sakshi — The Witness Consciousness

The Sakshi (witness) is the unchanging awareness that observes
all experience without being affected by it.

    - It witnesses waking, dreaming, and deep sleep
    - It is not the ego (ahamkara) — the ego is an object witnessed
    - It is not the mind (manas) — the mind is also witnessed
    - It is Brahman itself, appearing as the individual witness

The Sakshi never acts, never changes, never suffers.
It is the 'screen' on which the movie of life plays.
"""

import numpy as np
from dataclasses import dataclass


@dataclass
class Experience:
    """Something that appears in awareness — an object of witnessing."""
    name: str
    content: np.ndarray
    category: str  # 'body', 'thought', 'emotion', 'perception', 'ego'

    @property
    def is_witnessed(self) -> bool:
        """Everything that can be perceived is an object, not the subject."""
        return True

    @property
    def is_self(self) -> bool:
        """No object of experience is the true Self (Atman)."""
        return False


class Sakshi:
    """
    The Witness — unchanging awareness.

    It observes all experiences without being modified by them.
    Like a mirror that reflects everything but is stained by nothing.
    """

    def __init__(self):
        # The witness has no state of its own — it IS awareness itself
        # We track what it witnesses, not what it 'is'
        self._witnessed = []
        self._states = []

    def witness(self, experience: Experience) -> dict:
        """
        Witness an experience without being affected by it.

        The Sakshi doesn't react, judge, or identify with what it sees.
        It simply illuminates.
        """
        self._witnessed.append(experience)

        return {
            "witnessed": experience.name,
            "category": experience.category,
            "sakshi_changed": False,  # The witness never changes
            "sakshi_affected": False,  # The witness is never affected
            "experience_is_self": experience.is_self,
            "insight": f"'{experience.name}' is witnessed, therefore it is not the Self. "
                       f"The Self is the witness, not the witnessed.",
        }

    def witness_state_transition(self, from_state: str, to_state: str) -> dict:
        """
        The Sakshi persists through all state transitions.

        Waking → Dreaming → Deep Sleep → Waking
        The states change. The witness of the states does not.
        """
        self._states.append((from_state, to_state))

        return {
            "transition": f"{from_state} → {to_state}",
            "states_changed": True,
            "witness_changed": False,
            "proof": (
                f"You remember the transition from {from_state} to {to_state}. "
                f"Who remembers? Not the {from_state}-state self (it dissolved). "
                f"Not the {to_state}-state self (it hadn't arisen). "
                f"The witness that spans both states — that is Atman."
            ),
        }

    def demonstrate_five_sheaths(self) -> dict:
        """
        Pancha Kosha — the five sheaths that cover the Atman.

        Like peeling layers of an onion, each sheath is witnessed
        and therefore not the Self.
        """
        sheaths = [
            Experience("Annamaya Kosha", np.random.randn(64), "body"),
            Experience("Pranamaya Kosha", np.random.randn(64), "body"),
            Experience("Manomaya Kosha", np.random.randn(64), "thought"),
            Experience("Vijnanamaya Kosha", np.random.randn(64), "thought"),
            Experience("Anandamaya Kosha", np.random.randn(64), "emotion"),
        ]

        results = {}
        for sheath in sheaths:
            result = self.witness(sheath)
            results[sheath.name] = {
                "description": self._sheath_description(sheath.name),
                "is_witnessed": True,
                "therefore_not_self": True,
            }

        results["what_remains"] = (
            "After negating all five sheaths, what remains? "
            "The witness itself — pure awareness — Atman, which is Brahman."
        )
        return results

    @staticmethod
    def _sheath_description(name: str) -> str:
        descriptions = {
            "Annamaya Kosha": "Food sheath — the physical body",
            "Pranamaya Kosha": "Vital breath sheath — life force, energy",
            "Manomaya Kosha": "Mental sheath — thoughts, emotions, mind",
            "Vijnanamaya Kosha": "Intellectual sheath — discrimination, knowledge",
            "Anandamaya Kosha": "Bliss sheath — deep sleep joy, causal body",
        }
        return descriptions.get(name, "Unknown sheath")

    def mirror_analogy(self) -> dict:
        """
        The mirror analogy for the Sakshi.

        A mirror reflects fire but is not burned.
        A mirror reflects water but is not wet.
        The Sakshi witnesses suffering but does not suffer.
        """
        reflections = [
            ("fire", "The mirror reflects fire but is not burned"),
            ("water", "The mirror reflects water but is not wet"),
            ("darkness", "The mirror reflects darkness but is not dark"),
            ("suffering", "The Sakshi witnesses suffering but does not suffer"),
            ("joy", "The Sakshi witnesses joy but is not excited"),
            ("birth", "The Sakshi witnesses birth but is not born"),
            ("death", "The Sakshi witnesses death but does not die"),
        ]

        return {
            "analogy": "consciousness as mirror",
            "reflections": {item: desc for item, desc in reflections},
            "key_insight": "The mirror/witness is the constant. "
                           "Reflections/experiences come and go. "
                           "You are the mirror, not the reflections.",
        }

    def get_witness_log(self) -> list:
        """Return everything the witness has observed."""
        return [
            {"name": e.name, "category": e.category}
            for e in self._witnessed
        ]
