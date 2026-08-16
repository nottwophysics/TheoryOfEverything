"""Tests for the constants module — derivation, fine structure, cosmological.

HONESTY NOTE (2026-08-15 test-suite audit)
------------------------------------------
Most of the assertions in this file used to be either ``isinstance(result, dict)``
or a comparison of a module literal against the same literal written out again in
the test (``assert result["heegner_number"] == 163``). A stub-scan confirmed the
consequence: ``FineStructureDerivation.attempt_geometric``,
``ConstantsFromConsciousness.attempt_mass_ratios`` and
``CosmologicalConstant.vacuum_energy_problem`` could each be replaced by a
hand-written literal dict and this file stayed green.

Every assertion below now either (a) recomputes the quantity from a closed form
or a literature value that is written independently of the module, or (b) pins a
documented FAILURE (these α "derivations" do not work, and the tests say so).
Tests that only pin editorial prose are named ``*_contract`` so they cannot be
read as evidence.
"""

import numpy as np
import pytest

from numerology.derivation import ConstantsFromConsciousness
from numerology.fine_structure import FineStructureDerivation
from constants.cosmological import CosmologicalConstant
from numerology.fine_structure_v3 import FineStructureV3, SelfReferentialDerivation, ModularBootstrap, HolographicConstraint

# CODATA 2018 fine-structure constant, written here independently of the module.
CODATA_ALPHA_INV = 137.035999084

# PDG 2020 charged-lepton masses (MeV), written here independently of the module.
PDG_M_E = 0.51099895
PDG_M_MU = 105.6583755
PDG_M_TAU = 1776.86


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            return False
    return True


def _superstable_r(n: int, lo: float, hi: float, tol: float = 1e-13) -> float:
    """Parameter r at which x = 1/2 lies on the superstable 2**n cycle of the
    logistic map f_r(x) = r x (1 - x). Solved here by bisection — no module code
    is involved, so this is an independent computation."""
    k = 2 ** n

    def g(r):
        x = 0.5
        for _ in range(k):
            x = r * x * (1.0 - x)
        return x - 0.5

    a, b = lo, hi
    fa = g(a)
    assert fa * g(b) < 0, f"bad bracket for n={n}"
    for _ in range(200):
        m = 0.5 * (a + b)
        fm = g(m)
        if fa * fm <= 0:
            b = m
        else:
            a, fa = m, fm
        if b - a < tol:
            break
    return 0.5 * (a + b)


class TestConstantsFromConsciousness:
    def test_self_reference_fixed_point(self):
        cc = ConstantsFromConsciousness()
        result = cc.self_reference_fixed_point()
        # phi is the positive root of x^2 - x - 1 = 0; check that identity
        # rather than a decimal expansion of the same literal.
        phi = result["golden_ratio"]["value"]
        assert abs(phi ** 2 - phi - 1.0) < 1e-9
        assert abs(result["euler_number"]["value"] - np.exp(1.0)) < 1e-12
        # pi is summed from the (very slowly converging) Leibniz series, so it
        # is only good to ~1e-4. Pin the accuracy the method actually achieves.
        pi_val = result["pi"]["value"]
        assert abs(pi_val - np.pi) < 1e-3
        assert abs(pi_val - np.pi) > 1e-6, (
            "Leibniz series with 10000 terms cannot be exact — if this passes "
            "the method is no longer summing the series it documents")

    def test_information_theoretic(self):
        cc = ConstantsFromConsciousness()
        result = cc.information_theoretic_constants()
        # Closed forms, written independently: ln 2, ln 3, log_2(3), 2*pi.
        assert abs(result["bit_entropy"] - np.log(2)) < 1e-12
        assert abs(result["guna_entropy"] - np.log(3)) < 1e-12
        assert abs(result["dimension_ratio"] - np.log2(3)) < 1e-12
        assert abs(result["holographic_bound_unit_sphere"] - 2 * np.pi) < 1e-12

    def test_koide_formula(self):
        """Koide Q recomputed independently from the lepton masses.

        HISTORY (fixed 2026-08-15): this test was previously guarded by
        ``if "koide_ratio" in result:`` — a key the module has never returned —
        so the body never executed and the test asserted nothing at all.
        """
        cc = ConstantsFromConsciousness()
        result = cc.attempt_mass_ratios()
        koide = result["koide_formula"]

        # The module's own (rounded) inputs, restated here.
        m_e, m_mu, m_tau = 0.511, 105.7, 1776.9
        q_independent = ((m_e + m_mu + m_tau)
                         / (np.sqrt(m_e) + np.sqrt(m_mu) + np.sqrt(m_tau)) ** 2)
        assert abs(koide["computed"] - q_independent) < 1e-12, (
            "module's Koide Q does not match the formula it documents")

        # Q is CLOSE to 2/3 but is not 2/3: with these masses it sits 6.0e-5
        # (relative) below. Both bounds matter — the lower one would fail for a
        # stub that simply returned 2/3.
        rel_dev = abs(q_independent - 2 / 3) / (2 / 3)
        assert rel_dev < 1e-4
        assert rel_dev > 1e-6, "Q must not come out exactly 2/3 — that would be a stub"
        assert abs(koide["accuracy"] - rel_dev) < 1e-12

        # Mass ratios must reproduce the PDG values to the precision allowed by
        # the module's rounded inputs (~0.05%).
        ratios = result["mass_ratios"]
        assert abs(ratios["mu/e"] / (PDG_M_MU / PDG_M_E) - 1.0) < 5e-3
        assert abs(ratios["tau/mu"] / (PDG_M_TAU / PDG_M_MU) - 1.0) < 5e-3
        assert abs(ratios["tau/e"] / (PDG_M_TAU / PDG_M_E) - 1.0) < 5e-3

    def test_run_all_derivations_delegates(self):
        """run_all_derivations must return the SAME numbers as the individual
        methods (it is an orchestrator; a stub would break this)."""
        cc = ConstantsFromConsciousness()
        result = cc.run_all_derivations()
        assert (result["information_theory"]["bit_entropy"]
                == pytest.approx(cc.information_theoretic_constants()["bit_entropy"]))
        assert (result["mass_ratios"]["koide_formula"]["computed"]
                == pytest.approx(cc.attempt_mass_ratios()["koide_formula"]["computed"]))


