"""
The Three Gunas — Fundamental Qualities of Prakriti (Nature/Maya)

    Sattva = Clarity, harmony, truth, illumination
    Rajas  = Activity, passion, distortion, restlessness
    Tamas  = Inertia, darkness, concealment, delusion

All phenomenal experience arises from the interplay of these three.
They are the 'RGB' of Maya — every experiential 'color' is a mix.

In Advaita, even the Gunas are part of Maya. Brahman is Nirguna
(beyond all gunas). Liberation means transcending all three.
"""

import numpy as np
from dataclasses import dataclass
from enum import Enum


class GunaState(Enum):
    """Dominant guna states."""
    SATTVIC = "sattva_dominant"
    RAJASIC = "rajas_dominant"
    TAMASIC = "tamas_dominant"
    BALANCED = "gunas_balanced"
    TRANSCENDED = "nirguna"  # Beyond gunas — liberation


@dataclass
class GunaBalance:
    """The current proportion of the three gunas."""
    sattva: float
    rajas: float
    tamas: float

    def __post_init__(self):
        total = self.sattva + self.rajas + self.tamas
        if total > 0:
            self.sattva /= total
            self.rajas /= total
            self.tamas /= total

    @property
    def dominant(self) -> GunaState:
        values = {"sattva": self.sattva, "rajas": self.rajas, "tamas": self.tamas}
        max_guna = max(values, key=values.get)
        max_val = values[max_guna]

        # Check if roughly balanced
        if max_val < 0.4:
            return GunaState.BALANCED

        return {
            "sattva": GunaState.SATTVIC,
            "rajas": GunaState.RAJASIC,
            "tamas": GunaState.TAMASIC,
        }[max_guna]

    def as_array(self) -> np.ndarray:
        return np.array([self.sattva, self.rajas, self.tamas])


class Gunas:
    """
    The Guna dynamics engine.

    Models how different guna proportions transform the same
    underlying reality into different experiential qualities.
    """

    def __init__(self, initial_balance: GunaBalance = None):
        self.balance = initial_balance or GunaBalance(1 / 3, 1 / 3, 1 / 3)
        self.history = [self.balance]

    def apply_to_field(self, field: np.ndarray) -> np.ndarray:
        """
        Transform a field according to current guna balance.

        Sattva: preserves the original signal (clarity)
        Rajas:  adds oscillation and noise (agitation)
        Tamas:  dampens and obscures (concealment)
        """
        n = len(field)
        t = np.linspace(0, 2 * np.pi, n)

        # Sattva: clarity — signal passes through clearly
        sattva_component = field * self.balance.sattva

        # Rajas: activity — adds oscillation and distortion
        rajas_component = (
            self.balance.rajas
            * np.sin(7 * t + np.random.randn(n) * 0.3)
            * np.std(field)
        )

        # Tamas: inertia — dampens toward mean, adds fog
        field_mean = np.mean(field)
        tamas_component = self.balance.tamas * (field_mean - field) * 0.5

        return sattva_component + rajas_component + tamas_component

    def evolve(self, dt: float = 0.1, perturbation: np.ndarray = None) -> GunaBalance:
        """
        Evolve the guna balance over time.

        Gunas are in constant flux — the balance shifts continuously.
        This models the ever-changing nature of phenomenal experience.
        """
        current = self.balance.as_array()

        if perturbation is None:
            # Natural fluctuation
            perturbation = np.random.randn(3) * 0.05

        new_values = current + dt * perturbation
        new_values = np.clip(new_values, 0.01, None)  # Gunas never fully vanish
        total = np.sum(new_values)
        new_values /= total

        self.balance = GunaBalance(*new_values)
        self.history.append(self.balance)
        return self.balance

    def simulate_cycle(self, steps: int = 100) -> list:
        """
        Simulate the natural cycling of gunas over time.

        Returns the history of guna states — demonstrates how
        experience constantly shifts even though the substrate
        (Brahman) remains unchanged.
        """
        history = []
        for _ in range(steps):
            self.evolve()
            history.append({
                "sattva": self.balance.sattva,
                "rajas": self.balance.rajas,
                "tamas": self.balance.tamas,
                "dominant": self.balance.dominant.value,
            })
        return history

    def transcend(self) -> GunaState:
        """
        Liberation: transcending all three gunas.

        Not achieving perfect sattva, but going beyond the
        guna framework entirely. The witness (Sakshi) is Nirguna.
        """
        return GunaState.TRANSCENDED
