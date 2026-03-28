# Vías de Investigación Post-P13
## Estado actual y caminos posibles
### Marzo 18, 2026

---

## 0. DÓNDE ESTAMOS

### Resultados obtenidos en esta sesión

**P9 — CERRADA (teorema).** La ambivalencia de S\_5 garantiza que el similarity attack es ciego en todos los niveles del árbol de Barrington, para todo ℓ, toda elección de permutaciones base, y todo target T. La "open question" de la Sección 3.4.3 del paper queda resuelta negativamente: no hay filtración en ningún nivel.

**P6 — CERRADA (análisis de literatura).** Ninguna familia de ataques publicada aplica a la construcción:

| Familia de ataque | Razón de inaplicabilidad |
|---|---|
| Aniquilación (MSZ16) | Requiere GGH13 + juego iO con dos programas |
| Kernel ADP (Bartusek+) | Requiere múltiples inputs aceptantes (punto tiene 1) |
| Rango (Chen+ TCC19) | Falla contra funciones evasivas (los autores lo reconocen) |
| NLinFE (Agrawal-PM) | Explota estructura NTRU inexistente aquí |
| Zeroizing (CLT13/GGH15) | Requiere parámetros de zero-testing inexistentes |
| Similaridad | Neutralizado por ambivalencia de S\_5 (P9) |

**P13 — PARCIALMENTE RESUELTA (descubrimiento).** Los caminos inconsistentes SÍ producen π\_accept (~1/120 de las veces para ℓ≥8). Pero la tasa es independiente de T. El argumento de seguridad cambia fundamentalmente: de "las colisiones son improbables" a "las colisiones son no-informativas".

### Lo que cambió

El paper ya no puede sostener su argumento original de seguridad (union bound con probabilidad 1/min(p,q) por camino). Pero tiene un argumento *mejor*: T-independencia de la distribución de colisiones. Esto es un paradigma de seguridad nuevo que no aparece en la literatura de ofuscación existente.

### Lo que el paper es ahora

Un marco teórico genuinamente útil (destrucción estructural, ker(F), H\_sec) + una construcción candidata sin LWE ni mapas multilineales + un argumento de seguridad novedoso basado en T-independencia + evidencia empírica fuerte + la pregunta matemática precisa que falta resolver.

---

## VÍA 1: PUBLICAR LO QUE HAY

### Qué implica

Reescribir las secciones afectadas del paper con los resultados de esta sesión y subir a ePrint.

### Cambios concretos al paper

**Sección 3.4.3:** Reemplazar la "open question" sobre cycle structure en niveles profundos con la Proposición de All-Level Blindness (ambivalencia de S\_5). Incluir referencia al script de verificación.

**Sección 3.5.7:** Reescritura completa. Eliminar el union bound incorrecto y la tabla paramétrica. Reemplazar con:
- Datos empíricos: 249/65520 para ℓ=4, ~1/120 para ℓ=8
- Observación de T-independencia (249 exactas para las 16 targets de ℓ=4)
- Argumento de que las colisiones son no-informativas, no improbables
- Convergencia a distribución uniforme sobre S\_5

**Sección 3.7:** Reformular los argumentos estructurales para MBPI:
- Reemplazar "commutator resilience against inconsistent evaluation" con "T-independence of collision distribution"
- Mantener los otros 4 argumentos (factoring barrier, single-program, bookend compression, similarity immunity)

**Sección 3.8:** Reformular el Open Problem 1 como: "Probar que D\_T converge a uniforme sobre S\_5 con velocidad independiente de T"

### Impacto esperado

Moderado. Primer candidato de ofuscación de funciones punto desde factorización sin LWE. Paradigma de seguridad novedoso (T-independencia). Publicable en workshop de criptografía o ePrint con invitación a criptoanálisis.

### Tiempo: semanas
### Riesgo: bajo

---

## VÍA 2: PROBAR T-INDEPENDENCIA FORMALMENTE

### La pregunta matemática precisa

Sea BP el branching program de Barrington para CC\_T sobre {0,1}^ℓ con target π\_accept ∈ S\_5. Sea D\_T la distribución sobre S\_5 inducida por evaluar BP en un string uniformemente aleatorio de L = ℓ² bits (ignorando consistencia de variables).

**Demostrar:** d\_TV(D\_T, U\_{S\_5}) → 0 cuando ℓ → ∞, con velocidad independiente de T, donde U\_{S\_5} es la distribución uniforme sobre S\_5.

### Herramientas disponibles

**Teoría de representaciones de S\_5.** S\_5 tiene exactamente 7 representaciones irreducibles, de dimensiones 1, 1, 4, 4, 5, 5, 6. La distancia a uniforme se puede expresar como:

d\_TV(D\_T, U) ≤ (1/2) · √(Σ\_ρ d\_ρ · ||E[ρ(X)]||²\_F)

donde la suma es sobre representaciones no triviales ρ, d\_ρ es la dimensión, y X es la permutación aleatoria bajo D\_T. Si cada término decae exponencialmente con la profundidad del árbol, la convergencia es exponencial.

**Mixing en grupos finitos.** El árbol de conmutadores induce una secuencia de multiplicaciones en S\_5 donde en cada paso se multiplica por un elemento aleatorio (dependiendo del bit elegido). Esto es una caminata aleatoria no estándar (las multiplicaciones no son i.i.d. — la estructura del árbol determina qué elemento se usa en cada paso). Pero la composición de conmutadores actúa como un operador de mixing: si las representaciones no triviales se contraen en cada nivel del árbol, la convergencia sigue.

**Análisis espectral.** Para cada representación ρ de S\_5, el operador de transición del conmutador en esa representación tiene un valor singular máximo σ\_ρ < 1. Si σ\_ρ < 1 para todas las representaciones no triviales, la distancia a uniforme decae como σ\_max^{depth} donde depth = log₂(ℓ).

### Pasos concretos

1. **Computacional (días).** Descomponer D\_T en las 7 representaciones irreducibles de S\_5 para ℓ=4, 8, 16. Medir la norma de Frobenius de cada componente. Verificar decaimiento exponencial con la profundidad.

2. **Semi-formal (semanas).** Para cada representación ρ, computar el operador de transición del conmutador: dado que un nivel del árbol toma dos permutaciones independientes g, h y produce [g, h] = ghg⁻¹h⁻¹, ¿cuál es la contracción de ρ([g,h]) cuando g y h están distribuidos según las salidas de niveles anteriores?

3. **Formal (meses).** Demostrar que la contracción es estricta (σ\_ρ < 1) para todas las representaciones no triviales, y que no depende de T.

### Impacto esperado

Alto. Un teorema limpio sobre mixing en S\_5 vía conmutadores de Barrington, con aplicación directa a seguridad de ofuscación. Publicable en conferencia seria (posiblemente CRYPTO/EUROCRYPT si la prueba es elegante y las implicaciones se articulan bien).

### Tiempo: meses
### Riesgo: medio — la evidencia empírica es fuerte pero formalizar puede revelar sutilezas (por ejemplo, que la convergencia sea más lenta para ciertos T en ℓ intermedios)

---

## VÍA 3: EXTENDER A CONJUNCIONES Y C&C

### La pregunta

¿La T-independencia se sostiene para funciones más allá de funciones punto?

### Candidatas naturales

**Conjunciones con wildcards:** CC\_T(x) = 1 iff x coincide con T en todas las posiciones donde T no es wildcard (\*). Por ejemplo, T = (1, \*, 0, 1, \*, \*) acepta todo x donde x\_0=1, x\_2=0, x\_3=1. El branching program es similar pero los bloques wildcard son identidades en ambas ramas.

**Funciones C&C generales:** CC[f,y](x) = 1 iff f(x) = y para f en NC¹. El branching program computa f primero y luego compara con y.

**Hamming distance threshold:** CC\_T^d(x) = 1 iff d\_H(x, T) ≤ d. Más complejo — requiere circuito de conteo.

### Método

Computacional primero: construir branching programs para conjunciones con diferentes patrones de wildcards, medir tasas de colisión para diferentes T. Si la tasa es T-independiente (incluyendo independencia del patrón de wildcards), la extensión funciona. Si depende del número de wildcards, entendemos el límite.

### Impacto esperado

Muy alto si funciona. Extender de funciones punto a conjunciones generales ampliaría significativamente el resultado. Extender a C&C general sería un resultado mayor.

### Tiempo: semanas para evidencia empírica, meses para prueba
### Riesgo: alto — no hay garantía de que generalice. La T-independencia para funciones punto depende de la simetría del árbol AND, que se rompe con wildcards.

---

## VÍA 4: BUSCAR CONSTRUCCIÓN CON T-INDEPENDENCIA DEMOSTRABLE

### La idea

El descubrimiento de P13 sugiere que la propiedad clave no es la imposibilidad de colisiones sino la T-independencia. ¿Hay una construcción donde esto sea demostrable por diseño?

### Direcciones posibles

**Caminatas aleatorias explícitas.** En lugar de usar conmutadores de Barrington (cuyo mixing es un teorema pendiente), diseñar un branching program donde cada nivel aplica una multiplicación aleatoria conocida por tener mixing rápido sobre S\_5. El mixing time de caminatas aleatorias sobre S\_n está bien estudiado — para generadores que incluyen una transposición y un ciclo largo, el mixing time es O(n log n). Para S\_5 con n=5, eso es ~8 pasos. Si el programa tiene depth ≥ 8, la convergencia a uniforme sería inmediata por resultados existentes.