class TestFineStructureDerivation:
    def test_geometric_attempts_recomputed(self):
        """Each geometric α "attempt" is recomputed from its own closed form."""
        fsd = FineStructureDerivation()
        result = fsd.attempt_geometric()
        alpha = result["target"]
        assert abs(1.0 / alpha - CODATA_ALPHA_INV) < 1e-6, "target is not CODATA alpha"

        a = result["attempts"]
        # pi/(6 pi^2 - pi) = 1/(6 pi - 1)
        assert abs(a["pi/(6pi^2-pi)"]["value"] - 1.0 / (6 * np.pi - 1)) < 1e-15
        assert abs(a["1/(2^7+2^3+2^0+2^-3)"]["value"] - 1.0 / 137.125) < 1e-15
        assert abs(a["cos(pi/137)"]["value"] - np.cos(np.pi / 137)) < 1e-15
        phi = (1 + np.sqrt(5)) / 2
        assert abs(a["1/(phi^7 * pi/2)"]["value"] - 1.0 / (phi ** 7 * np.pi / 2)) < 1e-15

        # Honest reading: only the hand-tuned binary expansion 1/137.125 lands
        # anywhere near alpha, and it is a fit, not a derivation. The other three
        # are off by 100%+ and must stay flagged as non-matches.
        assert a["1/(2^7+2^3+2^0+2^-3)"]["matches"] is True
        assert a["pi/(6pi^2-pi)"]["matches"] is False
        assert a["cos(pi/137)"]["matches"] is False
        assert a["1/(phi^7 * pi/2)"]["error"] > 1.0  # >100% off

    def test_information_theoretic_route_misses_alpha(self):
        """The channel-capacity route is reproduced exactly and then shown to FAIL."""
        fsd = FineStructureDerivation()
        result = fsd.attempt_information_theoretic()
        # sum_{k=1..7} 2^-k is the geometric series 1 - 2^-7 = 127/128.
        assert abs(result["self_reference_correction"] - (1 - 2 ** -7)) < 1e-15
        expected_inv = 2 ** 7 + (1 - 2 ** -7) + 2
        assert abs(result["estimated_1_over_alpha"] - expected_inv) < 1e-12
        assert abs(result["estimated_alpha"] - 1.0 / expected_inv) < 1e-15
        # 130.99 vs 137.036 is a 4.4% miss — this is a documented failure, not a
        # derivation, and the test pins the failure so it cannot quietly improve
        # into a "success" by changing the fudge terms.
        assert abs(result["error_percent"]
                   - abs(expected_inv - 137.036) / 137.036 * 100) < 1e-9
        assert result["error_percent"] > 4.0

    def test_alpha_significance_contract(self):
        """CONTRACT ONLY — this method is editorial prose plus one number.

        The only checkable content is that the quoted alpha is CODATA's; the
        anthropic-window strings are not evidence of anything and are not
        asserted here.
        """
        fsd = FineStructureDerivation()
        result = fsd.demonstrate_alpha_significance()
        assert abs(1.0 / result["value"] - CODATA_ALPHA_INV) < 1e-6
        assert set(result["anthropic_window"]) == {
            "if_alpha_larger", "if_alpha_smaller", "actual_range"}


