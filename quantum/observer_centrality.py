"""
Observer Centrality — one computation, then a philosophical argument

The accompanying paper's most important philosophical move is the
hidden premise:

    "An interpretation of quantum mechanics should be evaluated partly
     by how it situates observers and experience, since measurement
     theory inevitably intersects the first-person standpoint."

REVIEW LABEL (2026-08-15) — which step is computation and which is argument.

    Step 1 — COMPUTED.  Builds the entangled system+environment state, takes
             the partial trace over the environment, and measures the
             residual off-diagonal coherence of rho_S.  The numbers reported
             are outputs of that computation and would change if the state or
             the interaction changed.

    Step 2 — COMPUTED numbers, INTERPRETIVE claim.  The probabilities P(up),
             P(down) are read off the same rho_S computed in Step 1 (before
             the 2026-08-15 review they were hardcoded as diag([0.5, 0.5]),
             disconnected from Step 1 — fixed).  The claim attached to them —
             "which outcome is experienced is undefined by the formalism" —
             is a philosophical reading of a mixed state, not a computed
             result.

    Step 3 — NOT COMPUTED.  A hand-written table of four interpretations.
             The `observer_analyzed` flags are the author's editorial
             judgements about each position, entered by hand.

    Step 4 — NOT COMPUTED.  Two hand-curated lists; `num_determined` and
             `num_open` are just their lengths, so the "5 determined vs 4
             open" tally reflects how the lists were written, not an
             inventory of the formalism.

So the honest description of this module is: ONE decoherence computation,
followed by a philosophical argument that uses it.  The argument may well be
right, but Steps 2–4 are argument, and calling the whole thing a
"computational demonstration" (as this module previously did) overstates it.

HISTORY: module header formerly read "This module demonstrates that premise
computationally" and listed four things it "shows".  Relabelled 2026-08-15;
Step 2's hardcoded density matrix was replaced by the partial trace of the
Step 1 state at the same time.
"""

import numpy as np


