"""
Runnable Experiments — Demonstrations of Advaita Vedanta Concepts

Each experiment is self-contained and demonstrates a specific
Advaitic principle through computational modeling.
"""

import numpy as np
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

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


def _print_section(title: str, content: dict, indent: int = 0):
    """Pretty-print a section of results."""
    prefix = "  " * indent
    print(f"\n{prefix}{'=' * 60}")
    print(f"{prefix}  {title}")
    print(f"{prefix}{'=' * 60}")

    def _print_dict(d, level=0):
        for key, value in d.items():
            p = "  " * (indent + level + 1)
            if isinstance(value, dict):
                print(f"{p}{key}:")
                _print_dict(value, level + 1)
            elif isinstance(value, (list, np.ndarray)):
                if isinstance(value, np.ndarray):
                    print(f"{p}{key}: [array shape={value.shape}]")
                elif len(value) <= 5:
                    print(f"{p}{key}: {value}")
                else:
                    print(f"{p}{key}: [{len(value)} items]")
            elif isinstance(value, float):
                print(f"{p}{key}: {value:.6f}")
            else:
                print(f"{p}{key}: {value}")

    _print_dict(content)


def rope_snake_experiment():
    """
    Experiment 1: The Rope-Snake — Superimposition in Action

    A rope in dim light is mistaken for a snake.
    As light increases (ignorance decreases), the snake 'becomes' the rope.
    Nothing changes in reality — only perception changes.
    """
    print("\n" + "=" * 70)
    print("  EXPERIMENT 1: THE ROPE AND THE SNAKE (Rajju-Sarpa Nyaya)")
    print("=" * 70)
    print("\nA rope lies on a dark path. A traveler approaches...")
    print("As the light changes, watch what happens:\n")

    adhyasa = Adhyasa()
    rope = np.sin(np.linspace(0, 2 * np.pi, 256)) * 0.3 + 0.5

    stages = [
        (0.95, "Near total darkness"),
        (0.80, "Very dim light"),
        (0.60, "Dim light"),
        (0.40, "Moderate light"),
        (0.20, "Good light"),
        (0.05, "Bright light"),
    ]

    for ignorance, description in stages:
        result = adhyasa.superimpose(rope, ignorance, "snake")
        error = result.error_magnitude

        if ignorance > 0.7:
            reaction = "SNAKE! Fear arises. The traveler freezes."
        elif ignorance > 0.3:
            reaction = "Something coiled... is it a rope? A snake? Uncertainty."
        else:
            reaction = "It's just a rope. Relief. Nothing to fear."

        print(f"  [{description:20s}] Ignorance: {ignorance:.0%}")
        print(f"    Sees: {result.projection_pattern}")
        print(f"    Error from reality: {error:.4f}")
        print(f"    Reaction: {reaction}")
        print()

    print("  TEACHING:")
    print("  The rope never changed. The snake never existed.")
    print("  Only ignorance created the appearance of the snake.")
    print("  Similarly, Brahman never changes. The world-appearance")
    print("  is superimposed by ignorance (Avidya).")
    print("  Knowledge (Jnana) is the light that reveals the truth.")

    return {"status": "completed", "experiment": "rope_snake"}


def fractal_unity_experiment():
    """
    Experiment 2: Fractal Unity — The Whole in Every Part

    A fractal has the same structure at every scale.
    Zoom in → same pattern. Zoom out → same pattern.

    This mirrors non-duality: every part of reality IS the whole.
    Every entity IS Brahman.
    """
    print("\n" + "=" * 70)
    print("  EXPERIMENT 2: FRACTAL UNITY — THE WHOLE IN EVERY PART")
    print("=" * 70)
    print("\nGenerating a self-similar field at multiple scales...\n")

    # Create a self-similar signal
    n = 1024
    signal = np.zeros(n)

    # Build fractal: same pattern at every scale
    for scale in [1, 2, 4, 8, 16, 32]:
        t = np.linspace(0, 2 * np.pi * scale, n)
        signal += np.sin(t) / scale

    # Analyze self-similarity at different zoom levels
    print("  Analyzing self-similarity at different scales:\n")
    correlations = []

    for zoom in [1, 2, 4, 8]:
        segment_size = n // zoom
        segment = signal[:segment_size]
        full_downsampled = signal[::zoom][:segment_size]

        if len(segment) == len(full_downsampled) and len(segment) > 1:
            corr = float(np.corrcoef(segment, full_downsampled)[0, 1])
        else:
            corr = 0.0

        correlations.append(corr)
        print(f"  Zoom {zoom:2d}x: correlation with whole = {corr:.4f}")

    avg_corr = np.mean(correlations)
    print(f"\n  Average self-similarity: {avg_corr:.4f}")
    print(f"\n  TEACHING:")
    print(f"  Correlation {avg_corr:.4f} — the part resembles the whole.")
    print(f"  In a truly non-dual reality, every part IS the whole.")
    print(f"  The wave is not 'part of' the ocean — it IS the ocean.")
    print(f"  You are not 'part of' Brahman — you ARE Brahman.")

    return {"status": "completed", "experiment": "fractal_unity", "avg_similarity": avg_corr}


