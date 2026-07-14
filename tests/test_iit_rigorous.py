"""Tests for the non-circular IIT-entanglement bridge test."""
import numpy as np
from predictions.iit_entanglement_rigorous import RigorousIITEntanglementBridge


class TestRigorousBridge:
    def setup_method(self):
        self.br = RigorousIITEntanglementBridge(num_nodes=4, transverse_field=1.0)

    def test_ground_state_is_normalized(self):
        rng = np.random.default_rng(0)
        W = self.br._random_network(rng)
        psi = self.br.ground_state(W)
        assert abs(np.vdot(psi, psi) - 1.0) < 1e-9

    def test_S_depends_on_structure_not_just_sum(self):
        # Two networks with the SAME total connectivity but different geometry
        # must give different entanglement — otherwise the map is still
        # effectively a function of Sum(W) and the test would be circular.
        W1 = np.zeros((4, 4)); W1[0, 1] = W1[1, 0] = 0.5
        W2 = np.zeros((4, 4)); W2[0, 2] = W2[2, 0] = 0.25
        W2[1, 3] = W2[3, 1] = 0.25  # same total = 0.5, different geometry
        s1 = self.br.ent.total_entanglement(self.br.ground_state(W1))
        s2 = self.br.ent.total_entanglement(self.br.ground_state(W2))
        assert abs(s1 - s2) > 1e-6, "S is a function of Sum(W) alone (circular)"

    def test_not_artifactual_perfect_correlation(self):
        # The original circular test produced Pearson = -1.0. A non-circular
        # mapping must NOT reproduce that artifact.
        r = self.br.run(num_trials=60, seed=1, n_perm=300)
        assert abs(r["real"]["pearson"]) < 0.9

    def test_null_correlation_is_centered_on_zero(self):
        r = self.br.run(num_trials=60, seed=1, n_perm=300)
        assert abs(r["null_pairing"]["mean_correlation"]) < 0.2
