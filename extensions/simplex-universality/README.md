# Simplex Universality: Conjecture 4.6 is False for n >= 6

## Summary

Conjecture 4.6 of the paper predicted that the regular simplex structure
observed at level 2 in S_5 would generalize to S_n for all n >= 5.

**This conjecture is false.** We prove (analytically and computationally)
that spectral contraction at level 3 is impossible for n >= 6 due to a
dimensional obstruction.

See [THEOREM.md](THEOREM.md) for the complete proof and verification details.

## Root Cause: Dimensional Obstruction

The level-1 Fourier transform D_1 = (P_sigma P_tau)^2 decomposes as:

- On W^perp (dim **n-3**): D_1 = Identity (n-3 singular values = 1)
- On W (dim 2): D_1 has singular values **1/8** and **0**

The 2x2 block on W is **independent of n** — it depends only on the
universal angle <v_sigma, v_tau> = -1/2 between adjacent transpositions.

Two preserved subspaces of dimension n-3 in R^{n-1} must intersect in
dimension >= 2(n-3) - (n-1) = **n-5**:

- n=5: n-5 = 0 → subspaces CAN be disjoint → contraction possible
- n>=6: n-5 >= 1 → subspaces ALWAYS share directions → op-norm stays at 1

## Verification (8 independent methods)

| # | Method | Scope | Status |
|---|--------|-------|--------|
| 1 | Analytic proof (W + W^perp decomposition) | All n >= 5 | **QED** |
| 2 | Exact rational arithmetic (sympy) | S_5, S_6, S_7: 390 pairs | **PASS** |
| 3 | Numerical (numpy, local Mac) | S_5, S_6, S_7, S_8 | **PASS** |
| 4 | Character-theoretic 2D reduction | All n | **PASS** |
| 5 | Exhaustive level-2 enumeration | 405 + 1620 + 4725 quads | **PASS** |
| 6 | Exhaustive level-3 enumeration | 73K + 1.2M + 10.3M configs | **PASS** |
| 7 | GCP cloud replication (yang-mills-gpu) | S_5, S_6, S_7 | **PASS** |
| 8 | Independent sympy implementation | S_5, S_6, S_7 all pairs | **PASS** |

## Key Results

| | S_5 | S_6 | S_7 |
|---|:-:|:-:|:-:|
| SVs of D_1 | [1, 1, 1/8, 0] | [1, 1, 1, 1/8, 0] | [1, 1, 1, 1, 1/8, 0] |
| Preserved dim | 2 | 3 | 4 |
| Min intersection | **0** | **1** | **2** |
| L2 op-norm = 1 | 270/405 (66.7%) | 1620/1620 (100%) | 4725/4725 (100%) |
| L3 contraction | lambda = 0.035 | lambda = 1.0 | lambda = 1.0 |
| Conjecture 4.6 | HOLDS | **FALSE** | **FALSE** |

## Files

- `THEOREM.md` — Complete analytic proof with all verification details
- `14_conjecture_S6_S7_verification.py` — Exhaustive computational verification
- `exact_proof_singular_values.py` — Exact sympy proof of singular value structure
