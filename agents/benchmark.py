"""
Beat-the-baselines benchmark: does |Omega| catch parity-type emergence that a
designer's standard tools miss?

Committed 2026-08-16. Both classical reports had positioned against these
baselines using AUC and Cohen's d for months while **no AUC, ROC or Cohen's-d
computation existed anywhere in the tree** -- the result artifacts had been
lost and the reports said so, but they did not say the computation itself was
absent, so the "decisive test" was unrunnable by any reader. This module makes
it runnable.

WHAT THE AUC HERE DOES AND DOES NOT MEAN
----------------------------------------
For the noiseless parity construction the separation is **deterministic by
construction**, not an empirical discovery: in the synergistic regime the last
bit IS the parity of the others, so O-information is bounded away from zero,
while in the independent regime every column is an independent coin and the
population O-information is exactly zero. An AUC of 1.00 is therefore the
*expected* outcome and confirms the estimator behaves as derived -- it is not
evidence that the detector would separate emergence in the wild.

Total correlation reaches AUC 1.00 on this benchmark too. That is disclosed
here rather than omitted: |Omega| is NOT distinguished from TC by separation
on this task. What distinguishes them is the SIGN of Omega -- but only on a
comparison that holds TC fixed, since at the default redundancy noise TC
separates synergy from redundancy perfectly well (in reverse order). See
`sign_separation()`, which matches the two regimes on TC first.

Cohen's d is deliberately NOT computed. On this construction the within-group
spread shrinks with sample count while the between-group gap does not, so d
grows without bound in the number of samples per instance and reports a
property of the protocol rather than of the detector. The figure that
previously circulated (d ~ 68) is a sample-count artifact and must not be
cited.
"""
from __future__ import annotations

import numpy as np

from .emergence_detector import measures
from .multiagent_testbed import independent, synergistic

SEED = 42


def _auc(pos: np.ndarray, neg: np.ndarray) -> float:
    """
    Rank-statistic AUC (Mann-Whitney U / n1*n2), ties counted as half.

    Equivalent to P(score(pos) > score(neg)) + 0.5 * P(equal).
    """
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    allv = np.concatenate([pos, neg])
    order = allv.argsort()
    ranks = np.empty(len(allv), float)
    ranks[order] = np.arange(1, len(allv) + 1)
    # average ranks within tie groups
    _, inv, counts = np.unique(allv, return_inverse=True, return_counts=True)
    sums = np.zeros(len(counts))
    np.add.at(sums, inv, ranks)
    ranks = (sums / counts)[inv]
    n1, n2 = len(pos), len(neg)
    return float((ranks[:n1].sum() - n1 * (n1 + 1) / 2) / (n1 * n2))


def _metrics(samples: np.ndarray) -> dict:
    """The detector's statistic plus the three baselines a designer already has."""
    m = measures(samples)
    corr = np.corrcoef(samples, rowvar=False)
    off = corr[~np.eye(corr.shape[0], dtype=bool)]
    off = np.abs(np.nan_to_num(off))
    return {
        "abs_o_information": abs(m["o_information"]),
        "total_correlation": m["total_correlation"],
        "max_abs_pairwise_corr": float(off.max()),
        "mean_abs_pairwise_corr": float(off.mean()),
        "max_per_agent_variance": float(samples.var(axis=0).max()),
    }


def run_benchmark(n_instances: int = 100, n: int = 4,
                  n_samples: int = 4000, seed: int = SEED) -> dict:
    """
    Score each metric by its AUC separating the synergistic regime from the
    independent regime, over `n_instances` seeded instances per regime.
    """
    rng = np.random.default_rng(seed)
    pos = [_metrics(synergistic(n, n_samples, rng)) for _ in range(n_instances)]
    neg = [_metrics(independent(n, n_samples, rng)) for _ in range(n_instances)]

    keys = list(pos[0])
    aucs = {k: _auc(np.array([p[k] for p in pos]),
                    np.array([q[k] for q in neg])) for k in keys}
    return {
        "n_instances_per_regime": n_instances,
        "n_agents": n,
        "n_samples_per_instance": n_samples,
        "seed": seed,
        "auc": aucs,
        "separation_is_by_construction": True,
        "total_correlation_also_separates": aucs["total_correlation"] >= 0.99,
        "cohens_d_not_computed": (
            "d grows without bound in n_samples on this construction; the "
            "previously circulated d ~ 68 is a sample-count artifact"),
    }


