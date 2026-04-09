"""
Pratibhasika — The Illusory Level of Reality

Pure error — seeing what is not there at all.
- Mistaking a rope for a snake
- Dream objects
- Mirages, hallucinations
- Optical illusions

This level is corrected even within the empirical (Vyavaharika) level.
You don't need spiritual realization to know a mirage isn't water.

Key insight: the relationship between Pratibhasika and Vyavaharika
mirrors the relationship between Vyavaharika and Paramarthika.
The dream teaches us about waking.
"""

import numpy as np


class Pratibhasika:
    """
    The illusory level — pure error and projection.

    Generates experiences that are recognized as false
    even within the empirical framework.
    """

    def __init__(self, seed: int = 42):
        self.rng = np.random.RandomState(seed)
        self._dream_state = None

    def generate_dream(self, dreamer_mind: np.ndarray = None, duration: int = 50) -> dict:
        """
        Generate a dream world.

        Key property: the dream world is entirely made of the dreamer's mind.
        There is no external 'dream matter' — the dreamer IS the dream.

        This parallels the Advaitic claim: the waking world is entirely
        made of Brahman (consciousness). There is no external 'world matter'.
        """
        if dreamer_mind is None:
            dreamer_mind = np.ones(256) / np.sqrt(256)

        dream_frames = []
        mind_state = dreamer_mind.copy()

        for t in range(duration):
            # Dream content emerges from the dreamer's own mind
            # Random recombination of mental impressions (vasanas)
            perturbation = self.rng.randn(len(mind_state)) * 0.1
            mind_state = mind_state + perturbation
            mind_state /= np.linalg.norm(mind_state)

            dream_frames.append(mind_state.copy())

        self._dream_state = dream_frames

        return {
            "duration": duration,
            "num_frames": len(dream_frames),
            "dream_substance": "dreamer's own mind",
            "seems_real_during": True,
            "recognized_as_unreal_upon_waking": True,
            "lesson": "If dream objects are made of the dreamer's consciousness, "
                      "could waking objects be made of Brahman's consciousness?",
        }

    def mirage(self, actual_field: np.ndarray) -> dict:
        """
        Generate a mirage — seeing water where there is desert.

        The desert is real. The water is projected by the perceiver.
        Upon closer investigation, the water vanishes.
        """
        # Desert: hot, uniform field with heat shimmer
        shimmer = np.sin(np.linspace(0, 20 * np.pi, len(actual_field))) * 0.1
        mirage_field = actual_field + shimmer

        # "Water" appears where the field dips (purely projected)
        threshold = np.mean(actual_field) - np.std(actual_field)
        water_illusion = mirage_field < threshold

        return {
            "actual": "desert (uniform field)",
            "perceived": f"water at {np.sum(water_illusion)} locations",
            "upon_investigation": "water vanishes — only desert remains",
            "substrate_unchanged": True,
        }

    def rope_snake(self, rope: np.ndarray, darkness_level: float = 0.8) -> dict:
        """
        The classic example: a rope is mistaken for a snake in dim light.

        - In darkness (high ignorance): see snake
        - In dim light: see something ambiguous
        - In full light (low ignorance): see rope

        Nothing changes except the level of illumination (knowledge).
        """
        noise = self.rng.randn(len(rope)) * darkness_level * 0.5
        perceived = rope * (1 - darkness_level) + noise

        if darkness_level > 0.7:
            interpretation = "snake (fear arises)"
        elif darkness_level > 0.3:
            interpretation = "ambiguous (is it a rope or snake?)"
        else:
            interpretation = "rope (clearly seen as-is)"

        return {
            "actual": "rope",
            "perceived_as": interpretation,
            "darkness_level": darkness_level,
            "reality_changed": False,
            "only_perception_changed": True,
        }

    def wake_up(self) -> dict:
        """
        Waking from a dream. All dream objects are recognized as unreal.

        The philosophical question: could 'waking up' from the empirical
        world to the absolute be analogous?
        """
        dream_existed = self._dream_state is not None
        self._dream_state = None

        return {
            "dream_objects_remain": False,
            "dreamer_remains": True,
            "insight": "The dreamer was real; dream objects were appearances "
                       "in the dreamer's awareness. Similarly, Brahman is real; "
                       "world objects are appearances in Brahman's awareness.",
        }
