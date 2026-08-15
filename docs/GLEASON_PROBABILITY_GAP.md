# The Gleason–Probability Gap: A Technical Note

**Supplementary to**: *A Non-Dual Interpretation of Quantum Mechanics: Consciousness as Ontological Primitive* (Chauhan, 2026)

**Status**: Technical note. Engages referee-anticipated objections to the paper's use of Gleason's theorem as the source of the Born rule. The paper's §3.3 notes that Gleason is used by Everettians and QBists alike; this note closes the engagement with Kent (2010) and Baker (2007), who have argued that Gleason-based derivations do not in fact ground *probability*.

---

## 1. The Measure vs. Probability Distinction

Gleason's theorem (Gleason, 1957) establishes:

> In a separable Hilbert space $H$ with $\dim H \geq 3$, any non-negative, normalized, countably additive measure $\mu$ on the closed subspaces of $H$ is of the form $\mu(P) = \mathrm{Tr}(\rho P)$ for some density operator $\rho$.

The theorem is a mathematical fact about measures on lattices of subspaces. It says: *if* you want a real-valued function on projectors that behaves like a measure (non-negative, additive on orthogonal projectors, normalized to $1$), it *must* take the $\mathrm{Tr}(\rho P)$ form.

What Gleason does not establish:

- That such a measure *exists* as a matter of physical fact.
- That this measure represents *probability* in any of the senses probability is normally used (frequency, credence, propensity).
- That an agent should set their *credences* according to this measure.
- That the long-run *frequency* of measurement outcomes will track this measure.

In short: Gleason fixes the *form* of a probability-like object given the Hilbert space structure, but the identification of this object with probability in a physically meaningful sense is an additional step.

This is the "probability gap." It is the opening that Kent (2010) and Baker (2007) exploit when arguing that Everettian and QBist uses of Gleason do not actually solve the Born-rule problem.

---

## 2. Kent's Critique (2010)

Kent's argument against Everettian Gleason-based derivations runs as follows:

1. In Everett, every outcome occurs in some branch. There is no objective chance of any single outcome failing to occur.
2. Hence there is no *single-case probability* in the ordinary sense (propensity or chance) associated with measurement.
3. What we call "probability" in Everett must therefore be reduced either to (i) subjective credence of an agent about which branch they are in (self-locating uncertainty), or (ii) a rational betting rule (decision theory).
4. The Deutsch–Wallace decision-theoretic derivation (Deutsch, 1999; Wallace, 2012) aims to show that a rational agent must bet according to $|\langle n|\psi\rangle|^2$.
5. Kent argues: the derivation either (a) assumes substantive principles equivalent to Born, or (b) leaves agents free to bet on any coherent measure, including non-Born ones, since in Everett every outcome occurs and no rational pressure selects Born uniquely.

For our purposes, the critical point is (5). Kent does not dispute Gleason. He disputes that Gleason plus Everettian ontology yields probability.

The critique can be summarized as:

> Gleason tells you the *mathematical form* of any additive measure. It does not tell you *which* such measure corresponds to the frequencies you will experience, nor *why* you should bet according to it. In a universe where every outcome occurs, the link between mathematical measure and experienced frequency is what needs explaining, and Gleason does not supply it.

---

## 3. Baker's Critique (2007)

Baker's argument is more internal: he examines the Deutsch–Wallace derivation step by step and argues that circularity enters at multiple points. In particular:

- The rationality postulates invoked in the derivation (transitivity, dominance, continuity) make use of equivalences between branches that are already amplitude-weighted.
- The symmetry arguments (e.g., that branches with equal amplitudes should be treated symmetrically) presuppose that amplitude is the relevant equivalence relation — which is the Born-rule assumption in disguise.
- Dropping Born-like assumptions breaks the derivation.

Baker concludes that decision-theoretic derivations of the Born rule in Everett do not provide an *independent* justification of $|\langle n|\psi\rangle|^2$: they recover it from premises that are equivalent to it.

The combined effect of Kent and Baker: even granting Gleason, the Everettian does not have a non-circular account of why the measure $\mathrm{Tr}(\rho P)$ should be interpreted as probability at all.

---

## 4. How the Paper's Framework Is Affected

The paper's §3.3 observes that Gleason gives the Born rule and that this is a move shared with Everett and QBism. It does not address Kent or Baker. A referee sympathetic to either will ask:

