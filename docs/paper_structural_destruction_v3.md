# Structural Destruction: A Framework for Point Function Obfuscation over Composite Moduli

**Working Draft — March 2026**

---

## Abstract

We introduce a theoretical framework for privacy-preserving computation
based on the principle of *structural destruction*: security is achieved
by embedding a secret in a computational object that destroys all
structural relations except those required by a set of authorized
functions. The framework, inspired by Benacerraf's structuralism in the
philosophy of mathematics, provides a unified treatment of functional
encryption and program obfuscation through the *function kernel* ker(F)
and a corresponding *security entropy* metric H_sec.

As a concrete instantiation, we construct a candidate obfuscator for
point functions CC_T(x) = [x = T] over Z_n, where n = pq is an RSA
modulus. The construction uses Barrington's theorem to represent point
functions as width-5 branching programs, randomized via Kilian's
technique over Z_n — without lattices, multilinear maps, or graded
encodings. We present a base construction with static Kilian
randomization, analyze it via a systematic cryptanalysis (including a
similarity attack that we prove universally blind by the ambivalence
of S_5), and introduce a hardened variant with state-dependent dynamic
encoding for defense in depth against algebraic attacks.

We identify the *global consistency barrier* — the inability to
cryptographically bind multiple reads of the same variable across the
branching program — and prove that it is not a security threat for
point functions. We prove *exact T-independence*: the distribution of
outputs from inconsistent evaluation paths is identical for all targets
T (by an explicit flip bijection that requires no property of S_5).
We further prove *doubly exponential convergence to uniform*: Fourier
analysis over S_5 combined with spectral contraction analysis yields
the bound d_TV(D_T, Uniform(S_5)) ≤ 0.546^{4^{log₂(ℓ)-2}}, which
is negligible for ℓ ≥ 8. This bound is universal: it holds for any
Barrington construction where sibling transposition pairs have
element overlap 1, verified across all 135 overlap-1 combinations
and all 6 non-trivial representations of S_5 with exact arithmetic. The security of the construction rests not
on collisions being improbable (they are not — rate ≈ 1/|S_5| is
constant), but on collisions being uninformative: the adversary's
view is identically distributed regardless of the embedded target.
Security is formalized under a new assumption (MBPI — Matrix Branching
Program Indistinguishability over Z_n), which with T-independence
proved reduces to factoring plus algebraic security of Kilian
randomization over composite moduli. We further demonstrate that
both T-independence and spectral contraction extend to conjunctions
with wildcards, broadening the applicability to pattern matching
and attribute-based access control.

---

## 1. Introduction

### 1.1 Motivation

Since Gentry's breakthrough (2009), all practical fully homomorphic
encryption (FHE) and most functional encryption (FE) schemes rely on
the same mathematical foundation: the hardness of lattice problems,
specifically the Learning With Errors (LWE) and Ring-LWE assumptions.
Security in these schemes comes from noise — random perturbations
injected into ciphertexts that make the underlying algebraic structure
computationally hidden.

This paradigm has been enormously successful. Schemes such as BGV,
BFV, CKKS, TFHE, and GSW support increasingly practical applications,
and recent hardware accelerators (Intel Heracles, Niobium ASIC) have
narrowed the performance gap with plaintext computation. Yet the
mathematical foundation has remained essentially unchanged for over
fifteen years: every scheme relies on lattice problems, and every
scheme pays the cost of noise management (bootstrapping, modulus
switching, or both).

A natural question arises: **is it possible to achieve privacy-
preserving computation from a fundamentally different mathematical
base?** Specifically, can security come not from noise injection but
from the *structural properties* of how secrets are embedded in
computational objects?

### 1.2 A Structuralist Perspective

Our starting point is an observation from the philosophy of
mathematics. Benacerraf (1965) argued that mathematical objects are
not defined by what they "are" but by the structural relations they
satisfy. Two different representations (e.g., von Neumann and Zermelo
ordinals) can serve equally well as "the natural numbers" because
they preserve the same arithmetic structure.

We apply this insight to cryptography: if computation depends only on
certain structural relations among data, then one can change the
*representation* of the data — destroying all relations except those
needed for computation — without affecting the computation's
correctness. The destroyed relations become the source of security.

This leads to a design principle we call **structural destruction**:
instead of hiding data behind noise, hide it by embedding it in a
representation that retains only the computational structure authorized
by a set of functions F, and nothing more.

### 1.3 Contributions

This paper makes three contributions:

**1. A theoretical framework (Section 2).** We formalize the
structural destruction principle through:
- The *function kernel* ker(F), which characterizes the equivalence
  classes of inputs indistinguishable under F.
- *Security entropy* H_sec, a metric quantifying residual uncertainty
  about the secret after observing all authorized function outputs.
- *Admissible transformations*, which change representation while
  preserving exactly the structure F requires.
- A fundamental limit theorem: any scheme computing a point-
  separating set of functions has H_sec = 0.
- Formal security definitions (IND-StructObf and IND-StructFE)
  applicable to both obfuscation and functional encryption.
- A classification of function classes by their suitability for
  obfuscation vs. FE, identifying point functions as the unique
  optimal class for obfuscation under adaptive queries.

**2. A candidate construction (Section 3).** We construct a candidate
obfuscator for point functions over Z_n using:
- Barrington's theorem to represent CC_T as a width-5 branching
  program of length ℓ² (for ℓ-bit inputs).
- Kilian's randomization technique over the composite modulus Z_n,
  with vectorial bookends that compress 5×5 matrix products to
  single scalars.
- A hardened variant with state-dependent dynamic encoding that
  prevents algebraic manipulation of the randomized matrices.

**3. A systematic cryptanalysis (Sections 3.4–3.5).** We analyze the
construction against concrete attacks:
- A *similarity attack via matrix quotients* that reveals the
  conjugacy class of internal permutations. We prove this attack
  does not factorize n and is locally blind at leaf nodes.
- Identification of the *global consistency barrier* — the inability
  to bind multiple reads of the same variable — as the precise
  theoretical gap, with a heuristic resilience argument based on the
  commutator topology of Barrington's construction and explicit
  parametric bounds.
- Analysis of GCD, CRT, bookend probing, and evaluation-based attacks.

### 1.4 What This Paper Does Not Claim

We emphasize what this paper does **not** claim:

- We do NOT claim provable security under standard assumptions.
  Security is formalized under a new assumption (MBPI) that is
  presented as a candidate for community validation.

- We do NOT claim to solve the global consistency problem for
  branching programs over Z_n. This problem — which is the
  historical reason for the existence of multilinear maps in
  indistinguishability obfuscation — remains open. We identify it
  explicitly as the primary barrier and provide heuristic arguments
  for why it may not be exploitable for point functions.

- We do NOT claim practical superiority over LWE-based constructions.
  Our construction is conceptually simpler (matrix multiplication
  over Z_n with no lattice operations) but produces large programs
  (hundreds of megabytes for 32-bit inputs).

What we DO claim is: (a) a new theoretical framework that provides
a different lens on privacy-preserving computation, (b) a concrete
construction that instantiates this framework without lattices or
multilinear maps, and (c) a thorough and honest analysis of what
works, what doesn't, and exactly where the open problems lie.

### 1.5 Relationship to Existing Work

**Compute-and-Compare obfuscation.** Wichs and Zirdelis (FOCS 2017)
and Goyal, Koppula, and Waters (2017) construct obfuscation for
compute-and-compare programs under LWE. Our construction targets the
same function class but from a different mathematical base
(composite moduli vs. lattices).

**Branching program obfuscation.** The use of Barrington's theorem
and Kilian's randomization in obfuscation has a long history,
beginning with the candidate constructions of Garg et al. (2013)
for iO. These constructions require multilinear maps or graded
encodings to enforce global variable consistency. Our construction
operates directly over Z_n without such machinery, at the cost of
the global consistency gap identified in Section 3.5.7.

**Affine Determinant Programs.** Bartusek et al. (2020) proposed
ADPs as a candidate for obfuscation without multilinear maps.
These were subsequently attacked. Our construction differs in
targeting a restricted function class (point functions) rather than
general circuits, and in using width-5 branching programs with
state-dependent encoding rather than affine determinant programs.

**Evasive functions.** Barak et al. (TCC 2014) showed that evasive
functions (which almost always output 0) admit stronger forms of
obfuscation than general functions. Point functions are the
canonical example of evasive functions, and our construction
exploits this evasiveness directly.

### 1.6 Paper Organization

Section 2 presents the theoretical framework: function kernels,
security entropy, admissible transformations, and security
definitions. Section 3 presents the candidate construction: the
base scheme, its cryptanalysis, the hardened variant with dynamic
encoding, parameters, security analysis, and open problems.
Section 4 analyzes published attacks on obfuscation schemes and
establishes that none transfer to our construction, identifies
the genuine threat (algebraic invariants of Kilian randomization,
which we prove blind by ambivalence of S_5), and compares with
existing work. Section 5 presents the empirical analysis and proofs:
Fourier decomposition of the collision distribution on S_5,
the proof of exact T-independence via flip bijection, the proof of
doubly exponential convergence via spectral contraction, and the
extension to conjunctions with wildcards. Section 6 concludes.

---

## 2. Structural Destruction — A Framework for Privacy-Preserving Computation

### 2.1 Overview and Scope

We introduce a theoretical framework for analyzing and constructing
schemes where a secret value is embedded in a computational object
(a ciphertext or a program) such that only authorized functions of
the secret can be extracted.

The framework is built on a single principle: **security comes from
destroying structural relations that the authorized functions do not
need, while preserving those they do.** This principle applies equally
to two dual paradigms:

- **Functional Encryption (FE):** The secret is a datum x, embedded
  in a ciphertext. Functional keys allow computing P(x) without
  revealing x.

- **Program Obfuscation:** The secret is a parameter T, embedded in
  a program. Anyone can evaluate the program on inputs of their
  choice, but cannot extract T.

These are dual in the following sense: in FE, the function P is
public and the input x is secret; in obfuscation, the input x is
public and the function's internal parameter T is secret. In both
cases, the goal is identical: reveal only P(x) and nothing more.

Our metric (Section 2.3) and admissibility conditions (Section 2.4)
apply to both paradigms. In Section 2.7, we specialize to program
obfuscation for Compute-and-Compare functions, which is the setting
for our concrete construction in Section 3.

### 2.2 The Kernel of a Function Set

Let X be a finite space with |X| = N. A function P: X → Y induces
a natural equivalence relation capturing what P can and cannot
distinguish about its input.

**Definition 1 (Function Kernel).** The kernel of P: X → Y is:

    ker(P) = {(x₁, x₂) ∈ X × X : P(x₁) = P(x₂)}

This partitions X into equivalence classes. Elements within a class
are indistinguishable from P's perspective.

*Examples:*
- P(x) = x mod 10 over Z₁₀₀: classes are {0,10,20,...}, {1,11,21,...},
  etc. P destroys all information except the last digit.
- CC_T(x) = [x = T]: two classes, {T} and X\{T}. The function
  destroys all information except whether x equals T.
- P(x) = x: the trivial kernel. P destroys nothing.

**Definition 2 (Joint Kernel).** For F = {P₁, ..., Pₖ}, the joint
kernel is:

    ker(F) = ∩ᵢ ker(Pᵢ)

We write x₁ ~_F x₂ when P_i(x₁) = P_i(x₂) for all P_i ∈ F.

The joint kernel captures the total information revealed by F. Adding
functions to F can only refine (shrink or maintain) the equivalence
classes — never coarsen them.

### 2.3 Security Entropy

The equivalence classes of ker(F) determine the inherent information
leakage of any correct scheme implementing F. We quantify this using
the average conditional min-entropy.

**Definition 3 (Security Entropy).** Let D be a distribution over X.
The security entropy of F with respect to D is:

    H_sec(F, D) = -log₂( E_{y ← F(D)} [ max_{x ∈ X} Pr_D[x | F(x) = y] ] )

where F(x) = (P₁(x), ..., Pₖ(x)) is the vector of all authorized
function outputs.

For each output vector y, the preimage class is
C_y = {x' ∈ X : F(x') = y}. The security entropy measures how
unpredictable x remains after observing all function outputs.

