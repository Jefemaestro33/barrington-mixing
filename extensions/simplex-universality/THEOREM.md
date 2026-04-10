# Theorem: Dimensional Obstruction to Spectral Contraction in S_n for n >= 6

## Statement

**Theorem.** Let $\rho_{(n-1,1)}$ be the standard representation of $S_n$ on the
hyperplane $V = \{v \in \mathbb{R}^n : \sum v_i = 0\}$ (dimension $n-1$). For any
pair of adjacent transpositions $\sigma = (a\;b)$ and $\tau = (b\;c)$ in $S_n$,
define the level-1 Fourier transform

$$D_1(\sigma, \tau) = (P_\sigma P_\tau)^2, \qquad P_\sigma = \frac{\rho(\sigma) + I}{2}.$$

Then $D_1$ has singular values

$$\underbrace{1, \ldots, 1}_{n-3}, \quad \frac{1}{8}, \quad 0.$$

**Corollary.** For $n \geq 6$, the level-2 commutator $D_2$ has operator norm $1$
for *every* valid quadruple of transpositions, and level-3 spectral contraction
fails. Consequently, the proof strategy of the main paper (spectral contraction
at level 3 via the simplex obstruction and direction mixing) is specific to $S_5$
and does not extend to $S_n$ for $n \geq 6$.

## Proof

### Step 1: Null vectors of the projections

The transposition $\sigma = (a\;b)$ acts on $V$ with eigenvalues $\{+1, -1\}$.
The $(-1)$-eigenspace is spanned by

$$v_\sigma = \frac{e_a - e_b}{\sqrt{2}} \in V.$$

Since $P_\sigma = \frac{1}{2}(\rho(\sigma) + I)$ projects onto the $(+1)$-eigenspace:

$$P_\sigma = I_V - v_\sigma v_\sigma^T, \qquad \text{rank}(P_\sigma) = n-2.$$

Similarly for $\tau = (b\;c)$:

$$v_\tau = \frac{e_b - e_c}{\sqrt{2}}, \qquad P_\tau = I_V - v_\tau v_\tau^T.$$

### Step 2: The inner product is universal

$$\langle v_\sigma, v_\tau \rangle = \frac{1}{2}\langle e_a - e_b, e_b - e_c \rangle = \frac{1}{2}(0 - 1 - 0 + 0) = -\frac{1}{2}.$$

This value is **independent of $n$** and depends only on the adjacency structure
(sharing exactly one element).

### Step 3: Block decomposition $V = W \oplus W^\perp$

Define $W = \text{span}(v_\sigma, v_\tau)$, which is 2-dimensional since
$|\langle v_\sigma, v_\tau \rangle| = 1/2 \neq 1$.

- **On $W^\perp$ (dimension $n-3$):** Both $P_\sigma$ and $P_\tau$ act as the
  identity (since $\langle w, v_\sigma \rangle = \langle w, v_\tau \rangle = 0$
  for $w \in W^\perp$). Therefore $D_1 = (P_\sigma P_\tau)^2 = I$ on $W^\perp$,
  contributing **$n-3$ singular values equal to $1$**.

- **On $W$ (dimension 2):** Both projections map $W$ into $W$. The restriction
  $D_1|_W$ is a $2 \times 2$ problem.

### Step 4: The 2x2 block (independent of n)

Orthonormalize: let $f_1 = v_\sigma$ and

$$f_2 = \frac{v_\tau + \frac{1}{2}v_\sigma}{\|v_\tau + \frac{1}{2}v_\sigma\|} = \frac{v_\tau + \frac{1}{2}v_\sigma}{\sqrt{3}/2}.$$

In the basis $(f_1, f_2)$:

$$P_\sigma|_W = \begin{pmatrix} 0 & 0 \\ 0 & 1 \end{pmatrix}, \qquad
P_\tau|_W = \begin{pmatrix} 3/4 & \sqrt{3}/4 \\ \sqrt{3}/4 & 1/4 \end{pmatrix}.$$

Computing the product and its square:

$$D_1|_W = (P_\sigma P_\tau)^2|_W = \begin{pmatrix} 0 & 0 \\ \sqrt{3}/16 & 1/16 \end{pmatrix}.$$

The matrix $D_1|_W^T D_1|_W$:

$$D_1|_W^T D_1|_W = \frac{1}{256}\begin{pmatrix} 3 & \sqrt{3} \\ \sqrt{3} & 1 \end{pmatrix}.$$

This has trace $= 4/256 = 1/64$ and determinant $= (3 - 3)/256^2 = 0$.

**Eigenvalues: $1/64$ and $0$. Singular values: $1/8$ and $0$.** $\square$

### Step 5: Dimensional obstruction for n >= 6

