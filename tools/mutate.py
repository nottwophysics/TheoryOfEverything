#!/usr/bin/env python3
"""
Mutation battery — do the tests have teeth?

    python tools/mutate.py            # run every mutation, report survivors
    python tools/mutate.py -k seed    # only mutations whose name matches

A green suite says nothing about whether the tests COULD fail. The only real
check is to break the implementation and confirm something notices. When this
battery was first run by hand (2026-08-16) it found **6 of 16 mutations
survived undetected**, including two that mattered:

  * the seed argument to the Phi<=S system family could be ignored entirely
    with all tests passing -- so the "216 systems, seed 42" reproducibility
    guarantee the whole falsification rests on was protected by nothing;
  * every per-site MERA isometry could be replaced by one fixed isometry --
    destroying the network while leaving it non-trivial -- and all 33 MERA
    tests passed, because the existing control catches a ZEROED tensor but not
    a WRONG one.

Work happens in a scratch copy; the working tree is never modified, and the
run asserts that before and after.

Two ways this instrument can lie, both of which it caught in itself on the first
real run and now guards against:

  * a mutation that does not COMPILE makes the suite fail on an import error,
    which would be scored as a catch and credit the tests with teeth they have
    not shown -> rejected as INVALID before the suite runs;
  * a mutation that is a NO-OP (`1.0 * x`, adding an unused dict key) can never
    be caught, and reporting it as a survivor slanders the tests -> such
    mutations must change behaviour, and are rewritten when found.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (name, relative path, pattern, replacement)  -- applied to a scratch copy.
MUTATIONS = [
    ("seed-ignored", "predictions/phi_s_systems.py",
     r"rng = np\.random\.default_rng\(seed\)",
     "rng = np.random.default_rng(999)"),
    ("mera-wrong-isometry", "quantum/tensor_network.py",
     r"self\._apply_isometry\(psi, isometries\[layer\]\[k\], k\)",
     "self._apply_isometry(psi, isometries[0][0], k)"),
    ("gauss-bonnet-flag", "gravity/einstein_2d.py",
     r"\"passes\": bool\(", "\"passes\": True or bool("),
    ("gleason-dimension", "quantum/gleason.py",
     r"dim >= 3", "dim >= 0"),
    ("decoherence-no-pressure", "predictions/decoherence_calculator.py",
     r"n = pressure_pa / \(KB \* temperature_k\)",
     "n = 1.0e20 / (KB * temperature_k)"),
    ("superimposition-zero-error", "philosophy/maya/superimposition.py",
     r"return float\(np\.linalg\.norm\(self\.apparent - self\.actual\)\)",
     "return 0.0"),
    ("qec-logical-one", "quantum/error_correction.py",
     r"self\.logical_one = self\.logical_x @ self\.logical_zero",
     "self.logical_one = self.logical_zero"),
    ("first-law-ignore-eps", "gravity/entanglement_first_law.py",
     r"t = 1\.0 \+ epsilon \* self\.bond_modulation",
     "t = 1.0 + 0.001 * self.bond_modulation"),
    ("geometry-excited-state", "gravity/entanglement_geometry.py",
     r"evecs\[:, 0\]", "evecs[:, 1]"),
    ("detector-off-by-one", "agents/emergence_detector.py",
     r"\(n - 1\) \* H_all", "n * H_all"),
    ("lookelsewhere-first-not-closest", "numerology/look_elsewhere.py",
     r"return float\(vals\[np\.argmin\(np\.abs\(vals - target\)\)\]\)",
     "return float(vals[0])"),
    ("koide-constant", "constants/koide.py",
     r"q = num / den", "q = 2.0 / 3.0"),
    ("benchmark-auc-constant", "agents/benchmark.py",
     r"return float\(\(ranks\[:n1\]\.sum\(\) - n1 \* \(n1 \+ 1\) / 2\) / \(n1 \* n2\)\)",
     "return 0.5"),
    ("unity-identity-not-haar", "quantum/unity_of_experience.py",
     r"def _haar_unitary\(dim: int, rng: np\.random\.Generator\) -> np\.ndarray:",
     "def _haar_unitary(dim: int, rng: np.random.Generator) -> np.ndarray:\n        return np.eye(dim)"),
    ("verlinde-drop-G", "gravity/entropic.py",
     r"G_NEWTON = 6\.67430e-11", "G_NEWTON = 1.0e-11"),
    ("entanglement-chsh-constant", "quantum/entanglement.py",
     r"CHSH_S_value\": ", "CHSH_S_value\": 2.8284271247461903 or "),
]


def _tree_clean():
    out = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                         capture_output=True, text=True).stdout.strip()
    return out


def run_one(name, relpath, pattern, repl, workdir, verbose):
    src = os.path.join(workdir, relpath)
    if not os.path.exists(src):
        return {"name": name, "status": "SKIP", "reason": f"{relpath} missing"}
    original = open(src, encoding="utf-8").read()
    mutated, n = re.subn(pattern, repl, original, count=1)
    if n == 0:
        return {"name": name, "status": "SKIP",
                "reason": f"pattern not found in {relpath} (code moved?)"}
    # A mutation that breaks the file syntactically is not a mutation: the
    # suite "fails" on an import error and would be scored as a catch, which
    # would credit the tests with teeth they have not shown. Reject it here.
    try:
        compile(mutated, src, "exec")
    except SyntaxError as e:
        return {"name": name, "status": "INVALID",
                "reason": f"mutation does not compile ({e.msg}) — fix the pattern"}

    open(src, "w", encoding="utf-8").write(mutated)
    try:
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "--no-header",
                            "-p", "no:cacheprovider"],
                           cwd=workdir, capture_output=True, text=True,
                           env=dict(os.environ, PYTHONPATH=workdir))
        out = p.stdout + p.stderr
        m = re.search(r"(\d+) failed", out)
        failed = int(m.group(1)) if m else 0
        collect_err = bool(re.search(r"error(s)? during collection|ImportError|"
                                     r"ModuleNotFoundError", out))
        if collect_err and failed == 0:
            # The suite could not even load the mutated module. That is an
            # instrument fault, not evidence about the tests.
            return {"name": name, "status": "INVALID", "file": relpath,
                    "reason": "suite failed to collect — mutation broke imports"}
        return {"name": name, "status": "caught" if failed > 0 else "SURVIVED",
                "failed": failed, "file": relpath}
    finally:
        open(src, "w", encoding="utf-8").write(original)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-k", help="only mutations whose name contains this")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    before = _tree_clean()
    muts = [m for m in MUTATIONS if not args.k or args.k in m[0]]
    print(f"mutation battery: {len(muts)} mutation(s)\n")

    with tempfile.TemporaryDirectory(prefix="mutate-") as tmp:
        work = os.path.join(tmp, "repo")
        subprocess.run(["git", "worktree", "add", "-q", "--detach", work, "HEAD"],
                       cwd=ROOT, check=True, capture_output=True)
        try:
            results = [run_one(*m, work, args.verbose) for m in muts]
        finally:
            subprocess.run(["git", "worktree", "remove", "--force", work],
                           cwd=ROOT, capture_output=True)

    survived = [r for r in results if r["status"] == "SURVIVED"]
    skipped = [r for r in results if r["status"] in ("SKIP", "INVALID")]
    for r in results:
        mark = {"caught": "caught  ", "SURVIVED": "SURVIVED",
                "SKIP": "skip    ", "INVALID": "INVALID "}[r["status"]]
        extra = (f"{r.get('failed', 0)} test(s) failed" if r["status"] == "caught"
                 else r.get("reason", "no test noticed"))
        print(f"  {mark} {r['name']:<32} {extra}")

    after = _tree_clean()
    print(f"\nworking tree unchanged: {before == after}")
    if before != after:
        print("  !! the battery modified the working tree — investigate")
        return 2

    print(f"\n{len(results) - len(survived) - len(skipped)} caught, "
          f"{len(survived)} survived, {len(skipped)} skipped")
    if skipped:
        print("  skipped mutations are NOT passes — the code moved and the "
              "pattern no longer matches; update tools/mutate.py")
    if survived:
        print("\nSURVIVORS (no test noticed the implementation was broken):")
        for r in survived:
            print(f"  - {r['name']}  [{r['file']}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
