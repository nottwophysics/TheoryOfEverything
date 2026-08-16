"""
3D discrete geometry on a Delaunay tetrahedralization, plus a LEGACY
entropy-vs-energy correlation that is retained but WITHDRAWN as evidence.

What is COMPUTED here:
- A genuine 3D simplicial complex: Delaunay tetrahedralization of a random
  point cloud, per-tetrahedron volumes, dual vertex volumes and dual areas.
- Solid angles at each vertex via the Oosterom-Strackee formula, and the
  deficit 4π − ΣΩ.  On a FLAT Euclidean point cloud that deficit vanishes
  identically at every interior vertex (the tetrahedra around it fill the
  whole solid angle) and is nonzero only on convex-hull vertices.  So
  ``R_geometric`` here measures hull membership, not intrinsic curvature —
  ``derive_einstein_equations()`` reports this as a computed diagnostic
  (``geometric_diagnostic``: max |R_geometric| off the hull, and the count of
  vertices carrying deficit vs. the hull-vertex count).  A flat triangulated
  point set has no intrinsic curvature to find; in 3D Regge calculus the
  curvature lives on edge hinges of a genuinely curved simplicial geometry,
  not on the vertices of a flat embedding.

What is LEGACY / INTERPRETATION (withdrawn as evidence, 2026-08-15):
- ``derive_einstein_equations()`` and ``demonstrate_mass_curves_3d_space()``:
  the "entanglement entropy" field is DEFINED from the energy density
  (S_i = area_i · T_00_i + neighbour-gradient terms) and R_entropy is a local
  weighted average of that same S.  Correlating R_entropy with T_00 therefore
  measures the definition, not a field equation.  This is the identical
  circularity named in gravity/einstein_2d.py, in 3D.
- No metric, connection, Ricci tensor or Einstein tensor is ever formed in
  this module, and there is no time dimension: this is a static 3D point
  cloud, not 3+1D spacetime.  Nothing here tests G_μν = 8πG T_μν.
- ``gravitational_wave_signature()``: the difference between two STATIC
  configurations with the source placed at two different points.  Nothing
  propagates — there is no wave equation, no retarded time, no radiative
  degree of freedom.  The near/far comparison is a computed fact about that
  difference field, not evidence of gravitational radiation.

HISTORY: the headline this module used to carry ("Einstein's equations emerge
from consciousness thermodynamics in the correct number of spatial
dimensions") was withdrawn by the 2026-08-15 adversarial review, which found
the entropy circular.  The 2D companion was reimplemented the same day around
``gauss_bonnet_check()`` (REAL_PHYSICS_REIMPLEMENTATION_MEMO.md, Track D);
einstein_3d.py was explicitly recorded as out of scope for that
reimplementation, so its legacy construction is retained here — relabelled,
not deleted.  The old docstring also advertised a 2D "R-T correlation of 0.94"
as the result being extended: that number is deleted, because the 2D module
now disavows the correlation entirely and it was never evidence in either
dimension.  The genuinely computable entanglement-thermodynamics statements
live in gravity/entanglement_first_law.py and gravity/entanglement_geometry.py
(Experiment 20).

STATUS: 3D discrete geometry, honestly labelled.  NOT a derivation of the
Einstein equations, and not 3+1D spacetime.
"""

import numpy as np
from scipy.spatial import Delaunay
from scipy.spatial.distance import pdist, squareform