class TestCosmologicalConstant:
    def test_vacuum_energy_discrepancy_is_the_known_120_orders(self):
        cc = CosmologicalConstant()
        result = cc.vacuum_energy_problem()
        # Independent recomputation from the module's stated observed value.
        expected = -np.log10(result["observed_planck"])
        assert abs(result["discrepancy_orders_of_magnitude"] - expected) < 1e-9
        # The literature figure for the cosmological-constant problem is
        # ~120 orders of magnitude; the module must land in that band.
        assert 118.0 < result["discrepancy_orders_of_magnitude"] < 124.0
        assert result["qft_prediction_planck"] == 1.0

    def test_consciousness_resolution_is_order_of_magnitude_only(self):
        cc = CosmologicalConstant()
        result = cc.consciousness_resolution()
        pred = result["consciousness_prediction"]
        obs = result["observed"]
        # 1/S with S = 10^122 gives 1e-122 against an observed 2.888e-122:
        # same order of magnitude, NOT a match. Pin both facts.
        assert abs(np.log10(pred) - np.log10(obs)) < 1.0
        assert abs(pred / obs - 1.0) > 0.1, (
            "an exact match would mean the module started fitting the observed "
            "value; the documented claim is order-of-magnitude consistency only")
        # The caveats that make this honest must survive.
        assert any("empirical input" in c for c in result["caveats"])
        assert any("not a derivation" in c for c in result["caveats"])

    def test_dark_energy_composition_matches_planck_2018(self):
        cc = CosmologicalConstant()
        comp = cc.dark_energy_as_residual_maya()["composition"]
        # Planck 2018 concordance values, written independently.
        assert abs(comp["dark_energy"] - 0.685) < 0.01
        assert abs(comp["dark_matter"] - 0.265) < 0.01
        assert abs(comp["ordinary_matter"] - 0.049) < 0.01
        assert abs(sum(comp.values()) - 1.0) < 0.01

    def test_run_all_delegates(self):
        cc = CosmologicalConstant()
        result = cc.run_all()
        flat = str(result)
        # Orchestrator must carry the individual results, not a summary literal.
        assert str(cc.vacuum_energy_problem()["discrepancy_orders_of_magnitude"]) in flat


