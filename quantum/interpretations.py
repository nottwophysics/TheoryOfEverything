"""
Four Interpretations of Quantum Mechanics — Formal Comparison

Each interpretation is implemented as a class that:
    1. Defines its axioms
    2. Answers all 8 phenomena from interpretation_experiment.py
    3. Computes the same physical predictions (must agree on observables)
    4. States what it CANNOT explain
    5. Lists novel predictions unique to it

The interpretations:
    1. Copenhagen           — Bohr, Heisenberg (1927)
    2. Many-Worlds (Everett) — Everett, DeWitt (1957)
    3. Pilot Wave (de Broglie-Bohm) — de Broglie (1927), Bohm (1952)
    4. Advaita (this framework) — Consciousness-first (2024)

The comparison is then: axiom count, explanatory scope, parsimony,
and novel testable predictions.
"""

import numpy as np
from scipy.linalg import expm
from .interpretation_experiment import QuantumSetup, PHENOMENA


# ============================================================
# Base class
# ============================================================

class Interpretation:
    """Base class for a quantum mechanics interpretation."""

    def __init__(self):
        self.setup = QuantumSetup()
        self._name = "Base"
        self._year = 0
        self._founders = []
        self._axioms = []
        self._answers = {}
        self._cannot_explain = []
        self._novel_predictions = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def axiom_count(self) -> int:
        return len(self._axioms)

    def compute_predictions(self) -> dict:
        """All interpretations must agree on empirical predictions."""
        state = self.setup.prepared_state()
        probs = self.setup.probabilities()
        stats = self.setup.run_many_trials()

        # Bell state analysis
        bell = self.setup.bell_state()
        rho_bell = self.setup.density_matrix(bell)
        # Reduced state of first particle
        rho_bell_4 = rho_bell.reshape(2, 2, 2, 2)
        rho_A = np.trace(rho_bell_4, axis1=1, axis2=3)
        purity_A = float(np.real(np.trace(rho_A @ rho_A)))

        return {
            "P(up)": probs["P(up)"],
            "P(down)": probs["P(down)"],
            "statistical_match": stats["deviation"] < 0.02,
            "bell_state_subsystem_purity": purity_A,
            "bell_state_is_mixed": purity_A < 1.0 - 1e-6,
            "all_interpretations_agree_on_these": True,
        }

    def full_report(self) -> dict:
        """Generate the complete interpretation report."""
        return {
            "name": self._name,
            "year": self._year,
            "founders": self._founders,
            "axioms": self._axioms,
            "axiom_count": self.axiom_count,
            "answers": self._answers,
            "phenomena_addressed": len(self._answers),
            "phenomena_total": len(PHENOMENA),
            "cannot_explain": self._cannot_explain,
            "novel_predictions": self._novel_predictions,
            "predictions": self.compute_predictions(),
        }


# ============================================================
# 1. Copenhagen Interpretation
# ============================================================

