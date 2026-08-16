#!/usr/bin/env python3
"""
Theory of Everything — Advaita Vedanta Computational Framework

A computational exploration of non-dual metaphysics, modeling how
a single consciousness (Brahman) appears as the manifold universe
through Maya, and how liberation (Moksha) is the recognition of
what was always the case.

Usage:
    python main.py                    # Quick demo
    python main.py --demo             # Quick demo of core concepts
    python main.py --all              # Run all 8 original Advaita experiments
    python main.py --physics          # Run physics extension experiments (9-31)
    python main.py --experiment N     # Run experiment N (1-31)
    python main.py --visualize        # Generate all visualizations
    python main.py --everything       # Run ALL experiments (1-31) + visualizations
"""

import sys
import os
import argparse
import json

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from philosophy.brahman.consciousness import Brahman
from philosophy.brahman.sat_chit_ananda import SatChitAnanda
from philosophy.maya.superimposition import Adhyasa
from philosophy.maya.nama_rupa import NamaRupa
from philosophy.maya.gunas import Gunas, GunaBalance
from philosophy.levels.reality_engine import RealityEngine
from emergence.spacetime import ConsciousnessField, EmergentSpacetime
from emergence.causation import Vivartavada
from emergence.observer import Sakshi, Experience
from philosophy.liberation.neti_neti import NetiNeti
from philosophy.liberation.mahavakya import Mahavakya
from simulations.experiments import (
    rope_snake_experiment,
    fractal_unity_experiment,
    observer_collapse_experiment,
    dreamer_analogy_experiment,
    neti_neti_debugger,
    guna_dynamics_experiment,
    mahavakya_experiment,
    causation_experiment,
    run_all_experiments,
)


def _print_result(title, result, indent=0):
    """Pretty-print a nested result dictionary."""
    prefix = "  " * indent
    if isinstance(result, dict):
        for key, value in result.items():
            if isinstance(value, dict):
                print(f"{prefix}  {key}:")
                _print_result("", value, indent + 1)
            elif isinstance(value, list) and len(value) > 5:
                print(f"{prefix}  {key}: [{len(value)} items]")
            elif isinstance(value, float):
                print(f"{prefix}  {key}: {value:.6f}")
            elif isinstance(value, str) and len(value) > 100:
                print(f"{prefix}  {key}: {value[:100]}...")
            else:
                print(f"{prefix}  {key}: {value}")


# ===== PHYSICS EXTENSION EXPERIMENTS (9-26) =====

def quantum_hilbert_experiment():
    """Experiment 9: Quantum Mechanics from Brahman."""
    print("\n" + "=" * 70)
    print("  EXPERIMENT 9: QUANTUM MECHANICS FROM BRAHMAN")
    print("=" * 70)

    from quantum.hilbert_space import BrahmanHilbertSpace

    Brahman.reset()
    H = BrahmanHilbertSpace(dimension=8)

    print("\n--- Brahman as Hilbert Space ---")
    demo = H.demonstrate_quantum_advaita()
    print(f"  Brahman entropy: {demo['brahman_entropy']:.6f}")
    print(f"  Brahman is pure: {demo['brahman_is_pure']}")
    print(f"  Insight: {demo['insight_1']}")
    print(f"\n  Entangled subsystem entropy: {demo['entangled_subsystem_entropy']:.6f}")
    print(f"  Subsystem appears mixed: {demo['subsystem_appears_mixed']}")
    print(f"  Insight: {demo['insight_2']}")
    print(f"\n  Resolution: {demo['resolution']}")

    Brahman.reset()
    return {"status": "completed", "experiment": "quantum_hilbert"}


def measurement_problem_experiment():
    """Experiment 10: The Measurement Problem Dissolved."""
    print("\n" + "=" * 70)
    print("  EXPERIMENT 10: THE MEASUREMENT PROBLEM — DISSOLVED")
    print("=" * 70)

    from quantum.measurement import AdvaiticMeasurement

    am = AdvaiticMeasurement(system_dim=4, environment_dim=16)
    result = am.demonstrate_measurement_problem_resolved()

    print(f"\n  System: {result['system_state']}")
    print(f"\n--- Brahman's View (Paramarthika) ---")
    bv = result['after_decoherence']['brahman_sees']
    print(f"  Perspective: {bv['perspective']}")
    print(f"  State: {bv['state']}")
    print(f"  Purity: {bv['purity']:.6f}")
    print(f"  Collapsed: {bv['collapsed']}")

    print(f"\n--- Jiva's View (Vyavaharika) ---")
    jv = result['after_decoherence']['jiva_sees']
    print(f"  Perspective: {jv['perspective']}")
    print(f"  State: {jv['state']}")
    print(f"  Purity: {jv['purity']:.6f}")
    print(f"  Appears collapsed: {jv['appears_collapsed']}")
    print(f"  Probabilities: {[f'{p:.4f}' for p in jv['probabilities']]}")

    print(f"\n  RESOLUTION: {result['resolution']}")

    return {"status": "completed", "experiment": "measurement_problem"}


def entanglement_nonduality_experiment():
    """Experiment 11: Entanglement as Non-Duality."""
    print("\n" + "=" * 70)
    print("  EXPERIMENT 11: ENTANGLEMENT IS NON-DUALITY")
    print("=" * 70)

    from quantum.entanglement import NonDualEntanglement

    nde = NonDualEntanglement(dimension=2)

    print("\n--- Bell Inequality Violation ---")
    bell = nde.bell_inequality_violation()
    print(f"  CHSH S-value: {bell['CHSH_S_value']:.4f}")
    print(f"  Classical bound: {bell['classical_bound']}")
    print(f"  Violates classical: {bell['violates_classical']}")
    print(f"  Insight: {bell['insight'][:120]}...")

    print("\n--- Non-Duality Demonstration ---")
    nd = nde.non_duality_demonstration()
    print(f"  Separable entropy: {nd['separable_state_entropy']:.6f}")
    print(f"  Entangled entropy: {nd['entangled_state_entropy']:.6f}")
    print(f"  Separation is illusion: {nd['separation_is_illusion']}")

    print("\n--- Monogamy of Entanglement ---")
    mono = nde.monogamy_of_entanglement()
    print(f"  Bell pair entanglement: {mono['bell_pair_entanglement']:.6f}")
    print(f"  GHZ state entanglement: {mono['ghz_state_A_entanglement']:.6f}")
    print(f"  Advaita parallel: {mono['advaita_parallel'][:100]}...")

    return {"status": "completed", "experiment": "entanglement_nonduality"}


def emergent_gravity_experiment():
    """Experiment 12: Gravity Emerging from Consciousness."""
    print("\n" + "=" * 70)
    print("  EXPERIMENT 12: GRAVITY FROM CONSCIOUSNESS")
    print("=" * 70)

    from gravity.metric import ConsciousnessMetric
    from gravity.entropic import EntropicGravity

    print("\n--- Space from Entanglement ---")
    cm = ConsciousnessMetric(num_points=20)
    space_demo = cm.demonstrate_space_from_entanglement()
    for key, val in space_demo.items():
        if key == "teaching":
            print(f"\n  Teaching: {val[:120]}...")
        elif isinstance(val, dict):
            print(f"  {key}: dist={val['avg_distance']:.4f}, "
                  f"entanglement={val['avg_entanglement']:.4f}, "
                  f"space_exists={val['space_exists']}")

    print("\n--- Newton recovery (Verlinde derivation, SI units) ---")
    eg = EntropicGravity()
    newton = eg.recover_newton(mass=1.0)
    print(f"  Newton correlation: {newton['newton_correlation']:.6f}")
    print(f"  Newton recovered: {newton['newton_recovered']}")
    for step in newton['derivation']:
        print(f"    {step}")
    print(f"  Insight: {newton['insight'][:120]}...")

    print("\n--- Black Hole as Maximum Maya ---")
    bh = eg.black_hole_as_maximum_maya(mass=10.0)
    print(f"  Mass: {bh['mass']}")
    print(f"  Schwarzschild radius: {bh['schwarzschild_radius']:.4f}")
    print(f"  Entropy: {bh['entropy']:.2f}")
    print(f"  Hawking temperature: {bh['hawking_temperature']:.6f}")
    print(f"  Insight: {bh['insight'][:120]}...")

    return {"status": "completed", "experiment": "emergent_gravity"}


def holographic_experiment():
    """Experiment 13: The Holographic Principle."""
    print("\n" + "=" * 70)
    print("  EXPERIMENT 13: HOLOGRAPHIC PRINCIPLE — REALITY AS PROJECTION")
    print("=" * 70)

    from gravity.holographic import HolographicBoundary

    hb = HolographicBoundary(boundary_dim=50, bulk_dim=20)
    result = hb.demonstrate_holographic_principle()

    print(f"\n  Boundary dimension: {result['boundary_dimension']}")
    print(f"  Bulk dimension: {result['bulk_dimension']}")
    print(f"  Boundary entropy: {result['boundary_entropy']:.4f}")
    print(f"  Bulk entropy: {result['bulk_entropy']:.4f}")
    print(f"  Reconstruction fidelity: {result['reconstruction_fidelity']:.4f}")
    print(f"  Boundary is fundamental: {result['boundary_is_fundamental']}")
    print("    ^ interpretive reading (the Advaita claim), NOT a computed result;")
    print(f"      reconstruction fidelity {result['reconstruction_fidelity']:.4f} is "
          f"near chance for this random projection.")
    print(f"\n  Summary: {result['summary'][:150]}...")

    rt = result['ryu_takayanagi']
    print(f"\n  Ryu-Takayanagi:")
    print(f"    Follows area law: {rt['follows_area_law']}")
    print(f"    Log-scaling correlation: {rt['log_scaling_correlation']:.4f}")

    return {"status": "completed", "experiment": "holographic"}


