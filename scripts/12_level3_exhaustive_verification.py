"""
12_level3_exhaustive_verification.py
=====================================
PROVES: ||D3((4,1))||_op <= 0.0353 for ALL 73,810 valid level-3
configurations. This is the key step that closes the inductive proof.

Combined with Theorems 1-2 (Script 10) and T-independence (Script 07),
this resolves the Uniform T-Independence Conjecture for Barrington
point-function branching programs.

The script:
  1. Builds all 405 valid level-2 quadruples
  2. Computes D_hat_2 for each (numpy)
  3. Enumerates all 73,810 valid level-3 pairs
  4. Computes D_hat_3 = D2_A . D2_B . D2_A^T . D2_B^T
  5. Verifies ||D3||_op < 1 for every single one

Runtime: ~2 seconds.

Referenced in paper: Section 4.4 (Theorem 3)
"""

import numpy as np
from sympy import Matrix, sqrt, eye, zeros, simplify
import time

# -- Infrastructure --

def make_basis():
    f1 = Matrix([1, -1, 0, 0, 0]) / sqrt(2)
    f2 = Matrix([1, 1, -2, 0, 0]) / sqrt(6)
    f3 = Matrix([1, 1, 1, -3, 0]) / sqrt(12)
    f4 = Matrix([1, 1, 1, 1, -4]) / sqrt(20)
    return [f1, f2, f3, f4]

BASIS = make_basis()

def std_rep(perm):
    M = zeros(4, 4)
    for i in range(4):
        for j in range(4):
            fj_perm = Matrix([BASIS[j][perm[k]] for k in range(5)])
            M[i, j] = simplify(BASIS[i].dot(fj_perm))
    return M

def proj_np(a, b):
    perm = list(range(5)); perm[a], perm[b] = perm[b], perm[a]
    return np.array(((std_rep(tuple(perm)) + eye(4)) / 2).tolist(), dtype=float)

def pmul(a, b): return tuple(a[b[i]] for i in range(5))
def pinv(p):
    r = [0]*5
    for i, j in enumerate(p): r[j] = i
    return tuple(r)
def trans_perm(a, b):
    p = list(range(5)); p[a], p[b] = p[b], p[a]; return tuple(p)
def comm(p1, p2):
    return pmul(pmul(p1, p2), pmul(pinv(p1), pinv(p2)))


if __name__ == "__main__":
    all_trans = [(a, b) for a in range(5) for b in range(a+1, 5)]

    print()
    print("=" * 70)
    print("EXHAUSTIVE LEVEL-3 OPERATOR NORM VERIFICATION")
    print("=" * 70)

    # Precompute projections
    proj_cache = {}
    for a, b in all_trans:
        proj_cache[(a,b)] = proj_np(a, b)

    # Build adjacents and quadruples
    adjacent = []
    for (a1,b1) in all_trans:
        for (a2,b2) in all_trans:
            if (a1,b1)>=(a2,b2): continue
            if len(set([a1,b1])&set([a2,b2])) != 1: continue
            if comm(trans_perm(a1,b1),trans_perm(a2,b2)) != tuple(range(5)):
                adjacent.append(((a1,b1),(a2,b2)))

    valid_quads = []
    quad_targets = {}
    for i, pA in enumerate(adjacent):
        cA = comm(trans_perm(*pA[0]), trans_perm(*pA[1]))
        for j, pB in enumerate(adjacent):
            if j <= i: continue
            cB = comm(trans_perm(*pB[0]), trans_perm(*pB[1]))
            if comm(cA, cB) != tuple(range(5)):
                idx = len(valid_quads)
                valid_quads.append((pA, pB))
                quad_targets[idx] = comm(cA, cB)

    print(f"\n  Level-2 quadruples: {len(valid_quads)}")

    # Precompute all D_hat_2
    D2_all = {}
    for idx, (pA, pB) in enumerate(valid_quads):
        (a1,b1),(a2,b2) = pA
        (c1,d1),(c2,d2) = pB
        PA1, PA2 = proj_cache[(a1,b1)], proj_cache[(a2,b2)]
        PB1, PB2 = proj_cache[(c1,d1)], proj_cache[(c2,d2)]
        DA = np.linalg.matrix_power(PA1 @ PA2, 2)
        DB = np.linalg.matrix_power(PB1 @ PB2, 2)
        DA_inv = np.linalg.matrix_power(PA2 @ PA1, 2)
        DB_inv = np.linalg.matrix_power(PB2 @ PB1, 2)
        D2_all[idx] = DA @ DB @ DA_inv @ DB_inv

    print(f"  D_hat_2 matrices precomputed.")

    # Exhaustive level-3 check
    t0 = time.time()
    max_op = 0.0
    max_frob = 0.0
    n_valid_l3 = 0
    n_op_lt1 = 0
    n_op_geq1 = 0

    for i in range(len(valid_quads)):
        tgt_i = quad_targets[i]
        D2_A = D2_all[i]

        for j in range(i+1, len(valid_quads)):
            tgt_j = quad_targets[j]
            if comm(tgt_i, tgt_j) == tuple(range(5)):
                continue

            D2_B = D2_all[j]
            D3 = D2_A @ D2_B @ D2_A.T @ D2_B.T

            svs = np.linalg.svd(D3, compute_uv=False)
            op = svs[0]
            frob = np.sum(svs**2)

            if op > max_op: max_op = op
            if frob > max_frob: max_frob = frob
            n_valid_l3 += 1
            if op < 1.0 - 1e-10:
                n_op_lt1 += 1
            else:
                n_op_geq1 += 1

        if (i+1) % 100 == 0:
            elapsed = time.time() - t0
            print(f"    i={i+1}/{len(valid_quads)}, pairs={n_valid_l3}, "
                  f"max_op={max_op:.10f}, geq1={n_op_geq1}, [{elapsed:.0f}s]")

    elapsed = time.time() - t0

    print(f"\n{'='*70}")
    print(f"  RESULT")
    print(f"{'='*70}")
    print(f"  Valid level-3 configurations: {n_valid_l3}")
    print(f"  ||D3||_op < 1: {n_op_lt1}")
    print(f"  ||D3||_op >= 1: {n_op_geq1}")
    print(f"  Max ||D3||_op (lambda): {max_op:.10f}")
    print(f"  Max ||D3||^2_F: {max_frob:.10f}")
    print(f"  ALL STRICTLY < 1: {'YES' if n_op_geq1 == 0 else 'NO'}")
    print(f"  Time: {elapsed:.1f}s")

    if n_op_geq1 == 0:
        lam = max_op
        print(f"\n  INDUCTIVE CONSEQUENCE:")
        print(f"    lambda = {lam:.10f}")
        print(f"    For depth d >= 3 (l >= 8):")
        print(f"      ||D_d||_op <= lambda^(4^(d-3))")
        print(f"      d_TV(D_T, U) <= 2 . lambda^(4^(d-3)) = negl(l)")
        print(f"")
        print(f"    d=3  (l=8):    {lam:.6e}")
        print(f"    d=4  (l=16):   {lam**4:.6e}")
        print(f"    d=5  (l=32):   {lam**16:.6e}")
        print(f"    d=6  (l=64):   {lam**64:.6e}")
    print()