*Interpretation:*
- H_sec = 0: function outputs uniquely determine x (zero security).
- H_sec = log₂(N): outputs reveal nothing (perfect security).
- H_sec intermediate: partial security proportional to class sizes.

**Remark (Entropy in Obfuscation).** The definition above is stated
with x as the secret (the FE perspective). In the obfuscation
paradigm, the roles are reversed: the parameter T is the secret drawn
from distribution D, and the adversary observes the function's
behavior P_T(x) over adaptively chosen queries x. In this context,
H_sec measures the conditional min-entropy of T given oracle access
to P_T(·). For evasive point functions, this oracle returns 0 on all
but one input, so adaptive queries reveal at most one bit per query
(hit or miss), preserving the high entropy of T as long as the query
space is cryptographically large.

**Theorem 1 (Fundamental Limit).** If F separates all points of X
(i.e., for every x₁ ≠ x₂ there exists P ∈ F with P(x₁) ≠ P(x₂)),
then H_sec(F, D) = 0 for any distribution D with full support.

*Proof.* If F separates all points, every preimage class C_y is a
singleton {x}. Then max_{x'} Pr[x' | F(x') = y] = 1 for all y,
giving H_sec = -log₂(1) = 0. □

**Corollary 1.** Any scheme computing a Turing-complete set of
functions has H_sec = 0. Non-trivial security requires restricting F.

### 2.4 Admissible Transformations

We define the structural requirements for a scheme compatible with F.
Crucially, we separate the **functional requirement** (correctness)
from the **security requirement** (indistinguishability), which is
deferred to the security definitions in Section 2.6.

**Definition 4 (Admissible Transformation).** Let S be the secret
space (the datum x in FE, or the parameter T in obfuscation), R a
randomness space, and C the output space (ciphertext or obfuscated
program). A transformation E: S × R → C is admissible for F if it
satisfies:

**(Completeness)** For every P ∈ F, there exists an efficient
evaluation procedure Eval_P such that for all s ∈ S and all r ∈ R:

    Eval_P(E(s, r), ·) correctly computes P(s, ·)

In the FE setting: Eval_P(c) = P(x) where c = E(x, r).
In the obfuscation setting: Eval_P(π, x) = P_T(x) where π = E(T, r).

The randomization r does not affect the functional output.

**Remark (What admissibility does NOT require).** Admissibility is
a correctness condition only. It says the scheme works — it computes
the right answers. Whether the scheme is *secure* (hides s beyond
what F reveals) is a separate question addressed in Section 2.6.
This separation avoids the circularity of assuming security in the
definition of the primitive.

**Remark (Structural interpretation).** An admissible transformation
changes the representation of s (from a value in S to an object in C)
while preserving exactly the computational structure that F requires.
This embodies Benacerraf's insight: what matters is the structure
(the relations needed for computation), not the representation.

### 2.5 The Fusion Operator

In the FE setting, the key functional component is the fusion
operator Φ_P that extracts P(x) from a ciphertext E(x, r).

**Definition 5 (Fusion Operator).** A function Φ_P: C → Y_P is a
fusion operator for P with respect to E if:

    Φ_P(E(x, r)) = P(x) for all x ∈ X, r ∈ R

Conceptually, Φ_P realizes P ∘ E⁻¹ as a single computational object.

**Remark.** In the obfuscation setting, there is no separate fusion
operator — the obfuscated program itself plays the role of Φ,
accepting public inputs and producing outputs.

**Remark (On irreducibility).** A natural desideratum is that Φ_P
(or the obfuscated program) cannot be decomposed to separately
recover its internal components (E⁻¹, or the secret parameters).
We do NOT formalize this as an axiom; following Barak et al. (2001),
"inability to extract" is formally problematic as a standalone
definition. Instead, irreducibility is captured as a consequence of
the security game: if the scheme is secure (Definition 7), then no
efficient adversary can extract information beyond what F reveals.

### 2.6 Security Definitions

We provide security definitions for both paradigms. Both follow the
standard indistinguishability approach.

#### 2.6.1 Security for Program Obfuscation (IND-StructObf)

This is the primary setting for our construction in Section 3.

The key subtlety in defining security for obfuscation of point
functions is that the adversary must not know the targets T₀, T₁
exactly — otherwise they could trivially evaluate the obfuscated
program on T₀ and distinguish. We therefore adopt a **distributional**
security definition, following Wichs-Zirdelis (2017).

**Definition 6 (Distributional IND-StructObf Game).** Let Π be a
structural obfuscation scheme. Let D = {D_λ} be a family of
distributions that sample (T₀, T₁, aux), where T₀, T₁ ∈ X and
aux is auxiliary information available to the adversary.

The IND-StructObf game between a challenger C and a PPT adversary A
proceeds as follows:

1. **Sampling.** C samples (T₀, T₁, aux) ← D_λ.

2. **Challenge.** C samples b ←$ {0,1} and constructs the obfuscated
   program: π_b ← Obfuscate(T_b).

3. **Interaction.** A receives (π_b, aux) and may evaluate π_b on
   any inputs x of their choice (polynomially many times).

4. **Guess.** A outputs b'.

**Definition 7 (IND-StructObf Security).** Π is IND-StructObf secure
for a distribution class D if for all D ∈ D satisfying the
**unpredictability condition**, and for all PPT adversaries A:

    Adv_A(λ) = |Pr[b' = b] - 1/2| ≤ negl(λ)

The unpredictability condition requires that both T₀ and T₁ have
sufficient pseudo-entropy given aux:

    Pr[A(aux) = T₀] ≤ negl(λ)  and  Pr[A(aux) = T₁] ≤ negl(λ)

for all PPT A. In other words, even with the auxiliary information,
no efficient adversary can guess either target.

**Remark (Why distributional?).** If the adversary knew T₀ or T₁
exactly, they could evaluate π_b(T₀): output 1 reveals b = 0, and
output 0 reveals b = 1. The unpredictability condition prevents this
trivial attack by ensuring the adversary cannot query the
distinguishing input. Since CC_T is evasive (outputs 0 on all but
one input), the adversary's queries return 0 with overwhelming
probability regardless of b, making the programs functionally
indistinguishable on all feasible queries.

**Remark (Practical interpretation).** The unpredictability condition
means T must come from a high-entropy space (e.g., cryptographic
keys, hashes, long identifiers). For small domains (ages, small
salaries), point function obfuscation does not provide meaningful
security — this is inherent, not a limitation of our scheme.

**Remark (What security implies).** If Π is IND-StructObf secure:
- A cannot determine which target T_b is embedded in the program.
- A cannot extract T_b from the obfuscated program.
- A cannot reconstruct the secret randomness used during obfuscation.
These are consequences of indistinguishability, not separate axioms.

#### 2.6.2 Security for Functional Encryption (IND-StructFE)

For completeness and to demonstrate the generality of the framework,
we also define the FE variant.

**Definition 8 (IND-StructFE Game).** Let Π be a structural FE scheme
for a function class F. The IND-StructFE game proceeds:

1. **Setup.** C runs KeyGen(1^λ) to obtain master secret key msk.

2. **Key queries.** A submits functions P₁, ..., Pₖ ∈ F and receives
   fusion operators Φ_{P₁}, ..., Φ_{Pₖ}.

3. **Challenge.** A submits x₀, x₁ ∈ X subject to the restriction
   P_i(x₀) = P_i(x₁) for all queried P_i. C samples b ←$ {0,1}
   and returns c_b = Enc(msk, x_b).

4. **Guess.** A outputs b'.

**Definition 9 (IND-StructFE Security).** Π is IND-StructFE secure
if for all PPT adversaries A:

    Adv_A(λ) = |Pr[b' = b] - 1/2| ≤ negl(λ)

**Remark (Scope).** Definition 8 is a 1-ciphertext (1-CT) game.
Extending to multi-ciphertext security (where A receives encryptions
of multiple challenge pairs) requires additional analysis. We note
that 1-CT security does not generically imply multi-CT security for
SK-FE schemes. For the obfuscation setting (Definition 6), this
issue does not arise since there are no ciphertexts.

**Remark (Duality).** Definitions 6 and 8 are dual formulations of
the same principle: the computational object (obfuscated program or
ciphertext + fusion operators) should not reveal any information
about the secret (T or x) beyond what the authorized functions
output. The security entropy H_sec(F, D) provides an upper bound on
the achievable security in both settings.

### 2.7 Optimal Function Classes

**Proposition 1 (Point Functions).** Let F = {CC_T} for a secret
T, where CC_T(x) = 1 if x = T and 0 otherwise. Under uniform D
with |X| = N:

    H_sec(F, D) = log₂(N) - 1

*Proof.* CC_T partitions X into {T} and X\{T}. For uniform x:
- Pr[CC_T(x) = 1] = 1/N. Given output 1: max_x Pr[x|y=1] = 1.
- Pr[CC_T(x) = 0] = (N-1)/N. Given output 0: max_x Pr[x|y=0] = 1/(N-1).

    E[max_x Pr[x|y]] = (1/N)(1) + ((N-1)/N)(1/(N-1)) = 2/N

    H_sec = -log₂(2/N) = log₂(N) - 1

For N = 2^128: H_sec = 127 bits. □

**Proposition 2 (Threshold Functions).** Let F = {P_T} with
P_T(x) = [x > T] over X = {0,...,N-1}, uniform D, and T at the
median. Then:

    H_sec(F, D) = log₂(N) - 1

*Proof.* P_T partitions X into two classes of size N/2 each (when
T = N/2 - 1). Both outputs have probability 1/2, and within each
class, the conditional max probability is 1/(N/2) = 2/N. Therefore:

    E[max_x Pr[x|y]] = (1/2)(2/N) + (1/2)(2/N) = 2/N

    H_sec = -log₂(2/N) = log₂(N) - 1 □

**Remark (Learnability of Thresholds).** While Proposition 2 shows
that threshold functions have high H_sec for a single evaluation,
this does NOT mean threshold obfuscation is secure. In the
obfuscation setting, the adversary can adaptively query the program
on inputs of their choice. For threshold functions, an adversary
can extract T exactly in log₂(N) queries via binary search: evaluate
on N/2, then N/4 or 3N/4 depending on the result, and so on. This
is fundamentally different from point functions, where each query
has probability 1/N of hitting T — there is no "direction" toward
T, and no binary search is possible. Therefore, threshold functions
are suitable for FE (where the adversary has a ciphertext, not
oracle access) but NOT for obfuscation (where the adversary has
adaptive query access). This highlights why point functions are the
optimal *unconstrained* class for obfuscation.

**Proposition 3 (Negative Result: Arithmetic Functions).** If F
contains the identity function or, more generally, separates all
points, then H_sec(F, D) = 0 by Theorem 1.

**Summary:**

| Function Class F | H_sec (uniform) | FE? | Obfuscation? |
|---|---|---|---|
| Point function CC_T | log₂(N) - 1 | YES | YES (optimal) |
| Threshold [x > T] | log₂(N) - 1 | YES | NO (binary search) |
| k-bit output | ≥ log₂(N) - k | YES if k ≪ log N | Depends on learnability |
| Linear P(x) = ax + b | 0 | NO | NO |
| All polynomials | 0 | NO | NO |
| Identity | 0 | NO | NO |

**Corollary 2.** For unrestricted obfuscation (where the adversary
has adaptive oracle access), point functions are the unique optimal
class: they maximize H_sec AND resist extraction via adaptive queries.
Other function classes with high H_sec (such as thresholds) may still
be learnable through adaptive queries, making them suitable for FE
but not for obfuscation without query restrictions.

### 2.8 Discussion

**The structural destruction principle.** The framework presented here
formalizes a simple but powerful idea: the security of a scheme is
determined by how much structural information the authorized functions
destroy. Security is not achieved by adding noise (as in LWE-based
schemes) but by ensuring that the computational object (program or
ciphertext) embodies only the residual structure that the functions
need — and nothing more.

This perspective, inspired by Benacerraf's structuralism in the
philosophy of mathematics, suggests a different design methodology:
instead of starting with a hard problem and building encryption around
it, start with the function class F, analyze ker(F) and H_sec, and
then design a transformation that destroys exactly the right relations.

**Limitations.** The framework provides necessary conditions and
information-theoretic bounds, but does not by itself guarantee that a
secure construction exists. The gap between "H_sec is large" (which
says security is information-theoretically possible) and "we can build
a secure scheme" (which requires computational assumptions) must be
bridged by a concrete construction and proof. We address this in
Section 3.

**Relationship to existing work.** The security entropy H_sec is
related to, but distinct from, existing information-theoretic measures
in functional encryption (e.g., the residual leakage of Boneh-Sahai-
Waters). Our contribution is the explicit connection to equivalence
classes of ker(F), the structural destruction principle, and the
applicability to both FE and obfuscation via a single framework.

---

## 3. Candidate Construction — Point Function Obfuscation over Z_n

### 3.1 Overview

We construct a candidate obfuscator for point functions
CC_T(x) = [x = T] over Z_n where n = pq is an RSA modulus.

The presentation follows a deliberate narrative arc:
- Section 3.2: Background on branching programs (Barrington's theorem)
- Section 3.3: The base construction using static Kilian randomization
- Section 3.4: Cryptanalysis of the base construction, including a
  similarity attack and analysis of why it partially fails
- Section 3.5: A hardened construction using dynamic (state-dependent)
  encoding that eliminates the similarity attack entirely
- Section 3.6: Parameters and efficiency
- Section 3.7: Security analysis and honest assessment

### 3.2 Branching Programs from Barrington's Theorem

**Theorem (Barrington, 1989).** Any function computable by a Boolean
circuit of depth d and fan-in 2 can be computed by a permutation
branching program of width 5 and length 4^d.

A permutation branching program of width w and length L over an input
x = (x_1, ..., x_ℓ) ∈ {0,1}^ℓ is a sequence of L instructions:

    (i_1, M_{1,0}, M_{1,1}), ..., (i_L, M_{L,0}, M_{L,1})

where i_j ∈ {1,...,ℓ} specifies which input bit to read, and
M_{j,0}, M_{j,1} ∈ S_5 are 5×5 permutation matrices. The program
evaluates to:

    BP(x) = ∏_{j=1}^{L} M_{j, x_{i_j}}

The program accepts if BP(x) = π_accept (a fixed target permutation)
and rejects otherwise.

#### 3.2.1 Point Function as Branching Program

The point function CC_T for T = (t_1,...,t_ℓ) is:

    CC_T(x) = AND(EQ_1, ..., EQ_ℓ)

where EQ_i = [x_i = t_i]. This is a balanced AND tree of depth
d = log₂(ℓ), yielding a branching program of length:

    L = 4^{log₂(ℓ)} = ℓ²

#### 3.2.2 Building Blocks

We use two non-commuting elements in S_5. Let σ = (1 2) and
τ = (2 3) be transpositions. Note that σ = σ^{-1} and τ = τ^{-1}
(transpositions are involutions).

**Encoding a single bit equality EQ_i = [x_i = t_i]:**

- If t_i = 0: M_{0} = σ, M_{1} = I. Product is σ when x_i = 0
  (match), I when x_i = 1 (mismatch).
- If t_i = 1: M_{0} = I, M_{1} = σ. Product is σ when x_i = 1
  (match), I when x_i = 0 (mismatch).

**Encoding AND via commutator:**

Given encodings of bits a (with target σ) and b (with target τ),
the AND is encoded as the commutator:

    Encode(a,σ) ∘ Encode(b,τ) ∘ Encode(a,σ^{-1}) ∘ Encode(b,τ^{-1})

- When a=1 AND b=1: product = σ τ σ^{-1} τ^{-1} = [σ,τ] ≠ I
- When a=0: σ terms become I, product = τ τ^{-1} = I
- When b=0: τ terms become I, product = σ σ^{-1} = I

The AND tree is built recursively. The final target permutation
π_accept is the iterated commutator at the root of the tree.

#### 3.2.3 Concrete Example (ℓ = 4)

Let T = (1,0,1,1). The AND tree has depth 2:

    Level 1: A = AND([x₁=1], [x₂=0]),  B = AND([x₃=1], [x₄=1])
    Level 2: CC_T = AND(A, B)

Level 1 uses targets σ, τ. Level 2 uses targets [σ,τ] and [σ',τ']
(with σ' = (1 3), τ' = (3 4) for independence).

Total: L = 4² = 16 instructions, each a pair of 5×5 permutation
matrices.

---

### 3.3 The Base Construction: Static Kilian over Z_n

#### 3.3.1 Setup

Let n = pq with p, q large primes of equal bitlength. The factorization
(p, q) is secret. The modulus n is public.

The branching program BP for CC_T has L = ℓ² instructions with
permutation matrices M_{j,0}, M_{j,1} ∈ {0,1}^{5×5}. These are
lifted to matrices over Z_n (entries remain 0 or 1 mod n).

#### 3.3.2 Static Kilian Randomization

Choose L+1 random invertible 5×5 matrices S_0, S_1, ..., S_L over
Z_n. Invertibility requires gcd(det(S_j), n) = 1, which holds with
overwhelming probability for random matrices over Z_n when p, q
are large.

Compute the randomized matrices:

    M̂_{j,b} = S_{j-1} · M_{j,b} · S_j^{-1}  (mod n)

for j = 1,...,L and b ∈ {0,1}.

#### 3.3.3 Vectorial Bookends

Rather than having the evaluator see the full 5×5 product matrix
(which would expose algebraic structure), we compress the output to
a single scalar using random bookend vectors.

The data owner chooses:
- Random row vector u^T ∈ (Z_n^*)^5
- Random column vector v ∈ (Z_n^*)^5
- Computes target scalar s = u^T · π_accept · v (mod n)

The bookend vectors are absorbed into the Kilian randomization:
- Left bookend:  û^T = u^T · S_0^{-1}  (mod n)
- Right bookend: v̂ = S_L · v  (mod n)

#### 3.3.4 The Obfuscated Program (Base Version)

The obfuscated program π_base consists of:
- Public modulus n
- Left bookend û^T ∈ Z_n^5
- Right bookend v̂ ∈ Z_n^5
- Target scalar s ∈ Z_n
- Instruction set: {(i_j, M̂_{j,0}, M̂_{j,1})}_{j=1}^{L}

#### 3.3.5 Evaluation (Base Version)

**Input:** x = (x_1, ..., x_ℓ) ∈ {0,1}^ℓ

**Algorithm:**
    R ← I_{5×5}
    For j = 1 to L:
        R ← R · M̂_{j, x_{i_j}}  (mod n)
    α ← û^T · R · v̂  (mod n)
    If α = s: return 1 (accept)
    Else: return 0 (reject)

**Correctness.** By telescoping cancellation of the S_j:

    R = S_0 · BP(x) · S_L^{-1}

The scalar output is:

    α = û^T · R · v̂
      = (u^T S_0^{-1}) · (S_0 · BP(x) · S_L^{-1}) · (S_L · v)
      = u^T · BP(x) · v

When x = T: BP(T) = π_accept, so α = u^T · π_accept · v = s. ✓

When x ≠ T: BP(x) = P ≠ π_accept, so α = u^T · P · v. The
probability that u^T · P · v = s for random u, v is at most
1/min(p,q) = negl(λ), since u^T · (P - π_accept) · v = 0 mod n
requires a nontrivial relation among random elements. ✓

---

### 3.4 Cryptanalysis of the Base Construction

We now analyze the security of the base construction by examining
concrete attacks. This analysis reveals both strengths and a
theoretical concern that motivates the hardened construction in
Section 3.5.

#### 3.4.1 The Similarity Attack via Matrix Quotients

An adversary observing the public matrices M̂_{j,0} and M̂_{j,1}
can compute their "quotient":

    Q_j = M̂_{j,0} · M̂_{j,1}^{-1}
        = (S_{j-1} · M_{j,0} · S_j^{-1}) · (S_j · M_{j,1}^{-1} · S_{j-1}^{-1})
        = S_{j-1} · (M_{j,0} · M_{j,1}^{-1}) · S_{j-1}^{-1}  (mod n)

The inner S_j matrices cancel. The result Q_j is a similarity
transform of the "raw quotient" M_{j,0} · M_{j,1}^{-1}.

This is potentially dangerous: similarity transforms preserve
eigenvalues, determinant, trace, and characteristic polynomial. If
these invariants differ between t_j = 0 and t_j = 1 (the two possible
values of the secret bit), the adversary could extract T bit by bit.

#### 3.4.2 Why the Attack Does Not Factorize n

One might expect that computing eigenvalues of Q_j over Z_n (a
composite modulus) could reveal divisors of n, since eigenvalue
computations over Z_n can produce zero divisors when the
characteristic polynomial factors differently mod p vs mod q.

However, this does NOT occur here. The matrices M_{j,0} and M_{j,1}
are permutation matrices with entries in {0, 1}. Their entries are
identical mod p and mod q (since 0 and 1 are the same in any ring).
Therefore:

- The raw quotient M_{j,0} · M_{j,1}^{-1} is the same matrix mod p
  and mod q.
- Its characteristic polynomial is identical mod p and mod q.
- Computing eigenvalues of Q_j over Z_n produces no zero divisors.

**Proposition.** The similarity attack on the base construction does
not yield a factorization of n.

*Proof.* Let D = M_{j,0} · M_{j,1}^{-1}. Since M_{j,0}, M_{j,1}
have entries in {0,1}, D has integer entries (independent of n).
The characteristic polynomial χ_D(λ) = det(λI - D) has integer
coefficients. Its roots mod p and mod q are identical. Therefore
gcd(χ_D(λ), n) ∈ {1, n} for all λ, yielding no nontrivial
factor of n. □

#### 3.4.3 Universal Blindness via Ambivalence of S_5

Even though the similarity attack does not factorize n, it reveals
the conjugacy class of M_{j,0} · M_{j,1}^{-1} in S_5. Could this
distinguish whether t_j = 0 or t_j = 1?

**For leaf-level instructions (single bit equalities):**

Recall from Section 3.2.2:
- If t_j = 0: M_{j,0} = σ, M_{j,1} = I. Quotient: σ · I^{-1} = σ.
- If t_j = 1: M_{j,0} = I, M_{j,1} = σ. Quotient: I · σ^{-1} = σ^{-1}.

For transpositions: σ = σ^{-1} (transpositions are involutions).
Therefore the quotient is **identical** regardless of t_j:

    Q_j = S_{j-1} · σ · S_{j-1}^{-1}  in both cases.

The adversary learns nothing about t_j from the quotient at the
leaf level. The attack is **locally blind**.

**For ALL levels (general proof via ambivalence):**

The leaf-level argument used the special property σ = σ^{-1} for
transpositions. We now give a general argument that applies to
every instruction in the branching program, regardless of depth,
based on a classical property of symmetric groups.

**Definition (Ambivalent group).** A finite group G is *ambivalent*
if every element is conjugate to its inverse: for every g ∈ G,
there exists h ∈ G with h g h^{-1} = g^{-1}.

**Theorem (S_n is ambivalent).** The symmetric group S_n is
ambivalent for all n ≥ 1.

*Proof.* Decompose g into disjoint cycles g = c_1 · c_2 · ... · c_k.
Each cycle c_i = (a_1 a_2 ... a_m) has inverse (a_m ... a_2 a_1).
Define r_i by r_i(a_j) = a_{m+1-j} (reversal within the cycle),
fixing all points outside the cycle. Then r_i · c_i · r_i^{-1} =
c_i^{-1}. Since the cycles are disjoint, P = r_1 · r_2 · ... · r_k
satisfies P · g · P^{-1} = g^{-1}. Moreover, P is a permutation
matrix with entries in {0,1} and det(P) = ±1, so P is invertible
over Z_n for any n > 2. □

At any instruction j, the target permutation π_j ∈ S_5 is
determined by the position in the Barrington tree (not by T). The
raw quotient is D_j = π_j if t_{i_j} = 0, or D_j = π_j^{-1} if
t_{i_j} = 1. The adversary observes:

    Q_j = S_{j-1} · D_j · S_{j-1}^{-1}  (mod n)

**Proposition (Universal blindness).** The distribution of Q_j is
identical whether D_j = π_j or D_j = π_j^{-1}. This holds for
ANY permutation π_j ∈ S_5, at ANY level of the Barrington tree,
with ANY choice of base permutations.

*Proof.* By ambivalence of S_5, there exists a permutation matrix
P ∈ S_5 (with entries in {0,1}, invertible over Z_n) such that
π_j^{-1} = P · π_j · P^{-1}. Substituting:

    S_{j-1} · π_j^{-1} · S_{j-1}^{-1}
    = S_{j-1} · P · π_j · P^{-1} · S_{j-1}^{-1}
    = (S_{j-1} P) · π_j · (S_{j-1} P)^{-1}

Since S_{j-1} is a uniformly random invertible matrix over Z_n,
and P is a fixed invertible matrix, the product S_{j-1} P is also
uniformly random over GL_5(Z_n). Therefore Q_j has the same
distribution in both cases. □

**Corollary (Cross-step independence).** When two instructions j
and k read the same input bit x_i, the joint distribution
(Q_j, Q_k) is identical for t_i = 0 vs t_i = 1. This is because
S_{j-1} and S_{k-1} are independent random matrices, so the
marginal distributions are independent and each is individually
blind by the Proposition above.

**Corollary (Eigenspace correlations).** An adversary examining
eigenspaces of Q_j and Q_k (for steps reading the same bit) cannot
detect correlations, because the conjugating matrices S_{j-1}P and
S_{k-1}P' are independently uniform, randomizing the eigenspaces
independently.

**Empirical verification.** The universal blindness property has
been verified computationally: (a) exhaustive check that all 120
elements of S_5 satisfy cycle_type(g) = cycle_type(g^{-1}) and are
conjugate to their inverses; (b) blindness of all L instructions
for all 16 targets with ℓ = 4; (c) blindness for ℓ = 4, 8, 16, 32
(up to L = 1024 instructions); (d) blindness with alternative base
permutations (3-cycles, 5-cycles, mixed); (e) 2000-trial paired
test over Z_n confirming identical traces; (f) 2000-trial cross-
step test confirming zero correlation.
*[See supplementary code: `01_p9_ambivalence_verification.py`]*

**Summary.** The similarity attack is **completely blind at every
level** of the Barrington tree, not just at leaves. This
significantly strengthens the security of the base construction:
the similarity attack reveals no information about T whatsoever.

#### 3.4.4 Other Attacks on the Base Construction

**GCD attack on matrix entries.** Each entry of M̂_{j,b} is a
Z_n-linear combination of entries of S_{j-1} and S_j^{-1}. For
random S_j, each entry is uniform in Z_n, so gcd(entry, n) = 1
with overwhelming probability. **Not a threat.**

**CRT decomposition.** Reducing M̂_{j,b} mod p would reveal the
raw permutation matrix M_{j,b}, immediately exposing T. But
computing mod p requires factoring n. **Reduced to RSA.**

**Bookend probing.** The adversary has û^T, v̂, and s. Recovering
u and v requires inverting S_0 and S_L (which requires factoring n).
From s alone: one equation in 10 unknowns plus unknown π_accept.
**Heavily underdetermined, not a threat.**

**Evaluation-based attacks.** The adversary evaluates π_base on
many inputs x ≠ T, obtaining scalars α_x = u^T · BP(x) · v. Since
|S_5| = 120, there are at most 120 distinct scalar values. But the
adversary does not know which permutation produced each scalar
(the mapping x → BP(x) is hidden by the Kilian randomization).
Without this labeling, the system of equations is unstructured.
**Mitigated but deserves further analysis (see Section 3.7).**

#### 3.4.5 Summary of Base Construction Cryptanalysis

| Attack | Result | Status |
|---|---|---|
| Similarity (eigenvalues) | Does not factorize n | Proven (Prop. 3.4.2) |
| Similarity (cycle structure) | Universally blind (ambivalence of S_5) | Proven (Prop. 3.4.3) |
| Similarity (cross-step eigenspaces) | No detectable correlation | Proven (Cor. 3.4.3) |
| GCD on entries | Not a threat | Random entries |
| CRT decomposition | Reduced to RSA | |
| Bookend probing | Not a threat | Underdetermined |
| Evaluation-based | Mitigated by unknown labeling | Needs analysis |

---

### 3.5 The Hardened Construction: Dynamic Encoding

The cryptanalysis of Section 3.4 shows that the similarity attack is
completely blind at all levels — a stronger result than initially
expected. Nevertheless, we introduce a state-dependent variant of
Kilian randomization for two reasons: (1) defense in depth against
future attacks that may exploit the shared randomizer S_j in ways
beyond the similarity quotient, and (2) prevention of local mix-and-
match combinations of matrices from different evaluation paths, which
is a prerequisite for the global consistency analysis in Section 3.5.7.

#### 3.5.1 Intuition

The similarity attack works because the two matrices at step j share
the same randomizer S_j on the right:

    M̂_{j,0} = S_{j-1} · M_{j,0} · S_j^{-1}
    M̂_{j,1} = S_{j-1} · M_{j,1} · S_j^{-1}

When the adversary computes M̂_{j,0} · M̂_{j,1}^{-1}, the shared
S_j cancels. The fix is to make S_j depend on the bit value, so
that different bit choices use different right-randomizers.

#### 3.5.2 State-Dependent Randomization

For each step j ∈ {1,...,L} and each bit value b ∈ {0,1}, sample
an independent random invertible matrix S_{j,b} ∈ GL_5(Z_n).

Boundary conditions:
- S_{0,0} = S_{0,1} = S_0 (fixed, independent of b, to match the
  left bookend)
- S_{L,0} = S_{L,1} = S_L (fixed, independent of b, to match the
  right bookend)

For each step j and each pair (b_prev, b_curr) ∈ {0,1}², compute:

    M̃_{j, b_prev, b_curr} = S_{j-1, b_prev} · M_{j, b_curr} · S_{j, b_curr}^{-1}  (mod n)

This yields 4 matrices per step instead of 2.

#### 3.5.3 The Obfuscated Program (Hardened Version)

The obfuscated program π_hard consists of:
- Public modulus n
- Left bookend û^T = u^T · S_0^{-1} (mod n)
- Right bookend v̂ = S_L · v (mod n)
- Target scalar s = u^T · π_accept · v (mod n)
- Instruction set: {(i_j, M̃_{j,00}, M̃_{j,01}, M̃_{j,10}, M̃_{j,11})}_{j=1}^{L}

where M̃_{j,bc} abbreviates M̃_{j, b_prev=b, b_curr=c}.

#### 3.5.4 Evaluation (Hardened Version)

**Input:** x = (x_1, ..., x_ℓ) ∈ {0,1}^ℓ

**Algorithm:**
    R ← I_{5×5}
    b_prev ← 0  (initial state)
    For j = 1 to L:
        b_curr ← x_{i_j}
        R ← R · M̃_{j, b_prev, b_curr}  (mod n)
        b_prev ← b_curr
    α ← û^T · R · v̂  (mod n)
    If α = s: return 1
    Else: return 0

**Correctness.** For a consistent input x, at each step j the
evaluator uses b_prev = x_{i_{j-1}} (the bit read at the previous
step) and b_curr = x_{i_j} (the current bit). The product telescopes:

    M̃_{j, x_{i_{j-1}}, x_{i_j}} · M̃_{j+1, x_{i_j}, x_{i_{j+1}}}
    = (S_{j-1, x_{i_{j-1}}} · M_{j, x_{i_j}} · S_{j, x_{i_j}}^{-1})
      · (S_{j, x_{i_j}} · M_{j+1, x_{i_{j+1}}} · S_{j+1, x_{i_{j+1}}}^{-1})

The middle terms S_{j, x_{i_j}}^{-1} · S_{j, x_{i_j}} = I cancel.
Over the full product:

    R = S_0 · BP(x) · S_L^{-1}

and the scalar output is α = u^T · BP(x) · v, exactly as in the
base construction. Correctness is identical. ✓

**Remark (Initial state).** The choice b_prev = 0 for j = 1 is
fixed and public. Since S_{0,0} = S_{0,1} = S_0, this does not
affect the telescoping or the security.

#### 3.5.5 Why Dynamic Encoding Eliminates the Similarity Attack

The adversary attempts the same quotient attack as in Section 3.4.1.
Taking two matrices from step j with the same b_prev = 0:

    M̃_{j,0,0} · (M̃_{j,0,1})^{-1}
    = (S_{j-1,0} · M_{j,0} · S_{j,0}^{-1}) · (S_{j,1} · M_{j,1}^{-1} · S_{j-1,0}^{-1})
    = S_{j-1,0} · M_{j,0} · S_{j,0}^{-1} · S_{j,1} · M_{j,1}^{-1} · S_{j-1,0}^{-1}

The critical difference: the middle term is S_{j,0}^{-1} · S_{j,1},
which is NOT the identity (since S_{j,0} and S_{j,1} are independent
random matrices). The adversary does not obtain a similarity transform
of M_{j,0} · M_{j,1}^{-1}. Instead, they get:

    S_{j-1,0} · M_{j,0} · (RANDOM MATRIX) · M_{j,1}^{-1} · S_{j-1,0}^{-1}

The random matrix in the middle destroys all algebraic structure.
The eigenvalues, trace, and cycle structure of the raw permutation
quotient are completely hidden.

**Proposition.** In the hardened construction, the quotient
M̃_{j,b,0} · (M̃_{j,b,1})^{-1} is computationally indistinguishable
from a uniformly random matrix in GL_5(Z_n), assuming S_{j,0} and
S_{j,1} are independent and uniformly random.

#### 3.5.6 Mix-and-Match Prevention

The dynamic encoding also prevents mix-and-match attacks, where the
adversary tries to combine matrices from different evaluation paths.

If the adversary multiplies M̃_{j, 0, b_j} · M̃_{j+1, 1, b_{j+1}}
(using b_prev = 0 for step j but b_prev = 1 for step j+1, which is
inconsistent), the middle term becomes S_{j, b_j}^{-1} · S_{j, 1},
which equals I only if b_j = 1. For b_j = 0, the mismatch
S_{j,0}^{-1} · S_{j,1} produces a random matrix that destroys the
telescoping.

Therefore, only consistent evaluation paths (corresponding to actual
input strings x) produce meaningful results. All inconsistent paths
produce chaotic products.

#### 3.5.7 The Global Consistency Barrier and T-Independence

While dynamic encoding prevents local mix-and-match attacks (Section
3.5.5-3.5.6), it does not cryptographically enforce global input
consistency. Barrington's theorem requires reading each input bit x_i
multiple times (O(ℓ) times across L = ℓ² steps). An evaluator could
theoretically feed inconsistent values for the same bit at different
steps — for instance, asserting x_1 = 0 at step 2 but x_1 = 1 at
step 50. The dynamic encoding only enforces Markovian (step-to-step)
consistency: the transition from step j to step j+1 is valid, but
nothing binds distant reads of the same variable.

This "inconsistent path" vulnerability is the historical reason why
general-purpose obfuscation (iO) requires graded encodings
(multilinear maps) to cryptographically bind variables globally.
The entire apparatus of multilinear maps in the iO literature exists
precisely to solve this problem.

**Clarification on dynamic encoding's role.** Dynamic encoding
defends against algebraic attacks on the randomized matrices
(similarity attack, local mix-and-match). It does NOT defend against
inconsistent evaluation — an evaluator can still feed different
values for the same variable at different steps while maintaining
valid step-to-step transitions. The defense against inconsistent
evaluation relies on a different property, analyzed below.

**Empirical analysis of inconsistent paths.** We exhaustively
enumerated all 2^L paths for the ℓ = 4 construction (L = 16,
65,536 total paths) and sampled 10^6 paths for the ℓ = 8
construction (L = 64).

Key finding: **inconsistent paths CAN produce π_accept.** For
ℓ = 4, exactly 249 of 65,520 inconsistent paths produce π_accept
(rate 0.38%). For ℓ = 8, the rate is approximately 0.83% ≈ 1/120
= 1/|S_5|. The distribution of output permutations converges to
uniform over S_5 as the commutator tree depth increases.

| ℓ | L | Collision rate | 1/|S_5| | Ratio |
|---|---|---|---|---|
| 4 | 16 | 0.380% | 0.833% | 0.456 |
| 8 | 64 | 0.834% | 0.833% | 1.00 |

*[See supplementary code: `02_p13_collision_exhaustive.py` (ℓ=4 exhaustive),
`03_p13_collision_scaling.py` (ℓ=8 sampling)]*

This means an adversary evaluating a random L-bit path obtains
ACCEPT with probability approximately 1/120 — a constant, not a
negligible quantity. The adversary can find accepting paths in
approximately 120 random attempts.

**The T-independence property.** Despite the existence of
collisions, the collision count is **independent of the target T**.
For ℓ = 4: exactly 249 collisions for each of the 16 possible
targets. For ℓ = 8: rates within statistical noise across different
targets. The collision distribution depends on the structure of the
Barrington tree and the group S_5, not on which target T was
embedded.

This T-independence is the key security property. An adversary
evaluating inconsistent paths sees ACCEPT responses at a rate
(≈ 1/120) that carries zero information about which target T_b
was embedded in the program. In the IND-StructObf game:

- Consistent evaluations: accept iff x = T_b. Since T_b has
  super-logarithmic min-entropy, the adversary cannot find T_b.
  Each consistent query returns REJECT with probability 1 - 2^{-ℓ}.

- Inconsistent evaluations: accept with rate ≈ 1/|S_5|,
  INDEPENDENT of T_b. These acceptances tell the adversary nothing
  about the challenge bit b because the rate is the same for T_0
  and T_1.

The security does not come from "collisions are improbable"
(they are not — rate ≈ 1/120 is constant). It comes from
"collisions are T-independent": the adversary's view is
identically distributed regardless of the embedded target.

**Theorem (Uniform T-independence — proved).** Let BP_T be the
Barrington branching program for CC_T over {0,1}^ℓ using any
pair assignment where sibling pairs have element overlap 1. Let
D_T be the distribution over S_5 induced by evaluating BP_T on a
uniformly random L-bit string (ignoring variable consistency). Then:

    sup_{T ∈ {0,1}^ℓ}  d_TV(D_T, Uniform(S_5)) ≤ 0.546^{4^{k-2}}

where k = log₂(ℓ) is the tree depth. The constant 0.546 is the
worst-case operator norm across all 135 overlap-1 sibling
combinations and all 6 non-trivial representations of S_5,
verified with exact rational arithmetic (810 checks, zero failures).
For the paper's specific construction, the tighter bound
λ₃ = 1.99 × 10⁻³ at level 3 gives even faster convergence.

The proof has two independent parts:

*Part A (Exact T-independence):* D_T = D_{T'} for all T, T'. The
proof is by explicit bijection: for T, T' differing on bit set S,
define F_S: {0,1}^L → {0,1}^L by flipping b_j at every step j
that reads a variable in S. F_S is an involution that preserves
inconsistency (it flips ALL reads of each variable simultaneously)
and satisfies φ_{T'}(b) = φ_T(F_S(b)) (flipping the target bit and
flipping the input bit cancel). By change of variables, D_{T'} = D_T.
This proof requires no property of S_5 — it works for any group.
*[See: `07_proof_T_independence.py`]*

*Part B (Doubly exponential convergence):* The level-3 (ℓ = 8)
Fourier coefficients are computed exactly for all 6 non-trivial
representations by matrix multiplication. The worst-case operator
norm is λ₃ = 1.99 × 10⁻³ (representation (4,1)). From level 3
onward, submultiplicativity gives λ_{k+1} ≤ λ_k⁴, yielding
λ_k ≤ λ₃^{4^{k-3}} — doubly exponential decay. The level-2
contraction depends on the pair assignment: 3 of 6 possible sibling
combinations contract, and the paper's construction uses only
contracting combinations.
*[See: `06_contraction_operator.py`, `04_fourier_spectral_analysis.py`]*

Explicit decay table:

| ℓ | Tree depth k | d_TV upper bound |
|---|---|---|
| 8 | 3 | 1.99 × 10⁻³ |
| 16 | 4 | 1.58 × 10⁻¹¹ |
| 32 | 5 | 6.17 × 10⁻⁴⁴ |
| 64 | 6 | ~10⁻¹⁷⁴ |

**Summary.** The global consistency barrier means that an adversary
CAN find accepting paths easily (≈ 120 random tries). However,
these acceptances are T-independent noise: they exist equally for
every possible target and carry zero information about which target
was embedded. The security of the scheme rests on this T-independence,
not on the rarity of collisions.

---

### 3.6 Parameters and Efficiency

**Branching program length:** L = ℓ² for ℓ-bit inputs, since point
functions have AND-tree depth d = log₂(ℓ) and L = 4^d = ℓ².

**Remark.** This is tight for Barrington's construction. Point
functions are particularly well-suited because their logarithmic
circuit depth yields polynomial-length branching programs. General
NC¹ circuits could have larger depth and correspondingly longer
programs.

#### 3.6.1 Base Construction Size

- 2L matrices of 5×5 over Z_n, plus 2 bookend vectors and 1 scalar
- Total: (50L + 11) × log₂(n) bits ≈ 50L · log₂(n) bits

| Input bits ℓ | L = ℓ² | Size (n=2048 bit) | Eval time (~1μs/mul) |
|---|---|---|---|
| 32 | 1,024 | 105 MB | ~130 ms |
| 64 | 4,096 | 420 MB | ~0.5 s |
| 128 | 16,384 | 1.68 GB | ~2 s |

#### 3.6.2 Hardened Construction Size

- 4L matrices of 5×5 over Z_n (doubled due to (b_prev, b_curr) pairs)
- Total: (100L + 11) × log₂(n) bits ≈ 100L · log₂(n) bits

| Input bits ℓ | L = ℓ² | Size (n=2048 bit) | Eval time |
|---|---|---|---|
| 32 | 1,024 | 210 MB | ~260 ms |
| 64 | 4,096 | 840 MB | ~1 s |
| 128 | 16,384 | 3.36 GB | ~4 s |

Evaluation time is dominated by 5×5 matrix multiplications over Z_n
(125 modular multiplications each). This is simple arithmetic with
no lattice operations, FFTs, or Gaussian sampling.

**Remark (modulus sizing).** The tables above use a fixed n = 2048
bits for illustration. The modulus size is determined by the
factoring assumption: n should be large enough that factoring n is
computationally infeasible (standard RSA parameters of 2048-4096
bits suffice). Unlike LWE-based schemes, our modulus size does not
depend on the input length ℓ.

#### 3.6.3 Comparison with LWE-based Constructions

Wichs-Zirdelis (2017) achieves C&C obfuscation under LWE for general
functions, but requires encoding via branching programs + multilinear
maps. Concrete parameters are not explicitly published but are
estimated to produce programs of comparable or larger size.

Our construction trades a new (unproven) security assumption for:
- Conceptual simplicity (matrix multiplication over Z_n)
- No lattice operations or Gaussian sampling
- No multilinear maps or graded encodings
- Security based on number-theoretic structure (composite modulus)
  rather than worst-case lattice problems

**OPEN PROBLEM: Compact representation.** Can the randomized matrices
be represented more compactly via seed-based generation (derive S_j
from a PRG), structured randomization, or compression?

---

### 3.7 Security Analysis

#### 3.7.1 Security Assumption

**Assumption 1 (MBPI — Matrix Branching Program Indistinguishability
over Z_n).** Let n = pq be an RSA modulus. Let CC_{T_0} and CC_{T_1}
be two point functions with targets T_0, T_1 drawn from a distribution
D where both have super-logarithmic min-entropy given auxiliary
information aux. Let π_0 and π_1 be their obfuscations (under either
the base or hardened construction) with independent randomness.

The MBPI assumption states that:

    (π_0, aux) ≈_c (π_1, aux)

**Theorem (informal).** If the MBPI assumption holds, then the
(base or hardened) construction satisfies IND-StructObf security
(Definition 7 of Section 2).

*Proof sketch.* The IND-StructObf game samples (T_0, T_1, aux)
from D, obfuscates T_b, and challenges the adversary to guess b.
The adversary's advantage is exactly the MBPI distinguishing
advantage. □

#### 3.7.2 Structural Arguments for Security

While we do not have a full reduction to a standard assumption, we
identify four structural barriers that any adversary must overcome:

**1. Factoring barrier.** The CRT decomposition of matrices over Z_n
requires knowing p and q. Without factoring, the adversary cannot
separate the permutation structure (which lives in {0,1}) from the
randomization (which lives in Z_n). This is the RSA assumption.

**2. Single-program distributional setting.** Unlike iO (where the
adversary receives two functionally equivalent programs), our
adversary receives a single program π_b. The most powerful known
attacks on obfuscation (annihilation attacks, Miles-Sahai-Zhandry
2016) require comparing two obfuscations of equivalent programs.
In our setting, there is no second program to compare against.

More precisely: annihilation attacks evaluate both programs on zero-
inputs and find polynomial relations between the encodings. With only
one program, the adversary can evaluate on zero-inputs but has no
reference point for comparison. The attack does not apply.

**3. Bookend compression.** The evaluator's output per query is a
single scalar in Z_n, not a full 5×5 matrix. This eliminates 24 of
25 algebraic coordinates that eigenvalue and rank attacks would
exploit. The adversary's view of each evaluation is one pseudorandom
element of Z_n.

**4. Similarity attack immunity (hardened version).** In the dynamic
encoding construction, the quotient M̃_{j,b,0} · (M̃_{j,b,1})^{-1}
no longer yields a similarity transform of the raw permutation
quotient. The independent randomizers S_{j,0} and S_{j,1} inject
entropy that destroys the algebraic structure.

**5. T-independence of inconsistent evaluation (proved).** We prove
(Theorem, Section 3.5.7) that inconsistent evaluation paths produce
permutations whose distribution is exactly independent of T and
converges to uniform over S_5 with doubly exponential speed. The
T-independence is an exact algebraic identity (proved by a flip
bijection, Section 5.4.1), and the convergence rate satisfies
d_TV ≤ 0.546^{4^{k-2}} where k = log₂(ℓ) (proved by spectral
contraction analysis, Section 5.4.2). An adversary CAN find
accepting paths easily (≈ 120 random tries), but these acceptances
carry exactly zero information about T and cannot be used to
distinguish obfuscations of different targets in the IND-StructObf
game. *[See: `07_proof_T_independence.py`, `06_contraction_operator.py`]*

#### 3.7.3 Honest Assessment

The MBPI assumption is **new** and not yet validated by the
cryptographic community. We do NOT claim provable security under
standard assumptions. Our contribution is:

1. A concrete candidate that instantiates the structural destruction
   framework of Section 2
2. Identification and analysis of the most natural attack vectors
3. A base construction with proven complete resistance to the
   similarity attack at all levels (no factoring leak, complete
   blindness via ambivalence of S_5)
4. A hardened construction with defense-in-depth via state-dependent
   randomization and local mix-and-match prevention
5. Proof that inconsistent evaluation paths produce a distribution
   over S_5 that is exactly T-independent (by flip bijection) and
   converges to uniform doubly exponentially (by spectral contraction),
   resolving the global consistency barrier for point functions
6. Reduction of MBPI to: factoring + algebraic security of Kilian
   randomization over Z_n (the T-independence component is now proved)

The closest studied assumptions in the literature are:
- Matrix DDH over prime-order groups (different setting: prime vs
  composite, no branching program structure)
- Branching program indistinguishability in graded encoding models
  (different: uses multilinear maps, not raw Z_n arithmetic)
- Security of Kilian randomization in the generic group model
  (different: generic model abstracts away the ring structure)

We encourage cryptanalysis of both the base and hardened
constructions. The remaining open question is whether Kilian
randomization over Z_n (without graded encodings) hides permutation
structure from algebraic attacks beyond similarity — a qualitatively
simpler question than the original MBPI assumption.

---

### 3.8 Open Problems

1. ~~**Prove uniform T-independence.**~~ **RESOLVED.** The
   T-independence of D_T is proved exactly by flip bijection
   (Section 5.4.1): for any T, T' differing on bit set S, the
   map F_S that flips all readings of variables in S is an
   inconsistency-preserving involution satisfying φ_{T'}(b) =
   φ_T(F_S(b)). Convergence to uniform is proved with doubly
   exponential bound d_TV ≤ 0.546^{4^{k-2}} by spectral
   contraction analysis (Section 5.4.2). MBPI now reduces to
   factoring + algebraic security of Kilian over Z_n.
   *[See: `07_proof_T_independence.py`, `06_contraction_operator.py`]*

2. **Prove or disprove MBPI.** With T-independence resolved, can
   MBPI be reduced to factoring alone, or is there a polynomial-time
   algebraic attack on Kilian randomization over Z_n? This is now
   the primary open problem.

3. ~~**Rate of convergence.**~~ **RESOLVED.** The convergence is
   doubly exponential: d_TV ≤ λ^{4^{k-2}} with λ₂ = 0.546 (universal). This is
   far faster than the exponential decay initially conjectured.

4. **Formal analysis of evaluation-based attacks.** Rigorously
   characterize what the collection of scalars {α_x : x queried}
   reveals about T, given that consistent queries return 0 except
   at T, inconsistent queries accept with T-independent rate
   ≈ 1/120, and the bookends compress 25 coordinates to 1.

5. **Compact representation.** Can the program size be reduced via
   seed-based generation (deriving S_{j,b} from a PRG), matrix
   compression, or algebraic structure?

6. ~~**Extension beyond point functions.**~~ **PARTIALLY RESOLVED.**
   Computational experiments confirm the construction extends to
   conjunctions with wildcards. T-independence is exact for all
   conjunction patterns (verified exhaustively for ℓ = 4, all 16
   wildcard configurations × 16 targets). The flip bijection proof
   extends directly. Spectral contraction from ℓ = 4 to ℓ = 8 is
   strong for all wildcard fractions up to 75% (contraction ≤ 0.12).
   The only case without contraction is the trivial function (100%
   wildcards), which has no secret to protect. Remaining work:
   formal contraction bound for conjunctions, and extension to
   general C&C functions beyond conjunctions.
   *[See: `08_via3_conjunctions.py`]*

7. **Universal mixing conjecture — investigated, partially negative.**
   Computational investigation (Section 5.6) tested whether
   functionally equivalent branching programs with different structure
   produce indistinguishable inconsistent-path distributions. Findings:
   (a) Variable grouping does NOT affect D (exact, ℓ=4).
   (b) Different pair assignments for the same circuit produce
       different distributions D, but with nearly identical d_TV to
       uniform (0.190 vs 0.192 for two OR-of-AND circuits).
   (c) Both balanced and skewed trees converge to uniform at ℓ=8
       (d_TV ≈ 0.008 for both), suggesting iO via triangle inequality
       (both → uniform → indistinguishable) rather than D₁ = D₂.
   (d) NOT gates introduce constant steps (m₀=m₁) that inflate program
       length without contributing to mixing.
   (e) Non-monotone circuits (XOR, MAJORITY) require a careful global
       implementation of Barrington's theorem; ad hoc constructions
       fail. This remains open for future work.
   The universal mixing hypothesis is FALSE in the strong sense
   (D_{C₀} ≠ D_{C₁} for structurally different programs), but may
   hold in the weak sense needed for iO (both converge to uniform).
   *[See: `09_io_investigation.py`]*

8. **Divisor-of-zero analysis.** Characterize the probability and
   impact of S_j matrices that are invertible mod n but singular
   mod p or mod q.

**Resolved during preparation of this manuscript:**

(a) The similarity attack is universally blind at all levels of the
Barrington tree, by the ambivalence of S_5 (Section 3.4.3).
*[See: `01_p9_ambivalence_verification.py`]*

(b) The Uniform T-Independence Conjecture (original Problem 1) is
proved: D_T is exactly T-independent, and converges to uniform
doubly exponentially (Section 5.4).
*[See: `07_proof_T_independence.py`, `06_contraction_operator.py`]*

---

## 4. Related Work and Security Against Known Attacks

This section positions our construction within the landscape of
obfuscation research and provides a systematic analysis of why
published attacks on obfuscation schemes do not transfer to our
setting. We organize by attack family, identify the structural
features each attack exploits, and explain why those features are
absent from our construction.

### 4.1 Annihilation Attacks (Miles-Sahai-Zhandry, CRYPTO 2016)

Miles, Sahai, and Zhandry introduced annihilation attacks against
iO candidates built on GGH13 multilinear maps. The attack
constructs a low-degree polynomial that annihilates the algebraic
structure leaked through GGH13's zero-testing parameter.

The attack requires three structural features simultaneously:

(a) **GGH13's ring structure and zero-testing parameter.** In
GGH13, an encoded element u = [(α + gr)/z^j]_q is tested for zero
via a public parameter p_zt = [hz^k/g]_q. After zero-testing, the
leading coefficient retains algebraic structure from the branching
program — the "g-stratification" that the annihilating polynomial
exploits. Over raw Z_n without multilinear maps, there is no
encoding, no zero-testing parameter, and no ring structure to
stratify.

(b) **The iO two-program game.** The attacker designs two
functionally equivalent candidate programs before receiving the
obfuscation, then constructs the annihilating polynomial based on
algebraic differences between the candidates. In our distributional
single-program setting, the adversary receives one program π_b and
has no second program to compare against.

(c) **Zero-output evaluations that reveal algebraic structure.**
Over GGH13, evaluating the obfuscated program on zero-output inputs
and applying p_zt produces ring elements with exploitable structure.
Over Z_n, evaluating on zero-output inputs produces the scalar
û^T · P · v̂ (mod n) for some permutation P ≠ π_accept — a single
pseudorandom element of Z_n with no algebraic content beyond its
value.

Follow-up works (Apon-Döttling-Garg-Mukherjee, ICALP 2017;
Chen-Gentry-Halevi, EUROCRYPT 2017; Cheon-Hhan-Kim-Lee, CRYPTO
2018) extend annihilation to other GGH13-based constructions but
all require GGH13 structure. **None apply to our setting.**

### 4.2 ADP Attacks (Bartusek et al., ITCS 2020; Yao-Chen-Yu, EUROCRYPT 2022)

Affine Determinant Programs compute f(x) = Eval(det(A + Σ x_i B_i))
over F_p. Bartusek et al. identified five vulnerability classes in
their own self-cryptanalysis:

**Polynomial extension attack (§9.1):** Exploits the fact that
det(M(x)) is a multilinear polynomial of degree ≤ k in the input
bits. Two functionally equivalent programs may disagree on non-binary
extensions to F_p^n. This is a polynomial identity testing attack
that can extract structural information from a single program, but
operates in the ADP computational model (access to full ADP matrix
entries, evaluation on non-binary inputs) which differs from
Kilian-randomized branching programs over Z_n.

**Kernel attack:** For accepting inputs x_i, det(M(x_i)) = 0 and
M(x_i) has a one-dimensional kernel. Linear relationships between
kernel vectors across different accepting inputs reveal program
structure. This attack requires **multiple accepting inputs**. For
point functions with exactly one accepting input, this attack surface
vanishes entirely.

**External attack (Yao-Chen-Yu, EUROCRYPT 2022):** Targets the
Random Local Substitution (RLS) step in the ADP obfuscation pipeline
specifically. Applies to "a fairly general class of programs" but
exploits algebraic weaknesses in RLS — a transformation that does
not appear in our construction.

Notably, Bartusek et al. themselves observed that **conjunction and
point function obfuscation has provable security under the LPN
assumption** when using the construction of Bartusek, Lepoint, Ma,
and Zhandry (EUROCRYPT 2019). This is a direct precedent: restricted
function classes avoid the vulnerabilities of general-circuit
candidates.

### 4.3 Rank Attacks

**Gentry-Jutla-Kane (ePrint 2018/756)** proposed purely algebraic
obfuscation using tensor products over matrix groups without
multilinear maps. The paper contains self-cryptanalysis based on
computing tangent spaces of the underlying algebraic sets — Jacobian
matrices reveal rank information that exposes branching program
structure. The paper was never published at a peer-reviewed venue.

**Chen's evaluation matrix attack (TCC 2019):** Given oracle access
to F: {0,1}^ℓ → R computed by a read-c, width-w branching program,
construct an evaluation matrix V where V(i,j) = F(x_i || x_j). For
a branching program, rank(V) ≤ w^{2c-1}, while a random function
has full rank. This attack works through scalar output alone.

However, **this attack is ineffective against evasive point
functions.** When F is a point function, V(i,j) = 0 for all entries
except at most one, giving rank ≤ 1 regardless of computational
model. The authors explicitly acknowledge this: the attack "cannot
be mounted when the function being obfuscated is evasive."

### 4.4 Zeroizing and Statistical Zeroizing Attacks

These attacks (Hu-Jia, EUROCRYPT 2016; Cheon-Lee-Ryu, ASIACRYPT
2015; Coron, EUROCRYPT 2014) exploit the zero-testing parameter
of multilinear maps. In our construction, there are no multilinear
maps and no zero-testing parameter. **These attacks have no analog
in our setting.**

### 4.5 NLinFE Attacks (Agrawal-Pellet-Mary, EUROCRYPT 2020)

Agrawal's "Noisy Linear FE" used NTRU-like noise at multiple levels
structured by public moduli p_0, p_1. The attack isolates a weak
noise term by reducing modulo p_1, then divides by p_0 and reduces
modulo p_0 to recover a small term. A matrix constructed from these
isolated terms has rank revealing the encrypted message bit.

This attack exploits the specific multi-level noise structure of
NTRU-based functional encryption. **It has no analog in raw matrix
arithmetic over Z_n** — there are no noise levels, no public moduli
to reduce by, and no NTRU structure.

### 4.6 Ye-Liu Dynamic Fencing (ePrint 2016/095)

Ye and Liu proposed "dynamic encoding" to eliminate multilinear maps
from branching program obfuscation for regular NC^1 programs. The
paper was **never published at any peer-reviewed venue** and has
zero citations in the mainstream obfuscation literature. The
definitive works on iO without multilinear maps (Ananth-Jain-Sahai,
Agrawal, Jain-Lin-Sahai 2021) none cite it. No formal cryptanalysis
was published. The authors' own follow-up work (ePrint 2017/321)
reverted to graded encoding schemes.

Our dynamic encoding (Section 3.5) addresses a similar intuition
(state-dependent randomization to prevent mix-and-match) but differs
in construction details, target function class (point functions vs
general NC^1), and security claims (we present a candidate with
honest assessment vs their claimed but unvalidated security).

### 4.7 The Genuine Threat: Algebraic Invariants of Kilian Randomization

The analysis above shows that published attacks on obfuscation
schemes do not transfer to our construction. The genuine threat
comes from a more elementary direction: **algebraic invariants of
Kilian randomization itself.**

Given randomized matrices M̂_{j,0} = S_{j-1} · M_{j,0} · S_j^{-1}
and M̂_{j,1} = S_{j-1} · M_{j,1} · S_j^{-1}, the quotient
M̂_{j,0} · M̂_{j,1}^{-1} = S_{j-1} · (M_{j,0} · M_{j,1}^{-1}) ·
S_{j-1}^{-1} reveals the similarity class of the raw quotient.
The characteristic polynomial, trace, determinant, and eigenvalue
ratios are all conjugacy invariants computable without knowing S.

This is the attack we analyze in detail in Section 3.4. We prove:

(a) The attack does not factorize n (Proposition, §3.4.2), because
permutation matrices have entries in {0,1} identical mod p and mod q.

(b) The attack is universally blind at all levels (Proposition,
§3.4.3), because S_5 is ambivalent: every element is conjugate to
its inverse, so the similarity invariants of π and π^{-1} are
identical. This holds for any choice of base permutations.

(c) Cross-step correlations are undetectable (Corollary, §3.4.3),
because the randomizing matrices at different steps are independent.

### 4.8 What This Analysis Does and Does Not Establish

**What it establishes:** Our construction resists all published
attack families in the obfuscation literature, for concrete
structural reasons documented attack by attack. The similarity
attack — the most natural threat in our encoding-free setting —
is provably blind by the ambivalence of S_5.

**What it does not establish:** The absence of attacks from adjacent
fields (computational algebra over GL_5(Z_n), algebraic geometry,
number-theoretic techniques for matrix factorization over composite
moduli) that may apply to our specific setting but have not been
connected to the obfuscation literature. Additionally, the
community has never seriously cryptanalyzed Kilian randomization
over Z_n without encodings — the absence of published attacks
reflects lack of interest, not proven security.

This is precisely why we formalize security under the new MBPI
assumption (Section 3.7.1) and invite cryptanalysis. "Resists all
known attacks" is an argument for taking the candidate seriously.
"Provably secure" requires resolving the open problems of Section
3.8 — particularly the global consistency barrier (Problem 1) and
the structured collision analysis (Problem 3).

### 4.9 Comparison with Wichs-Zirdelis (FOCS 2017)

Wichs and Zirdelis construct compute-and-compare obfuscation under
the LWE assumption, achieving distributional virtual-black-box
security. Their construction uses LWE-based encodings and achieves
provable security — a qualitatively stronger result than ours.

Our construction targets the same function class but from a
different mathematical base:

| | Wichs-Zirdelis | This work |
|---|---|---|
| Assumption | LWE (standard) | MBPI (new, unvalidated) |
| Encoding | Lattice-based | None (raw Z_n arithmetic) |
| Multilinear maps | Via LWE machinery | None |
| Security | Provable (distributional VBB) | Candidate (empirical) |
| Similarity attack | Not applicable (hidden matrices) | Proven blind (ambivalence) |
| Global consistency | Enforced by LWE encoding | Not enforced (T-independence) |
| Inconsistent paths | Cannot be constructed | Accept with rate 1/|S_5|, T-independent |
| Conceptual simplicity | Complex | Simple (matrix multiplication) |

The comparison is not favorable to our construction in terms of
security guarantees. Our contribution is orthogonal: demonstrating
that a conceptually simple construction reaches the global
consistency barrier and resists all known attacks, potentially
opening a third path toward obfuscation that bypasses both
multilinear maps and lattices.

---

## 5. Empirical Analysis: Fourier Decomposition and Spectral Evidence

This section reports the results of a systematic computational
investigation of the construction's security properties. The
analysis produced three categories of results: a closed theorem
(P9, similarity blindness), a closed survey (P6, resistance to
published attacks), and strong empirical evidence toward the
central open conjecture (P13/Fourier, T-independence and
convergence to uniform).

### 5.1 Universal Blindness of the Similarity Attack (P9)

The open question of whether cycle structures at deep levels of
the Barrington tree leak information about T (Section 3.4.3) was
resolved by invoking the ambivalence of S_5. The key property —
cycle_type(g) = cycle_type(g⁻¹) for all g ∈ S_5 — was verified
exhaustively for all 120 group elements. This implies that the
similarity quotient Q_j at any step j has identical invariants
regardless of the secret bit, at any depth, for any choice of base
permutations. The result is a theorem (Proposition, Section 3.4.3),
not a heuristic.

Verification scope: all 120 elements of S_5; all 16 targets for
ℓ = 4; branching programs up to ℓ = 32 (L = 1024 instructions);
four alternative base permutation configurations (transpositions,
3-cycles, 5-cycles, mixed). Zero counterexamples in any test.
*[See: `01_p9_ambivalence_verification.py`]*

### 5.2 Resistance to Published Attacks (P6)

Six families of published attacks on obfuscation schemes were
analyzed for transferability to this construction. None apply,
for structural reasons specific to each attack:

- Annihilation attacks (MSZ16): require GGH13 ring structure,
  zero-testing parameter, and the iO two-program game — all absent.
- ADP kernel attacks (Bartusek+, Yao-Chen-Yu): require multiple
  accepting inputs — point functions have exactly one.
- Evaluation rank attacks (Chen+ TCC19): authors explicitly
  acknowledge ineffectiveness against evasive functions.
- NLinFE attacks (Agrawal-PM): exploit NTRU noise structure with
  no analog in raw Z_n arithmetic.
- Zeroizing attacks: require multilinear map zero-testing
  parameters that do not exist here.
- Similarity attacks: neutralized by ambivalence of S_5 (§5.1).

The analysis does not rule out attacks from adjacent fields
(computational algebra over GL_5(Z_n), algebraic geometry) that
have not been connected to the obfuscation literature. This gap
motivates the MBPI assumption and the invitation to cryptanalysis.

### 5.3 Collision Analysis and T-Independence Discovery (P13)

Exhaustive enumeration of all 2^16 = 65,536 evaluation paths for
ℓ = 4 revealed that 249 of 65,520 inconsistent paths produce
π_accept (rate 0.380%). Statistical sampling (10^6 paths) for
ℓ = 8 yielded a collision rate of 0.834% ≈ 1/|S_5| = 1/120.

The critical discovery: the collision count is **exactly
independent of T**. For ℓ = 4, all 16 possible targets produce
exactly 249 collisions. For ℓ = 8, rates across tested targets
fall within statistical noise of 1/120.

This falsifies the paper's original union bound argument (which
assumed collision probability 1/min(p,q) per path) but does NOT
break the scheme, because T-independent collisions carry zero
information about which target was embedded. The security argument
shifts from "collisions are improbable" to "collisions are
uninformative" — a fundamentally different and more accurate claim.

Dynamic encoding does NOT prevent these collisions: all 249
collision paths for ℓ = 4 survive the hardened construction. The
dynamic encoding defends against algebraic attacks on the matrices
(similarity, local mix-and-match), not against evaluation with
inconsistent bit sequences.
*[See: `02_p13_collision_exhaustive.py` (ℓ=4 exhaustive),
`03_p13_collision_scaling.py` (ℓ=8 sampling)]*

### 5.4 Fourier Decomposition on S_5

The distribution D_T over S_5 (induced by evaluating the branching
program on uniformly random L-bit strings, ignoring variable
consistency) was decomposed into the 7 irreducible representations
of S_5 using non-abelian Fourier analysis.

#### 5.4.1 T-Independence is Algebraically Exact

For ℓ = 4, the Fourier norms ||D̂_T(ρ)||²_F for all 6 non-trivial
representations have spread **exactly zero** across all 16 targets.
This is not a numerical approximation — the spread is 0.00e+00 at
machine precision. The distribution D_T depends on the structure
of the Barrington tree and the group S_5, not on T.

**Proof of exact T-independence.** The algebraic proof is short.
For T, T' differing on bit set S, define F_S: {0,1}^L → {0,1}^L
by flipping b_j at every step j that reads a variable in S. Then:
(1) F_S is an involution; (2) F_S preserves inconsistency (it flips
ALL reads of each variable simultaneously); (3) φ_{T'}(b) =
φ_T(F_S(b)) (changing the target bit and flipping the input bit
cancel at each step). By change of variables, D_{T'} = D_T. This
proof requires no property of S_5 — it works for any group, any
branching program width. It extends to conjunctions with wildcards.
*[See: `07_proof_T_independence.py`]*

#### 5.4.2 Doubly Exponential Spectral Decay (Proved)

Three correct Barrington constructions were verified:

| ℓ | L | Tree depth | Correctness | Rejects → I |
|---|---|---|---|---|
| 4 | 16 | 2 | 16/16 | ✓ |
| 8 | 64 | 3 | 256/256 | ✓ |
| 16 | 256 | 4 | 65,536/65,536 | ✓ |

The ℓ = 16 construction required a tree-based builder that inverts
compound programs by swapping children of the commutator (not by
replacing individual permutations), and two distinct sets of
non-commuting transposition pairs with non-commuting level-3
targets.
*[See: `05_barrington_construction_verification.py` (construction + Kilian test)]*

The Fourier analysis yields:

| ℓ | Depth | d_TV bound | Decay/level | ||D̂(4,1)||² |
|---|---|---|---|---|
| 4 | 2 | 3.24 × 10⁻¹ | — | 9.97 × 10⁻² |
| 8 | 3 | 1.91 × 10⁻² | 0.059 | 1.90 × 10⁻⁴ |
| 16 | 4 | 8.18 × 10⁻³ | 0.429 | 6.72 × 10⁻⁵ |

Geometric mean decay per tree level: **0.159**. The spectral gap
is approximately 0.84 per level — convergence to uniform is fast.

The standard representation (4,1) of dimension 4 dominates the
distance to uniform; all other non-trivial representations
contribute orders of magnitude less. The sign-twisted
representations have Fourier norms of order 10⁻⁸ (nonzero but
negligible).
*[See: `04_fourier_spectral_analysis.py` (all Fourier results)]*

#### 5.4.3 Analytic Contraction and Proof of Convergence

The empirical decay observed in §5.4.2 is explained analytically.
At each leaf of the Barrington tree, the output distribution is
{σ: 1/2, I: 1/2} for a transposition σ. For any irreducible
representation ρ of dimension d, the Fourier coefficient is
P_σ = (I_d + ρ(σ))/2, an orthogonal projection.

At level 1 (single AND block with transpositions σ, τ), the Fourier
coefficient is D̂ = (P_σ · P_τ)². Its operator norm can equal 1.0
because the projection eigenspaces may share an invariant direction.

**Level-2 contraction is pair-dependent.** An AND(A, B) at level 2
combines two level-1 blocks using different transposition pairs.
Exhaustive computation over all 6 possible sibling combinations of
the 4 pairs used in the construction reveals that 3 combinations
contract (||D̂||_op < 1) and 3 do not:

| Contracting | λ₂ | Non-contracting | λ₂ |
|---|---|---|---|
| A+B: (01)/(12)+(23)/(34) | 0.383 | A+C: (01)/(12)+(02)/(24) | 1.085 |
| C+D: (02)/(24)+(03)/(13) | 0.546 | A+D: (01)/(12)+(03)/(13) | 1.000 |
| B+D: (23)/(34)+(03)/(13) | 0.379 | B+C: (23)/(34)+(02)/(24) | 1.089 |

The paper's construction uses ONLY contracting combinations: A+B
for the ℓ=4 tree, and level2(A+B) with level2(C+D) for ℓ=8.
*[See: `06_contraction_operator.py`]*

**Level-3 base case (exact, all representations).** Rather than
relying on level-2 bounds, we compute the level-3 Fourier
coefficients EXACTLY for the paper's ℓ=8 construction by matrix
multiplication over all 6 non-trivial representations:

| Representation | dim | ||D̂_level3||_op |
|---|---|---|
| (4,1) | 4 | 1.99 × 10⁻³ |
| (3,2) | 5 | 4.61 × 10⁻⁷ |
| (3,1,1) | 6 | 2.50 × 10⁻¹² |
| (2,2,1) | 5 | 2.78 × 10⁻¹⁷ |
| (2,1,1,1) | 4 | ~0 |
| (1,1,1,1,1) | 1 | 0 |

**ALL representations contract massively at level 3.** The worst
case is (4,1) with λ₃ = 1.99 × 10⁻³.

**Inductive bound.** From level 3 onward, by submultiplicativity:
λ_{k+1} ≤ λ_k⁴. Starting from λ₃ = 1.99 × 10⁻³:

| ℓ | Tree depth k | d_TV upper bound |
|---|---|---|
| 8 | 3 | 1.99 × 10⁻³ |
| 16 | 4 | 1.58 × 10⁻¹¹ |
| 32 | 5 | 6.17 × 10⁻⁴⁴ |
| 64 | 6 | ~10⁻¹⁷⁴ |

**All-paths vs inconsistent-paths.** The analysis uses the
all-paths model (each bit iid). The security-relevant model
conditions on inconsistency. For ℓ=4, the exact operator norm
difference is 6.28 × 10⁻⁵ (relative error 0.016%). For ℓ ≥ 8,
the difference is bounded by p_con = 2^{ℓ-ℓ²} < 10⁻¹⁷. The
bound transfers with negligible error.

Combined with exact T-independence (§5.4.1), this proves:

    sup_{T ∈ {0,1}^ℓ}  d_TV(D_T, Uniform(S_5)) ≤ λ₃^{4^{k-3}}

where λ₃ = 1.99 × 10⁻³, for the paper's specific construction.
This is negligible for all ℓ ≥ 8.  □

**Universality (proved by exhaustive enumeration).** The level-2
contraction is governed by the element overlap between sibling pairs
and holds universally for ALL 6 non-trivial representations of S_5.
Exhaustive computation (135 overlap-1 combinations × 6
representations = 810 checks, zero failures) establishes:

**Theorem (Universal contraction criterion).** Let (σ_A, τ_A) and
(σ_B, τ_B) be two non-commuting transposition pairs in S_5. Let
E_A and E_B be the sets of elements moved by each pair (|E_A| =
|E_B| = 3). If |E_A ∩ E_B| = 1, then:

    ||D̂_level2(ρ)||_op < 1  for ALL non-trivial irreducible ρ

with worst-case λ₂ = 0.546 (attained by representation (4,1)).
If |E_A ∩ E_B| ≥ 2, then ||D̂_level2((4,1))||_op ≥ 1.

| Element overlap | (4,1) contracts | All reps contract |
|---|---|---|
| 1 | 135/135 (100%) | 135/135 (100%) |
| ≥ 2 | 0/300 (0%) | — |

The (4,1) representation is the bottleneck: all other representations
contract even MORE strongly (max op norms: (3,2): 0.078, (3,1,1):
0.011, (2,2,1): 2.4×10⁻⁴, (2,1,1,1): 4.0×10⁻⁵, sign: 0).

**Consequence:** For ANY Barrington construction using transposition
pairs where siblings have element overlap 1, the proof holds at
level 2 with λ₂ ≤ 0.546. This is not specific to the paper's
construction — it covers all valid pair assignments satisfying the
overlap condition. With 4 pairs of 3 elements in a universe of 5,
it is combinatorially impossible for ALL 6 pairings of 4 pairs to
have overlap 1 simultaneously (verified: 0 out of 27,405 four-pair
sets are universal). But the tree only requires overlap 1 for pairs
that appear as SIBLINGS, which is always achievable.

The doubly exponential bound starting from level 2:

    sup_T d_TV(D_T, Uniform(S_5)) ≤ 0.546^{4^{k-2}}

| ℓ | Level k | d_TV bound |
|---|---|---|
| 4 | 2 | 5.46 × 10⁻¹ |
| 8 | 3 | 8.87 × 10⁻² |
| 16 | 4 | 6.20 × 10⁻⁵ |
| 32 | 5 | 1.48 × 10⁻¹⁷ |

For the paper's specific construction, the tighter level-3 base
case λ₃ = 1.99 × 10⁻³ gives even faster convergence.

The convergence proof for conjunctions
(§5.5) is empirical, not analytic, though the mechanism (different
invariant subspaces at sibling blocks) is the same.

### 5.5 Extension to Conjunctions with Wildcards

The T-independence paradigm extends beyond point functions to
conjunctions — functions of the form CC_{T,W}(x) = 1 iff x[i] = T[i]
for all non-wildcard positions i ∉ W. In the branching program,
wildcard positions output σ for BOTH bit values (instead of σ for
one and I for the other).

#### 5.5.1 Construction and Correctness

Conjunction branching programs were constructed for ℓ = 8 with 0
through 8 wildcard positions. All constructions verified correct
(256/256 inputs for every wildcard pattern).
*[See: `08_via3_conjunctions.py`]*

#### 5.5.2 T-Independence for Conjunctions (Exact)

For a fixed wildcard pattern W, changing the target values T[i] at
non-wildcard positions does not affect D_T. This was verified
exhaustively for ℓ = 4: all 16 wildcard configurations × 16 targets
give Fourier norm spread of exactly zero. The flip bijection proof
extends directly: flipping bits at non-wildcard positions preserves
inconsistency and transforms one program into another; wildcard
positions are unaffected because they output σ regardless of bit value.

#### 5.5.3 Spectral Contraction for Conjunctions

The contraction from ℓ = 4 to ℓ = 8 was measured for matched
wildcard fractions:

| Wildcard fraction | ||D̂||² at ℓ=4 | ||D̂||² at ℓ=8 | Contraction |
|---|---|---|---|
| 0% (point function) | 1.47 × 10⁻¹ | 3.71 × 10⁻⁵ | 0.000252 |
| 25% | 2.12 × 10⁻¹ | 4.07 × 10⁻⁴ | 0.00192 |
| 50% | 6.08 × 10⁻¹ | 8.42 × 10⁻⁵ | 0.000138 |
| 75% | 1.69 | 2.08 × 10⁻¹ | 0.123 |
| 100% (trivial) | 7.00 | 7.00 | 1.000 (no contraction) |

The contraction is strong (< 0.002) for up to 50% wildcards,
moderate (0.12) for 75% wildcards, and absent only for the trivial
function (100% wildcards, accepts all inputs). The trivial function
is not a meaningful conjunction — it has no secret to protect.

Even with 7 of 8 bits wildcarded (a single-bit check), d_TV = 0.74
at ℓ = 8, and the contraction from deeper trees would drive it to
negligible.

#### 5.5.4 Implications

The extension to conjunctions significantly broadens the applicability
of the construction. Conjunctions capture pattern matching, attribute-
based access control, database queries with wildcards, and private
information retrieval with partial matching. The T-independence proof
(Part A) is fully rigorous for conjunctions. The spectral contraction
(Part B) is empirically verified and follows the same mechanism as
for point functions — different transposition pairs at sibling AND
blocks create non-identical invariant subspaces that destroy each
other in the commutator product.

The only caveat is the degenerate case of 100% wildcards, where no
contraction occurs. This is expected and harmless: a conjunction that
matches every input contains no secret information.

### 5.6 Investigation: Universal Mixing and iO Viability

The most ambitious question raised by the T-independence results is
whether the mixing phenomenon extends to ALL branching programs of
width 5 — not just those computing point functions or conjunctions.
If so, the paradigm would yield iO for NC¹ from factoring. We
investigated this computationally.

#### 5.6.1 The Correct Question

The naive question — "do functionally equivalent BPs produce
identical D?" — has a clear negative answer: different pair
assignments and tree structures produce different distributions.
However, iO does not require D_{C₀} = D_{C₁}. It requires
d_TV(D_{C₀}, D_{C₁}) ≤ negl(ℓ), which follows by triangle
inequality if both converge to uniform independently:

    d_TV(D_{C₀}, D_{C₁}) ≤ d_TV(D_{C₀}, U) + d_TV(D_{C₁}, U)

The real question is therefore: does EVERY branching program of
width 5 and sufficient depth have D → Uniform(S_5)?

#### 5.6.2 Results for Monotone Circuits

For AND-of-AND (point functions) and OR-of-AND circuits with
correct Barrington constructions:

| Circuit | L | d_TV to uniform |
|---|---|---|
| AND(x₀,x₁) | 4 | 0.958 |
| OR(x₀,x₁) | 9 | 0.950 |
| POINT(4 bits) | 16 | 0.309 |
| (x₀∧x₁)∨(x₂∧x₃) v.A | 21 | 0.190 |
| (x₀∧x₁)∨(x₂∧x₃) v.B | 21 | 0.192 |

Two versions of the same OR-of-AND circuit (different internal pair
assignments) produce different distributions (||D̂||² = 0.060 vs
0.134) but nearly identical distance to uniform (0.190 vs 0.192).
At ℓ = 8, both balanced and skewed AND-trees achieve d_TV ≈ 0.008.

**Variable grouping does not affect D** — permuting which variables
are grouped as siblings produces identical distributions (exact,
ℓ = 4).

#### 5.6.3 The NOT Gate Problem

NOT in Barrington is implemented by prepending a constant step
(m₀ = m₁ = π⁻¹). These constant steps contribute to program length
but NOT to mixing — they output the same permutation regardless of
input bit. An OR gate (= NOT∘AND∘NOT∘NOT) introduces 3 constant
steps per invocation. Complex circuits with many NOT gates carry
substantial "dead weight" that inflates L without improving
convergence. This does not prevent convergence, but it means
the effective mixing depth is less than L.

#### 5.6.4 Non-Monotone Circuits

Attempts to construct XOR and MAJORITY via Barrington's theorem
failed in this investigation due to the complexity of global
permutation assignment (ensuring non-commuting targets at every
AND gate). This is an implementation challenge, not a theoretical
barrier — Barrington's theorem guarantees that any NC¹ circuit
has a width-5 BP. A correct implementation would require a
systematic top-down assignment of target permutations.

#### 5.6.5 Verdict

The universal mixing hypothesis is **FALSE** in the strong sense:
D_{C₀} ≠ D_{C₁} for structurally different programs computing the
same function. But it may hold in the **weak sense** needed for iO:
both distributions converge to uniform, so their distance to each
other vanishes by triangle inequality. The critical open question
is whether convergence to uniform holds for ALL width-5 BPs of
sufficient depth, including those arising from non-monotone NC¹
circuits with many NOT gates.
*[See: `09_io_investigation.py`]*

---

## 6. Conclusions

We have presented a theoretical framework for privacy-preserving
computation based on structural destruction — the principle that
security comes from destroying structural relations that authorized
functions do not need. The framework provides a unified treatment
of functional encryption and program obfuscation through the
function kernel ker(F) and security entropy H_sec.

As a concrete instantiation, we constructed a candidate obfuscator
for point functions and conjunctions over Z_n using Barrington's
theorem and Kilian's randomization, without lattices, multilinear
maps, or graded encodings. The construction was subjected to
systematic analysis with the following results:

**Proven results:**
- The similarity attack is universally blind at all levels of the
  Barrington tree, by the ambivalence of S_5 (Section 3.4.3).
- No published attack family in the obfuscation literature
  transfers to this construction (Section 4).
- The construction is correct for ℓ = 4, 8, 16 with all rejects
  producing the identity permutation (Section 5.4.2).
- **The distribution D_T of outputs from inconsistent paths is
  exactly T-independent** — proved by flip bijection (Section 5.4.1).
  This proof requires no property of S_5 and extends to conjunctions.
- **D_T converges to uniform over S_5 doubly exponentially** — proved
  by spectral contraction analysis (Section 5.4.3), with explicit
  bound d_TV ≤ 0.546^{4^{k-2}} where k = log₂(ℓ).
- **The construction extends to conjunctions with wildcards**
  (Section 5.5). T-independence is exact for all conjunction patterns.
  Spectral contraction is empirically verified for wildcard fractions
  up to 75%, with strong convergence (contraction < 0.002) for up to
  50% wildcards.

**Change of security paradigm:**
The security of the construction does not rely on collisions being
improbable — they are not (rate ≈ 1/120 is constant). It relies on
collisions being T-independent: the adversary's view from
inconsistent evaluations is identically distributed regardless of
the embedded target. This "uninformative collisions" paradigm is,
to our knowledge, new in the obfuscation literature.

**Resolution of the global consistency barrier (for point functions
and conjunctions):**
The global consistency barrier — the inability to cryptographically
bind multiple reads of the same variable — has been the central
obstacle in obfuscation since Garg et al. (2013). For point
functions, we show this barrier is not a security threat: inconsistent
paths produce noise that is exactly T-independent and converges to
uniform doubly exponentially. The barrier remains open for general
circuits, but the assumption that it is insurmountable without
multilinear maps is no longer supported for restricted function
classes.

**Remaining open problem:** With T-independence proved, MBPI reduces
to: factoring + algebraic security of Kilian randomization over Z_n.
The remaining question is whether Kilian randomization over composite
moduli (without graded encodings) hides permutation structure from
algebraic attacks beyond similarity — a qualitatively simpler and
more focused question than the original MBPI assumption.

**Future directions:** Computational investigation (Section 5.6)
shows that the universal mixing hypothesis is false in the strong
sense (D_{C₀} ≠ D_{C₁}) but may hold in the weak sense needed for
iO (both → uniform → indistinguishable by triangle inequality).
The critical remaining question is whether convergence to uniform
holds for ALL width-5 BPs, including those from non-monotone NC¹
circuits with many NOT gates. Resolving this requires a careful
implementation of the full Barrington construction for general NC¹
and spectral analysis of the resulting branching programs.

We encourage cryptanalysis of both the base and hardened
constructions.

### Supplementary code

| Script | Verifies |
|---|---|
| `01_p9_ambivalence_verification.py` | Ambivalence of S_5, similarity blindness at all levels |
| `02_p13_collision_exhaustive.py` | 249 collisions for ℓ=4, exact T-independence (16 targets) |
| `03_p13_collision_scaling.py` | Collision rate convergence to 1/120 for ℓ=8 |
| `04_fourier_spectral_analysis.py` | Fourier decomposition, spectral decay for ℓ=4,8,16 |
| `05_barrington_construction_verification.py` | Correctness of Barrington + Kilian constructions |
| `06_contraction_operator.py` | Level-by-level contraction, spectral gap computation |
| `07_proof_T_independence.py` | Exhaustive verification of flip bijection proof |
| `08_via3_conjunctions.py` | Extension to conjunctions: correctness, T-independence, contraction |
| `09_io_investigation.py` | iO viability: equivalent circuits, overlap criterion, OR gates |
