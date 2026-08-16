"""
Guards for the mutations that `tools/mutate.py` found nothing noticed.

Each test here exists because breaking a specific piece of the implementation
left the whole suite green. They are written to fail under exactly that
mutation, and each was verified in BOTH directions -- passing on the real code
and failing on the mutated copy -- via `python tools/mutate.py -k <name>`.

A test that has never been seen to fail is not a guard.
"""
import re

import numpy as np
import pytest


class TestSeedIsHonoured:
    """
    mutate.py::seed-ignored

    Every §8 statement is qualified "216 coupling matrices, seed 42". Replacing
    the seed argument with a constant left all tests passing, so the
    reproducibility guarantee the falsification rests on was protected by
    nothing at all.
    """

    def test_different_seeds_give_different_families(self):
        from predictions.phi_s_systems import make_family
        a = make_family(seed=42)
        b = make_family(seed=43)
        assert len(a) == len(b)
        assert any(x["W"] != y["W"] for x, y in zip(a, b)), (
            "make_family ignored its seed: two different seeds produced an "
            "identical family")

    def test_seed_42_is_reproducible_and_pinned(self):
        """The published family must be stable run to run AND be seed 42's."""
        from predictions.phi_s_systems import make_family
        first = make_family(seed=42)
        second = make_family(seed=42)
        assert [s["W"] for s in first] == [s["W"] for s in second]

        # A structural fingerprint of seed 42's family. If make_family stops
        # honouring its argument, or the generator changes, this moves and the
        # §8 data set is no longer the one the paper describes.
        flat = np.concatenate([np.asarray(s["W"], float).ravel() for s in first])
        assert len(first) == 216
        assert flat.shape[0] == sum(np.asarray(s["W"], float).size for s in first)
        assert abs(float(np.abs(flat).sum()) - 378.9924) < 1e-3, (
            "seed-42 family fingerprint moved — either the seed is not honoured "
            "or the generator changed; §8's data set is no longer as described")


class TestMeraUsesEachIsometry:
    """
    mutate.py::mera-wrong-isometry

    The reimplementation's headline control is that perturbing a layer moves
    the state, where the retired version scored exactly 0. But that control
    catches a ZEROED tensor, not a WRONG one: replacing every per-site isometry
    with one fixed isometry destroyed the network and all 33 MERA tests passed.
    """

    def test_swapping_in_one_isometry_everywhere_changes_the_state(self):
        from quantum.tensor_network import MERATensorNetwork
        a = MERATensorNetwork(num_sites=16, bond_dim=2, seed=7)
        psi_true = a.boundary_state().copy()

        b = MERATensorNetwork(num_sites=16, bond_dim=2, seed=7)
        # Use ONE valid isometry at every site, rather than each site's own.
        # Every tensor stays a legitimate isometry, so this is not caught by
        # any isometry/unitarity check -- only by the state actually differing.
        fixed = b.isometries[0][0]
        b.isometries = [[fixed for _ in layer] for layer in b.isometries]
        b._state = None                      # bypass the memoised state
        from quantum import tensor_network as tn
        tn._STATE_CACHE.clear()              # ...and the module-level cache
        psi_wrong = b.boundary_state()

        assert psi_true.shape == psi_wrong.shape
        assert np.linalg.norm(psi_true - psi_wrong) > 1e-6, (
            "the MERA state is unchanged when every per-site isometry is "
            "replaced by one fixed isometry — the network is not using them")