class Copenhagen(Interpretation):
    """
    The Copenhagen Interpretation (1927)
    Bohr, Heisenberg, Born

    The 'standard' interpretation taught in most textbooks.
    """

    def __init__(self):
        super().__init__()
        self._name = "Copenhagen"
        self._year = 1927
        self._founders = ["Niels Bohr", "Werner Heisenberg", "Max Born"]

        self._axioms = [
            "A1: The state of a system is described by a wave function |ψ⟩ in Hilbert space",
            "A2: Observables are represented by Hermitian operators",
            "A3: Time evolution is unitary: |ψ(t)⟩ = U(t)|ψ(0)⟩ (Schrödinger equation)",
            "A4: Upon measurement, |ψ⟩ collapses to an eigenstate of the measured observable (COLLAPSE POSTULATE)",
            "A5: The probability of outcome aₙ is P(aₙ) = |⟨aₙ|ψ⟩|² (Born rule)",
            "A6: Complementary observables cannot be simultaneously known (complementarity)",
            "A7: There exists a classical/quantum boundary (Heisenberg cut) — measurement apparatus is classical",
        ]

        self._answers = {
            "P1_superposition": {
                "answer": "The wave function is a complete description of the system. "
                          "The particle is not 'secretly' in one state — it genuinely has no definite value.",
                "mechanism": "Mathematical axiom (A1)",
            },
            "P2_measurement": {
                "answer": "The wave function COLLAPSES to an eigenstate. This is instantaneous and irreversible.",
                "mechanism": "Collapse postulate (A4) — added as a separate axiom",
                "problem": "What triggers collapse? Where is the Heisenberg cut?",
            },
            "P3_born_rule": {
                "answer": "The Born rule is a fundamental axiom (A5). It is not derived from anything deeper.",
                "mechanism": "Axiom (A5)",
                "problem": "Why |amplitude|² and not some other function?",
            },
            "P4_entanglement": {
                "answer": "Entanglement is a feature of the wave function. Measurement of one particle "
                          "collapses both instantaneously (non-local collapse).",
                "mechanism": "Collapse postulate applied to composite systems",
                "problem": "Tension with special relativity (non-local collapse)",
            },
            "P5_delayed_choice": {
                "answer": "The particle has no definite path until measured. "
                          "The measurement choice retroactively determines what 'happened.'",
                "mechanism": "Complementarity (A6) — particle/wave are complementary descriptions",
            },
            "P6_wigners_friend": {
                "answer": "Ambiguous. Bohr would say the friend's lab is classical (Heisenberg cut). "
                          "But where exactly is the cut?",
                "mechanism": "Heisenberg cut (A7) — but placement is arbitrary",
                "problem": "No principled way to place the classical/quantum boundary",
            },
            "P7_preferred_basis": {
                "answer": "The measurement apparatus determines the basis. "
                          "The apparatus is classical (by assumption).",
                "mechanism": "Heisenberg cut (A7)",
                "problem": "Circular: 'classical' apparatus is made of quantum parts",
            },
            "P8_consciousness": {
                "answer": "Not addressed. Consciousness is outside the scope of physics.",
                "mechanism": "None",
                "problem": "COMPLETE SILENCE on the hard problem",
            },
        }

        self._cannot_explain = [
            "What triggers collapse (the measurement problem)",
            "Where to place the Heisenberg cut",
            "Why the Born rule holds",
            "The nature of consciousness / subjective experience",
            "What the wave function 'is' (ontology)",
        ]

        self._novel_predictions = [
            "None beyond standard QM — Copenhagen makes no unique predictions",
        ]


# ============================================================
# 2. Many-Worlds Interpretation
# ============================================================

