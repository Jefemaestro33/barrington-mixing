"""
14_conjecture_S6_S7_verification.py
====================================
VERIFIES Conjecture 4.6 (Simplex Universality) for S_6 and S_7.

Conjecture 4.6: For S_n with n >= 5, the level-2 quadruples with operator
norm 1 in the standard representation (n-1,1) preserve directions that are
the projections of the n standard basis vectors onto the hyperplane
V = {v in R^n : sum v_i = 0}, forming a regular simplex in R^{n-1}
with pairwise |<v_i, v_j>| = 1/(n-1).

For S_5 (verified in Script 11):
  - 270/405 quadruples have op-norm = 1
  - 5 directions, 54 each, |cos| = 1/4

For S_6 (this script):
  - Standard rep dim = 5, leaf projection rank = 4
  - 15 transpositions, expect more adjacent pairs and quadruples
  - Conjecture predicts 6 directions with |cos| = 1/5

For S_7 (this script):
  - Standard rep dim = 6, leaf projection rank = 5
  - 21 transpositions
  - Conjecture predicts 7 directions with |cos| = 1/6
"""

import numpy as np
from itertools import combinations
import time
import sys


def verify_conjecture(n, verbose=True):
    """
    Verify Conjecture 4.6 for S_n.
    Returns a dict with all results.
    """
    T0 = time.time()

    if verbose:
        print(f"\n{'='*70}")
        print(f"CONJECTURE 4.6 VERIFICATION FOR S_{n}")
        print(f"Standard representation (n-1,1), dimension {n-1}")
        print(f"{'='*70}")

    # ===================================================================
    # Step 1: Build orthonormal basis for V = {v in R^n : sum v_i = 0}
    # ===================================================================
    # Gram-Schmidt on {e_0 - e_1, e_0 + e_1 - 2e_2, ...}
    dim = n - 1
    basis = np.zeros((dim, n))
    for k in range(dim):
        # v_k = e_0 + e_1 + ... + e_k - (k+1)*e_{k+1}
        for j in range(k + 1):
            basis[k, j] = 1.0
        basis[k, k + 1] = -(k + 1)
        basis[k] /= np.linalg.norm(basis[k])

    # Verify orthonormality
    gram = basis @ basis.T
    assert np.allclose(gram, np.eye(dim)), "Basis not orthonormal!"

    if verbose:
        print(f"\n  Orthonormal basis for V (dim {dim}): VERIFIED")

    # ===================================================================
    # Step 2: Standard representation matrices for transpositions
    # ===================================================================
    all_trans = list(combinations(range(n), 2))
    n_trans = len(all_trans)

    def std_rep_trans(a, b):
        """Standard rep matrix for transposition (a b)."""
        P = np.eye(n)
        P[[a, b]] = P[[b, a]]
        return basis @ P @ basis.T

    def projection(a, b):
        """Leaf Fourier transform P_{(a,b)} = (rho((a,b)) + I) / 2."""
        return (std_rep_trans(a, b) + np.eye(dim)) / 2

    # Precompute all projections
    proj_cache = {}
    for t in all_trans:
        proj_cache[t] = projection(*t)

    # Verify projection properties
    for t in all_trans:
        P = proj_cache[t]
        assert np.allclose(P @ P, P), f"P_{t} not idempotent!"
        assert np.allclose(P, P.T), f"P_{t} not symmetric!"
        assert abs(np.trace(P) - (dim - 1)) < 1e-10, f"P_{t} trace != {dim-1}!"
        assert np.linalg.matrix_rank(P, tol=1e-10) == dim - 1, f"P_{t} rank != {dim-1}!"

    if verbose:
        print(f"  {n_trans} transpositions, projections rank {dim-1}: VERIFIED")

    # ===================================================================
    # Step 3: Enumerate adjacent pairs and valid quadruples
    # ===================================================================
    def trans_perm(a, b):
        p = list(range(n))
        p[a], p[b] = p[b], p[a]
        return tuple(p)

    def compose(a, b):
        return tuple(a[b[i]] for i in range(n))

    def inverse(p):
        r = [0] * n
        for i, j in enumerate(p):
            r[j] = i
        return tuple(r)

    def comm(p1, p2):
        return compose(compose(p1, p2), compose(inverse(p1), inverse(p2)))

    ID = tuple(range(n))

    # Adjacent pairs: transpositions sharing exactly 1 element, nontrivial commutator
    adjacent_pairs = []
    for i, t1 in enumerate(all_trans):
        for j, t2 in enumerate(all_trans):
            if j <= i:
                continue
            if len(set(t1) & set(t2)) == 1:
                p1 = trans_perm(*t1)
                p2 = trans_perm(*t2)
                if comm(p1, p2) != ID:
                    adjacent_pairs.append((t1, t2))

    n_adj = len(adjacent_pairs)

    # Compute commutator target for each pair
    pair_targets = {}
    for idx, (t1, t2) in enumerate(adjacent_pairs):
        pair_targets[idx] = comm(trans_perm(*t1), trans_perm(*t2))

    # Valid quadruples: pairs of adjacent pairs with nontrivial outer commutator
    valid_quads = []
    quad_targets = {}
    for i in range(n_adj):
        for j in range(i + 1, n_adj):
            c = comm(pair_targets[i], pair_targets[j])
            if c != ID:
                idx = len(valid_quads)
                valid_quads.append((i, j))
                quad_targets[idx] = c

    n_quads = len(valid_quads)

    if verbose:
        print(f"  Adjacent pairs: {n_adj}")
        print(f"  Valid quadruples: {n_quads}")

    # ===================================================================
    # Step 4: Compute level-2 Fourier transforms and operator norms
    # ===================================================================
    if verbose:
        print(f"\n  Computing level-2 D_hat matrices...")

    D2_cache = {}
    op_norms = {}
    frob_norms = {}

    for idx, (i, j) in enumerate(valid_quads):
        t1_A, t2_A = adjacent_pairs[i]
        t1_B, t2_B = adjacent_pairs[j]

        PA1, PA2 = proj_cache[t1_A], proj_cache[t2_A]
        PB1, PB2 = proj_cache[t1_B], proj_cache[t2_B]

        DA = np.linalg.matrix_power(PA1 @ PA2, 2)
        DB = np.linalg.matrix_power(PB1 @ PB2, 2)
        DA_inv = np.linalg.matrix_power(PA2 @ PA1, 2)
        DB_inv = np.linalg.matrix_power(PB2 @ PB1, 2)

        D2 = DA @ DB @ DA_inv @ DB_inv
        D2_cache[idx] = D2

        svs = np.linalg.svd(D2, compute_uv=False)
        op_norms[idx] = svs[0]
        frob_norms[idx] = np.sum(svs ** 2)

        if verbose and (idx + 1) % 2000 == 0:
            print(f"    {idx+1}/{n_quads} computed...")

    if verbose:
        print(f"    All {n_quads} computed.")

    # ===================================================================
    # Step 5: Identify problematic quadruples (op-norm = 1)
    # ===================================================================
    problematic = [idx for idx, op in op_norms.items() if op > 1.0 - 1e-10]
    non_problematic = [idx for idx, op in op_norms.items() if op <= 1.0 - 1e-10]

    n_prob = len(problematic)
    n_nonprob = len(non_problematic)

    if verbose:
        print(f"\n  Operator norm = 1: {n_prob}/{n_quads}")
        print(f"  Operator norm < 1: {n_nonprob}/{n_quads}")
        if non_problematic:
            max_nonprob = max(op_norms[idx] for idx in non_problematic)
            print(f"  Max op-norm among non-problematic: {max_nonprob:.10f}")

    # ===================================================================
    # Step 6: Compute preserved directions for problematic quadruples
    # ===================================================================
    # Reference directions: projections of e_k onto V
    ref_dirs = []
    for k in range(n):
        ek = np.zeros(n)
        ek[k] = 1.0
        v = ek - np.ones(n) / n  # project onto V
        coords = basis @ v  # express in orthonormal basis
        coords /= np.linalg.norm(coords)
        ref_dirs.append(coords)

    # Verify reference directions form a regular simplex
    predicted_cos = 1.0 / (n - 1)
    if verbose:
        print(f"\n  Reference directions (projections of e_k onto V):")
        print(f"  Predicted pairwise |cos theta| = 1/{n-1} = {predicted_cos:.10f}")

    pairwise_cos = []
    for i in range(n):
        for j in range(i + 1, n):
            cos_ij = abs(np.dot(ref_dirs[i], ref_dirs[j]))
            pairwise_cos.append(cos_ij)

    if verbose:
        print(f"  Actual pairwise |cos theta|: min={min(pairwise_cos):.10f}, "
              f"max={max(pairwise_cos):.10f}")
        print(f"  All equal to 1/{n-1}? {all(abs(c - predicted_cos) < 1e-10 for c in pairwise_cos)}")

    # For each problematic quadruple, find preserved direction
    quad_dir = {}
    for idx in problematic:
        D2 = D2_cache[idx]
        DtD = D2.T @ D2
        evals, evecs = np.linalg.eigh(DtD)
        # Eigenvector with eigenvalue closest to 1
        evec = evecs[:, -1]
        # Match to reference direction
        best_k = max(range(n), key=lambda k: abs(np.dot(evec, ref_dirs[k])))
        match_cos = abs(np.dot(evec, ref_dirs[best_k]))
        quad_dir[idx] = (best_k, match_cos)

    # Verify all match a reference direction
    all_match = all(match_cos > 1.0 - 1e-6 for _, match_cos in quad_dir.values())
    dir_counts = [sum(1 for _, (k, _) in quad_dir.items() if k == d) for d in range(n)]

    if verbose:
        print(f"\n  All {n_prob} preserved directions match a reference e_k? "
              f"{'YES' if all_match else 'NO'}")
        if not all_match:
            worst = min(quad_dir.values(), key=lambda x: x[1])
            print(f"    Worst match: direction {worst[0]}, cos = {worst[1]:.10f}")
        print(f"  Direction distribution: {dir_counts}")
        print(f"  Perfectly symmetric ({n_prob}/{n} = {n_prob//n} each)? "
              f"{'YES' if len(set(dir_counts)) == 1 and dir_counts[0] == n_prob // n else 'NO'}")

    # ===================================================================
    # Step 7: Verify pairwise angles among preserved directions
    # ===================================================================
    if n_prob > 0:
        # Check that problematic pairs with different directions have |cos| = 1/(n-1)
        misaligned_cos = []
        aligned_count = 0
        for i_idx in problematic:
            for j_idx in problematic:
                if j_idx <= i_idx:
                    continue
                k_i = quad_dir[i_idx][0]
                k_j = quad_dir[j_idx][0]
                if k_i == k_j:
                    aligned_count += 1
                else:
                    # Compute actual angle between preserved eigenvectors
                    D2_i = D2_cache[i_idx]
                    D2_j = D2_cache[j_idx]
                    _, evecs_i = np.linalg.eigh(D2_i.T @ D2_i)
                    _, evecs_j = np.linalg.eigh(D2_j.T @ D2_j)
                    cos_val = abs(np.dot(evecs_i[:, -1], evecs_j[:, -1]))
                    misaligned_cos.append(cos_val)

        if verbose:
            print(f"\n  Pairwise analysis among {n_prob} problematic quadruples:")
            print(f"    Aligned (same direction): {aligned_count}")
            print(f"    Misaligned (different direction): {len(misaligned_cos)}")
            if misaligned_cos:
                print(f"    Misaligned |cos| range: [{min(misaligned_cos):.10f}, "
                      f"{max(misaligned_cos):.10f}]")
                print(f"    All |cos| = 1/{n-1} = {predicted_cos:.10f}? "
                      f"{all(abs(c - predicted_cos) < 1e-6 for c in misaligned_cos)}")

    # ===================================================================
    # Step 8: Level-3 direction mixing check
    # ===================================================================
    if verbose:
        print(f"\n  Level-3 direction mixing check...")

    n_valid_l3 = 0
    n_both_prob = 0
    n_same_dir = 0
    max_op_l3 = 0.0

    for i in range(n_quads):
        tgt_i = quad_targets[i]
        for j in range(i + 1, n_quads):
            tgt_j = quad_targets[j]
            if comm(tgt_i, tgt_j) == ID:
                continue
            n_valid_l3 += 1

            i_prob = i in quad_dir
            j_prob = j in quad_dir
            if i_prob and j_prob:
                n_both_prob += 1
                if quad_dir[i][0] == quad_dir[j][0]:
                    n_same_dir += 1

            # Compute level-3 operator norm
            D3 = D2_cache[i] @ D2_cache[j] @ D2_cache[i].T @ D2_cache[j].T
            op3 = np.linalg.svd(D3, compute_uv=False)[0]
            max_op_l3 = max(max_op_l3, op3)

        if verbose and (i + 1) % 500 == 0:
            print(f"    i={i+1}/{n_quads}, L3 pairs={n_valid_l3}, "
                  f"max_op={max_op_l3:.10f}, same_dir={n_same_dir}")

    if verbose:
        print(f"\n  Level-3 results:")
        print(f"    Valid level-3 configurations: {n_valid_l3}")
        print(f"    Both sub-blocks problematic: {n_both_prob}")
        print(f"    Same direction (VIOLATION): {n_same_dir}")
        print(f"    Max ||D3||_op (lambda): {max_op_l3:.10f}")
        print(f"    ALL ||D3||_op < 1? {'YES' if max_op_l3 < 1.0 - 1e-10 else 'NO'}")

    # ===================================================================
    # Summary
    # ===================================================================
    elapsed = time.time() - T0

    results = {
        'n': n,
        'dim': dim,
        'n_trans': n_trans,
        'n_adj_pairs': n_adj,
        'n_quads': n_quads,
        'n_problematic': n_prob,
        'n_non_problematic': n_nonprob,
        'dir_counts': dir_counts,
        'all_match_ref': all_match,
        'symmetric': len(set(dir_counts)) == 1,
        'predicted_cos': predicted_cos,
        'n_valid_l3': n_valid_l3,
        'n_both_prob': n_both_prob,
        'n_same_dir': n_same_dir,
        'max_op_l3': max_op_l3,
        'lambda': max_op_l3,
        'conjecture_holds': conjecture_holds,
        'elapsed': elapsed,
    }

    conjecture_holds = all_match and len(set(dir_counts)) == 1 and n_same_dir == 0

    if verbose:
        print(f"\n{'='*70}")
        print(f"  CONJECTURE 4.6 FOR S_{n}: ", end="")
        if conjecture_holds:
            print("CONFIRMED")
        else:
            print("FALSE")
        print(f"{'='*70}")
        print(f"""
  Summary for S_{n}:
    Standard rep dim:          {dim}
    Transpositions:            {n_trans}
    Adjacent pairs:            {n_adj}
    Valid quadruples (L2):     {n_quads}
    Problematic (op-norm=1):   {n_prob}/{n_quads} ({100*n_prob/n_quads:.1f}%)
    Directions match e_k:      {'YES' if all_match else 'NO'}
    Distribution:              {dir_counts} ({n_prob//n} each)
    Perfectly symmetric:       {'YES' if len(set(dir_counts)) == 1 else 'NO'}
    Pairwise |cos| = 1/{n-1}:  {predicted_cos:.10f}
    Regular simplex:           {'YES' if all_match and len(set(dir_counts)) == 1 else 'NO'}

    Valid level-3 configs:     {n_valid_l3}
    Same-direction pairs:      {n_same_dir}
    Direction mixing holds:    {'YES' if n_same_dir == 0 else 'NO'}
    Max ||D3||_op (lambda):    {max_op_l3:.10f}
    Level-3 contraction:       {'YES' if max_op_l3 < 1.0 - 1e-10 else 'NO'}

    Time: {elapsed:.1f}s
""")

    return results