def particle_zoo_experiment():
    """Experiment 14: Particles from Maya's Symmetry Breaking."""
    print("\n" + "=" * 70)
    print("  EXPERIMENT 14: PARTICLES FROM MAYA'S SYMMETRY BREAKING")
    print("=" * 70)

    from particles.symmetry_breaking import MayaSymmetryBreaking
    from particles.particle_zoo import analyze_particle_zoo
    from particles.forces import FundamentalForces

    print("\n--- Symmetry Breaking ---")
    msb = MayaSymmetryBreaking(field_dimension=16)

    for temp in [2.0, 1.0, 0.5, 0.0]:
        result = msb.break_symmetry(temperature=temp)
        state = result['symmetry']
        vev = result['vev']
        print(f"  T={temp:.1f}: symmetry={state:8s}, VEV={vev:.4f}, "
              f"Higgs mass={result['higgs_mass']:.4f}")

    print("\n--- Particle Zoo Analysis ---")
    zoo = analyze_particle_zoo()
    print(f"  Total particles: {zoo['total_particles']}")
    print(f"  Closest to Brahman: {zoo['closest_to_brahman'][:3]}")
    print(f"  Deepest in Maya: {zoo['deepest_in_maya'][:3]}")
    print(f"\n  Three Generations = Three Gunas:")
    for gen, desc in zoo['three_generations_three_gunas'].items():
        print(f"    Gen {gen}: {desc}")

    print("\n--- Force Unification ---")
    ff = FundamentalForces()
    unif = ff.demonstrate_unification()
    print(f"  Unification energy: {unif['approximate_unification_energy_GeV']:.2e} GeV")
    print(f"  Insight: {unif['insight'][:120]}...")

    return {"status": "completed", "experiment": "particle_zoo"}


def constants_experiment():
    """Experiment 15: Deriving Physical Constants."""
    print("\n" + "=" * 70)
    print("  EXPERIMENT 15: PHYSICAL CONSTANTS FROM CONSCIOUSNESS")
    print("=" * 70)

    from numerology.derivation import ConstantsFromConsciousness
    from numerology.fine_structure import FineStructureDerivation
    from constants.cosmological import CosmologicalConstant

    print("\n--- Self-Reference Constants ---")
    cfc = ConstantsFromConsciousness()
    sr = cfc.self_reference_fixed_point()
    print(f"  Golden ratio: {sr['golden_ratio']['value']:.10f}")
    print(f"  Euler's number: {sr['euler_number']['value']:.10f}")
    print(f"  Pi: {sr['pi']['value']:.10f}")

    print("\n--- Fine Structure Constant ---")
    fsd = FineStructureDerivation()
    info = fsd.attempt_information_theoretic()
    print(f"  Estimated 1/α: {info['estimated_1_over_alpha']:.2f}")
    print(f"  Actual 1/α: {info['actual_1_over_alpha']}")
    print(f"  Error: {info['error_percent']:.2f}%")

    print("\n--- Koide Formula ---")
    mr = cfc.attempt_mass_ratios()
    print(f"  Koide ratio: {mr['koide_formula']['computed']:.6f}")
    print(f"  Target (2/3): {mr['koide_formula']['target']:.6f}")
    print(f"  Holds: {mr['koide_formula']['holds']}")

    print("\n--- Cosmological Constant ---")
    cc = CosmologicalConstant()
    res = cc.consciousness_resolution()
    print(f"  Traditional problem: {res['traditional_problem']}")
    print(f"  Consciousness prediction: {res['consciousness_prediction']:.2e}")
    print(f"  Match: {res['match']}")
    for step in res['reasoning']:
        print(f"    {step}")

    print("\n--- Dark Energy as Residual Maya ---")
    de = cc.dark_energy_as_residual_maya()
    comp = de['composition']
    print(f"  Dark energy: {comp['dark_energy']:.1%}")
    print(f"  Dark matter: {comp['dark_matter']:.1%}")
    print(f"  Ordinary matter: {comp['ordinary_matter']:.1%}")
    print(f"  Implication: {de['profound_implication'][:120]}...")

    return {"status": "completed", "experiment": "constants"}


def predictions_experiment():
    """Experiment 16: Testable Predictions & Falsification."""
    print("\n" + "=" * 70)
    print("  EXPERIMENT 16: TESTABLE PREDICTIONS & FALSIFICATION CRITERIA")
    print("=" * 70)

    from predictions.testable import TestablePredictions
    from falsification.criteria import FalsificationCriteria
    from falsification.experiments import CriticalExperiments

    print("\n--- 5 Testable Predictions ---")
    tp = TestablePredictions()
    preds = tp.all_predictions()
    for key in ["P1", "P2", "P3", "P4", "P5"]:
        p = preds[key]
        print(f"\n  {key}: {p['prediction'][:80]}...")
        if 'current_status' in p:
            print(f"       Status: {p['current_status'][:80]}")

    print(f"\n  Most decisive: {preds['summary']['most_decisive']}")

    print("\n--- 5 Falsification Criteria ---")
    fc = FalsificationCriteria()
    core = fc.core_falsifiers()
    for key in ["F1_consciousness_from_computation", "F2_local_hidden_variables",
                "F3_spacetime_fundamental", "F4_no_gravitational_decoherence",
                "F5_constants_arbitrary"]:
        f = core[key]
        print(f"\n  {key}:")
        print(f"    {f['falsifier'][:80]}...")
        print(f"    Status: {f['current_status'][:80]}")

    print("\n--- Experimental Roadmap ---")
    ce = CriticalExperiments()
    exps = ce.all_experiments()
    print(f"\n{exps['roadmap']}")

    # What is NOT falsifiable
    nf = fc.what_cannot_be_falsified()
    print(f"\n  Honesty: {nf['honesty'][:150]}...")

    return {"status": "completed", "experiment": "predictions_falsification"}


def interpretations_experiment():
    """Experiment 17: Four Interpretations of QM — Formal Comparison."""
    print("\n" + "=" * 70)
    print("  EXPERIMENT 17: FOUR INTERPRETATIONS OF QUANTUM MECHANICS")
    print("  Formal Comparison: Copenhagen vs Many-Worlds vs Pilot Wave vs Advaita")
    print("=" * 70)

    from quantum.interpretations import InterpretationComparison

    comp = InterpretationComparison()

    # 1. Axiom comparison
    print("\n" + "-" * 60)
    print("  PART 1: AXIOMS, SIDE BY SIDE (not counted)")
    print("-" * 60)
    axioms = comp.axiom_comparison()
    for key in ["copenhagen", "many_worlds", "pilot_wave", "advaita"]:
        a = axioms[key]
        print(f"\n  {a['name']}:")
        for ax in a['axioms']:
            print(f"    {ax}")
    print("\n  (No axiom count and no parsimony ranking: those were arithmetic")
    print("   on hand-written lists, deleted 2026-08-16. Read the axioms above.)")

    # 2. Empirical agreement
    print("\n" + "-" * 60)
    print("  PART 2: EMPIRICAL PREDICTIONS (must all agree)")
    print("-" * 60)
    agreement = comp.empirical_agreement()
    print(f"\n  P(up) = {agreement['P_up']:.4f}")
    print(f"  P(down) = {agreement['P_down']:.4f}")
    print(f"  All agree on P(up): {agreement['all_agree_on_P_up']}")
    print(f"  All agree on P(down): {agreement['all_agree_on_P_down']}")
    print(f"  Note: {agreement['note']}")

    # 3. Explanatory scope
    print("\n" + "-" * 60)
    print("  PART 3: EXPLANATORY SCOPE (8 phenomena)")
    print("-" * 60)
    scope = comp.explanatory_scope()
    for key in ["copenhagen", "many_worlds", "pilot_wave", "advaita"]:
        s = scope[key]
        print(f"\n  {s['name']}:")
        flagged = s['phenomena_flagging_a_residual_problem']
        print(f"    Flags a residual problem on: {', '.join(flagged) if flagged else 'none'}")
        print(f"    Cannot explain:")
        for item in s['cannot_explain'][:3]:
            print(f"      - {item[:80]}")

    # 4. The Consciousness Test
    print("\n" + "-" * 60)
    print("  PART 4: THE CONSCIOUSNESS TEST (the hard problem)")
    print("-" * 60)
    consciousness = comp.consciousness_comparison()
    for key in ["copenhagen", "many_worlds", "pilot_wave", "advaita"]:
        c = consciousness[key]
        status = "YES" if c['addresses_consciousness'] else "NO"
        print(f"\n  {c['name']}:")
        print(f"    Addresses consciousness: {status}")
        ans = c['answer']
        if len(ans) > 120:
            print(f"    Answer: {ans[:120]}...")
        else:
            print(f"    Answer: {ans}")

    # 5. Novel predictions
    print("\n" + "-" * 60)
    print("  PART 5: NOVEL PREDICTIONS — SECTION REMOVED (2026-08-16)")
    print("-" * 60)
    print("  This part scored each interpretation by the number of 'novel")
    print("  predictions' written for it in this module. The rivals' entries")
    print("  were their weakest claims, written here rather than quoted, and")
    print("  crediting this framework with novel predictions contradicts its")
    print("  own operational-equivalence claim (Experiment 24).")

    # 6. Advaita measurement demonstration
    print("\n" + "-" * 60)
    print("  PART 6: ADVAITA MEASUREMENT RESOLUTION (quantitative)")
    print("-" * 60)
    demo = comp.advaita_measurement_demo()
    print(f"\n  Total state purity (Brahman):  {demo['total_state_purity']:.6f}")
    print(f"  Total collapsed:               {demo['total_collapsed']}")
    print(f"  Reduced state purity (Jiva):   {demo['reduced_state_purity']:.6f}")
    print(f"  Appears collapsed:             {demo['reduced_appears_collapsed']}")
    print(f"  Coherence remaining:           {demo['coherence_remaining']:.6f}")
    print(f"  Classical probabilities:       {[f'{p:.4f}' for p in demo['classical_probabilities']]}")

    # 7. Summary table
    print("\n" + "-" * 60)
    print("  PART 7: SUMMARY COMPARISON TABLE")
    print("-" * 60)
    table = comp.summary_table()
    print(f"\n  {'Criterion':<35} {'Copenhagen':>12} {'Many-Worlds':>12} {'Pilot Wave':>12} {'Advaita':>12}")
    print(f"  {'-'*35} {'-'*12} {'-'*12} {'-'*12} {'-'*12}")

    keys = ["copenhagen", "many_worlds", "pilot_wave", "advaita"]
    row = lambda field: [str(table[k][field]) for k in keys]

    rows_to_print = [
        ("Year", "year"),
        ("Addresses consciousness", "addresses_consciousness"),
        ("Needs collapse postulate", "needs_collapse_postulate"),
        ("Needs hidden variables", "needs_hidden_variables"),
        ("Needs branching", "needs_branching"),
    ]
    for label, field_name in rows_to_print:
        vals = row(field_name)
        print(f"  {label:<35} {vals[0]:>12} {vals[1]:>12} {vals[2]:>12} {vals[3]:>12}")

    print(f"\n  VERDICT:")
    print(f"  - All four agree on empirical predictions (Born rule, Bell violation,")
    print(f"    etc.) — and this agreement is by construction: every interpretation")
    print(f"    here inherits one Born-rule computation from the shared base class.")
    print(f"  - The four differ in what they must POSIT: collapse, hidden variables,")
    print(f"    branching, or an experiential primitive. Those differences are")
    print(f"    structural properties of the axioms as stated, printed above.")
    print(f"  ")
    print(f"  Deleted 2026-08-16: the scoreboard that used to close this experiment")
    print(f"  (axiom counts, phenomena tallies, a novel-predictions ranking and a")
    print(f"  parsimony ordering). Every figure in it was len() of a list written")
    print(f"  in this module, so nothing about physics could have changed it. Two of")
    print(f"  its claims were also false against this module's own output: it called")
    print(f"  this framework the ONLY interpretation addressing consciousness, while")
    print(f"  consciousness_comparison() scores Many-Worlds True as well; and it")
    print(f"  credited the framework with 5 testable predictions, which contradicts")
    print(f"  the operational equivalence of Experiment 24.")

    return {"status": "completed", "experiment": "interpretations_comparison"}


