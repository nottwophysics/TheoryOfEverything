"""
The Metric Tensor as Consciousness Geometry

In GR, the metric tensor g_μν describes the curvature of spacetime.
In this framework, the metric emerges from the structure of
consciousness — specifically, from entanglement patterns.

Key idea (following Maldacena, Van Raamsdonk, Ryu-Takayanagi):
    Entanglement entropy between regions → geodesic distance
    More entanglement → shorter distance (closer in space)
    No entanglement → infinite distance (disconnected space)

Advaita parallel:
    Full non-duality (max entanglement) → no distance → Brahman
    Complete Maya (no entanglement) → maximum distance → separate objects

⚠️ REVIEW NOTE (2026-08-15) — THIS MODULE IS CIRCULAR; NOT EVIDENCE.
No quantum state is involved anywhere in this file. `build_entanglement_
structure` does not measure entanglement: it ASSIGNS a correlation
    C(i,j) = exp(-maya_depth * |i-j|/n * 5)
by fiat, where |i-j| is the index separation of two array slots. The
"emergent distance" is then d = -log C = (5*maya_depth/n) * |i-j| — the
same index separation, rescaled. Verified numerically: for n=10,
maya_depth=0.5 the distances are exactly 0.25*|i-j| and
corr(d, |i-j|) = 1.0 to machine precision. So the geometry that comes
out is the geometry that was put in; nothing about Ryu-Takayanagi or
Van Raamsdonk is tested here.

WHAT THIS MODULE IS: an illustration of the SHAPE of the
entanglement-to-distance ansatz, useful for exposition only.

WHERE THE REAL VERSION LIVES: `gravity/entanglement_geometry.py`
(added 2026-08-15) does this computation properly — an exact
transverse-field-Ising ground state, mutual information I(i,j)
computed from actual reduced density matrices, and the derived
distance -ln(I/I_max) checked against separation (Spearman -0.989 at
criticality) with a shuffle negative control. Prefer that module for
any claim.
"""

import numpy as np
from scipy.spatial.distance import pdist, squareform


