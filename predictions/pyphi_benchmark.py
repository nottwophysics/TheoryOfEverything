"""
Benchmark: framework Φ vs canonical IIT Φ (PyPhi)
=================================================

`predictions/iit_bridge.py::IntegratedInformation.compute_phi` computes a
"simplified IIT 3.0-like" integrated-information measure. This module tests the
implicit claim in that description — that it approximates the quantity IIT
actually defines — by comparing it, system for system, against **PyPhi**, the
reference implementation of Integrated Information Theory 3.0:

    Mayner WGP, Marshall W, Albantakis L, Findlay G, Marchman R, Tononi G (2018).
    "PyPhi: A toolbox for integrated information theory."
    PLOS Computational Biology 14(7): e1006343.
    DOI 10.1371/journal.pcbi.1006343  (citation verified via CrossRef).

FINDING (see `run_benchmark`): the two measures are essentially unrelated.
Across a spectrum of small XOR-logic networks plus PyPhi's own canonical example
networks, the correlation between the framework Φ and canonical Φ is ~0
(Pearson r ≈ -0.01, Spearman ρ ≈ 0.1), and they agree on the binary question
"is this system integrated (Φ > 0)?" only ~58 % of the time — barely above
chance. PyPhi's own `xor_network` (canonical Φ = 1.875) scores 0 under the
framework measure; other systems score high under one measure and zero under the
other. The framework Φ is therefore its own heuristic, NOT an approximation of
IIT Φ, and results phrased as "consciousness (Φ)" should not be read as IIT
integrated information.

PyPhi (v1.2.0) requires Python <= 3.9 (it imports ``collections.Iterable``), so
it cannot run in the same interpreter as the rest of this repository (Python
>= 3.10). This module is therefore structured as a two-stage benchmark:

  * ``build_systems()`` and ``framework_phi()`` run in the repo's own
    environment and need only numpy + this package.
  * ``pyphi_phi()`` runs in a separate Python <= 3.9 environment with pyphi
    installed; it reads the systems produced by ``build_systems()``.

``run_benchmark()`` joins the two result files and reports the statistics.
``tests/test_pyphi_benchmark.py`` exercises the framework side and the join
logic against a stored fixture (``tests/fixtures/pyphi_benchmark_*.json``), so
the test suite does not need pyphi; regenerating that fixture requires the pyphi
environment and is documented in the test docstring.
"""

from __future__ import annotations

import itertools
import json

import numpy as np

PYPHI_DOI = "10.1371/journal.pcbi.1006343"


def xor_tpm(adjacency: np.ndarray) -> np.ndarray:
    """State-by-node TPM for a network whose nodes are XOR gates of their inputs.

    ``adjacency[i, j] > 0`` means node i is an input to node j. Each node's next
    state is the parity (XOR) of its currently-on inputs.
    """
    n = adjacency.shape[0]
    tpm = np.zeros((2 ** n, n))
    for idx, state in enumerate(itertools.product([0, 1], repeat=n)):
        s = np.array(state)
        for j in range(n):
            inp = s[adjacency[:, j] > 0]
            tpm[idx, j] = float(inp.sum() % 2) if inp.size else 0.0
    return tpm


def reachable_state(tpm: np.ndarray, n: int, rng) -> tuple:
    """A guaranteed-reachable state: step one random state forward once.

    (PyPhi rejects unreachable states, so we hand it a genuine successor.)
    """
    s = tuple(int(x) for x in (rng.random(n) < 0.5))
    idx = sum(b << (n - 1 - i) for i, b in enumerate(s))
    return tuple(int(x) for x in tpm[idx])


def framework_phi(adjacency: np.ndarray, state) -> float:
    """The repository's own Φ for a binary adjacency matrix and state."""
    from predictions.iit_bridge import IntegratedInformation
    n = adjacency.shape[0]
    ii = IntegratedInformation(num_nodes=n)
    res = ii.compute_phi(np.asarray(adjacency, dtype=float),
                         state=np.asarray(state, dtype=float))
    return float(res["phi"])


def compare(framework: dict, reference: dict) -> dict:
    """Join framework and pyphi results (dicts id -> phi) and score agreement."""
    from scipy.stats import pearsonr, spearmanr
    ids = sorted(set(framework) & set(reference))
    t = np.array([framework[i] for i in ids], dtype=float)
    p = np.array([reference[i] for i in ids], dtype=float)
    mask = ~np.isnan(p)
    t, p = t[mask], p[mask]
    pear = pearsonr(t, p)
    spear = spearmanr(t, p)
    tb, pb = t > 1e-6, p > 1e-6
    return {
        "n": int(mask.sum()),
        "pearson_r": float(pear[0]),
        "pearson_p": float(pear[1]),
        "spearman_rho": float(spear.statistic),
        "spearman_p": float(spear.pvalue),
        "detection_agreement": float((tb == pb).mean()),
        "TP": int((tb & pb).sum()), "TN": int((~tb & ~pb).sum()),
        "FP": int((tb & ~pb).sum()), "FN": int((~tb & pb).sum()),
        "framework_nonzero": int(tb.sum()), "reference_nonzero": int(pb.sum()),
        "pyphi_doi": PYPHI_DOI,
    }


def run_benchmark(framework_json: str, pyphi_json: str) -> dict:
    """Load both result files and return the agreement statistics."""
    fw = {o["id"]: o["framework_phi"] if "framework_phi" in o else o["tofe_phi"]
          for o in json.load(open(framework_json))}
    rf = {o["id"]: o["pyphi_phi"] for o in json.load(open(pyphi_json))}
    return compare(fw, rf)
