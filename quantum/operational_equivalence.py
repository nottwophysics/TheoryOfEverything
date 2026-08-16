"""
Everett–Advaita operational equivalence — an ANALYTIC point, not a test.

The accompanying paper states that this interpretation is empirically
equivalent to Everett.  That claim is *analytic*, and this module does not
test it, because there is nothing to test:

    Both readings use the same Hilbert space, the same unitary dynamics, the
    same Born rule and the same decoherence.  There is ONE calculation.
    "Everett" and "Advaita" are two readings of what that calculation is
    ABOUT.  Identical predictions therefore follow by construction, and no
    computation could show otherwise.

Equivalently: the equivalence is secured by the no-collapse dynamics (axiom
A3), which both readings share — not by anything specific to either.  What
this module does is compute the shared quantities once, and set out the
ontological divergences that carry no measurable consequence.

HISTORY (2026-08-16 adversarial review).  Until this rewrite the module
claimed to "PROVE that claim computationally by running identical quantum
scenarios under both interpretations".  It did not.  Every "test" built one
array and copied it twice --

    everett_probs = probs.copy()
    advaita_probs = probs.copy()

-- so the reported difference was identically zero for any input; the
measurement-statistics "test" reset the same RNG seed before each draw;
two tests returned a hardcoded ``"numbers_identical": True``; the
divergence tallies (5 ontological, 0 measurable) were integer literals equal
to the length of a hand-written dict; and the summary flag was computed as

    all(d.get("identical", True) or d.get("all_identical", True)
        or d.get("numbers_identical", True) for d in ...)

in which each sub-result carries only ONE of those three keys, so the two
absent ones defaulted to True and the disjunction short-circuited -- the flag
was True for every possible input, including one where every test failed.
There was no Everettian computation anywhere in the tree: no branch
decomposition, no Deutsch–Wallace step.  The scoreboard is deleted rather
than repaired, because the honest version of the claim is one sentence and
needs no arithmetic.
"""

import numpy as np
from scipy.linalg import expm


