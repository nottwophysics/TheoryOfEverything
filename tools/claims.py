"""
Claims manifest — one source of truth per headline number, and the register of
claims this project has retired.

Read by tools/check_claims.py, which runs in CI. Two failure modes it exists to
stop, both of which have actually happened here:

  1. A number quoted in eight documents drifts when the code changes. Test
     counts alone were hand-propagated five times in a single day.
  2. A retired claim survives as a PARAPHRASE two paragraphs from its own
     refutation, because the retirement was recorded as a phrase and then
     hunted as that phrase.

It also checks the direction that keeps being missed: a CORRECTION can itself go
stale. "does NOT recover Newton" was true when written and false three commits
later, and a stale correction is as false as a stale overclaim.

Deliberately a Python module rather than YAML. A hand-rolled parser for a config
that guards against silent drift would be the one component able to fail
silently and return a false all-clear; and adding a YAML dependency to CI to
read seventy lines is not worth it. Here there is no parser.
"""

# ---------------------------------------------------------------------------
# Live counts: measured, never transcribed. `check_claims.py --fix` rewrites
# every occurrence from the measurement.
# ---------------------------------------------------------------------------
COUNTS = [
    {
        "name": "test_total",
        "producer": "pytest --collect-only -q",
        # Anchored deliberately. A bare r"(\d+) tests" also matches per-file
        # counts ("20 tests") and dated snapshots ("237 tests"), which are
        # legitimately different numbers -- a checker that flags those trains
        # you to ignore it.
        "patterns": [
            r"test suite \((?P<v>\d+) tests\)",
            r"(?P<v>\d+) automated tests",
            r"— (?P<v>\d+) Automated Tests",
            r"TEST SUITE: (?P<v>\d+)",
            r"suite is (?P<v>\d+)",
            r"pytest tests/ -v\s+# Run all (?P<v>\d+) tests",
            r"\((?P<v>\d+) collected\)",
            r"(?P<v>\d+) tests across",
        ],
    },
    {
        "name": "test_files",
        "producer": "ls tests/test_*.py",
        "patterns": [r"across (?P<v>\d+) test files"],
    },
    {
        "name": "experiments",
        "producer": "main.py experiments_map",
        "patterns": [
            r"(?P<v>\d+) runnable experiments",
            r"All (?P<v>\d+) Experiments",
        ],
    },
]

# ---------------------------------------------------------------------------
# Derived numbers: produced by a script, quoted in prose. The check re-runs the
# producer and compares against what the manifest pins.
# ---------------------------------------------------------------------------
DERIVED = [
    {"name": "phi_s_systems",    "producer": "phi_s_verdict", "key": "n_systems",        "pinned": 216},
    {"name": "phi_s_nonzero",    "producer": "phi_s_verdict", "key": "n_phi_nonzero",    "pinned": 51},
    {"name": "phi_s_violations", "producer": "phi_s_verdict", "key": "violations",       "pinned": 50},
    {"name": "phi_s_max_phi",    "producer": "phi_s_verdict", "key": "max_phi_bits",     "pinned": 4.012},
    {"name": "phi_s_max_S",      "producer": "phi_s_verdict", "key": "max_S_bits",       "pinned": 0.833},
    {"name": "phi_s_pearson",    "producer": "phi_s_verdict", "key": "pearson_r_phi_s",  "pinned": 0.643},
]