**Problema:** cambiar la estructura del branching program podría romper la correctness de la función punto. La elegancia de Barrington es que los conmutadores computan AND exactamente. Una caminata aleatoria arbitraria no computa nada útil.

**Híbrido:** usar Barrington para la correctness pero inyectar pasos adicionales de "mixing" entre los niveles del árbol. Cada paso de mixing multiplica por una permutación aleatoria fija (parte de la clave pública) que no depende del input. Esto no afecta la distinción accept/reject (la permutación de mixing se aplica igualmente en ambos caminos) pero acelera la convergencia a uniforme para caminos inconsistentes.

### Impacto esperado

Potencialmente muy alto — una construcción con prueba directa de T-independencia resolvería P13 completamente sin necesidad de análisis de mixing complejo.

### Tiempo: incierto
### Riesgo: alto — es investigación abierta sin garantías

---

## VÍA 5: LA RUTA NUCLEAR — VOLVER A INTENTAR P12

### Por qué podría tener sentido ahora

P13 reveló que la barrera de consistencia global no es lo que pensábamos. Los caminos inconsistentes no necesitan eliminarse — necesitan ser T-independientes. Pero ¿qué pasaría si encontramos una forma de hacer que los caminos inconsistentes sean *computacionalmente inaccesibles* en lugar de simplemente inofensivos?

Si el autor pudiera modificar la construcción para que evaluar un camino inconsistente requiera factorizar n, los caminos inconsistentes serían tanto inofensivos (por T-independencia) como inaccesibles (por factorización). Belt and suspenders.

### Cómo podría funcionar

La codificación dinámica ya fuerza consistencia local (paso a paso). Lo que falta es binding entre lecturas distantes de la misma variable. Una idea: para cada variable x\_i, publicar un commitment c\_i. En cada paso j que lee x\_i, el evaluador debe proporcionar una apertura del commitment que sea consistente con su elección de bit. Si el commitment está basado en factorización (por ejemplo, c\_i = g^{x\_i} · h^{r\_i} mod n donde g y h generan subgrupos de órdenes secretos relacionados con p y q), verificar la apertura sin conocer la factorización podría ser imposible, pero evaluar con la apertura correcta podría ser eficiente.

### Por qué probablemente no funcione

Esto recrea la necesidad de mapas multilineales o graded encodings por la puerta trasera. El commitment necesita ser verificable (para que el evaluador honesto pueda verificar su propia consistencia) pero no manipulable (para que el evaluador deshonesto no pueda crear aperturas inconsistentes). Eso es esencialmente un mapa bilineal, que es exactamente lo que el paper intenta evitar.

### Impacto esperado

Si funcionara: Tier 1, cambia el campo.

### Tiempo: incierto
### Riesgo: muy alto — este es el problema que una década de investigación no resolvió

---

## RECOMENDACIÓN

```
INMEDIATO (semanas):
├── Vía 1: Reescribir paper y subir a ePrint
│   └── Incorporar P9, P6, P13 con argumento de T-independencia
│
CORTO PLAZO (1-3 meses):
├── Vía 2, paso 1: Descomposición computacional en representaciones de S_5
│   └── Verificar decaimiento exponencial de componentes no triviales
├── Vía 3, paso 1: Tests empíricos de T-independencia para conjunciones
│   └── Construir BPs para conjunciones con wildcards, medir tasas
│
MEDIO PLAZO (3-6 meses):
├── Vía 2, completa: Prueba formal de T-independencia
│   └── Teorema de mixing via representaciones de S_5
│   └── ESTE ES EL RESULTADO QUE HARÍA EL PAPER PUBLICABLE EN TOP VENUE
│
LARGO PLAZO / EXPLORATORIO:
├── Vía 3, prueba: Extender T-independencia a conjunciones
├── Vía 4: Construcción con mixing demostrable
└── Vía 5: P12 (solo si todo lo demás se estanca)
```

### La apuesta óptima

Publicar inmediatamente (Vía 1) para obtener feedback y criptoanálisis comunitario. En paralelo, atacar la descomposición en representaciones de S\_5 (Vía 2, paso computacional). Si los números muestran decaimiento exponencial, invertir en la prueba formal. Ese teorema — que la distribución de permutaciones inducida por el árbol de Barrington converge a uniforme independientemente de T — sería un resultado de combinatoria algebraica con aplicación criptográfica directa. No necesita resolver P12 para ser valioso. Se sostiene solo.

---

*Documento generado: Marzo 18, 2026*
*Basado en análisis de: paper "Structural Destruction" v1, bitácora de investigación v3, scripts P9/P6/P13, y documento "P13 Findings and Corrected Security"*
