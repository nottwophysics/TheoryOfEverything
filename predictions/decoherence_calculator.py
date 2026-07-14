"""
Decoherence-threshold calculator (P2 turned into a quantitative tool)
=====================================================================

`predictions/testable.py::prediction_2_decoherence_mass_threshold` asserts a
gravitational (Diósi–Penrose) decoherence threshold. On its own that is only
half the physics: whether an object can show interference is set by *whichever
decoherence channel is fastest* — gravitational collapse OR ordinary
environmental decoherence (gas collisions, thermal photons). A collapse-model
signature is only observable in the mass/pressure/temperature window where the
Diósi–Penrose time is SHORTER than every environmental time yet still long
enough to run the experiment.

This module computes both, so the question "where could a collapse model
actually be tested?" gets a quantitative answer instead of a single hand-picked
mass.

Physics and references (all DOIs verified via CrossRef):
  * Diósi–Penrose gravitational decoherence — the coherent superposition of a
    mass at separation Δx decoheres on τ_DP = ħ / ΔE_grav, where ΔE_grav is the
    gravitational self-energy of the mass *difference* between the two branches.
    For a uniform sphere of mass m and radius R this is computed in closed form
    below (no small-Δx approximation).
    Diósi, Phys. Rev. A 40, 1165 (1989), DOI 10.1103/PhysRevA.40.1165;
    Penrose, Gen. Rel. Grav. 28, 581 (1996), DOI 10.1007/BF02105068.
  * Collisional (gas) decoherence — τ_coll = 1 / (n v̄ σ), with number density
    n = P/(k_B T), mean thermal speed v̄ = sqrt(8 k_B T / π m_gas), and
    geometric cross-section σ = π R².
    Joos & Zeh, Z. Phys. B 59, 223 (1985), DOI 10.1007/BF01725541.
  * Thermal-photon (blackbody) scattering decoherence — scales as R⁶ T⁹; the
    prefactor here follows the standard long-wavelength Rayleigh estimate used
    in the collapse-model literature.
    Schlosshauer, Rev. Mod. Phys. 76, 1267 (2005), DOI 10.1103/RevModPhys.76.1267.
  * Overview / formula collection: Bassi, Lochan, Satin, Singh & Ulbricht,
    "Models of wave-function collapse…", Rev. Mod. Phys. 85, 471 (2013),
    DOI 10.1103/RevModPhys.85.471.

This is standard, textbook decoherence physics; nothing here depends on the
Advaita framework. It sharpens (and partly reframes) the framework's own P2
claim by showing the gravitational channel is almost never the fastest one.
"""

from __future__ import annotations

import numpy as np

HBAR = 1.054571817e-34      # J s
G = 6.67430e-11             # m^3 kg^-1 s^-2
KB = 1.380649e-23           # J/K
C = 2.99792458e8            # m/s
M_AIR = 4.81e-26            # kg, mean air molecule (~29 amu)

# verified-CrossRef reference DOIs, exposed for provenance
REFERENCES = {
    "diosi_1989": "10.1103/PhysRevA.40.1165",
    "penrose_1996": "10.1007/BF02105068",
    "joos_zeh_1985": "10.1007/BF01725541",
    "schlosshauer_2005": "10.1103/RevModPhys.76.1267",
    "bassi_rmp_2013": "10.1103/RevModPhys.85.471",
}


def sphere_radius(mass_kg: float, density_kg_m3: float) -> float:
    """Radius of a uniform sphere of given mass and density."""
    return (3.0 * mass_kg / (4.0 * np.pi * density_kg_m3)) ** (1.0 / 3.0)


def _mutual_gravitational_energy(m: float, R: float, s: float) -> float:
    """∫∫ ρ(r)ρ(r')/|r-r'| energy (times G) between two uniform spheres of mass
    m, radius R, whose centres are separated by s. Closed form (Diósi 1989)."""
    if s >= 2.0 * R:
        return G * m * m / s
    x = s / R
    return (G * m * m / R) * (6.0 / 5.0 - 0.5 * x ** 2
                              + (3.0 / 16.0) * x ** 3 - (1.0 / 160.0) * x ** 5)


def dp_energy_difference(mass_kg: float, radius_m: float,
                         separation_m: float) -> float:
    """Diósi–Penrose gravitational self-energy of the branch difference for a
    uniform sphere displaced by ``separation_m``. Zero at zero separation; the
    two spheres no longer overlap at s = 2R, where ΔE = (7/5) G m²/R; it then
    rises with separation toward the point-mass asymptote (12/5) G m²/R as
    s → ∞."""
    self_term = (12.0 / 5.0) * G * mass_kg ** 2 / radius_m
    return self_term - 2.0 * _mutual_gravitational_energy(mass_kg, radius_m,
                                                          separation_m)


def tau_diosi_penrose(mass_kg: float, radius_m: float,
                      separation_m: float | None = None) -> float:
    """Gravitational (DP) decoherence time τ = ħ / ΔE_grav. Default separation
    = 2R (fully-separated branches, the maximal-effect / minimum-time case)."""
    if separation_m is None:
        separation_m = 2.0 * radius_m
    dE = dp_energy_difference(mass_kg, radius_m, separation_m)
    return HBAR / dE if dE > 0 else float("inf")


