"""
Entropic Gravity — Verlinde's Framework Through Advaita

Erik Verlinde (2011): gravity is an entropic force — it arises
from the tendency of systems to increase entropy.

In Advaita: Maya tends to deepen (increase entropy/ignorance).
This 'tendency' manifests as gravity — objects 'fall' toward
regions of higher entanglement/Maya.

F = T ∇S (gravity = temperature × entropy gradient)
"""

import numpy as np


class EntropicGravity:
    """
    Gravity as an entropic force arising from consciousness dynamics.
    """

    def __init__(self, num_points: int = 100):
        self.num_points = num_points
        self.x = np.linspace(0.1, 10, num_points)  # Radial distance
        self.k_B = 1.0  # Boltzmann constant (natural units)

    def holographic_screen_entropy(self, radius: float, mass: float) -> float:
        """
        Entropy on a holographic screen at radius r from mass M.

        S = A/(4G) = πr²/(G)   (Bekenstein-Hawking-like)

        In Advaita: the 'amount of Maya' on a surface surrounding
        a concentration of consciousness.
        """
        G = 1.0  # Natural units
        area = 4 * np.pi * radius ** 2
        return area / (4 * G)

    def unruh_temperature(self, acceleration: float) -> float:
        """T = ℏa/(2πck_B) → a/(2π) in natural units."""
        return abs(acceleration) / (2 * np.pi)

    def entropic_force(self, mass: float, radius: float) -> float:
        """
        F = T dS/dr — gravity as entropy gradient.

        The force 'pulling' objects toward a mass is the
        tendency of Maya to deepen where consciousness
        is more concentrated.
        """
        G = 1.0
        # dS/dr = 2πr/G (from Bekenstein bound)
        dS_dr = 2 * np.pi * radius / G

        # Acceleration at radius r: a = GM/r²
        acceleration = G * mass / radius ** 2

        # Temperature at the screen
        T = self.unruh_temperature(acceleration)

        # Entropic force: F = T × dS/dr
        # This should recover Newton's law: F = GM m/r²
        force = T * dS_dr
        return float(force)

    def recover_newton(self, mass: float = 1.0) -> dict:
        """
        Attempt to recover Newton's law via entropic gravity.

        With the holographic-screen entropy used here (dS/dr = 2πr/G):
        F = T × dS/dr = (a/2π)(2πr/G) = a·r/G = M/r

        REVIEW NOTE (2026-08-15): M/r is NOT Newton's GMm/r². Verlinde's
        derivation requires the entropy gradient associated with the
        displaced TEST MASS (dS/dx = 2π k_B m c / ħ), which this toy does
        not implement. The returned newton_recovered flag is False and the
        0.93 correlation only reflects that 1/r and 1/r² are both
        monotonically decreasing.
        """
        G = 1.0
        radii = self.x

        entropic_forces = np.array([self.entropic_force(mass, r) for r in radii])
        newton_forces = G * mass / radii ** 2

        if np.std(entropic_forces) > 0 and np.std(newton_forces) > 0:
            correlation = float(np.corrcoef(entropic_forces, newton_forces)[0, 1])
        else:
            correlation = 0.0

        ratio = entropic_forces / (newton_forces + 1e-15)
        avg_ratio = float(np.mean(ratio))

        return {
            "test_mass": mass,
            "radii_range": (float(radii[0]), float(radii[-1])),
            "newton_correlation": correlation,
            "avg_ratio_entropic_newton": avg_ratio,
            "newton_recovered": abs(correlation) > 0.99,
            "derivation": [
                "F = T × dS/dr",
                "T = a/(2π) = GM/(2πr²)",
                "dS/dr = 2πr/G",
                "F = [GM/(2πr²)] × [2πr/G] = M/r",
                "NOTE: M/r is NOT Newton's GMm/r² — the screen-entropy "
                "gradient used here is not the displaced-test-mass entropy "
                "Verlinde's derivation requires; the 1/r² law is NOT "
                "recovered (newton_recovered is False).",
            ],
            "insight": (
                "An entropic force emerges from the consciousness-field "
                "thermodynamics, but with the screen entropy used here it "
                "scales as F ∝ M/r — Newton's 1/r² law is NOT recovered "
                "(newton_recovered stays False; the 0.93 correlation only "
                "reflects that both curves decrease). The Advaitic reading "
                "of gravity as Maya's entropic tendency remains an "
                "interpretation, not a derived result."
            ),
        }

    def black_hole_as_maximum_maya(self, mass: float = 10.0) -> dict:
        """
        A black hole is maximum Maya — maximum entropy in minimum space.

        The event horizon is the boundary where Maya becomes total:
        no information escapes (complete concealment).

        In Advaita: a black hole is where ignorance is so concentrated
        that even light (knowledge/sattva) cannot escape.
        """
        G = 1.0
        c = 1.0

        # Schwarzschild radius
        r_s = 2 * G * mass / c ** 2

        # Bekenstein-Hawking entropy
        S_BH = np.pi * r_s ** 2 / G  # A/(4G) with A = 4πr_s²

        # Hawking temperature
        T_H = 1 / (8 * np.pi * G * mass)

        # Information content
        bits = S_BH / np.log(2)

        return {
            "mass": mass,
            "schwarzschild_radius": float(r_s),
            "entropy": float(S_BH),
            "hawking_temperature": float(T_H),
            "information_bits": float(bits),
            "is_maximum_entropy": True,
            "advaita_interpretation": {
                "event_horizon": "Boundary of total concealment (Avarana Shakti)",
                "singularity": "Where Maya's concealment is absolute",
                "hawking_radiation": "Even maximum Maya slowly dissolves — "
                                    "liberation is inevitable, given enough time",
                "information_paradox": "Resolved if information is in consciousness "
                                      "(which is non-local), not in spacetime",
            },
            "insight": (
                f"A black hole of mass {mass} has entropy {S_BH:.2f} "
                f"and temperature {T_H:.6f}. "
                "It represents maximum Maya — total concealment. "
                "But even it radiates (Hawking) — Maya is never permanent. "
                "All concealment eventually dissolves. "
                "This is the physics of the inevitability of liberation."
            ),
        }