class EmergentEinstein3D:
    """
    3D Delaunay simplicial complex with dual volumes/areas, solid-angle
    deficits, and a legacy entropy-vs-energy correlation kept for API
    compatibility.

    The geometric machinery (tetrahedralization, volumes, solid angles) is
    real; the "Einstein equation test" it feeds is circular and is labelled
    as such everywhere it appears.  See the module docstring.
    """

    def __init__(self, num_points: int = 80, seed: int = 42):
        self.num_points = num_points
        self.seed = seed
        np.random.seed(seed)

        # Generate points in 3D space
        self.points = np.random.randn(num_points, 3)

        # Tetrahedralize (3D Delaunay gives us a simplicial complex)
        self.triangulation = Delaunay(self.points)
        self.simplices = self.triangulation.simplices  # Each is 4 vertex indices

        # Convex-hull vertices, straight from the same Qhull run.  Used only
        # as a diagnostic: on a flat point cloud these are the ONLY vertices
        # that can carry a nonzero solid-angle deficit.
        self.hull_vertices = np.unique(
            np.asarray(self.triangulation.convex_hull).ravel()
        )

        # Build discrete geometry
        self._build_geometry()

    def _build_geometry(self):
        """Build the discrete 3D geometry from the point cloud."""
        n = self.num_points

        # Distance matrix
        self.distances = squareform(pdist(self.points))

        # Adjacency from tetrahedralization
        self.adjacency = np.zeros((n, n), dtype=bool)
        for simplex in self.simplices:
            for i in range(4):
                for j in range(i + 1, 4):
                    self.adjacency[simplex[i], simplex[j]] = True
                    self.adjacency[simplex[j], simplex[i]] = True

        # Vertex volumes (dual cell volume for each vertex)
        # Each tetrahedron contributes 1/4 of its volume to each vertex
        self.vertex_volumes = np.zeros(n)
        self.tetra_volumes = np.zeros(len(self.simplices))
        for idx, simplex in enumerate(self.simplices):
            p0, p1, p2, p3 = self.points[simplex]
            vol = abs(np.dot(p1 - p0, np.cross(p2 - p0, p3 - p0))) / 6.0
            self.tetra_volumes[idx] = vol
            for v in simplex:
                self.vertex_volumes[v] += vol / 4.0

        # Vertex surface areas (boundary area of dual cell)
        # Approximate as sum of face areas of adjacent tetrahedra / 3
        self.vertex_areas = np.zeros(n)
        for simplex in self.simplices:
            # 4 triangular faces per tetrahedron
            for i in range(4):
                face = [simplex[j] for j in range(4) if j != i]
                p0, p1, p2 = self.points[face]
                area = 0.5 * np.linalg.norm(np.cross(p1 - p0, p2 - p0))
                for v in face:
                    self.vertex_areas[v] += area / 3.0

    def consciousness_energy_density(self, mass_positions=None,
                                      mass_values=None) -> np.ndarray:
        """
        Energy-momentum content of the consciousness field in 3D.

        Mass-energy concentrations represent deep Maya — regions where
        consciousness is highly differentiated. In 3D, the Gaussian
        mass distribution falls off as exp(-r²/σ²) / (2πσ²)^(3/2).
        """
        T_00 = np.zeros(self.num_points)

        if mass_positions is None:
            mass_positions = [
                np.array([0.0, 0.0, 0.0]),
                np.array([2.0, 1.0, 0.5]),
            ]
            mass_values = [5.0, 3.0]

        sigma_sq = 0.5
        norm_3d = (2 * np.pi * sigma_sq) ** 1.5

        for pos, mass in zip(mass_positions, mass_values):
            for i in range(self.num_points):
                r_sq = np.sum((self.points[i] - pos) ** 2)
                T_00[i] += mass * np.exp(-r_sq / sigma_sq) / norm_3d

        return T_00

    def entanglement_entropy_field(self, T_00: np.ndarray) -> np.ndarray:
        """
        The LEGACY "entropy" field — a function of the energy density.

        As implemented (unchanged since before the review, so the numbers
        stay reproducible):

            S_i = A_i · T_00_i  +  0.1 · Σ_{j~i} |T_00_i − T_00_j| / d_ij

        where A_i is the dual-cell area.  This is an area-weighted rewriting
        of T_00 plus a gradient term, NOT an entanglement entropy computed
        from any state — no density matrix exists anywhere in this module.
        Because S is defined from T_00, anything downstream that correlates a
        function of S against T_00 is circular; that is exactly what
        ``derive_einstein_equations()`` does, and why its correlation is
        withdrawn as evidence.

        (The pre-review docstring described this as "S_i = A_i^(2/3) × T_i",
        which the code never did, and justified it by the Bekenstein-Hawking
        area law.  Both claims are removed.)
        """
        S = np.zeros(self.num_points)

        for i in range(self.num_points):
            # Boundary area of the dual cell (holographic surface)
            boundary_area = self.vertex_areas[i] if self.vertex_areas[i] > 0 else 0

            # Area-law entropy: S ∝ boundary area × energy density
            S[i] = boundary_area * T_00[i]

            # Entanglement gradient corrections from neighbors
            neighbors = np.where(self.adjacency[i])[0]
            for j in neighbors:
                d_ij = self.distances[i, j]
                if d_ij > 1e-15:
                    S[i] += 0.1 * abs(T_00[i] - T_00[j]) / d_ij

        return S

    def discrete_ricci_scalar(self, S: np.ndarray):
        """
        Two per-vertex scalars, neither of which is a Ricci scalar.

        1. ``R_geometric_i = (4π − ΣΩ_i) / V_i`` — the solid-angle deficit at
           vertex i.  Computed correctly (Oosterom-Strackee), but on a flat
           Euclidean point cloud the tetrahedra around an INTERIOR vertex fill
           the full 4π, so this is ~1e-15 everywhere except on convex-hull
           vertices, where it only registers that the cloud stops.  It detects
           the boundary of the sample, not curvature.  (True 3D Regge
           curvature sits on edge hinges of a curved simplicial geometry.)

        2. ``R_entropy_i`` — a distance-weighted local average of the legacy
           S field over vertex i and its neighbours.  Since S is defined from
           T_00 (see ``entanglement_entropy_field``), this is a smoothed copy
           of the energy density, not curvature derived from thermodynamics.

        Names are kept for API compatibility; the labels above are the honest
        description of what the two arrays contain.
        """
        n = self.num_points
        R_geometric = np.zeros(n)
        R_entropy = np.zeros(n)

        # Geometric curvature: solid angle deficit
        for i in range(n):
            solid_angle_sum = 0.0
            for simplex in self.simplices:
                if i not in simplex:
                    continue
                # Compute solid angle at vertex i in this tetrahedron
                idx = list(simplex)
                idx.remove(i)
                j, k, l = idx

                v1 = self.points[j] - self.points[i]
                v2 = self.points[k] - self.points[i]
                v3 = self.points[l] - self.points[i]

                n1 = np.linalg.norm(v1)
                n2 = np.linalg.norm(v2)
                n3 = np.linalg.norm(v3)

                if n1 < 1e-15 or n2 < 1e-15 or n3 < 1e-15:
                    continue

                v1, v2, v3 = v1 / n1, v2 / n2, v3 / n3

                # Solid angle via the Oosterom-Strackee formula
                numer = np.dot(v1, np.cross(v2, v3))
                denom = 1 + np.dot(v1, v2) + np.dot(v2, v3) + np.dot(v1, v3)

                if abs(denom) > 1e-15:
                    omega = 2 * np.arctan2(abs(numer), denom)
                    solid_angle_sum += omega

            if self.vertex_volumes[i] > 1e-15:
                # Deficit from 4π steradians (flat space)
                R_geometric[i] = (4 * np.pi - solid_angle_sum) / self.vertex_volumes[i]

        # Entropy-derived curvature: integrated entropy in local ball
        for i in range(n):
            neighbors = np.where(self.adjacency[i])[0]
            if len(neighbors) == 0:
                continue

            S_integrated = S[i] * self.vertex_volumes[i]
            total_weight = self.vertex_volumes[i]
            for j in neighbors:
                d_ij = self.distances[i, j]
                weight = self.vertex_volumes[j] / (1 + d_ij ** 2)
                S_integrated += S[j] * weight
                total_weight += weight

            if total_weight > 1e-15:
                R_entropy[i] = S_integrated / total_weight

        return R_geometric, R_entropy

    def derive_einstein_equations(self, mass_positions=None,
                                   mass_values=None) -> dict:
        """
        LEGACY construction, retained under its original name for API
        compatibility.  It builds T_00, defines S from T_00, smooths S into
        R_entropy, and correlates R_entropy with T_00.

        That correlation is CIRCULAR and is not evidence for any field
        equation — see the module docstring.  The method name is a historical
        artifact: no Einstein equation is derived, tested, or approximated
        here.  What the returned dict does contain that IS computed: the
        manifold counts, the energy totals, and ``geometric_diagnostic``,
        which shows that the solid-angle deficit is confined to the convex
        hull (i.e. the "curvature" channel is a boundary artifact).
        """
        T_00 = self.consciousness_energy_density(mass_positions, mass_values)
        S = self.entanglement_entropy_field(T_00)
        R_geometric, R_entropy = self.discrete_ricci_scalar(S)

        # Correlation test
        mask = (np.abs(T_00) > 1e-10) | (np.abs(R_entropy) > 1e-10)
        if np.sum(mask) > 5 and np.std(T_00[mask]) > 1e-10 and np.std(R_entropy[mask]) > 1e-10:
            correlation = float(np.corrcoef(R_entropy[mask], T_00[mask])[0, 1])
        else:
            correlation = 0.0

        if np.sum(mask) > 5 and np.std(R_geometric[mask]) > 1e-10:
            geo_correlation = float(np.corrcoef(R_geometric[mask], T_00[mask])[0, 1])
        else:
            geo_correlation = 0.0

        # Guard against an empty/singleton mask (no-mass case), where np.std
        # over a zero-length slice raises "Degrees of freedom <= 0".
        if np.sum(mask) > 1 and np.std(T_00[mask]) > 1e-10:
            G_eff = float(np.mean(R_entropy[mask] / (T_00[mask] + 1e-15)))
        else:
            G_eff = 0.0

        # Diagnostic (computed, not asserted): where does the solid-angle
        # deficit actually live?  On a flat cloud it must be confined to the
        # convex hull; if this ever came out otherwise the geometry would be
        # telling us something new.
        off_hull = np.setdiff1d(np.arange(self.num_points), self.hull_vertices)
        deficit_tol = 1e-8
        carriers = np.where(np.abs(R_geometric) > deficit_tol)[0]
        max_off_hull = (float(np.max(np.abs(R_geometric[off_hull])))
                        if off_hull.size else 0.0)

        return {
            "num_points": self.num_points,
            "num_tetrahedra": len(self.simplices),
            "dimensions": 3,
            "energy_momentum": {
                "total_energy": float(np.sum(T_00 * self.vertex_volumes)),
                "max_density": float(np.max(T_00)),
                "nonzero_points": int(np.sum(T_00 > 1e-10)),
            },
            "entropy_field": {
                "total_entropy": float(np.sum(S)),
                "max_entropy": float(np.max(S)),
                "mean_entropy": float(np.mean(S)),
            },
            "geometric_diagnostic": {
                "deficit_tolerance": deficit_tol,
                "num_hull_vertices": int(self.hull_vertices.size),
                "num_vertices_carrying_deficit": int(carriers.size),
                "max_abs_R_geometric_off_hull": max_off_hull,
                "deficit_confined_to_hull": bool(max_off_hull <= deficit_tol),
                "meaning": (
                    "On a flat point cloud the solid-angle deficit can only "
                    "live on convex-hull vertices, so R_geometric detects the "
                    "edge of the sample, not curvature."
                ),
            },
            # Key name kept for API compatibility. Nothing below is a test of
            # the Einstein equation; see "status".
            "einstein_equation_test": {
                "R_entropy_T_correlation": correlation,
                "R_geometric_T_correlation": geo_correlation,
                "effective_G": G_eff,
                "correlation_threshold": 0.7,
                "correlation_exceeds_threshold": bool(abs(correlation) > 0.7),
                "status": (
                    "WITHDRAWN AS EVIDENCE (2026-08-15) — circular: S is "
                    "defined from T_00 and R_entropy is a local average of S, "
                    "so this correlation measures the definition. Whether it "
                    "clears 0.7 says nothing about any field equation."
                ),
            },
            "legacy_steps_annotated": [
                "1. 3D point cloud tetrahedralized via Delaunay (real simplicial complex)",
                f"2. T_00 built from {len(mass_positions or [])} Gaussian sources — an input, not a result",
                "3. S DEFINED from T_00 (S_i = A_i·T_00_i + gradient terms) — the circular step",
                "4. R_geometric = solid-angle deficit — ~0 off the convex hull (flat embedding)",
                f"5. R_entropy vs T_00 correlation: {correlation:.4f} — circular by construction",
                f"6. R_geometric vs T_00 correlation: {geo_correlation:.4f} — boundary artifact",
                "7. No metric, connection, Ricci or Einstein tensor is formed; "
                "G_μν = 8πG T_μν is never evaluated",
            ],
            "status_note": (
                f"3D simplicial complex: {self.num_points} points, "
                f"{len(self.simplices)} tetrahedra — that part is real. The "
                f"R_entropy-T_00 correlation ({correlation:.4f}) is circular "
                "and withdrawn as evidence; this is a static 3D point cloud, "
                "not 3+1D spacetime. (The claim this replaces cited a 2D "
                "correlation of ~0.94 as the baseline being extended; the 2D "
                "module now disavows that correlation, so the number is gone.)"
            ),
        }

    def demonstrate_mass_curves_3d_space(self) -> dict:
        """
        Run the legacy construction on four source configurations.

        This does NOT show that mass curves space: the geometry (the point
        cloud and its tetrahedra) is identical in all four cases and never
        moves.  Only the input field T_00 changes, and with it the field S
        that is defined from T_00.  The four cases are a sensitivity check on
        the legacy correlation, nothing more.
        """
        # Case 1: Empty
        result_empty = self.derive_einstein_equations([], [])

        # Case 2: Single mass at origin
        result_one = self.derive_einstein_equations(
            [np.array([0.0, 0.0, 0.0])], [5.0]
        )

        # Case 3: Binary system
        result_binary = self.derive_einstein_equations(
            [np.array([-1.0, 0.0, 0.0]), np.array([1.0, 0.0, 0.0])],
            [5.0, 3.0],
        )

        # Case 4: Mass shell (4 masses on approximate sphere)
        r = 1.0
        shell_positions = [
            np.array([r, 0, 0]), np.array([-r, 0, 0]),
            np.array([0, r, 0]), np.array([0, 0, r]),
        ]
        result_shell = self.derive_einstein_equations(
            shell_positions, [2.0, 2.0, 2.0, 2.0]
        )

        return {
            "empty_space": {
                "total_energy": result_empty["energy_momentum"]["total_energy"],
                "R_T_correlation": result_empty["einstein_equation_test"]["R_entropy_T_correlation"],
                "interpretation": "No sources: T_00 = 0, so S = 0 and the correlation is undefined (reported as 0.0)",
            },
            "single_mass": {
                "total_energy": result_one["energy_momentum"]["total_energy"],
                "R_T_correlation": result_one["einstein_equation_test"]["R_entropy_T_correlation"],
                "interpretation": "One Gaussian source — no metric is solved, so nothing Schwarzschild-like is computed",
            },
            "binary_system": {
                "total_energy": result_binary["energy_momentum"]["total_energy"],
                "R_T_correlation": result_binary["einstein_equation_test"]["R_entropy_T_correlation"],
                "interpretation": "Two Gaussian sources, superposed linearly; they do not interact",
            },
            "mass_shell": {
                "total_energy": result_shell["energy_momentum"]["total_energy"],
                "R_T_correlation": result_shell["einstein_equation_test"]["R_entropy_T_correlation"],
                "interpretation": "Four sources on a sphere — no Birkhoff statement follows without a metric",
            },
            "insight": (
                "WITHDRAWN AS EVIDENCE (2026-08-15). The geometry is the same "
                "point cloud in all four cases; only the input T_00 changes, "
                "and the field it is correlated against is defined from that "
                "same T_00. This shows the construction is stable, not that "
                "mass curves anything, and no Einstein equation emerges. "
                "(Superseded claim: 'Einstein's equations emerge from "
                "consciousness thermodynamics in the correct number of "
                "spatial dimensions.') The computable entanglement-"
                "thermodynamics results are in "
                "gravity/entanglement_first_law.py and "
                "gravity/entanglement_geometry.py."
            ),
        }

    def gravitational_wave_signature(self) -> dict:
        """
        Difference field between two STATIC source placements — NOT a wave.

        The method name is legacy.  What is computed: T_00 (and hence the
        derived S and R_entropy) for a source at x = +0.5 and at x = −0.5,
        and the difference of the two R_entropy fields.  There is no time
        coordinate, no wave equation, no retarded propagation and no
        radiative degree of freedom anywhere in this module, so the result
        cannot be evidence of gravitational radiation.  The returned
        near-field/far-field numbers are honest facts about the difference
        field: both source placements sit near the origin, so the difference
        is largest there and smaller far away — that is the Gaussian profile
        of the input, not a 1/r radiation law.
        """
        # Two static configurations: source at A, then the same source at B
        pos_A = [np.array([0.5, 0.0, 0.0])]
        pos_B = [np.array([-0.5, 0.0, 0.0])]
        mass = [5.0]

        T_A = self.consciousness_energy_density(pos_A, mass)
        T_B = self.consciousness_energy_density(pos_B, mass)

        S_A = self.entanglement_entropy_field(T_A)
        S_B = self.entanglement_entropy_field(T_B)

        _, R_A = self.discrete_ricci_scalar(S_A)
        _, R_B = self.discrete_ricci_scalar(S_B)

        # Difference of the two static fields (labelled "wave" for API
        # compatibility only — see the docstring).
        delta_R = R_B - R_A
        wave_amplitude = float(np.std(delta_R))
        wave_nonzero = int(np.sum(np.abs(delta_R) > 1e-10))

        # Is the difference field nonzero far from the sources? (A statement
        # about the Gaussian tails, not about propagation.)
        distances_from_origin = np.linalg.norm(self.points, axis=1)
        far_mask = distances_from_origin > np.median(distances_from_origin)
        far_wave = float(np.mean(np.abs(delta_R[far_mask])))
        near_wave = float(np.mean(np.abs(delta_R[~far_mask])))

        return {
            "wave_amplitude": wave_amplitude,
            "points_affected": wave_nonzero,
            "total_points": self.num_points,
            "near_field_amplitude": near_wave,
            "far_field_amplitude": far_wave,
            # Legacy key names, computed values, honest meanings below.
            "propagates": far_wave > 0,
            "falls_off_with_distance": near_wave > far_wave,
            "propagates_means": (
                "the difference field is nonzero beyond the median radius — "
                "a statement about Gaussian tails, NOT about anything moving "
                "in time (this computation has no time coordinate)"
            ),
            "status": (
                "WITHDRAWN AS EVIDENCE (2026-08-15). Superseded claim: 'this "
                "is a gravitational wave ... consistent with the 1/r behavior "
                "of gravitational radiation.' No wave equation is solved and "
                "no 1/r law is fitted; this is the difference between two "
                "static configurations of an input field."
            ),
        }
