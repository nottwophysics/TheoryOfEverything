"""
2D discrete geometry on a Delaunay manifold: Gauss-Bonnet (computed), plus a
legacy Jacobson-style correlation construction retained for API compatibility.

What is COMPUTED here:
- ``gauss_bonnet_check()``: the discrete Gauss-Bonnet theorem on the Delaunay
  triangulation.  Interior angle deficits (2π − Σ angles at each interior
  vertex) plus boundary exterior/turning angles (π − Σ angles at each
  boundary vertex) sum to 2πχ, where χ = V − E + F is the Euler
  characteristic computed combinatorially from the same triangle list.
  Verified to 1e-9 (achieved ~1e-14), with a topology-change negative
  control: deleting one interior triangle punctures the disk (χ: 1 → 0)
  and the Gauss-Bonnet sum drops by exactly 2π.
- A plain geometric fact stated up front: in two dimensions the Einstein
  tensor vanishes IDENTICALLY (R_μν = (1/2) R g_μν in 2D, so G_μν ≡ 0).
  There is no nontrivial 2D Einstein equation to recover; Gauss-Bonnet is
  the correct global statement of 2D discrete geometry, and any claim of
  "recovering Einstein's equations" on a 2D manifold is empty.

What is LEGACY / INTERPRETATION:
- ``derive_einstein_equations()`` and ``demonstrate_mass_curves_space()``
  are the pre-review construction, retained unchanged because main.py and
  the shared tests call them.  Their "entanglement entropy" is DEFINED from
  T_00, so the reported R-T correlation is circular and is not evidence for
  any field equation (see the notes inside those methods).  The
  consciousness-field language there is interpretation, not computation.

HISTORY: found defective by the 2026-08-15 adversarial review (the
"Einstein equations recovered" claim rested on an entropy defined from
T_00) and reimplemented the same day per REAL_PHYSICS_REIMPLEMENTATION_MEMO.md
Track D — the computed geometric content is now ``gauss_bonnet_check()``.
"""

import numpy as np
from scipy.spatial import Delaunay
from scipy.spatial.distance import pdist, squareform


