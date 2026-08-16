"""
Track B acceptance tests — real binary MERA (N=16, chi=2).

Pre-registered criteria (REAL_PHYSICS_REIMPLEMENTATION_MEMO.md, 2026-08-15):
  B1  every disentangler satisfies U^dag U = I and every isometry satisfies
      W^dag W = I to 1e-10;
  B2  (negative control — the old defect inverted) replacing any single
      layer's tensors with different random ones changes the boundary state
      (||delta psi|| > 0.01); zeroing tensors must NOT leave the state
      unchanged;
  B3  (RT-type bound, computed) for intervals of length 2, 4, 8 the exact
      entropy of the constructed state obeys S <= ln(chi)*|minimal cut| + 1e-9
      with the minimal cut counted on the actual network graph; saturation
      ratios reported;
  B4  (disconnection, computed) as lambda -> 0 the mutual information
      I(left half : right half) decreases monotonically over >= 5 values to
      < 1e-8, and the derived distance -ln(I/I0) grows accordingly;
  B5  the log-shaped minimal cut is stated as a BY-CONSTRUCTION property of
      the network; only B3's inequality on the actual state is claimed as a
      computed result.

The old (pre-2026-08-15) module applied its tensors as a global phase — a
physical no-op.  Several tests below therefore measure with a phase-invariant
distance so a regression to that defect cannot pass by accident, and the
flag-consistency tests recompute every verdict flag from the reported numbers
so a hardcoded verdict would be caught.
"""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from quantum.tensor_network import MERATensorNetwork, disconnection_scan

N_SITES = 16
CHI = 2
SEED = 42
NUM_LAYERS = 4  # log2(16)


@pytest.fixture(scope="module")
def mera():
    """The memo's network: N=16, chi=2, lambda=1 (generic), seed 42.
    The module caches the boundary state per lambda, so reuse is cheap."""
    return MERATensorNetwork(num_sites=N_SITES, bond_dim=CHI,
                             entangling_strength=1.0, seed=SEED)


# ----------------------------------------------------------------------
# construction sanity (prerequisites for every acceptance claim)
# ----------------------------------------------------------------------

class TestConstruction:
    def test_boundary_state_is_explicit_65536_dim_unit_vector(self, mera):
        psi = mera.boundary_state()
        assert psi.shape == (2 ** N_SITES,)
        assert psi.size == 65536
        assert abs(np.linalg.norm(psi) - 1.0) < 1e-10

    def test_state_is_deterministic_for_fixed_seed(self, mera):
        other = MERATensorNetwork(num_sites=N_SITES, bond_dim=CHI,
                                  entangling_strength=1.0, seed=SEED)
        assert np.allclose(other.boundary_state(), mera.boundary_state(),
                           atol=1e-12)

    def test_different_seed_gives_different_state(self, mera):
        """Mechanical check A: the headline state can come out differently."""
        other = MERATensorNetwork(num_sites=N_SITES, bond_dim=CHI,
                                  entangling_strength=1.0, seed=SEED + 1)
        overlap = abs(np.vdot(mera.boundary_state(), other.boundary_state()))
        assert overlap < 1.0 - 0.01  # genuinely different, not a phase

    def test_rebuild_with_same_tensors_reproduces_state(self, mera):
        """The perturbation measurement is not structurally guaranteed to
        fire: descending with the UNCHANGED tensors reproduces the state
        exactly, so B2's 'state changed' verdicts are earned, not automatic."""
        psi = mera.boundary_state()
        rebuilt = mera._descend(mera.top_state, mera.isometries,
                                mera.disentanglers)
        assert np.linalg.norm(rebuilt - psi) < 1e-10


# ----------------------------------------------------------------------
# B1 — tensor algebra
# ----------------------------------------------------------------------