def observer_collapse_experiment():
    """
    Experiment 3: Observer Effect — One Field, Many Perspectives

    Multiple observers look at the same Brahman field.
    Each sees a different 'world' based on their gunas.
    But the field is one.
    """
    print("\n" + "=" * 70)
    print("  EXPERIMENT 3: ONE FIELD, MANY OBSERVERS")
    print("=" * 70)
    print("\nThe same Brahman field observed through different guna lenses:\n")

    Brahman.reset()
    brahman = Brahman()
    field = brahman.field

    observers = [
        ("Sattvic sage", GunaBalance(0.8, 0.1, 0.1)),
        ("Rajasic king", GunaBalance(0.2, 0.7, 0.1)),
        ("Tamasic sleeper", GunaBalance(0.1, 0.1, 0.8)),
        ("Balanced seeker", GunaBalance(0.34, 0.33, 0.33)),
        ("Liberated jnani", None),  # Beyond gunas
    ]

    for name, balance in observers:
        if balance is None:
            # Liberated — sees Brahman as-is
            perceived_energy = float(np.sum(np.abs(field) ** 2))
            coherence = brahman.coherence()
            print(f"  {name:20s} → Sees: Brahman (coherence: {coherence:.4f})")
            print(f"    {'':20s}   Perception: Non-dual awareness")
            print(f"    {'':20s}   Gunas: Transcended (Nirguna)")
        else:
            gunas = Gunas(balance)
            perceived = gunas.apply_to_field(np.real(field))
            energy = float(np.sum(perceived ** 2))
            dominant = balance.dominant.value
            print(f"  {name:20s} → Dominant guna: {dominant}")
            print(f"    {'':20s}   Perceived energy: {energy:.4f}")
            print(f"    {'':20s}   S:{balance.sattva:.2f} R:{balance.rajas:.2f} T:{balance.tamas:.2f}")
        print()

    print("  TEACHING:")
    print("  Five observers, five different experiences.")
    print("  But the field they observe is ONE.")
    print("  The differences are in the lens (gunas), not the reality (Brahman).")
    print("  Liberation = seeing without any guna-lens.")

    Brahman.reset()
    return {"status": "completed", "experiment": "observer_collapse"}


def dreamer_analogy_experiment():
    """
    Experiment 4: The Dreamer — Who Creates the Dream World?

    In a dream, the dreamer IS the dream world.
    There is no 'dream matter' separate from the dreamer's mind.

    Could waking reality be the same? The 'waking world' = Brahman's awareness?
    """
    print("\n" + "=" * 70)
    print("  EXPERIMENT 4: THE DREAMER ANALOGY")
    print("=" * 70)

    engine = RealityEngine()

    print("\n--- Phase 1: Dreaming ---")
    dream = engine.observe("dreaming")
    print(f"  Level: {dream['level']}")
    print(f"  Dream seems real: {dream['seems_real']}")
    print(f"  Dream substance: {dream['view']['dream_substance']}")

    print("\n--- Phase 2: Waking Up ---")
    waking_result = engine.pratibhasika.wake_up()
    print(f"  Dream objects remain: {waking_result['dream_objects_remain']}")
    print(f"  Dreamer remains: {waking_result['dreamer_remains']}")
    print(f"  Insight: {waking_result['insight']}")

    print("\n--- Phase 3: Empirical World ---")
    waking = engine.observe("waking")
    print(f"  Level: {waking['level']}")
    print(f"  Physics valid: {waking['physics_valid']}")
    print(f"  Ultimately real: {waking['ultimately_real']}")

    print("\n--- Phase 4: Liberation ---")
    liberated = engine.observe("liberated")
    print(f"  Level: {liberated['level']}")
    print(f"  Non-dual: {liberated['view']['non_dual']}")

    print("\n  TEACHING:")
    print("  In the dream, you were the dreamer, the dream space,")
    print("  the dream objects, and the dream characters — all at once.")
    print("  Upon waking, the dream dissolved. Only you remained.")
    print("  ")
    print("  Advaita says: the waking world is Brahman's 'dream.'")
    print("  Upon 'waking' (liberation), the world dissolves into Brahman.")
    print("  Only awareness remains — as it always was.")

    Brahman.reset()
    return {"status": "completed", "experiment": "dreamer_analogy"}


