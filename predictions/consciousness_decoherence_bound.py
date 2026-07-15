"""
P4 developed fully: consciousness-dependent decoherence as a quantitative,
falsifiable BOUNDED CONJECTURE (roadmap item 19)
==================================================================

The framework's P4 (`predictions/testable.py`) is the project's only claim that
is not borrowed from mainstream physics: that conscious observation produces a
decoherence signature distinct from environmental decoherence. As written it is
*qualitative* ("the rate differs") and leans on discredited PEAR / Global
Consciousness Project results. The roadmap demands we either derive a
quantitative effect size from the axioms or drop it.

**Honest finding first.** The framework's consciousness axioms
(`philosophy/brahman/consciousness.py`) contain NO parameter with physical
units — Brahman is a normalized field with a dimensionless "coherence" ratio,
and the consciousness signatures use dimensionless IIT Φ. There is therefore no
quantity in the stated axioms that fixes the magnitude of a decoherence rate.
**P4 cannot be a derivation.** Pretending otherwise would be dishonest.

**What we CAN do — make it sharp and falsifiable.** Introduce the single
phenomenological coupling the framework would need, define it operationally, map
it to a directly measured quantity, bound it from existing null experiments, and
specify the experiment (with a power calculation) that would detect or further
constrain it. This converts an untestable slogan into a quantitative conjecture
with an experimental upper bound.

Operational definition
----------------------
In a which-path / quantum-eraser interferometer, standard QM fixes the fringe
visibility ``V`` from the physical which-path distinguishability ``D`` via the
complementarity bound ``V² + D² ≤ 1`` (Englert 1996). Consciousness plays no
role. The conjecture adds ONE dimensionless coupling ``ε ≥ 0``: conscious
observation of the which-path record suppresses visibility by an extra factor,

    V_conscious = V_physical · (1 − ε),

with everything physical (which-path coupling, detector interaction, EMF,
thermal, gravitational) held identical between the conscious and automated arms.
An experiment that compares visibility under conscious observation vs automated
recording therefore measures

    ε = (V_auto − V_conscious) / V_auto   (=  ΔV / V ).

``ε = 0`` is standard QM (all interpretations agree). ``ε > 0`` is the
framework-unique claim. This is now falsifiable: any measured ΔV/V consistent
with 0 at the experiment's precision sets ``ε < precision``.

References (all DOIs verified via CrossRef):
  * Englert, complementarity / V²+D²≤1: Phys. Rev. Lett. 77, 2154 (1996),
    DOI 10.1103/PhysRevLett.77.2154.
  * Walborn et al., double-slit quantum eraser: Phys. Rev. A 65, 033818 (2002),
    DOI 10.1103/PhysRevA.65.033818.
  * Kim et al., delayed-choice quantum eraser: Phys. Rev. Lett. 84, 1 (2000),
    DOI 10.1103/PhysRevLett.84.1.
  * Jacques et al., realization of Wheeler's delayed choice: Science 315, 966
    (2007), DOI 10.1126/science.1136303.
  * Ma, Kofler & Zeilinger, review of delayed-choice experiments:
    Rev. Mod. Phys. 88, 015005 (2016), DOI 10.1103/RevModPhys.88.015005.

None of these experiments — the standard body of which-path / eraser work — has
ever reported an observer-consciousness dependence; all agree with QM (ε = 0) to
their measurement precision. That is the current empirical bound on ε.
"""

from __future__ import annotations

import numpy as np

# verified-CrossRef reference DOIs
REFERENCES = {
    "englert_1996": "10.1103/PhysRevLett.77.2154",
    "walborn_2002": "10.1103/PhysRevA.65.033818",
    "kim_2000": "10.1103/PhysRevLett.84.1",
    "jacques_2007": "10.1126/science.1136303",
    "ma_2016": "10.1103/RevModPhys.88.015005",
}

# The framework exposes NO parameter that fixes epsilon. This flag records that
# fact so callers cannot mistake the conjecture for a derivation.
EPSILON_IS_DERIVABLE_FROM_AXIOMS = False


def epsilon_from_visibilities(v_auto: float, v_conscious: float) -> float:
    """Measured consciousness coupling ε = (V_auto − V_conscious)/V_auto."""
    if v_auto <= 0:
        raise ValueError("V_auto must be positive")
    return (v_auto - v_conscious) / v_auto


def upper_bound_from_null(visibility_precision: float,
                          v_reference: float = 1.0,
                          confidence_sigma: float = 2.0) -> float:
    """Upper bound on ε implied by a null experiment that confirms QM visibility.

    If a measurement determines the visibility to an absolute 1σ precision
    ``sigma_V = visibility_precision`` and finds no deviation from the QM value
    ``v_reference``, then at ``confidence_sigma`` σ the fractional suppression is
    bounded by  ε < confidence_sigma · sigma_V / v_reference.
    """
    return confidence_sigma * visibility_precision / v_reference