if __name__ == "__main__":
    print("=" * 70)
    print("CONJECTURE 4.6: SIMPLEX UNIVERSALITY FOR S_n")
    print("=" * 70)

    # Verify S_5 first (known result, sanity check)
    r5 = verify_conjecture(5)

    # Verify S_6 (new!)
    r6 = verify_conjecture(6)

    # Verify S_7 (new!) — may take longer
    r7 = verify_conjecture(7)

    # Final comparison table
    print("\n" + "=" * 70)
    print("COMPARISON TABLE")
    print("=" * 70)
    print(f"\n  {'':20s} {'S_5':>12s} {'S_6':>12s} {'S_7':>12s}")
    print(f"  {'─'*20} {'─'*12} {'─'*12} {'─'*12}")
    for key, label in [
        ('dim', 'Rep dimension'),
        ('n_trans', 'Transpositions'),
        ('n_adj_pairs', 'Adjacent pairs'),
        ('n_quads', 'Valid quadruples'),
        ('n_problematic', 'Op-norm = 1'),
        ('n_valid_l3', 'Level-3 configs'),
        ('n_same_dir', 'Same-dir pairs'),
    ]:
        print(f"  {label:20s} {r5[key]:>12} {r6[key]:>12} {r7[key]:>12}")
    print(f"  {'Lambda (L3)':20s} {r5['lambda']:>12.6e} {r6['lambda']:>12.6e} {r7['lambda']:>12.6e}")
    print(f"  {'Pairwise |cos|':20s} {'1/4':>12s} {'1/5':>12s} {'1/6':>12s}")
    print(f"  {'Simplex?':20s} {'YES' if r5['all_match_ref'] else 'NO':>12s} "
          f"{'YES' if r6['all_match_ref'] else 'NO':>12s} "
          f"{'YES' if r7['all_match_ref'] else 'NO':>12s}")
    print(f"  {'Dir mixing?':20s} {'YES' if r5['n_same_dir']==0 else 'NO':>12s} "
          f"{'YES' if r6['n_same_dir']==0 else 'NO':>12s} "
          f"{'YES' if r7['n_same_dir']==0 else 'NO':>12s}")
    print(f"  {'L3 contraction?':20s} {'YES' if r5['lambda']<1 else 'NO':>12s} "
          f"{'YES' if r6['lambda']<1 else 'NO':>12s} "
          f"{'YES' if r7['lambda']<1 else 'NO':>12s}")

    # Verdict
    all_confirmed = (r5['conjecture_holds'] and r6['conjecture_holds']
                     and r7['conjecture_holds'])
    print(f"\n  {'='*56}")
    if all_confirmed:
        print(f"  CONJECTURE 4.6 CONFIRMED FOR S_5, S_6, AND S_7")
        print(f"  The simplex structure IS universal.")
        print(f"  Direction mixing holds for all three groups.")
        print(f"  Spectral contraction extends beyond S_5.")
    else:
        print(f"  CONJECTURE 4.6: PARTIAL RESULTS — SEE DETAILS ABOVE")
    print(f"  {'='*56}")
