"""Pins the Φ ≤ S figures that previously had no producer in the tree.

The two-sided permutation p for the hold rate (0.21), the 34 distinct
dynamics, and the ≈1-bit entropy reached only as h → 0 are all printed by the
manuscript. Each test also checks that the producer can give a different
answer, so a green run means something.
"""
import csv
import json
import subprocess
import sys

import numpy as np

from predictions.phi_s_family_checks import distinct_dynamics, entropy_sweep
from predictions.phi_s_systems import make_family

CSV = "reproducibility/phi_s/data/phi_s_validated_results.csv"


def _verdict(csv_path, tmp_path, nperm=2000):
    out = tmp_path / "verdict.json"
    subprocess.run([sys.executable, "predictions/phi_s_verdict.py", "--csv", str(csv_path),
                    "--nperm", str(nperm), "--out", str(out)],
                   check=True, capture_output=True, env={"PYTHONPATH": "."})
    return json.loads(out.read_text())


class TestHoldRatePermutationP:
    def test_reported_p_reproduces(self, tmp_path):
        res = _verdict(CSV, tmp_path, nperm=10000)
        assert res["hold_rate_vs_null_p_two_sided"] == 0.208
        assert round(res["hold_rate_vs_null_p_two_sided"], 2) == 0.21

    def test_p_falls_when_the_hold_rate_departs_from_the_null(self, tmp_path):
        # Same S column, Φ set to track S just below it: the bound now holds
        # for the true pairing far more often than under shuffling.
        rows = list(csv.DictReader(open(CSV)))
        for r in rows:
            r["phi"] = str(max(float(r["S"]) - 1e-3, 0.0))
        fake = tmp_path / "fake.csv"
        with open(fake, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader(); w.writerows(rows)
        res = _verdict(fake, tmp_path)
        assert res["hold_rate_phi_le_S"] == 1.0
        assert res["hold_rate_vs_null_p_two_sided"] < 0.01


class TestDistinctDynamics:
    def test_reported_count(self):
        res = distinct_dynamics(make_family())
        assert res["n_systems"] == 216
        assert res["distinct_dynamics"] == 34
        assert res["distinct_dynamics_by_n"] == {3: 8, 4: 26}

    def test_count_is_scale_invariant_but_not_constant(self):
        fam = make_family()
        scaled = [{**s, "W": (2.5 * np.array(s["W"])).tolist()} for s in fam]
        assert distinct_dynamics(scaled)["distinct_dynamics"] == 34
        # An inhibitory copy of a fully connected system is a new dynamic, so
        # the count can move.
        extra = {**fam[190], "id": 999, "W": (-np.array(fam[190]["W"])).tolist()}
        assert distinct_dynamics(fam + [extra])["distinct_dynamics"] == 35


class TestEntropyAcrossFields:
    def test_reported_h_value(self):
        res = entropy_sweep(make_family(), 1.0, 1.0, 0.01)
        assert res["max_S_at_reported_h"] == 0.8332
        assert res["max_S_over_grid"] == 0.8332

    def test_saturates_near_one_bit_at_small_h(self):
        res = entropy_sweep(make_family(), 0.01, 0.10, 0.01)
        assert res["max_S_over_grid"] == 1.0003
        assert res["argmax_h"] == 0.03
        # The excess over 1 bit lives where the ground state is near-degenerate.
        assert res["spectral_gap_at_argmax"] < 1e-3

    def test_maximum_rises_as_the_field_falls_and_stays_far_from_two_bits(self):
        fam = make_family()
        at = {h: entropy_sweep(fam, h, h, 0.01)["max_S_over_grid"] for h in (2.0, 1.0, 0.5)}
        assert at[2.0] < at[1.0] < at[0.5] < 1.0
        assert at[1.0] == 0.8332
        assert entropy_sweep(fam, 0.01, 2.0, 0.05)["max_S_over_grid"] < 1.01
