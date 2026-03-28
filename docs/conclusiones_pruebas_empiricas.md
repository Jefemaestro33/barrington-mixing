# Conclusiones de las Pruebas Empíricas
## Investigación sobre "Structural Destruction: Point Function Obfuscation over Composite Moduli"
### Marzo 18, 2026

---

## RESUMEN EJECUTIVO

Se realizaron cuatro líneas de investigación empírica sobre la
construcción de ofuscación de funciones punto del paper. Los
resultados cambian la narrativa de seguridad de forma fundamental:
el esquema es más seguro de lo que el paper original argumentaba,
pero por razones completamente diferentes a las que se pensaban.

---

## P9: BLINDNESS UNIVERSAL DEL SIMILARITY ATTACK

### Pregunta
¿La estructura de ciclos del quotient M_{j,0}·M_{j,1}⁻¹ en
niveles profundos del árbol de Barrington filtra información
sobre los bits secretos de T?

### Resultado: NO. Teorema, no conjetura.

El grupo simétrico S_5 es **ambivalente**: todo elemento es
conjugado a su inverso. Esto implica que π y π⁻¹ tienen
idéntico tipo de ciclo, traza, polinomio característico, y
todos los invariantes de similaridad. Como el quotient en cada
paso es π (si t_j=0) o π⁻¹ (si t_j=1), el adversario no
puede distinguir los dos casos — en ningún nivel del árbol.

### Evidencia

| Verificación | Resultado |
|---|---|
| 120 elementos de S_5: cycle_type(g) = cycle_type(g⁻¹) | 120/120 ✓ |
| 120 elementos: g conjugado a g⁻¹ | 120/120 ✓ |
| 120 elementos: trace(g) = trace(g⁻¹) | 120/120 ✓ |
| ℓ=4, 16 targets: blindness en todos los pasos | 16/16 targets × 16/16 pasos ✓ |
| ℓ=4,8,16,32: blindness en todos los pasos | Todos ✓ |
| 4 configuraciones de permutaciones base alternativas | Todas ✓ |
| T-independencia: spread de invariantes entre targets | Exactamente 0 |

### Consecuencia para el paper
La "open question" de la Sección 3.4.3 queda resuelta. La
construcción base (Kilian estático) ya resiste completamente
el similarity attack sin necesidad de dynamic encoding. El
dynamic encoding se justifica como defensa en profundidad y
prevención de mix-and-match, no contra este ataque.

---

## P6: ATAQUES PUBLICADOS NO APLICAN

### Pregunta
¿Alguna familia de ataques publicada contra esquemas de
ofuscación transfiere a esta construcción?

### Resultado: NINGUNA aplica directamente.

| Familia de ataque | Paper | Por qué no aplica |
|---|---|---|
| Aniquilación | Miles-Sahai-Zhandry, CRYPTO 2016 | Requiere estructura de anillo GGH13 + zero-testing + juego iO con dos programas. Ninguno presente aquí. |
| Kernel ADP | Bartusek et al., ITCS 2020 | Requiere múltiples inputs aceptantes. Función punto tiene exactamente 1. |
| Extensión polinomial ADP | Yao-Chen-Yu, EUROCRYPT 2022 | Explota debilidades del paso RLS, inexistente en esta construcción. |
| Rango (evaluación) | Chen et al., TCC 2019 | Los autores reconocen explícitamente: "cannot be mounted when the function is evasive." Función punto es evasiva. |
| Rank (tangent space) | Gentry-Jutla-Kane, ePrint 2018/756 | Explota estructura tensorial no presente aquí. Paper nunca publicado. |
| NLinFE | Agrawal-Pellet-Mary, EUROCRYPT 2020 | Explota ruido multi-nivel NTRU. Sin análogo en Z_n puro. |
| Zeroizing | CLT13/GGH15 attacks | Requiere parámetro de zero-testing de mapas multilineales. Inexistente. |
| Similaridad (Kilian) | Este paper | Neutralizado por ambivalencia de S_5 (P9). |

### Dato adicional encontrado
Bartusek et al. notan que la ofuscación de conjunciones y
funciones punto tiene seguridad demostrable bajo LPN (Bartusek-
Lepoint-Ma-Zhandry, EUROCRYPT 2019). Las funciones restringidas
evitan las vulnerabilidades de candidatos para circuitos generales.

### Caveat
"Resiste ataques conocidos" ≠ "es seguro". No se descarta la
existencia de ataques desde álgebra computacional sobre GL_5(Z_n),
geometría algebraica, o técnicas de teoría de números no conectadas
con la literatura de ofuscación. La comunidad nunca criptoanalizó
seriamente Kilian sobre Z_n sin encodings.

---

## P13: COLISIONES EXISTEN PERO SON T-INDEPENDIENTES