class ManyWorlds(Interpretation):
    """
    The Many-Worlds Interpretation (1957)
    Hugh Everett III, Bryce DeWitt

    No collapse. All outcomes happen. The universe branches.
    """

    def __init__(self):
        super().__init__()
        self._name = "Many-Worlds (Everett)"
        self._year = 1957
        self._founders = ["Hugh Everett III", "Bryce DeWitt"]

        self._axioms = [
            "A1: The state of a system is described by a wave function |ψ⟩ in Hilbert space",
            "A2: Observables are represented by Hermitian operators",
            "A3: Time evolution is ALWAYS unitary — no exceptions, no collapse",
            "A4: The universal wave function describes ALL of reality",
            "A5: Branching: when a measurement occurs, the universe splits into branches, one per outcome",
        ]

        self._answers = {
            "P1_superposition": {
                "answer": "The superposition is the complete physical reality. Nothing is hidden.",
                "mechanism": "Axiom (A1, A4)",
            },
            "P2_measurement": {
                "answer": "No collapse. The observer becomes entangled with the system. "
                          "Both outcomes happen — in different branches of the universal wave function.",
                "mechanism": "Unitary evolution only (A3) + branching (A5)",
                "advantage": "No collapse postulate needed",
            },
            "P3_born_rule": {
                "answer": "Controversial. Attempts to derive it from branch counting or decision theory (Deutsch-Wallace). "
                          "Not universally accepted as successful.",
                "mechanism": "Attempted derivation, not an axiom",
                "problem": "The Born rule derivation is disputed",
            },
            "P4_entanglement": {
                "answer": "Entangled particles are in a joint superposition. "
                          "Measurement causes branching — in each branch, correlations are perfect.",
                "mechanism": "Unitary evolution of the total state",
                "advantage": "No non-local collapse needed",
            },
            "P5_delayed_choice": {
                "answer": "All paths are taken. The 'choice' determines which branch structure you see, "
                          "not what 'actually happened.'",
                "mechanism": "Universal wave function contains all possibilities",
            },
            "P6_wigners_friend": {
                "answer": "Both are correct in their respective branches. "
                          "The friend measures and branches. Wigner describes a superposition of branches.",
                "mechanism": "Branching (A5) — no contradiction because they're in different branches",
                "advantage": "Cleanest resolution of Wigner's friend",
            },
            "P7_preferred_basis": {
                "answer": "Decoherence selects the preferred basis. "
                          "Environment interaction makes certain bases stable (pointer states).",
                "mechanism": "Decoherence (derived, not axiom)",
                "advantage": "Preferred basis emerges naturally",
            },
            "P8_consciousness": {
                "answer": "Consciousness is a physical process that branches along with everything else. "
                          "Each branch-copy of you experiences one outcome.",
                "mechanism": "Functionalism — consciousness = computation = branches",
                "problem": "Does not address the HARD PROBLEM — why is there experience at all?",
            },
        }

        self._cannot_explain = [
            "Why the Born rule (derivation attempts are controversial)",
            "Why we experience ONE branch (the 'basis problem')",
            "What consciousness IS (hard problem)",
            "Whether the other branches are 'real' in any verifiable sense",
            "Extraordinary ontological cost: infinite copies of everything",
        ]

        self._novel_predictions = [
            "No unique predictions that differ from standard QM",
            "In principle: quantum immortality (unfalsifiable)",
            "In principle: quantum suicide thought experiment (untestable)",
        ]


# ============================================================
# 3. Pilot Wave (de Broglie-Bohm)
# ============================================================

class PilotWave(Interpretation):
    """
    The Pilot Wave / de Broglie-Bohm Interpretation (1927/1952)
    Louis de Broglie, David Bohm

    Particles have definite positions at all times.
    A 'pilot wave' guides them.
    """

    def __init__(self):
        super().__init__()
        self._name = "Pilot Wave (de Broglie-Bohm)"
        self._year = 1952
        self._founders = ["Louis de Broglie", "David Bohm"]

        self._axioms = [
            "A1: Particles have definite positions at all times (hidden variables)",
            "A2: A pilot wave ψ evolves according to the Schrödinger equation",
            "A3: Particle velocity is determined by the pilot wave: v = (ℏ/m) Im(∇ψ/ψ) (guidance equation)",
            "A4: The initial distribution of particles follows |ψ|² (quantum equilibrium hypothesis)",
            "A5: The pilot wave is a real physical field in configuration space",
        ]

        self._answers = {
            "P1_superposition": {
                "answer": "The particle always has a definite position. "
                          "The 'superposition' is a property of the pilot WAVE, not the particle.",
                "mechanism": "Hidden variable (A1) + pilot wave (A2)",
            },
            "P2_measurement": {
                "answer": "No collapse. The particle was always in one position. "
                          "Measurement reveals the pre-existing value. "
                          "The pilot wave changes shape (effective collapse) but nothing discontinuous happens.",
                "mechanism": "Guidance equation (A3) steers particle to one detector",
                "advantage": "Deterministic — no randomness at the fundamental level",
            },
            "P3_born_rule": {
                "answer": "Follows from the quantum equilibrium hypothesis (A4). "
                          "If particles start |ψ|²-distributed, they stay that way.",
                "mechanism": "Quantum equilibrium (A4)",
                "problem": "Why the initial distribution? This is assumed, not derived.",
            },
            "P4_entanglement": {
                "answer": "The pilot wave lives in configuration space (3N dimensions for N particles). "
                          "It is fundamentally non-local — changing one particle's wave instantly affects others.",
                "mechanism": "Non-local pilot wave (A5)",
                "problem": "Explicitly non-local — accepted as feature, not bug",
            },
            "P5_delayed_choice": {
                "answer": "The particle took a definite path (determined by initial conditions). "
                          "The delayed choice changes the pilot wave's shape, which retroactively "
                          "determines which path was 'revealed.'",
                "mechanism": "Guidance equation responds to apparatus configuration",
            },
            "P6_wigners_friend": {
                "answer": "The friend's particle has a definite position. The friend sees one outcome. "
                          "Wigner can describe the lab quantum-mechanically, but the particle's position "
                          "was always definite.",
                "mechanism": "Hidden variable (A1) — always definite",
            },
            "P7_preferred_basis": {
                "answer": "Position is always the preferred basis. "
                          "Particles have positions; the pilot wave guides them.",
                "mechanism": "Built into the theory (A1) — position is fundamental",
                "problem": "Why position? This is assumed, not derived.",
            },
            "P8_consciousness": {
                "answer": "Not addressed. Consciousness plays no special role. "
                          "The particle's position exists whether or not anyone observes it.",
                "mechanism": "None",
                "problem": "Complete silence on the hard problem (same as Copenhagen)",
            },
        }

        self._cannot_explain = [
            "Why position is the preferred variable",
            "Why quantum equilibrium holds initially",
            "Non-locality is explicit (tension with relativity)",
            "Configuration space is 3N-dimensional (ontologically extravagant for N particles)",
            "The nature of consciousness (hard problem)",
        ]

        self._novel_predictions = [
            "Quantum non-equilibrium: if particles are NOT |ψ|²-distributed, "
            "deviations from Born rule would appear (potentially testable in early-universe cosmology)",
            "Subquantum measurement: in principle, more precise than Heisenberg limit "
            "(if non-equilibrium exists)",
        ]