class TestB1TensorAlgebra:
    def test_reported_deviations_within_1e10(self, mera):
        result = mera.tensor_algebra_check()
        assert result["max_unitarity_deviation"] < 1e-10
        assert result["max_isometry_deviation"] < 1e-10
        assert result["all_within_1e-10"] is True

    def test_tensor_counts_match_binary_mera(self, mera):
        result = mera.tensor_algebra_check()
        # layers of 1 + 2 + 4 + 8 tensors of each kind
        assert result["num_disentanglers"] == 15
        assert result["num_isometries"] == 15

    def test_every_tensor_directly(self, mera):
        """Independent recomputation (not trusting the module's own dict):
        U^dag U = I_4 for all 15 disentanglers, W^dag W = I_2 for all 15
        isometries, to 1e-10."""
        for layer in mera.disentanglers:
            for U in layer:
                assert U.shape == (4, 4)
                assert np.max(np.abs(U.conj().T @ U - np.eye(4))) < 1e-10
        for layer in mera.isometries:
            for W in layer:
                assert W.shape == (4, 2)
                assert np.max(np.abs(W.conj().T @ W - np.eye(2))) < 1e-10

    def test_flag_is_computed_from_deviations(self, mera):
        result = mera.tensor_algebra_check()
        expected = (result["max_unitarity_deviation"] < 1e-10
                    and result["max_isometry_deviation"] < 1e-10)
        assert result["all_within_1e-10"] == expected


# ----------------------------------------------------------------------
# B2 — negative control: the old global-phase defect inverted
# ----------------------------------------------------------------------

class TestB2PerturbationResponse:
    @pytest.mark.parametrize("layer", range(NUM_LAYERS))
    def test_replacing_any_single_layer_changes_state(self, mera, layer):
        """Memo B2: ||delta psi|| > 0.01 for EVERY layer.  Also checked with
        the phase-invariant distance, so a global-phase-only change (the old
        defect) could not pass."""
        result = mera.perturbation_response(layer=layer, mode="replace")
        assert result["delta_norm"] > 0.01
        assert result["phase_invariant_distance"] > 0.01
        assert result["state_changed"] is True

    @pytest.mark.parametrize("layer", range(NUM_LAYERS))
    def test_zeroing_a_layer_does_not_leave_state_unchanged(self, mera, layer):
        """The old defect's signature: zeroing every tensor left the output
        untouched.  Now zeroing a layer annihilates the descended vector,
        a maximal change from the unit-norm state."""
        result = mera.perturbation_response(layer=layer, mode="zero")
        assert result["delta_norm"] > 0.01
        assert result["perturbed_norm"] < 1e-10  # zero tensors -> zero vector
        assert result["state_changed"] is True

    def test_change_flag_is_computed_not_hardcoded(self, mera):
        result = mera.perturbation_response(layer=1, mode="replace")
        assert result["state_changed"] == (
            result["phase_invariant_distance"] > 1e-12)


# ----------------------------------------------------------------------
# B3 — RT-type bound: exact entropies vs minimal cuts on the real graph
# ----------------------------------------------------------------------

