"""
Neti Neti — "Not This, Not This"

The primary method of self-inquiry in Advaita Vedanta.

Systematically negate everything that can be perceived or conceived,
because the Self (Atman) is the perceiver, not the perceived.

Whatever you can observe, you are not that — because you are
the one observing it.

Computationally: strip away all projected layers until only
the irreducible witness remains.
"""

import numpy as np
from dataclasses import dataclass


@dataclass
class Layer:
    """A layer of identification that can be negated."""
    name: str
    description: str
    content: np.ndarray
    attachment_strength: float  # How strongly identified with this layer


class NetiNeti:
    """
    The Neti-Neti inquiry engine.

    Builds up layers of identification (body, mind, emotions, ego)
    and then systematically negates each one, revealing what remains.
    """

    def __init__(self, field_size: int = 256):
        self.field_size = field_size
        self.layers = self._build_default_layers()
        self._negated = []

    def _build_default_layers(self) -> list:
        """Build the default layers of identification."""
        np.random.seed(108)  # 108 is sacred in Vedanta
        n = self.field_size

        return [
            Layer(
                "Physical Body",
                "I am this body — tall, short, young, old",
                np.random.randn(n) * 0.5 + np.sin(np.linspace(0, 2 * np.pi, n)),
                attachment_strength=0.9,
            ),
            Layer(
                "Vital Energy",
                "I am alive — breath, hunger, fatigue",
                np.random.randn(n) * 0.3 + np.cos(np.linspace(0, 4 * np.pi, n)),
                attachment_strength=0.7,
            ),
            Layer(
                "Thoughts",
                "I am my thoughts — beliefs, opinions, knowledge",
                np.random.randn(n) * 0.8,
                attachment_strength=0.85,
            ),
            Layer(
                "Emotions",
                "I am my feelings — happy, sad, angry, afraid",
                np.random.randn(n) * 0.6 + 0.2 * np.sin(np.linspace(0, 8 * np.pi, n)),
                attachment_strength=0.8,
            ),
            Layer(
                "Memories",
                "I am my past — experiences, stories, identity",
                np.random.randn(n) * 0.4 + 0.5,
                attachment_strength=0.75,
            ),
            Layer(
                "Intellect",
                "I am the knower — the one who understands and discriminates",
                np.random.randn(n) * 0.2 + 0.7,
                attachment_strength=0.6,
            ),
            Layer(
                "Ego (Ahamkara)",
                "I am the 'I' — the sense of being a separate self",
                np.random.randn(n) * 0.1 + 1.0,
                attachment_strength=0.95,  # Hardest to let go
            ),
            Layer(
                "Bliss of Deep Sleep",
                "I am the peace experienced in deep sleep",
                np.ones(n) * 0.9 + np.random.randn(n) * 0.05,
                attachment_strength=0.5,
            ),
        ]

    def inquire(self, verbose: bool = True) -> dict:
        """
        Perform the full Neti-Neti inquiry.

        For each layer: "Can I observe this? Yes. Then I am not this."
        What remains after negating everything observable?
        """
        total_field = np.zeros(self.field_size)
        for layer in self.layers:
            total_field += layer.content

        results = []
        remainder = total_field.copy()

        for layer in self.layers:
            # "Can I observe this?" — Yes, I can observe my body/thoughts/etc.
            # "Then I am not this." — The observer is not the observed.
            remainder = remainder - layer.content
            self._negated.append(layer)

            negation = {
                "layer": layer.name,
                "inquiry": f"Can I observe my {layer.name.lower()}?",
                "answer": "Yes — therefore I am not this",
                "negation": f"Neti — I am not the {layer.name.lower()}",
                "attachment_released": layer.attachment_strength,
                "remainder_energy": float(np.sum(remainder ** 2)),
            }
            results.append(negation)

        # What remains?
        remainder_energy = float(np.sum(remainder ** 2))

        return {
            "process": results,
            "remainder": {
                "energy": remainder_energy,
                "is_zero": remainder_energy < 1e-10,
                "interpretation": (
                    "After removing all layers, the remainder approaches zero. "
                    "But WHO performed this inquiry? WHO observed each layer? "
                    "That witness cannot be negated — because it is the one negating. "
                    "THAT is Atman. THAT is Brahman."
                ),
            },
            "final_teaching": (
                "The Self is not found by adding something new. "
                "It is revealed by removing what it is not. "
                "Like a sculptor removing stone to reveal the statue "
                "that was always within."
            ),
        }

    def inquire_step_by_step(self):
        """Generator that yields one negation at a time."""
        total_field = np.zeros(self.field_size)
        for layer in self.layers:
            total_field += layer.content

        remainder = total_field.copy()

        for layer in self.layers:
            remainder = remainder - layer.content
            yield {
                "negating": layer.name,
                "description": layer.description,
                "neti": f"I am not the {layer.name.lower()}",
                "because": f"I can observe my {layer.name.lower()}, "
                           f"so I must be separate from it",
                "remaining_layers": len(self.layers) - len(self._negated) - 1,
                "remainder_magnitude": float(np.linalg.norm(remainder)),
            }
            self._negated.append(layer)

        yield {
            "complete": True,
            "what_remains": "Pure Awareness — the witness of all layers",
            "identity": "Atman = Brahman",
        }

    def reset(self):
        """Reset the inquiry for a fresh start."""
        self._negated = []
        self.layers = self._build_default_layers()