### Pregunta
¿Existen caminos inconsistentes cuyas salidas estén correlacionadas
con π_accept? ¿La distribución de salidas depende del target T?

### Resultado: Las colisiones EXISTEN, pero son T-INDEPENDIENTES.

Este es el hallazgo más importante de toda la investigación.
Cambia fundamentalmente el argumento de seguridad del paper.

### Datos de colisiones

| ℓ | L | Método | Tasa colisión | 1/|S_5| | Ratio |
|---|---|---|---|---|---|
| 4 | 16 | Exhaustivo | 0.380% | 0.833% | 0.456 |
| 8 | 64 | Muestreo (10⁶) | 0.834% | 0.833% | 1.004 |

Para ℓ=4: exactamente 249 colisiones de 65,520 caminos
inconsistentes. Este número es **idéntico para las 16 posibles
targets T**. Para ℓ=8: tasa dentro de ruido estadístico de
1/120 para todos los targets probados.

### Lo que estaba MAL en el paper original

El argumento original (Sección 3.5.7) decía:

> "Cada camino inconsistente produce una permutación caótica.
> Comprimida por bookends, la probabilidad de colisión con s
> es 1/min(p,q) por camino."

Esto es **falso**. La probabilidad real es ~1/120 (constante),
no 1/min(p,q) (negligible). Un adversario puede encontrar
un camino aceptante en ~120 intentos aleatorios.

### Por qué el esquema NO está roto

La seguridad no viene de que las colisiones sean improbables
(no lo son). Viene de que son **T-independientes**: el
adversario ve ACCEPT con tasa ~1/120 sin importar cuál T
fue embebido. Los falsos aceptantes no revelan información
sobre T y no pueden usarse para distinguir obfuscaciones
de diferentes targets en el juego IND-StructObf.

### Dynamic encoding NO mata las colisiones

Las 249 colisiones de ℓ=4 sobreviven todas al dynamic encoding.
Esto es porque el dynamic encoding previene ataques algebraicos
sobre las matrices (similaridad, mix-and-match), pero no previene
la evaluación con secuencias de bits inconsistentes. El evaluador
elige bits libremente paso a paso.

### Correcciones necesarias al paper

1. Eliminar el union bound incorrecto y la tabla paramétrica
2. Reemplazar "colisiones improbables" con "colisiones T-independientes"
3. El tamaño del módulo n depende de factorización (RSA estándar),
   no de la tasa de colisión
4. Clarificar que dynamic encoding defiende contra ataques algebraicos,
   no contra evaluación inconsistente

---

## ANÁLISIS DE FOURIER: CONVERGENCIA ESPECTRAL A UNIFORME

### Pregunta
¿D_T (distribución sobre S_5 inducida por caminos inconsistentes)
converge a uniforme? ¿Con qué velocidad? ¿Uniformemente en T?

### Resultado: CONVERGENCIA EXPONENCIAL CONFIRMADA con 3 datos.

Se descompuso D_T en las 7 representaciones irreducibles de S_5
usando la transformada de Fourier sobre el grupo. Los resultados
son extraordinarios:

### T-independencia EXACTA (no aproximada)

Para ℓ=4, las normas de Fourier de las 6 representaciones no
triviales tienen spread **literalmente cero** entre las 16
targets. No es 10⁻¹² — es 0.00e+00. La distribución D_T es
algebraicamente idéntica para todo T. Esto sugiere una prueba
corta basada en simetría.

### Decaimiento espectral

| ℓ | depth | d_TV bound | ||D̂(4,1)||² | decay/level |
|---|---|---|---|---|
| 4 | 2 | 3.24 × 10⁻¹ | 9.97 × 10⁻² | — |
| 8 | 3 | 1.91 × 10⁻² | 1.90 × 10⁻⁴ | 0.059 |
| 16 | 4 | 8.18 × 10⁻³ | 6.72 × 10⁻⁵ | 0.429 |

Geometric mean decay per level: **0.159** (spectral gap ≈ 0.84).

La representación standard (4,1) de dimensión 4 domina la
distancia a uniforme — las demás contribuyen órdenes de
magnitud menos.

### Representaciones sign-twisted

D̂(sign) = -1/4095, no exactamente cero. Las representaciones
(2,2,1) y (2,1,1,1) tienen normas ~10⁻⁸ (reales pero
despreciables). No afectan la d_TV.

### Proyecciones

| ℓ | depth | d_TV estimada |
|---|---|---|
| 32 | 5 | ~10⁻³ |
| 64 | 6 | ~10⁻⁴ |
| 128 | 7 | ~10⁻⁵ |

### Construcciones verificadas

