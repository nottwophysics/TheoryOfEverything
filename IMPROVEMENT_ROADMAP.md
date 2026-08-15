# TheoryOfEverything — fix / improve / enhance roadmap

> **Dated internal record.** Suite counts and "[DONE]" statuses reflect the
> repository at the time of writing (e.g. "250 passed", "237 passed" — the
> current public suite is 306) and some assessments were superseded by the
> 2026-08-15 adversarial review (notably: `quantum/tensor_network.py`, praised
> below, was found to apply its tensors as no-ops — see the module's review
> note). Read this file as history, not as current status.

Grounded in the executed review (`PHYSICS_DERIVATIONS_REVIEW.md`). The project's
biggest asset is that it is **clean, well-tested, and candid in its own
comments**; its biggest liability is that it **conflates three different kinds of
activity** under one "theory of everything" banner: (A) legitimate
computational-physics demos, (B) numerical curve-fitting presented as
"derivation," and (C) philosophy of mind. The single most valuable change is to
*separate these three* so each can be judged — and improved — on its own terms.

Recommendations are ordered by effort-to-value. P0 = do now (bugs), P1 =
integrity (stop over-claiming), P2 = engineering, P3 = genuine enhancements,
P4 = ambitious directions.

---

## P0 — Correctness bugs (small, do immediately) — ALL DONE

*Status: all four fixed; `pytest -W error::RuntimeWarning` → **237 passed, 0
warnings**. Diff touches only `einstein_2d.py`, `einstein_3d.py`,
`predictions/testable.py`, `tests/test_predictions.py`.*

1. **[DONE] NumPy-2 cross-product.** `gravity/einstein_2d.py:74` — fixed to the
   explicit scalar 2-D cross (`v1[0]*v2[1] - v1[1]*v2[0]`). Still recommended:
   add an upper pin `numpy>=1.24,<3` and a CI matrix (numpy 1.26 + 2.x) so this
   class of break is caught automatically.

2. **[DONE] P5 holographic-noise dimensional bug.**
   `prediction_5_holographic_noise` previously returned `sqrt(l_planck)` (units
   √m). Replaced with the dimensionally-consistent Hogan scaling for a stated
   arm length L=40 m (Fermilab Holometer): RMS displacement
   `Δx ~ sqrt(l_P·L)` = 2.5×10⁻¹⁷ m, and amplitude spectral density
   `L·sqrt(l_P/c)` = 9.3×10⁻²¹ m/√Hz. Added a unit test asserting the RMS lies
   between the Planck length and the arm length (i.e. is genuinely lengthlike).

3. **[DONE] P2 threshold now derived, not hard-coded.**
   `prediction_2_decoherence_mass_threshold` now solves `τ(m,R)=τ_obs` for `m`
   at a stated density (ρ=2000 kg/m³, τ_obs=1 s), giving a threshold of
   **8.6×10⁻¹⁶ kg**, and states explicitly that the threshold is
   decoherence-time- and density-dependent rather than a single universal mass.
   Added a test checking the threshold is physical and consistent with the
   per-object table (electron coheres, cat does not).

4. **[DONE] Degenerate-geometry warnings.** The `RuntimeWarning: Degrees of
   freedom <= 0` came from `np.std(T_00[mask])` on the empty no-mass slice in
   `einstein_2d.py`/`einstein_3d.py`. Added a `np.sum(mask) > 1` guard at both
   sites; the suite now passes under `-W error::RuntimeWarning`.

---

## P1 — Scientific integrity (the highest-value change)

The code's *comments* are already honest ("numerological", "not a derivation",
"consistency check"). The problem is the **framing at the module/dir level**:
files named `derivation.py` and a `fine_structure` trio read as claims to have
derived α. Align the packaging with the honest comments.

