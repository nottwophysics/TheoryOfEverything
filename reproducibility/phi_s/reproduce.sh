#!/usr/bin/env bash
# Reproduce every §8 (Phi <= S) number from the frozen results table.
# No PyPhi needed here (that is the upstream Phi/S generation; see README.md).
# Run from the repo root:  bash reproducibility/phi_s/reproduce.sh
set -euo pipefail

CSV="reproducibility/phi_s/data/phi_s_validated_results.csv"

# Interpreter resolution. Needs numpy + scipy, so prefer an explicit $PYTHON,
# then the repo's own venv, then python3. (A bare `python` is absent on many
# systems, which previously made this script exit 127 without producing any
# numbers.)
if [ -n "${PYTHON:-}" ]; then PY="$PYTHON"
elif [ -x "./toenv/bin/python" ]; then PY="./toenv/bin/python"
else PY="python3"; fi
echo "# interpreter: $PY"
"$PY" -c 'import numpy, scipy' 2>/dev/null || {
  echo "ERROR: $PY lacks numpy/scipy. Activate the venv, or set PYTHON=/path/to/python." >&2
  exit 1
}

echo "############################################################"
echo "# 1/2  Phi <= S falsification  (predictions/phi_s_verdict.py)"
echo "############################################################"
PYTHONPATH=. "$PY" predictions/phi_s_verdict.py --csv "$CSV"

echo
echo "############################################################"
echo "# 2/2  Phi-S connectivity confound  (predictions/partial_corr_phi_s.py)"
echo "############################################################"
PYTHONPATH=. "$PY" predictions/partial_corr_phi_s.py --csv "$CSV"
