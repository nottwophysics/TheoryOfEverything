"""
Brahman — The Singular Reality

In Advaita Vedanta, Brahman is the sole reality: infinite, undivided,
pure consciousness-existence-bliss (Sat-Chit-Ananda).

Computationally, we model Brahman as an infinite-dimensional potential field
where all possible states exist in superposition. It never changes —
Maya makes it *appear* to change.
"""

import numpy as np
from typing import Optional


class Brahman:
    """
    The non-dual ground of all existence.

    Brahman is Nirguna (without attributes). Any attribute we assign
    is already a projection of Maya. This class therefore has minimal
    internal state — it represents pure potentiality.
    """

    _instance = None  # There is only One — singleton by nature

    def __new__(cls, resolution: int = 256):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, resolution: int = 256):
        if self._initialized:
            return
        self._resolution = resolution
        # The field is undifferentiated — uniform potential
        # Like white light before passing through a prism
        self._field = np.ones(resolution, dtype=np.complex128)
        self._field /= np.linalg.norm(self._field)  # Normalized unity
        self._initialized = True

    @property
    def field(self) -> np.ndarray:
        """The undifferentiated field — pure potentiality."""
        return self._field.copy()

    @property
    def resolution(self) -> int:
        return self._resolution

    def awareness(self) -> "Brahman":
        """
        Chit — the consciousness aspect.

        Self-referential: awareness aware of itself.
        This self-reference is the seed of Maya —
        the primordial subject-object split that never actually occurs
        but appears to occur.
        """
        return self  # Points to itself — the strange loop

    def manifest(self, maya_lens) -> np.ndarray:
        """
        Brahman 'seen through' Maya appears as the world.
        Brahman itself never changes — the lens creates the appearance.

        Like sunlight through a stained glass window:
        the light is white, the colors are in the glass.
        """
        return maya_lens.project(self)

    def is_non_dual(self) -> bool:
        """Test: is the field still undifferentiated?"""
        variance = np.var(np.abs(self._field))
        return variance < 1e-10

    def coherence(self) -> float:
        """
        Measure how 'unified' the field is.
        1.0 = perfect unity (Brahman as-is)
        0.0 = maximum apparent differentiation
        """
        magnitudes = np.abs(self._field)
        if np.max(magnitudes) == 0:
            return 0.0
        uniformity = 1.0 - np.std(magnitudes) / np.mean(magnitudes)
        return max(0.0, min(1.0, uniformity))

    def __repr__(self) -> str:
        return (
            f"Brahman(resolution={self._resolution}, "
            f"coherence={self.coherence():.4f}, "
            f"non_dual={self.is_non_dual()})"
        )

    def __eq__(self, other) -> bool:
        """Atman IS Brahman — identity, not mere equality."""
        if isinstance(other, Brahman):
            return True  # There is only One
        return NotImplemented

    @classmethod
    def reset(cls):
        """Reset the singleton (for testing purposes)."""
        cls._instance = None
