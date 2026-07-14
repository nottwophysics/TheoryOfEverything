"""
numerology/ — coincidence-search explorations, honestly labelled.

This package holds the fine-structure formula-fitting (v1/v2/v3), the
"derive constants from consciousness" explorations (ConstantsFromConsciousness),
and the diagnostics that quantify *why* such number-matching carries no
predictive content:

  - LookElsewhereAnalysis: how many equally-complex formulas hit a target by
    chance (trials factor / multiple-comparisons correction).
  - CrossValidation: whether a formula 'rule' fit on one constant predicts a
    second with no re-tuning (it does not).

These modules were moved here from ``constants/`` so the package name matches the
activity: this is coincidence search, not derivation. Genuine verification work
(Koide, Lambda consistency) lives in ``constants/``.
"""
from .look_elsewhere import LookElsewhereAnalysis, PHYSICS_CONSTANTS  # noqa: F401
from .cross_validation import CrossValidation  # noqa: F401
from .fine_structure import FineStructureDerivation  # noqa: F401
from .fine_structure_v2 import FineStructureV2  # noqa: F401
from .fine_structure_v3 import FineStructureV3  # noqa: F401
from .derivation import ConstantsFromConsciousness  # noqa: F401