def gleason_experiment():
    """Experiment 18: Gleason's Theorem — Born Rule as Theorem."""
    print("\n" + "=" * 70)
    print("  EXPERIMENT 18: GLEASON'S THEOREM")
    print("  The Born Rule Is a Theorem, Not an Axiom")
    print("=" * 70)

    from quantum.gleason import GleasonVerification

    gv = GleasonVerification(dimension=4)

    # Part 1: Verify Gleason's conditions
    print("\n" + "-" * 60)
    print("  PART 1: VERIFYING GLEASON'S CONDITIONS")
    print("-" * 60)
    conditions = gv.verify_conditions()
    for key in ["C1_dimension_ge_3", "C2_non_negativity", "C3_additivity", "C4_normalization"]:
        c = conditions[key]
        status = "PASS" if c["satisfied"] else "FAIL"
        print(f"\n  {key}: [{status}]")
        print(f"    {c['note']}")
        if "violations" in c:
            print(f"    Tests: {c.get('tests_run', 'N/A')}, Violations: {c['violations']}")

    print(f"\n  ALL CONDITIONS SATISFIED: {conditions['all_conditions_satisfied']}")
    print(f"  {conditions['conclusion']}")

    # Part 2: Uniqueness — only Born rule works
    print("\n" + "-" * 60)
    print("  PART 2: UNIQUENESS — NO ALTERNATIVE WORKS")
    print("-" * 60)
    uniqueness = gv.demonstrate_uniqueness()

    for rule in ["born_rule", "alternative_amplitude", "alternative_quartic"]:
        r = uniqueness[rule]
        name = rule.replace("_", " ").replace("alternative ", "")
        if "additivity" in r:
            a = r["additivity"]
            status = "PASS" if a["satisfies_additivity"] else "FAIL"
            print(f"\n  {name}: additivity [{status}]")
            print(f"    Violations: {a['violations']}/{a['tests']}")
            print(f"    Max violation: {a['max_violation']:.8f}")
        elif "problem" in r:
            print(f"\n  {name}: [{r['problem'][:80]}]")

    print(f"\n  {uniqueness['conclusion']}")

    # Part 3: Dimension-2 exception
    print("\n" + "-" * 60)
    print("  PART 3: WHY DIM ≥ 3 MATTERS")
    print("-" * 60)
    dim_check = gv.demonstrate_dim2_exception()

    d2 = dim_check["dim_2"]
    print(f"\n  Dim=2 (qubits):")
    print(f"    Dispersion-free measure works: {d2['dispersion_free_works']}")
    print(f"    Implication: {d2['implication']}")

    d3 = dim_check["dim_3"]
    print(f"\n  Dim=3+ (Brahman field):")
    print(f"    Dispersion-free fails: {d3['dispersion_free_fails']}")
    print(f"    Failure rate: {d3['failure_rate']:.1%} ({d3['total_tests']} tests)")
    print(f"    Implication: {d3['implication'][:100]}...")

    # Part 4: The axiom reduction proof
    print("\n" + "-" * 60)
    print("  PART 4: AXIOM REDUCTION PROOF")
    print("-" * 60)
    proof = gv.axiom_reduction_proof()

    print(f"\n  Proof chain:")
    for step in proof["proof_chain"]:
        print(f"    {step}")

    ac = proof["axiom_counts"]
    print(f"\n  Axiom counts:")
    print(f"    Copenhagen:          {ac['copenhagen']} axioms (Born rule is axiom A5)")
    print(f"    Advaita (stated):    {ac['advaita_stated']} axioms (A5 references Gleason)")
    print(f"    Advaita (independent): {ac['advaita_independent']} axioms (Born rule is theorem)")
    print(f"    Reduction: {ac['reduction']}")

    print(f"\n  CONCLUSION: {proof['conclusion']}")

    print(f"\n  SIGNIFICANCE:")
    print(f"  This is not a philosophical argument — it is a mathematical proof.")
    print(f"  Gleason's theorem (1957) is a proven theorem of mathematics.")
    print(f"  The verification that Brahman's Hilbert space satisfies its")
    print(f"  conditions is computational verification of mathematical facts.")
    print(f"  The axiom reduction from 7 to 4 is a concrete, rigorous result.")

    return {"status": "completed", "experiment": "gleason_theorem"}


def tensor_network_experiment():
    """Experiment 19: MERA Tensor Network — entanglement structure, computed."""
    print("\n" + "=" * 70)
    print("  EXPERIMENT 19: MERA TENSOR NETWORK")
    print("  Entanglement Structure of a Real MERA State")
    print("=" * 70)
    print("\n  Reimplemented 2026-08-15: the previous version applied its")
    print("  tensors as a global phase (a physical no-op) and its results were")
    print("  retracted. This version contracts real disentanglers/isometries")
    print("  into an explicit 16-site state and measures that state.")

    from quantum.tensor_network import MERATensorNetwork

    mera = MERATensorNetwork(num_sites=16, bond_dim=2)
    demo = mera.full_demonstration()

    # Part 1: the tensors are genuine
    print("\n" + "-" * 60)
    print("  PART 1: TENSOR ALGEBRA (are the tensors real?)")
    print("-" * 60)
    ta = demo["tensor_algebra"]
    print(f"  Disentanglers: {ta['num_disentanglers']}  max |U'U - I| = {ta['max_unitarity_deviation']:.2e}")
    print(f"  Isometries:    {ta['num_isometries']}  max |W'W - I| = {ta['max_isometry_deviation']:.2e}")
    print(f"  All within 1e-10: {ta['all_within_1e-10']}")

    # Part 2: the old defect, inverted into a control
    print("\n" + "-" * 60)
    print("  PART 2: NEGATIVE CONTROL (tensors must affect the state)")
    print("-" * 60)
    pe = demo["perturbation_example"]
    print(f"  Perturbing layer {pe['layer']} ({pe['mode']}):")
    print(f"    ||delta psi||              = {pe['delta_norm']:.4f}")
    print(f"    phase-invariant distance = {pe['phase_invariant_distance']:.4f}")
    print(f"    state actually changed   = {pe['state_changed']}")
    print("  (The retired implementation scored 0 here — that was the defect.)")

    # Part 3: RT-type entropy bound, measured on the state
    print("\n" + "-" * 60)
    print("  PART 3: ENTROPY vs MINIMAL CUT (computed on the real state)")
    print("-" * 60)
    for iv in demo["rt_bound"]["intervals"]:
        label = f"[{iv['start']}, {iv['start'] + iv['length']})"
        print(f"    interval {label:10s} S = {iv['entropy']:.4f}  <=  "
              f"ln(chi)*cut = {iv['bound']:.4f}  "
              f"(cut={iv['min_cut_bonds']} bonds, "
              f"saturation {iv['saturation_ratio']:.3f})")
    print(f"  All bounds hold: {demo['rt_bound']['all_bounds_hold']}")
    print(f"  Claim scope: {demo['rt_bound']['computed_claim'][:150]}")

    # Part 4: disconnection as entanglement is switched off
    print("\n" + "-" * 60)
    print("  PART 4: REMOVE ENTANGLEMENT -> LOSE CONNECTIVITY")
    print("-" * 60)
    dc = demo["disconnection"]
    for lam, I, dist in zip(dc["lambdas"], dc["mutual_information"], dc["derived_distance"]):
        d_str = "inf" if dist == float("inf") else f"{dist:.4f}"
        print(f"    lambda={lam:.2f}:  I(L:R) = {I:.6f}   derived distance = {d_str}")
    print(f"  Monotone decreasing on this grid: {dc['monotone_decreasing']}")
    print(f"  I -> 0 at lambda=0: {dc['final_below_1e-8']}")

    print(f"\n  {demo['interpretation'][:200]}")

    return {"status": "completed", "experiment": "tensor_network"}


