"""
Real binary MERA (Multiscale Entanglement Renormalization Ansatz), N=16, chi=2.

WHAT IS COMPUTED (all claims below are checked by tests/test_mera_real.py):
    - An explicit 2^16 = 65536-dimensional boundary state, built by descending
      from a 1-site top state through 4 layers of isometry adjoints (4x2,
      W^dag W = I) and 2-site disentanglers (4x4 unitaries). Every tensor is
      CONTRACTED into the state (tensordot / gate application), never applied
      as a phase.
    - Unitarity / isometry checks on every tensor (B1).
    - Perturbation response: replacing or zeroing a layer's tensors and
      measuring the actual change in the boundary state (B2 negative control).
    - Exact interval entanglement entropies from the state (Schmidt
      decomposition of the full 65536-dim vector).
    - Minimal cuts counted on the actual network graph by max-flow/min-cut,
      and the RT-type bound S(A) <= ln(chi) * |min cut| checked against the
      exact entropies (B3).
    - Mutual information between the two halves as a function of the
      entangling strength lambda, with lambda = 0 the exact product limit
      (B4 disconnection scan).

WHAT IS INTERPRETATION (not computed results):
    - The log-shaped minimal cut is a property of the MERA graph BY
      CONSTRUCTION (B5); only the inequality checked in B3 is claimed as a
      computed result about the state.
    - MERA-layer <-> AdS-radial-slice (Swingle 2012), entanglement <->
      spacetime connectivity (Van Raamsdonk 2010), and the Advaita reading
      (coarse-graining as the dissolution of Maya, the top tensor as the
      non-dual limit) are interpretive glosses on the computed structure.

Tensor construction: each unitary is exp(-i * lambda * H) for a seeded
Gaussian Hermitian generator H (exactly unitary via eigendecomposition;
generic at lambda = 1, identity at lambda = 0). Isometries are
W(lambda) = exp(-i * lambda * H4) @ W0 with W0 the product embedding
|i> -> |i>|0>, so lambda = 0 yields exactly the product state |00...0>.

History: the pre-2026-08-15 version applied its tensors only through a global
phase (a physical no-op — zeroing every tensor left the output unchanged);
the 2026-08-15 adversarial review found the module defective and it was
reimplemented the same day per REAL_PHYSICS_REIMPLEMENTATION_MEMO.md Track B.
Experiment 19's earlier claims remain retracted as evidence; only the
quantities computed here are claimed.
"""

from collections import deque

import numpy as np

# Cache of boundary states keyed by (num_sites, bond_dim, seed, lambda), so
# repeated scans over lambda (B4) and repeated test fixtures reuse the state.
_STATE_CACHE = {}

_BIG_CAPACITY = 10 ** 6  # "infinite" capacity for source/sink edges (min cut)


def _unitary_from_generator(H: np.ndarray, lam: float) -> np.ndarray:
    """exp(-i * lam * H) for Hermitian H, via eigendecomposition (exactly
    unitary up to machine precision; identity at lam = 0)."""
    w, V = np.linalg.eigh(H)
    return (V * np.exp(-1j * lam * w)) @ V.conj().T


def _hermitian_generator(rng: np.random.Generator, d: int) -> np.ndarray:
    """Seeded Gaussian Hermitian d x d generator: H = (M + M^dag)/2."""
    M = rng.standard_normal((d, d)) + 1j * rng.standard_normal((d, d))
    return (M + M.conj().T) / 2.0


