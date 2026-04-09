"""
Vivartavada — Apparent Transformation

Advaita's theory of causation: the effect is not a real transformation
of the cause but an apparent one.

    Parinamavada: milk really becomes curd (real change)
    Vivartavada:  rope appears as snake (no real change)

Brahman appears as the world without undergoing any real change.
The gold doesn't change when you mold it into a ring — only the
name and form (nama-rupa) change.
"""

import numpy as np
from dataclasses import dataclass


@dataclass
class CausalEvent:
    """An event in the causal chain."""
    cause: np.ndarray
    effect: np.ndarray
    transformation_type: str  # 'apparent' or 'real'
    substrate_changed: bool

    @property
    def substrate_preserved(self) -> float:
        """How much of the original substrate is preserved in the effect."""
        if np.linalg.norm(self.cause) == 0:
            return 0.0
        correlation = np.dot(self.cause[:len(self.effect)], self.effect[:len(self.cause)])
        max_corr = np.linalg.norm(self.cause[:len(self.effect)]) * np.linalg.norm(self.effect[:len(self.cause)])
        if max_corr == 0:
            return 0.0
        return float(abs(correlation / max_corr))


class Vivartavada:
    """
    The doctrine of apparent transformation.

    Models how Brahman appears as the world without undergoing
    any real change — like a movie screen that appears to contain
    fire, water, landscapes, but remains unchanged.
    """

    def __init__(self):
        self.causal_chain = []

    def apparent_transformation(
        self,
        substrate: np.ndarray,
        form_function: callable = None,
    ) -> CausalEvent:
        """
        Apply an apparent transformation.

        The substrate (Brahman/gold/clay) remains unchanged.
        Only the name and form change.

        substrate + form_function → appearance
        """
        if form_function is None:
            # Default: sinusoidal modulation (like waves on the ocean)
            t = np.linspace(0, 4 * np.pi, len(substrate))
            form_function = lambda s: s * (1 + 0.3 * np.sin(t[:len(s)]))

        effect = form_function(substrate)

        event = CausalEvent(
            cause=substrate,
            effect=effect,
            transformation_type="apparent (vivarta)",
            substrate_changed=False,
        )

        self.causal_chain.append(event)
        return event

    def gold_ornament_demo(self, resolution: int = 256) -> dict:
        """
        Classic example: gold → ornament.

        The gold doesn't become something other than gold.
        'Ring', 'necklace', 'bracelet' are names and forms
        imposed on the same gold.
        """
        # Gold: the substrate
        gold = np.ones(resolution) * 0.8  # Uniform substance

        # Different ornament "forms" — same gold, different shapes
        t = np.linspace(0, 2 * np.pi, resolution)
        ornaments = {
            "ring": gold * (1 + 0.3 * np.cos(t * 1)),
            "necklace": gold * (1 + 0.2 * np.cos(t * 8)),
            "bracelet": gold * (1 + 0.4 * np.cos(t * 3)),
            "earring": gold * (1 + 0.5 * np.cos(t * 12)),
        }

        results = {}
        for name, ornament in ornaments.items():
            # How much gold is preserved?
            gold_content = float(np.dot(gold, ornament)) / (
                np.linalg.norm(gold) * np.linalg.norm(ornament)
            )
            results[name] = {
                "form": name,
                "substance": "gold",
                "gold_preserved": gold_content,
                "real_change": False,
                "only_nama_rupa_changed": True,
            }

        results["teaching"] = (
            "All ornaments are gold. Names differ, forms differ, "
            "but the substance is one. Similarly, all objects are Brahman."
        )
        return results

    def ocean_wave_demo(self, resolution: int = 256) -> dict:
        """
        The ocean and its waves.

        Waves appear on the ocean. Each wave seems distinct.
        But every wave IS the ocean — there is no 'wave substance'
        separate from water.
        """
        # Ocean: the substrate
        ocean = np.ones(resolution) * 0.5
        t = np.linspace(0, 10 * np.pi, resolution)

        waves = []
        for i in range(5):
            freq = 2 + i * 1.5
            amplitude = 0.1 + i * 0.05
            wave = ocean + amplitude * np.sin(freq * t + i)
            waves.append(wave)

        # Each wave is made of ocean
        ocean_content = []
        for w in waves:
            # Use cosine similarity since ocean is near-constant
            dot = np.dot(ocean, w)
            norms = np.linalg.norm(ocean) * np.linalg.norm(w)
            corr = float(dot / norms) if norms > 0 else 0.0
            ocean_content.append(corr)

        return {
            "num_waves": len(waves),
            "each_wave_is_ocean": True,
            "ocean_correlation": ocean_content,
            "wave_substance": "water (same as ocean)",
            "teaching": (
                "No wave has an existence apart from the ocean. "
                "No object has an existence apart from Brahman. "
                "The wave doesn't need to 'merge back' — it was never separate."
            ),
        }
