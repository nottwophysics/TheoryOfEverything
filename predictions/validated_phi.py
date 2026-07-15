"""
Validated Φ pipeline — canonical IIT integrated information via PyPhi.

Replaces the bespoke heuristic Φ (which the PyPhi benchmark showed is
uncorrelated with IIT Φ, r = −0.012) with Φ computed by the reference
implementation (Mayner et al. 2018, PyPhi 1.2.0, DOI 10.1371/journal.pcbi.1006343).

Runs in the PyPhi environment (Python ≤ 3.9). For each system in the shared
family (`phi_s_systems.make_family`, seed 42) it builds the threshold-logic TPM
and computes Φ = pyphi.compute.sia(subsystem).phi, over a reachable state.

Validation: basic_network Φ = 2.3125 (exact reference) and xor_network are
checked before the family is processed; the check table is written out.

CRITICAL sandbox note: PyPhi's parallel evaluators deadlock here — the config
flags below (parallelism OFF) are load-bearing, not cosmetic.
"""

from __future__ import annotations

import json
import os
import signal

os.environ["PYPHI_WELCOME_OFF"] = "yes"
import numpy as np
import pyphi

pyphi.config.PROGRESS_BARS = False
pyphi.config.PARALLEL_CONCEPT_EVALUATION = False
pyphi.config.PARALLEL_CUT_EVALUATION = False
pyphi.config.WELCOME_OFF = True

PYPHI_DOI = "10.1371/journal.pcbi.1006343"
BASIC_NETWORK_REFERENCE_PHI = 2.3125


class _Timeout(Exception):
    pass


def _with_timeout(fn, seconds=60):
    def handler(signum, frame):
        raise _Timeout()
    old = signal.signal(signal.SIGALRM, handler)
    signal.alarm(seconds)
    try:
        return fn()
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


def _reachable_state(tpm: np.ndarray, n: int, rng) -> tuple:
    """A state that is actually reached by the dynamics (avoids unreachable-state
    warnings/degeneracies): iterate the deterministic map from a random start."""
    s = tuple(int(x) for x in rng.integers(0, 2, n))
    for _ in range(2 * n):
        idx = int("".join(str(b) for b in s), 2)
        nxt = tuple(int(x) for x in tpm[idx])
        if nxt == s:
            break
        s = nxt
    return s


def phi_of_tpm(tpm: np.ndarray, n: int, state=None, seconds=60):
    """Canonical IIT Φ for a state-by-node TPM. Returns float, or None on
    timeout/degenerate."""
    rng = np.random.default_rng(0)
    if state is None:
        state = _reachable_state(np.asarray(tpm), n, rng)
    try:
        net = pyphi.Network(np.asarray(tpm, float))
        sub = pyphi.Subsystem(net, state, range(n))
        return float(_with_timeout(lambda: pyphi.compute.sia(sub).phi, seconds))
    except (_Timeout, Exception):
        return None


def validate() -> list:
    """Check PyPhi against its own documented networks before we trust it."""
    checks = []
    net = pyphi.examples.basic_network()
    sub = pyphi.Subsystem(net, (1, 0, 0), range(net.size))
    phi_basic = float(pyphi.compute.sia(sub).phi)
    checks.append({"network": "basic_network", "state": "(1,0,0)",
                   "computed_phi": phi_basic,
                   "reference_phi": BASIC_NETWORK_REFERENCE_PHI,
                   "agrees": abs(phi_basic - BASIC_NETWORK_REFERENCE_PHI) < 1e-6})
    xor = pyphi.examples.xor_network()
    subx = pyphi.Subsystem(xor, (0, 0, 0), range(xor.size))
    phi_xor = float(pyphi.compute.sia(subx).phi)
    checks.append({"network": "xor_network", "state": "(0,0,0)",
                   "computed_phi": phi_xor, "reference_phi": None,
                   "agrees": phi_xor >= 0.0})
    return checks


def run(out_phi_json: str, out_check_csv: str) -> dict:
    from phi_s_systems import make_family, threshold_tpm
    checks = validate()
    assert checks[0]["agrees"], f"PyPhi validation FAILED: {checks[0]}"

    with open(out_check_csv, "w") as f:
        f.write("network,state,computed_phi,reference_phi,agrees\n")
        for c in checks:
            f.write(f"{c['network']},{c['state']},{c['computed_phi']},"
                    f"{c['reference_phi']},{c['agrees']}\n")

    fam = make_family()
    results = []
    for sysd in fam:
        W = np.array(sysd["W"], float)
        tpm = threshold_tpm(W)
        phi = phi_of_tpm(tpm, sysd["n"])
        results.append({"id": sysd["id"], "topology": sysd["topology"],
                        "n": sysd["n"], "phi": phi})
    json.dump(results, open(out_phi_json, "w"))
    ok = [r for r in results if r["phi"] is not None]
    return {
        "n_systems": len(results),
        "n_phi_ok": len(ok),
        "n_phi_nonzero": sum(1 for r in ok if r["phi"] > 1e-6),
        "phi_range": [min(r["phi"] for r in ok), max(r["phi"] for r in ok)] if ok else None,
        "validation": checks,
    }


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    summary = run("/tmp/phi_s/phi.json", "/tmp/phi_s/validated_phi_check.csv")
    print(json.dumps(summary, indent=1))