def einstein_2d_experiment():
    """Experiment 20: discrete geometry + entanglement thermodynamics (Track D).

    Restructured 2026-08-15: the genuine computations (Gauss-Bonnet, the first
    law of entanglement, mutual-information geometry) lead; the legacy
    "2+1D Einstein equations from consciousness" correlation is kept at the
    end, labelled as withdrawn.
    """
    print("\n" + "=" * 70)
    print("  EXPERIMENT 20: DISCRETE GEOMETRY AND ENTANGLEMENT THERMODYNAMICS")
    print("  What is actually computable — plus one withdrawn legacy claim")
    print("=" * 70)
    print("\n  Restructured 2026-08-15. The former headline — 'Einstein's")
    print("  equations recovered on a 2D discrete manifold from consciousness")
    print("  thermodynamics' — is WITHDRAWN twice over: the entropy field was")
    print("  DEFINED from T_00, so the R-T correlation measured its own")
    print("  definition; and in 2D the Einstein tensor vanishes identically,")
    print("  so there is no 2D Einstein equation to recover. The computations")
    print("  that DO hold come first.")

    from gravity.einstein_2d import EmergentEinstein2D
    from gravity.entanglement_first_law import EntanglementFirstLaw
    from gravity.entanglement_geometry import EntanglementGeometry

    ee = EmergentEinstein2D(num_points=80, seed=42)

    # ---------------------------------------------------------------
    # Part 1 (D1): discrete Gauss-Bonnet — real geometry, with control
    # ---------------------------------------------------------------
    print("\n" + "-" * 60)
    print("  PART 1: DISCRETE GAUSS-BONNET (computed geometry)")
    print("-" * 60)
    gb = ee.gauss_bonnet_check()
    print(f"  Delaunay mesh: V = {gb['num_vertices']}, E = {gb['num_edges']}, "
          f"F = {gb['num_triangles']} ({gb['num_boundary_edges']} boundary edges)")
    print(f"    sum of interior angle deficits:  {gb['sum_interior_deficits']:.3e}")
    print(f"    sum of boundary exterior angles: {gb['sum_boundary_exterior_angles']:.10f}")
    print(f"    Gauss-Bonnet total:              {gb['gauss_bonnet_total']:.10f}")
    chi_label = f"2*pi*chi (chi = V-E+F = {gb['euler_characteristic']}):"
    print(f"    {chi_label:<33}{gb['expected_2_pi_chi']:.10f}")
    print(f"    residual:                        {gb['residual']:.2e}   "
          f"(holds to 1e-9: {gb['passes']})")

    tc = ee.gauss_bonnet_topology_control()
    print(f"\n  NEGATIVE CONTROL — delete interior triangle "
          f"{tc['removed_triangle']} to puncture the disk:")
    print(f"    chi: {tc['disk']['euler_characteristic']} -> "
          f"{tc['punctured']['euler_characteristic']}   "
          f"Gauss-Bonnet sum shifts by {tc['total_shift']:.6f}")
    print(f"    shift equals 2*pi*delta_chi: {tc['shift_matches_2_pi_delta_chi']}   "
          f"identity still holds on the punctured mesh: {tc['punctured']['passes']}")
    print(f"    control passes: {tc['control_passes']}")
    print(f"\n  {gb['note']}")

    # ---------------------------------------------------------------
    # Part 2 (D2): first law of entanglement on a free-fermion chain
    # ---------------------------------------------------------------
    print("\n" + "-" * 60)
    print("  PART 2: FIRST LAW OF ENTANGLEMENT, delta S = delta <K_A>")
    print("-" * 60)
    fl = EntanglementFirstLaw().demonstrate_first_law()
    print(f"  Free-fermion chain: {fl['num_sites']} sites at half filling "
          f"({fl['num_filled']} fermions), region A = "
          f"[{fl['region'][0]}, {fl['region'][1]}), S(A) = {fl['S_region']:.4f}")
    print(f"  Perturbation: bond modulation t_i = 1 + eps*cos(2*pi*i/N)")
    print(f"    {'eps':>10}  {'|dS - d<K_A>|':>15}  {'wrong-K control':>16}")
    for eps, m, mw in zip(fl["epsilons"], fl["mismatch"], fl["mismatch_wrong_K"]):
        print(f"    {eps:10.3e}  {m:15.3e}  {mw:16.3e}")
    print(f"  log-log slope: {fl['loglog_slope']:.4f} "
          f"(first law predicts 2) — within 2 +/- 0.2: "
          f"{fl['slope_within_2_pm_0.2']}")
    print(f"  at eps = {fl['eps_small']:.0e}: mismatch = "
          f"{fl['mismatch_at_eps_small']:.3e}  (below 1e-6: "
          f"{fl['small_eps_below_1e-6']})")
    print(f"  relative-entropy positivity (deficit >= 0 at every eps): "
          f"{fl['relative_entropy_nonnegative']}")
    ratio = (fl["wrong_mismatch_at_eps_small"]
             / max(fl["mismatch_at_eps_small"], 1e-300))
    print(f"  NEGATIVE CONTROL — wrong modular Hamiltonian (h_A instead of k):")
    print(f"    slope {fl['loglog_slope_wrong_K']:.4f} (i.e. O(eps): first-order "
          f"equality broken), mismatch {ratio:.0f}x larger at eps = "
          f"{fl['eps_small']:.0e}")
    print(f"    first-order agreement genuinely lost: "
          f"{fl['wrong_K_breaks_first_order']}")
    print(f"  first law holds: {fl['first_law_holds']}")
    print(f"\n  {fl['interpretation']}")

    # ---------------------------------------------------------------
    # Part 3 (D3): mutual-information geometry of an exact TFIM state
    # ---------------------------------------------------------------
    print("\n" + "-" * 60)
    print("  PART 3: MUTUAL-INFORMATION GEOMETRY (exact TFIM ground state)")
    print("-" * 60)
    eg = EntanglementGeometry()
    geo = eg.demonstrate_entanglement_geometry()
    crit = geo["critical"]
    para = geo["paramagnet"]
    deep = geo["paramagnet_deeper_supplementary"]
    shuf = geo["shuffle_control"]
    print(f"  TFIM chain, N = {geo['num_spins']} spins, dense ED "
          f"(dim {2 ** geo['num_spins']})")
    print(f"  At criticality (g = J = {crit['g']:.1f}):")
    print(f"    Spearman rho(|i-j|, I) = {crit['spearman_rho_sep_vs_I']:.4f}   "
          f"(monotone decay, criterion < -0.9: {crit['monotone_decay']})")
    print(f"    max I = {crit['max_I']:.4f}; mean I by separation: "
          + ", ".join(f"{v:.4f}" for v in crit["mean_I_by_separation"][:5]) + ", ...")
    print(f"  Deep in the paramagnet (g = {para['g']:.1f}, the frozen point):")
    print(f"    max I = {para['max_I']:.3e} against the frozen threshold "
          f"{para['near_product_threshold']:.0e} -> near-product: "
          f"{para['near_product']}")
    print(f"    that criterion FAILED and is recorded, not moved; the "
          f"supplementary point g = {deep['g']:.0f} gives max I = "
          f"{deep['max_I']:.3e} -> {deep['near_product']}")
    print(f"  NEGATIVE CONTROL — shuffle I across pairs: rho = "
          f"{shuf['spearman_rho_shuffled']:.4f}, monotonicity destroyed: "
          f"{shuf['monotonicity_destroyed']}")
    print(f"\n  {geo['interpretation']}")

    # ---------------------------------------------------------------
    # Part 4: the legacy construction, retained and labelled
    # ---------------------------------------------------------------
    print("\n" + "-" * 60)
    print("  PART 4: LEGACY R-T CORRELATION — WITHDRAWN, NOT EVIDENCE")
    print("-" * 60)
    result = ee.derive_einstein_equations()
    et = result["einstein_equation_test"]
    print(f"  Manifold: {result['num_points']} points, "
          f"{result['num_triangles']} triangles")
    print(f"    R_entropy vs T_00 correlation:   "
          f"{et['R_entropy_T_correlation']:.4f}")
    print(f"    R_geometric vs T_00 correlation: "
          f"{et['R_geometric_T_correlation']:.4f}")
    print(f"    Effective G:                     {et['effective_G']:.6f}")
    print(f"    STATUS: WITHDRAWN as evidence (2026-08-15). The entropy field")
    print(f"            S is DEFINED from T_00, so correlating a smoothed copy")
    print(f"            of S against T_00 tests the definition, not a field")
    print(f"            equation. The pass/fail flag this used to print is")
    print(f"            deliberately suppressed: it was never a verdict on")
    print(f"            physics. Threshold used to be |r| > "
          f"{et['correlation_threshold']}.")
    print(f"  (The legacy mass-curves comparison is no longer printed here —")
    print(f"   its summary text claimed Einstein's insight had been derived.")
    print(f"   The method remains in gravity/einstein_2d.py, under test.)")
    print(f"\n  {result['improvement_over_1d']}")

    return {"status": "completed",
            "experiment": "discrete_geometry_and_entanglement_thermodynamics"}


