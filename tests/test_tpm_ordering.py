"""Regression tests for the TPM state-ordering boundary (2026-08-12 audit).

`threshold_tpm` enumerates rows big-endian (node 0 = MSB of the row index);
PyPhi reads 2-D state-by-node TPMs little-endian (node 0 = LSB). Feeding
big-endian rows to PyPhi analyzes a convention-scrambled system — the audit
measured Φ shifts up to ~1.6 bits on the published N=216 family. These tests
pin the numpy side of the fix (`phi_s_systems.to_little_endian`); the in-env
PyPhi side is pinned by `validated_phi.validate()`'s ordering self-test.
"""

import itertools

import numpy as np
import pytest

from predictions.phi_s_systems import make_family, threshold_tpm, to_little_endian


def _be(s):
    return int("".join(str(b) for b in s), 2)


def _le(s):
    return sum(b << k for k, b in enumerate(s))


def test_reindex_matches_hand_computed_two_node_case():
    # f: node0 copies node1; node1 always off. Asymmetric under bit reversal.
    f = {s: (float(s[1]), 0.0) for s in itertools.product((0, 1), repeat=2)}
    tpm_be = np.zeros((4, 2))
    for s, out in f.items():
        tpm_be[_be(s)] = out
    tpm_le = to_little_endian(tpm_be)
    for s, out in f.items():
        assert np.array_equal(tpm_le[_le(s)], np.array(out))


def test_reindex_is_a_row_permutation():
    rng = np.random.default_rng(42)
    for n in (2, 3, 4):
        tpm = rng.random((2 ** n, n))
        out = to_little_endian(tpm)
        # same multiset of rows, and applying the map twice returns the original
        # (bit-reversal is an involution on indices)
        assert sorted(map(tuple, tpm)) == sorted(map(tuple, out))
        assert np.allclose(to_little_endian(out), tpm)


def test_reindex_fixes_palindromic_states_and_moves_asymmetric_ones():
    n = 3
    tpm = np.arange(2 ** n * n, dtype=float).reshape(2 ** n, n)
    out = to_little_endian(tpm)
    for s in itertools.product((0, 1), repeat=n):
        assert np.array_equal(out[_le(s)], tpm[_be(s)])
        if s == tuple(reversed(s)):
            assert _le(s) == _be(s)


def test_family_tpms_actually_differ_under_reindex():
    # The audit's premise: for asymmetric couplings the two encodings disagree.
    fam = make_family()
    differing = sum(
        1
        for sysd in fam[:60]
        if not np.array_equal(
            threshold_tpm(np.array(sysd["W"])),
            to_little_endian(threshold_tpm(np.array(sysd["W"]))),
        )
    )
    assert differing > 0, "reindex is a no-op on every sampled system — audit premise broken"
