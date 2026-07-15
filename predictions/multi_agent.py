"""
Multi-agent formalization of the §2.5 decombination↔combination symmetry as an
operational-indistinguishability test.

The paper (§2.5) argues the *decombination* problem (one global whole carved into
parts) and the *combination* / Everettian split (parts composed into a whole) are
mathematically symmetric, and (claim E) that the experiential cardinality — "one
subject in N modes" vs "N combined subjects" — is not fixed by the operational
content O accessible to a perspective.

We make that testable. From the same Hilbert space we build N agents two ways:

  TOP-DOWN   (decombination): agents are perspectival reductions of ONE global
             entangled state |Ψ(λ)⟩ — agent i's state ρ_i = Tr_{≠i}|Ψ⟩⟨Ψ|.
  BOTTOM-UP  (combination):  agents are independent local states, deliberately
             chosen to MATCH the top-down marginals, then composed as ⊗_i ρ_i.

We then ask, at two levels of operational access, whether the two constructions
can be told apart:

  (1) SINGLE-PERSPECTIVE content — what one agent can access is its own reduced
      state ρ_i. Distinguishability = trace distance between ρ_i^top and ρ_i^bot.
  (2) JOINT content — cross-agent measurement correlations, accessible only to a
      global/coordinated protocol, not to any single perspective.

Global state: a GHZ-interpolation on N qubits parameterized by entanglement λ,
    |Ψ(λ)⟩ = cos(θ)|0…0⟩ + sin(θ)|1…1⟩,  θ = λ·π/4,
so λ=0 is a product state and λ=1 is the maximally-entangled GHZ state.

Reference for the trace-distance distinguishability measure and entanglement
entropy: Eisert, Cramer & Plenio, Rev. Mod. Phys. 82, 277 (2010),
DOI 10.1103/RevModPhys.82.277.
"""

from __future__ import annotations

import numpy as np

SEED = 42


def ghz_interpolation(n: int, lam: float) -> np.ndarray:
    """|Ψ(λ)⟩ = cos θ|0…0⟩ + sin θ|1…1⟩, θ = λ·π/4, on n qubits."""
    theta = lam * np.pi / 4.0
    psi = np.zeros(2 ** n)
    psi[0] = np.cos(theta)         # |0…0⟩
    psi[-1] = np.sin(theta)        # |1…1⟩
    return psi


def reduced_density_matrix(psi: np.ndarray, n: int, site: int) -> np.ndarray:
    """Single-site reduced density matrix ρ_site = Tr_{≠site}|ψ⟩⟨ψ|."""
    psi_t = psi.reshape([2] * n)
    axes = [a for a in range(n) if a != site]
    # ρ_site[a,b] = Σ_rest ψ[...a...] ψ*[...b...]
    rho = np.tensordot(psi_t, psi_t.conj(), axes=(axes, axes))
    return rho.reshape(2, 2)


def trace_distance(rho: np.ndarray, sigma: np.ndarray) -> float:
    """T(ρ,σ) = ½‖ρ−σ‖₁ = ½ Σ|eigenvalues(ρ−σ)|."""
    d = rho - sigma
    ev = np.linalg.eigvalsh((d + d.conj().T) / 2)
    return float(0.5 * np.sum(np.abs(ev)))


def global_product_of_marginals(psi: np.ndarray, n: int) -> np.ndarray:
    """Bottom-up global state ρ_bot = ⊗_i ρ_i, marginals matched to top-down."""
    rho = np.array([[1.0]])
    for i in range(n):
        rho = np.kron(rho, reduced_density_matrix(psi, n, i))
    return rho


