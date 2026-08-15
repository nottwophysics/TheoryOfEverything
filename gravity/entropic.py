"""
Entropic Gravity — Verlinde's Derivation, Implemented Faithfully in SI Units

Erik Verlinde (2011, "On the origin of gravity and the laws of Newton",
JHEP 2011:29): gravity is an entropic force. This module implements the
actual derivation chain in SI units:

  1. Displacement entropy (Bekenstein):  dS/dx = 2π k_B (m c / ħ)
     — moving a test mass m a Compton wavelength toward the screen
     changes the screen entropy by 2π k_B.
  2. Route 1 (Unruh):  T = ħ a / (2π c k_B)  with a = GM/r²
     → F = T · dS/dx = m a = G M m / r².
     NOTE (honesty): Route 1 takes the Newtonian acceleration a = GM/r²
     as INPUT, so its arrival at GMm/r² is F = ma by construction. It
     demonstrates the entropy/temperature bookkeeping is consistent; it
     is NOT an independent derivation of the inverse-square law. Route 2
     is the one that derives the r-dependence, from the holographic
     screen-area count alone.
  3. Route 2 (holographic screen + equipartition, no Unruh input):
     N = A c³ / (G ħ) bits on the screen of area A = 4π r²,
     E = M c² = ½ N k_B T  → T = 2 M c² / (N k_B)
     → F = T · dS/dx = G M m / r²  (ħ cancels, as it must — Newton's
     law contains no quantum of action).

WHAT IS COMPUTED: both routes are evaluated numerically and compared to
Newton's F = GMm/r² across lab-to-astronomical scales; agreement is at
machine precision (checked to 1e-12 relative). That agreement is
ALGEBRAIC, not empirical — once the derivation is faithful the identity
holds exactly, so machine-precision agreement confirms the implementation
is correct, and nothing about nature. Dimensional bookkeeping
over (kg, m, s, K) exponent tuples verifies F comes out in kg·m·s⁻².
The legacy defective route (screen-AREA entropy gradient, which yields
F = M c²/r — not Newton) is retained as `screen_area_route_wrong()` as
a negative control.

WHAT IS INTERPRETATION: faithfulness to Verlinde's algebra does not make
entropic gravity correct physics — that remains open in the literature.
The Advaitic reading (gravity as the entropic tendency of Maya to deepen
toward concentrations of consciousness) is an interpretive layer on top
of the computation, not a derived result.

HISTORY: the original module was found defective by the 2026-08-15
adversarial review (it used the screen-area entropy gradient and produced
F = M/r, not Newton's law) and was reimplemented the same day per
REAL_PHYSICS_REIMPLEMENTATION_MEMO.md Track C.
"""

import numpy as np

# ---------------------------------------------------------------------------
# Physical constants (SI). CODATA 2018; c and k_B are exact by definition.
# ---------------------------------------------------------------------------
C_LIGHT = 2.99792458e8      # m s^-1 (exact)
G_NEWTON = 6.67430e-11      # m^3 kg^-1 s^-2
HBAR = 1.054571817e-34      # J s = kg m^2 s^-1
K_BOLTZMANN = 1.380649e-23  # J K^-1 = kg m^2 s^-2 K^-1 (exact)

# ---------------------------------------------------------------------------
# Dimensional bookkeeping: exponent tuples over (kg, m, s, K).
# Multiplying quantities adds exponent tuples; dividing subtracts.
# ---------------------------------------------------------------------------
DIMENSIONS = {
    "c": (0, 1, -1, 0),            # m/s
    "G": (-1, 3, -2, 0),           # m^3 kg^-1 s^-2
    "hbar": (1, 2, -1, 0),         # kg m^2 s^-1
    "k_B": (1, 2, -2, -1),         # kg m^2 s^-2 K^-1
    "mass": (1, 0, 0, 0),          # kg
    "length": (0, 1, 0, 0),        # m
    "area": (0, 2, 0, 0),          # m^2
    "acceleration": (0, 1, -2, 0), # m s^-2
    "temperature": (0, 0, 0, 1),   # K
    "energy": (1, 2, -2, 0),       # kg m^2 s^-2
    "force": (1, 1, -2, 0),        # kg m s^-2  (newton)
    "dimensionless": (0, 0, 0, 0),
}