class OperationalEquivalence:
    """
    Computes the quantities Everett and this interpretation SHARE, once.

    No method here compares two arms, because there is only one arm.  The
    two readings differ in what they say the numbers are about; that is
    catalogued in :meth:`ontological_divergences`.
    """

    def __init__(self, dimension: int = 4, seed: int = 42):
        self.dim = dimension
        self.seed = seed
        np.random.seed(seed)

        # A random Hamiltonian and initial state. Shared physics: there is no
        # "Everettian" or "Advaitic" version of either.
        A = np.random.randn(dimension, dimension) + 1j * np.random.randn(dimension, dimension)
        self.H = (A + A.conj().T) / 2

        psi = np.random.randn(dimension) + 1j * np.random.randn(dimension)
        self.initial_state = psi / np.linalg.norm(psi)

    # ---- shared machinery -------------------------------------------------

    def _evolve(self, state: np.ndarray, time: float) -> np.ndarray:
        """Unitary time evolution."""
        U = expm(-1j * self.H * time)
        return U @ state

    def _born_probabilities(self, state: np.ndarray) -> np.ndarray:
        return np.abs(state) ** 2

    def _density_matrix(self, state: np.ndarray) -> np.ndarray:
        return np.outer(state, state.conj())

    def _partial_trace(self, rho: np.ndarray, dim_a: int, dim_b: int) -> np.ndarray:
        rho_reshaped = rho.reshape(dim_a, dim_b, dim_a, dim_b)
        return np.trace(rho_reshaped, axis1=1, axis2=3)

    def _von_neumann_entropy(self, rho: np.ndarray) -> float:
        eigenvalues = np.real(np.linalg.eigvalsh(rho))
        eigenvalues = eigenvalues[eigenvalues > 1e-15]
        eigenvalues = eigenvalues / np.sum(eigenvalues)
        return float(-np.sum(eigenvalues * np.log(eigenvalues + 1e-15)))

    # ---- the shared quantities, each computed once ------------------------

    def shared_born_probabilities(self) -> dict:
        """Born-rule probabilities. One computation; two justifications."""
        probs = self._born_probabilities(self.initial_state)
        return {
            "quantity": "Born rule probabilities",
            "probabilities": probs.tolist(),
            "everett_justification": "Deutsch–Wallace decision-theoretic argument",
            "advaita_justification": "Gleason's theorem given the Hilbert-space structure",
            "note": "Same formula |<n|psi>|^2. The readings differ over why the "
                    "measure is the right one, not over its value.",
        }

    def shared_time_evolution(self) -> dict:
        """Unitary evolution at several times. One trajectory."""
        times = [0.0, 0.5, 1.0, 2.0, 5.0]
        steps = []
        for t in times:
            evolved = self._evolve(self.initial_state, t)
            steps.append({
                "time": t,
                "norm": float(np.linalg.norm(evolved)),
                "probabilities": self._born_probabilities(evolved).tolist(),
            })
        return {
            "quantity": "Unitary time evolution",
            "time_steps": steps,
            "everett_reading": "the wave function IS reality, evolving",
            "advaita_reading": "the universal subject's structure evolves",
            "note": "One Schrodinger equation. No second trajectory exists to compare against.",
        }

    def shared_measurement_statistics(self, num_trials: int = 10000) -> dict:
        """Sampled outcome frequencies from the shared Born distribution."""
        state = self._evolve(self.initial_state, 1.0)
        probs = self._born_probabilities(state)
        probs = probs / np.sum(probs)

        rng = np.random.default_rng(self.seed)
        outcomes = rng.choice(self.dim, size=num_trials, p=probs)
        freq = np.bincount(outcomes, minlength=self.dim) / num_trials

        return {
            "quantity": "Measurement statistics",
            "num_trials": num_trials,
            "born_probabilities": probs.tolist(),
            "sampled_frequencies": freq.tolist(),
            "max_sampling_deviation": float(np.max(np.abs(freq - probs))),
            "note": "Frequencies are sampled from the shared Born distribution and "
                    "converge to it. The readings differ over what an outcome IS "
                    "(a branch, or a perspective's content), not over its frequency.",
        }

    def shared_entanglement_correlations(self) -> dict:
        """Bell-state entropy (computed) and the CHSH value (analytic)."""
        bell = np.zeros(4, dtype=np.complex128)
        bell[0] = 1 / np.sqrt(2)
        bell[3] = 1 / np.sqrt(2)

        rho_A = self._partial_trace(self._density_matrix(bell), 2, 2)
        S = self._von_neumann_entropy(rho_A)

        # CHSH for the Bell state, evaluated analytically from the angles.
        # NOTE: this expression does not consume `bell`; it is the textbook
        # value for that state, not a measurement of the array above. The
        # entanglement entropy S, by contrast, IS computed from the state.
        a1, a2 = 0, np.pi / 4
        b1, b2 = np.pi / 8, 3 * np.pi / 8
        E = lambda a, b: -np.cos(2 * (a - b))
        chsh = E(a1, b1) - E(a1, b2) + E(a2, b1) + E(a2, b2)

        return {
            "quantity": "Entanglement correlations",
            "entanglement_entropy_computed_from_state": float(S),
            "chsh_value_analytic": float(chsh),
            "chsh_is_analytic_not_measured": True,
            "everett_reading": "both branches exist; correlations reflect the structure of the universal psi",
            "advaita_reading": "one subject, two perspectives; correlations reflect non-separability",
            "note": "The readings differ over what non-locality MEANS, not over what "
                    "it predicts. See quantum/entanglement.py for the state-consuming "
                    "CHSH evaluation with its separable/singlet controls.",
        }

    def shared_decoherence(self) -> dict:
        """System-environment entangling; pure total, mixed reduced."""
        sys_state = np.array([1, 1], dtype=np.complex128) / np.sqrt(2)
        env_dim = 8

        total_post = np.zeros(2 * env_dim, dtype=np.complex128)
        total_post[0] = sys_state[0]
        total_post[env_dim + 1] = sys_state[1]
        total_post /= np.linalg.norm(total_post)

        rho_total = self._density_matrix(total_post)
        purity_total = float(np.real(np.trace(rho_total @ rho_total)))

        rho_sys = self._partial_trace(rho_total, 2, env_dim)
        purity_reduced = float(np.real(np.trace(rho_sys @ rho_sys)))
        coherence = float(np.sum(np.abs(rho_sys - np.diag(np.diag(rho_sys)))))

        return {
            "quantity": "Decoherence",
            "total_state_purity": purity_total,
            "reduced_state_purity": purity_reduced,
            "coherence_remaining": coherence,
            "appears_classical": coherence < 0.01,
            "everett_reading": "branch structure emerges; the observer is in one branch",
            "advaita_reading": "perspectival reduction; the observer is one localized "
                               "perspective of the universal subject",
            "note": "Pure total state, mixed reduced state. This is a theorem of the "
                    "formalism and is agreed by every no-collapse interpretation, so "
                    "it cannot favour one reading over another.",
        }

    # ---- where they actually differ ---------------------------------------

    def ontological_divergences(self) -> dict:
        """
        The differences between the two readings. None is measurable.

        This is a hand-written catalogue of positions, not a computation, and
        it is not counted or scored: the number of rows reflects how the table
        was written, not a fact about the interpretations.
        """
        return {
            "quantity": "Ontological divergences (not measurable; hand-written catalogue)",
            "is_a_computation": False,
            "divergences": {
                "what_exists": {
                    "everett": "The universal wave function — a mathematical object in Hilbert space",
                    "advaita": "A universal conscious subject, whose self-relational structure is |psi>",
                    "measurable_difference": None,
                },
                "what_branches_are": {
                    "everett": "Equally real, independently existing worlds",
                    "advaita": "Modes of self-relation of one subject — perspectives, not worlds",
                    "measurable_difference": None,
                },
                "what_observer_is": {
                    "everett": "A functional subsystem that branches with the wave function",
                    "advaita": "A localized perspective of the universal subject",
                    "measurable_difference": None,
                },
                "why_experience_exists": {
                    "everett": "Not addressed (experience assumed functional/computational)",
                    "advaita": "Experience is intrinsic to the primitive",
                    "measurable_difference": None,
                },
                "status_of_hard_problem": {
                    "everett": "Outside scope — physics need not explain consciousness",
                    "advaita": "Reframed — cross-categorial gap becomes an intra-categorial question",
                    "measurable_difference": None,
                },
            },
            "conclusion": (
                "Every divergence is about what the formalism MEANS, not about what it "
                "PREDICTS. The case for either reading rests on conceptual grounds."
            ),
        }

    def full_report(self) -> dict:
        """
        The shared quantities plus the ontological catalogue.

        Deliberately returns no pass/fail flag, no count of 'tests passed' and
        no tally of divergences: operational equivalence is analytic, so there
        is no verdict for this module to reach.
        """
        return {
            "equivalence_status": (
                "ANALYTIC, not tested. Both readings share the Hilbert space, the "
                "unitary dynamics, the Born rule and decoherence, so their predictions "
                "coincide by construction. The equivalence is secured by the no-collapse "
                "dynamics both adopt, not by either reading's distinctive commitments."
            ),
            "shared_quantities": {
                "probabilities": self.shared_born_probabilities(),
                "time_evolution": self.shared_time_evolution(),
                "measurement_statistics": self.shared_measurement_statistics(),
                "entanglement": self.shared_entanglement_correlations(),
                "decoherence": self.shared_decoherence(),
            },
            "divergences": self.ontological_divergences(),
        }
