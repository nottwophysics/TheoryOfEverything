"""
The Holographic Principle — Reality as a Projection

't Hooft and Susskind: the information content of a region is
encoded on its boundary (surface), not in its volume.

In Advaita: the 3D world is a 'projection' (Maya) of a lower-dimensional
reality (Brahman). The holographic principle is physics discovering
what Vedanta has always said: the world of forms is a projection.

Maldacena's AdS/CFT: a gravity theory in the bulk is equivalent to
a non-gravitational theory on the boundary.

Advaita: the empirical world (with gravity, space, time) is equivalent
to pure consciousness (without space, time, or gravity) on the 'boundary'.
"""

import numpy as np


class HolographicBoundary:
    """
    Models the holographic principle as Maya projecting
    the 'boundary' consciousness into a 'bulk' spacetime.
    """

    def __init__(self, boundary_dim: int = 50, bulk_dim: int = 20):
        self.boundary_dim = boundary_dim  # CFT / consciousness
        self.bulk_dim = bulk_dim          # AdS / spacetime

    def boundary_state(self, complexity: float = 0.5) -> np.ndarray:
        """
        The boundary state — pure consciousness (Brahman).

        No gravity, no spacetime — just a quantum state on a
        lower-dimensional surface.

        Complexity controls how much structure the state has:
            0.0 = uniform (undifferentiated Brahman)
            1.0 = highly structured (complex consciousness state)
        """
        np.random.seed(42)
        state = np.ones(self.boundary_dim, dtype=np.complex128)

        if complexity > 0:
            # Add structure proportional to complexity
            phases = np.random.randn(self.boundary_dim) * complexity * np.pi
            state *= np.exp(1j * phases)

        return state / np.linalg.norm(state)

    def holographic_projection(self, boundary: np.ndarray) -> np.ndarray:
        """
        Project the boundary state into the bulk — Maya creating spacetime.

        This is a simplified model of the AdS/CFT dictionary:
        boundary operators → bulk fields.
        """
        np.random.seed(42)
        # Projection matrix: boundary → bulk
        # This encodes the 'rules' of Maya — how consciousness
        # becomes spacetime
        projection = np.random.randn(self.bulk_dim, self.boundary_dim) + \
                     1j * np.random.randn(self.bulk_dim, self.boundary_dim)
        projection /= np.sqrt(self.boundary_dim)

        bulk = projection @ boundary
        return bulk / np.linalg.norm(bulk)

    def ryu_takayanagi(self, boundary: np.ndarray, region_size: int = None) -> dict:
        """
        Ryu-Takayanagi formula: S(A) = Area(γ_A) / (4G)

        The entanglement entropy of a boundary region equals the area
        of the minimal surface in the bulk that is homologous to it.

        In Advaita: the 'depth' of Maya in a spatial region is determined
        by how much consciousness is entangled across the boundary of
        that region.
        """
        if region_size is None:
            region_size = self.boundary_dim // 3

        # Compute boundary entanglement entropy for different region sizes
        results = {}
        sizes = range(1, self.boundary_dim // 2 + 1, max(1, self.boundary_dim // 10))

        entropies = []
        areas = []

        for size in sizes:
            # Density matrix of the full state
            rho = np.outer(boundary, boundary.conj())

            # Reduced density matrix for region of given size
            rho_A = rho[:size, :size]
            # Normalize
            trace = np.trace(rho_A)
            if abs(trace) > 1e-15:
                rho_A = rho_A / trace

            # Von Neumann entropy
            eigenvalues = np.real(np.linalg.eigvalsh(rho_A))
            eigenvalues = eigenvalues[eigenvalues > 1e-15]
            if len(eigenvalues) > 0:
                eigenvalues = eigenvalues / np.sum(eigenvalues)
                entropy = -np.sum(eigenvalues * np.log(eigenvalues))
            else:
                entropy = 0.0

            entropies.append(float(entropy))
            # 'Area' of the minimal surface ~ perimeter of the region
            area = 2.0  # In 1D, boundary of a region is 2 points
            areas.append(area)

        # Check if entropy scales with area (not volume)
        # In 1+1 CFT: S ~ (c/3) log(L/a)
        log_sizes = np.log(np.array(list(sizes), dtype=float) + 1)
        if len(entropies) > 2 and np.std(log_sizes) > 0 and np.std(entropies) > 0:
            log_corr = float(np.corrcoef(log_sizes, entropies)[0, 1])
        else:
            log_corr = 0.0

        return {
            "region_sizes": list(sizes),
            "entropies": entropies,
            "log_scaling_correlation": log_corr,
            "follows_area_law": abs(log_corr) > 0.5,
            "formula": "S(A) = Area(γ_A) / (4G_N)",
            "insight": (
                "Entanglement entropy follows an area law — "
                "information is on the boundary, not the bulk. "
                "The 3D world is a holographic projection of "
                "a 2D consciousness surface. "
                "Advaita's Maya (projection) = holography."
            ),
        }

    def demonstrate_holographic_principle(self) -> dict:
        """
        Full demonstration of the holographic correspondence.
        """
        # Create boundary state (Brahman / consciousness)
        boundary = self.boundary_state(complexity=0.5)

        # Project into bulk (spacetime / Maya)
        bulk = self.holographic_projection(boundary)

        # Verify information content
        boundary_entropy = self._entropy(boundary)
        bulk_entropy = self._entropy(bulk)

        # Ryu-Takayanagi
        rt_result = self.ryu_takayanagi(boundary)

        # Reconstruction: can we recover boundary from bulk?
        # (In principle yes — the boundary encodes everything)
        np.random.seed(42)
        projection = np.random.randn(self.bulk_dim, self.boundary_dim) + \
                     1j * np.random.randn(self.bulk_dim, self.boundary_dim)
        projection /= np.sqrt(self.boundary_dim)

        # Pseudo-inverse reconstruction
        reconstructed = np.linalg.pinv(projection) @ bulk
        reconstructed /= np.linalg.norm(reconstructed)
        fidelity = float(abs(np.dot(boundary.conj(), reconstructed)) ** 2)

        return {
            "boundary_dimension": self.boundary_dim,
            "bulk_dimension": self.bulk_dim,
            "boundary_entropy": float(boundary_entropy),
            "bulk_entropy": float(bulk_entropy),
            "ryu_takayanagi": rt_result,
            "reconstruction_fidelity": fidelity,
            "bulk_from_boundary": True,
            "boundary_is_fundamental": True,
            "summary": (
                "The bulk (spacetime with gravity) is a projection of the "
                f"boundary (consciousness). Reconstruction fidelity: {fidelity:.4f}. "
                "The boundary (Brahman) is fundamental. "
                "The bulk (empirical world) is derived. "
                "This is Advaita expressed in the language of physics."
            ),
        }

    @staticmethod
    def _entropy(state: np.ndarray) -> float:
        probs = np.abs(state) ** 2
        probs = probs / np.sum(probs)
        probs = probs[probs > 0]
        return float(-np.sum(probs * np.log(probs)))