# ============================================================
# 4. Advaita Interpretation
# ============================================================

class AdvaitaInterpretation(Interpretation):
    """
    The Advaita (Non-Dual) Interpretation
    Based on Advaita Vedanta + decoherence + holographic principle

    Consciousness is fundamental. The wave function is a mode of
    Brahman's self-awareness. 'Collapse' is perspectival, not physical.
    """

    def __init__(self):
        super().__init__()
        self._name = "Advaita (Consciousness-First)"
        self._year = 2024
        self._founders = ["Shankaracharya (8th c.)", "This framework (2024)"]

        self._axioms = [
            "A1: Consciousness (universal subject) is the ontological primitive — not emergent from matter "
                "(distinctive metaphysical commitment)",
            "A2: The state of reality is represented by |ψ⟩ in Hilbert space "
                "(shared with Everett — the interpretive claim is that H describes the subject's structure)",
            "A3: Time evolution is always unitary — no collapse (shared with Everett)",
            "A4: Definite outcomes arise from decoherence + partial tracing "
                "(shared with Everett — novelty is ontological, not dynamical)",
            "A5: Born rule follows from Gleason's theorem given non-contextuality and H "
                "(shared with Everett — not a novel observation)",
        ]

        self._answers = {
            "P1_superposition": {
                "answer": "Superposition is the natural state of the universal subject prior to any "
                          "particular perspective. This is not ignorance of a hidden state — it is the "
                          "genuine mode of undifferentiated awareness. Operationally identical to Everett.",
                "mechanism": "Axiom A2 — Hilbert space as structure of the universal subject",
                "advantage": "Superposition has a natural ontology in this framework",
                "shared_with_everett": True,
            },
            "P2_measurement": {
                "answer": "No collapse. System + apparatus + environment become entangled. "
                          "The total state remains pure. The observer's reduced state appears mixed. "
                          "This is perspectival, not physical. Operationally identical to Everett.",
                "mechanism": "Decoherence + partial trace (A4) — shared with Everett",
                "advantage": "No collapse postulate needed. Novelty is ontological, not dynamical.",
                "demonstration": "Experiment 10: total purity = 1.000, reduced purity = 0.250",
                "shared_with_everett": True,
            },
            "P3_born_rule": {
                "answer": "Gleason's theorem (1957) proves: in any Hilbert space of dimension ≥ 3, "
                          "the ONLY consistent probability measure on subspaces is P(aₙ) = Tr(ρ Pₙ), "
                          "which for pure states gives |⟨aₙ|ψ⟩|². "
                          "We verify that Brahman's Hilbert space satisfies Gleason's conditions "
                          "(dimension ≥ 3, non-contextual measure). The Born rule then follows as a "
                          "theorem, not an independent axiom.",
                "mechanism": "Gleason's theorem verified for Brahman Hilbert space (see quantum/gleason.py)",
                "advantage": "Born rule is a THEOREM in this framework, not an axiom "
                             "(unlike Copenhagen A5 and Bohm A4). Reduces axiom count.",
            },
            "P4_entanglement": {
                "answer": "Entanglement is the NATURAL state — non-duality (Advaita) at the quantum level. "
                          "Separation is the exception that requires explanation, not entanglement. "
                          "Bell violation (S = 2√2) confirms reality is non-local = non-dual.",
                "mechanism": "Axiom A1 (consciousness is one) → entanglement is default",
                "advantage": "Entanglement is not mysterious — it is the quantum signature of non-duality. "
                             "Non-locality is expected, not problematic.",
                "demonstration": "Experiment 11: CHSH S = -2.828, Bell violation confirmed",
            },
            "P5_delayed_choice": {
                "answer": "The particle has no trajectory independent of observation (same as Copenhagen). "
                          "But here it's not mysterious: Brahman (the total state) is timeless. "
                          "The 'delayed choice' operates within the appearance of time (Maya). "
                          "From the absolute perspective (Paramarthika), there is no before/after.",
                "mechanism": "A1 — consciousness is prior to time. Time is emergent (Maya).",
                "advantage": "No retrocausality paradox — time itself is part of the appearance",
            },
            "P6_wigners_friend": {
                "answer": "Wigner and friend are both entangled with the system — both are within Maya. "
                          "From within Maya (Vyavaharika), the friend sees one outcome and Wigner describes a superposition. "
                          "Both are correct at their level. "
                          "From the absolute level (Paramarthika), the total state is one pure state — no contradiction.",
                "mechanism": "Three levels of reality (Paramarthika/Vyavaharika/Pratibhasika)",
                "advantage": "Resolves the paradox by recognizing that 'observer' is a level-dependent concept. "
                             "There is no absolute observer within Maya — only Brahman (Sakshi) is absolute.",
            },
            "P7_preferred_basis": {
                "answer": "The preferred basis is selected by decoherence — the same mechanism that creates "
                          "the classical world from quantum Brahman. The environment (Maya) interacts most "
                          "strongly with position-like variables, making them 'pointer states.'",
                "mechanism": "Decoherence (derived from A4)",
                "advantage": "Same as Many-Worlds but with ontological grounding — "
                             "the decoherence basis is the pattern of Maya's interaction with Brahman",
            },
            "P8_consciousness": {
                "answer": "This is where the interpretation is distinctive. "
                          "Consciousness is not produced by measurement — it is the ontological primitive (A1). "
                          "The subjective experience of one outcome arises because the observer "
                          "is a localized perspective within the universal subject, correlated with "
                          "one branch via decoherence. The hard problem is REFRAMED (not solved): "
                          "the question shifts from cross-categorial (why does matter produce experience?) "
                          "to intra-categorial (why does the universal subject have Hilbert space structure?).",
                "mechanism": "Axiom A1 — consciousness as ontological primitive",
                "advantage": "Engages the hard problem explicitly, which standard realist interpretations "
                             "typically do not prioritize. Does not claim to solve it.",
                "residual_question": "Why does the universal subject have this particular mathematical structure? "
                                    "This is analogous to asking why spacetime has the metric it does.",
            },
        }

        self._cannot_explain = [
            "Currently empirically equivalent to Everett — no experiment distinguishes them",
            "Why the universal subject has Hilbert space structure (the transformed hard problem)",
            "Whether the ontological additions over Everett justify the metaphysical commitments",
            "Whether consciousness as primitive is explanatory or merely relocates the mystery",
            "Scope note on the prediction list (review 2026-08-15): P1/P2/P3/P5 "
            "are consequences of broader quantum-gravity/QM programs rather than "
            "discriminators of THIS interpretation; P4 is the only candidate "
            "discriminator and is the furthest from testability. P2, if "
            "observed, would favor objective-collapse models over this "
            "framework's own no-collapse axiom A3 — it functions as a "
            "falsifier (cf. F4), not a confirmation.",
        ]

        self._novel_predictions = [
            "P1: Entanglement between massive objects produces gravitational signatures (testable 15-25 yr)",
            "P2: Gravitational decoherence mass threshold at ~10⁹-10¹² amu (testable 5-15 yr)",
            "P3: Vacuum has measurable entanglement structure scaling as area law (testable 5-15 yr)",
            "P4: Conscious observation has a specific decoherence signature distinct from automated detection (testable 20+ yr)",
            "P5: Holographic noise in interferometers — EXCLUDED at the stated amplitude by the Fermilab Holometer (2015-2016)",
        ]

    def demonstrate_measurement_resolution(self) -> dict:
        """
        Run the measurement problem resolution quantitatively.

        Show that the SAME physical setup produces:
        - Brahman's view: pure state, purity = 1.0
        - Jiva's view: mixed state, purity = 1/d
        """
        state = self.setup.prepared_state()

        # System + apparatus (4-dimensional total)
        apparatus_ready = np.array([1, 0], dtype=np.complex128)
        total_pre = np.kron(state, apparatus_ready)

        # Measurement interaction: entanglement
        # |ψ⟩|ready⟩ → α|↑⟩|recorded_up⟩ + β|↓⟩|recorded_down⟩
        total_post = np.zeros(4, dtype=np.complex128)
        total_post[0] = self.setup.alpha   # |↑⟩|↑_app⟩ = |00⟩
        total_post[3] = self.setup.beta    # |↓⟩|↓_app⟩ = |11⟩
        total_post /= np.linalg.norm(total_post)

        # Total state (Brahman's view)
        rho_total = np.outer(total_post, total_post.conj())
        purity_total = float(np.real(np.trace(rho_total @ rho_total)))

        # Reduced state (Jiva's view) — trace out apparatus
        rho_system = np.zeros((2, 2), dtype=np.complex128)
        rho_4 = rho_total.reshape(2, 2, 2, 2)
        rho_system = np.trace(rho_4, axis1=1, axis2=3)
        purity_reduced = float(np.real(np.trace(rho_system @ rho_system)))

        # Off-diagonal coherence
        coherence = float(np.sum(np.abs(rho_system - np.diag(np.diag(rho_system)))))

        return {
            "total_state_purity": purity_total,
            "total_collapsed": purity_total < 1.0 - 1e-6,
            "reduced_state_purity": purity_reduced,
            "reduced_appears_collapsed": purity_reduced < 1.0 - 1e-6,
            "coherence_remaining": coherence,
            "classical_probabilities": np.real(np.diag(rho_system)).tolist(),
            "resolution": (
                f"Total state purity: {purity_total:.6f} (PURE — no collapse). "
                f"Reduced state purity: {purity_reduced:.6f} (MIXED — appears collapsed). "
                "Same physics. Two perspectives. "
                "The 'collapse' is the jiva's limited view of Brahman's non-dual reality."
            ),
        }