> **Status — items 5, 6, 7 DONE** (suite: **250 passed**, `main.py` exit 0).
> - **#5 done:** `git mv` split — `numerology/` now holds `fine_structure{,_v2,_v3}.py`,
>   `derivation.py`, `look_elsewhere.py`, `cross_validation.py` (each labelled
>   coincidence-search); `constants/` keeps only `cosmological.py` (Λ note) and a
>   new `koide.py` (verification + 0-param m_τ hold-out, DOI-cited). Both
>   `__init__.py` re-scoped; `main.py` and `tests/` imports updated; git tracked
>   the four moves as renames (history preserved).
> - **#6 done:** `numerology/look_elsewhere.py` (383 formulas hit 1/α at 0.01%;
>   100% coverage near 137; 13/25 constants hit) + `numerology/cross_validation.py`
>   (α's base 163 recurs for 0/5 others; Koide predicts m_τ to 0.006%). Figures
>   `alpha_look_elsewhere.png`, `alpha_cross_validation.png`.
> - **#7 done:** `predictions/iit_entanglement_rigorous.py` — independent
>   TFIM-ground-state mapping + permutation null + independent-draw baseline; the
>   old −1.0 correlation is gone (r=+0.08, n.s., p=0.21), and the 99.5% hold rate
>   is shown uninformative (within 0.5 pp of both controls). Figure
>   `iit_bridge_rigorous.png`.

5. **Rename and re-scope the constants work.** `constants/` currently mixes a
   real thing (evaluating known relations) with numerology. Split it:
   - `numerology/` (explicit name) for the α number-matching. Keep it — it's a
     fun exploration — but label it as *coincidence search*, and add the
     discipline below.
   - `constants/` keeps only the honest, verifiable content: the Koide-formula
     *check*, the Λ ∝ 1/S *dimensional-analysis note* (with its existing
     caveats), each clearly labelled "verification" / "consistency check", not
     "derivation".

6. **Make the α search falsifiable instead of decorative.** The
   `163 − 26 + π/100` result has 3 free choices fitted to 1 target, so 0.003 %
   is meaningless. Two concrete upgrades that would turn it into real evidence:
   - **Look-elsewhere / degrees-of-freedom accounting.** Implement a brute-force
     search over the *same* family (small integers, Heegner numbers, low-order
     π/e/φ corrections) and report **how many formulas of comparable complexity
     hit ANY of the ~25 SM constants to <0.01 %**. If thousands do, a single hit
     is expected by chance — quantify that. This is the single most honest thing
     the module could add.
   - **Cross-validation across constants.** A real formula-generating principle
     should hit α *and* (say) the weak mixing angle or a mass ratio with the
     *same* rule and *no re-tuning*. Add a test: fix the rule on α, predict a
     second constant, report the error. This is falsifiable and currently absent.

7. **Fix the IIT–entanglement "bridge" test — it is circular.**
   `predictions/iit_bridge.py:test_conjecture` computes Φ and S from the *same*
   scalar (matrix connectivity ΣW), so the 100 % hold-rate and −1.0 correlation
   are artifacts. Rebuild it as a real test:
   - Draw the classical network and the quantum state **independently**, or map
     one to the other through a *non-trivial, stated* physical channel (e.g. a
     Jordan–Wigner / stabilizer construction), not a linear interpolation keyed
     to ΣW.
   - Report the inequality margin distribution and a **null model** (shuffle the
     Φ–S pairing; show the conjecture fails under the null). Without a null, "it
     holds" is not informative.
   - State precisely what "Φ ≤ S" would *mean* physically and what would refute
     it. Right now it can't be refuted because both sides are the same knob.

8. **Retire the parapsychology citations.** P4 cites PEAR lab and the Global
   Consciousness Project as "controversial results." These are widely regarded
   as non-reproducible and are a credibility liability. Either remove them or add
   an explicit note that they failed replication and are cited only as historical
   attempts. Keep P4's *protocol* framing (pre-registration, confound control) —
   that part is sound.

9. **Tag every prediction with prior art.** P1 = Bose–Marletto–Vedral (2017),
   P2 = Diósi–Penrose, P3 = Ryu–Takayanagi / Bisognano–Wichmann area law,
   P5 = Hogan/Holometer. Add a `prior_art` field with citations so the framework
   doesn't appear to claim borrowed predictions as original. The honest position
   ("we inherit these testable predictions from emergent-gravity programs, and
   add interpretation X") is *stronger*, not weaker.

---

## P2 — Engineering & reproducibility

10. **Make the package importable.** Running the modules needed `PYTHONPATH=.`;
    add `[tool.setuptools] packages=[...]` (or `src/` layout) and `pip install
    -e .` so `import constants.fine_structure_v2` works from anywhere. Add
    `__main__` entry points or a `tofe` console script.

11. **Separate "internal-consistency" tests from "physics" tests.** 233 of 237
    tests check that the code's own constructions are self-consistent (sums to 1,
    Hermitian, etc.), which is good but easy to mistake for empirical validation.
    Mark physics-facing assertions with a `@pytest.mark.physics` and add a
    handful that compare against **external references** (CODATA constants,
    published decoherence rates), so a green suite means something stronger.

12. **Add numerical-reproducibility hygiene.** Seed every stochastic routine
    (the IIT bridge already does; the synthetic generators elsewhere should),
    pin a lockfile, and record library versions in a `provenance` field on any
    result dict that reports a number — the same discipline the review applied.

13. **Type hints + a `results` schema.** The functions return free-form dicts.
    Define `TypedDict`/`dataclass` result types (e.g. `PredictionResult` with
    `value`, `units`, `error_pct`, `prior_art`, `status`) so units and provenance
    are structurally enforced — this alone would have prevented the P5
    dimensional bug.

14. **CI + a one-command reproduction.** GitHub/Codeberg Actions running the test
    matrix and a `make reproduce` that regenerates every reported number and
    figure. Ship a `figures/` regeneration script.

---

## P3 — Genuine enhancements (turn demos into contributions)

These are places where the physics engine is real and could produce something
publishable *as computational physics*, independent of the philosophy.

15. **Emergent-gravity sandbox → a proper entanglement-geometry demo.** The
    `gravity/` (entropic, holographic, einstein_2d/3d) and `quantum/tensor_network`
    modules are the strongest physics content. Build a clean, cited notebook that
    reproduces a known result — e.g. Ryu–Takayanagi area law on a small tensor
    network, or Jacobson's entropic-derivation of Einstein's equations on a
    lattice — and validate against the analytic answer. That is a real,
    checkable deliverable.

16. **IIT toolkit done right.** The `compute_phi` implementation is a decent
    small-network Φ calculator. Benchmark it against **PyPhi** (the reference IIT
    library) on identical networks and report agreement/discrepancy. A validated,
    fast small-Φ implementation is genuinely useful to the IIT community and needs
    no metaphysics.

17. **Decoherence-threshold calculator with real experiments.** Turn P2 into a
    quantitative tool: given (mass, size, temperature, pressure), compute
    Diósi–Penrose *and* standard environmental decoherence times, and overlay the
    envelopes of real experiments (MAQRO, molecular interferometry records,
    optomechanics). That is a legitimately useful figure and sharpens which mass
    range actually discriminates collapse models.

18. **Constants "coincidence engine" as a teaching tool.** Reframe the α
    numerology as an honest demonstrator of the **look-elsewhere effect**: let
    users search formula families and *see* how easily any target is hit. This
    turns a weakness into a genuinely instructive module about why numerology
    fails.

---

## P4 — Ambitious directions (if the goal is to be taken seriously as physics)

19. **Pick ONE distinctive, falsifiable prediction and develop it fully.** The
    only framework-unique claim is P4 (consciousness-dependent decoherence).
    Either commit to it — derive a *quantitative* predicted effect size from
    stated axioms, specify the exact experiment, and pre-register — or drop it.
    A single sharp, quantitative, falsifiable prediction is worth more than five
    borrowed ones.

20. **Derive, don't fit.** If the claim is that α is *determined* by structure,
    the standard to meet is: **zero free parameters, fixed by axioms, predicts α
    AND a second constant, agrees with CODATA.** Until then, call it a search.
    The honest interim goal: show the axioms *constrain* α to a range, even a
    loose one, from first principles — that would be real progress and is
    currently not attempted.

21. **Keep the philosophy, but wall it off.** The Advaita framework (`brahman/`,
    `maya/`, `levels/`, `liberation/`) is coherent and the `falsification` module
    already concedes it's non-scientific. Move it into a clearly-labelled
    `philosophy/` package with its own README stating it is interpretive, not
    empirical. This *protects* the physics modules from being dismissed by
    association, and is intellectually cleaner.

---

## The one-paragraph version

Fix the three concrete bugs (numpy done, P5 units, P2 threshold). Then do the
single highest-value thing: **stop calling curve-fitting "derivation"** — rename
`constants/`→ split into honest `constants/` + explicit `numerology/`, add a
look-elsewhere/degrees-of-freedom analysis to the α search, and rebuild the
circular IIT bridge test with an independent mapping and a null model. Package
the genuinely good physics (`gravity/`, `tensor_network`, `compute_phi`) as
validated, cited computational-physics demos benchmarked against known results
(Ryu–Takayanagi, PyPhi, real decoherence experiments). Wall the philosophy into
its own labelled package. Keep the project's existing honesty — it's the best
thing about it — and push it all the way down into the directory structure and
the result schemas.

*Advisory only. Grounded in the executed review; no endorsement of the
framework's metaphysical claims is implied or intended.*