class MERATensorNetwork:
    """
    Binary MERA with an explicitly constructed boundary state.

    Network (descending, top -> boundary), num_sites = 16, chi = 2:

        top state (1 site, dim 2)
          layer 0:  1 isometry adjoint (site k -> sites 2k, 2k+1), 1 disentangler
          layer 1:  2 isometries, 2 disentanglers
          layer 2:  4 isometries, 4 disentanglers
          layer 3:  8 isometries, 8 disentanglers
        boundary (16 sites, dim 65536)

    At each layer every site is split by an isometry adjoint W (4x2,
    W^dag W = I), then disentanglers (4x4 unitaries) act on the offset pairs
    (1,2), (3,4), ..., (n-1,0) (periodic), i.e. across the seams between
    isometry blocks — the standard binary-MERA wiring.

    All results are computed by contracting these tensors into the state.
    The Advaita labels (UV = fine-grained appearance, top = non-dual limit)
    are interpretation, not computation.
    """

    def __init__(self, num_sites: int = 16, bond_dim: int = 2,
                 entangling_strength: float = 1.0, seed: int = 42):
        """
        Args:
            num_sites: boundary sites, power of 2 (memo Track B uses 16).
            bond_dim: bond dimension chi. Only chi = 2 is implemented (the
                boundary dimension is chi^num_sites; chi = 2, N = 16 gives
                the memo's 65536-dim state).
            entangling_strength: lambda in [0, 1]. lambda = 0 gives exactly
                the product state |00...0> (identity limit); lambda = 1 is
                the generic network.
            seed: seed for the Gaussian generators (deterministic build).
        """
        if num_sites < 2 or (num_sites & (num_sites - 1)) != 0:
            raise ValueError("num_sites must be a power of 2, >= 2")
        if bond_dim != 2:
            raise ValueError("only bond_dim=2 is implemented (memo Track B)")

        self.num_sites = num_sites
        self.bond_dim = bond_dim
        self.entangling_strength = float(entangling_strength)
        self.seed = seed
        self.num_layers = int(np.log2(num_sites))

        # Product-embedding isometry W0: |i> -> |i>|0>  (4x2, W0^dag W0 = I)
        self._W0 = np.zeros((4, 2), dtype=np.complex128)
        self._W0[0, 0] = 1.0  # |0> -> |00>
        self._W0[2, 1] = 1.0  # |1> -> |10>

        self._build_tensors()
        self._state = None  # lazily built boundary state

    # ------------------------------------------------------------------
    # construction
    # ------------------------------------------------------------------

    def _build_tensors(self):
        """Draw seeded Hermitian generators and realize every tensor at the
        instance's lambda. Layer L has 2^L isometries and 2^L disentanglers."""
        rng = np.random.default_rng(self.seed)
        lam = self.entangling_strength

        self._top_generator = _hermitian_generator(rng, 2)
        self.top_state = _unitary_from_generator(self._top_generator, lam)[:, 0]

        self._iso_generators = []
        self._dis_generators = []
        self.isometries = []     # isometries[layer][k]: 4x2, W^dag W = I
        self.disentanglers = []  # disentanglers[layer][g]: 4x4 unitary
        for layer in range(self.num_layers):
            n = 2 ** layer
            iso_gens = [_hermitian_generator(rng, 4) for _ in range(n)]
            dis_gens = [_hermitian_generator(rng, 4) for _ in range(n)]
            self._iso_generators.append(iso_gens)
            self._dis_generators.append(dis_gens)
            self.isometries.append(
                [_unitary_from_generator(G, lam) @ self._W0 for G in iso_gens])
            self.disentanglers.append(
                [_unitary_from_generator(G, lam) for G in dis_gens])

    @staticmethod
    def _apply_isometry(psi: np.ndarray, W: np.ndarray, k: int) -> np.ndarray:
        """Contract the 4x2 isometry adjoint into site k of an n-site state:
        site k (dim 2) becomes sites k, k+1 (dim 4). Returns a 2x-longer
        vector — the tensor genuinely acts (this is the fix for the old
        global-phase defect)."""
        dim = psi.size
        rest = dim // (2 ** (k + 1))
        psi3 = psi.reshape(2 ** k, 2, rest)
        out = np.tensordot(psi3, W, axes=([1], [1]))   # (2^k, rest, 4)
        out = np.moveaxis(out, 2, 1)                   # (2^k, 4, rest)
        return out.reshape(-1)

    @staticmethod
    def _apply_two_site(psi: np.ndarray, U: np.ndarray, i: int, j: int,
                        n: int) -> np.ndarray:
        """Contract a 4x4 gate into sites (i, j) of an n-site state (handles
        the periodic wrap pair (n-1, 0))."""
        t = psi.reshape((2,) * n)
        t = np.moveaxis(t, (i, j), (0, 1))
        shp = t.shape
        m = U @ t.reshape(4, -1)
        t = m.reshape((2, 2) + shp[2:])
        t = np.moveaxis(t, (0, 1), (i, j))
        return t.reshape(-1)

    def _descend(self, top, isometries, disentanglers) -> np.ndarray:
        """Build the boundary state by explicit contraction, top -> bottom."""
        psi = np.asarray(top, dtype=np.complex128)
        n = 1
        for layer in range(self.num_layers):
            for k in reversed(range(n)):
                psi = self._apply_isometry(psi, isometries[layer][k], k)
            n *= 2
            for g in range(n // 2):
                psi = self._apply_two_site(
                    psi, disentanglers[layer][g],
                    (2 * g + 1) % n, (2 * g + 2) % n, n)
        return psi

    def boundary_state(self) -> np.ndarray:
        """The explicit 2^N boundary state (N=16: dim 65536), cached per
        (num_sites, bond_dim, seed, lambda). Norm is 1 up to machine
        precision because every tensor is an exact isometry/unitary; the
        residual is renormalized away."""
        if self._state is not None:
            return self._state
        key = (self.num_sites, self.bond_dim, self.seed,
               round(self.entangling_strength, 12))
        if key in _STATE_CACHE:
            self._state = _STATE_CACHE[key]
            return self._state
        psi = self._descend(self.top_state, self.isometries, self.disentanglers)
        psi = psi / np.linalg.norm(psi)
        _STATE_CACHE[key] = psi
        self._state = psi
        return psi

    # ------------------------------------------------------------------
    # B1 — tensor algebra
    # ------------------------------------------------------------------

    def tensor_algebra_check(self) -> dict:
        """Computed check that every disentangler is unitary (U^dag U = I)
        and every isometry satisfies W^dag W = I."""
        max_u = 0.0
        n_u = 0
        for layer in self.disentanglers:
            for U in layer:
                dev = np.max(np.abs(U.conj().T @ U - np.eye(4)))
                max_u = max(max_u, float(dev))
                n_u += 1
        max_w = 0.0
        n_w = 0
        for layer in self.isometries:
            for W in layer:
                dev = np.max(np.abs(W.conj().T @ W - np.eye(2)))
                max_w = max(max_w, float(dev))
                n_w += 1
        return {
            "num_disentanglers": n_u,
            "num_isometries": n_w,
            "max_unitarity_deviation": max_u,
            "max_isometry_deviation": max_w,
            "all_within_1e-10": bool(max_u < 1e-10 and max_w < 1e-10),
        }

    # ------------------------------------------------------------------
    # B2 — perturbation response (negative control on the old defect)
    # ------------------------------------------------------------------

    def perturbation_response(self, layer: int, mode: str = "replace",
                              replacement_seed: int = 12345) -> dict:
        """Rebuild the boundary state with one layer's tensors replaced by
        fresh random ones (mode='replace', realized at strength 1.0 so they
        are genuinely different) or by zeros (mode='zero'), and measure the
        actual change. The old defect was that this change was ~machine
        epsilon; here it is computed, not asserted.

        Returns delta_norm = ||psi' - psi||, the phase-invariant distance
        sqrt(||psi'||^2 + ||psi||^2 - 2|<psi|psi'>|) (immune to the
        global-phase loophole), and a computed state_changed flag."""
        if not (0 <= layer < self.num_layers):
            raise ValueError(f"layer must be in [0, {self.num_layers})")
        if mode not in ("replace", "zero"):
            raise ValueError("mode must be 'replace' or 'zero'")

        isos = [list(l) for l in self.isometries]
        diss = [list(l) for l in self.disentanglers]
        n = 2 ** layer
        if mode == "replace":
            rng = np.random.default_rng(replacement_seed)
            isos[layer] = [
                _unitary_from_generator(_hermitian_generator(rng, 4), 1.0)
                @ self._W0 for _ in range(n)]
            diss[layer] = [
                _unitary_from_generator(_hermitian_generator(rng, 4), 1.0)
                for _ in range(n)]
        else:  # zero — the old defect left the state unchanged under this
            isos[layer] = [np.zeros((4, 2), dtype=np.complex128)
                           for _ in range(n)]
            diss[layer] = [np.zeros((4, 4), dtype=np.complex128)
                           for _ in range(n)]

        psi = self.boundary_state()
        psi_pert = self._descend(self.top_state, isos, diss)  # NOT renormalized

        overlap = abs(np.vdot(psi, psi_pert))
        delta_norm = float(np.linalg.norm(psi_pert - psi))
        n_pert = float(np.linalg.norm(psi_pert))
        phase_inv = float(np.sqrt(max(0.0, n_pert ** 2 + 1.0 - 2.0 * overlap)))
        return {
            "layer": layer,
            "mode": mode,
            "delta_norm": delta_norm,
            "phase_invariant_distance": phase_inv,
            "overlap_modulus": float(overlap),
            "perturbed_norm": n_pert,
            "state_changed": bool(phase_inv > 1e-12),
        }

    # ------------------------------------------------------------------
    # exact entropies and network min cut
    # ------------------------------------------------------------------

    def interval_entropy(self, start: int, length: int) -> float:
        """Exact von Neumann entropy (natural log) of a contiguous interval
        of the boundary state, from the Schmidt decomposition of the full
        vector (periodic wrap allowed)."""
        n = self.num_sites
        if not (0 < length < n):
            raise ValueError("length must be in (0, num_sites)")
        psi = self.boundary_state()
        axes_a = [(start + a) % n for a in range(length)]
        t = psi.reshape((2,) * n)
        t = np.moveaxis(t, axes_a, range(length))
        m = t.reshape(2 ** length, -1)
        s = np.linalg.svd(m, compute_uv=False)
        p = s ** 2
        p = p[p > 1e-16]
        p = p / p.sum()
        return float(-np.sum(p * np.log(p)))

    def _network_edges(self):
        """The bond list of the network actually contracted in _descend:
        top -> iso[0][0]; iso[l][k] outputs slots 2k, 2k+1 which feed the
        disentangler covering that slot (pairs (2g+1, 2g+2 mod n)); each
        disentangler output feeds the next layer's isometry (or a boundary
        site at the last layer). Every edge is one chi=2 bond."""
        edges = [("top", ("iso", 0, 0))]
        L = self.num_layers
        for layer in range(L):
            n_out = 2 ** (layer + 1)
            for k in range(2 ** layer):
                for slot in (2 * k, 2 * k + 1):
                    g = ((slot - 1) % n_out) // 2
                    edges.append((("iso", layer, k), ("dis", layer, g)))
            for g in range(n_out // 2):
                for slot in (2 * g + 1, (2 * g + 2) % n_out):
                    if layer == L - 1:
                        edges.append((("dis", layer, g), ("site", slot)))
                    else:
                        edges.append((("dis", layer, g),
                                      ("iso", layer + 1, slot)))
        return edges

    @staticmethod
    def _max_flow(cap: np.ndarray, src: int, snk: int) -> int:
        """Edmonds–Karp max-flow on a dense integer capacity matrix; by
        max-flow/min-cut this equals the minimal cut (in bonds)."""
        cap = cap.copy()
        n = cap.shape[0]
        flow = 0
        while True:
            parent = np.full(n, -1, dtype=np.int64)
            parent[src] = src
            q = deque([src])
            while q and parent[snk] == -1:
                u = q.popleft()
                for v in np.nonzero(cap[u] > 0)[0]:
                    if parent[v] == -1:
                        parent[v] = u
                        q.append(v)
            if parent[snk] == -1:
                return flow
            # bottleneck along the augmenting path
            b = _BIG_CAPACITY
            v = snk
            while v != src:
                u = int(parent[v])
                b = min(b, int(cap[u, v]))
                v = u
            v = snk
            while v != src:
                u = int(parent[v])
                cap[u, v] -= b
                cap[v, u] += b
                v = u
            flow += b

    def minimal_cut(self, start: int, length: int) -> int:
        """Minimal number of chi=2 bonds whose removal separates the interval's
        boundary sites from the rest, counted on the actual network graph by
        max-flow/min-cut. For any tensor network this bounds the Schmidt rank
        across the cut, so S(A) <= ln(chi) * min_cut — the RT-type bound of B3."""
        n = self.num_sites
        sites_a = {(start + a) % n for a in range(length)}
        edges = self._network_edges()
        ids = {}
        for u, v in edges:
            for x in (u, v):
                if x not in ids:
                    ids[x] = len(ids)
        N = len(ids) + 2
        src, snk = N - 2, N - 1
        cap = np.zeros((N, N), dtype=np.int64)
        for u, v in edges:  # undirected chi=2 bonds, capacity 1 each
            cap[ids[u], ids[v]] += 1
            cap[ids[v], ids[u]] += 1
        for s in range(n):
            node = ids[("site", s)]
            if s in sites_a:
                cap[src, node] = _BIG_CAPACITY
            else:
                cap[node, snk] = _BIG_CAPACITY
        return int(self._max_flow(cap, src, snk))

    # ------------------------------------------------------------------
    # B3 / B5 — RT-type bound on the actual state
    # ------------------------------------------------------------------

    def rt_bound_check(self, intervals=((0, 2), (0, 4), (0, 8))) -> dict:
        """B3: for each interval, compare the EXACT entropy of the boundary
        state against ln(chi) * |minimal cut| (cut counted on the network
        graph). The bound flags and saturation ratios are computed.

        B5 honesty note: the log-shaped growth of the minimal cut with
        interval length is a BY-CONSTRUCTION property of the MERA graph
        (reported here as cut_by_length for inspection); it is NOT claimed
        as a computed result about the state. Only the inequality
        S <= ln(chi)*|cut| checked below is the computed claim."""
        ln_chi = float(np.log(self.bond_dim))
        rows = []
        for start, length in intervals:
            S = self.interval_entropy(start, length)
            cut = self.minimal_cut(start, length)
            bound = ln_chi * cut
            rows.append({
                "start": start,
                "length": length,
                "entropy": S,
                "min_cut_bonds": cut,
                "bound": bound,
                "bound_holds": bool(S <= bound + 1e-9),
                "saturation_ratio": float(S / bound) if bound > 0 else float("nan"),
            })
        return {
            "intervals": rows,
            "all_bounds_hold": bool(all(r["bound_holds"] for r in rows)),
            "computed_claim": (
                "exact S(interval) of the constructed boundary state obeys "
                "S <= ln(chi) * |minimal cut| for every checked interval"),
            "log_cut_shape": {
                "status": (
                    "by construction: the minimal cut grows logarithmically "
                    "with interval length because the MERA graph is "
                    "hierarchical; this is a property of the network graph, "
                    "not claimed as a computed result about the state"),
                "cut_by_length": {L: self.minimal_cut(0, L)
                                  for L in (1, 2, 3, 4, 6, 8)},
            },
        }

    # ------------------------------------------------------------------
    # B4 — mutual information between halves
    # ------------------------------------------------------------------

    def mutual_information_halves(self) -> dict:
        """I(L:R) = S(L) + S(R) - S(LR) for the two halves. S(L) and S(R)
        are computed exactly from the state; S(LR) = 0 because the boundary
        state is a pure vector by construction (its norm is computed and
        reported)."""
        half = self.num_sites // 2
        s_left = self.interval_entropy(0, half)
        s_right = self.interval_entropy(half, half)
        s_total = 0.0  # pure state (explicit normalized vector)
        return {
            "S_left": s_left,
            "S_right": s_right,
            "S_total_pure": s_total,
            "state_norm": float(np.linalg.norm(self.boundary_state())),
            "mutual_information": float(s_left + s_right - s_total),
        }

    # ------------------------------------------------------------------
    # aggregate demo (used by Experiment 19 after integration)
    # ------------------------------------------------------------------

    def full_demonstration(self) -> dict:
        """Aggregate of the computed Track-B results (B1-B5) plus the
        lambda-disconnection scan. Interpretive reading (Van Raamsdonk /
        Advaita: less entanglement = less connected space) is labeled as
        interpretation."""
        return {
            "tensor_algebra": self.tensor_algebra_check(),
            "perturbation_example": self.perturbation_response(layer=2),
            "rt_bound": self.rt_bound_check(),
            "halves": self.mutual_information_halves(),
            "disconnection": disconnection_scan(
                num_sites=self.num_sites, bond_dim=self.bond_dim,
                seed=self.seed),
            "interpretation": (
                "Computed: the entangling strength lambda controls the "
                "mutual information between the halves, vanishing in the "
                "product limit. Interpretation (not computed): reading the "
                "derived distance -ln(I/I0) as spatial disconnection "
                "(Van Raamsdonk 2010); in Advaita terms, entanglement as "
                "the non-separation Maya cannot fully sever."),
        }


def disconnection_scan(lambdas=(1.0, 0.6, 0.35, 0.2, 0.1, 0.0),
                       num_sites: int = 16, bond_dim: int = 2,
                       seed: int = 42) -> dict:
    """B4: build the SAME seeded network at decreasing entangling strength
    lambda and compute the mutual information I(left half : right half) from
    each explicit boundary state. lambda = 0 is exactly the product limit.

    The derived distance is -ln(I/I0) with I0 = I at the largest lambda
    (infinite when I = 0): smaller mutual information = larger derived
    distance. All monotonicity flags are computed from the values."""
    lambdas = tuple(float(l) for l in lambdas)
    mutual_infos = []
    for lam in lambdas:
        mera = MERATensorNetwork(num_sites=num_sites, bond_dim=bond_dim,
                                 entangling_strength=lam, seed=seed)
        mutual_infos.append(mera.mutual_information_halves()["mutual_information"])
    I0 = mutual_infos[0]
    distances = [float(-np.log(I / I0)) if I > 0 else float("inf")
                 for I in mutual_infos]
    monotone_dec = bool(all(mutual_infos[k + 1] < mutual_infos[k]
                            for k in range(len(mutual_infos) - 1)))
    distances_grow = bool(all(distances[k + 1] > distances[k]
                              for k in range(len(distances) - 1)))
    return {
        "lambdas": list(lambdas),
        "mutual_information": [float(I) for I in mutual_infos],
        "derived_distance": distances,
        "I0": float(I0),
        "monotone_decreasing": monotone_dec,
        "final_below_1e-8": bool(mutual_infos[-1] < 1e-8),
        "distances_grow": distances_grow,
    }