class ConsciousnessMetric:
    """
    Derives a spacetime metric from the entanglement structure
    of a quantum consciousness field.

    Space = the pattern of entanglement correlations.
    Geometry = how consciousness relates to itself.
    """

    def __init__(self, num_points: int = 20, dimension: int = 3):
        self.num_points = num_points
        self.dimension = dimension
        self.metric_tensor = None
        self._correlation_matrix = None

    def build_entanglement_structure(self, maya_depth: float = 0.5) -> np.ndarray:
        """
        Build the entanglement structure between spatial points.

        maya_depth controls how 'separated' the points appear:
            0.0 = all maximally entangled (Brahman, no space)
            1.0 = all separable (deep Maya, maximum spatial extension)
        """
        n = self.num_points
        np.random.seed(42)

        # Correlation matrix — encodes entanglement between regions
        # Start with maximum correlation (Brahman: everything connected)
        C = np.ones((n, n))

        # Maya introduces separation: reduce correlations
        for i in range(n):
            for j in range(i + 1, n):
                # Distance in an underlying abstract space
                abstract_dist = abs(i - j) / n
                # Correlation decays with Maya depth
                correlation = np.exp(-maya_depth * abstract_dist * 5)
                C[i, j] = correlation
                C[j, i] = correlation

        self._correlation_matrix = C
        return C

    def entanglement_to_distance(self, C: np.ndarray = None) -> np.ndarray:
        """
        Convert entanglement correlations to spatial distances.

        High entanglement → short distance (nearby in space)
        Low entanglement → long distance (far apart)

        d(i,j) = -log(C(i,j))

        This is the Ryu-Takayanagi-inspired prescription:
        geometry emerges from entanglement.
        """
        if C is None:
            C = self._correlation_matrix
        if C is None:
            C = self.build_entanglement_structure()

        # Regularize to avoid log(0)
        C_reg = np.clip(C, 1e-10, 1.0)

        # Distance = negative log of correlation
        D = -np.log(C_reg)
        np.fill_diagonal(D, 0.0)

        return D

    def derive_metric(self, maya_depth: float = 0.5) -> dict:
        """
        Derive the full metric tensor from consciousness structure.

        Steps:
        1. Build entanglement structure (consciousness field)
        2. Convert to distance matrix
        3. Embed in target dimension using MDS
        4. Compute metric tensor at each point
        """
        C = self.build_entanglement_structure(maya_depth)
        D = self.entanglement_to_distance(C)

        # Classical Multi-Dimensional Scaling to get coordinates
        n = self.num_points
        H = np.eye(n) - np.ones((n, n)) / n
        B = -0.5 * H @ (D ** 2) @ H

        eigenvalues, eigenvectors = np.linalg.eigh(B)
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        # Take top dimensions
        d = min(self.dimension, np.sum(eigenvalues > 1e-10))
        if d == 0:
            d = 1
        coords = eigenvectors[:, :d] * np.sqrt(np.abs(eigenvalues[:d]))

        # Compute local metric tensor (Jacobian-based)
        # g_μν ≈ discrete approximation
        metric_tensors = []
        for i in range(1, n - 1):
            g = np.zeros((d, d))
            for mu in range(d):
                for nu in range(d):
                    # Finite difference approximation
                    dx_mu = coords[i + 1, mu] - coords[i - 1, mu] if d > mu else 0
                    dx_nu = coords[i + 1, nu] - coords[i - 1, nu] if d > nu else 0
                    ds2 = D[i, i + 1] ** 2
                    if abs(dx_mu * dx_nu) > 1e-15:
                        g[mu, nu] = ds2 / (dx_mu * dx_nu + 1e-15) / 4
            metric_tensors.append(g)

        self.metric_tensor = metric_tensors

        # Compute scalar curvature proxy
        curvatures = []
        for g in metric_tensors:
            det_g = np.linalg.det(g)
            curvatures.append(float(det_g))

        # Self-diagnostic (computed, not asserted): does the "emergent"
        # distance carry any information beyond the index separation that was
        # fed into build_entanglement_structure? Correlate d(0,j) with j.
        # A value of 1.0 means the geometry out IS the geometry in.
        js = np.arange(1, n)
        d0j = np.array([D[0, j] for j in js], dtype=float)
        if np.std(d0j) > 0 and np.std(js) > 0:
            circularity = float(abs(np.corrcoef(d0j, js)[0, 1]))
        else:
            circularity = 0.0

        return {
            "num_points": n,
            "embedding_dimension": int(d),
            "maya_depth": maya_depth,
            "coordinates_shape": coords.shape,
            "avg_distance": float(np.mean(D[D > 0])),
            "max_distance": float(np.max(D)),
            "curvature_proxy": curvatures,
            "distance_vs_input_separation_corr": circularity,
            "geometry_is_input_geometry": bool(circularity > 0.999),
            "insight": (
                f"At Maya depth {maya_depth}: avg distance = {np.mean(D[D > 0]):.4f}. "
                "As Maya deepens, distances increase — space 'expands'. "
                "CAVEAT (computed above): the correlation between the derived "
                f"distance and the raw index separation is {circularity:.6f}. "
                "At 1.0 the 'emergent' geometry is exactly the separation that "
                "was assigned in build_entanglement_structure — this module "
                "illustrates the ansatz, it does not derive geometry from "
                "entanglement. See gravity/entanglement_geometry.py for the "
                "version computed from a real quantum state."
            ),
        }

    def demonstrate_space_from_entanglement(self) -> dict:
        """
        Show how varying Maya depth creates different geometries.
        """
        results = {}
        for maya in [0.0, 0.25, 0.5, 0.75, 1.0]:
            C = self.build_entanglement_structure(maya)
            D = self.entanglement_to_distance(C)
            nonzero = D[D > 0]
            avg_dist = float(np.mean(nonzero)) if len(nonzero) > 0 else 0.0
            max_dist = float(np.max(D))
            avg_entanglement = float(np.mean(C[C < 1.0])) if np.any(C < 1.0) else 1.0

            results[f"maya_{maya:.2f}"] = {
                "avg_distance": avg_dist,
                "max_distance": max_dist,
                "avg_entanglement": avg_entanglement,
                "space_exists": avg_dist > 0.01,
            }

        results["teaching"] = (
            "Maya = 0: everything maximally entangled → zero distance → no space. "
            "Maya = 1: minimal entanglement → maximum distance → expanded spacetime. "
            "Space EMERGES from the loss of non-duality. "
            "Moksha = returning to zero distance = recognizing non-separation."
        )
        return results