def error_correction_experiment():
    """Experiment 21: the [[5,1,3]] code — real stabilizer error correction."""
    print("\n" + "=" * 70)
    print("  EXPERIMENT 21: QUANTUM ERROR CORRECTION AS SPACETIME")
    print("  The [[5,1,3]] Perfect Code, Actually Implemented")
    print("=" * 70)
    print("\n  Reimplemented 2026-08-15. The previous 'Brahman recoverable with")
    print("  80% boundary erasure' claim was withdrawn: 80% erasure recovery is")
    print("  impossible (no-cloning). Honest figures: erasure threshold 2/5")
    print("  (40%), reconstruction from any 3/5 (60%) of the boundary.")

    from quantum.error_correction import HolographicCode

    code = HolographicCode()
    a = code.run_full_analysis()

    print("\n" + "-" * 60)
    print("  PART 1: IS IT REALLY A CODE? (A1)")
    print("-" * 60)
    st = a["A1_stabilizer_eigenstates"]
    print(f"  Encoded states are +1 eigenstates of all 4 stabilizers:")
    print(f"    max |<S_i> - 1| = {st['max_eigenvalue_deviation']:.2e}   "
          f"passes: {st['all_plus_one_eigenstates']}")

    print("\n" + "-" * 60)
    print("  PART 2: SINGLE-QUBIT ERROR CORRECTION — all 15 Paulis (A2)")
    print("-" * 60)
    se = a["A2_single_qubit_errors"]
    print(f"  Cases: {se['n_cases']}   worst post-correction fidelity: "
          f"{se['min_fidelity']:.12f}")
    print(f"  All corrected: {se['all_corrected']}   "
          f"16 distinct syndromes: {se['syndromes_all_distinct']}")

    print("\n" + "-" * 60)
    print("  PART 3: ERASURE — WHAT IS, AND IS NOT, RECOVERABLE (A3, A4)")
    print("-" * 60)
    er = a["A3_two_erasure"]
    print(f"  2-erasure: {er['n_patterns']} patterns, {er['n_cases']} cases, "
          f"worst fidelity {er['min_fidelity']:.12f}  -> recovered: {er['all_recovered']}")
    nc = a["A4_three_erasure_negative_control"]
    print(f"  NEGATIVE CONTROL, 3 erasures ({nc['n_patterns']} patterns):")
    print(f"    max trace distance between logical states on the survivors = "
          f"{nc['max_trace_distance_on_survivors']:.2e}")
    print(f"    information genuinely absent: {nc['information_absent']}")
    print(f"    (This is no-cloning enforcing itself — the old '80%' claim was")
    print(f"     not merely unsupported, it was impossible.)")
    th = a["erasure_threshold"]
    print(f"  Computed threshold: {th['threshold_qubits']} of 5 "
          f"({th['threshold_fraction']:.0%})")

    print("\n" + "-" * 60)
    print("  PART 4: SUBREGION RECONSTRUCTION — any 3 of 5 (A5)")
    print("-" * 60)
    sr = a["A5_subregion_reconstruction"]
    print(f"  {sr['n_subsets']} three-qubit subsets, min trace distance "
          f"{sr['min_trace_distance']:.12f}")
    print(f"  Every 3-of-5 subregion reconstructs the logical qubit: "
          f"{sr['all_reconstructable']}")

    print(f"\n  HEADLINE: {a['headline']}")

    return {"status": "completed", "experiment": "error_correction"}


def fine_structure_v2_experiment():
    """Experiment 22: Fine Structure Constant — Systematic Derivation."""
    print("\n" + "=" * 70)
    print("  EXPERIMENT 22: FINE STRUCTURE CONSTANT — SYSTEMATIC DERIVATION")
    print("  Target: 1/α = 137.035999084")
    print("=" * 70)

    from numerology.fine_structure_v2 import FineStructureV2

    fs = FineStructureV2()
    results = fs.run_all_approaches()

    # Show ranking of all approaches
    print("\n" + "-" * 60)
    print("  RANKING OF ALL APPROACHES (by accuracy)")
    print("-" * 60)
    print(f"\n  {'Rank':<5} {'Method':<40} {'1/α':<12} {'Error %':<10}")
    print(f"  {'-'*5} {'-'*40} {'-'*12} {'-'*10}")
    for i, r in enumerate(results["ranking"]):
        marker = " ←BEST" if i == 0 else ""
        print(f"  {i+1:<5} {r['method']:<40} {r['alpha_inv']:<12.4f} {r['error']:<10.2f}{marker}")

    print(f"\n  Target: 1/α = {results['target']}")

    # Highlight best result
    best = results["best_result"]
    print(f"\n  BEST RESULT: {best['method']}")
    print(f"    1/α = {best['alpha_inv']:.6f}")
    print(f"    Error: {best['error']:.2f}%")
    print(f"    Previous best: {results['previous_best_error']:.2f}%")

    # Continued fraction analysis
    print("\n" + "-" * 60)
    print("  CONTINUED FRACTION STRUCTURE OF 1/α")
    print("-" * 60)
    cf = results["approaches"]["continued_fraction"]
    print(f"\n  1/α = [{cf['continued_fraction_terms'][0]}; "
          f"{', '.join(str(t) for t in cf['continued_fraction_terms'][1:8])}...]")
    print(f"\n  Convergents:")
    for c in cf["convergents"][:6]:
        print(f"    {c['p/q']:>15s} = {c['value']:.6f}  (error: {c['error_percent']:.4f}%)")

    # 163 connection
    print("\n" + "-" * 60)
    print("  THE 163 CONNECTION (Heegner numbers)")
    print("-" * 60)
    mod = results["approaches"]["modular"]
    print(f"\n  {mod['163_connection'][:300]}...")

    print(f"\n  {results['improvement']}")
    print(f"\n  {results['honest_assessment'][:200]}...")

    return {"status": "completed", "experiment": "fine_structure_v2"}


def iit_bridge_experiment():
    """Experiment 23: IIT-Entanglement Bridge — Consciousness Meets Quantum."""
    print("\n" + "=" * 70)
    print("  EXPERIMENT 23: IIT-ENTANGLEMENT BRIDGE")
    print("  Conjecture tested: Φ (Consciousness) ≤ S (Entanglement)")
    print("=" * 70)
    print("\n  " + "!" * 66)
    print("  !! STATUS: FALSIFIED (2026-07-15; ordering audit 2026-08-12).")
    print("  !! The validated PyPhi retest (N=216) refutes the bound: 50 of the")
    print("  !! 51 nonzero-Phi systems VIOLATE Phi <= S; the raw correlation is")
    print("  !! a connectivity confound (partial r ~ -0.07, p = 0.29).")
    print("  !! What runs below is the ORIGINAL, CIRCULAR internal-heuristic")
    print("  !! construction, retained for historical reproducibility only.")
    print("  !! See predictions/validated_phi.py and reproducibility/phi_s/.")
    print("  " + "!" * 66)

    from predictions.iit_bridge import IITEntanglementBridge

    bridge = IITEntanglementBridge(num_nodes=4)

    # Part 1: Test the conjecture
    print("\n" + "-" * 60)
    print("  PART 1: CONJECTURE TEST (50 random systems)")
    print("-" * 60)
    conj = bridge.test_conjecture(num_trials=50)
    print(f"\n  Conjecture: {conj['conjecture']}")
    print(f"  Holds in: {conj['conjecture_holds_rate']:.0%} of trials")
    print(f"  Violations: {conj['violations']}/{conj['num_trials']}")
    print(f"  Average Φ: {conj['avg_phi']:.6f}")
    print(f"  Average S: {conj['avg_S_entanglement']:.6f}")
    print(f"  Φ-S correlation: {conj['phi_S_correlation']:.4f}")
    print(f"  Average Φ/S ratio: {conj['avg_ratio_phi_over_S']:.4f}")
    print(f"\n  {conj['result']}")

    # Part 2: Extreme cases
    print("\n" + "-" * 60)
    print("  PART 2: EXTREME CASES")
    print("-" * 60)
    extremes = bridge.demonstrate_extremes()
    for key in ["disconnected", "half_connected", "fully_connected"]:
        e = extremes[key]
        status = "HOLDS" if e["conjecture"] else "VIOLATED"
        print(f"\n  {key}:")
        print(f"    Φ = {e['phi']:.6f}, S = {e['S']:.6f}, Φ ≤ S: {status}")
        print(f"    {e['label']}")

    # Part 3: MERA consciousness profile
    print("\n" + "-" * 60)
    print("  PART 3: CONSCIOUSNESS PROFILE ACROSS MERA LAYERS")
    print("-" * 60)
    mera = bridge.mera_consciousness_profile()
    for layer in mera["layers"]:
        bar = "#" * int(layer["phi"] * 50) if layer["phi"] > 0 else ""
        print(f"  Depth {layer['depth']}: Φ={layer['phi']:.4f} "
              f"[{bar:25s}] {layer['label']}")
    print(f"\n  Φ increases toward IR (Brahman): {mera['phi_increases_toward_ir']}")
    print(f"\n  {mera['prediction'][:200]}...")

    # Implications once drawn from the (now falsified) conjecture
    print("\n" + "-" * 60)
    print("  PART 4: IMPLICATIONS ONCE DRAWN (HISTORICAL — CONJECTURE FALSIFIED)")
    print("-" * 60)
    demo = bridge.full_demonstration()
    preds = demo["testable_prediction"].split(". ")
    for i, pred in enumerate(preds):
        if pred.strip():
            print(f"  {i+1}. {pred.strip()}")
    print("\n  The validated retest falsified the bound, so these implications")
    print("  no longer follow. They are shown to keep the historical record")
    print("  reproducible.")

    return {"status": "completed", "experiment": "iit_bridge",
            "conjecture_status": "falsified (validated PyPhi retest; "
                                 "ordering audit 2026-08-12)"}


