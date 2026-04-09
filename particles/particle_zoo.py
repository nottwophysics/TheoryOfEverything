"""
The Particle Zoo — Nama-Rupa of the Quantum World

Each particle is a specific 'name and form' (nama-rupa) that Maya
carves out of the Brahman field. They differ in:
    Mass — how much Maya 'weighs them down'
    Charge — how they interact with specific aspects of Maya
    Spin — their intrinsic rotational symmetry

All particles are excitations of the SAME underlying field (Brahman).
An electron is not a 'different substance' from a quark —
both are patterns in one consciousness.
"""

import numpy as np
from dataclasses import dataclass


@dataclass
class ParticleFromMaya:
    """A particle as a specific excitation mode of the Brahman field."""
    name: str
    mass_MeV: float
    charge: float
    spin: float
    color_charge: str     # 'none', 'r', 'g', 'b', 'rgb' (confined)
    generation: int       # 1, 2, or 3
    maya_depth: float     # How 'differentiated' from Brahman (0=Brahman, 1=deep Maya)

    @property
    def is_massless(self) -> bool:
        return self.mass_MeV == 0

    @property
    def guna_association(self) -> str:
        """Map generation to guna."""
        return {1: "Sattva (clarity/light)", 2: "Rajas (activity/medium)",
                3: "Tamas (inertia/heavy)"}.get(self.generation, "beyond gunas")

    def as_field_excitation(self, field_size: int = 256) -> np.ndarray:
        """
        Represent this particle as an excitation of the Brahman field.

        Mass → localization (heavier = more localized = deeper Maya)
        Spin → rotational structure
        Charge → phase structure
        """
        x = np.linspace(-10, 10, field_size)

        # Width inversely proportional to mass (Compton wavelength)
        if self.mass_MeV > 0:
            width = 1.0 / (self.mass_MeV / 100)
        else:
            width = 10.0  # Massless: delocalized

        # Gaussian envelope (localization)
        envelope = np.exp(-x ** 2 / (2 * width ** 2))

        # Spin structure (oscillation frequency)
        spin_freq = self.spin * 2 * np.pi
        spin_structure = np.cos(spin_freq * x)

        # Charge structure (phase)
        charge_phase = np.exp(1j * self.charge * x)

        psi = envelope * spin_structure * charge_phase
        norm = np.linalg.norm(psi)
        if norm > 0:
            psi /= norm

        return psi

    def compute_maya_depth(self) -> float:
        """
        How deep in Maya is this particle?

        Massless, uncharged → close to Brahman
        Massive, charged, confined → deep in Maya
        """
        mass_factor = min(1.0, self.mass_MeV / 1000)
        charge_factor = min(1.0, abs(self.charge))
        confinement_factor = 1.0 if self.color_charge != "none" else 0.0

        return (mass_factor + charge_factor + confinement_factor) / 3


# The Standard Model particles as excitations of Brahman
STANDARD_MODEL = [
    # Leptons - Generation 1
    ParticleFromMaya("electron", 0.511, -1, 0.5, "none", 1, 0.0),
    ParticleFromMaya("electron_neutrino", 0.0000022, 0, 0.5, "none", 1, 0.0),
    # Leptons - Generation 2
    ParticleFromMaya("muon", 105.7, -1, 0.5, "none", 2, 0.0),
    ParticleFromMaya("muon_neutrino", 0.17, 0, 0.5, "none", 2, 0.0),
    # Leptons - Generation 3
    ParticleFromMaya("tau", 1776.9, -1, 0.5, "none", 3, 0.0),
    ParticleFromMaya("tau_neutrino", 15.5, 0, 0.5, "none", 3, 0.0),
    # Quarks - Generation 1
    ParticleFromMaya("up_quark", 2.2, 2/3, 0.5, "rgb", 1, 0.0),
    ParticleFromMaya("down_quark", 4.7, -1/3, 0.5, "rgb", 1, 0.0),
    # Quarks - Generation 2
    ParticleFromMaya("charm_quark", 1275, 2/3, 0.5, "rgb", 2, 0.0),
    ParticleFromMaya("strange_quark", 95, -1/3, 0.5, "rgb", 2, 0.0),
    # Quarks - Generation 3
    ParticleFromMaya("top_quark", 173100, 2/3, 0.5, "rgb", 3, 0.0),
    ParticleFromMaya("bottom_quark", 4180, -1/3, 0.5, "rgb", 3, 0.0),
    # Gauge bosons
    ParticleFromMaya("photon", 0, 0, 1, "none", 0, 0.0),
    ParticleFromMaya("W_boson", 80379, 1, 1, "none", 0, 0.0),
    ParticleFromMaya("Z_boson", 91188, 0, 1, "none", 0, 0.0),
    ParticleFromMaya("gluon", 0, 0, 1, "rgb", 0, 0.0),
    # Higgs
    ParticleFromMaya("higgs", 125100, 0, 0, "none", 0, 0.0),
]

# Compute maya depths
for p in STANDARD_MODEL:
    p.maya_depth = p.compute_maya_depth()


def analyze_particle_zoo() -> dict:
    """
    Analyze the Standard Model through the lens of Advaita.
    """
    # Sort by Maya depth
    by_maya = sorted(STANDARD_MODEL, key=lambda p: p.maya_depth)

    closest_to_brahman = by_maya[:3]
    deepest_in_maya = by_maya[-3:]

    # Mass hierarchy
    masses = [(p.name, p.mass_MeV) for p in STANDARD_MODEL if p.mass_MeV > 0]
    masses.sort(key=lambda x: x[1])

    # Generation pattern
    gen_avg_mass = {}
    for gen in [1, 2, 3]:
        gen_particles = [p for p in STANDARD_MODEL if p.generation == gen and p.mass_MeV > 0]
        if gen_particles:
            gen_avg_mass[gen] = np.mean([p.mass_MeV for p in gen_particles])

    return {
        "total_particles": len(STANDARD_MODEL),
        "closest_to_brahman": [(p.name, p.maya_depth) for p in closest_to_brahman],
        "deepest_in_maya": [(p.name, p.maya_depth) for p in deepest_in_maya],
        "mass_hierarchy": masses[:5],
        "generation_avg_mass": gen_avg_mass,
        "three_generations_three_gunas": {
            1: "Sattva — lightest, most transparent to Brahman",
            2: "Rajas — intermediate, active",
            3: "Tamas — heaviest, most opaque to Brahman",
        },
        "insight": (
            "Neutrinos are closest to Brahman (nearly massless, barely interacting). "
            "Top quarks are deepest in Maya (most massive, strongly confined). "
            "Three generations mirror three gunas. "
            "All particles are ONE field in different modes of excitation."
        ),
    }
