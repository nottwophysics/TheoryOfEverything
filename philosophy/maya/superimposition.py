"""
Adhyasa (Superimposition) — The Core Mechanism of Maya

Shankaracharya's Adhyasa Bhashya identifies superimposition as the
fundamental error: projecting the attributes of one thing onto another.

    - Rope seen as snake (Rajju-Sarpa)
    - Brahman seen as world
    - Self seen as body/mind

The substrate is always there. Only the projection changes based
on the degree of ignorance (Avidya).
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional


@dataclass
class SuperimposedObject:
    """An object that appears to be one thing but is actually another."""
    apparent: np.ndarray      # What you perceive (snake / world)
    actual: np.ndarray        # What is really there (rope / Brahman)
    ignorance_level: float    # How much concealment is active
    projection_pattern: str   # What pattern was projected

    @property
    def is_real(self) -> bool:
        """Superimposed objects are never independently real."""
        return False

    @property
    def error_magnitude(self) -> float:
        """How far the appearance is from reality."""
        return float(np.linalg.norm(self.apparent - self.actual))

    def recognize(self) -> np.ndarray:
        """
        Sublation (Badha) — recognizing what was actually there all along.
        The snake 'becomes' the rope. The world 'becomes' Brahman.
        Nothing changes in reality — only the perception corrects.
        """
        return self.actual


class Adhyasa:
    """
    The superimposition engine.

    Models how ignorance (avidya) of the substrate leads to
    projection of familiar patterns onto it.
    """

    def __init__(self, memory_patterns: Optional[dict] = None):
        """
        memory_patterns: dict of name -> np.ndarray
        These represent vasanas (latent impressions) that the mind
        projects onto ambiguous stimuli.
        """
        self.memory_patterns = memory_patterns or self._default_patterns()
        self.clarity_threshold = 0.7

    @staticmethod
    def _default_patterns() -> dict:
        """Default projection patterns — common forms the mind imposes."""
        np.random.seed(42)
        return {
            "snake": np.random.randn(256) * 0.3 + np.sin(np.linspace(0, 4 * np.pi, 256)),
            "water": np.random.randn(256) * 0.1 + np.cos(np.linspace(0, 2 * np.pi, 256)),
            "silver": np.random.randn(256) * 0.2 + 0.8,
            "self_as_body": np.random.randn(256) * 0.5,
            "world_as_real": np.random.randn(256) * 0.4 + 0.5,
        }

    def superimpose(
        self,
        substrate: np.ndarray,
        ignorance_level: float = 0.8,
        pattern_name: Optional[str] = None,
    ) -> SuperimposedObject:
        """
        Apply superimposition to a substrate.

        When ignorance is high, the mind projects familiar patterns.
        When ignorance is low, the substrate is seen as-is.

        Args:
            substrate: The actual reality (rope / Brahman field)
            ignorance_level: 0.0 (clear seeing) to 1.0 (total concealment)
            pattern_name: Which pattern to project (random if None)
        """
        ignorance_level = np.clip(ignorance_level, 0.0, 1.0)

        # Step 1: Avarana — concealment. Ignorance hides the true nature.
        perception = substrate * (1.0 - ignorance_level)

        # Step 2: Check if perception is clear enough to see the truth
        perception_clarity = 1.0 - ignorance_level
        if perception_clarity >= self.clarity_threshold:
            # Clear perception — no superimposition occurs
            return SuperimposedObject(
                apparent=substrate,
                actual=substrate,
                ignorance_level=ignorance_level,
                projection_pattern="none (clear seeing)",
            )

        # Step 3: Vikshepa — projection. Mind fills gaps with patterns.
        if pattern_name is None:
            pattern_name = self._best_match(perception)

        pattern = self.memory_patterns.get(pattern_name, np.zeros_like(substrate))
        # Resize pattern to match substrate if needed
        if len(pattern) != len(substrate):
            pattern = np.interp(
                np.linspace(0, 1, len(substrate)),
                np.linspace(0, 1, len(pattern)),
                pattern,
            )

        # The appearance is a blend: faint perception + projected pattern
        apparent = perception + ignorance_level * pattern

        return SuperimposedObject(
            apparent=apparent,
            actual=substrate,
            ignorance_level=ignorance_level,
            projection_pattern=pattern_name,
        )

    def _best_match(self, partial_perception: np.ndarray) -> str:
        """Find the memory pattern most similar to the partial perception."""
        best_name = "world_as_real"
        best_score = -np.inf

        for name, pattern in self.memory_patterns.items():
            if len(pattern) != len(partial_perception):
                pattern = np.interp(
                    np.linspace(0, 1, len(partial_perception)),
                    np.linspace(0, 1, len(pattern)),
                    pattern,
                )
            score = float(np.dot(partial_perception, pattern))
            if score > best_score:
                best_score = score
                best_name = name

        return best_name

    def rope_snake_demo(self, rope_length: int = 256) -> dict:
        """
        Classic demonstration of Adhyasa.

        A rope in dim light is mistaken for a snake.
        As light increases (ignorance decreases), the snake
        'becomes' the rope — nothing changed except perception.
        """
        rope = np.sin(np.linspace(0, 2 * np.pi, rope_length)) * 0.3 + 0.5
        results = {}

        for ignorance in [0.95, 0.8, 0.6, 0.4, 0.2, 0.05]:
            result = self.superimpose(rope, ignorance, "snake")
            results[f"ignorance_{ignorance:.2f}"] = {
                "sees": result.projection_pattern,
                "error": result.error_magnitude,
                "is_real": result.is_real,
            }

        return results
