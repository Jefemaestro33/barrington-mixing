# Veredicto y Roadmap de Investigación
## Análisis del paper "Structural Destruction" y la bitácora de investigación
### Marzo 17, 2026

---

## 1. VEREDICTO DEL PAPER

### 1.1 Evaluación general

Este es un paper serio, bien estructurado y escrito con una honestidad intelectual poco común. El working draft presenta: (a) un marco teórico genuinamente útil para pensar sobre ofuscación y encriptación funcional, y (b) una construcción candidata interesante pero no probada. No hay errores técnicos graves detectados. Las pruebas que se ofrecen son correctas dentro de su alcance.

### 1.2 Fortalezas

**Marco teórico (Sección 2) — la parte más sólida.** La idea de formalizar la seguridad criptográfica a través del *function kernel* ker(F) y la *security entropy* H_sec es elegante y conceptualmente clara. La conexión con el estructuralismo de Benacerraf es más que decorativa: captura genuinamente la intuición de que la seguridad proviene de destruir relaciones estructurales innecesarias, no de inyectar ruido.

Contribuciones concretas del marco:

- El Teorema 1 (límite fundamental): si F separa todos los puntos, H_sec = 0 para cualquier distribución con soporte completo. Resultado limpio y útil.
- El Corolario 2 (optimalidad de funciones punto para ofuscación): las funciones punto maximizan H_sec Y resisten extracción por consultas adaptativas. Otras clases con H_sec alto (como umbrales) son vulnerables a búsqueda binaria.
- La tabla comparativa de clases de funciones (punto, umbral, k-bit, lineal, polinomial, identidad) organiza el panorama de forma clara.
- La observación sobre funciones umbral — alto H_sec pero vulnerables bajo consultas adaptativas — es un insight limpio y bien argumentado que justifica la restricción a funciones punto para ofuscación.

**Criptoanálisis (Secciones 3.4–3.5) — bien ejecutado.**

- La prueba de que el similarity attack no factoriza n es correcta y no trivial de anticipar. Las matrices de permutación tienen entradas en {0,1}, idénticas mod p y mod q, lo que hace que el polinomio característico del quotient sea el mismo en ambos componentes CRT.
- La demostración de "ceguera local" (local blindness) en nodos hoja es un argumento bonito: las transposiciones son involuciones (σ = σ⁻¹), por lo que el quotient es idéntico independientemente del bit secreto.
- La identificación de la debilidad en nodos profundos del árbol de conmutadores y su uso como motivación para la variante endurecida muestra madurez criptográfica.

**Narrativa de auto-ataque.** Presentar la construcción base, atacarla, probar que los ataques parcialmente fallan, y luego presentar la construcción hardened como respuesta es la estructura de los mejores papers de criptografía. Da confianza de que el autor no está siendo ingenuo.

### 1.3 Limitaciones reconocidas (donde el paper tiene razón en ser honesto)

**La barrera de consistencia global — el elefante en la habitación.** Toda la maquinaria de mapas multilineales en la literatura de iO existe para resolver este problema. El paper propone una defensa heurística: las evaluaciones inconsistentes producen permutaciones caóticas que, comprimidas por los bookends, colisionan con el escalar objetivo solo con probabilidad 1/min(p,q). El union bound sobre 2^{ℓ²} caminos es correcto *si* se acepta la hipótesis de que cada camino produce una permutación efectivamente aleatoria e independiente. Esa hipótesis es exactamente lo que no está probado.

**La asunción MBPI es circular en sentido técnico.** Dice "el esquema es seguro si el esquema es indistinguible", sin reducción a un problema estándar. El autor lo declara con total transparencia, pero la contribución constructiva queda como *candidato*, no como resultado.

### 1.4 Debilidades técnicas identificadas

**1. Brecha entre consistencia local y global.** La codificación dinámica resuelve el ataque de similaridad local e introduce dependencia Markoviana entre pasos adyacentes. Pero en el programa de Barrington, la variable leída en el paso j puede ser la misma que en el paso j-50, y la consistencia solo se aplica entre pasos contiguos. La brecha entre consistencia local y global sigue abierta, y la codificación dinámica no la cierra — solo dificulta un tipo particular de ataque.

**2. Parámetros impracticables para inputs grandes.** Para ℓ = 64 bits de entrada: módulo n de ~8,448 bits y programas de ~840 MB (variante endurecida). El "sweet spot" declarado de ℓ ≤ 48 es honesto pero limita severamente la utilidad.