def trials_needed(epsilon_target: float, sigma_V_single: float,
                  v_reference: float = 1.0,
                  alpha: float = 0.05, power: float = 0.8) -> int:
    """Number of independent trials to detect a coupling ``epsilon_target``.

    Two-sided z-test on the visibility difference ΔV = ε·V_ref. Per-trial
    visibility noise ``sigma_V_single``; combined noise over N trials
    ``sigma_V_single/√N``. Require signal ≥ (z_{1-α/2} + z_{1-power}) · noise:

        N ≥ [ (z_{1-α/2} + z_{power}) · sigma_V_single / (ε · V_ref) ]²
    """
    from scipy.stats import norm
    if epsilon_target <= 0:
        raise ValueError("epsilon_target must be positive")
    z_alpha = norm.ppf(1.0 - alpha / 2.0)
    z_power = norm.ppf(power)
    signal = epsilon_target * v_reference
    n = ((z_alpha + z_power) * sigma_V_single / signal) ** 2
    return int(np.ceil(n))


class ConsciousnessDecoherenceBound:
    """Quantitative, falsifiable treatment of P4 as a bounded conjecture."""

    def __init__(self, v_reference: float = 1.0):
        self.v_reference = v_reference

    def analyze_experiment(self, v_auto: float, v_conscious: float,
                           sigma_V: float, confidence_sigma: float = 2.0) -> dict:
        """Given a conscious-vs-automated visibility comparison, report the
        measured ε, whether it is consistent with 0, and the resulting bound."""
        eps = epsilon_from_visibilities(v_auto, v_conscious)
        sigma_eps = confidence_sigma * sigma_V / v_auto
        consistent_with_zero = abs(eps) <= sigma_eps
        return {
            "epsilon_measured": float(eps),
            "epsilon_uncertainty": float(sigma_eps),
            "consistent_with_standard_QM": bool(consistent_with_zero),
            "epsilon_upper_bound": float(max(0.0, eps) + sigma_eps),
            "confidence_sigma": confidence_sigma,
            "interpretation": (
                "consistent with epsilon = 0 (standard QM); consciousness "
                "coupling bounded above" if consistent_with_zero else
                "deviation from QM at this confidence — would require replication"
            ),
        }

    def design_test(self, epsilon_target: float, sigma_V_single: float,
                    alpha: float = 0.05, power: float = 0.8) -> dict:
        """Pre-registerable protocol summary + required sample size."""
        n = trials_needed(epsilon_target, sigma_V_single, self.v_reference,
                           alpha, power)
        return {
            "epsilon_target": epsilon_target,
            "per_trial_visibility_noise": sigma_V_single,
            "significance_alpha": alpha,
            "power": power,
            "trials_required": n,
            "protocol": [
                "Two-path interferometer (double-slit or Mach-Zehnder) with a "
                "which-path marker that can be read by (a) a conscious human "
                "observer or (b) an automated recorder, chosen at random per trial.",
                "Hold ALL physical interactions identical between arms: same "
                "marker coupling, same detector, same EMF/thermal/gravitational "
                "environment; the ONLY difference is whether a human consciously "
                "reads the record before the interference data are binned.",
                "Blind and pre-register: randomize arm assignment, blind the "
                "analyst to arm labels, fix N and the ε decision threshold before "
                "data collection.",
                "Estimate ε = (V_auto - V_conscious)/V_auto with bootstrap CIs; "
                "a null (CI contains 0) tightens the upper bound on ε.",
            ],
            "distinguishes_from": (
                "ALL standard QM interpretations (Copenhagen, many-worlds, pilot "
                "wave) predict epsilon = 0; any epsilon > 0 is unique to this "
                "framework."
            ),
        }

    def status(self) -> dict:
        """Honest status: the framework cannot predict ε; P4 is a conjecture."""
        return {
            "epsilon_derivable_from_axioms": EPSILON_IS_DERIVABLE_FROM_AXIOMS,
            "classification": "bounded conjecture (NOT a derivation)",
            "reason": (
                "The consciousness axioms contain no parameter with physical "
                "units, so no effect size can be computed from them. P4 makes a "
                "positive prediction only if a coupling axiom fixing epsilon is "
                "added; until then it is a falsifiable conjecture currently "
                "consistent with epsilon = 0."
            ),
            "recommendation": (
                "Reclassify P4 from 'prediction' to 'bounded conjecture'; retire "
                "the PEAR / GCP citations (methodologically discredited); state "
                "the current experimental bound and the protocol that would "
                "improve it."
            ),
        }


def _main() -> None:
    m = ConsciousnessDecoherenceBound()
    print("P4 as a bounded conjecture — status:")
    for k, v in m.status().items():
        print(f"  {k}: {v}")
    print("\nUpper bound on epsilon from a null experiment at 1% visibility precision:")
    print(f"  epsilon < {upper_bound_from_null(0.01):.3f}  (2 sigma)")
    print("\nExample: a real conscious-vs-automated comparison, both V≈0.90 ± 0.01:")
    res = m.analyze_experiment(v_auto=0.90, v_conscious=0.90, sigma_V=0.01)
    for k, v in res.items():
        print(f"  {k}: {v}")
    print("\nTrials needed to detect epsilon = 0.01 at per-trial noise 0.05:")
    print(f"  N = {trials_needed(0.01, 0.05)}")


if __name__ == "__main__":
    _main()