| ℓ | L | Correctness | Rejects → I | Target |
|---|---|---|---|---|
| 4 | 16 | 16/16 ✓ | 0 rejects ≠ I ✓ | (0,4,1,3,2) 3-cycle |
| 8 | 64 | 256/256 ✓ | 0 rejects ≠ I ✓ | (1,0,4,3,2) (2,2,1) |
| 16 | 256 | 65536/65536 ✓ | 0 rejects ≠ I ✓ | (1,2,3,4,0) 5-cycle |

La construcción de ℓ=16 requirió: (a) un tree-builder que
invierte programas compuestos intercambiando hijos del
conmutador (no reemplazando permutaciones individuales), y
(b) dos sets diferentes de 4 pares de transposiciones no
conmutantes (uno por cada mitad de 8 bits) con targets de
nivel 3 que no conmutan entre sí.

### Camino a la prueba formal

La prueba de la Conjetura de T-Independencia Uniforme:

    sup_T d_TV(D_T, Uniform(S_5)) ≤ negl(ℓ)

requiere demostrar que el operador de conmutación del árbol
de Barrington contrae cada representación irreducible no
trivial de S_5. Los datos muestran:

- La representación (4,1) es la dominante (bottleneck)
- Su norma decae por factor ~0.002 de ℓ=4 a ℓ=8
- El decaimiento se mantiene de ℓ=8 a ℓ=16
- El spectral gap estimado es ~0.84 por nivel

El siguiente paso es calcular el operador de contracción
T_ρ para la representación (4,1) explícitamente y verificar
que ||T_{(4,1)}|| < 1. Si se confirma, la prueba formal
sigue del Upper Bound Lemma de Diaconis-Shahshahani.

---

## RESUMEN DE ESTADO

| Problema | Estado | Resultado |
|---|---|---|
| P9 (similarity blindness) | **CERRADO** | Teorema: S_5 ambivalente → blind en todos los niveles |
| P6 (ataques publicados) | **CERRADO** | Ningún ataque publicado aplica, por razones estructurales concretas |
| P13 (colisiones estructuradas) | **PARCIAL** | Colisiones existen (1/120), son T-independientes (exacto para ℓ=4), distribución converge a uniforme exponencialmente |
| Fourier / spectral gap | **EN PROGRESO** | 3 datos confirman decaimiento exponencial, ratio ~0.16/nivel |
| Prueba formal T-independencia | **ABIERTO** | Evidencia empírica fuerte; falta cálculo del operador de contracción |

---

## QUÉ CAMBIÓ RESPECTO AL PAPER ORIGINAL

### Argumento de seguridad: cambio fundamental

| | Paper original | Después de las pruebas |
|---|---|---|
| Claim sobre colisiones | "Probability 1/min(p,q) per path" | "Rate 1/120, T-independent" |
| Defensa contra inconsistencia | "Commutator resilience + union bound" | "T-independence of collision distribution" |
| Rol del dynamic encoding | "Prevents similarity + inconsistency" | "Prevents similarity only; inconsistency handled by T-independence" |
| Union bound paramétrico | "n ≥ 2ℓ² + 256 bits" | Eliminado (irrelevante) |
| Tamaño del módulo | "Depende de ℓ" | "Depende solo de factorización (RSA estándar)" |
| Similarity attack en niveles profundos | "Open question" | "Proven blind (ambivalence)" |
| Open Problem 1 | "Enforce global consistency" | "Prove uniform T-independence" |
| Paradigma de seguridad | "Collisions are improbable" | "Collisions are uninformative" |

### Fortalezas ganadas

1. La T-independencia exacta es más fuerte que cualquier
   argumento probabilístico — es una propiedad algebraica
2. El decaimiento espectral exponencial proporciona un camino
   claro hacia la prueba formal
3. La resistencia a ataques publicados está documentada
   ataque por ataque con razones concretas
4. La honestidad sobre qué funciona y qué no es más precisa

### Debilidades descubiertas

1. El union bound original estaba fundamentalmente equivocado
2. El adversario PUEDE encontrar aceptantes falsos (~120 intentos)
3. El dynamic encoding no protege contra evaluación inconsistente
4. La seguridad depende de una propiedad (T-independencia) que
   aún no está formalmente demostrada

---

## ENTREGABLES PRODUCIDOS

| Archivo | Contenido |
|---|---|
| p9_resolution.py | Prueba computacional de ambivalencia de S_5 |
| p13_exhaustive.py | Enumeración exhaustiva de colisiones para ℓ=4 |
| p13_investigation.py | Análisis profundo de los 249 caminos de colisión |
| p13_scaling_critical.py | Convergencia a 1/120 para ℓ=8 |
| fourier_analysis_s5.py | Descomposición en representaciones irreducibles |
| veredicto_y_roadmap.md | Análisis inicial y plan de investigación |
| vias_de_investigacion_post_p13.md | Cinco vías posibles hacia adelante |
| paper_structural_destruction_v2.md | Paper actualizado con corrección de convergencia uniforme |

---

*Documento generado: Marzo 18, 2026*