def combine_dimensions(*terms) -> tuple:
    """
    Combine (name, power) pairs into a single exponent tuple over
    (kg, m, s, K). E.g. F = T · dS/dx is
    combine_dimensions(("temperature", 1), ("k_B", 1), ("mass", 1),
                       ("c", 1), ("hbar", -1)).
    """
    total = np.zeros(4, dtype=int)
    for name, power in terms:
        total += power * np.array(DIMENSIONS[name], dtype=int)
    return tuple(int(e) for e in total)


class EntropicGravity:
    """
    Verlinde's entropic gravity in SI units: two independent routes to the
    force on a test mass, both computed and both compared against Newton.

    Everything reported in return dicts is computed here; the Advaita
    reading attached to some outputs is labeled interpretation.
    """

    def __init__(self, num_points: int = 100):
        self.num_points = num_points
        # Radii from centimeter-lab scale to ~10^4 AU (meters).
        self.x = np.logspace(-2, 12, num_points)
        # Constants as instance attributes so tests can perturb them
        # (negative controls) without touching module globals.
        self.c = C_LIGHT
        self.G = G_NEWTON
        self.hbar = HBAR
        self.k_B = K_BOLTZMANN

    # ------------------------------------------------------------------
    # Building blocks of the derivation
    # ------------------------------------------------------------------

    def displacement_entropy_gradient(self, test_mass: float) -> float:
        """
        Verlinde's postulate (from Bekenstein's argument): moving a test
        mass m by Δx = ħ/(mc) (its reduced Compton wavelength) toward the
        screen changes the screen entropy by 2π k_B. Hence

            dS/dx = 2π k_B m c / ħ      [J K^-1 m^-1]

        This is the entropy gradient associated with the DISPLACED TEST
        MASS — the quantity the legacy code wrongly replaced with the
        screen-area gradient.
        """
        return 2 * np.pi * self.k_B * test_mass * self.c / self.hbar

    def unruh_temperature(self, acceleration: float) -> float:
        """
        Unruh (1976): an observer with proper acceleration a sees thermal
        radiation at

            T = ħ a / (2π c k_B)        [K]
        """
        return self.hbar * abs(acceleration) / (2 * np.pi * self.c * self.k_B)

    def holographic_screen_entropy(self, radius: float, mass: float = 1.0) -> float:
        """
        Bekenstein-Hawking entropy of a holographic screen of radius r:

            S = k_B A c³ / (4 G ħ),  A = 4π r²      [J K^-1]

        `mass` is accepted for interface compatibility with the legacy
        signature but does not enter S (area law only).
        """
        area = 4 * np.pi * radius ** 2
        return self.k_B * area * self.c ** 3 / (4 * self.G * self.hbar)

    def screen_dof(self, radius: float) -> float:
        """
        Number of holographic degrees of freedom on the screen:

            N = A c³ / (G ħ),  A = 4π r²      [dimensionless]
        """
        area = 4 * np.pi * radius ** 2
        return area * self.c ** 3 / (self.G * self.hbar)

    def equipartition_temperature(self, source_mass: float, radius: float) -> float:
        """
        Screen temperature from equipartition, with no Unruh input:
        the energy inside the screen is E = M c², distributed over the
        N screen degrees of freedom with ½ k_B T each:

            M c² = ½ N k_B T  →  T = 2 M c² / (N k_B)      [K]
        """
        N = self.screen_dof(radius)
        return 2 * source_mass * self.c ** 2 / (N * self.k_B)

    # ------------------------------------------------------------------
    # The two independent routes to the force
    # ------------------------------------------------------------------

    def force_unruh_route(self, source_mass: float, test_mass: float,
                          radius: float) -> float:
        """
        Route 1: screen temperature from the Unruh formula with the
        gravitational acceleration a = GM/r² at the screen.

            F = T · dS/dx = [ħa/(2πck_B)] · [2πk_B m c/ħ] = m a = GMm/r²
        """
        a = self.G * source_mass / radius ** 2
        T = self.unruh_temperature(a)
        return T * self.displacement_entropy_gradient(test_mass)

    def force_equipartition_route(self, source_mass: float, test_mass: float,
                                  radius: float) -> float:
        """
        Route 2: screen temperature from holography + equipartition
        (independent of Route 1 — no acceleration is put in).

            F = T · dS/dx = [2Mc²/(Nk_B)] · [2πk_B m c/ħ]
              = 4π M m c³ / (N ħ) = GMm/r²      (with N = 4πr²c³/(Għ))

        Note ħ cancels from the final force, as it must.
        """
        T = self.equipartition_temperature(source_mass, radius)
        return T * self.displacement_entropy_gradient(test_mass)

    def newton_force(self, source_mass: float, test_mass: float,
                     radius: float) -> float:
        """Reference: Newton's F = GMm/r² [N]."""
        return self.G * source_mass * test_mass / radius ** 2

    def entropic_force(self, mass: float, radius: float,
                       test_mass: float = 1.0) -> float:
        """
        Entropic force on `test_mass` at `radius` from source `mass`, via
        the equipartition route (the route that does not presuppose the
        Newtonian acceleration). Equals GMm/r² to machine precision.
        """
        return self.force_equipartition_route(mass, test_mass, radius)

    # ------------------------------------------------------------------
    # Legacy defective route — retained as a negative control (memo C2)
    # ------------------------------------------------------------------

    def screen_area_route_wrong(self, mass: float = 1.0,
                                test_mass: float = 1.0) -> dict:
        """
        The ORIGINAL (pre-2026-08-15) construction, retained deliberately
        as a negative control: it pairs the Unruh temperature with the
        gradient of the SCREEN-AREA entropy (dS/dr = 2π k_B r c³/(Għ))
        instead of the displaced-test-mass entropy gradient. The algebra
        gives

            F_wrong = T · dS/dr = [ħGM/(2πck_B r²)] · [2πk_B r c³/(Għ)]
                    = M c² / r

        (the "F = M/r" of the original natural-units code) — no test-mass
        dependence and 1/r instead of 1/r²: NOT Newton. The ratio
        F_wrong/F_newton = c²r/(Gm) grows linearly with r, which the
        returned dict demonstrates numerically.

        HISTORY: this was the module's headline route until the
        2026-08-15 adversarial review flagged it; it is kept only to show
        the defect is real and detectable, per memo Track C (C2).
        """
        radii = self.x
        wrong_forces = np.empty_like(radii)
        for i, r in enumerate(radii):
            a = self.G * mass / r ** 2
            T = self.unruh_temperature(a)
            # Screen-AREA entropy gradient — the wrong gradient:
            dS_dr = 2 * np.pi * self.k_B * r * self.c ** 3 / (self.G * self.hbar)
            wrong_forces[i] = T * dS_dr

        newton_forces = self.G * mass * test_mass / radii ** 2
        ratio = wrong_forces / newton_forces
        ratio_spread = float(ratio.max() / ratio.min())
        # Computed verdicts — this route must FAIL them:
        reproduces_newton = bool(np.max(np.abs(ratio - 1.0)) < 1e-12)
        ratio_varies_with_r = bool(ratio_spread > 10.0)
        # The ratio should scale linearly with r: ratio = c² r / (G m)
        linear_scaling_error = float(
            np.max(np.abs(ratio / (self.c ** 2 * radii / (self.G * test_mass)) - 1.0))
        )

        return {
            "source_mass": float(mass),
            "test_mass": float(test_mass),
            "radii_range": (float(radii[0]), float(radii[-1])),
            "force_law": "F_wrong = M c^2 / r  (the legacy 'F = M/r' in SI)",
            "ratio_to_newton_min": float(ratio.min()),
            "ratio_to_newton_max": float(ratio.max()),
            "ratio_spread": ratio_spread,
            "ratio_varies_with_r": ratio_varies_with_r,
            "linear_scaling_error": linear_scaling_error,
            "reproduces_newton": reproduces_newton,
            "history": (
                "Original pre-2026-08-15 route: screen-area entropy gradient "
                "instead of the displaced-test-mass gradient; produced F = M/r "
                "(natural units) / Mc^2/r (SI), not Newton. Retained as a "
                "negative control per the 2026-08-15 reimplementation memo."
            ),
        }

    # ------------------------------------------------------------------
    # Dimensional bookkeeping (memo C3)
    # ------------------------------------------------------------------

    def dimensional_check(self) -> dict:
        """
        Programmatic dimensional analysis over (kg, m, s, K) exponent
        tuples. Every tuple below is COMPUTED by combining the exponents
        of the constituent quantities exactly as the formulas combine the
        quantities themselves; the booleans compare computed tuples to
        the expected ones.
        """
        # dS/dx = 2π k_B m c / ħ  →  entropy per length
        dim_dS_dx = combine_dimensions(
            ("k_B", 1), ("mass", 1), ("c", 1), ("hbar", -1))
        expected_dS_dx = combine_dimensions(("k_B", 1), ("length", -1))

        # T_unruh = ħ a / (2π c k_B)
        dim_T_unruh = combine_dimensions(
            ("hbar", 1), ("acceleration", 1), ("c", -1), ("k_B", -1))

        # N = A c³ / (G ħ)
        dim_N = combine_dimensions(
            ("area", 1), ("c", 3), ("G", -1), ("hbar", -1))

        # T_equip = 2 M c² / (N k_B)   (N dimensionless)
        dim_T_equip = combine_dimensions(
            ("mass", 1), ("c", 2), ("k_B", -1))

        # F = T · dS/dx, for each route
        dim_force_unruh = tuple(
            int(a + b) for a, b in zip(dim_T_unruh, dim_dS_dx))
        dim_force_equip = tuple(
            int(a + b) for a, b in zip(dim_T_equip, dim_dS_dx))

        expected_force = DIMENSIONS["force"]
        expected_temperature = DIMENSIONS["temperature"]

        return {
            "dim_dS_dx": dim_dS_dx,
            "dim_dS_dx_ok": dim_dS_dx == expected_dS_dx,
            "dim_T_unruh": dim_T_unruh,
            "dim_T_unruh_is_kelvin": dim_T_unruh == expected_temperature,
            "dim_N": dim_N,
            "dim_N_dimensionless": dim_N == DIMENSIONS["dimensionless"],
            "dim_T_equip": dim_T_equip,
            "dim_T_equip_is_kelvin": dim_T_equip == expected_temperature,
            "dim_force_unruh_route": dim_force_unruh,
            "dim_force_equipartition_route": dim_force_equip,
            "expected_force": expected_force,
            "force_dimensions_ok": (dim_force_unruh == expected_force
                                    and dim_force_equip == expected_force),
            "basis": "(kg, m, s, K) exponent tuples",
        }

    # ------------------------------------------------------------------
    # Newton recovery (memo C4)
    # ------------------------------------------------------------------

    def recover_newton(self, mass: float = 1.0, test_mass: float = 1.0) -> dict:
        """
        Recover Newton's law via entropic gravity: evaluate BOTH routes
        (Unruh and screen-equipartition) across the radius grid and
        compare each to F = GMm/r².

        `newton_recovered` is COMPUTED: it requires the maximum relative
        deviation of both routes from Newton to be < 1e-12 AND the two
        routes to agree with each other to < 1e-12. It is True because
        the derivation is faithful — the criterion did not move (the
        legacy correlation>0.99 criterion is gone: correlation cannot
        distinguish GMm/r² from 3·GMm/r², as the negative-control test
        demonstrates).

        HISTORY: found defective by the 2026-08-15 review (the old route
        yielded F = M/r and honestly reported newton_recovered=False);
        reimplemented the same day per the reimplementation memo, Track C.
        """
        radii = self.x

        forces_unruh = np.array(
            [self.force_unruh_route(mass, test_mass, r) for r in radii])
        forces_equip = np.array(
            [self.force_equipartition_route(mass, test_mass, r) for r in radii])
        newton_forces = np.array(
            [self.newton_force(mass, test_mass, r) for r in radii])

        # Route-vs-Newton deviations (relative)
        dev_unruh = float(np.max(np.abs(forces_unruh / newton_forces - 1.0)))
        dev_equip = float(np.max(np.abs(forces_equip / newton_forces - 1.0)))
        # Route-vs-route agreement (relative)
        dev_routes = float(np.max(np.abs(forces_unruh / forces_equip - 1.0)))

        tolerance = 1e-12
        routes_agree = bool(dev_routes < tolerance)
        newton_recovered = bool(dev_unruh < tolerance
                                and dev_equip < tolerance
                                and routes_agree)

        # Correlation kept for continuity with the legacy report format;
        # it is NOT the recovery criterion (see docstring).
        if np.std(forces_equip) > 0 and np.std(newton_forces) > 0:
            correlation = float(
                np.corrcoef(forces_equip, newton_forces)[0, 1])
        else:
            correlation = 0.0

        avg_ratio = float(np.mean(forces_equip / newton_forces))

        dims = self.dimensional_check()

        return {
            "test_mass": float(test_mass),
            "source_mass": float(mass),
            "radii_range": (float(radii[0]), float(radii[-1])),
            "newton_correlation": correlation,
            "avg_ratio_entropic_newton": avg_ratio,
            "newton_recovered": newton_recovered,
            "max_rel_deviation_unruh_route": dev_unruh,
            "max_rel_deviation_equipartition_route": dev_equip,
            "max_rel_deviation_between_routes": dev_routes,
            "routes_agree": routes_agree,
            "force_dimensions_ok": dims["force_dimensions_ok"],
            "derivation": [
                "Displacement entropy (Bekenstein): dS/dx = 2π k_B m c / ħ",
                "Route 1 (Unruh): T = ħa/(2πck_B), a = GM/r² "
                "→ F = T·dS/dx = ma = GMm/r²",
                "Route 2 (equipartition): N = 4πr²c³/(Għ), Mc² = ½Nk_BT "
                "→ T = 2Mc²/(Nk_B) → F = T·dS/dx = 4πMmc³/(Nħ) = GMm/r²",
                "ħ cancels from both final forces, as Newton's law requires",
                f"Computed: max relative deviation from GMm/r² = "
                f"{max(dev_unruh, dev_equip):.3e} over r ∈ "
                f"[{radii[0]:.1e}, {radii[-1]:.1e}] m (both routes)",
            ],
            "insight": (
                "With the displaced-test-mass entropy gradient "
                "dS/dx = 2πk_B mc/ħ — the gradient Verlinde's derivation "
                "actually requires — both the Unruh route and the independent "
                "screen-equipartition route reproduce Newton's F = GMm/r² to "
                f"machine precision (max relative deviation "
                f"{max(dev_unruh, dev_equip):.1e}). This makes the code "
                "faithful to Verlinde (2011); whether gravity is genuinely "
                "entropic remains open in the literature. The Advaitic "
                "reading — gravity as Maya's tendency to deepen toward "
                "concentrations of consciousness — is an interpretation "
                "layered on the computation, not a derived result."
            ),
        }

    # ------------------------------------------------------------------
    # Black hole thermodynamics (SI)
    # ------------------------------------------------------------------

    def black_hole_as_maximum_maya(self, mass: float = 10.0) -> dict:
        """
        Schwarzschild black-hole thermodynamics in SI units.

        COMPUTED: r_s = 2GM/c², S_BH = k_B A c³/(4Għ) with A = 4πr_s²,
        T_H = ħc³/(8πGMk_B), and the check that S_BH saturates the
        Bekenstein bound S ≤ 2πk_B E R/(ħc) with E = Mc², R = r_s —
        `is_maximum_entropy` is that computed saturation check, not an
        assertion.

        INTERPRETATION: the Advaita reading (event horizon as total
        concealment / Avarana Shakti; Hawking evaporation as the
        impermanence of concealment) is labeled as such.
        """
        # Schwarzschild radius
        r_s = 2 * self.G * mass / self.c ** 2

        # Bekenstein-Hawking entropy: S = k_B A c³ / (4 G ħ)
        area = 4 * np.pi * r_s ** 2
        S_BH = self.k_B * area * self.c ** 3 / (4 * self.G * self.hbar)

        # Hawking temperature: T = ħ c³ / (8π G M k_B)
        T_H = self.hbar * self.c ** 3 / (8 * np.pi * self.G * mass * self.k_B)

        # Bekenstein bound with E = Mc², R = r_s: S ≤ 2π k_B E R / (ħ c)
        S_bound = 2 * np.pi * self.k_B * (mass * self.c ** 2) * r_s / (self.hbar * self.c)
        # A Schwarzschild BH saturates the bound exactly — computed check:
        is_maximum_entropy = bool(abs(S_BH / S_bound - 1.0) < 1e-12)

        bits = S_BH / (self.k_B * np.log(2))

        return {
            "mass": float(mass),
            "schwarzschild_radius": float(r_s),
            "entropy": float(S_BH),
            "hawking_temperature": float(T_H),
            "information_bits": float(bits),
            "bekenstein_bound": float(S_bound),
            "bekenstein_saturation_ratio": float(S_BH / S_bound),
            "is_maximum_entropy": is_maximum_entropy,
            "advaita_interpretation": {
                "event_horizon": "Boundary of total concealment (Avarana Shakti)",
                "singularity": "Where Maya's concealment is absolute",
                "hawking_radiation": "Even maximum Maya slowly dissolves — "
                                     "liberation is inevitable, given enough time",
                "information_paradox": "Resolved if information is in consciousness "
                                       "(which is non-local), not in spacetime",
            },
            "insight": (
                f"A black hole of mass {mass} kg has r_s = {r_s:.3e} m, "
                f"entropy {S_BH:.3e} J/K ({bits:.3e} bits) and Hawking "
                f"temperature {T_H:.3e} K. It saturates the Bekenstein bound "
                "(computed), i.e. maximum entropy for its energy and size — "
                "the physics behind the 'maximum Maya' reading, which itself "
                "is interpretation. Hawking evaporation means even this "
                "concealment is impermanent."
            ),
        }