def tau_collisional(radius_m: float, pressure_pa: float,
                    temperature_k: float = 300.0,
                    gas_mass_kg: float = M_AIR) -> float:
    """Gas-collision decoherence time τ = 1/(n v̄ σ) (Joos–Zeh)."""
    if pressure_pa <= 0:
        return float("inf")
    n = pressure_pa / (KB * temperature_k)
    v_bar = np.sqrt(8.0 * KB * temperature_k / (np.pi * gas_mass_kg))
    sigma = np.pi * radius_m ** 2
    rate = n * v_bar * sigma
    return 1.0 / rate if rate > 0 else float("inf")


def tau_thermal_photon(radius_m: float, temperature_k: float = 300.0,
                       separation_m: float | None = None) -> float:
    """Thermal-photon (blackbody) scattering decoherence time in the Rayleigh
    long-wavelength regime (Joos–Zeh 1985; Schlosshauer 2005). The blackbody
    localisation *rate* has units 1/(m² s):

        Λ = 8.55 · ζ(9) · c · R⁶ · (k_B T / ħ c)⁹

    and the decoherence time over a separation Δx is τ = 1 / (Λ Δx²). This
    regime holds because the thermal-photon wavelength (~48 µm at 300 K) is much
    larger than the separations of interest, so a single scattering event only
    partially resolves Δx. Default Δx = 2R (matching the DP convention)."""
    if temperature_k <= 0:
        return float("inf")
    if separation_m is None:
        separation_m = 2.0 * radius_m
    zeta9 = 1.002008
    lam_rate = 8.55 * zeta9 * C * radius_m ** 6 * (KB * temperature_k / (HBAR * C)) ** 9
    denom = lam_rate * separation_m ** 2
    return 1.0 / denom if denom > 0 else float("inf")


class DecoherenceCalculator:
    """Compute and compare gravitational vs environmental decoherence times."""

    def __init__(self, density_kg_m3: float = 2000.0):
        self.density = density_kg_m3

    def evaluate(self, mass_kg: float, pressure_pa: float,
                 temperature_k: float = 300.0,
                 radius_m: float | None = None,
                 separation_m: float | None = None) -> dict:
        R = radius_m if radius_m is not None else sphere_radius(mass_kg, self.density)
        # Use a consistent branch separation Δx = 2R across all channels.
        dx = separation_m if separation_m is not None else 2.0 * R
        taus = {
            "gravitational_DP": tau_diosi_penrose(mass_kg, R, dx),
            "collisional_gas": tau_collisional(R, pressure_pa, temperature_k),
            "thermal_photon": tau_thermal_photon(R, temperature_k, dx),
        }
        # The observable decoherence is the fastest channel.
        limiting = min(taus, key=lambda k: taus[k])
        return {
            "mass_kg": mass_kg,
            "radius_m": R,
            "pressure_pa": pressure_pa,
            "temperature_k": temperature_k,
            "tau_s": taus,
            "limiting_channel": limiting,
            "tau_limiting_s": taus[limiting],
            "gravity_is_dominant": limiting == "gravitational_DP",
        }

    def discriminating_window(self, mass_grid: np.ndarray, pressure_pa: float,
                              temperature_k: float = 300.0,
                              min_exp_time_s: float = 1e-3) -> dict:
        """Masses for which the DP channel is BOTH the fastest AND slower than a
        minimum experiment time — i.e. where a collapse model is actually
        testable against environmental decoherence."""
        testable = []
        for m in mass_grid:
            r = self.evaluate(m, pressure_pa, temperature_k)
            if r["gravity_is_dominant"] and r["tau_limiting_s"] >= min_exp_time_s:
                testable.append(float(m))
        return {
            "pressure_pa": pressure_pa,
            "temperature_k": temperature_k,
            "min_experiment_time_s": min_exp_time_s,
            "n_testable_masses": len(testable),
            "mass_min_kg": min(testable) if testable else None,
            "mass_max_kg": max(testable) if testable else None,
        }


def _main() -> None:
    calc = DecoherenceCalculator(density_kg_m3=2000.0)
    print("Decoherence channels for a 10^-14 kg sphere (rho=2000):")
    for P_mbar in (1e-6, 1e-10, 1e-13):
        r = calc.evaluate(1e-14, P_mbar * 100.0)
        taus = r["tau_s"]
        print(f"  P={P_mbar:.0e} mbar: DP={taus['gravitational_DP']:.2e}s "
              f"gas={taus['collisional_gas']:.2e}s photon={taus['thermal_photon']:.2e}s "
              f"-> limited by {r['limiting_channel']}")
    grid = np.logspace(-17, -9, 200)
    for P_mbar in (1e-10, 1e-13, 1e-16):
        w = calc.discriminating_window(grid, P_mbar * 100.0)
        lo = f"{w['mass_min_kg']:.2e}" if w['mass_min_kg'] else "none"
        hi = f"{w['mass_max_kg']:.2e}" if w['mass_max_kg'] else "none"
        print(f"P={P_mbar:.0e} mbar: {w['n_testable_masses']} testable masses, "
              f"range {lo} - {hi} kg")


if __name__ == "__main__":
    _main()