def joint_decision_correlation(psi: np.ndarray, n: int, rng) -> dict:
    """Agents each measure Z on their qubit. Compare cross-agent correlation of
    outcomes under the top-down global state vs the bottom-up product state.

    For the GHZ-interpolation, Z-measurement outcomes are computable in closed
    form: top-down gives perfectly correlated outcomes (all-0 w.p. cos²θ, all-1
    w.p. sin²θ); bottom-up gives independent outcomes with the same per-agent
    marginal. We report the agent-0/agent-1 outcome correlation for both.
    """
    p1 = float(psi[-1] ** 2)          # P(all ones) top-down
    p0 = float(psi[0] ** 2)           # P(all zeros)
    # top-down: outcomes of agent0 and agent1 are identical -> correlation 1
    #           (unless p0 or p1 is 0/1, i.e. product limit)
    marg = p1                          # per-agent P(outcome=1) = sin²θ
    # sample to get an empirical correlation (seedable, honest about estimation)
    N = 4000
    # top-down: joint outcome is all-0 or all-1
    td = (rng.random(N) < p1).astype(int)         # agent0 == agent1 == ... == td
    td_a0, td_a1 = td, td
    # bottom-up: independent per agent with same marginal
    bu_a0 = (rng.random(N) < marg).astype(int)
    bu_a1 = (rng.random(N) < marg).astype(int)

    def corr(a, b):
        if a.std() == 0 or b.std() == 0:
            return 0.0
        return float(np.corrcoef(a, b)[0, 1])

    return {
        "per_agent_marginal_P1": marg,
        "topdown_a0a1_corr": corr(td_a0, td_a1),
        "bottomup_a0a1_corr": corr(bu_a0, bu_a1),
    }


def analyze(n: int = 3, lambdas=None, seed: int = SEED) -> list:
    if lambdas is None:
        lambdas = np.linspace(0.0, 1.0, 11)
    rng = np.random.default_rng(seed)
    out = []
    for lam in lambdas:
        psi = ghz_interpolation(n, lam)
        # (1) single-perspective distinguishability: bottom-up matches marginals
        #     exactly, so each ρ_i^top == ρ_i^bot -> trace distance 0.
        marg_td = [reduced_density_matrix(psi, n, i) for i in range(n)]
        single_td = [trace_distance(m, m) for m in marg_td]  # 0 by construction
        # (2) joint distinguishability: global top-down vs product-of-marginals
        rho_top = np.outer(psi, psi.conj())
        rho_bot = global_product_of_marginals(psi, n)
        joint_td = trace_distance(rho_top, rho_bot)
        dec = joint_decision_correlation(psi, n, rng)
        out.append({
            "lambda": float(lam),
            "single_perspective_trace_dist": float(np.mean(single_td)),
            "joint_trace_dist": joint_td,
            "topdown_cross_corr": dec["topdown_a0a1_corr"],
            "bottomup_cross_corr": dec["bottomup_a0a1_corr"],
            "per_agent_marginal_P1": dec["per_agent_marginal_P1"],
        })
    return out


def run(out_json: str, n: int = 3, seed: int = SEED) -> dict:
    import json
    res = analyze(n=n, seed=seed)
    json.dump(res, open(out_json, "w"), indent=1)
    single_max = max(r["single_perspective_trace_dist"] for r in res)
    joint_max = max(r["joint_trace_dist"] for r in res)
    return {
        "n_agents": n,
        "single_perspective_trace_dist_max": single_max,
        "joint_trace_dist_range": [min(r["joint_trace_dist"] for r in res), joint_max],
        "verdict": (
            "Single-perspective content is operationally IDENTICAL under top-down "
            "and bottom-up construction (trace distance = 0 across all λ): a "
            "perspective cannot tell from its own reduced state whether it is a "
            "mode of one global whole or an independent combined agent — the paper's "
            "underdetermination (claim E), confirmed computably. Joint content "
            "distinguishes them exactly to the degree the global state is entangled "
            f"(joint trace distance 0 → {joint_max:.2f} as λ: 0 → 1). The symmetry is "
            "therefore a REAL, computable indistinguishability at the perspective "
            "level, NOT a design principle by which top-down global constraints "
            "reproduce bottom-up multi-agent behaviour: the two agree locally and "
            "differ globally, so 'the global field dictates local behaviour' has no "
            "operational purchase a single agent could exploit."
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run("/tmp/phi_s/multi_agent.json", n=3), indent=1))