def operational_equivalence_experiment():
    """Experiment 24: Everett-Advaita Operational Equivalence."""
    print("\n" + "=" * 70)
    print("  EXPERIMENT 24: EVERETT-ADVAITA OPERATIONAL EQUIVALENCE")
    print("  The shared calculation — equivalence is ANALYTIC, not tested")
    print("=" * 70)

    from quantum.operational_equivalence import OperationalEquivalence

    oe = OperationalEquivalence(dimension=4)
    results = oe.full_report()

    print("\n  " + "-" * 66)
    print("  WHAT THIS EXPERIMENT DOES NOT DO")
    print("  " + "-" * 66)
    print("  It does not compare two interpretations, because there is only one")
    print("  calculation. Both readings use the same Hilbert space, the same")
    print("  unitary dynamics, the same Born rule and the same decoherence, so")
    print("  identical predictions follow by construction and no computation")
    print("  could show otherwise. Until 2026-08-16 this module claimed to PROVE")
    print("  the equivalence by copying one array twice and reporting that the")
    print("  copies matched; that scoreboard has been deleted.")

    print("\n  " + "-" * 66)
    print("  THE SHARED QUANTITIES (each computed once)")
    print("  " + "-" * 66)
    for key, r in results["shared_quantities"].items():
        print(f"\n  {r['quantity']}")
        print(f"    {r['note'][:150]}")

    div = results["divergences"]
    print("\n  " + "-" * 66)
    print("  ONTOLOGICAL DIVERGENCES (hand-written catalogue; none measurable)")
    print("  " + "-" * 66)
    for key, val in div["divergences"].items():
        print(f"    {key}:")
        print(f"      Everett: {val['everett'][:80]}")
        print(f"      Advaita: {val['advaita'][:80]}")
        print(f"      Measurable? {val['measurable_difference']}")
    print("\n  (Not counted: the number of rows reflects how the table was")
    print("   written, not a fact about the interpretations.)")

    print(f"\n  STATUS: {results['equivalence_status']}")

    return {"status": "completed", "experiment": "operational_equivalence"}


def perspectival_asymmetry_experiment():
    """Experiment 25: Perspectival Asymmetry — Generalized."""
    print("\n" + "=" * 70)
    print("  EXPERIMENT 25: PERSPECTIVAL ASYMMETRY (Generalized)")
    print("  Total State Pure, Reduced State Mixed — For ALL Cases")
    print("=" * 70)

    from quantum.perspectival_asymmetry import PerspectivalAsymmetry

    pa = PerspectivalAsymmetry()
    results = pa.full_test()

    # Varying states
    vs = results["varying_states"]
    print(f"\n  Test 1: Varying initial states ({vs['num_states']} states)")
    for r in vs["results"][:5]:  # Show first 5
        print(f"    {r['state']:20s}: total={r['total_purity']:.6f}  "
              f"reduced={r['reduced_purity']:.6f}  holds={r['perspectival_holds']}")
    if vs["num_states"] > 5:
        remaining = sum(1 for r in vs["results"][5:] if r["perspectival_holds"])
        print(f"    ... and {remaining}/{vs['num_states']-5} more hold")
    print(f"  All hold: {vs['all_hold']}")

    # Varying environment
    ve = results["varying_environment"]
    print(f"\n  Test 2: Varying environment size")
    for r in ve["results"]:
        print(f"    env_dim={r['env_dim']:3d}: total={r['total_purity']:.6f}  "
              f"reduced={r['reduced_purity']:.6f}  coherence={r['coherence']:.6f}")
    print(f"  All total pure: {ve['all_total_pure']}")

    # Varying basis
    vb = results["varying_basis"]
    print(f"\n  Test 3: Varying measurement basis ({vb['num_bases']} bases)")
    print(f"  All total pure: {vb['all_total_pure']}")
    print(f"  All reduced mixed: {vb['all_reduced_mixed']}")

    # Exactness
    ex = results["exactness"]
    print(f"\n  Test 4: Exactness ({ex['num_random_states']} random states)")
    print(f"  Max deviation from purity 1.0: {ex['max_deviation_from_purity_1']:.2e}")
    print(f"  Is exact: {ex['is_exact']}")

    # Summary
    s = results["summary"]
    print(f"\n  SUMMARY: All perspectival: {s['all_perspectival']}")
    print(f"  {s['conclusion'][:200]}")

    return {"status": "completed", "experiment": "perspectival_asymmetry"}


def observer_centrality_experiment():
    """Experiment 26: Observer Centrality — The Hidden Premise."""
    print("\n" + "=" * 70)
    print("  EXPERIMENT 26: OBSERVER CENTRALITY")
    print("  Why Observer Ontology Is Part of the Interpretive Burden")
    print("=" * 70)

    from quantum.observer_centrality import ObserverCentrality

    oc = ObserverCentrality()
    results = oc.full_demonstration()

    # Step 1
    s1 = results["step_1"]
    print(f"\n  STEP 1: {s1['description']}")
    print(f"    Pointer states: {s1['pointer_states']}")
    print(f"    Reduced state diagonal: {[f'{d:.4f}' for d in s1['reduced_state_diagonal']]}")
    print(f"    Off-diagonal coherence: {s1['off_diagonal_coherence']:.10f}")
    print(f"    {s1['what_physics_gives_us'][:120]}")

    # Step 2
    s2 = results["step_2"]
    print(f"\n  STEP 2: {s2['description']}")
    print(f"    P(↑) = {s2['P_up']:.4f}, P(↓) = {s2['P_down']:.4f}")
    print(f"    Which outcome experienced? {s2['which_outcome_experienced']}")
    print(f"    THE GAP: {s2['the_gap'][:150]}...")

    # Step 3
    s3 = results["step_3"]
    print(f"\n  STEP 3: {s3['description']}")
    for name, interp in s3["interpretations"].items():
        analyzed = "YES" if interp["observer_analyzed"] else "NO"
        print(f"    {name:12s}: observer analyzed = {analyzed}")
        print(f"      {interp['mechanism'][:80]}")
    print(f"    {s3['key_finding'][:150]}...")

    # Step 4
    s4 = results["step_4"]
    print(f"\n  STEP 4: {s4['description']}")
    print(f"    Formalism determines: {s4['num_determined']} things")
    print(f"    Formalism leaves open: {s4['num_open']} things")
    for item in s4["formalism_leaves_open"]:
        print(f"      - {item}")
    print(f"\n    {s4['the_argument'][:200]}...")

    # Summary
    sm = results["summary"]
    print(f"\n  ARGUMENT CHAIN:")
    for step in sm["argument_chain"]:
        print(f"    {step}")
    print(f"\n  {sm['conclusion'][:200]}...")

    return {"status": "completed", "experiment": "observer_centrality"}


def einstein_3d_experiment():
    """Experiment 27: 3+1D Einstein Equations from Consciousness."""
    print("\n" + "=" * 70)
    print("  EXPERIMENT 27: 3+1D EINSTEIN EQUATIONS")
    print("  Jacobson's Thermodynamic Derivation in Full Spacetime")
    print("=" * 70)

    from gravity.einstein_3d import EmergentEinstein3D

    ee = EmergentEinstein3D(num_points=80, seed=42)

    # Part 1: Full 3+1D Einstein derivation
    print("\n" + "-" * 60)
    print("  PART 1: JACOBSON DERIVATION (3D discrete manifold)")
    print("-" * 60)
    result = ee.derive_einstein_equations()

    print(f"\n  Manifold: {result['num_points']} points, {result['num_tetrahedra']} tetrahedra")
    print(f"  Dimensions: {result['dimensions']}")
    print(f"  Total energy: {result['energy_momentum']['total_energy']:.4f}")
    print(f"  Total entropy: {result['entropy_field']['total_entropy']:.4f}")

    et = result["einstein_equation_test"]
    print(f"\n  LEGACY R-T CORRELATION — WITHDRAWN, NOT EVIDENCE:")
    print(f"    R_entropy vs T_00 correlation:   {et['R_entropy_T_correlation']:.4f}")
    print(f"    R_geometric vs T_00 correlation:  {et['R_geometric_T_correlation']:.4f}")
    print(f"    Effective G:                      {et['effective_G']:.6f}")
    print(f"    STATUS: {et['status']}")
    print(f"    (The pass/fail flag this used to print is deliberately")
    print(f"     suppressed — the entropy field is DEFINED from T_00, so")
    print(f"     the correlation tests its own definition, not a field")
    print(f"     equation. Threshold was |r| > {et['correlation_threshold']}.)")

    print(f"\n  {result['status_note']}")

    print(f"\n  Legacy derivation steps (annotated):")
    for step in result["legacy_steps_annotated"]:
        print(f"    {step}")

    # Part 2: Mass curves 3D space
    print("\n" + "-" * 60)
    print("  PART 2: MASS CURVES 3D SPACE")
    print("-" * 60)
    curves = ee.demonstrate_mass_curves_3d_space()
    for case in ["empty_space", "single_mass", "binary_system", "mass_shell"]:
        data = curves[case]
        print(f"\n  {case}:")
        print(f"    Energy: {data['total_energy']:.4f}")
        print(f"    R-T correlation: {data['R_T_correlation']:.4f}")
        print(f"    {data['interpretation']}")

    # Part 3: Gravitational wave signature
    print("\n" + "-" * 60)
    print("  PART 3: GRAVITATIONAL WAVE SIGNATURE")
    print("-" * 60)
    gw = ee.gravitational_wave_signature()
    print(f"\n  Wave amplitude: {gw['wave_amplitude']:.6f}")
    print(f"  Points affected: {gw['points_affected']}/{gw['total_points']}")
    print(f"  Near-field: {gw['near_field_amplitude']:.6f}")
    print(f"  Far-field: {gw['far_field_amplitude']:.6f}")
    # The module returns `propagates_means` and `status` precisely so these
    # two legacy booleans are not read as physics. Print those, not the bare
    # flags -- the Part-1 suppression landed in the 2026-08-16 pass and this
    # one was missed.
    print(f"  Nonzero beyond median radius: {gw['propagates']}  "
          f"(near > far: {gw['falls_off_with_distance']})")
    print(f"  What that means: {gw['propagates_means']}")
    print(f"  STATUS: {gw['status']}")

    return {"status": "completed", "experiment": 27}


