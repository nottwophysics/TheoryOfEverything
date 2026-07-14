"""
Nama-Rupa (Name and Form) — The Differentiation Engine

The undifferentiated Brahman appears as the world of distinct objects
through the imposition of names (nama) and forms (rupa).

Names and forms are not independently real — they are the way
Maya carves up the seamless whole into apparently separate entities.

Like drawing lines on water: the water doesn't actually divide,
but the lines create the appearance of separate regions.
"""

import numpy as np
from dataclasses import dataclass


@dataclass
class NamedForm:
    """A differentiated entity — carved out of the undifferentiated field."""
    nama: str           # Name — the conceptual label
    rupa: np.ndarray    # Form — the apparent shape/pattern
    source_field: np.ndarray  # The original undifferentiated field it came from
    region: tuple       # (start, end) indices in the source field

    @property
    def is_separate(self) -> bool:
        """
        Appears separate, but is it really?
        Check if the form is made of the same substance as the source.
        """
        return False  # Never truly separate — always Brahman

    def dissolve(self) -> np.ndarray:
        """Remove the name and form — return to the undifferentiated source."""
        return self.source_field


class NamaRupa:
    """
    The name-and-form generator.

    Takes a unified field and creates the appearance of distinct objects
    by imposing boundaries, labels, and patterns.
    """

    def __init__(self, seed: int = 42):
        self.rng = np.random.RandomState(seed)
        self._form_templates = {
            "particle": lambda n: np.exp(-np.linspace(-3, 3, n) ** 2),
            "wave": lambda n: np.sin(np.linspace(0, 4 * np.pi, n)),
            "structure": lambda n: np.where(
                np.abs(np.linspace(-1, 1, n)) < 0.5, 1.0, 0.0
            ),
            "spiral": lambda n: np.sin(np.linspace(0, 8 * np.pi, n))
            * np.exp(-np.linspace(0, 3, n)),
            "pulse": lambda n: np.sinc(np.linspace(-4, 4, n)),
        }

    def differentiate(
        self,
        unified_field: np.ndarray,
        num_entities: int = 5,
        names: list = None,
    ) -> list:
        """
        Carve the unified field into apparently distinct entities.

        The field itself is unchanged — we just assign names and forms
        to different regions.
        """
        n = len(unified_field)
        segment_size = n // num_entities

        if names is None:
            names = [f"entity_{i}" for i in range(num_entities)]

        entities = []
        templates = list(self._form_templates.values())

        for i in range(num_entities):
            start = i * segment_size
            end = start + segment_size if i < num_entities - 1 else n

            # Apply a form template to this region
            template_fn = templates[i % len(templates)]
            form = template_fn(end - start)

            # The form modulates the underlying field, not replaces it
            modulated = unified_field[start:end] * (0.5 + 0.5 * form)

            name = names[i] if i < len(names) else f"entity_{i}"
            entities.append(
                NamedForm(
                    nama=name,
                    rupa=modulated,
                    source_field=unified_field,
                    region=(start, end),
                )
            )

        return entities

    def reunify(self, entities: list) -> np.ndarray:
        """
        Dissolve all names and forms back into the source field.
        Demonstrates that the separate entities were never truly separate.
        """
        if not entities:
            return np.array([])

        source = entities[0].source_field
        # All entities should share the same source
        for entity in entities:
            assert entity.source_field is source, "All entities share one source (Brahman)"
        return source

    def show_non_separation(self, entities: list) -> dict:
        """
        Demonstrate that all named forms are made of the same substance.
        """
        if not entities:
            return {}

        source = entities[0].source_field
        results = {}

        for entity in entities:
            # Correlation with the source field in this region
            start, end = entity.region
            source_region = source[start:end]
            correlation = float(
                np.corrcoef(entity.rupa, source_region)[0, 1]
            ) if len(entity.rupa) > 1 else 1.0

            results[entity.nama] = {
                "appears_separate": True,
                "actually_separate": entity.is_separate,
                "correlation_with_source": correlation,
                "substance": "Brahman",
            }

        return results