$D_1(\sigma, \tau)$ preserves $W^\perp(\sigma, \tau)$ isometrically (all singular
values $= 1$ there). This subspace has dimension $n-3$.

For a level-2 commutator using two level-1 blocks $A$ and $B$:

$$\dim(W_A^\perp \cap W_B^\perp) \geq (n-3) + (n-3) - (n-1) = n - 5.$$

| $n$ | $\dim W^\perp$ | Min intersection | Contraction possible? |
|-----|:-:|:-:|:-:|
| 5 | 2 | **0** | Yes (and proven in the paper) |
| 6 | 3 | **1** | No |
| 7 | 4 | **2** | No |
| $n$ | $n-3$ | $n-5$ | No for $n \geq 6$ |

For $n \geq 6$, any unit vector in $W_A^\perp \cap W_B^\perp$ is preserved
isometrically by both $D_{1,A}$ and $D_{1,B}$. The level-2 commutator
$D_2 = D_{1,A} D_{1,B} D_{1,A}^T D_{1,B}^T$ therefore has operator norm $1$,
and this propagates to level 3. $\blacksquare$

## Verification

This theorem has been verified by 8 independent methods:

| # | Method | Scope | Status |
|---|--------|-------|--------|
| 1 | Analytic proof (this document) | All $n \geq 5$ | **QED** |
| 2 | Exact rational arithmetic (sympy) | $S_5$: 60 pairs, $S_6$: 120, $S_7$: 210 | **PASS** |
| 3 | Numerical computation (numpy, local Mac) | $S_5, S_6, S_7, S_8$ | **PASS** |
| 4 | Character-theoretic 2D reduction (sympy) | All $n$ | **PASS** |
| 5 | Exhaustive level-2 enumeration (local) | $S_5$: 405, $S_6$: 1620, $S_7$: 4725 quads | **PASS** |
| 6 | Exhaustive level-3 enumeration (local) | $S_5$: 73810, $S_6$: 1.2M, $S_7$: 10.3M configs | **PASS** |
| 7 | GCP cloud replication (`yang-mills-gpu`) | $S_5, S_6, S_7$ (725s total) | **PASS** |
| 8 | Independent implementation (sympy agent) | $S_5, S_6, S_7$ all adjacent pairs | **PASS** |

### Exact eigenvalues (verified for all adjacent pairs)

| $S_n$ | Pairs checked | Eigenvalues of $D_1^T D_1$ | SVs of $D_1$ |
|-------|:---:|:---:|:---:|
| $S_5$ | 60 | $\{1: 2,\; 1/64: 1,\; 0: 1\}$ | $[1, 1, 1/8, 0]$ |
| $S_6$ | 120 | $\{1: 3,\; 1/64: 1,\; 0: 1\}$ | $[1, 1, 1, 1/8, 0]$ |
| $S_7$ | 210 | $\{1: 4,\; 1/64: 1,\; 0: 1\}$ | $[1, 1, 1, 1, 1/8, 0]$ |

### Level-2 and level-3 exhaustive results

| | $S_5$ | $S_6$ | $S_7$ |
|---|:---:|:---:|:---:|
| Level-2 quads with op-norm = 1 | 270/405 (66.7%) | 1620/1620 (100%) | 4725/4725 (100%) |
| Level-3 same-direction pairs | 0 | 215,451 | 2,338,842 |
| Level-3 max op-norm ($\lambda$) | 0.0353 | 1.0 | 1.0 |
| Level-3 contraction | YES | NO | NO |

## Implications for the Paper

1. **Main Theorem (S_5) is unaffected.** The spectral contraction proof for S_5
   remains correct. S_5 is the unique case where the simplex structure and
   direction mixing hold.

2. **Conjecture 4.6 must be withdrawn.** The simplex universality conjecture is
   false. The preserved directions for $n \geq 6$ do not form a regular simplex
   and are not aligned with the standard basis projections.

3. **New open question.** Does uniform mixing for Barrington branching programs
   hold for $S_n$ with $n > 5$? If so, a fundamentally different proof strategy
   is needed — the level-3 spectral contraction approach cannot work due to the
   dimensional obstruction.

4. **S_5 is structurally unique.** The non-solvable group $S_5$ is the smallest
   symmetric group where the standard representation allows spectral contraction,
   precisely because it is the unique case where the preserved subspace dimension
   ($n-3 = 2$) equals half the ambient dimension ($n-1 = 4$), permitting
   disjoint placement of preserved subspaces.

## Scripts

- `14_conjecture_S6_S7_verification.py` — Exhaustive verification for $S_5, S_6, S_7$
- `exact_proof_singular_values.py` — Exact sympy proof of SV structure
