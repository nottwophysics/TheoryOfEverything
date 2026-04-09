"""
Maya as Symmetry Breaking — How Particles Emerge

The Standard Model is built on symmetry groups: SU(3)×SU(2)×U(1).
At high energies, these symmetries are unified.
As the universe cools, symmetries break → distinct particles emerge.

In Advaita:
    Full symmetry = Brahman (no distinctions)
    Symmetry breaking = Maya (distinctions emerge)
    Higgs mechanism = the specific process by which Maya gives
                      'mass' (apparent solidity/substance) to forms

The particles of physics are the 'nama-rupa' (names and forms)
that Maya carves out of the symmetric Brahman-field.
"""

import numpy as np


class MayaSymmetryBreaking:
    """
    Models how the symmetry of Brahman breaks to produce
    the particle spectrum of the Standard Model.
    """

    def __init__(self, field_dimension: int = 64):
        self.dim = field_dimension

    def unified_symmetry(self) -> np.ndarray:
        """
        The fully symmetric state — Brahman before Maya.

        All directions in the field space are equivalent.
        No preferred direction → no distinct particles.
        The symmetry group is maximal.
        """
        # Fully symmetric: uniform on the unit sphere
        state = np.ones(self.dim, dtype=np.complex128)
        return state / np.linalg.norm(state)

    def mexican_hat_potential(self, field: np.ndarray,
                              mu_squared: float = -1.0,
                              lambda_param: float = 0.5) -> np.ndarray:
        """
        V(φ) = μ²|φ|² + λ|φ|⁴

        The 'Mexican hat' potential that drives symmetry breaking.

        In Advaita: this potential represents Maya's 'pull' toward
        differentiation. The symmetric point (φ=0) is unstable —
        Brahman 'wants' to manifest (but this is appearance only).

        The circle of minima = the many equivalent 'worlds' Maya
        could project (many possible manifestations of the same Brahman).
        """
        phi_squared = np.abs(field) ** 2
        V = mu_squared * phi_squared + lambda_param * phi_squared ** 2
        return V

    def break_symmetry(self, temperature: float = 0.0) -> dict:
        """
        Spontaneous symmetry breaking: the symmetric state becomes unstable.

        At high temperature: symmetry restored (Brahman, no distinctions)
        At low temperature: symmetry breaks (Maya, distinct particles)

        The critical temperature T_c is the 'moment of creation' —
        when Maya first differentiates Brahman.
        """
        # Critical temperature
        mu_squared = -1.0
        lambda_param = 0.5
        T_c = np.sqrt(-mu_squared / lambda_param)

        # Vacuum expectation value (VEV)
        if temperature < T_c:
            # Below critical: symmetry broken
            vev = np.sqrt(-mu_squared / (2 * lambda_param))
            # Choose a direction (Maya's 'choice')
            np.random.seed(42)
            direction = np.random.randn(self.dim) + 1j * np.random.randn(self.dim)
            direction /= np.linalg.norm(direction)
            vacuum = vev * direction
            symmetry_state = "broken"
        else:
            # Above critical: symmetry intact
            vev = 0.0
            vacuum = np.zeros(self.dim, dtype=np.complex128)
            symmetry_state = "intact"

        # Fluctuations around the vacuum
        # Radial (massive) + Goldstone (massless)
        if vev > 0:
            # Higgs-like mass (radial mode)
            m_higgs = np.sqrt(-2 * mu_squared)
            # Goldstone bosons (tangential modes) — massless
            n_goldstone = self.dim - 1
        else:
            m_higgs = 0.0
            n_goldstone = 0

        return {
            "temperature": temperature,
            "critical_temperature": float(T_c),
            "symmetry": symmetry_state,
            "vev": float(vev),
            "higgs_mass": float(m_higgs),
            "num_goldstone_bosons": n_goldstone,
            "interpretation": {
                "high_T": "Brahman — fully symmetric, no distinctions",
                "T_c": "The moment Maya activates — creation begins",
                "low_T": "The empirical world — symmetry broken, particles exist",
                "vev": f"Maya's 'strength' = {vev:.4f}",
                "higgs": "The mechanism giving mass (substance) to forms",
                "goldstone": f"{n_goldstone} massless modes — the 'residual freedom' "
                             "that Maya doesn't constrain",
            },
        }

    def particle_spectrum_from_breaking(self) -> dict:
        """
        Map Standard Model particles to modes of symmetry breaking.
        """
        result = self.break_symmetry(temperature=0.0)

        # Map to Standard Model structure
        particles = {
            "gauge_bosons": {
                "photon": {"mass": 0, "symmetry": "U(1)_EM unbroken", "maya": "massless messenger"},
                "W_boson": {"mass": 80.4, "symmetry": "SU(2) broken", "maya": "massive from Higgs/Maya"},
                "Z_boson": {"mass": 91.2, "symmetry": "SU(2)×U(1) broken", "maya": "massive from Higgs/Maya"},
                "gluon": {"mass": 0, "symmetry": "SU(3) unbroken", "maya": "confined, never free"},
            },
            "fermions": {
                "electron": {"mass": 0.511, "generation": 1, "maya": "lightest charged lepton"},
                "muon": {"mass": 105.7, "generation": 2, "maya": "heavier copy — deeper Maya"},
                "tau": {"mass": 1777, "generation": 3, "maya": "heaviest copy — deepest Maya"},
                "neutrinos": {"mass": "~0", "maya": "almost massless — closest to Brahman"},
            },
            "higgs": {
                "mass": 125.1,
                "role": "The field that GIVES mass to other particles",
                "maya": "Maya itself — the mechanism of differentiation",
            },
        }

        return {
            "symmetry_breaking": result,
            "particle_spectrum": particles,
            "pattern": (
                "Three generations of fermions = three gunas (Sattva/Rajas/Tamas). "
                "Gauge bosons = the forces binding Maya's forms together. "
                "Higgs = Maya's mechanism for giving 'substance' to appearances. "
                "Neutrinos (nearly massless) = closest to Brahman in the particle world."
            ),
            "open_question": (
                "WHY three generations? WHY these specific masses? "
                "If the Brahman-field's self-referential structure uniquely "
                "determines the symmetry breaking pattern, these numbers "
                "should be derivable. That would be the ultimate test."
            ),
        }