class TestB3RTBound:
    def test_memo_intervals_obey_bound(self, mera):
        """S(interval) <= ln(chi) * |min cut| + 1e-9 for lengths 2, 4, 8,
        recomputed here from the module's raw entropy and cut values."""
        ln_chi = np.log(CHI)
        for start, length in ((0, 2), (0, 4), (0, 8)):
            entropy = mera.interval_entropy(start, length)
            cut = mera.minimal_cut(start, length)
            assert entropy <= ln_chi * cut + 1e-9, (
                f"interval ({start},{length}): S={entropy} > "
                f"ln(chi)*cut={ln_chi * cut}")

    def test_bound_holds_at_other_starts_too(self, mera):
        ln_chi = np.log(CHI)
        for start in (1, 3, 7, 11):
            for length in (2, 4, 8):
                entropy = mera.interval_entropy(start, length)
                cut = mera.minimal_cut(start, length)
                assert entropy <= ln_chi * cut + 1e-9

    def test_rt_check_reports_saturation_ratios(self, mera):
        result = mera.rt_bound_check()
        assert result["all_bounds_hold"] is True
        for row in result["intervals"]:
            assert 0.0 <= row["saturation_ratio"] <= 1.0 + 1e-9
            # flag consistency: computed from the row's own numbers
            assert row["bound_holds"] == (
                row["entropy"] <= row["bound"] + 1e-9)

    def test_entropies_are_nontrivial_and_exact(self, mera):
        """The generic (lambda=1) state is genuinely entangled — entropies
        are far from zero — and, because the state is pure, S(A) equals
        S(complement of A) (Schmidt), a strong independent check that the
        entropy really comes from the constructed vector."""
        s4 = mera.interval_entropy(0, 4)
        s12 = mera.interval_entropy(4, 12)  # complement of sites 0..3
        assert s4 > 0.5
        assert abs(s4 - s12) < 1e-8

    def test_min_cut_is_counted_on_the_graph(self, mera):
        """Cut sanity on the actual network graph: one site is severed by
        its single bond; cuts are positive and no larger than the interval
        length (cutting each site's boundary bond always works)."""
        assert mera.minimal_cut(0, 1) == 1
        for length in (2, 4, 8):
            cut = mera.minimal_cut(0, length)
            assert 1 <= cut <= length


# ----------------------------------------------------------------------
# B4 — disconnection: lambda -> 0 kills the halves' mutual information
# ----------------------------------------------------------------------

class TestB4Disconnection:
    @pytest.fixture(scope="class")
    def scan(self):
        return disconnection_scan(num_sites=N_SITES, bond_dim=CHI, seed=SEED)

    def test_scan_covers_at_least_five_lambdas_down_to_zero(self, scan):
        assert len(scan["lambdas"]) >= 5
        assert scan["lambdas"][0] == max(scan["lambdas"])
        assert scan["lambdas"][-1] == 0.0

    def test_mutual_information_decreases_monotonically(self, scan):
        infos = scan["mutual_information"]
        for k in range(len(infos) - 1):
            assert infos[k + 1] < infos[k], (
                f"I not strictly decreasing at step {k}: {infos}")
        assert scan["monotone_decreasing"] is True

    def test_product_limit_below_1e8(self, scan):
        assert scan["mutual_information"][-1] < 1e-8
        assert scan["final_below_1e-8"] is True

    def test_derived_distance_grows(self, scan):
        dists = scan["derived_distance"]
        for k in range(len(dists) - 1):
            assert dists[k + 1] > dists[k]
        assert dists[-1] == float("inf")  # I = 0: infinitely far
        assert scan["distances_grow"] is True

    def test_flags_recomputed_from_reported_values(self, scan):
        infos = scan["mutual_information"]
        dists = scan["derived_distance"]
        assert scan["monotone_decreasing"] == all(
            infos[k + 1] < infos[k] for k in range(len(infos) - 1))
        assert scan["distances_grow"] == all(
            dists[k + 1] > dists[k] for k in range(len(dists) - 1))
        assert scan["final_below_1e-8"] == (infos[-1] < 1e-8)

    def test_lambda_zero_is_exactly_the_product_state(self):
        """Identity limit: lambda = 0 must give |00...0> exactly, with zero
        entropy for every interval probed."""
        mera0 = MERATensorNetwork(num_sites=N_SITES, bond_dim=CHI,
                                  entangling_strength=0.0, seed=SEED)
        psi = mera0.boundary_state()
        assert abs(abs(psi[0]) - 1.0) < 1e-10  # all weight on |00...0>
        assert np.linalg.norm(psi[1:]) < 1e-10
        for start, length in ((0, 2), (0, 8), (5, 4)):
            assert mera0.interval_entropy(start, length) < 1e-10
        halves = mera0.mutual_information_halves()
        assert halves["mutual_information"] < 1e-10

    def test_generic_lambda_has_nonzero_mutual_information(self, mera):
        """The contrast that makes B4 meaningful: at lambda = 1 the halves
        are strongly correlated (this number could have come out ~0 if the
        tensors did not act — the old defect)."""
        halves = mera.mutual_information_halves()
        assert halves["mutual_information"] > 0.1
        assert abs(halves["state_norm"] - 1.0) < 1e-10


