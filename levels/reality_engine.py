"""
Reality Engine — The Three-Level Framework

Orchestrates the three levels of reality and demonstrates
how each sublates (negates) the one below it.
"""

from .paramarthika import Paramarthika
from .vyavaharika import Vyavaharika
from .pratibhasika import Pratibhasika
from brahman.consciousness import Brahman


class RealityEngine:
    """
    Three nested levels of reality, each valid within its own scope.

    Paramarthika (Absolute) sublates Vyavaharika (Empirical)
    Vyavaharika (Empirical) sublates Pratibhasika (Illusory)
    """

    def __init__(self):
        self.brahman = Brahman()
        self.paramarthika = Paramarthika()
        self.vyavaharika = Vyavaharika(self.brahman)
        self.pratibhasika = Pratibhasika()

    def observe(self, observer_state: str = "waking") -> dict:
        """
        What is observed depends on the state of the observer.

        'liberated'  → sees only Brahman (Paramarthika)
        'waking'     → sees the empirical world (Vyavaharika)
        'dreaming'   → sees dream projections (Pratibhasika)
        """
        if observer_state == "liberated":
            return {
                "level": "Paramarthika",
                "view": self.paramarthika.view(),
                "field": self.paramarthika.pure_awareness(),
            }
        elif observer_state == "waking":
            return {
                "level": "Vyavaharika",
                "view": self.vyavaharika.simulate(),
                "physics_valid": True,
                "ultimately_real": False,
            }
        elif observer_state == "dreaming":
            return {
                "level": "Pratibhasika",
                "view": self.pratibhasika.generate_dream(self.brahman.field),
                "seems_real": True,
                "is_real": False,
            }
        else:
            raise ValueError(f"Unknown observer state: {observer_state}")

    def demonstrate_sublation(self) -> dict:
        """
        Show how each level sublates the one below.

        Waking sublates dreaming → dream snake vanishes
        Self-knowledge sublates waking → empirical world is seen as Brahman
        """
        # Level 1: Dream
        dream = self.pratibhasika.generate_dream(self.brahman.field)

        # Level 2: Wake up — dream is sublated
        waking = self.pratibhasika.wake_up()
        empirical = self.vyavaharika.simulate()

        # Level 3: Self-knowledge — empirical is sublated
        absolute = self.paramarthika.sublate(empirical)

        return {
            "step_1_dreaming": {
                "experience": dream,
                "status": "seems real while dreaming",
            },
            "step_2_waking": {
                "dream_sublated": waking,
                "empirical_view": empirical,
                "status": "dream recognized as unreal; waking world seems real",
            },
            "step_3_liberation": {
                "empirical_sublated": absolute,
                "status": "waking world recognized as appearance in Brahman",
            },
            "teaching": (
                "Each level is valid from within, but recognized as "
                "appearance from the level above. Only Paramarthika "
                "(Brahman) is never sublated."
            ),
        }

    def compare_levels(self) -> dict:
        """Side-by-side comparison of all three levels."""
        return {
            "paramarthika": {
                "ontology": "Only Brahman exists",
                "epistemology": "Direct non-dual awareness (Anubhava)",
                "sublated_by": "Nothing — this is the final truth",
                "analogy": "The screen on which the movie plays",
            },
            "vyavaharika": {
                "ontology": "Many objects, beings, and forces exist",
                "epistemology": "Perception, inference, testimony",
                "sublated_by": "Paramarthika (Self-knowledge)",
                "analogy": "The movie — real while watching, but just light on a screen",
            },
            "pratibhasika": {
                "ontology": "Dream/illusory objects appear to exist",
                "epistemology": "Confused perception",
                "sublated_by": "Vyavaharika (waking up)",
                "analogy": "A dream within the movie",
            },
        }