> If Everettian Gleason-based derivations are circular or incomplete, why isn't your use of Gleason equally affected? You share the formalism. What changes with the consciousness-primitive ontology?

This note's purpose is to state clearly what changes — and what does not.

### 4.1 What Does Not Change

The mathematical content of Gleason is exactly as in Everett and QBism. Nothing in the paper's ontology modifies what Gleason proves. The *measure* $\mathrm{Tr}(\rho P)$ is fixed by the Hilbert space structure alone.

The paper therefore inherits any gaps in the Everettian use of Gleason that are purely mathematical. If Gleason by itself is insufficient to ground probability, then Gleason by itself is insufficient to ground probability in our framework too.

### 4.2 What Changes

What changes is the interpretation of "probability." Specifically, *what it is a probability of*.

In Everett, the interpretive target is either:

- **Propensity-style:** probability that a single outcome will occur (fails because all outcomes occur).
- **Self-locating uncertainty:** probability that an agent is in a particular branch (Vaidman, 1998; Sebens and Carroll, 2018) — which requires an account of pre-measurement agents identifying with post-measurement branches.
- **Decision-theoretic:** probability as a rational betting weight (Deutsch–Wallace) — attacked by Kent and Baker.

In the consciousness-primitive framework, the interpretive target is different: **the measure $\mathrm{Tr}(\rho P)$ describes the relative weight of modes of self-relation of a single universal subject**. The "probability of outcome $n$" is not the chance that outcome $n$ rather than some other occurs — the total state remains pure and contains all outcomes. It is the *measure-theoretic weight* of the perspective in which outcome $n$ is the reduced-state appearance.

This has three consequences for the Kent/Baker critique.

**(a) The single-case propensity problem is avoided at its root.** In Everett, Kent's complaint is that every outcome occurs, so there is no chance of non-occurrence. In our framework, every outcome is likewise realized in the total state — but we do not claim propensity. We claim a *weight* on perspectives. The question "with what probability does outcome $n$ occur?" is replaced by "with what measure-theoretic weight is the perspective-$n$ mode realized in the subject?" The latter is a structural question with a Gleason-fixed answer, not a frequency claim requiring independent justification.

**(b) The self-locating-uncertainty regress is not triggered.** In Everett, identifying the pre-measurement agent with a particular post-measurement branch is a substantive and contested move (Wallace, 2012, Ch. 7; critics include Kent, 2015). Our framework does not need this move: perspectives are not post-measurement *copies* of a pre-measurement agent. They are modes of one subject, indexed structurally rather than historically. The pre/post identity problem does not arise because there is no branching identity to track — there is one subject with modes, not many agents to distinguish.

**(c) The decision-theoretic derivation is not needed.** We do not claim that rational agents must bet according to $|\langle n|\psi\rangle|^2$ as the *justification* of the Born rule. Instead, we claim that the measure is a structural feature of the universal subject, and observed frequencies in any localized perspective must track this measure because the perspective itself is defined as a reduction of the global structure. Rational betting behavior, if it follows Born, does so because the agent's credences are constrained by the structure of the perspective they inhabit — not because a decision-theoretic theorem forces them to.

### 4.3 The Residual Gap

None of this eliminates the gap entirely. It relocates it. In our framework, the unanswered question becomes:

> Why does the universal subject have Hilbert space structure, such that its natural measure is $\mathrm{Tr}(\rho P)$?

This is a structural question about the subject's ontology, not a frequency question about outcomes. Following the paper's §3.8, we treat this as *intra-categorial* — a question about the internal structure of a single kind of thing — rather than *cross-categorial*, a question about a bridge between kinds. Intra-categorial questions are the normal business of foundational physics ("why does spacetime have a Lorentzian metric?"), and we do not claim to answer this one.

Honestly stated: we have not derived probability from consciousness. We have *defined* what probability means in the consciousness-primitive ontology in a way that avoids the specific regresses Kent and Baker identify in Everett. Whether that redefinition counts as progress depends on whether one accepts that the question "what is probability *of*?" has a different natural answer when the ontology is non-dual.

---

## 5. Comparison Table

