# Algebraic Proof of the Direction Mixing Lemma

## Summary

The Direction Mixing Lemma (Lemma 4.7 in the paper) was originally proved
by exhaustive enumeration of 73,810 level-3 configurations. This extension
provides a short algebraic proof that replaces brute force with group theory.

## The Proof (10 lines)

1. A level-2 quadruple preserves direction v_k **iff** all 4 transpositions fix element k
2. If both quadruples fix the same k, all transpositions lie in Stab(k) ~ S_4
3. S_4 is **solvable** with derived series: S_4 > A_4 > V_4 > {e}
4. Level-1 targets (commutators of transpositions) are 3-cycles in A_4
5. Level-2 targets (commutators of 3-cycles) lie in [A_4, A_4] = V_4
6. Level-3 commutator: [alpha_A, alpha_B] with both in V_4
7. V_4 (Klein four-group) is **abelian** => [V_4, V_4] = {e}
8. So the level-3 commutator is trivial => not a valid configuration
9. Contradiction => both quadruples CANNOT preserve the same direction. QED

## Why S_5 is Special

This proof reveals that S_5 works because of a structural coincidence:

- **S_5 is non-solvable** (A_5 is simple) => Barrington's theorem works
- **Stab(k) ~ S_4 is solvable** with derived length exactly **3**
- The commutator tree reaches depth **3** at the contraction level
- The preserved subspace dimension (2) equals half the ambient dimension (4)

These four facts conspire to make S_5 the unique symmetric group where
spectral contraction at level 3 is possible.

## Verification

Every step verified computationally (verify_algebraic_proof.py):

| Step | Claim | Result |
|------|-------|--------|
| 1 | preserves v_k => all trans fix k | 270/270 PASS |
| 1' | all trans fix k => preserves v_k | 270/270 PASS |
| 2a | [S_4, S_4] = A_4, |A_4| = 12 | VERIFIED |
| 2b | [A_4, A_4] = V_4, |V_4| = 4 | VERIFIED |
| 2c | [V_4, V_4] = {e} (abelian) | VERIFIED |
| 2d | L2 targets in V_4(k) for all k | VERIFIED (all 5 stabilizers) |
| 2e | L3 commutators = {e} for all k | VERIFIED |
| Direct | 0/29160 same-direction pairs | VERIFIED |

## Files

- `PROOF.md` — Complete formal proof
- `verify_algebraic_proof.py` — Computational verification of each proof step