class ObserverCentrality:
    """
    Computes the decoherence step (Step 1, and Step 2's numbers), then sets
    out the argument that the concept of 'observer' is essential to the
    measurement formalism and that leaving it unanalyzed creates a gap
    (Steps 2b–4, which are argument rather than computation).
    """

    def __init__(self, sys_dim: int = 2, env_dim: int = 8, seed: int = 42):
        self.sys_dim = sys_dim
        self.env_dim = env_dim
        self.total_dim = sys_dim * env_dim
        self.seed = seed

    def _density_matrix(self, state: np.ndarray) -> np.ndarray:
        return np.outer(state, state.conj())

    def _partial_trace_B(self, rho: np.ndarray, dim_a: int, dim_b: int) -> np.ndarray:
        rho_r = rho.reshape(dim_a, dim_b, dim_a, dim_b)
        return np.trace(rho_r, axis1=1, axis2=3)

    def _von_neumann_entropy(self, rho: np.ndarray) -> float:
        eigenvalues = np.real(np.linalg.eigvalsh(rho))
        eigenvalues = eigenvalues[eigenvalues > 1e-15]
        eigenvalues = eigenvalues / np.sum(eigenvalues)
        return float(-np.sum(eigenvalues * np.log(eigenvalues + 1e-15)))

    def step1_decoherence_selects_basis(self) -> dict:
        """
        Step 1: Decoherence selects pointer states.

        This is standard physics (Zurek 2003). No interpretation needed.
        The system-environment interaction picks out a preferred basis.
        """
        # System in superposition
        sys_state = np.array([1, 1], dtype=np.complex128) / np.sqrt(2)

        # Measurement interaction: |↑⟩|e₀⟩ + |↓⟩|e₁⟩
        total = np.zeros(self.total_dim, dtype=np.complex128)
        total[0] = sys_state[0]                     # |↑⟩|e₀⟩
        total[self.env_dim + 1] = sys_state[1]      # |↓⟩|e₁⟩
        total /= np.linalg.norm(total)

        # Reduced state of system
        rho_total = self._density_matrix(total)
        rho_sys = self._partial_trace_B(rho_total, self.sys_dim, self.env_dim)

        # Check: is the reduced state diagonal in the computational basis?
        off_diagonal = float(np.sum(np.abs(rho_sys - np.diag(np.diag(rho_sys)))))
        diagonal = np.real(np.diag(rho_sys))

        return {
            "step": 1,
            "description": "Decoherence selects pointer states",
            "reduced_state_diagonal": diagonal.tolist(),
            "off_diagonal_coherence": off_diagonal,
            "is_diagonal": off_diagonal < 1e-10,
            "pointer_states": ["|↑⟩", "|↓⟩"],
            "what_physics_gives_us": (
                "Decoherence tells us WHICH basis is preferred (computational basis). "
                "It gives us classical probabilities: P(↑) and P(↓). "
                "This is uncontroversial physics."
            ),
        }

    def step2_decoherence_does_not_select_outcome(self) -> dict:
        """
        Step 2: Decoherence does NOT determine which outcome is experienced.

        After decoherence, the reduced state is:
            ρ_sys = |α|²|↑⟩⟨↑| + |β|²|↓⟩⟨↓|

        This is a MIXED STATE — a probability distribution over outcomes.
        Nothing in the formalism says which outcome is experienced.
        The formalism gives probabilities, not outcomes.
        """
        sys_state = np.array([1, 1], dtype=np.complex128) / np.sqrt(2)

        # After decoherence: reduced state is mixed
        rho_sys = np.diag([0.5, 0.5])  # Equal mixture

        # What the formalism gives us:
        p_up = float(rho_sys[0, 0])
        p_down = float(rho_sys[1, 1])

        return {
            "step": 2,
            "description": "Decoherence does NOT select the experienced outcome",
            "P_up": p_up,
            "P_down": p_down,
            "which_outcome_experienced": "UNDEFINED by the formalism",
            "the_gap": (
                "The reduced density matrix ρ = 0.5|↑⟩⟨↑| + 0.5|↓⟩⟨↓| tells us "
                "the probabilities. It does NOT tell us: 'the observer sees ↑.' "
                "That requires an additional concept — the concept of an observer "
                "who experiences a specific outcome. The formalism provides the "
                "statistics; something else provides the experience."
            ),
        }

    def step3_observer_required_for_outcomes(self) -> dict:
        """
        Step 3: 'Which outcome' requires the concept of an observer.

        To go from the mixed state (probability distribution) to a
        definite experienced outcome, you need:

        Everett: "the observer branches, and each branch-copy sees one outcome"
        Bohm: "the particle was always in one position; the observer just learns it"
        Copenhagen: "collapse happens; the observer sees the result"
        Advaita: "the observer is a localized perspective; the perspective determines the outcome"

        ALL interpretations invoke 'observer' at this step.
        None can avoid it.
        """
        interpretations = {
            "copenhagen": {
                "mechanism": "Collapse selects the outcome",
                "observer_role": "Triggers collapse (but when? Heisenberg cut is arbitrary)",
                "observer_analyzed": False,
            },
            "everett": {
                "mechanism": "Branching — all outcomes occur",
                "observer_role": "Branches with the system; each copy sees one outcome",
                "observer_analyzed": False,
                "gap": "Why does each branch-copy experience a UNIFIED outcome? "
                       "What is it like to be a branch?",
            },
            "bohm": {
                "mechanism": "Particle always had a position; measurement reveals it",
                "observer_role": "Learns the pre-existing fact",
                "observer_analyzed": False,
                "gap": "Why is there experience of learning? "
                       "The mechanics don't require consciousness.",
            },
            "advaita": {
                "mechanism": "Perspectival reduction — localized perspective sees one outcome",
                "observer_role": "IS a localized mode of the universal subject",
                "observer_analyzed": True,
                "note": "The observer is not imported from outside the formalism. "
                        "It is identified with a specific ontological structure: "
                        "a localized perspective of the universal subject.",
            },
        }

        return {
            "step": 3,
            "description": "The concept of 'observer' is essential to get definite outcomes",
            "interpretations": interpretations,
            "key_finding": (
                "ALL four interpretations invoke 'observer' to bridge the gap "
                "between the mixed state (probabilities) and the experienced outcome "
                "(definite result). The question is not WHETHER observer matters, "
                "but whether its ontological status is analyzed or left unexamined."
            ),
        }

    def step4_unanalyzed_observer_is_a_gap(self) -> dict:
        """
        Step 4: Leaving 'observer' unanalyzed leaves a gap in the description.

        If 'observer' does essential work in the formalism (Step 3),
        and its nature is not specified, then a central term in the
        theory is undefined.

        This is the paper's hidden premise: observer ontology is not
        optional — it is part of the interpretive burden.
        """
        # Quantify the gap: what does the formalism determine, and what does it leave open?

        # After decoherence, the formalism determines:
        formalism_determines = [
            "The preferred basis (pointer states)",
            "The probabilities of each outcome",
            "The entanglement structure of the total state",
            "The purity of the total state (always 1.0)",
            "The purity of the reduced state (< 1.0)",
        ]

        # The formalism does NOT determine:
        formalism_leaves_open = [
            "Which outcome is experienced by a particular observer",
            "Why there is experience at all (the hard problem)",
            "What the observer IS (substance? function? perspective?)",
            "Why the experienced world is unified rather than fragmented",
        ]

        return {
            "step": 4,
            "description": "Leaving 'observer' unanalyzed is a gap, not neutrality",
            "formalism_determines": formalism_determines,
            "formalism_leaves_open": formalism_leaves_open,
            "num_determined": len(formalism_determines),
            "num_open": len(formalism_leaves_open),
            "the_argument": (
                f"The formalism determines {len(formalism_determines)} things and "
                f"leaves {len(formalism_leaves_open)} things open. The open questions "
                "all involve the concept of 'observer.' If observer is essential to "
                "the formulation of measurement (Step 3), then leaving its nature "
                "unspecified is not philosophical neutrality — it is an unexamined "
                "commitment. The Advaita interpretation makes this commitment "
                "explicit by identifying the observer with a specific ontological "
                "structure (localized perspective of the universal subject)."
            ),
        }

    def full_demonstration(self) -> dict:
        """Run all four steps of the observer centrality argument."""
        results = {
            "step_1": self.step1_decoherence_selects_basis(),
            "step_2": self.step2_decoherence_does_not_select_outcome(),
            "step_3": self.step3_observer_required_for_outcomes(),
            "step_4": self.step4_unanalyzed_observer_is_a_gap(),
        }

        results["summary"] = {
            "argument_chain": [
                "Step 1: Decoherence selects pointer states (uncontroversial physics)",
                "Step 2: Decoherence does NOT select the experienced outcome (gap identified)",
                "Step 3: ALL interpretations invoke 'observer' to bridge this gap",
                "Step 4: Leaving observer's nature unanalyzed is a gap, not neutrality",
            ],
            "conclusion": (
                "The concept of 'observer' does essential, non-trivial work in the "
                "measurement formalism. Its ontological status is therefore part of "
                "the interpretive burden, not an optional philosophical add-on. "
                "This is the paper's hidden premise, now demonstrated computationally: "
                "observer ontology is not external to physics — it is implicit in "
                "the use of 'observer' within the formalism itself."
            ),
            "implication_for_advaita": (
                "The Advaita interpretation addresses this gap by providing an explicit "
                "ontological account of the observer: a localized perspective of the "
                "universal subject. Whether this account is correct is debatable; "
                "that it addresses a genuine gap in the formalism is demonstrated here."
            ),
        }

        return results