# ---------------------------------------------------------------------------
# Retired claims. `banned` is how it was written; `paraphrases` is how someone
# would say it WITHOUT the banned words -- which is where survivals actually
# hide. Both stale overclaims and stale corrections live here.
# ---------------------------------------------------------------------------
RETIRED = [
    {
        "name": "phi_le_S_holds",
        "why": "Falsified by the project's own validated PyPhi retest (2026-07-15); "
               "numbers corrected by the 2026-08-12 ordering audit.",
        "banned": [r"conjecture holds 100%", r"holds without violation"],
        "paraphrases": [
            r"sets a lower bound on its quantum entanglement",
            r"consciousness is bounded by (quantum )?entanglement",
            r"[Pp]hi cannot exceed",
            r"capped by the bipartition",
            r"maximum consciousness = maximum entanglement",
        ],
    },
    {
        "name": "phi_s_pre_audit_numbers",
        "why": "Superseded by the 2026-08-12 TPM-ordering audit; these are the "
               "big-endian generation still carried by the published v2.",
        "banned": [r"every one of the 23", r"apparent 89% satisfaction"],
        "paraphrases": [r"all 23 systems with nonzero"],
    },
    {
        "name": "newton_non_recovery",
        "why": "STALE CORRECTION. gravity/entropic.py was reimplemented 2026-08-15 "
               "and DOES recover GMm/r^2; tests/test_gravity.py asserts it.",
        "banned": [r"honest Newton NON-recovery", r"does NOT recover Newton"],
        "paraphrases": [r"fails to recover the inverse-square"],
    },
    {
        "name": "bell_no_state_consumed",
        "why": "STALE CORRECTION. quantum/entanglement.py was rewritten 2026-08-15 to "
               "consume its input state; its docstring says the caveat must be retired.",
        "banned": [r"consumes no quantum state", r"no quantum state consumed"],
        "paraphrases": [r"a separable state would score identically"],
    },
    {
        "name": "mera_inert",
        "why": "STALE CORRECTION. The MERA was reimplemented 2026-08-15; its tensors "
               "are contracted and perturbing a layer moves the state.",
        "banned": [r"MERA is a no-op"],
        "paraphrases": [r"zeroed tensors produce identical output"],
    },
    {
        "name": "scoreboards",
        "why": "Experiment 17/24 scoreboards deleted 2026-08-16: every figure was "
               "len() of a list written inside the module.",
        "banned": [r"5/5 tests identical", r"5/5 empirical tests identical",
                   r"0 measurable divergences", r"ranking_by_parsimony",
                   r"full_equivalence_test"],
        "paraphrases": [r"uniquely the only interpretation that addresses",
                        r"0 unresolved phenomena"],
    },
    {
        "name": "cohens_d_68",
        "why": "Sample-count artifact; grows without bound in n_samples. Retracted "
               "and must not be cited as an effect size.",
        "banned": [r"\+68\.5"],
        "paraphrases": [r"effect size of 68"],
    },
    {
        "name": "bell_sign_and_analytic",
        "why": "quantum/entanglement.py consumes its state since 2026-08-15. The "
               "caveat is false, and the sign was wrong: |Phi+> gives +2sqrt(2), "
               "the singlet gives -2sqrt(2).",
        "banned": [r"S = -2\.82", r"S = -2\.83", r"CHSH S = -2\.8",
                   r"-2\.828 \(= -2√2\)"],
        "paraphrases": [r"analytic textbook value; the demo consumes"],
    },
    {
        "name": "er_epr_confirmed",
        "why": "The throat-entropy relation is imposed by assignment in the demo, "
               "not derived; Experiment 28 is illustrative.",
        "banned": [r"ER = EPR confirmed", r"Wormholes ARE entanglement",
                   r"Completes Path 2"],
        "paraphrases": [],
    },
    {
        "name": "bulk_derived_from_boundary",
        "why": "Reconstruction fidelity is ~0.4976 (chance) and bulk_from_boundary "
               "is False; 'boundary is fundamental' is an interpretive reading.",
        "banned": [r"bulk \(empirical world with gravity\) is derived from the boundary"],
        "paraphrases": [],
    },
    {
        "name": "rt_correlation_094_as_result",
        "why": "Circular by construction: the entropy is defined proportional to "
               "T_00 and the correlated curvature is a smoothed copy of it. The "
               "genuine Regge deficit-angle curvature ANTI-correlates.",
        "banned": [r"\*\*Key result\*\*: R_entropy vs T_00 correlation"],
        "paraphrases": [],
    },
    {
        "name": "einstein_3d_headline",
        "why": "Withdrawn by the 2026-08-15 review; no metric, connection, Ricci or "
               "Einstein tensor is formed and the construction is a static point cloud.",
        "banned": [],
        "paraphrases": [r"in the correct number of spatial dimensions"],
    },
    {
        "name": "axiom_reduction_proven",
        "why": "Gleason's theorem is established mathematics and is illustrated "
               "faithfully; the 7->4 COUNT is arithmetic on hand-entered "
               "enumerations, as the module states at runtime. Not a theorem.",
        "banned": [r"\*\*PROVEN\*\* \| Mathematical fact",
                   r"first mathematically rigorous result"],
        "paraphrases": [r"axiom reduction[^.]{0,40}is a concrete result",
                        r"This is not a philosophical argument"],
    },
    {
        "name": "p5_excluded",
        "why": "Exclusion at a stated amplitude needs a comparison against the "
               "Holometer's published sensitivity. That comparison is not in "
               "the repo and the experimental paper is uncited. Downgraded to "
               "'constrained' 2026-08-16.",
        "banned": [r"EXCLUDED at the stated amplitude",
                   r"Excluded at the Hogan-scale amplitude",
                   r"Excluded at the predicted amplitude"],
        "paraphrases": [r"holographic noise was \*\*excluded\*\*"],
    },
    {
        "name": "five_novel_predictions",
        "why": "None of P1-P5 is entailed by A1-A4; each belongs to another "
               "programme and is consistent with the thesis's negation. "
               "Reclassified 2026-08-16 as compatible programmes.",
        "banned": [r"5 Testable Predictions",
                   r"Novel predictions that distinguish the consciousness-first"],
        "paraphrases": [r"The framework states \*\*5 predictions\*\*",
                        r"makes 5 (novel|testable) predictions"],
    },
]

# A paragraph containing any of these is exempt: it is a note recording a
# retirement, and naming the retired claim is how a retraction works.
# `claims-ok` is the explicit escape hatch for anything these miss.
EXEMPT_MARKERS = [
    "retracted", "retired", "withdrawn", "superseded", "deleted", "falsified",
    "no longer", "must not be cited", "stale", "previously", "used to",
    "historical", "correction", "does not replicate", "was found",
    "until 2026", "deprecated", "claims-ok",
    # Added after the first real run: a paragraph that REFUTES a claim, or
    # quotes it to contrast against, necessarily names it.
    "refut", "opposite of", "is false", "does not hold", "violates",
    # Added after the first run against the PRIVATE line, whose review docs
    # quote the old wording in order to recommend replacing it. Quoting a claim
    # to say "replace this" is not asserting it.
    "should be replaced", "current wording", "what the paper says",
    "recommend", "off-message",
    # "Formerly X" / "reclassified" are retirement notes naming their own claim.
    "formerly", "reclassified", "no longer presented",
]
