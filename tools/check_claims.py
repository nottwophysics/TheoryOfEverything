#!/usr/bin/env python3
"""
Claims checker — keeps the documents honest about what the code produces.

    python tools/check_claims.py            # verify; exit 1 on any problem
    python tools/check_claims.py --fix      # rewrite drifted counts from measurement
    python tools/check_claims.py -v         # show what was checked

Runs in CI. It exists because two things kept happening in this repository:

  * A count quoted across eight documents drifted every time the suite changed.
    Test totals alone were hand-propagated five times in a single day.
  * A retired claim survived as a PARAPHRASE, because the retirement was
    recorded as a phrase and then hunted as that phrase. One sat two paragraphs
    from its own refutation for months.

And the direction that keeps being missed: a CORRECTION can go stale too.
"does NOT recover Newton" was true when written and false three commits later.
So `retired:` in the manifest carries both kinds, and a stale correction is
reported exactly like a stale overclaim.

Whitespace is normalised before searching. Prose here is hard-wrapped, so a
naive grep misses any phrase that happens to straddle a newline -- which is how
several survivals were missed by earlier sweeps.

The manifest (tools/claims.py) is a plain Python module, not YAML: a hand-rolled
parser for the config that guards against silent drift would be the one part able
to fail silently and hand back a false all-clear.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import glob
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import claims as MANIFEST  # noqa: E402


# ----------------------------------------------------------------- measuring

def measure(name):
    """Live values. Never transcribed."""
    if name == "test_total":
        out = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q"],
                             cwd=ROOT, capture_output=True, text=True).stdout
        m = re.search(r"(\d+) tests collected", out)
        return int(m.group(1)) if m else None
    if name == "test_files":
        d = os.path.join(ROOT, "tests")
        return len([f for f in os.listdir(d)
                    if f.startswith("test_") and f.endswith(".py")])
    if name == "experiments":
        src = io.open(os.path.join(ROOT, "main.py"), encoding="utf-8").read()
        m = re.search(r"experiments_map\s*=\s*\{(.*?)\n    \}", src, re.S)
        return len(re.findall(r"^\s*(\d+):", m.group(1), re.M)) if m else None
    return None


def run_producer(name):
    if name == "phi_s_verdict":
        csv = os.path.join(ROOT, "reproducibility", "phi_s", "data",
                           "phi_s_validated_results.csv")
        env = dict(os.environ, PYTHONPATH=ROOT)
        out = subprocess.run([sys.executable, "predictions/phi_s_verdict.py", "--csv", csv],
                             cwd=ROOT, capture_output=True, text=True, env=env).stdout
        try:
            return json.loads(out)
        except json.JSONDecodeError:
            return None
    if name == "gleason_counts":
        # Deterministic: dimension defaults to 4, both sweeps seed np.random with 42.
        # Re-run rather than transcribed -- these are the figures s3.1 prints.
        sys.path.insert(0, ROOT)
        from quantum.gleason import GleasonVerification
        gv = GleasonVerification()
        uniq = gv.demonstrate_uniqueness()
        d3 = gv.demonstrate_dim2_exception()["dim_3"]
        return {
            "uniqueness_trials_default_dim":
                uniq["alternative_amplitude"]["additivity"]["tests"],
            "dispersion_free_bases_dim3": d3["total_tests"],
            "dispersion_free_failures_dim3":
                int(round(d3["failure_rate"] * d3["total_tests"])),
        }
    if name == "unity_env_counts":
        # Deterministic: UnityOfExperience() defaults (n_outcomes=3, seed=42) and
        # environment_unitary_invariance() defaults (n_trials=20). Re-run, never
        # transcribed -- these are the figures s2.4 prints.
        sys.path.insert(0, ROOT)
        from quantum.unity_of_experience import UnityOfExperience
        res = UnityOfExperience().environment_unitary_invariance()
        return {
            "trials": res["trials"],
            # Rounded to the two decimals the manuscript prints. The raw value is
            # 0.42425511347782846; pinning the full float would fail on BLAS noise
            # without any claim having changed.
            "min_rho_E_trace_norm_change":
                round(res["min_rho_E_trace_norm_change"], 2),
        }
    return None


# ----------------------------------------------------------------- helpers

# Directories this project treats as OUTBOUND but deliberately keeps out of git:
# manuscripts, cover letters, deposit notes, the outreach claims ledger. They are
# gitignored, so `git ls-files` never saw them -- which meant that for as long as this
# checker has existed it reported "OK -- no retired claim survives" while NO MANUSCRIPT
# WAS IN ITS FIELD OF VIEW AT ALL. The published paper carried a retired claim through
# eight green runs. A checker that is silent about what it did not read is worse than
# one that never ran, so scan these when present and say so either way.
# `cv` added 2026-08-18. The PhilPapers CV is the single most-public artefact this
# project has -- it sits on a public author profile -- and it was outside this list
# for seven weeks while carrying a retired claim, a superseded v1 DOI and two stale
# counts. It was found by hand, not by this checker. Outbound means "a stranger can
# read it", not "it is a manuscript".
UNTRACKED_OUTBOUND = ["submission", "outreach", "cv"]
UNTRACKED_GLOBS = ["docs/PAPER*.md"]


def tracked_docs():
    out = subprocess.run(["git", "ls-files", "*.md"], cwd=ROOT,
                         capture_output=True, text=True).stdout.split()
    return [os.path.join(ROOT, f) for f in out]


def untracked_outbound_docs():
    """Outbound .md files that git does not track. Absent in CI; present locally."""
    found = []
    for d in UNTRACKED_OUTBOUND:
        base = os.path.join(ROOT, d)
        if not os.path.isdir(base):
            continue
        for root, _dirs, files in os.walk(base):
            found += [os.path.join(root, f) for f in files if f.endswith(".md")]
    for pattern in UNTRACKED_GLOBS:
        found += glob.glob(os.path.join(ROOT, pattern))
    return found


def docs_to_scan():
    """Every document this project could send outward, tracked or not, deduped."""
    seen, out = set(), []
    for p in tracked_docs() + untracked_outbound_docs():
        rp = os.path.realpath(p)
        if rp in seen:
            continue
        seen.add(rp)
        out.append(p)
    return out


def paragraphs(text):
    """(start_offset, paragraph) over blank-line-separated blocks."""
    pos = 0
    for para in re.split(r"\n\s*\n", text):
        yield pos, para
        pos += len(para) + 2


def flat(s):
    return re.sub(r"\s+", " ", s)


def line_of(text, offset):
    return text.count("\n", 0, offset) + 1


# ----------------------------------------------------------------- checks

def _demph(text):
    """Lower-case and drop markdown emphasis/code marks, for marker matching."""
    return re.sub(r"[*_`~]", "", text).lower()


_NEG = re.compile(r"(not|never|no longer|n't|cannot|isn't|aren't|fails to)\s+(\w+\s+){0,3}$",
                  re.I)


def _negated(text, start):
    """
    True if the match is negated by what precedes it.

    "Phi is NOT capped by the bipartition entropy" states the refutation, and
    flagging it as a surviving claim is the checker crying wolf -- which is the
    fastest way to get a checker ignored.
    """
    return bool(_NEG.search(text[max(0, start - 60):start]))



def _renumber(actual):
    """re.sub replacement that refuses to rewrite a value sliced out of a larger
    number. Mirrors the mid-number test the detection loop applies."""
    def repl(mm):
        whole, subject = mm.group(0), mm.string
        vs, ve = mm.start("v"), mm.end("v")      # absolute, not match-relative:
        # the capture can sit at offset 0 of the match while the digits it was
        # sliced out of sit just before it in the FILE ("~1,|496 automated tests").
        if vs > 0 and subject[vs - 1] in "0123456789,.":
            return whole
        if ve < len(subject) and subject[ve] in "0123456789":
            return whole
        off = vs - mm.start(0)
        return whole[:off] + str(actual) + whole[ve - mm.start(0):]
    return repl


def _renumber_text(text, pats, actual):
    """Apply the count repair PARAGRAPH BY PARAGRAPH, honouring `claims-ok`.

    The second half of the same 2026-08-21 defect: the repair used to run one
    re.sub over the whole file, so a paragraph the report had skipped for its
    explicit `claims-ok` hatch was rewritten anyway. Caught on a dry run against
    submission/PoP/membership-enquiry-pop-society.md, which quotes the stale
    "30 experiments / 237 automated tests" precisely in order to record that the
    figures were superseded -- and would have had 237 rewritten to today's total,
    falsifying a record of what a public deposit used to say.
    """
    parts = re.split(r"(\n\s*\n)", text)
    renumber = _renumber(actual)
    for i, part in enumerate(parts):
        if i % 2 or "claims-ok" in flat(part).lower():
            continue
        for pat in pats:
            part = re.sub(pat, renumber, part)
        parts[i] = part
    return "".join(parts)


def check_counts(fix, verbose, problems):
    for entry in MANIFEST.COUNTS:
        name = entry["name"]
        actual = measure(name)
        if actual is None:
            problems.append(f"[{name}] could not measure — producer failed")
            continue
        if verbose:
            print(f"  measured {name} = {actual}")
        pats = entry.get("patterns", [])
        # NO exemption list for counts. Reusing the retirement vocabulary here
        # was a design error: ARCHITECTURE.md's directory tree lists
        # `error_correction.py`, whose substring "correction" exempted the whole
        # block and silently skipped a stale "TEST SUITE: 424". A checker that
        # skips quietly is worse than one that never ran. The patterns in the
        # manifest are anchored to phrasings that mean "the current total", so a
        # dated snapshot ("302, historical count at the time of writing") does
        # not match them in the first place and needs no exemption.
        for path in docs_to_scan():
            # A frozen prior version is SUPPOSED to carry the count of its day; demanding
            # it report today's is what trains you to ignore the checker. `_is_frozen_archive`
            # already exempts these from retired-claim checks -- it was never applied here,
            # which only showed up when cv/ (with its cv/versions/ archive) entered scope
            # on 2026-08-18.
            if _is_frozen_archive(path):
                continue
            text = io.open(path, encoding="utf-8").read()
            new = text
            for off, para in paragraphs(text):
                fp = flat(para)
                # Counts still get NO vocabulary-based exemption -- reusing the
                # retirement words here once let "error_correction.py" in a directory
                # listing exempt a whole block via the substring "correction". Only the
                # explicit hatch counts, and only for dated records that are SUPPOSED to
                # quote the number of the day.
                if "claims-ok" in fp.lower():
                    continue
                for pat in pats:
                    for m in re.finditer(pat, fp):
                        # Reject a match that begins mid-number: "~1,700 automated
                        # tests" (the PSF figure on the master CV) captured "700" and
                        # was reported as a drifted test total. A digit, comma or
                        # period immediately before the captured value means we have
                        # sliced into a larger number, not found a count.
                        vstart = m.start("v")
                        if vstart > 0 and fp[vstart - 1] in "0123456789,.":
                            continue
                        written = int(m.group("v"))
                        if written == actual:
                            continue
                        rel = os.path.relpath(path, ROOT)
                        if fix:
                            # The mid-number guard above protects only the REPORT.
                            # Until 2026-08-21 the repair below had none, so --fix
                            # rewrote every match in the file including the ones
                            # detection had just skipped: it turned the master CV's
                            # PSF figure "~1,496 automated tests" into "~1,501",
                            # silently, in a document that goes on a public author
                            # profile. Caught by running it, not by reading it.
                            # A guard that reports correctly and repairs wrongly is
                            # worse than no guard, so the repair now carries the
                            # same tests the report does -- mid-number AND the
                            # explicit `claims-ok` hatch, per paragraph.
                            new = _renumber_text(new, pats, actual)
                        else:
                            problems.append(
                                f"[{name}] {rel}:~{line_of(text, off)}: says {written}, "
                                f"measured {actual}  ({pat!r})")
            if fix and new != text:
                io.open(path, "w", encoding="utf-8").write(new)
                print(f"  fixed {os.path.relpath(path, ROOT)} [{name}] -> {actual}")


def check_derived(verbose, problems):
    cache = {}
    for entry in MANIFEST.DERIVED:
        prod = entry["producer"]
        if prod not in cache:
            cache[prod] = run_producer(prod)
        data = cache[prod]
        if data is None:
            problems.append(f"[{entry['name']}] producer {prod!r} did not run")
            continue
        actual = data.get(entry["key"])
        written = entry.get("pinned")
        if str(actual) != str(written):
            problems.append(
                f"[{entry['name']}] manifest pins {written!r} but {prod}.{entry['key']} "
                f"now returns {actual!r} — update the manifest AND every document quoting it")
        elif verbose:
            print(f"  {entry['name']}: {actual} (matches manifest)")


def _is_declared_archive(text):
    """
    True if the document declares itself superseded in its own opening banner.

    `versions/` covers archives identified by PATH. This covers the other kind: a
    draft or an old master that is dead but still on disk. Requiring an invisible
    per-paragraph marker for those would hide the status from the one person who
    most needs it -- whoever opens the file next -- so the banner does both jobs.
    Scoped to the head of the file so a passing mention cannot exempt a live one.
    """
    head = _demph(text[:900])
    return ("superseded" in head and
            ("do not" in head or "archive" in head or "provenance only" in head
             or "not for submission" in head or "history, not current" in head
             # PHI_S_MULTIAGENT_RESEARCH_REPORT.md's banner: the honest form for a
             # dated result whose body is deliberately left as it was written.
             or "dated record" in head or "body left as written" in head))


def _is_frozen_archive(path):
    """
    A file under a `versions/` directory is a frozen prior version. It is SUPPOSED to
    contain the wording that was retired -- that is what freezing it is for -- and
    flagging it trains you to ignore the checker. Added 2026-08-17, when widening the
    Phi<=S paraphrases lit up four frozen manuscripts at once.
    """
    return os.sep + "versions" + os.sep in path


def retired_hits(entry, text, markers):
    """
    Every un-exempted match of one retired entry in one document.

    Extracted 2026-08-17 so that tests exercise THE CHECKER rather than a copy of it.
    A test that re-implements this loop would have passed happily while the real loop
    was structurally incapable of firing -- which is exactly what happened to
    `phi_s_pre_audit_numbers` for as long as it existed.

    Yields (paragraph_offset, pattern, match).
    """
    pats = list(entry.get("banned", [])) + list(entry.get("paraphrases", []))
    for off, para in paragraphs(text):
        fp = flat(para)
        for pat in pats:
            m = re.search(pat, fp, re.I)
            if not m or _negated(fp, m.start()):
                continue
            # Exemption is PROXIMITY-based, not whole-paragraph. A paragraph-wide
            # exemption let a genuinely stale caveat hide anywhere in a long paragraph
            # that happened to mention "withdrawn" -- which is how the Bell caveat
            # survived in six documents past the first sweep. Markdown emphasis is
            # stripped first: "is **false** of this module" does not contain the
            # substring "is false", so bold silently defeated the exemption.
            window = _demph(fp[max(0, m.start() - 300):m.end() + 300])
            if entry.get("no_exempt"):
                # Only the explicit hatch, and PARAGRAPH-scoped: it is a deliberate
                # statement about this block, and a marker at the top of a long block
                # was missed when this was proximity-scoped.
                if "claims-ok" in _demph(fp):
                    continue
            elif any(mk in window for mk in markers):
                continue
            yield off, pat, m


def check_retired(verbose, problems):
    markers = [m.lower() for m in MANIFEST.EXEMPT_MARKERS]
    for entry in MANIFEST.RETIRED:
        name = entry["name"]
        pats = list(entry.get("banned", [])) + list(entry.get("paraphrases", []))
        hits = 0
        for path in docs_to_scan():
            if _is_frozen_archive(path):
                continue
            text = io.open(path, encoding="utf-8").read()
            if _is_declared_archive(text):
                continue
            for off, pat, m in retired_hits(entry, text, markers):
                hits += 1
                rel = os.path.relpath(path, ROOT)
                fp = flat(text[off:off + 4000])
                problems.append(
                    f"[{name}] {rel}:~{line_of(text, off)}: retired claim survives "
                    f"un-exempted: ...{fp[max(0, m.start()-60):m.start()+90]}...")
        if verbose and not hits:
            print(f"  {name}: clear ({len(pats)} patterns, incl. paraphrases)")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fix", action="store_true",
                    help="rewrite drifted counts from live measurement")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    problems = []

    tracked = len(tracked_docs())
    untracked = len(untracked_outbound_docs())
    frozen = sum(1 for p in docs_to_scan() if _is_frozen_archive(p))
    print(f"scanning {tracked} tracked + {untracked} untracked outbound .md "
          f"({frozen} frozen archives skipped for retired-claim checks)")
    if not untracked:
        print("  NOTE: no untracked outbound docs found (submission/, outreach/ absent) — "
              "this run says nothing about any manuscript.")

    print("counts")
    check_counts(args.fix, args.verbose, problems)
    print("derived numbers")
    check_derived(args.verbose, problems)
    print("retired claims (incl. paraphrases, whitespace-normalised)")
    check_retired(args.verbose, problems)

    if problems:
        print(f"\n{len(problems)} problem(s):\n")
        for p in problems:
            print("  " + p)
        print("\nFAIL")
        return 1
    print("\nOK — documents agree with the code, and no retired claim survives.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