class TestGaussBonnetFlagIsComputed:
    """
    mutate.py::gauss-bonnet-flag

    `passes` is `residual < 1e-9`. Forcing it True was not noticed, because
    every test asserted the residual directly and none asserted that the flag
    tracks it.
    """

    def test_flag_agrees_with_the_residual_it_reports(self):
        from gravity.einstein_2d import EmergentEinstein2D
        res = EmergentEinstein2D(num_points=50, seed=42).gauss_bonnet_check()
        assert res["passes"] == (res["residual"] < 1e-9), (
            "the passes flag does not track its own residual")

    def test_flag_goes_False_on_a_triangulation_that_violates_the_identity(self):
        """
        The flag must be able to come out False, on real input.

        Asserting `passes == (residual < 1e-9)` on the intact mesh is not
        enough: the residual there is ~5e-15, so both sides are True and a
        hardcoded `True` satisfies the assertion. Removing a triangle breaks
        the complex so the angle sum no longer matches 2*pi*chi, and the flag
        must follow the residual down.
        """
        from gravity.einstein_2d import EmergentEinstein2D
        m = EmergentEinstein2D(num_points=50, seed=42)

        intact = m._gauss_bonnet_on(m.simplices)
        assert intact["residual"] < 1e-9 and intact["passes"] is True

        broken = m._gauss_bonnet_on(m.simplices[:-1])
        assert broken["residual"] > 1e-3, (
            "dropping a triangle did not break the identity — pick a different "
            "corruption, this test proves nothing as written")
        assert broken["passes"] is False, (
            "Gauss-Bonnet reported passes=True on a triangulation whose "
            "residual is {:.4f} — the flag is not computed".format(
                broken["residual"]))


class TestGleasonDimensionGuard:
    """
    mutate.py::gleason-dimension

    Gleason's theorem requires dim >= 3; qubits are the known exception. The
    guard was `self.dim >= 3`, and relaxing it to `>= 0` was not noticed.
    """

    def test_constructor_rejects_dimension_below_three(self):
        """
        The LIVE guard is in the constructor, not in verify_conditions().

        Running the mutation exposed something the report had not: because
        __init__ raises for dim < 3, the later `c1 = self.dim >= 3` can never
        be False for any object that exists. It is unreachable-False -- dead
        code, and a member of the same "cannot fail" class the 2026 review
        catalogued. No behavioural test could have caught mutating it, so the
        honest fixes are to test the guard that IS live (here) and to label
        c1 in the module for what it is.
        """
        from quantum.gleason import GleasonVerification
        with pytest.raises(ValueError, match=r"dimension"):
            GleasonVerification(dimension=2)
        with pytest.raises(ValueError):
            GleasonVerification(dimension=1)

    def test_c1_is_structurally_true_and_says_so(self):
        from quantum.gleason import GleasonVerification
        c1 = GleasonVerification(dimension=4).verify_conditions()["C1_dimension_ge_3"]
        assert c1["satisfied"] is True
        assert "cannot be False" in c1["note"], (
            "C1 is unreachable-False (the constructor already enforces dim>=3) "
            "and the module must say so rather than presenting it as a check")

    def test_dimension_three_and_above_satisfies_C1(self):
        from quantum.gleason import GleasonVerification
        for d in (3, 4):
            assert GleasonVerification(dimension=d).verify_conditions() \
                ["C1_dimension_ge_3"]["satisfied"] is True


class TestChshIsComputedFromTheState:
    """
    mutate.py::entanglement-chsh-constant

    quantum/entanglement.py was rewritten 2026-08-15 to consume its input
    state, and returns separable/singlet controls to prove it. But pinning
    CHSH_S_value to the Tsirelson value was not noticed, because no test
    asserted what the CONTROLS return.
    """

    def test_separable_state_does_not_violate(self):
        from quantum.entanglement import NonDualEntanglement
        r = NonDualEntanglement().bell_inequality_violation()
        sep = r["state_dependence_controls"]["separable_|00>"]
        assert abs(sep["CHSH_S_value"] - np.sqrt(2)) < 1e-6, (
            f"separable |00> returned {sep['CHSH_S_value']} — the CHSH value is "
            f"not being computed from the state")
        assert sep["violates_classical"] is False

    def test_controls_span_a_real_range(self):
        """A pinned constant would collapse the spread to zero."""
        from quantum.entanglement import NonDualEntanglement
        r = NonDualEntanglement().bell_inequality_violation()
        vals = [r["CHSH_S_value"]] + [
            c["CHSH_S_value"] for c in r["state_dependence_controls"].values()]
        assert max(vals) - min(vals) > 1.0, (
            f"all CHSH values collapsed to {vals} — the statistic ignores its input")
        assert r["output_depends_on_state"] is True