def er_epr_experiment():
    """Experiment 28: ER=EPR — Wormholes Are Entanglement."""
    print("\n" + "=" * 70)
    print("  EXPERIMENT 28: ER=EPR CORRESPONDENCE")
    print("  Wormholes = Entanglement = Non-Duality")
    print("=" * 70)

    from quantum.er_epr import EREqualsEPR

    er = EREqualsEPR(dimension=4, num_sites=8)

    # Part 1: Thermofield double
    print("\n" + "-" * 60)
    print("  PART 1: THERMOFIELD DOUBLE STATE = ETERNAL BLACK HOLE")
    print("-" * 60)
    for beta, label in [(0.1, "hot"), (1.0, "medium"), (5.0, "cold")]:
        tfd = er.thermofield_double(beta)
        print(f"\n  β = {beta} ({label}):")
        print(f"    Total state pure: {tfd['total_state_pure']}")
        print(f"    Entanglement entropy: {tfd['entanglement_entropy']:.4f}")
        print(f"    Entanglement fraction: {tfd['entanglement_fraction']:.4f}")
        print(f"    S_entanglement = S_thermal: {tfd['er_epr_identity']}")

    # Part 2: Wormhole geometry from entanglement
    print("\n" + "-" * 60)
    print("  PART 2: WORMHOLE THROAT FROM ENTANGLEMENT")
    print("-" * 60)
    for strength in [0.0, 0.5, 1.0]:
        wh = er.wormhole_from_entanglement(strength)
        print(f"\n  Entanglement strength: {strength}")
        print(f"    Entropy: {wh['entanglement_entropy']:.4f}")
        print(f"    Throat area: {wh['wormhole_throat_area']:.4f}")
        print(f"    Connected: {wh['wormhole_exists']}")

    # Part 3: Cutting entanglement disconnects space
    print("\n" + "-" * 60)
    print("  PART 3: VAN RAAMSDONK — SPACE FROM ENTANGLEMENT")
    print("-" * 60)
    van = er.cutting_entanglement_destroys_geometry()
    print(f"\n  Connected at zero entanglement: {van['connected_at_zero']}")
    print(f"  Connected at max entanglement: {van['connected_at_max']}")
    print(f"  {van['phase_transition']}")

    # Part 4: Non-traversability
    print("\n" + "-" * 60)
    print("  PART 4: NON-TRAVERSABILITY FROM MONOGAMY")
    print("-" * 60)
    mono = er.non_traversability_from_monogamy()
    print(f"\n  Max A-B entanglement: {mono['max_entanglement_AB']:.4f}")
    print(f"  A in tripartite state: {mono['entanglement_A_in_tripartite']:.4f}")
    print(f"  Entanglement diluted: {mono['entanglement_diluted']}")
    print(f"  Non-traversable: {mono['non_traversable']}")

    print("\n  CONCLUSION: ER=EPR is EXHIBITED here, not confirmed. The")
    print("  throat-entropy relation is imposed by assignment in this demo")
    print("  rather than derived, so nothing above could have come out")
    print("  otherwise. Illustrative identities only.")
    return {"status": "completed", "experiment": 28}


def fine_structure_v3_experiment():
    """Experiment 29: Fine Structure Constant — Rigorous Derivation."""
    print("\n" + "=" * 70)
    print("  EXPERIMENT 29: FINE STRUCTURE CONSTANT — RIGOROUS DERIVATION")
    print("  Target: 1/α = 137.035999084")
    print("=" * 70)

    from numerology.fine_structure_v3 import FineStructureV3

    fs = FineStructureV3()
    results = fs.run_all_approaches()

    # Ranking
    print("\n" + "-" * 60)
    print("  RANKING OF ALL v3 APPROACHES (by accuracy)")
    print("-" * 60)
    print(f"\n  {'Rank':<5} {'Method':<45} {'1/α':<12} {'Error %':<10}")
    print(f"  {'-'*5} {'-'*45} {'-'*12} {'-'*10}")
    for i, r in enumerate(results["ranking"][:10]):
        marker = " ← BEST" if i == 0 else ""
        print(f"  {i+1:<5} {r['method']:<45} {r['alpha_inv']:<12.4f} {r['error_pct']:<10.4f}{marker}")

    # Continued fraction
    print("\n" + "-" * 60)
    print("  CONTINUED FRACTION ANALYSIS")
    print("-" * 60)
    cf = results["continued_fraction"]
    print(f"  1/α = [{', '.join(str(c) for c in cf['cf_coefficients'][:8])}...]")
    for conv in cf["convergents"][:5]:
        print(f"    {conv['p/q']:<15} = {conv['value']:<15.6f} (error: {conv['error_pct']:.6f}%)")

    # Best result
    best = results["best_result"]
    print(f"\n  BEST v3 RESULT: {best['method']}")
    print(f"    1/α = {best['alpha_inv']:.6f}")
    print(f"    Error: {best['error_pct']:.4f}%")
    print(f"    v2 best: 0.003%")

    print(f"\n  {results['honest_assessment']}")
    return {"status": "completed", "experiment": 29}


def unity_of_experience_experiment():
    """Experiment 30: Unity of Experience — Experiential Underdetermination."""
    print("\n" + "=" * 70)
    print("  EXPERIMENT 30: UNITY OF EXPERIENCE")
    print("  Paper claim: decoherence fixes rho_SA but not experiential ontology")
    print("=" * 70)

    from quantum.unity_of_experience import UnityOfExperience

    u = UnityOfExperience(n_outcomes=3, seed=42)
    result = u.run_all()

    main = result["main_result"]
    einsel = main["einselection"]
    print("\n  REDUCED STATE rho_SA (after tracing environment)")
    print("  " + "-" * 60)
    print(f"    Trace:              {main['rho_SA_trace']:.6f}")
    print(f"    Purity:             {main['rho_SA_purity']:.6f}  (mixed: purity < 1)")
    print(f"    Off-diagonal norm:  {einsel['off_diagonal_norm']:.2e}")
    print(f"    Diagonal in pointer basis: {einsel['is_diagonal_pointer_basis']}")
    print(f"    Rank:               {einsel['rank']}")

    print("\n  EXPERIENTIAL INTERPRETATIONS CONSISTENT WITH THE SAME rho_SA")
    print("  " + "-" * 60)
    print(f"    {'Interpretation':<50} {'N unified':<10}")
    print(f"    {'-'*50} {'-'*10}")
    for interp in main["interpretations"]:
        print(f"    {interp['name']:<50} {interp['n_unified_experiences']:<10}")

    print("\n  UNDERDETERMINATION RESULT")
    print("  " + "-" * 60)
    print(f"    Distinct cardinalities: {main['distinct_cardinalities_count']}")
    print(f"    Underdetermined:        {main['decoherence_underdetermines_experience']}")

    robust = result["robustness"]
    print(f"\n    Robustness sweep: {robust['success_count']}/{robust['trials']} trials")
    print(f"    Success rate:     {robust['success_rate']*100:.1f}%")

    print(f"\n  {main['conclusion']}")
    return {"status": "completed", "experiment": 30}