# ============================================================
# Formal Comparison Engine
# ============================================================

class InterpretationComparison:
    """
    Runs all four interpretations on the same experiment and
    produces a formal comparison.
    """

    def __init__(self):
        self.interpretations = {
            "copenhagen": Copenhagen(),
            "many_worlds": ManyWorlds(),
            "pilot_wave": PilotWave(),
            "advaita": AdvaitaInterpretation(),
        }

    def axiom_comparison(self) -> dict:
        """Compare axiom counts and types."""
        result = {}
        for key, interp in self.interpretations.items():
            report = interp.full_report()
            result[key] = {
                "name": report["name"],
                "axiom_count": report["axiom_count"],
                "axioms": report["axioms"],
            }

        # Rank by parsimony
        ranked = sorted(result.items(), key=lambda x: x[1]["axiom_count"])
        result["ranking_by_parsimony"] = [
            f"{r[1]['name']}: {r[1]['axiom_count']} axioms" for r in ranked
        ]

        return result

    def explanatory_scope(self) -> dict:
        """Compare how many phenomena each interpretation addresses."""
        result = {}
        for key, interp in self.interpretations.items():
            report = interp.full_report()
            addressed = 0
            has_problem = 0
            for pid, answer in report["answers"].items():
                addressed += 1
                if "problem" in answer or "residual_question" in answer:
                    has_problem += 1

            result[key] = {
                "name": report["name"],
                "phenomena_addressed": addressed,
                "phenomena_with_problems": has_problem,
                "phenomena_clean": addressed - has_problem,
                "cannot_explain": report["cannot_explain"],
            }

        return result

    def novel_predictions_comparison(self) -> dict:
        """Compare novel predictions."""
        result = {}
        for key, interp in self.interpretations.items():
            report = interp.full_report()
            result[key] = {
                "name": report["name"],
                "novel_predictions": report["novel_predictions"],
                "num_predictions": len(report["novel_predictions"]),
            }
        return result

    def consciousness_comparison(self) -> dict:
        """Compare how each addresses the hard problem of consciousness."""
        result = {}
        for key, interp in self.interpretations.items():
            report = interp.full_report()
            p8 = report["answers"].get("P8_consciousness", {})
            result[key] = {
                "name": report["name"],
                "addresses_consciousness": "mechanism" in p8 and p8["mechanism"] != "None",
                "answer": p8.get("answer", "Not addressed"),
                "has_problem": "problem" in p8,
            }
        return result

    def empirical_agreement(self) -> dict:
        """Verify all interpretations agree on measurable predictions."""
        predictions = {}
        for key, interp in self.interpretations.items():
            predictions[key] = interp.compute_predictions()

        # Check agreement
        p_ups = [p["P(up)"] for p in predictions.values()]
        p_downs = [p["P(down)"] for p in predictions.values()]

        return {
            "all_agree_on_P_up": max(p_ups) - min(p_ups) < 1e-10,
            "all_agree_on_P_down": max(p_downs) - min(p_downs) < 1e-10,
            "P_up": p_ups[0],
            "P_down": p_downs[0],
            "note": "All four interpretations make IDENTICAL empirical predictions. "
                    "They differ in ontology (what is real), not in observables (what is measured). "
                    "Except: each has unique novel predictions that could distinguish them.",
        }

    def advaita_measurement_demo(self) -> dict:
        """Run the Advaita-specific measurement demonstration."""
        advaita = self.interpretations["advaita"]
        return advaita.demonstrate_measurement_resolution()

    def full_comparison(self) -> dict:
        """Generate the complete formal comparison."""
        return {
            "axioms": self.axiom_comparison(),
            "explanatory_scope": self.explanatory_scope(),
            "novel_predictions": self.novel_predictions_comparison(),
            "consciousness": self.consciousness_comparison(),
            "empirical_agreement": self.empirical_agreement(),
            "advaita_measurement_demo": self.advaita_measurement_demo(),
        }

    def summary_table(self) -> dict:
        """Generate the final summary comparison table."""
        rows = {}
        for key, interp in self.interpretations.items():
            report = interp.full_report()
            answers = report["answers"]
            problems = sum(1 for a in answers.values() if "problem" in a or "residual_question" in a)
            p8 = answers.get("P8_consciousness", {})

            rows[key] = {
                "name": report["name"],
                "year": report["year"],
                "axiom_count": report["axiom_count"],
                "phenomena_addressed": len(answers),
                "phenomena_with_problems": problems,
                "addresses_consciousness": p8.get("mechanism", "None") != "None",
                "novel_predictions": len(report["novel_predictions"]),
                "needs_collapse_postulate": any(
                    "collapses" in a.lower() or "collapse postulate" in a.lower()
                    for a in report["axioms"]
                ),
                "needs_hidden_variables": any(
                    "hidden variable" in a.lower() or "definite positions" in a.lower()
                    for a in report["axioms"]
                ),
                "needs_branching": any(
                    "splits" in a.lower() or "branching" in a.lower()
                    for a in report["axioms"]
                ),
            }

        return rows
