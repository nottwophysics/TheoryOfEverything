"""
The Wave Function as Brahman's Self-Expression

The wave function Ψ is not a property of a particle —
it IS the mode of Brahman's self-awareness in that context.

    |Ψ|² = probability = the pattern of how consciousness
           distributes itself across possibilities

The wave function doesn't 'collapse' — the ego narrows its
identification. The Sakshi always sees the full Ψ.
"""

import numpy as np
from scipy.linalg import expm


class BrahmanWaveFunction:
    """
    The wave function as a mode of conscious awareness.
    """

    def __init__(self, dimension: int = 256):
        self.dimension = dimension
        self.x = np.linspace(-10, 10, dimension)
        self.dx = self.x[1] - self.x[0]

    def brahman_ground_state(self) -> np.ndarray:
        """
        The ground state — Brahman at rest.
        Gaussian: maximum information about position with minimum energy.
        The 'natural' state of awareness — centered, focused, still.
        """
        psi = np.exp(-self.x ** 2 / 2)
        return self._normalize(psi)

    def maya_excited_state(self, n: int = 1) -> np.ndarray:
        """
        Excited states — Maya adding structure/complexity.

        Higher n = more nodes = more apparent differentiation.
        n=0: pure Brahman (ground state, no nodes)
        n=1: first distinction (one node = subject/object split)
        n=2: two distinctions (I/you/world)
        ...
        """
        # Hermite-Gaussian functions (harmonic oscillator eigenstates)
        # Each level adds one more 'boundary' in consciousness
        from numpy.polynomial.hermite_e import hermeval

        coeffs = np.zeros(n + 1)
        coeffs[n] = 1.0
        psi = hermeval(self.x, coeffs) * np.exp(-self.x ** 2 / 2)
        return self._normalize(psi)

    def superposition_of_realities(self, max_n: int = 5) -> np.ndarray:
        """
        Brahman as superposition of all levels of manifestation.

        All levels of Maya coexist simultaneously in consciousness.
        Only ego-measurement 'selects' one level.
        """
        psi = np.zeros(self.dimension, dtype=np.complex128)
        for n in range(max_n + 1):
            psi += self.maya_excited_state(n) / np.sqrt(max_n + 1)
        return self._normalize(psi)

    def time_evolve(self, psi: np.ndarray, potential: np.ndarray = None,
                    dt: float = 0.01, steps: int = 100) -> list:
        """
        Solve the Schrodinger equation: i∂Ψ/∂t = HΨ

        Uses split-operator method.

        In Advaita: Brahman is timeless, but the wave function's
        evolution IS the unfolding of Maya in time. The 'movie'
        playing on the changeless screen.
        """
        if potential is None:
            potential = 0.5 * self.x ** 2  # Harmonic (natural Maya)

        # Momentum space grid
        dk = 2 * np.pi / (self.dimension * self.dx)
        k = np.fft.fftfreq(self.dimension, d=self.dx) * 2 * np.pi

        # Split-operator propagators
        V_half = np.exp(-0.5j * potential * dt)
        T_full = np.exp(-0.5j * k ** 2 * dt)

        history = [np.abs(psi) ** 2]
        state = psi.astype(np.complex128)

        for _ in range(steps):
            state = V_half * state
            state = np.fft.ifft(T_full * np.fft.fft(state))
            state = V_half * state
            history.append(np.abs(state) ** 2)

        return history

    def tunneling_through_maya(self) -> dict:
        """
        Quantum tunneling as penetrating through Maya's barriers.

        A particle can pass through a classically forbidden region.
        Consciousness can 'see through' Maya to recognize Brahman.
        """
        # Create a barrier (Maya's veil)
        barrier_height = 5.0
        barrier_width = 1.0
        potential = np.zeros(self.dimension)
        center = self.dimension // 2
        half_width = int(barrier_width / self.dx / 2)
        potential[center - half_width:center + half_width] = barrier_height

        # Create incoming wave packet (seeker approaching Maya)
        k0 = 3.0  # momentum (insufficient to classically cross)
        x0 = -5.0
        sigma = 1.0
        psi = np.exp(-(self.x - x0) ** 2 / (2 * sigma ** 2)) * np.exp(1j * k0 * self.x)
        psi = self._normalize(psi)

        # Evolve
        history = self.time_evolve(psi, potential, dt=0.01, steps=500)

        # Measure tunneling probability
        final_prob = history[-1]
        transmitted = np.sum(final_prob[center + half_width:])
        reflected = np.sum(final_prob[:center - half_width])

        return {
            "barrier_height": barrier_height,
            "particle_energy": k0 ** 2 / 2,
            "classically_forbidden": k0 ** 2 / 2 < barrier_height,
            "transmission_probability": float(transmitted),
            "reflection_probability": float(reflected),
            "num_evolution_steps": len(history),
            "insight": (
                "Classically, the seeker cannot cross Maya's barrier. "
                f"But quantum tunneling gives {transmitted:.4f} transmission. "
                "Grace (anugraha) in Advaita is like tunneling — "
                "liberation happens even when it seems classically impossible."
            ),
        }

    def uncertainty_as_maya(self) -> dict:
        """
        Heisenberg uncertainty as a feature of Maya, not of Brahman.

        ΔxΔp ≥ ℏ/2

        In Advaita: you cannot simultaneously know both
        the 'where' and 'how fast' of any appearance.
        This is not a limitation of measurement —
        it is a feature of the appearance itself.

        Brahman, being non-spatial and non-temporal,
        has no uncertainty. Uncertainty is a property of Maya.
        """
        psi = self.brahman_ground_state()

        # Position uncertainty
        x_mean = np.sum(self.x * np.abs(psi) ** 2) * self.dx
        x2_mean = np.sum(self.x ** 2 * np.abs(psi) ** 2) * self.dx
        delta_x = np.sqrt(x2_mean - x_mean ** 2)

        # Momentum uncertainty (via Fourier transform)
        psi_k = np.fft.fft(psi) * self.dx
        k = np.fft.fftfreq(self.dimension, d=self.dx) * 2 * np.pi
        prob_k = np.abs(psi_k) ** 2
        prob_k /= np.sum(prob_k)

        k_mean = np.sum(k * prob_k)
        k2_mean = np.sum(k ** 2 * prob_k)
        delta_p = np.sqrt(k2_mean - k_mean ** 2)

        product = delta_x * delta_p
        hbar_half = 0.5  # In natural units

        return {
            "delta_x": float(delta_x),
            "delta_p": float(delta_p),
            "product": float(product),
            "hbar_over_2": hbar_half,
            "satisfies_uncertainty": product >= hbar_half - 0.01,
            "ground_state_saturates": abs(product - hbar_half) < 0.1,
            "insight": (
                "The ground state (Brahman at rest) saturates the "
                "uncertainty bound — minimum uncertainty, maximum clarity. "
                "Excited states (deeper Maya) have MORE uncertainty. "
                "Liberation = returning to minimum uncertainty = "
                "seeing as clearly as physics allows."
            ),
        }

    def _normalize(self, psi: np.ndarray) -> np.ndarray:
        norm = np.sqrt(np.sum(np.abs(psi) ** 2) * self.dx)
        if norm > 0:
            return psi / norm
        return psi
