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
    python main.py --all              # Run all 8 original experiments
    python main.py --experiment N     # Run experiment N (1-8)
    python main.py --physics          # Run physics extension experiments (9-16)
    python main.py --experiment N     # Run experiment N (1-16)
    python main.py --visualize        # Generate all visualizations
    python main.py --everything       # Run ALL experiments (1-16) + visualizations
"""

import sys
import os
import argparse
import json

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from brahman.consciousness import Brahman
from brahman.sat_chit_ananda import SatChitAnanda
from maya.superimposition import Adhyasa
from maya.nama_rupa import NamaRupa
from maya.gunas import Gunas, GunaBalance
from levels.reality_engine import RealityEngine
from emergence.spacetime import ConsciousnessField, EmergentSpacetime
from emergence.causation import Vivartavada
from emergence.observer import Sakshi, Experience
from liberation.neti_neti import NetiNeti
from liberation.mahavakya import Mahavakya
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


# ===== PHYSICS EXTENSION EXPERIMENTS (9-16) =====

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

    print("\n--- Recovering Newton's Law ---")
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

    from constants.derivation import ConstantsFromConsciousness
    from constants.fine_structure import FineStructureDerivation
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


def run_physics_experiments():
    """Run all physics extension experiments (9-16)."""
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
    """Run ALL experiments (1-16) and generate visualizations."""
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
        "--experiment", type=int, choices=range(1, 17),
        help="Run a specific experiment (1-16)",
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
        help="Run physics extension experiments (9-16)",
    )
    parser.add_argument(
        "--everything", action="store_true",
        help="Run ALL experiments (1-16) + visualizations",
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