| Interpretation | What Gleason gives | What "probability" means | Vulnerability to Kent/Baker |
|----------------|---------------------|---------------------------|------------------------------|
| Copenhagen | Not invoked (Born is axiomatic) | Chance of collapse to outcome $n$ | N/A — Born is a postulate |
| Everett (Deutsch–Wallace) | Measure $\mathrm{Tr}(\rho P)$ | Rational betting weight | **High** — Kent and Baker argue circularity |
| Everett (Self-locating) | Measure $\mathrm{Tr}(\rho P)$ | Agent's uncertainty about branch | **Moderate** — requires pre/post identity |
| QBism | Measure $\mathrm{Tr}(\rho P)$ | Agent's personal credence | **Low technical** but anti-realist |
| **Consciousness-primitive** | Measure $\mathrm{Tr}(\rho P)$ | Structural weight on modes of subject | **Low** — but gap relocated to ontology |

---

## 6. Relation to the Repository

The repository module `quantum/gleason.py` verifies Gleason's conditions numerically for the Brahman Hilbert space ($\dim \geq 3$), tests non-Born measures for contradictions, and demonstrates that no other rule is consistent. It does not address the probability-gap question — that is the role of this note.

The repository modules `quantum/interpretations.py`, `quantum/operational_equivalence.py`, and `quantum/perspectival_asymmetry.py` compare the four interpretations across phenomena, verify operational equivalence with Everett on feasible experiments, and demonstrate that perspectival reduction is exact to machine precision. Together with this note, they constitute the technical basis of the paper's §3.3 and §4.3 claims.

---

## 7. What This Note Does and Does Not Claim

**Claims:**
- The probability gap identified by Kent (2010) and Baker (2007) is a real gap in Everettian uses of Gleason.
- The paper's framework does not inherit that gap in the same form because it does not interpret the measure as single-case propensity, branch-locating uncertainty, or rational betting weight.
- The framework's interpretation of the measure — as structural weight on modes of a single subject — is consistent with Gleason without requiring the disputed Everettian moves.

**Does not claim:**
- That probability has been derived from consciousness.
- That the measure's role as a weight on modes is itself uncontroversial. (A referee may ask: what licenses calling modes "weighted"? We accept this is a commitment, not a theorem.)
- That all philosophical critiques of Gleason-based probability have been answered. (The note engages Kent and Baker specifically; other critics — e.g., Saunders (2010), Greaves (2004) — are not addressed here.)

---

## References

Baker, D. (2007). Measurement outcomes and probability in Everettian quantum mechanics. *Studies in History and Philosophy of Modern Physics*, 38, 153–169.

Chauhan, R. (2026). The cardinality of experience is underdetermined by the quantum state: A constructive case for a consciousness-primitive interpretation. Preprint, Zenodo. https://doi.org/10.5281/zenodo.21007975 (earlier drafts circulated as "A non-dual interpretation of quantum mechanics: Consciousness as ontological primitive").

Deutsch, D. (1999). Quantum theory of probability and decisions. *Proceedings of the Royal Society A*, 455, 3129–3137.

Gleason, A. M. (1957). Measures on the closed subspaces of a Hilbert space. *Journal of Mathematics and Mechanics*, 6, 885–893.

Greaves, H. (2004). Understanding Deutsch's probability in a deterministic multiverse. *Studies in History and Philosophy of Modern Physics*, 35, 423–456.

Kent, A. (2010). One world versus many: The inadequacy of Everettian accounts of evolution, probability, and scientific confirmation. In S. Saunders, J. Barrett, A. Kent, & D. Wallace (Eds.), *Many Worlds? Everett, Quantum Theory, and Reality*. Oxford University Press.

Kent, A. (2015). Does it make sense to speak of self-locating uncertainty in the universal wave function? Remarks on Sebens and Carroll. *Foundations of Physics*, 45, 211–217.

Saunders, S. (2010). Chance in the Everett interpretation. In S. Saunders et al. (Eds.), *Many Worlds?* Oxford University Press.

Sebens, C., & Carroll, S. (2018). Self-locating uncertainty and the origin of probability in Everettian quantum mechanics. *British Journal for the Philosophy of Science*, 69, 25–74.

Vaidman, L. (1998). On schizophrenic experiences of the neutron, or why we should believe in the many-worlds interpretation. *International Studies in the Philosophy of Science*, 12, 245–261.

Wallace, D. (2012). *The Emergent Multiverse: Quantum Theory According to the Everett Interpretation*. Oxford University Press.
