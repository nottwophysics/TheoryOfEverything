#!/usr/bin/env bash
# Reproduce every §8 (Phi <= S) number from the frozen results table.
# No PyPhi needed here (that is the upstream Phi/S generation; see README.md).
# Run from the repo root:  bash reproducibility/phi_s/reproduce.sh
set -euo pipefail

CSV="reproducibility/phi_s/data/phi_s_validated_results.csv"

echo "############################################################"
echo "# 1/2  Phi <= S falsification  (predictions/phi_s_verdict.py)"
echo "############################################################"
PYTHONPATH=. python predictions/phi_s_verdict.py --csv "$CSV"

echo
echo "############################################################"
echo "# 2/2  Phi-S connectivity confound  (predictions/partial_corr_phi_s.py)"
echo "############################################################"
PYTHONPATH=. python predictions/partial_corr_phi_s.py --csv "$CSV"
