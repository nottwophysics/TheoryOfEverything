"""
Emergent Spacetime — Space and Time as Cognitive Structures

In Advaita, space (akasha) and time (kala) are not fundamental containers
but categories imposed by the mind (Maya) onto the non-spatial, non-temporal
Brahman.

This module models how the appearance of extended space and sequential time
emerges from a dimensionless consciousness field through self-differentiation.
"""

import numpy as np
from scipy.spatial.distance import pdist, squareform


class ConsciousnessField:
    """
    A field of pure awareness that, through self-reference,
    generates the appearance of spatial and temporal dimensions.

    Space = consciousness differentiating within itself (here vs. there)
    Time = consciousness sequencing its own states (before vs. after)
    """

    def __init__(self, resolution: int = 64):
        self.resolution = resolution
        # Initially undifferentiated — a single point of awareness
        self.awareness = np.ones(1, dtype=np.complex128)
        self.dimensions = 0
        self._history = []

    def differentiate(self, num_dimensions: int = 3) -> np.ndarray:
        """
        Each act of self-referential distinction creates a new dimension.

        First distinction: subject/object → 1D (observer ↔ observed)
        Second: left/right → 2D
        Third: up/down → 3D
        Fourth: before/after → time

        The dimensions aren't discovered — they are created by the
        act of distinction.
        """
        field = self.awareness

        for d in range(num_dimensions):
            # Each self-referential step: outer product with itself
            # This is the mathematical analogue of "consciousness
            # looking at itself from a new angle"
            if len(field) < self.resolution:
                new_dim = np.linspace(-1, 1, min(self.resolution, len(field) * 2))
                # Modulate with a wave to create spatial structure
                wave = np.cos(np.pi * new_dim * (d + 1))
                field = np.kron(field[:min(len(field), self.resolution)], wave[:self.resolution // max(len(field), 1)])
                field = field[:self.resolution]

            self.dimensions = d + 1
            self._history.append(field.copy())

        # Normalize
        norm = np.linalg.norm(field)
        if norm > 0:
            field = field / norm

        self.awareness = field
        return field

    def collapse_to_unity(self) -> np.ndarray:
        """
        Moksha — all dimensions fold back into undifferentiated awareness.
        Space and time dissolve. Only the dimensionless point remains.
        """
        self.awareness = np.ones(1, dtype=np.complex128)
        self.dimensions = 0
        return self.awareness

    def get_history(self) -> list:
        """Return the history of differentiation steps."""
        return self._history


class EmergentSpacetime:
    """
    Model how a metric (distances, geometry) emerges from
    the structure of conscious observation.

    The geometry is not imposed from outside — it arises from
    the pattern of relationships within the consciousness field.
    """

    def __init__(self, num_points: int = 50, dimensions: int = 3):
        self.num_points = num_points
        self.dimensions = dimensions
        self.points = None
        self.metric = None

    def generate_from_awareness(self, awareness_field: np.ndarray) -> dict:
        """
        Generate spatial points from the consciousness field.

        The positions of 'objects' in space are determined by
        the structure of the awareness field, not vice versa.
        """
        n = self.num_points
        d = self.dimensions

        # Use the awareness field to seed spatial positions
        # The field's structure determines the geometry
        np.random.seed(int(np.abs(awareness_field[0]) * 1e6) % (2**31))

        # Points emerge from the field's probability distribution
        probs = np.abs(awareness_field[:n * d]) ** 2
        if len(probs) < n * d:
            probs = np.tile(probs, (n * d) // len(probs) + 1)[:n * d]
        probs = probs / np.sum(probs)

        # Sample positions weighted by the awareness field
        indices = np.random.choice(len(probs), size=n * d, p=probs)
        self.points = indices.reshape(n, d).astype(float)
        self.points /= np.max(np.abs(self.points)) if np.max(np.abs(self.points)) > 0 else 1

        # Compute the emergent metric (distance matrix)
        self.metric = squareform(pdist(self.points))

        return {
            "num_points": n,
            "dimensions": d,
            "metric_shape": self.metric.shape,
            "mean_distance": float(np.mean(self.metric)),
            "max_distance": float(np.max(self.metric)),
            "insight": "These distances emerged from the consciousness field's structure, "
                       "not from a pre-existing space",
        }

    def curvature_proxy(self) -> float:
        """
        Estimate spacetime curvature from the emergent metric.

        In flat space, triangle inequality is tight.
        Curvature shows up as systematic deviations.
        """
        if self.metric is None:
            return 0.0

        n = min(self.num_points, 20)
        violations = 0
        total = 0

        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    sides = sorted([
                        self.metric[i, j],
                        self.metric[j, k],
                        self.metric[i, k],
                    ])
                    # In flat space: longest side ≈ sum of other two
                    # Positive curvature: longest side < sum
                    # Negative curvature: longest side approaches sum
                    ratio = sides[2] / (sides[0] + sides[1]) if (sides[0] + sides[1]) > 0 else 0
                    violations += ratio
                    total += 1

        return float(violations / total) if total > 0 else 0.0
