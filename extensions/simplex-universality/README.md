# Simplex Universality: Conjecture 4.6 is False for n >= 6

## Discovery

Conjecture 4.6 of the paper predicted that the regular simplex structure
observed at level 2 in S_5 would generalize to S_n for all n >= 5.

**Computational verification for S_6 and S_7 refutes this conjecture.**

The root cause is a dimension-counting obstruction: the level-1 Fourier
transform D_1 = (P_sigma P_tau)^2 preserves a subspace of dimension n-3
in R^{n-1}. The minimum intersection of two such subspaces is:

    2(n-3) - (n-1) = n - 5

- **n = 5**: n-5 = 0, subspaces CAN be disjoint -> contraction possible at level 3
- **n >= 6**: n-5 >= 1, subspaces ALWAYS share directions -> op-norm = 1 persists

## Singular Value Structure of D_1

Universal pattern across all S_n:

| S_n | dim | SVs at 1 | SVs between | SVs at 0 | Min intersection |
|-----|-----|----------|-------------|----------|-----------------|
| S_5 | 4   | 2        | 1 (= 1/8)   | 1        | **0**           |
| S_6 | 5   | 3        | 1 (= 1/8)   | 1        | **1**           |
| S_7 | 6   | 4        | 1 (= 1/8)   | 1        | **2**           |
| S_8 | 7   | 5        | 1 (= 1/8)   | 1        | **3**           |

The intermediate singular value is always exactly 1/8 for all n.

## Key Results

### S_5 (confirmed, matches paper)
- 270/405 quadruples have op-norm = 1 (66.7%)
- 5 preserved directions forming regular simplex, |cos| = 1/4
- Direction mixing holds (0 same-direction pairs at level 3)
- Level-3 contraction: lambda = 0.0353

### S_6 (NEW)
- **1620/1620** quadruples have op-norm = 1 **(100%)**
- Preserved directions do NOT form a regular simplex
- Direction mixing FAILS (213,978 same-direction pairs)
- Level-3 contraction FAILS (lambda = 1.0)

### S_7 (NEW)
- **4725/4725** quadruples have op-norm = 1 **(100%)**
- Same failure pattern as S_6
- Level-3 contraction FAILS (lambda = 1.0)

## Open Questions

1. Does spectral contraction occur at some higher level (4, 5, ...) for S_6?
2. Is uniform mixing achievable for S_n with n > 5 via a different proof strategy?
3. What makes S_5 structurally unique among symmetric groups for this problem?

## Scripts

- `14_conjecture_S6_S7_verification.py` — Full verification for S_5, S_6, S_7