class TestFineStructureV3:
    def test_feigenbaum_delta_matches_independent_bifurcation_computation(self):
        """delta is a hardcoded literal in the module; recompute it here."""
        sr = SelfReferentialDerivation()
        result = sr.logistic_fixed_point()

        brackets = [(1.9, 2.1), (3.1, 3.3), (3.49, 3.51), (3.554, 3.5551),
                    (3.5666, 3.5667), (3.56922, 3.56926)]
        s = [_superstable_r(n, lo, hi) for n, (lo, hi) in enumerate(brackets)]
        # Sanity anchor with a closed form: the superstable 2-cycle sits at 1+sqrt(5).
        assert abs(s[1] - (1 + np.sqrt(5))) < 1e-10
        delta_est = (s[4] - s[3]) / (s[5] - s[4])
        assert abs(result["feigenbaum_delta"] - delta_est) < 2e-3, (
            f"module delta {result['feigenbaum_delta']} vs independently "
            f"computed {delta_est}")
        assert len(result["attempts"]) >= 3
        # None of the three routes reaches alpha: best is far off.
        assert min(a["error_pct"] for a in result["attempts"]) > 1.0

    def test_continued_fraction(self):
        sr = SelfReferentialDerivation()
        result = sr.continued_fraction_analysis()
        # The leading partial quotient is floor(1/alpha) — recomputed, not echoed.
        assert result["cf_coefficients"][0] == int(np.floor(CODATA_ALPHA_INV))
        # Every convergent must actually be a convergent of 1/alpha: errors must
        # decrease and the last one must be very close.
        errs = [c["error_pct"] for c in result["convergents"]]
        assert len(errs) > 3
        assert errs[-1] < 1e-6
        assert errs[-1] < errs[0]
        assert result["is_simple_fraction"] is False, (
            "1/alpha is not a ratio of small integers")

    def test_modular_bootstrap_heegner_and_best_fit(self):
        mb = ModularBootstrap()
        result = mb.j_invariant_approach()
        h = result["heegner_number"]
        # Rabinowitsch criterion: disc -h has class number one iff
        # n^2 + n + (h+1)/4 is prime for n = 0 .. (h+1)/4 - 2. Verified here
        # rather than asserting `h == 163`.
        q = (h + 1) // 4
        assert 4 * q - 1 == h
        assert all(_is_prime(n * n + n + q) for n in range(q - 1))
        # Ramanujan's constant.
        assert abs(result["ramanujan_constant"] - np.exp(np.pi * np.sqrt(h))) < 1e5

        best = result["best"]
        assert best["error_pct"] < 1.0
        # Recompute the winning expression independently.
        assert abs(best["alpha_inv"] - (163 - 26 + np.pi / 100)) < 1e-9
        assert abs(best["error_pct"]
                   - abs(best["alpha_inv"] - CODATA_ALPHA_INV) / CODATA_ALPHA_INV * 100) < 1e-9
        # It is a fit, not a hit: it does not reproduce alpha.
        assert best["error_pct"] > 1e-4

    def test_holographic_constraint_fails_to_reproduce_alpha(self):
        """Every holographic route is recomputed and every one MISSES by >10%."""
        hc = HolographicConstraint()
        result = hc.holographic_alpha()
        d, n_charged = result["spacetime_dimensions"], result["charged_species"]
        n_gauge, n_gen = result["gauge_bosons"], result["generations"]
        by_method = {a["method"]: a for a in result["attempts"]}

        assert abs(by_method["1/(4π × N_charged × d)"]["alpha_inv"]
                   - 4 * np.pi * n_charged * d) < 1e-9
        assert abs(by_method["1/(N_gauge × N_gen × π)"]["alpha_inv"]
                   - n_gauge * n_gen * np.pi) < 1e-9
        assert abs(by_method["c/(4π² × N_charged)"]["alpha_inv"]
                   - 4 * np.pi ** 2 * n_charged / 2) < 1e-9

        for a in result["attempts"]:
            assert abs(a["error_pct"]
                       - abs(a["alpha_inv"] - CODATA_ALPHA_INV) / CODATA_ALPHA_INV * 100) < 1e-9
        assert min(a["error_pct"] for a in result["attempts"]) > 10.0, (
            "the holographic route does not reproduce alpha — if this ever "
            "passes, the constraint has been retuned to the answer")

    def test_run_all_approaches(self):
        fs = FineStructureV3()
        result = fs.run_all_approaches()
        assert abs(result["target"] - CODATA_ALPHA_INV) < 1e-9
        best = result["best_result"]
        # The ranking must actually be sorted by error, and best must be its head.
        errs = [r["error_pct"] for r in result["ranking"]]
        assert errs == sorted(errs)
        assert abs(best["error_pct"] - errs[0]) < 1e-12
        assert abs(best["error_pct"]
                   - abs(best["alpha_inv"] - CODATA_ALPHA_INV) / CODATA_ALPHA_INV * 100) < 1e-6
        assert best["error_pct"] < 1.0


class TestKoideRelation:
    def test_q_value_verification(self):
        from constants.koide import KoideRelation
        q = KoideRelation().q_value()
        # Independent recomputation from the PDG masses written at module top.
        q_indep = ((PDG_M_E + PDG_M_MU + PDG_M_TAU)
                   / (np.sqrt(PDG_M_E) + np.sqrt(PDG_M_MU) + np.sqrt(PDG_M_TAU)) ** 2)
        assert abs(q["Q_computed"] - q_indep) < 1e-12
        assert q["holds_to_1e-3"] is True
        assert q["rel_error_pct"] < 0.1
        # ...but it is NOT exact, and the module must not claim so.
        assert q["abs_error"] > 1e-8
        assert q["citation"] == "10.1103/PhysRevLett.47.1241"

    def test_tau_holdout_prediction(self):
        from constants.koide import KoideRelation
        p = KoideRelation().predict_tau()
        # Solve the same zero-parameter quadratic independently: with
        # s = sqrt(m_tau) and A = sqrt(m_e)+sqrt(m_mu),
        #   m_e + m_mu + s^2 = (2/3)(A + s)^2.
        A = np.sqrt(PDG_M_E) + np.sqrt(PDG_M_MU)
        roots = np.roots([1 - 2 / 3, -(4 / 3) * A, (PDG_M_E + PDG_M_MU) - (2 / 3) * A ** 2])
        m_tau_indep = float(max(r ** 2 for r in roots))
        assert abs(p["m_tau_predicted_MeV"] - m_tau_indep) < 1e-6
        assert p["free_parameters"] == 0
        # The prediction lands within 0.05% of the measured tau mass.
        assert abs(m_tau_indep - PDG_M_TAU) / PDG_M_TAU * 100 < 0.05
        assert abs(p["rel_error_pct"]
                   - abs(m_tau_indep - PDG_M_TAU) / PDG_M_TAU * 100) < 1e-9
        assert 1770 < p["m_tau_predicted_MeV"] < 1785
