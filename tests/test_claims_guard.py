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
import re
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


# ---------------------------------------------------------------- cv/ and archives
# Added 2026-08-18. Two gaps found the same afternoon, either of which alone would
# have hidden a retired claim on a public author profile for seven weeks:
#   1. `cv/` was not an outbound directory, so the PhilPapers CV was never scanned.
#   2. Frozen archives were exempt from retired-claim checks but NOT from count
#      checks, so adding cv/ (with its cv/versions/ snapshots) turned the checker
#      permanently red — and a permanently red guard is one you learn to ignore.


def test_cv_is_an_outbound_dir():
    """
    `cv/` is outbound. It sits on a public author profile.

    Pinned at the configuration level, like submission/ and outreach/ above, because
    the behavioural test cannot run where cv/ is absent (CI, mutation sandbox).
    """
    assert "cv" in check_claims.UNTRACKED_OUTBOUND, (
        "cv/ must be scanned. The CV uploaded to PhilPapers carried a retired claim, a "
        "superseded v1 DOI and two stale counts for seven weeks; it was found by hand, "
        "not by this checker. 'Outbound' means a stranger can read it."
    )


def test_frozen_archive_is_exempt_from_count_checks(tmp_path, monkeypatch):
    """
    A frozen prior version must NOT be asked to report today's numbers.

    Behavioural, not structural: two files are fed to the real counts checker with the
    same wrong number, differing only in whether their path is under `versions/`. The
    frozen one must be silent and the live one must complain — so this fails both if
    the exemption disappears and if it over-fires and silences everything.
    """
    entry = next((e for e in MANIFEST.COUNTS if e["name"] == "test_total"), None)
    if entry is None:
        pytest.skip("no test_total count entry")

    actual = check_claims.measure("test_total")
    if actual is None:
        pytest.skip("could not measure test_total")
    stale = actual + 1000            # cannot collide with the real value

    live = tmp_path / "live.md"
    frozen = tmp_path / "versions" / "old.md"
    frozen.parent.mkdir()
    body = f"The suite has {stale} automated tests.\n"
    live.write_text(body, encoding="utf-8")
    frozen.write_text(body, encoding="utf-8")

    monkeypatch.setattr(check_claims, "docs_to_scan",
                        lambda: [str(live), str(frozen)])
    problems = []
    check_claims.check_counts(False, False, problems)

    hits = [p for p in problems if str(stale) in p]
    assert any("live.md" in p for p in hits), (
        "the counts checker went silent on a LIVE document carrying a stale number — "
        "the frozen-archive exemption is over-firing."
    )
    assert not any("old.md" in p for p in hits), (
        "a file under versions/ was count-checked. Frozen snapshots are supposed to "
        "carry the number of their day; flagging them forever is how a guard gets ignored."
    )


def test_fix_refuses_to_renumber_digits_sliced_out_of_a_larger_number():
    """--fix must apply the SAME mid-number test the report applies.

    Until 2026-08-21 it did not. The detection loop skipped "~1,496 automated
    tests" correctly (the capture starts mid-number), and then the repair ran an
    unguarded re.sub over the whole file and rewrote it anyway -- turning the
    master CV's PSF figure into "~1,501" in a document that goes on a public
    author profile. The guard reported correctly and repaired wrongly, which is
    worse than not running at all. Found by running --fix, not by reading it.
    """
    pat = r"(?P<v>\d+) automated tests"
    renumber = check_claims._renumber(501)

    # Sliced out of a larger number: must be left exactly alone.
    for untouched in ("~1,496 automated tests", "2,490 automated tests",
                      "1.490 automated tests"):
        assert re.sub(pat, renumber, untouched) == untouched, untouched

    # A genuine count: must be rewritten to the measured value.
    assert re.sub(pat, renumber, "a suite with 490 automated tests") == \
        "a suite with 501 automated tests"
