# Decoherence-threshold calculator

**Roadmap item:** P3 — turn the framework's P2 decoherence claim into a
quantitative tool with real physics.

## Motivation
`predictions/testable.py` claims a gravitational (Diósi–Penrose) decoherence
mass threshold. That is only half the story: an object shows interference only
if the DP collapse time is shorter than **every environmental decoherence
time** (gas collisions, thermal photons) *and* still long enough to run an
experiment. A collapse-model signature is observable only in the narrow
mass/pressure/temperature window where gravity wins. This module computes all
three channels and finds that window.

## Physics (all references verified via CrossRef)
| channel | formula | reference |
|---|---|---|
| Gravitational (DP) | τ = ħ / ΔE_grav, ΔE_grav = uniform-sphere self-energy of the branch difference (closed form) | Diósi 1989 `10.1103/PhysRevA.40.1165`; Penrose 1996 `10.1007/BF02105068` |
| Gas collisions | τ = 1/(n v̄ σ), n = P/k_BT, v̄ = √(8k_BT/πm_gas), σ = πR² | Joos & Zeh 1985 `10.1007/BF01725541` |
| Thermal photons | τ = 1/(Λ Δx²), Λ = 8.55 ζ(9) c R⁶ (k_BT/ħc)⁹ (Rayleigh regime) | Schlosshauer 2005 `10.1103/RevModPhys.76.1267` |
| Overview | formula collection & collapse-model context | Bassi et al. 2013 `10.1103/RevModPhys.85.471` |

**Validation checks (in the test suite):**
- DP self-energy → 0 as Δx → 0 and saturates to (7/5)Gm²/R at Δx = 2R (exact analytic limits).
- A 10 pg osmium sphere (10⁻¹⁴ kg) gives τ_DP ≈ 5 ms (correct literature scale).
- A 10 µm grain at 300 K gives τ_photon ≈ 10⁻¹⁶ s, matching the Joos–Zeh table.

## Key result — gravity almost never wins at room temperature
For a representative solid-density nanosphere (ρ = 2000 kg/m³):

- **Room temperature (300 K), 10⁻¹⁰ mbar:** thermal photons dominate across the
  entire 10⁻¹⁷–10⁻⁸ kg range. There is **no mass** at which the DP channel is
  the fastest, so a collapse model cannot be tested — the environment hides it.
  This is exactly why matter-wave / levitated-optomechanics proposals
  (MAQRO-class) demand cryogenic temperatures.
- **Cryogenic (4 K), 10⁻¹³ mbar:** a DP-dominant, experimentally-accessible
  window opens at **~4×10⁻¹⁵ to 4×10⁻¹⁴ kg** (35 masses on the scan grid). The
  upper edge is where τ_DP drops below the 1 ms experiment time.
- **Colder still (0.1 K, 10⁻¹⁶ mbar):** the window widens to ~3×10⁻¹⁷–4×10⁻¹⁴ kg.

The discriminating mass scale is therefore **~10⁻¹⁴ kg, and only under
cryogenic extreme-vacuum conditions** — a concrete, quantitative sharpening of
the framework's vague "objects above a threshold decohere" claim.

## Reproducibility
- `predictions/decoherence_calculator.py` — `DecoherenceCalculator`,
  per-channel τ functions, and `discriminating_window`.
- `tests/test_decoherence_calculator.py` (8 tests) — physics-limit checks +
  the room-vs-cryogenic window result.
- Figure: `decoherence_envelopes.png` (τ-vs-mass, both regimes, DP window shaded).