# Redundancy noise at which total correlation matches the parity construction's
# TC (~1.0 bit for n=4). Found by bisection; see `find_tc_matched_noise()`.
TC_MATCHED_NOISE = 0.1195


def find_tc_matched_noise(n: int = 4, n_samples: int = 4000, seed: int = 1,
                          reps: int = 12, iters: int = 18) -> float:
    """Bisect for the redundancy noise whose TC equals the parity regime's."""
    from .multiagent_testbed import redundant
    rng = np.random.default_rng(seed)
    lo, hi = 0.01, 0.49
    for _ in range(iters):
        mid = (lo + hi) / 2
        tc = np.mean([measures(redundant(n, n_samples, rng, noise=mid))["total_correlation"]
                      for _ in range(reps)])
        lo, hi = (mid, hi) if tc > 1.0 else (lo, mid)
    return round((lo + hi) / 2, 4)


def sign_separation(n_instances: int = 40, n: int = 4, n_samples: int = 4000,
                    seed: int = SEED, noise: float = TC_MATCHED_NOISE) -> dict:
    """
    What Omega buys over total correlation: the SIGN, on a FAIR comparison.

    An earlier version of this compared parity against the default redundant
    regime and reported that TC "cannot tell them apart". That was wrong: at
    the default noise TC separates the two perfectly, just in reverse order
    (AUC 0.0), because redundancy at noise 0.1 happens to carry more total
    correlation than parity does.

    The honest test holds the baseline's own statistic fixed. At
    `TC_MATCHED_NOISE` the two regimes have the SAME total correlation, so TC
    is at chance between them -- and Omega's sign still separates them
    completely, because synergy and redundancy sit on opposite sides of zero.
    That is the differentiator worth citing, not the AUC in `run_benchmark`,
    which both statistics reach by construction.

    Scope: the sign claim holds where redundancy is actually present. In the
    noise-dominated limit (noise -> 0.5) both regimes collapse toward
    O = 0 and the sign is no longer meaningful.
    """
    from .multiagent_testbed import redundant
    rng = np.random.default_rng(seed)
    syn = [measures(synergistic(n, n_samples, rng)) for _ in range(n_instances)]
    red = [measures(redundant(n, n_samples, rng, noise=noise)) for _ in range(n_instances)]

    o_syn = np.array([m["o_information"] for m in syn])
    o_red = np.array([m["o_information"] for m in red])
    tc_syn = np.array([m["total_correlation"] for m in syn])
    tc_red = np.array([m["total_correlation"] for m in red])

    return {
        "redundancy_noise_tc_matched": noise,
        "mean_tc_synergistic": float(tc_syn.mean()),
        "mean_tc_redundant": float(tc_red.mean()),
        "tc_distributions_overlap": bool(tc_syn.min() < tc_red.max()
                                         and tc_red.min() < tc_syn.max()),
        "tc_auc_synergy_vs_redundancy": _auc(tc_syn, tc_red),
        "mean_omega_synergistic": float(o_syn.mean()),
        "mean_omega_redundant": float(o_red.mean()),
        "omega_synergistic_all_negative": bool((o_syn < 0).all()),
        "omega_redundant_all_positive": bool((o_red > 0).all()),
        "omega_sign_separates": bool((o_syn < 0).all() and (o_red > 0).all()),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_benchmark(), indent=2))
    print(json.dumps(sign_separation(), indent=2))