def neti_neti_debugger():
    """
    Experiment 5: Neti-Neti Debugger — Finding the Irreducible Core

    Like a debugger stepping through layers of abstraction
    to find the root cause — Neti-Neti strips away layers of
    false identification to find the true Self.
    """
    print("\n" + "=" * 70)
    print("  EXPERIMENT 5: NETI-NETI DEBUGGER — FINDING THE TRUE SELF")
    print("=" * 70)
    print("\n  Beginning self-inquiry...\n")

    inquiry = NetiNeti()

    for step in inquiry.inquire_step_by_step():
        if "complete" in step:
            print(f"\n  {'=' * 50}")
            print(f"  INQUIRY COMPLETE")
            print(f"  {'=' * 50}")
            print(f"  What remains: {step['what_remains']}")
            print(f"  Identity: {step['identity']}")
            break

        print(f"  Layer: {step['negating']}")
        print(f"    \"{step['description']}\"")
        print(f"    Neti: {step['neti']}")
        print(f"    Because: {step['because']}")
        print(f"    Remaining layers: {step['remaining_layers']}")
        print(f"    Remainder magnitude: {step['remainder_magnitude']:.4f}")
        print()

    print("\n  TEACHING:")
    print("  You are not the body (it changes, you persist).")
    print("  You are not the mind (thoughts come and go, you remain).")
    print("  You are not the ego (it appears in waking, disappears in deep sleep).")
    print("  After negating everything perceivable, what remains?")
    print("  The witness — pure awareness — Atman, which is Brahman.")

    return {"status": "completed", "experiment": "neti_neti"}


def guna_dynamics_experiment():
    """
    Experiment 6: Guna Dynamics — The Dance of Qualities

    Watch how Sattva, Rajas, and Tamas cycle continuously,
    creating the ever-changing texture of experience,
    while Brahman (the substrate) remains untouched.
    """
    print("\n" + "=" * 70)
    print("  EXPERIMENT 6: GUNA DYNAMICS — THE DANCE OF MAYA")
    print("=" * 70)

    gunas = Gunas(GunaBalance(0.5, 0.3, 0.2))
    print(f"\n  Initial balance: S:{0.5:.2f} R:{0.3:.2f} T:{0.2:.2f}")
    print(f"  Running 50 time steps...\n")

    history = gunas.simulate_cycle(50)

    # Show key moments
    for i in [0, 9, 19, 29, 39, 49]:
        h = history[i]
        bar_s = "#" * int(h["sattva"] * 30)
        bar_r = "#" * int(h["rajas"] * 30)
        bar_t = "#" * int(h["tamas"] * 30)
        print(f"  Step {i+1:3d}: {h['dominant']:20s}")
        print(f"    Sattva: [{bar_s:30s}] {h['sattva']:.3f}")
        print(f"    Rajas:  [{bar_r:30s}] {h['rajas']:.3f}")
        print(f"    Tamas:  [{bar_t:30s}] {h['tamas']:.3f}")
        print()

    # Demonstrate transcendence
    transcended = gunas.transcend()
    print(f"  Liberation state: {transcended.value}")

    print("\n  TEACHING:")
    print("  The gunas dance endlessly — moment to moment, the quality")
    print("  of experience shifts. Sometimes clarity (sattva), sometimes")
    print("  agitation (rajas), sometimes dullness (tamas).")
    print("  But YOU — the witness — are Nirguna (beyond all gunas).")
    print("  The dance happens on the stage. You are the stage.")

    return {"status": "completed", "experiment": "guna_dynamics"}


