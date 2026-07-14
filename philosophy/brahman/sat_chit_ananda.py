"""
Sat-Chit-Ananda — The Three Aspects of Brahman

    Sat   = Existence / Being / Truth
    Chit  = Consciousness / Awareness / Knowledge
    Ananda = Bliss / Fullness / Completeness

These are not three separate properties but three ways of pointing
at the same indivisible reality.
"""

import numpy as np
from .consciousness import Brahman


class SatChitAnanda:
    """
    The triple description of Brahman's nature.

    Not three attributes added to Brahman, but three lenses
    through which the one reality is apprehended.

    Computationally: three orthogonal projections of the same field,
    each revealing a different aspect while the source remains one.
    """

    def __init__(self, brahman: Brahman):
        self.brahman = brahman
        self._field = brahman.field

    def sat(self) -> np.ndarray:
        """
        Sat — Pure Existence.

        The fact that anything IS at all. The amplitude of the field.
        Not what exists, but THAT existence exists.
        """
        return np.abs(self._field)

    def chit(self) -> np.ndarray:
        """
        Chit — Pure Consciousness.

        The knowing aspect. The phase relationships in the field
        that encode self-referential structure.
        """
        return np.angle(self._field)

    def ananda(self) -> float:
        """
        Ananda — Bliss / Fullness.

        The completeness of Brahman — nothing is missing, nothing is extra.
        Measured as the coherence of the field: maximum when perfectly unified.
        """
        return self.brahman.coherence()

    def unity_check(self) -> dict:
        """
        Verify that Sat, Chit, and Ananda are aspects of one reality.

        If we can reconstruct the original field from Sat (magnitude)
        and Chit (phase), it proves they describe the same thing.
        """
        magnitude = self.sat()
        phase = self.chit()
        reconstructed = magnitude * np.exp(1j * phase)

        error = np.max(np.abs(reconstructed - self._field))

        return {
            "sat_mean": float(np.mean(magnitude)),
            "chit_range": (float(np.min(phase)), float(np.max(phase))),
            "ananda": self.ananda(),
            "reconstruction_error": float(error),
            "is_unified": error < 1e-10,
        }

    def __repr__(self) -> str:
        check = self.unity_check()
        return (
            f"SatChitAnanda(\n"
            f"  sat={check['sat_mean']:.6f},\n"
            f"  chit_range={check['chit_range']},\n"
            f"  ananda={check['ananda']:.6f},\n"
            f"  unified={check['is_unified']}\n"
            f")"
        )
