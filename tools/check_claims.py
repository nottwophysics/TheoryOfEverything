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
    return None


# ----------------------------------------------------------------- helpers

def tracked_docs():
    out = subprocess.run(["git", "ls-files", "*.md"], cwd=ROOT,
                         capture_output=True, text=True).stdout.split()
    return [os.path.join(ROOT, f) for f in out]


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
        for path in tracked_docs():
            text = io.open(path, encoding="utf-8").read()
            new = text
            for off, para in paragraphs(text):
                fp = flat(para)
                for pat in pats:
                    for m in re.finditer(pat, fp):
                        written = int(m.group("v"))
                        if written == actual:
                            continue
                        rel = os.path.relpath(path, ROOT)
                        if fix:
                            new = re.sub(
                                pat,
                                lambda mm: mm.group(0).replace(mm.group("v"), str(actual)),
                                new)
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


def _is_frozen_archive(path):
    """
    A file under a `versions/` directory is a frozen prior version. It is SUPPOSED to
    contain the wording that was retired -- that is what freezing it is for -- and
    flagging it trains you to ignore the checker. Added 2026-08-17, when widening the
    Phi<=S paraphrases lit up four frozen manuscripts at once.
    """
    return os.sep + "versions" + os.sep in path


def check_retired(verbose, problems):
    markers = [m.lower() for m in MANIFEST.EXEMPT_MARKERS]
    for entry in MANIFEST.RETIRED:
        name = entry["name"]
        pats = list(entry.get("banned", [])) + list(entry.get("paraphrases", []))
        hits = 0
        for path in tracked_docs():
            if _is_frozen_archive(path):
                continue
            text = io.open(path, encoding="utf-8").read()
            for off, para in paragraphs(text):
                fp = flat(para)
                for pat in pats:
                    m = re.search(pat, fp, re.I)
                    if not m or _negated(fp, m.start()):
                        continue
                    # Exemption is PROXIMITY-based, not whole-paragraph. A
                    # paragraph-wide exemption let a genuinely stale caveat hide
                    # anywhere in a long paragraph that happened to mention
                    # "withdrawn" -- which is exactly how the Bell caveat
                    # survived in six documents past the first sweep.
                    # Strip markdown emphasis before looking for markers.
                    # "is **false** of this module" does not contain the
                    # substring "is false", so bold/italics silently defeated
                    # the exemption and flagged a retraction note as a
                    # surviving claim. Emphasis is formatting, not meaning.
                    window = _demph(fp[max(0, m.start() - 300):m.end() + 300])
                    if any(mk in window for mk in markers):
                        continue
                    if True:
                        hits += 1
                        rel = os.path.relpath(path, ROOT)
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