**3. Ataques basados en evaluación insuficientemente analizados.** El adversario puede generar múltiples evaluaciones del mismo programa, creando potencialmente un sistema de ecuaciones sobre Z_n. El paper menciona esto tangencialmente pero no lo analiza a fondo.

### 1.5 Juicio de publicabilidad

Como contribución teórica/exploratoria, tiene mérito para ePrint y un buen workshop. El marco de la Sección 2 podría tener vida propia independientemente de si la construcción sobrevive al criptoanálisis comunitario. Sin embargo, no está en condiciones de ser un paper de conferencia top (CRYPTO/EUROCRYPT/FOCS) sin resolver o avanzar significativamente en la barrera de consistencia global.

---

## 2. LO QUE REVELA LA BITÁCORA

### 2.1 Magnitud del recorrido

La bitácora revela algo que el paper por sí solo no muestra con total claridad: la magnitud del proceso para llegar a la construcción final.

- 9 vías muertas documentadas
- 18 preguntas cerradas, 14 con respuesta "NO" (78%)
- Evolución conceptual desde "FHE con cambio de variable" (ambiciosa pero ingenua) hasta "ofuscación de funciones punto sobre Z_n con análisis honesto de la barrera de consistencia" (acotada pero sólida)

### 2.2 Muertes que enseñaron

Cada vía muerta produjo un insight concreto:

| Vía muerta | Insight ganado |
|---|---|
| Paillier estándar | La estructura lineal de (1+n)^m solo permite extraer m completo, no funciones parciales |
| CRT con Φ polinomial | Los coeficientes CRT gritan la factorización (ataque GCD) |
| Aniquilador c^M - 1 | El grado del polinomio filtra el orden del subgrupo |
| Línea escalar g^{ax+r} | La conmutatividad de Z_n* es insuficiente para distinguir caminos → se necesita no conmutatividad |
| Rescate Paillier con g^{x²} | La información para evaluar ES la información para factorizar |
| Ortogonalidad CRT | CRT puro no resuelve si Φ es públicamente inspeccionable |

El patrón de muerte es consistente: en Z_n con n=pq, cualquier operación que distinga los componentes mod p y mod q filtra la factorización si el evaluador puede inspeccionar la estructura de Φ. Esto no es un dato de libro — es un descubrimiento empírico por eliminación.

### 2.3 El insight de la no conmutatividad

La muerte de la línea escalar (Sección 7.8 de la bitácora) es particularmente reveladora. El autor intentó la construcción más simple posible y descubrió que en un grupo conmutativo, "x = s" y "x ≠ s" son algebraicamente indistinguibles. La conclusión — "necesitamos no conmutatividad, esto apunta a S_5 y Barrington" — muestra pensamiento criptográfico genuino. La dirección final no fue elegida por preferencia sino por eliminación.

### 2.4 Evolución orgánica de la codificación dinámica

La codificación dinámica no fue diseñada desde el principio como defensa contra la inconsistencia global. Nació como respuesta al similarity attack en nodos profundos. Una vez construida, el autor descubrió que también prevenía mix-and-match local — y ahí descubrió que lo que *no* prevenía era el mix-and-match global. El descubrimiento de la barrera fue consecuencia de intentar resolverla parcialmente y ver dónde se detenía la protección.

### 2.5 Evaluación de integridad

El 78% de preguntas cerradas con "NO" es la firma de alguien que investigó en lugar de racionalizar una idea preconcebida. La decisión explícita en la Sección 6.13 de la bitácora — "NO intentar resolverlo, declararlo como barrera" — es madurez investigativa.

---

## 3. ROADMAP: QUÉ SIGUE

### 3.1 Jerarquía de impacto (de mayor a menor)

---

#### TIER 1 — Cambiaría el campo

**P12: Binding global sobre Z_n sin mapas multilineales.**

Si el autor encuentra un mecanismo criptográfico que fuerce consistencia de variables a través de lecturas distantes en un branching program usando solo aritmética modular sobre compuestos, eso no es un paper — es un resultado que redefine lo que se creía posible en ofuscación.

