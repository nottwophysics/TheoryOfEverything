"""
Koide Relation — Verification (NOT a derivation)
================================================

The Koide relation is an empirical near-coincidence among the charged-lepton
masses:

    Q = (m_e + m_mu + m_tau) / (sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2  ~=  2/3

Reference: Y. Koide, "New view of quark and lepton mass hierarchy,"
*Phys. Rev. Lett.* 47, 1241 (1981), DOI 10.1103/PhysRevLett.47.1241
(citation verified via CrossRef).

This module *verifies* the relation against measured masses and demonstrates its
one genuinely predictive feature (fix Q = 2/3 and two masses, predict the third
with zero free parameters). It does NOT claim to derive Q = 2/3 from any deeper
principle — the origin of the relation is unexplained, and this framework does
not explain it. The module is placed in ``constants/`` (verification) rather than
``numerology/`` (coincidence search) precisely because a zero-free-parameter
cross-constant prediction is a real, falsifiable check, unlike the fine-structure
formula-fitting.

PDG 2020 charged-lepton masses (MeV) are used as inputs.
"""

from __future__ import annotations

import numpy as np

# PDG central values (MeV)
M_E = 0.51099895
M_MU = 105.6583755
M_TAU = 1776.86

KOIDE_TARGET = 2.0 / 3.0
KOIDE_DOI = "10.1103/PhysRevLett.47.1241"


class KoideRelation:
    """Verify the Koide relation and its zero-parameter predictive content."""

    def __init__(self, m_e: float = M_E, m_mu: float = M_MU, m_tau: float = M_TAU):
        self.m_e = m_e
        self.m_mu = m_mu
        self.m_tau = m_tau

    def q_value(self) -> dict:
        """Compute Q from the three measured masses and compare to 2/3."""
        num = self.m_e + self.m_mu + self.m_tau
        den = (np.sqrt(self.m_e) + np.sqrt(self.m_mu) + np.sqrt(self.m_tau)) ** 2
        q = num / den
        return {
            "Q_computed": float(q),
            "Q_target": KOIDE_TARGET,
            "abs_error": float(abs(q - KOIDE_TARGET)),
            "rel_error_pct": float(abs(q - KOIDE_TARGET) / KOIDE_TARGET * 100),
            "holds_to_1e-3": bool(abs(q - KOIDE_TARGET) < 1e-3),
            "citation": KOIDE_DOI,
            "status": (
                "VERIFICATION of an empirical relation, not a derivation. "
                "Q = 2/3 is not explained by this framework."
            ),
        }

    def predict_tau(self) -> dict:
        """
        Hold-out prediction: fix Q = 2/3 and (m_e, m_mu), solve for m_tau with
        ZERO free parameters, and compare to the measured value. This is the
        falsifiable, cross-constant content of the relation.
        """
        A = np.sqrt(self.m_e) + np.sqrt(self.m_mu)
        # (m_e + m_mu + s^2) = (2/3)(A + s)^2, with s = sqrt(m_tau)
        a = 1.0 - 2.0 / 3.0
        b = -(4.0 / 3.0) * A
        c = (self.m_e + self.m_mu) - (2.0 / 3.0) * A ** 2
        disc = b * b - 4 * a * c
        m_tau_pred = max(((-b + np.sqrt(disc)) / (2 * a)) ** 2,
                         ((-b - np.sqrt(disc)) / (2 * a)) ** 2)
        return {
            "m_tau_predicted_MeV": float(m_tau_pred),
            "m_tau_measured_MeV": self.m_tau,
            "rel_error_pct": float(abs(m_tau_pred - self.m_tau) / self.m_tau * 100),
            "free_parameters": 0,
            "citation": KOIDE_DOI,
        }

    def run_all(self) -> dict:
        return {"q_value": self.q_value(), "tau_prediction": self.predict_tau()}


if __name__ == "__main__":
    k = KoideRelation()
    q = k.q_value()
    p = k.predict_tau()
    print("Koide relation — VERIFICATION (not derivation)")
    print(f"  Q = {q['Q_computed']:.8f}  vs  2/3 = {q['Q_target']:.8f}  "
          f"(err {q['rel_error_pct']:.4f}%)")
    print(f"  hold-out: predict m_tau from m_e, m_mu, Q=2/3 (0 free params)")
    print(f"    predicted {p['m_tau_predicted_MeV']:.2f} MeV, "
          f"measured {p['m_tau_measured_MeV']:.2f} MeV "
          f"(err {p['rel_error_pct']:.4f}%)")
    print(f"  citation: {KOIDE_DOI} (Koide, PRL 47, 1241, 1981)")
