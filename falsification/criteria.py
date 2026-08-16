"""
Falsification Criteria — What Would Disprove This Framework?

A theory that cannot be falsified is not scientific.
This module explicitly states what observations or experiments
would DISPROVE the consciousness-first framework.

Intellectual honesty requires this.

Updated 2026-08-15 (review): the registry now also records OUTCOMES —
including the one conjecture this repository itself falsified (Φ ≤ S;
see ``outcomes_to_date``) — and status fields have been refreshed
against published experimental results. A caveat the review surfaced:
F1, F3 and F5 are stated at a strength that may not be practically
triggerable (a phenomenal-consciousness test does not exist; sub-Planck
structure cannot currently be probed; "truly random" constants cannot be
established across unobservable regions). They are kept as in-principle
falsifiers, with that limitation stated here rather than hidden.
"""

import numpy as np


class FalsificationCriteria:
    """
    Explicit criteria that would falsify the consciousness-first ToE.
    """

    def core_falsifiers(self) -> dict:
        """
        Observations that would decisively refute the framework.
        """
        return {
            "F1_consciousness_from_computation": {
                "falsifier": "Demonstrating that a purely computational system "
                             "(with no quantum effects) produces genuine consciousness",
                "how_to_test": "Create an AI that passes all consciousness tests "
                               "(not just behavioral, but phenomenal) on a classical "
                               "computer with full understanding of its mechanism",
                "if_falsified": "Consciousness is emergent from computation, not fundamental. "
                                "The framework's core premise is wrong.",
                "current_status": "No system has demonstrated consciousness "
                                  "(as opposed to intelligence). Open question.",
            },
            "F2_local_hidden_variables": {
                "falsifier": "Discovery that Bell inequality violations are due to "
                             "local hidden variables (loophole in all Bell tests)",
                "how_to_test": "Close all loopholes simultaneously in a Bell test "
                               "and find NO violation",
                "if_falsified": "Reality is local and separable. Non-duality is wrong. "
                                "Advaita's 'everything is one' would be refuted.",
                "current_status": "All loophole-free Bell tests confirm violations. "
                                  "Non-locality is well-established.",
            },
            "F3_spacetime_fundamental": {
                "falsifier": "Proving that spacetime is fundamental (not emergent)",
                "how_to_test": "Show that spacetime structure exists below the "
                               "Planck scale with no holographic noise, no discreteness, "
                               "and no entanglement origin",
                "if_falsified": "Spacetime is not a projection of consciousness. "
                                "The holographic/emergent spacetime program fails.",
                "current_status": "No experiment probes sub-Planck structure yet. "
                                  "Note: the Fermilab Holometer (2015-2016) searched for "
                                  "Hogan-scale holographic noise at interferometer scales "
                                  "and EXCLUDED it — see the P5 status in "
                                  "docs/PREDICTIONS.md. Theoretical arguments for "
                                  "emergence remain, but the specific holographic-noise "
                                  "signature this repo's P5 encoded is ruled out.",
            },
            "F4_no_gravitational_decoherence": {
                "falsifier": "Observing quantum superposition of arbitrarily "
                             "large masses with no spontaneous decoherence",
                "how_to_test": "Create macroscopic quantum superpositions "
                               "(e.g., Schrodinger cat states for >10^12 amu)",
                "if_falsified": "Gravity does not cause decoherence. "
                                "The Maya-as-decoherence picture fails.",
                "current_status": "Largest superposition: ~10^4 amu. "
                                  "Gap of ~8 orders of magnitude to test.",
            },
            "F5_constants_arbitrary": {
                "falsifier": "Proving that physical constants are truly random "
                             "(e.g., from a multiverse with no selection principle)",
                "how_to_test": "Find that constants show NO mathematical relationships — "
                               "no Koide formula, no patterns, pure randomness",
                "if_falsified": "Constants are not determined by consciousness structure. "
                                "They are arbitrary parameters of a random vacuum.",
                "current_status": "Koide formula verified as arithmetic (0-parameter "
                                  "m_tau check, 0.006%). But this repo's own "
                                  "look-elsewhere analysis (Experiment 31) shows its "
                                  "fine-structure formula family hits essentially any "
                                  "target at the claimed precision — the alpha 'pattern' "
                                  "is numerology by the repo's own hold-out test. "
                                  "Suggestive structure remains an open question, "
                                  "not evidence.",
            },
        }

    def partial_falsifiers(self) -> dict:
        """
        Observations that would weaken (but not destroy) the framework.
        """
        return {
            "PF1_dark_energy_not_constant": {
                "observation": "Dark energy equation of state w ≠ -1",
                "impact": "Would complicate the 'residual Maya' interpretation "
                          "but not necessarily refute it (Maya could evolve)",
                "current_status": "DESI BAO results (2024-2025) in combination with "
                                  "CMB and supernovae prefer an EVOLVING w at up to "
                                  "~4 sigma — not yet definitive, but this partial "
                                  "falsifier is under active pressure, no longer "
                                  "'consistent with constant'.",
            },
            "PF2_information_destroyed": {
                "observation": "Information is destroyed in black holes "
                               "(Page curve is wrong)",
                "impact": "Would challenge 'consciousness cannot be destroyed' "
                          "but might be reinterpreted",
                "current_status": "Recent results (island formula) support "
                                  "information conservation",
            },
            "PF3_no_quantum_biology": {
                "observation": "No quantum effects in biological systems relevant "
                               "to consciousness",
                "impact": "Would weaken Penrose-Hameroff-type connections "
                          "but consciousness could still be fundamental via "
                          "different mechanisms",
                "current_status": "Some evidence for quantum biology "
                                  "(photosynthesis, avian navigation)",
            },
        }

    def what_cannot_be_falsified(self) -> dict:
        """
        Honestly state what aspects of the framework are NOT falsifiable
        (and therefore not strictly scientific).
        """
        return {
            "metaphysical_claims": {
                "brahman_exists": (
                    "The claim that pure consciousness exists beyond spacetime "
                    "cannot be tested by instruments within spacetime. "
                    "This is a metaphysical axiom, not a scientific hypothesis."
                ),
                "maya_is_illusion": (
                    "The claim that the empirical world is 'not ultimately real' "
                    "cannot be tested from within the empirical world. "
                    "This is like asking a dream character to prove the dream is a dream."
                ),
                "atman_brahman_identity": (
                    "The identity of individual and universal consciousness "
                    "is a matter of direct realization (anubhava), not "
                    "experimental measurement."
                ),
            },
            "honesty": (
                "A complete Theory of Everything likely needs BOTH: "
                "1) Scientific predictions (falsifiable physics), and "
                "2) Metaphysical framework (not falsifiable but internally consistent). "
                "This module addresses (1). The philosophical framework (2) is "
                "evaluated by different criteria: coherence, explanatory power, "
                "and consistency with experience."
            ),
        }

    def outcomes_to_date(self) -> dict:
        """
        Falsification OUTCOMES recorded against this framework's own claims.
        A registry that only lists criteria, never verdicts, is decoration;
        this method is where verdicts live.
        """
        return {
            "PHI_LE_S_FALSIFIED": {
                "claim": "Φ ≤ S_entanglement (integrated information bounded "
                         "by entanglement entropy) — Experiment 23 / paper §8",
                "verdict": "FALSIFIED (2026-07-15; numbers corrected by the "
                           "TPM-ordering audit, 2026-08-12)",
                "evidence": "Validated retest with canonical PyPhi Φ against the "
                            "entanglement entropy of transverse-field Ising ground "
                            "states (N=216 systems): 50 of the 51 nonzero-Φ systems "
                            "VIOLATE the bound (max Φ ≈ 4.0 bits vs S ≤ 0.83). The "
                            "raw Φ–S correlation (r ≈ +0.64) is a connectivity "
                            "confound (partial r ≈ −0.07, p = 0.29). Reproduction: "
                            "reproducibility/phi_s/.",
                "disposition": "Conjecture withdrawn from the paper (preprint v2, "
                               "doi:10.5281/zenodo.21007975). The original "
                               "'holds in 100% of trials' result was circular "
                               "(internal heuristic; see PYPHI_BENCHMARK_MEMO.md).",
            },
            "P5_HOLOGRAPHIC_NOISE_EXCLUDED": {
                "claim": "P5: correlated holographic noise in interferometers",
                "verdict": "Constrained by the Fermilab Holometer (2015-2016), "
                           "which searched for this class of holographic noise "
                           "and reported no signal. NOT established as excluded "
                           "here: that is a quantitative claim requiring a "
                           "comparison of the predicted ASD against the "
                           "Holometer's published sensitivity, and neither the "
                           "comparison nor a citation to the experimental paper "
                           "is in this repository.",
                "disposition": "P5 cannot count as a live novel prediction of "
                               "this framework -- but see docs/PREDICTIONS.md: "
                               "it was never entailed by A1-A4 in the first "
                               "place.",
            },
        }

    def full_report(self) -> dict:
        """Generate the complete falsification report."""
        return {
            "core_falsifiers": self.core_falsifiers(),
            "partial_falsifiers": self.partial_falsifiers(),
            "outcomes_to_date": self.outcomes_to_date(),
            "non_falsifiable": self.what_cannot_be_falsified(),
            "scientific_integrity": (
                "This framework makes testable predictions (P1-P5) and "
                "states explicit falsification criteria (F1-F5), and it records "
                "outcomes against itself: one conjecture (Φ ≤ S) has been "
                "FALSIFIED by the repo's own validated retest, and one predicted "
                "signature (P5 holographic noise) was excluded by experiment. "
                "If further predictions fail, the physics component is wrong. "
                "This is the standard we hold ourselves to."
            ),
        }