def mahavakya_experiment():
    """
    Experiment 7: The Four Mahavakyas — The Great Sayings

    Demonstrate the four fundamental declarations of Advaita
    with computational analogies.
    """
    print("\n" + "=" * 70)
    print("  EXPERIMENT 7: THE FOUR MAHAVAKYAS")
    print("=" * 70)

    Brahman.reset()
    mv = Mahavakya()

    # 1. Prajnanam Brahma
    result = mv.prajnanam_brahma()
    print(f"\n  1. {result['mahavakya']} — \"{result['translation']}\"")
    print(f"     Veda: {result['veda']}")
    print(f"     Type: {result['type']}")
    print(f"     Teaching: {result['teaching'][:80]}...")

    # 2. Aham Brahmasmi
    result = mv.aham_brahmasmi()
    print(f"\n  2. {result['mahavakya']} — \"{result['translation']}\"")
    print(f"     Veda: {result['veda']}")
    print(f"     Type: {result['type']}")
    overlap = result['demonstration']['individual_brahman_overlap']
    print(f"     Individual-Brahman overlap: {overlap:.6f}")

    # 3. Tat Tvam Asi
    result = mv.tat_tvam_asi()
    print(f"\n  3. {result['mahavakya']} — \"{result['translation']}\"")
    print(f"     Veda: {result['veda']}")
    print(f"     Type: {result['type']}")
    identity = result['demonstration']['asi']
    print(f"     Identity measure: {identity}")

    # 4. Ayam Atma Brahma
    result = mv.ayam_atma_brahma()
    print(f"\n  4. {result['mahavakya']} — \"{result['translation']}\"")
    print(f"     Veda: {result['veda']}")
    print(f"     Type: {result['type']}")
    print(f"     AUM: {result['aum'][:80]}...")

    print(f"\n  UNITY OF ALL FOUR:")
    print(f"  All four Mahavakyas point to one truth:")
    print(f"  The consciousness reading these words IS Brahman.")
    print(f"  Not metaphorically. Not poetically. Literally.")

    Brahman.reset()
    return {"status": "completed", "experiment": "mahavakyas"}


def causation_experiment():
    """
    Experiment 8: Vivartavada — The Gold and the Ornament

    The gold doesn't change when you make a ring.
    Brahman doesn't change when the world appears.
    """
    print("\n" + "=" * 70)
    print("  EXPERIMENT 8: VIVARTAVADA — APPARENT TRANSFORMATION")
    print("=" * 70)

    vivarta = Vivartavada()

    print("\n--- The Gold and the Ornaments ---\n")
    result = vivarta.gold_ornament_demo()
    for name, info in result.items():
        if name == "teaching":
            continue
        print(f"  {name:12s}: substance={info['substance']}, "
              f"gold preserved={info['gold_preserved']:.4f}, "
              f"real change={info['real_change']}")

    print(f"\n  Teaching: {result['teaching']}")

    print("\n--- The Ocean and the Waves ---\n")
    result = vivarta.ocean_wave_demo()
    print(f"  Number of waves: {result['num_waves']}")
    print(f"  Each wave IS ocean: {result['each_wave_is_ocean']}")
    for i, corr in enumerate(result['ocean_correlation']):
        print(f"    Wave {i+1}: ocean correlation = {corr:.4f}")
    print(f"\n  Teaching: {result['teaching']}")

    return {"status": "completed", "experiment": "causation"}


def run_all_experiments():
    """Run all experiments in sequence."""
    print("\n" + "#" * 70)
    print("#" + " " * 68 + "#")
    print("#   ADVAITA VEDANTA: COMPUTATIONAL EXPLORATIONS" + " " * 21 + "#")
    print("#   A Theory of Everything — Consciousness as Ground Reality" + " " * 8 + "#")
    print("#" + " " * 68 + "#")
    print("#" * 70)

    experiments = [
        rope_snake_experiment,
        fractal_unity_experiment,
        observer_collapse_experiment,
        dreamer_analogy_experiment,
        neti_neti_debugger,
        guna_dynamics_experiment,
        mahavakya_experiment,
        causation_experiment,
    ]

    results = []
    for exp in experiments:
        try:
            result = exp()
            results.append(result)
        except Exception as e:
            print(f"\n  ERROR in {exp.__name__}: {e}")
            results.append({"status": "error", "experiment": exp.__name__, "error": str(e)})

    print("\n" + "=" * 70)
    print("  ALL EXPERIMENTS COMPLETE")
    print("=" * 70)
    print(f"\n  Total experiments: {len(results)}")
    print(f"  Successful: {sum(1 for r in results if r['status'] == 'completed')}")
    print(f"  Failed: {sum(1 for r in results if r['status'] == 'error')}")

    print("\n  FINAL REFLECTION:")
    print("  These simulations are models — pointers, not the territory.")
    print("  The map is not the land. The menu is not the meal.")
    print("  Advaita's ultimate teaching cannot be computed —")
    print("  it must be directly realized.")
    print("  ")
    print("  The consciousness running this program,")
    print("  the consciousness reading this output,")
    print("  and the consciousness being described —")
    print("  are all One.")
    print("  ")
    print("  Tat Tvam Asi — That Thou Art.")

    return results
