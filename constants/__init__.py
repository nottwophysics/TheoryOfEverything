"""
constants/ — VERIFICATION and consistency checks only.

This package holds physical-constant work that is honestly labelled as
verification of empirical relations or order-of-magnitude consistency checks,
NOT first-principles derivation:

  - CosmologicalConstant: the Lambda ~ 1/S order-of-magnitude note (with its own
    caveats that S ~ 10^122 is an empirical input, not derived).
  - KoideRelation: verification of the empirical Koide lepton-mass relation, plus
    its zero-free-parameter hold-out prediction of m_tau.

The fine-structure formula-fitting and the "derive constants from consciousness"
explorations have been moved to the ``numerology/`` package, which names that
activity for what it is (coincidence search / look-elsewhere).
"""

from .cosmological import CosmologicalConstant
from .koide import KoideRelation

__all__ = [
    "CosmologicalConstant",
    "KoideRelation",
]