# ----------------------------------------------------------------------
# B5 — honesty of the log-cut claim
# ----------------------------------------------------------------------

class TestB5HonestLabeling:
    def test_log_cut_labeled_by_construction_not_computed_result(self, mera):
        result = mera.rt_bound_check()
        status = result["log_cut_shape"]["status"]
        assert "by construction" in status
        assert "not claimed as a computed result" in status
        assert "S <= ln(chi) * |minimal cut|" in result["computed_claim"]

    def test_cut_by_length_matches_direct_recomputation(self, mera):
        """The reported by-construction cut profile must be the real graph's
        min-cut values, not a typed-in log curve."""
        reported = mera.rt_bound_check()["log_cut_shape"]["cut_by_length"]
        for length, cut in reported.items():
            assert cut == mera.minimal_cut(0, length)

    def test_cut_growth_is_sublinear_a_graph_property(self, mera):
        """The hierarchical shortcut exists in the GRAPH: the cut for the
        half interval (length 8) is smaller than the 8 boundary bonds a
        product-structure network would need.  Stated as a property of the
        network, per B5 — no state-level claim here."""
        assert mera.minimal_cut(0, 8) < 8


# ----------------------------------------------------------------------
# aggregate demo (what Experiment 19 will consume after integration)
# ----------------------------------------------------------------------

class TestFullDemonstration:
    def test_demo_reports_all_tracks_and_labels_interpretation(self, mera):
        demo = mera.full_demonstration()
        assert demo["tensor_algebra"]["all_within_1e-10"] is True
        assert demo["perturbation_example"]["state_changed"] is True
        assert demo["rt_bound"]["all_bounds_hold"] is True
        assert demo["disconnection"]["monotone_decreasing"] is True
        assert demo["disconnection"]["final_below_1e-8"] is True
        # interpretive gloss must be labeled as interpretation, not result
        assert "Interpretation (not computed)" in demo["interpretation"]


class TestRTBoundVacuityIsReported:
    """
    Phase 5 scope finding: at two of the three default intervals the
    "RT-type bound" is exactly the trivial maximum-entropy bound.

    Every boundary site hangs off one chi=2 bond, so min_cut <= |A| always.
    Where cut == length, ln(chi)*|cut| reduces to S <= |A|*ln2, which no state
    can violate. Only the length-8 row (cut 6 < 8) tests anything about the
    constructed state, and the module must say so rather than presenting three
    equally informative rows.
    """

    def test_two_of_three_default_intervals_are_vacuous(self):
        from quantum.tensor_network import MERATensorNetwork
        r = MERATensorNetwork().rt_bound_check()
        flags = {(row["start"], row["length"]): row["bound_is_vacuous"]
                 for row in r["intervals"]}
        assert flags[(0, 2)] is True
        assert flags[(0, 4)] is True
        assert flags[(0, 8)] is False
        assert r["n_vacuous"] == 2
        assert r["non_vacuous_intervals"] == [(0, 8)]

    def test_a_vacuous_row_is_exactly_the_max_entropy_bound(self):
        import numpy as np
        from quantum.tensor_network import MERATensorNetwork
        r = MERATensorNetwork().rt_bound_check()
        for row in r["intervals"]:
            if row["bound_is_vacuous"]:
                assert abs(row["bound"] - row["length"] * np.log(2)) < 1e-9, (
                    "a row flagged vacuous is not in fact the trivial "
                    "|A|*ln2 bound — the flag is mislabelling rows")

    def test_disconnection_monotonicity_is_declared_grid_specific(self):
        from quantum.tensor_network import disconnection_scan
        d = disconnection_scan()
        assert d["monotone_is_grid_and_seed_specific"] is True, (
            "monotone_decreasing is a property of this grid and seed, not of "
            "the network, and the returned dict must say so")
