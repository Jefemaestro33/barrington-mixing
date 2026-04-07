# Barrington Mixing: Obfuscation via Variable Transformations for FHE

Computational verification scripts and paper source for *Encriptacion Homomorfica basada en Transformaciones de Variable*.

This repository accompanies the research on a novel Fully Homomorphic Encryption (FHE) scheme based on nonlinear variable transformations, exploring connections to Barrington's theorem, spectral contraction, and indistinguishability obfuscation.

## Repository Structure

```
ofuscacion/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── paper/
│   ├── Smain.tex          # LaTeX source
│   ├── paper.tex           # Extended thesis source
│   ├── referencias.bib     # Bibliography
│   └── Spectral_Contraction_and_T_Independence_in_Barrington_Branching_Programs.pdf
├── submission-CiC/
│   ├── Smain_iacrcc.tex    # Formatted for IACR Communications in Cryptology
│   ├── iacrcc.cls          # IACR CiC document class
│   └── refs.bib            # Bibliography
└── scripts/
    ├── 01_p9_ambivalence_verification.py
    ├── 02_p13_collision_exhaustive.py
    ├── 03_p13_collision_scaling.py
    ├── 04_fourier_spectral_analysis.py
    ├── 05_barrington_construction_verification.py
    ├── 06_contraction_operator.py
    ├── 07_proof_T_independence.py
    ├── 08_via3_conjunctions.py
    ├── 09_io_investigation.py
    ├── 10_spectral_contraction_proof.py
    ├── 11_eigenvector_analysis.py
    ├── 12_level3_exhaustive_verification.py
    └── 13_all_representations_contraction.py
```

## Scripts Overview

| # | Script | Description |
|---|--------|-------------|
| 01 | `p9_ambivalence_verification` | Verifies ambivalence properties of P9 permutation groups |
| 02 | `p13_collision_exhaustive` | Exhaustive collision search over P13 |
| 03 | `p13_collision_scaling` | Scaling behavior of collisions in P13 |
| 04 | `fourier_spectral_analysis` | Fourier/spectral analysis of mixing operators |
| 05 | `barrington_construction_verification` | Verifies Barrington's theorem constructions |
| 06 | `contraction_operator` | Contraction operator analysis |
| 07 | `proof_T_independence` | Proves T-independence of the scheme |
| 08 | `via3_conjunctions` | Explores Via-3 conjunction constructions |
| 09 | `io_investigation` | Indistinguishability obfuscation investigation |
| 10 | `spectral_contraction_proof` | Spectral contraction proof verification |
| 11 | `eigenvector_analysis` | Eigenvector structure analysis |
| 12 | `level3_exhaustive_verification` | Level-3 exhaustive security verification |
| 13 | `all_representations_contraction` | Spectral contraction for all irreps of S_5 |

## Requirements

```bash
pip install -r requirements.txt
```

Python 3.9+ required. Dependencies: `numpy`, `sympy`.

## Usage

Run any script directly:

```bash
python scripts/01_p9_ambivalence_verification.py
```

## TODO

- [ ] Formalizar la prueba algebraica del Lemma de Direction Mixing (Lemma 3 / `lem:mixing`) — actualmente demostrado por enumeración exhaustiva. Una prueba algebraica cerrada fortalecería el resultado y potencialmente generaliza a profundidad arbitraria.

## Submission Status

- **IACR Communications in Cryptology (CiC):** Submitted 2026-03-31 (Submission #7, under review)
- **IACR ePrint:** Rejected (gap in Main Theorem proof — now fixed, see Script 13)

## License

MIT License. See [LICENSE](LICENSE).