*Por qué sería tan importante:* Toda la maquinaria de mapas multilineales (GGH13, CLT13, GGH15) y después la migración a LWE (Jain-Lin-Sahai 2021) existe porque nadie encontró cómo hacer esto. Un mecanismo limpio sobre Z_n abriría una tercera vía hacia iO que no pasa ni por mapas multilineales ni por LWE. Las implicaciones irían más allá de funciones punto: afectaría ofuscación general, FE general, y potencialmente la construcción de iO desde asunciones de factorización.

*Probabilidad realista:* Muy baja. Pero no es cero. El autor tiene una ventaja que otros no tuvieron: solo necesita el caso restringido de funciones punto con topología de conmutadores, no el caso general. Es posible que exista un truco específico para esta estructura que no generalice pero que funcione aquí.

*Clasificación:* Santo grial. Programa de investigación a largo plazo, no el siguiente paso.

---

#### TIER 2 — Paper fuerte en conferencia top (CRYPTO/EUROCRYPT)

**P13: Demostrar formalmente que caminos inconsistentes producen permutaciones con distribución cercana a la uniforme sobre S_5.**

Esto convertiría el argumento heurístico del union bound en teorema. Específicamente, se necesita demostrar que para la topología del árbol de conmutadores de Barrington aplicada a funciones punto, las permutaciones producidas por evaluaciones inconsistentes tienen distancia estadística negligible de la distribución uniforme sobre S_5.

*Impacto:* La asunción MBPI sería reducible a factorización más esta propiedad combinatoria demostrada. No resuelve la barrera de consistencia global en general, pero la resuelve para funciones punto bajo un argumento riguroso. Resultado: la primera construcción de ofuscación de funciones punto sin LWE ni mapas multilineales, con seguridad demostrada bajo factorización + propiedad combinatoria verificada.

*Probabilidad:* Moderada. Es un problema de combinatoria sobre un grupo finito (S_5, 120 elementos) con una estructura arbórea específica. Atacable con herramientas de teoría de grupos computacional y análisis de caminatas aleatorias sobre grupos de permutaciones.

*Herramientas sugeridas:* Teoría de representaciones de S_5 (para analizar distribuciones sobre el grupo), cotas de mixing time para caminatas en grupos de permutaciones, análisis espectral de la cadena de Markov inducida por la estructura de conmutadores.

*Clasificación:* Equilibrio óptimo entre impacto y factibilidad. Este es el resultado que convertiría el paper de "candidato interesante con barrera abierta" a "resultado criptográfico serio con prueba".

---

#### TIER 3 — Publicación sólida, cierra el paper limpiamente

**P6 + P9: Análisis de ataques ADP + verificación de ciclos en niveles profundos.**

*P9 (estructura de ciclos):* S_5 tiene 120 elementos. Los conmutadores que aparecen en el árbol de Barrington para funciones punto con ℓ = 4, 8, 16 son enumerables. El autor puede calcular explícitamente, para cada conmutador c que aparece como target en un nodo interno, si c y c⁻¹ tienen la misma estructura de ciclos.

- Si la respuesta es SÍ para todos los niveles: la construcción base ya es segura contra el similarity attack sin necesidad del dynamic encoding (simplificación mayor del esquema).
- Si la respuesta es NO: confirma que el dynamic encoding es estrictamente necesario y cierra la pregunta abierta.
- Esfuerzo estimado: una tarde con un script en Python.

*P6 (ataques ADP):* Los ADPs de Bartusek et al. son lo más parecido a la construcción del autor y fueron rotos. Se necesita un análisis formal de por qué los ataques no aplican aquí. La intuición ya existe: los ADPs buscan ofuscar circuitos generales, esta construcción solo ofusca funciones punto, y los ataques explotan la equivalencia funcional entre programas (que no existe en el setting de programa único). Falta escribirlo como argumento riguroso.

*Impacto combinado:* Cierra todas las preguntas abiertas excepto la barrera de consistencia global. El resultado sería: "construcción candidata que resiste todos los ataques conocidos, con barrera identificada y argumento heurístico paramétrico para por qué probablemente no es explotable". Publicable en buen workshop de criptografía o Journal of Cryptology como contribución exploratoria.

*Probabilidad:* Alta. P9 es verificación computacional directa. P6 requiere análisis cuidadoso pero los ataques están documentados.

---

#### TIER 4 — Mejora práctica, amplía audiencia

**P10: Representación compacta con PRG.**

