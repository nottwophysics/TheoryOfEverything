"""
Paramarthika — The Absolute Level of Reality

The highest truth: only Brahman exists.
No world, no individual self, no God — just non-dual awareness.

From this level, Maya itself is neither real nor unreal (anirvachaniya).
The world doesn't need to be destroyed or escaped —
it was never there as an independent reality.
"""

import numpy as np
from philosophy.brahman.consciousness import Brahman


class Paramarthika:
    """
    The absolute level of reality.

    At this level, all distinctions collapse. There is no observer
    and observed, no subject and object, no cause and effect.
    Just seamless, infinite awareness.
    """

    def __init__(self):
        self.brahman = Brahman()

    def view(self) -> dict:
        """
        What is seen from the absolute perspective.
        """
        return {
            "reality": "Brahman alone",
            "world": "not independently real",
            "self": "identical with Brahman",
            "god": "Brahman without attributes (Nirguna)",
            "maya": "anirvachaniya (neither real nor unreal)",
            "field_coherence": self.brahman.coherence(),
            "non_dual": self.brahman.is_non_dual(),
        }

    def pure_awareness(self) -> np.ndarray:
        """
        Return the undifferentiated field — Brahman as-is.
        No names, no forms, no distinctions.
        """
        return self.brahman.field

    def sublate(self, lower_level_view: dict) -> dict:
        """
        Badha (sublation) — the higher level negates the lower.

        Just as waking sublates the dream (the dream world is
        recognized as unreal), the absolute sublates the empirical.
        """
        return {
            "sublated": lower_level_view,
            "revealed": "All apparent multiplicity was Brahman alone",
            "analogy": "As dream objects dissolve upon waking, "
                       "empirical objects dissolve in Self-knowledge",
        }