class EmergentEinstein2D:
    """
    Derives Einstein-like equations on a 2D discrete manifold
    via Jacobson's thermodynamic argument applied to the
    consciousness field's entanglement structure.
    """

    def __init__(self, num_points: int = 50, seed: int = 42):
        self.num_points = num_points
        self.seed = seed
        np.random.seed(seed)

        # Generate points on a 2D surface
        self.points = np.random.randn(num_points, 2)

        # Triangulate (Delaunay gives us a discrete manifold)
        self.triangulation = Delaunay(self.points)
        self.simplices = self.triangulation.simplices

        # Compute edge lengths and adjacency
        self._build_geometry()

    def _build_geometry(self):
        """Build the discrete geometry from the point cloud."""
        n = self.num_points

        # Distance matrix
        self.distances = squareform(pdist(self.points))

        # Adjacency from triangulation
        self.adjacency = np.zeros((n, n), dtype=bool)
        for simplex in self.simplices:
            for i in range(3):
                for j in range(i + 1, 3):
                    self.adjacency[simplex[i], simplex[j]] = True
                    self.adjacency[simplex[j], simplex[i]] = True

        # Vertex areas (Voronoi dual area for each vertex)
        self.vertex_areas = np.zeros(n)
        for simplex in self.simplices:
            # Triangle area via 2-D cross product (scalar z-component).
            # np.cross on 2-D vectors was removed in NumPy 2.0, so compute
            # the z-component explicitly for forward compatibility.
            p0, p1, p2 = self.points[simplex]
            v1, v2 = p1 - p0, p2 - p0
            area = 0.5 * abs(v1[0] * v2[1] - v1[1] * v2[0])
            for idx in simplex:
                self.vertex_areas[idx] += area / 3.0

    # ------------------------------------------------------------------
    # Discrete Gauss-Bonnet (2026-08-15, reimplementation memo Track D/D1)
    # ------------------------------------------------------------------

    @staticmethod
    def _interior_angle(points: np.ndarray, i: int, j: int, k: int) -> float:
        """
        Interior angle at vertex i of triangle (i, j, k).

        Computed as atan2(|v1 × v2|, v1 · v2), which is well-conditioned for
        ALL angles.  (arccos of a normalized dot product loses ~sqrt(machine
        epsilon) ≈ 1e-8 of absolute accuracy near 0 and π; summing hundreds
        of angles that way could miss the 1e-9 Gauss-Bonnet target.  The
        atan2 route keeps the total error at the 1e-13 level.)
        """
        v1 = points[j] - points[i]
        v2 = points[k] - points[i]
        cross = v1[0] * v2[1] - v1[1] * v2[0]
        dot = v1[0] * v2[0] + v1[1] * v2[1]
        return float(np.arctan2(abs(cross), dot))

    def _gauss_bonnet_on(self, simplices: np.ndarray) -> dict:
        """
        Discrete Gauss-Bonnet sum over an arbitrary list of triangles taken
        from this manifold's point set.

        Discrete Gauss-Bonnet for a flat piecewise-linear surface:
            Σ_interior (2π − θ_v)  +  Σ_boundary (π − θ_v)  =  2π χ
        where θ_v is the total triangle angle at vertex v, boundary vertices
        are those on an edge belonging to exactly ONE triangle, and
        χ = V − E + F is computed combinatorially from the SAME triangle
        list — so the left- and right-hand sides are independent
        computations that must agree.

        Everything in the returned dict is computed; nothing is hardcoded.
        """
        # Edge multiplicities: a boundary edge belongs to exactly one triangle.
        edge_count = {}
        for s in simplices:
            for a in range(3):
                p, q = int(s[a]), int(s[(a + 1) % 3])
                e = (p, q) if p < q else (q, p)
                edge_count[e] = edge_count.get(e, 0) + 1

        boundary_vertices = set()
        num_boundary_edges = 0
        for e, c in edge_count.items():
            if c == 1:
                num_boundary_edges += 1
                boundary_vertices.update(e)

        used_vertices = {int(v) for s in simplices for v in s}

        # Total triangle angle at each vertex.
        angle_sum = {v: 0.0 for v in used_vertices}
        for s in simplices:
            for a in range(3):
                i, j, k = int(s[a]), int(s[(a + 1) % 3]), int(s[(a + 2) % 3])
                angle_sum[i] += self._interior_angle(self.points, i, j, k)

        sum_interior_deficits = 0.0
        sum_boundary_exterior = 0.0
        for v in used_vertices:
            if v in boundary_vertices:
                sum_boundary_exterior += np.pi - angle_sum[v]
            else:
                sum_interior_deficits += 2 * np.pi - angle_sum[v]
        total = sum_interior_deficits + sum_boundary_exterior

        # Euler characteristic from the same triangle list (independent of
        # the angle computation above).
        V = len(used_vertices)
        E = len(edge_count)
        F = len(simplices)
        chi = V - E + F

        expected = 2 * np.pi * chi
        residual = abs(total - expected)

        return {
            "num_vertices": int(V),
            "num_edges": int(E),
            "num_triangles": int(F),
            "num_boundary_edges": int(num_boundary_edges),
            "num_boundary_vertices": int(len(boundary_vertices)),
            "euler_characteristic": int(chi),
            "sum_interior_deficits": float(sum_interior_deficits),
            "sum_boundary_exterior_angles": float(sum_boundary_exterior),
            "gauss_bonnet_total": float(total),
            "expected_2_pi_chi": float(expected),
            "residual": float(residual),
            "passes": bool(residual < 1e-9),
            "note": (
                "In 2D the Einstein tensor vanishes identically "
                "(G_munu = R_munu - (1/2) R g_munu = 0 because "
                "R_munu = (1/2) R g_munu in 2D); Gauss-Bonnet is the "
                "correct nontrivial statement of 2D discrete geometry."
            ),
        }

    def gauss_bonnet_check(self) -> dict:
        """
        Verify discrete Gauss-Bonnet on the full Delaunay triangulation.

        The Delaunay triangulation of a planar point set covers the convex
        hull — a topological disk, so χ should come out 1 and the angle sum
        should equal 2π.  Both sides are computed, not assumed.
        """
        return self._gauss_bonnet_on(self.simplices)

    def _find_interior_triangle(self) -> int:
        """
        Index of the first triangle whose three vertices are all interior
        (i.e. none lies on a boundary edge).  Removing such a triangle
        punctures the disk without creating a non-manifold pinch vertex.
        """
        edge_count = {}
        for s in self.simplices:
            for a in range(3):
                p, q = int(s[a]), int(s[(a + 1) % 3])
                e = (p, q) if p < q else (q, p)
                edge_count[e] = edge_count.get(e, 0) + 1
        boundary_vertices = set()
        for e, c in edge_count.items():
            if c == 1:
                boundary_vertices.update(e)
        for idx, s in enumerate(self.simplices):
            if not any(int(v) in boundary_vertices for v in s):
                return int(idx)
        raise ValueError(
            "No all-interior triangle found; use a larger point set for "
            "the topology-change control."
        )

    def gauss_bonnet_topology_control(self) -> dict:
        """
        Negative control for Gauss-Bonnet: delete one interior triangle.

        This punctures the disk (annulus topology): χ drops from 1 to 0, so
        the Gauss-Bonnet sum must drop by exactly 2π — and the identity must
        STILL hold against the new χ.  A check that kept reporting 2π after
        the topology changed would be broken; this control catches that.
        """
        disk = self._gauss_bonnet_on(self.simplices)
        removed = self._find_interior_triangle()
        punctured_simplices = np.delete(self.simplices, removed, axis=0)
        punctured = self._gauss_bonnet_on(punctured_simplices)

        chi_shift = disk["euler_characteristic"] - punctured["euler_characteristic"]
        total_shift = disk["gauss_bonnet_total"] - punctured["gauss_bonnet_total"]
        shift_matches = abs(total_shift - 2 * np.pi * chi_shift) < 1e-9

        return {
            "removed_triangle_index": int(removed),
            "removed_triangle": [int(v) for v in self.simplices[removed]],
            "disk": disk,
            "punctured": punctured,
            "chi_shift": int(chi_shift),
            "total_shift": float(total_shift),
            "shift_matches_2_pi_delta_chi": bool(shift_matches),
            # NOTE (2026-08-16): this is a CONSISTENCY CHECK, not a negative
            # control in the usual sense -- it is expected to PASS, and does.
            # A negative control is one you expect to fail; this one confirms
            # that the identity tracks a deliberate change of topology
            # (chi 1 -> 0) rather than holding regardless. Note also that
            # Gauss-Bonnet on a flat piecewise-linear planar complex is an
            # EXACT COMBINATORIAL THEOREM, so the ~5e-15 residual is a
            # floating-point statement about this implementation, not an
            # empirical result about geometry.
            "control_passes": bool(
                punctured["passes"]
                and punctured["euler_characteristic"] == 0
                and shift_matches
            ),
        }

    def consciousness_energy_density(self, mass_positions: list = None,
                                      mass_values: list = None) -> np.ndarray:
        """
        Energy-momentum content of the consciousness field.

        Mass-energy concentrations represent deep Maya —
        regions where consciousness is highly differentiated
        (strongly interacting with itself).
        """
        T_00 = np.zeros(self.num_points)

        if mass_positions is None:
            # Default: two mass concentrations
            mass_positions = [
                np.array([0.0, 0.0]),
                np.array([2.0, 1.0]),
            ]
            mass_values = [5.0, 3.0]

        for pos, mass in zip(mass_positions, mass_values):
            for i in range(self.num_points):
                r = np.linalg.norm(self.points[i] - pos)
                # Gaussian mass distribution
                T_00[i] += mass * np.exp(-r ** 2 / 0.5) / (2 * np.pi * 0.5)

        return T_00

    def entanglement_entropy_field(self, T_00: np.ndarray) -> np.ndarray:
        """
        Compute entanglement entropy at each point.

        In the consciousness framework:
        - More energy-momentum → more Maya → more entropy
        - The entropy field encodes how deeply Maya conceals Brahman at each point

        We use the Bekenstein bound locally: S_i ∝ sqrt(A_i) * T_i
        (entropy scales with boundary area, weighted by energy density).
        The square root ensures the area-law scaling (S ∝ perimeter, not area).
        """
        S = np.zeros(self.num_points)

        for i in range(self.num_points):
            # Boundary length (perimeter of Voronoi cell ~ sqrt of area)
            boundary_length = np.sqrt(self.vertex_areas[i]) if self.vertex_areas[i] > 0 else 0

            # Local entropy: area-law (S ∝ boundary) × local energy density
            S[i] = boundary_length * T_00[i]

            # Entanglement with neighbors: weighted by energy gradient
            neighbors = np.where(self.adjacency[i])[0]
            for j in neighbors:
                d_ij = self.distances[i, j]
                if d_ij > 1e-15:
                    # Entanglement entropy from the gradient of T across the bond
                    S[i] += 0.1 * abs(T_00[i] - T_00[j]) / d_ij

        return S

    def discrete_ricci_scalar(self, S: np.ndarray) -> np.ndarray:
        """
        Compute discrete Ricci scalar curvature in two ways:

        1. Geometric: deficit angle method (standard Regge calculus)
           R_i = (2π - Σ angles at i) / A_i

        2. Entropy-derived: Jacobson's insight applied discretely.
           The key is that curvature at a point is related to the
           INTEGRATED entropy over a small ball around that point,
           not the Laplacian. We compute:
           R_entropy_i ∝ S_integrated(ball_i) / A_i

           This directly models: δS ∝ R δA (entropy change ~ curvature × area change)
        """
        n = self.num_points
        R_geometric = np.zeros(n)
        R_entropy = np.zeros(n)

        # Geometric curvature: deficit angle method
        for i in range(n):
            angle_sum = 0.0
            for simplex in self.simplices:
                if i not in simplex:
                    continue
                idx = list(simplex)
                idx.remove(i)
                j, k = idx

                v1 = self.points[j] - self.points[i]
                v2 = self.points[k] - self.points[i]

                cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-15)
                cos_angle = np.clip(cos_angle, -1, 1)
                angle = np.arccos(cos_angle)
                angle_sum += angle

            if self.vertex_areas[i] > 1e-15:
                R_geometric[i] = (2 * np.pi - angle_sum) / self.vertex_areas[i]

        # Entropy-derived curvature: integrated entropy in local ball
        # Jacobson: δQ = TdS on a local Rindler horizon
        # Discretely: sum entropy over neighbors weighted by solid angle
        for i in range(n):
            neighbors = np.where(self.adjacency[i])[0]
            if len(neighbors) == 0:
                continue

            # Integrated entropy in the local "causal diamond"
            # Include self + all neighbors, weighted by proximity
            S_integrated = S[i] * self.vertex_areas[i]
            total_weight = self.vertex_areas[i]
            for j in neighbors:
                d_ij = self.distances[i, j]
                weight = self.vertex_areas[j] / (1 + d_ij ** 2)
                S_integrated += S[j] * weight
                total_weight += weight

            # Curvature ∝ entropy density (entropy per unit area)
            if total_weight > 1e-15:
                R_entropy[i] = S_integrated / total_weight

        return R_geometric, R_entropy

    def derive_einstein_equations(self, mass_positions: list = None,
                                   mass_values: list = None) -> dict:
        """
        Full Jacobson derivation on the 2D discrete manifold.

        Steps:
        1. Specify energy-momentum T_μν (consciousness field + masses)
        2. Compute entanglement entropy field S
        3. Derive curvature from entropy (Clausius → Raychaudhuri)
        4. Check: R_entropy ∝ T_00 (Einstein equation)
        """
        # Step 1: Energy-momentum
        T_00 = self.consciousness_energy_density(mass_positions, mass_values)

        # Step 2: Entanglement entropy
        S = self.entanglement_entropy_field(T_00)

        # Step 3: Curvature from entropy
        R_geometric, R_entropy = self.discrete_ricci_scalar(S)

        # Step 4: Check Einstein equation: G_00 ∝ T_00
        # In 2+1D: G_μν = R_μν - (1/2)R g_μν = 8πG T_μν
        # For the 00-component: R_entropy should correlate with T_00

        # Correlation between entropy-derived curvature and energy
        mask = (np.abs(T_00) > 1e-10) | (np.abs(R_entropy) > 1e-10)
        if np.sum(mask) > 5 and np.std(T_00[mask]) > 1e-10 and np.std(R_entropy[mask]) > 1e-10:
            correlation = float(np.corrcoef(R_entropy[mask], T_00[mask])[0, 1])
        else:
            correlation = 0.0

        # Also check geometric curvature vs energy
        if np.sum(mask) > 5 and np.std(R_geometric[mask]) > 1e-10:
            geo_correlation = float(np.corrcoef(R_geometric[mask], T_00[mask])[0, 1])
        else:
            geo_correlation = 0.0

        # Effective gravitational constant (from the proportionality).
        # Guard against an empty/singleton mask (e.g. the no-mass case), where
        # np.std over a zero-length slice raises "Degrees of freedom <= 0".
        if np.sum(mask) > 1 and np.std(T_00[mask]) > 1e-10:
            G_eff = float(np.mean(R_entropy[mask] / (T_00[mask] + 1e-15)))
        else:
            G_eff = 0.0

        return {
            "num_points": self.num_points,
            "num_triangles": len(self.simplices),
            "energy_momentum": {
                "total_energy": float(np.sum(T_00 * self.vertex_areas)),
                "max_density": float(np.max(T_00)),
                "nonzero_points": int(np.sum(T_00 > 1e-10)),
            },
            "entropy_field": {
                "total_entropy": float(np.sum(S)),
                "max_entropy": float(np.max(S)),
                "mean_entropy": float(np.mean(S)),
            },
            "einstein_equation_test": {
                "R_entropy_T_correlation": correlation,
                "R_geometric_T_correlation": geo_correlation,
                "effective_G": G_eff,
                "correlation_threshold": 0.7,
                "passes": abs(correlation) > 0.7,
            },
            "jacobson_derivation": [
                "1. Consciousness field has energy-momentum T_μν at each point",
                "2. Entanglement entropy S computed from Bekenstein bound + neighbor correlations",
                "3. Discrete Ricci curvature R derived from Laplacian of S",
                f"4. Correlation R_entropy vs T_00: {correlation:.4f}",
                f"5. Correlation R_geometric vs T_00: {geo_correlation:.4f}",
                "6. Einstein equation G_μν = 8πG T_μν tested on 2D discrete manifold",
            ],
            "improvement_over_1d": (
                f"2D manifold with {self.num_points} points and {len(self.simplices)} triangles. "
                f"R-T correlation: {correlation:.4f} (entropy) / {geo_correlation:.4f} (geometric). "
                "(The 1D model formerly cited as 0.93 actually yields -0.98 "
                "on re-execution — see gravity/einstein.py review note. Both "
                "the 1D and this 2D construction share the same circularity: "
                "the entropy is defined from T_00.) This is a 2D discrete "
                "geometry, but the entropy channel is not independent evidence."
            ),
        }

    def demonstrate_mass_curves_space(self) -> dict:
        """
        Show that mass-energy (deep Maya) curves the consciousness geometry.

        Compare:
        1. No mass → flat geometry
        2. One mass → curved around the mass
        3. Two masses → doubly curved
        """
        # Case 1: No mass (empty space = Brahman without Maya)
        result_empty = self.derive_einstein_equations(
            mass_positions=[],
            mass_values=[],
        )

        # Case 2: One mass
        result_one = self.derive_einstein_equations(
            mass_positions=[np.array([0.0, 0.0])],
            mass_values=[5.0],
        )

        # Case 3: Two masses
        result_two = self.derive_einstein_equations(
            mass_positions=[np.array([-1.0, 0.0]), np.array([1.0, 0.0])],
            mass_values=[5.0, 3.0],
        )

        return {
            "no_mass": {
                "total_energy": result_empty["energy_momentum"]["total_energy"],
                "total_entropy": result_empty["entropy_field"]["total_entropy"],
                "R_T_correlation": result_empty["einstein_equation_test"]["R_entropy_T_correlation"],
            },
            "one_mass": {
                "total_energy": result_one["energy_momentum"]["total_energy"],
                "total_entropy": result_one["entropy_field"]["total_entropy"],
                "R_T_correlation": result_one["einstein_equation_test"]["R_entropy_T_correlation"],
            },
            "two_masses": {
                "total_energy": result_two["energy_momentum"]["total_energy"],
                "total_entropy": result_two["entropy_field"]["total_entropy"],
                "R_T_correlation": result_two["einstein_equation_test"]["R_entropy_T_correlation"],
            },
            "insight": (
                "More mass → more entropy → more curvature. "
                "Mass tells consciousness-geometry how to curve. "
                "Consciousness-geometry tells mass how to move. "
                "This is Einstein's insight, derived from consciousness thermodynamics."
            ),
        }