De 210 MB a kilobytes. Derivar las matrices S_j de un PRG con semilla corta en lugar de almacenarlas explícitamente. El evaluador recibe la semilla y regenera las S_j durante la evaluación.

*Impacto:* No cambia la teoría pero hace que alguien pueda implementar la construcción y experimentar. Invita a más gente a hacer criptoanálisis, que es exactamente lo que se necesita.

*Consideración de seguridad:* Las matrices S_j derivadas de PRG ya no son independientes — están determinadas por la semilla. Esto no afecta la seguridad si el PRG es seguro (las matrices siguen siendo pseudoaleatorias), pero el argumento formal necesita explicitarse.

*Probabilidad:* Alta. Es ingeniería criptográfica estándar.

---

### 3.2 Secuencia óptima recomendada

```
Fase 1 (inmediata, ~1 día):
  └─ P9: Script de verificación de ciclos en S_5
     → Cierra pregunta abierta sobre similarity attack en niveles profundos

Fase 2 (corto plazo, ~2 semanas):
  └─ P6: Análisis formal de ataques ADP vs. funciones punto
     → Demuestra que ataques conocidos no aplican al caso restringido

Fase 3 (medio plazo, ~1-3 meses):
  └─ P13: Análisis combinatorio de distribución de permutaciones
     en árboles de conmutadores
     → Convierte argumento heurístico en teorema (o descubre contraejemplo)

Fase 4 (paralelo con Fase 3, ~2-4 semanas):
  └─ P10: Representación compacta con PRG
     → Mejora práctica, invita implementación y criptoanálisis

Fase 5 (paralelo con todo, inmediata):
  └─ Someter paper actual a ePrint
     → Obtener criptoanálisis comunitario — lo que el autor pide en §3.7.3

Fase ∞ (programa de investigación a largo plazo):
  └─ P12: Binding global sobre Z_n
     → Santo grial, no condicionar nada a esto
```

### 3.3 Lo que NO debería hacer ahora

**No extender a funciones más allá de point functions (P3).** La fuerza del paper está en la restricción. Es lo que hace que los ataques de aniquilación no apliquen, que el argumento de conmutadores funcione, y que la evasividad dé seguridad distributional. Ampliar la clase de funciones antes de resolver la consistencia global para el caso simple sería construir sobre arena.

**No intentar el salto a FE general ni a iO (P4).** Es un programa de investigación de años, no el siguiente paso.

**No agregar más contenido al paper.** Ya tiene masa crítica para ePrint. Lo que falta no es más texto sino validación externa y resolución de las preguntas que el autor mismo identificó.

---

## 4. CONTEXTO: POR QUÉ IMPORTA ESTE TRABAJO

### 4.1 El campo de ofuscación sin LWE/mapas multilineales

La barrera de consistencia global en branching programs sobre módulos compuestos es el obstáculo que bloqueó la ofuscación por indistinguibilidad durante años. El campo entero migró a construcciones basadas en LWE — Jain-Lin-Sahai (2021) demostró iO desde asunciones estándar usando una ruta completamente diferente (functional encryption bootstrapping), precisamente porque la ruta directa vía branching programs sobre módulos compuestos no se pudo asegurar.

Nadie ha logrado ofuscación segura probada sin LWE ni mapas multilineales:

- Gentry-Jutla-Keane (algebraico puro): atacado vía rank attack
- ADPs (Bartusek et al.): atacados, debilidades en randomización
- Ye-Liu (dynamic fencing): preprint 10 años, nunca validado
- Agrawal (NLinFE desde NTRU): atacado

### 4.2 Lo que este trabajo aporta

El paper no resuelve el problema, pero llega más lejos que la mayoría de intentos previos en el caso restringido de funciones punto:

- Identifica la barrera con precisión quirúrgica
- Construye hasta la barrera con una construcción limpia y analizada
- Proporciona argumento heurístico paramétrico con cotas explícitas
- Presenta todo con honestidad completa sobre lo que funciona y lo que no

### 4.3 Valor independiente del marco teórico

El marco de la Sección 2 (ker(F), H_sec, destrucción estructural, dualidad FE/ofuscación, clasificación de clases de funciones) tiene valor independiente de si la construcción sobrevive. Es una forma de organizar el panorama de privacidad computacional que no existía antes y que podría influir en cómo se piensan futuros esquemas.

---

*Documento generado: 17 de marzo de 2026*
