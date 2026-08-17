"""
Can each guard in the claims manifest ever come out red?

A green checker is evidence only if you know what would make it fail. This project
learned that the expensive way: `phi_s_pre_audit_numbers` sat in the manifest for
days and could NEVER fire. Its patterns ("apparent 89% satisfaction", "every one of
the 23") occur only inside a section-8 falsification paragraph, and any such
paragraph necessarily contains "does not hold" and "violates" -- both EXEMPT_MARKERS.
The stale figures were exempted by their own refutation, in every document, on every
run, while the checker reported "OK -- no retired claim survives".

That is the same defect the project spent two days finding in its own experiments:
a value fixed by structure rather than by data. Check A -- "could this have come out
differently?" -- applies to the instruments, not only to what they measure.

So each retired entry carries a `witness`: the claim AS IT ACTUALLY APPEARED, sourced
from git history or the frozen archives. These tests assert every witness is still
caught. They import the checker's own matching function rather than re-implementing
it, because a test that re-implements the loop would have passed happily while the
real loop was dead.
"""
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import claims as MANIFEST  # noqa: E402
import check_claims  # noqa: E402

MARKERS = [m.lower() for m in MANIFEST.EXEMPT_MARKERS]
IDS = [e["name"] for e in MANIFEST.RETIRED]


def _hits(entry, text):
    return list(check_claims.retired_hits(entry, text, MARKERS))


@pytest.mark.parametrize("entry", MANIFEST.RETIRED, ids=IDS)
def test_every_entry_has_a_witness(entry):
    """
    No entry may be added without the wording it retires.

    Without a witness there is nothing to prove the entry works, and an entry that
    does not work is indistinguishable from one that finds nothing.
    """
    assert entry.get("witness"), (
        f"{entry['name']} has no `witness`. Add the claim as it actually appeared, "
        f"so this file can prove the entry is capable of firing."
    )


@pytest.mark.parametrize("entry", MANIFEST.RETIRED, ids=IDS)
def test_witness_is_caught(entry):
    """
    THE test this file exists for.

    The witness is the real sentence, including the refutation vocabulary that
    surrounded it. If an entry can only fire on text that never occurs in practice,
    it fails here -- which is precisely what `phi_s_pre_audit_numbers` would have
    done from the day it was written.
    """
    witness = entry.get("witness")
    if not witness:
        pytest.skip("covered by test_every_entry_has_a_witness")
    hits = _hits(entry, witness)
    assert hits, (
        f"{entry['name']} does NOT fire on its own witness — the guard is dead.\n"
        f"  witness: {witness[:160]}\n"
        f"  If the witness legitimately contains exemption vocabulary (a falsification "
        f"paragraph naming its own numbers), set \"no_exempt\": True on the entry."
    )


@pytest.mark.parametrize("entry", MANIFEST.RETIRED, ids=IDS)
def test_explicit_hatch_still_silences(entry):
    """
    The escape hatch must work, or every correction record becomes a false positive.

    An honest retraction has to NAME the claim it retracts; `claims-ok` is how a
    document says "I am quoting this in order to correct it."
    """
    witness = entry.get("witness")
    if not witness:
        pytest.skip("no witness")
    assert not _hits(entry, "<!-- claims-ok: quoting to correct -->\n" + witness), (
        f"{entry['name']}: an explicit claims-ok hatch failed to silence the entry."
    )


def test_no_entry_is_pattern_free():
    """An entry with no patterns is a comment, not a guard."""
    empty = [e["name"] for e in MANIFEST.RETIRED
             if not (e.get("banned") or e.get("paraphrases"))]
    assert not empty, f"entries with no patterns at all: {empty}"


# Named HERE, not read from check_claims. A first version of the test below took this
# list from the module under test, so emptying `UNTRACKED_OUTBOUND` made the test SKIP
# instead of FAIL -- a test whose expectation comes from the code it checks cannot fail.
# The mutation battery caught it (`claims-scan-tracked-only` survived); it is the same
# defect class as everything else this manifest exists to guard against.
OUTBOUND_DIRS = ["submission", "outreach"]


def test_outbound_dirs_are_configured():
    """
    The configuration must name the outbound directories.

    The behavioural test below can only run where `submission/` and `outreach/` exist,
    and they are absent both in CI and inside the mutation sandbox (tools/mutate.py
    excludes them from its scratch copy). So emptying UNTRACKED_OUTBOUND made the
    behavioural test skip and the mutation survive. This pins the configuration
    directly, which is checkable anywhere.
    """
    assert set(check_claims.UNTRACKED_OUTBOUND) >= {"submission", "outreach"}, (
        "UNTRACKED_OUTBOUND must name submission/ and outreach/. Dropping them makes "
        "the checker blind to every manuscript while it still reports OK — the exact "
        "failure this guard exists to prevent."
    )


def test_checker_scans_outbound_dirs_when_present():
    """
    The checker must see the manuscripts.

    For as long as it existed it scanned `git ls-files '*.md'` only, and
    `submission/` + `outreach/` are gitignored — so it reported OK while no
    manuscript was in its field of view, and the published paper carried a retired
    claim through eight green runs.
    """
    scanned = {os.path.realpath(p) for p in check_claims.docs_to_scan()}
    checked_any = False
    for d in OUTBOUND_DIRS:
        base = os.path.join(ROOT, d)
        if not os.path.isdir(base):
            continue  # absent in CI; the repo does not ship these
        found = [os.path.join(r, f)
                 for r, _dirs, files in os.walk(base)
                 for f in files if f.endswith(".md")]
        if not found:
            continue
        checked_any = True
        missed = [f for f in found if os.path.realpath(f) not in scanned]
        assert not missed, (
            f"docs_to_scan() does not return {len(missed)} .md file(s) under {d}/ — "
            f"the checker is blind to the manuscripts it exists to protect. "
            f"First missed: {os.path.relpath(missed[0], ROOT)}"
        )
    if not checked_any:
        pytest.skip("no outbound .md present in this checkout (expected in CI)")
