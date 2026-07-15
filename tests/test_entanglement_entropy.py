"""Tests for the independent entanglement-entropy pipeline (Φ ≤ S research)."""
import numpy as np

from predictions.entanglement_entropy import (
    ising_hamiltonian, ground_state, entanglement_entropy, S_of_W,
)
from predictions.phi_s_systems import make_family


class TestEntropyBasics:
    def test_disconnected_zero_field_pairs_give_product_state(self):
        # No couplings, only transverse field -> product state -> S = 0.
        W = np.zeros((3, 3))
        assert S_of_W(W) < 1e-9

    def test_entangled_coupling_gives_positive_S(self):
        W = np.zeros((2, 2)); W[0, 1] = W[1, 0] = 2.0
        assert S_of_W(W) > 1e-6

    def test_S_nonnegative_and_bounded(self):
        # S across a cut of size c is bounded by c bits.
        for sysd in make_family()[:20]:
            W = np.array(sysd["W"], float); n = sysd["n"]
            S = S_of_W(W)
            assert S >= -1e-9
            assert S <= (n + 1) // 2 + 1e-6

    def test_S_monotone_in_coupling(self):
        # Stronger coupling (vs fixed field) should not decrease entanglement
        # in the weak-coupling regime for a 2-site chain.
        base = np.array([[0.0, 0.3], [0.3, 0.0]])
        strong = np.array([[0.0, 1.5], [1.5, 0.0]])
        assert S_of_W(strong) >= S_of_W(base) - 1e-9


class TestHamiltonian:
    def test_hamiltonian_hermitian(self):
        W = np.array(make_family()[50]["W"], float)
        H = ising_hamiltonian(W)
        assert np.allclose(H, H.T)

    def test_ground_state_normalized(self):
        W = np.array(make_family()[50]["W"], float)
        gs = ground_state(W)
        assert abs(np.vdot(gs, gs) - 1.0) < 1e-9
