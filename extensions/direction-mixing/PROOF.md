# Algebraic Proof of the Direction Mixing Lemma

## Statement

**Lemma (Direction Mixing).** For every valid level-3 configuration
$(\mathrm{quad}_A, \mathrm{quad}_B)$ of the Barrington branching program for
point functions over $S_5$, if both sub-blocks have
$\|\widehat{D}_2\|_{\mathrm{op}} = 1$ in the standard representation $(4,1)$,
they preserve **different** directions.

*Previously proved by exhaustive enumeration of 73,810 configurations (Script 12).
This document gives a short algebraic proof.*

---

## Proof

The proof has two steps: (1) characterize which quadruples preserve which
direction, and (2) show that two quadruples preserving the same direction
cannot form a valid level-3 configuration.

### Step 1: Preserved direction determines a fixed element

**Claim.** A level-2 quadruple $(\sigma_1, \tau_1, \sigma_2, \tau_2)$ with
$\|\widehat{D}_2\|_{\mathrm{op}} = 1$ preserves direction $v_k$ if and only if
all four transpositions fix element $k$.

*Proof.*

The five candidate directions are $v_k = (e_k - \bar{e})/\|e_k - \bar{e}\|$
for $k = 0, \ldots, 4$, where $\bar{e} = \frac{1}{5}(1,1,1,1,1)^T$.

The null vector of $P_{(a,b)}$ is $v_{(a,b)} = (e_a - e_b)/\sqrt{2}$.

**Key inner product:**

$$\langle v_k, \, v_{(a,b)} \rangle = \frac{\delta_{k,a} - \delta_{k,b}}{\sqrt{2}\,\|e_k - \bar{e}\|}$$

This is **zero** if and only if $k \notin \{a, b\}$, i.e., the transposition
$(a\;b)$ fixes element $k$.

**Forward direction** ($\Leftarrow$): If all four transpositions fix $k$, then
$\langle v_k, v_\sigma \rangle = 0$ for each $\sigma \in \{\sigma_1, \tau_1,
\sigma_2, \tau_2\}$. Hence $v_k \in W_A^\perp \cap W_B^\perp$, and $D_1 v_k =
v_k$ for both level-1 blocks. The level-2 commutator $\widehat{D}_2 = D_{1,A}
\cdot D_{1,B} \cdot D_{1,A}^T \cdot D_{1,B}^T$ satisfies $\widehat{D}_2 v_k =
v_k$, so $v_k$ is preserved.

**Backward direction** ($\Rightarrow$): Suppose $\|\widehat{D}_2 v_k\| = 1$.
Since $\widehat{D}_2 = D_{1,A} \cdot D_{1,B} \cdot D_{1,A}^T \cdot D_{1,B}^T$
and each factor has operator norm $\leq 1$, the chain of inequalities

$$1 = \|D_{1,A} \cdot D_{1,B} \cdot D_{1,A}^T \cdot D_{1,B}^T \, v_k\| \leq \|D_{1,B} \cdot D_{1,A}^T \cdot D_{1,B}^T \, v_k\| \leq \cdots \leq \|v_k\| = 1$$

forces equality at each step. In particular, $\|D_{1,B}^T v_k\| = 1$, which
(since $D_{1,B}$ has singular values $[1, 1, 1/8, 0]$) requires $v_k$ to lie in
the rank-2 preserved subspace $W_B^\perp$ of $D_{1,B}$. Similarly, $v_k \in
W_A^\perp$.

Since $v_k \in W_A^\perp$ means $\langle v_k, v_{\sigma_1} \rangle =
\langle v_k, v_{\tau_1} \rangle = 0$, and this holds iff $\sigma_1$ and $\tau_1$
fix $k$. Likewise for $\sigma_2, \tau_2$. $\square$

### Step 2: The solvability obstruction

**Claim.** If both $\mathrm{quad}_A$ and $\mathrm{quad}_B$ have all transpositions
fixing the same element $k$, then their level-3 commutator is trivial, so the
configuration is not valid.

*Proof.*

All eight transpositions lie in $\mathrm{Stab}(k) \cong S_4$. The **derived
series** of $S_4$ is:

$$S_4 \;\supsetneq\; A_4 \;\supsetneq\; V_4 \;\supsetneq\; \{e\}$$

where $V_4 = \{e, (01)(23), (02)(13), (03)(12)\}$ is the Klein four-group
(relabeling elements of $\{0,1,2,3,4\} \setminus \{k\}$).

Trace the Barrington commutator tree within $\mathrm{Stab}(k)$:

| Level | Construction | Elements lie in |
|-------|-------------|----------------|
| 0 | Leaf transpositions | $S_4$ |
| 1 | $[\sigma, \tau]$ for adjacent transpositions | $[S_4, S_4] = A_4$ (3-cycles) |
| 2 | $[[\sigma_1,\tau_1], [\sigma_2,\tau_2]]$ | $[A_4, A_4] = V_4$ |
| **3** | $[\alpha_A, \alpha_B]$ with $\alpha_A, \alpha_B \in V_4$ | $[V_4, V_4] = \{e\}$ |

At level 3, the commutator $[\alpha_A, \alpha_B]$ must lie in $[V_4, V_4]$.
Since $V_4 \cong \mathbb{Z}_2 \times \mathbb{Z}_2$ is **abelian**,
$[V_4, V_4] = \{e\}$, so $[\alpha_A, \alpha_B] = e$.

But a valid level-3 configuration requires $[\alpha_A, \alpha_B] \neq e$.
**Contradiction.** $\square$

### Combining Steps 1 and 2

Suppose both $\mathrm{quad}_A$ and $\mathrm{quad}_B$ preserve the same direction
$v_k$. By Step 1, all transpositions in both quadruples fix element $k$.
By Step 2, the level-3 commutator is trivial, contradicting the validity
requirement. Therefore the two quadruples must preserve **different**
directions. $\blacksquare$

---

## Why S_5 is Special

This proof reveals the deep reason the main paper's spectral contraction
argument works specifically for $S_5$:

1. **$S_5$ is non-solvable** ($A_5$ is simple), so iterated commutators of
   non-identity elements never reach the identity — this is what makes
   Barrington's theorem work over $S_5$.

2. **$\mathrm{Stab}(k) \cong S_4$ is solvable** with derived length exactly 3.
   The Barrington commutator tree reaches depth 3 at level 3 of the
   construction, which is precisely where the derived series of $S_4$
   terminates.

3. This creates a **structural tension**: non-identity commutators at level 3
   require elements from *outside* $\mathrm{Stab}(k)$ (i.e., transpositions
   that move $k$), which forces a change in the preserved direction.

The coincidence of three numbers — derived length of $S_4$ (= 3), depth of
the commutator tree at the contraction level (= 3), and the number of SVs at 1
equaling half the dimension ($2 = 4/2$) — is what makes $S_5$ the unique
symmetric group where this proof strategy succeeds.

---

## Replacing Exhaustive Enumeration

This algebraic proof replaces the exhaustive verification of 73,810
configurations in the original paper (Lemma 4.7 / Script 12). The
computational verification remains as independent confirmation:

| Aspect | Exhaustive (original) | Algebraic (this proof) |
|--------|-----------------------|------------------------|
| Method | Check all 73,810 configs | Group-theoretic argument |
| Scope | $S_5$ only | Explains why $S_5$ is unique |
| Generality | None (brute force) | Connects to derived series |
| Dependencies | numpy computation | $S_4$ solvability (textbook) |
| Length | ~1 second computation | ~10 lines of proof |