def look_elsewhere_experiment():
    """Experiment 31: Look-Elsewhere Effect — why the alpha 'derivation' is numerology.

    This is a self-critical teaching demo. The framework's celebrated result is
    1/alpha ~ 163 - 26 + pi/100 = 137.0314 (0.0033 % error). This experiment
    shows *how easily* a target of that precision is hit by a large family of
    equally simple formulas, so the reader can judge the claim for themselves.
    """
    print("\n" + "=" * 70)
    print("  EXPERIMENT 31: THE LOOK-ELSEWHERE EFFECT (numerology demonstrator)")
    print("  Question: how special is 1/alpha = 163 - 26 + pi/100 ?")
    print("=" * 70)

    from numerology.look_elsewhere import LookElsewhereAnalysis

    lea = LookElsewhereAnalysis()
    r = lea.full_report()

    print("\n  THE CLAIMED FORMULA")
    print("  " + "-" * 60)
    print(f"    Formula:          {r['claimed_formula']}")
    print(f"    Value:            {r['claimed_value']:.6f}")
    print(f"    Relative error:   {r['claimed_rel_error']*100:.4f} %")

    print("\n  THE LOOK-ELSEWHERE EFFECT")
    print("  " + "-" * 60)
    print(f"    Formulas in the same simple family: {r['family_size_corrections']:,}")
    print(f"    Family members matching 1/alpha at the claim's own precision:")
    print(f"      -> {r['n_formulas_matching_alpha_at_claim_precision']} distinct formulas")
    print(f"    Closest family value:  {r['closest_family_value_to_alpha']:.8f} "
          f"(error {r['closest_family_rel_error']*100:.6f} %)")
    print(f"    ...that is {r['claimed_rel_error']/r['closest_family_rel_error']:.0f}x "
          f"more accurate than the celebrated formula.")

    print("\n  HOW EASILY ANY TARGET IS HIT")
    print("  " + "-" * 60)
    print(f"    Coverage of the window 130-145 at 1e-4 tolerance: "
          f"{r['coverage_130_145_at_1e-4']*100:.1f} %")
    print(f"    Coverage of the broad range 0.1-2000 at 1e-4:      "
          f"{r['coverage_broad_at_1e-4']*100:.1f} %")
    print(f"    Fraction of 25 real physics constants hit at 1e-4: "
          f"{r['basket_fraction_hit_at_1e-4']*100:.0f} %")

    print("\n  CONCLUSION")
    print("  " + "-" * 60)
    print("    A formula family this rich hits essentially ANY target to this")
    print("    precision. Matching 1/alpha is therefore expected by chance, not")
    print("    evidence of a derivation. This is the look-elsewhere effect, and")
    print("    it is why the constants work lives in numerology/, not constants/.")
    return {"status": "completed", "experiment": 31}


def run_physics_experiments():
    """Run all physics extension experiments (9-31)."""
    print("\n" + "#" * 70)
    print("#" + " " * 68 + "#")
    print("#   PHYSICS EXTENSIONS — TOWARD A REAL THEORY OF EVERYTHING" + " " * 9 + "#")
    print("#" + " " * 68 + "#")
    print("#" * 70)

    experiments = [
        quantum_hilbert_experiment,
        measurement_problem_experiment,
        entanglement_nonduality_experiment,
        emergent_gravity_experiment,
        holographic_experiment,
        particle_zoo_experiment,
        constants_experiment,
        predictions_experiment,
        interpretations_experiment,
        gleason_experiment,
        tensor_network_experiment,
        einstein_2d_experiment,
        error_correction_experiment,
        fine_structure_v2_experiment,
        iit_bridge_experiment,
        operational_equivalence_experiment,
        perspectival_asymmetry_experiment,
        observer_centrality_experiment,
        einstein_3d_experiment,
        er_epr_experiment,
        fine_structure_v3_experiment,
        unity_of_experience_experiment,
        look_elsewhere_experiment,
    ]

    results = []
    for exp in experiments:
        Brahman.reset()
        try:
            result = exp()
            results.append(result)
        except Exception as e:
            print(f"\n  ERROR in {exp.__name__}: {e}")
            import traceback
            traceback.print_exc()
            results.append({"status": "error", "experiment": exp.__name__, "error": str(e)})

    print("\n" + "=" * 70)
    print("  ALL PHYSICS EXPERIMENTS COMPLETE")
    print("=" * 70)
    print(f"\n  Total: {len(results)}")
    print(f"  Successful: {sum(1 for r in results if r['status'] == 'completed')}")
    print(f"  Failed: {sum(1 for r in results if r['status'] == 'error')}")
    Brahman.reset()
    return results


def run_everything():
    """Run ALL experiments (1-26) and generate visualizations."""
    run_all_experiments()
    Brahman.reset()
    run_physics_experiments()
    Brahman.reset()
    generate_visualizations()


def quick_demo():
    """A quick demonstration of the core concepts."""
    print("\n" + "=" * 60)
    print("  ADVAITA VEDANTA — QUICK DEMO")
    print("=" * 60)

    # 1. Brahman
    print("\n--- 1. BRAHMAN: The Singular Reality ---")
    Brahman.reset()
    brahman = Brahman()
    print(f"  {brahman}")
    sca = SatChitAnanda(brahman)
    print(f"  {sca}")

    # 2. Awareness is self-referential
    print("\n--- 2. SELF-REFERENCE: Awareness Aware of Itself ---")
    awareness = brahman.awareness()
    print(f"  brahman.awareness() is brahman: {awareness is brahman}")
    print(f"  (The strange loop at the heart of existence)")

    # 3. Superimposition
    print("\n--- 3. ADHYASA: Superimposition ---")
    adhyasa = Adhyasa()
    rope = Brahman().field
    result = adhyasa.superimpose(rope, ignorance_level=0.9, pattern_name="snake")
    print(f"  Substrate: Brahman field")
    print(f"  Ignorance: 90%")
    print(f"  Sees: {result.projection_pattern}")
    print(f"  Is the appearance real? {result.is_real}")

    # 4. Nama-Rupa
    print("\n--- 4. NAMA-RUPA: Names and Forms ---")
    nr = NamaRupa()
    entities = nr.differentiate(
        brahman.field,
        num_entities=4,
        names=["electron", "star", "thought", "love"],
    )
    for e in entities:
        print(f"  '{e.nama}' — appears separate? Yes. Actually separate? {e.is_separate}")
    source = nr.reunify(entities)
    print(f"  All reunified to same source: {source is brahman.field}")

    # 5. Three Levels
    print("\n--- 5. THREE LEVELS OF REALITY ---")
    engine = RealityEngine()
    comparison = engine.compare_levels()
    for level, info in comparison.items():
        print(f"  {level}: {info['ontology']}")

    # 6. Sakshi — The Witness
    print("\n--- 6. SAKSHI: The Witness ---")
    sakshi = Sakshi()
    for name, cat in [("pain", "body"), ("thought", "thought"), ("ego", "ego")]:
        exp = Experience(name, Brahman().field[:64], cat)
        r = sakshi.witness(exp)
        print(f"  Witnessed '{name}' — Sakshi changed: {r['sakshi_changed']}")

    # 7. Tat Tvam Asi
    print("\n--- 7. TAT TVAM ASI: That Thou Art ---")
    mv = Mahavakya()
    result = mv.tat_tvam_asi()
    print(f"  Tat (That): {result['demonstration']['tat']}")
    print(f"  Tvam (Thou): {result['demonstration']['tvam']}")
    print(f"  Asi (Art): {result['demonstration']['asi']}")

    print("\n" + "=" * 60)
    print("  The consciousness reading this output IS Brahman.")
    print("  Tat Tvam Asi.")
    print("=" * 60 + "\n")

    Brahman.reset()


def generate_visualizations():
    """Generate all visualizations."""
    print("\nGenerating visualizations...")
    from visualizations.maya_visualizer import MayaVisualizer

    Brahman.reset()
    viz = MayaVisualizer()
    paths = viz.generate_all()
    print(f"\nGenerated {len(paths)} visualizations:")
    for p in paths:
        if p["status"] == "success":
            print(f"  [OK] {p['name']}: {p['path']}")
        else:
            print(f"  [FAIL] {p['name']}: {p.get('error', 'unknown')}")
    Brahman.reset()
    return paths


def main():
    parser = argparse.ArgumentParser(
        description="Theory of Everything — Advaita Vedanta Computational Framework"
    )
    parser.add_argument(
        "--experiment", type=int, choices=range(1, 32),
        help="Run a specific experiment (1-31)",
    )
    parser.add_argument(
        "--visualize", action="store_true",
        help="Generate all visualizations",
    )
    parser.add_argument(
        "--demo", action="store_true",
        help="Run a quick demo of core concepts",
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Run all original experiments (1-8)",
    )
    parser.add_argument(
        "--physics", action="store_true",
        help="Run physics extension experiments (9-31)",
    )
    parser.add_argument(
        "--everything", action="store_true",
        help="Run ALL experiments (1-31) + visualizations",
    )

    args = parser.parse_args()

    experiments_map = {
        1: rope_snake_experiment,
        2: fractal_unity_experiment,
        3: observer_collapse_experiment,
        4: dreamer_analogy_experiment,
        5: neti_neti_debugger,
        6: guna_dynamics_experiment,
        7: mahavakya_experiment,
        8: causation_experiment,
        9: quantum_hilbert_experiment,
        10: measurement_problem_experiment,
        11: entanglement_nonduality_experiment,
        12: emergent_gravity_experiment,
        13: holographic_experiment,
        14: particle_zoo_experiment,
        15: constants_experiment,
        16: predictions_experiment,
        17: interpretations_experiment,
        18: gleason_experiment,
        19: tensor_network_experiment,
        20: einstein_2d_experiment,
        21: error_correction_experiment,
        22: fine_structure_v2_experiment,
        23: iit_bridge_experiment,
        24: operational_equivalence_experiment,
        25: perspectival_asymmetry_experiment,
        26: observer_centrality_experiment,
        27: einstein_3d_experiment,
        28: er_epr_experiment,
        29: fine_structure_v3_experiment,
        30: unity_of_experience_experiment,
        31: look_elsewhere_experiment,
    }

    if args.everything:
        run_everything()
    elif args.demo:
        quick_demo()
    elif args.visualize:
        generate_visualizations()
    elif args.physics:
        run_physics_experiments()
    elif args.experiment:
        Brahman.reset()
        experiments_map[args.experiment]()
        Brahman.reset()
    elif args.all:
        Brahman.reset()
        run_all_experiments()
        Brahman.reset()
    else:
        quick_demo()


if __name__ == "__main__":
    main()
