"""Phase-0 gate: does threshold_tpm's big-endian row order disagree with the
convention PyPhi 1.2.0 assumes for 2-D state-by-node TPMs — and if so, do the
published per-system Phi values change?

Design:
  Step 0 — determine PyPhi's convention EMPIRICALLY (no doc memory): build a
           hand-made asymmetric 2-node dynamics f, encode its TPM little-endian,
           and check pyphi.convert.to_multidimensional indexes it as f.
  Step 1 — revalidate the anchor (basic_network Phi = 2.3125).
  Step 2 — for the systems that carry section-8's weight (all nonzero-Phi rows of
           the frozen CSV) plus zero-Phi controls: compute
             phi_asis = production path (big-endian rows, as published)
             phi_le   = same dynamics, same state, rows re-indexed little-endian
           with the state fixed to the production _reachable_state, so row order
           is the ONLY difference. Compare both against the frozen CSV.
Run inside tofe-pyphi39.
"""
import csv
import itertools
import sys

REPO = "/Users/rohitchauhan/Downloads/TheoryOfEverything"
sys.path.insert(0, REPO + "/predictions")

import numpy as np
import validated_phi as vp          # sets pyphi config: parallelism OFF
import pyphi
from phi_s_systems import make_family, threshold_tpm


def be_index(s):  # node 0 = most-significant bit (threshold_tpm's enumeration)
    return int("".join(str(b) for b in s), 2)


def le_index(s):  # node 0 = least-significant bit
    return sum(b << k for k, b in enumerate(s))


def to_le(tpm_be, n):
    out = np.zeros_like(tpm_be)
    for s in itertools.product((0, 1), repeat=n):
        out[le_index(s)] = tpm_be[be_index(s)]
    return out


# ---- Step 0: PyPhi's convention, determined empirically -----------------
# f: node0 copies node1; node1 always 0.  Asymmetric, so conventions differ.
f = {s: (s[1], 0.0) for s in itertools.product((0, 1), repeat=2)}
tpm_le_test = np.zeros((4, 2))
tpm_be_test = np.zeros((4, 2))
for s, out in f.items():
    tpm_le_test[le_index(s)] = out
    tpm_be_test[be_index(s)] = out
md = pyphi.convert.to_multidimensional(tpm_le_test)
le_matches = all(np.array_equal(md[s], np.array(f[s])) for s in f)
md_be = pyphi.convert.to_multidimensional(tpm_be_test)
be_matches = all(np.array_equal(md_be[s], np.array(f[s])) for s in f)
print(f"STEP0 convention: little-endian-encoding-matches-PyPhi={le_matches}, "
      f"big-endian-matches={be_matches}")

# ---- Step 1: anchor ------------------------------------------------------
checks = vp.validate()
assert checks[0]["agrees"], f"anchor FAILED: {checks[0]}"
print(f"STEP1 anchor: basic_network phi={checks[0]['computed_phi']} OK")

# ---- Step 2: recompute on the load-bearing systems -----------------------
with open(REPO + "/reproducibility/phi_s/data/phi_s_validated_results.csv") as fh:
    rows = {int(r["id"]): r for r in csv.DictReader(fh)}
fam = {s["id"]: s for s in make_family()}

nonzero_ids = [i for i, r in rows.items() if float(r["phi"]) > 1e-6]
zero_ids = [i for i, r in rows.items() if float(r["phi"]) <= 1e-6][:8]
sample = nonzero_ids + zero_ids
print(f"STEP2 sample: {len(nonzero_ids)} nonzero-phi + {len(zero_ids)} zero-phi controls")

mismatch_vs_csv = 0
diffs = []
row_order_differs = 0
le_none = 0
for i in sample:
    sysd = fam[i]
    W = np.array(sysd["W"], float)
    n = sysd["n"]
    tpm = threshold_tpm(W)
    tpm_le = to_le(tpm, n)
    if not np.array_equal(tpm, tpm_le):
        row_order_differs += 1
    state = vp._reachable_state(tpm, n, np.random.default_rng(0))  # production
    phi_asis = vp.phi_of_tpm(tpm, n, state=state)
    phi_le = vp.phi_of_tpm(tpm_le, n, state=state)
    csv_phi = float(rows[i]["phi"])
    if phi_asis is None or abs(phi_asis - csv_phi) > 1e-6:
        mismatch_vs_csv += 1
        print(f"  id={i} ({sysd['topology']},n={n}): phi_asis={phi_asis} != CSV {csv_phi}  <-- repro problem")
    if phi_le is None:
        le_none += 1
        print(f"  id={i} ({sysd['topology']},n={n}): phi_le=None (unreachable/timeout under LE)")
        continue
    d = abs((phi_asis if phi_asis is not None else np.nan) - phi_le)
    diffs.append((i, sysd["topology"], n, csv_phi, phi_le, d))
    if d > 1e-9:
        print(f"  id={i} ({sysd['topology']},n={n}): phi_asis={phi_asis:.6f}  phi_le={phi_le:.6f}  |diff|={d:.6f}")

print("\n==== SUMMARY ====")
print(f"systems checked: {len(sample)}; TPMs where row order differs: {row_order_differs}")
print(f"production-path reproduces frozen CSV: {'YES' if mismatch_vs_csv == 0 else f'NO ({mismatch_vs_csv} mismatches)'}")
nz = [d for d in diffs if d[3] > 1e-6]
changed = [d for d in diffs if d[5] > 1e-9]
print(f"phi_le=None cases: {le_none}")
print(f"systems where phi changes under correct-convention encoding: {len(changed)}/{len(diffs)}")
if changed:
    mx = max(changed, key=lambda d: d[5])
    print(f"max |delta phi| = {mx[5]:.6f} at id={mx[0]} ({mx[1]}, n={mx[2]})")
    # does the falsification survive? recompute holds among nonzero-LE-phi
    viol = sum(1 for d in nz if d[4] > float(rows[d[0]]["S"]) + 1e-6)
    nz_le = sum(1 for d in nz if d[4] > 1e-6)
    print(f"of the {len(nz)} previously-nonzero systems: {nz_le} still nonzero under LE; "
          f"{viol} still violate phi<=S")
else:
    print("VERDICT: published per-system Phi values are UNCHANGED under the "
          "correct-convention encoding for every sampled system.")
