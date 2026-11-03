# Paso 2 · Investigación del público

## Para qué sirve

El brief y la landing son documentos de venta: dicen qué ofrece el cliente, no qué necesita saber el lead. Si la secuencia solo se alimenta de ellos, los emails de valor acaban siendo la landing recortada en trozos.

Este paso da a la skill **conocimiento sobre los avatares del cliente**, con fuentes y citas:
- qué sienten y temen;
- **qué les interesa**;
- **qué necesitan saber del servicio** para decidirse;
- **qué dudas y objeciones frecuentes** tienen sobre el servicio, y qué responden las fuentes y el cliente a cada una;
- en qué momentos lo pasan mal, qué pueden hacer por sí mismos hoy y cómo elegir bien.

De ahí salen los ángulos de los emails y **las dudas y objeciones que cada email derriba** (obligatorio, `secuencia.md` §2).

Se hace **siempre**, después del Paso 1 y antes de la Parada 1. No tiene parada propia: el resultado se enseña en la Parada 1.

## Reglas

1. **Dos tipos de fuente, dos usos distintos.**
   - **Voz del público** (foros, reseñas, preguntas públicas, comentarios): solo para saber **qué siente, qué le interesa, qué duda, qué le frena y cómo lo dice**. Nunca para dar un consejo, una cifra ni la respuesta a una objeción.
   - **Autoridad** (organismos oficiales, colegios profesionales, universidades, guías clínicas o técnicas, revistas científicas, medios de referencia, asociaciones de consumidores): lo único que vale para **consejos, datos, acciones y respuestas** que van en un email.
   - **Descarte**: webs de la competencia directa, contenido comercial disfrazado de guía, listas SEO sin autor, cursos, agregadores y textos generados sin fuente.
2. **El cliente manda.** Sus materiales (brief, onboarding, copys, landing, FAQ) son fuentes del grupo CLIENTE. Si un hallazgo choca con su método, su tono o su posicionamiento, gana el cliente y el hallazgo se marca «choca con el cliente». Las respuestas sobre **su** servicio (precio, plazos, garantías, proceso, confidencialidad) solo pueden venir de CLIENTE.
3. **Sectores sensibles** (salud, salud mental, adicciones, estética, legal, finanzas, inmobiliario): cada acción, consejo o respuesta que vaya a un email se marca **«validar con el cliente»** y se incluye en los datos que faltan de la Parada 1.
4. **No se inventa.** Si algo no está en una fuente que puedas citar, no existe. Una duda u objeción sin respuesta con fuente se marca `[FALTA: respuesta del cliente]` y se pregunta en la Parada 1; no se responde con conocimiento propio. Si no hay ninguna herramienta de búsqueda disponible, se dice al usuario y se le pide material del experto del negocio (transcripciones, podcasts, preguntas frecuentes de sus llamadas, reseñas).

## 0. Avatares (antes de buscar)

Con el brief, la landing y los materiales del cliente se definen **1-3 avatares**. Cada uno con su fuente («brief p. 4», «landing»):
- **Buyer persona**: quién es (edad, situación, país, trabajo, con quién vive), qué problema tiene y qué quiere conseguir.
- **Lead prototipo**: cómo llega al formulario (qué le ha pasado justo antes, qué ha buscado, qué espera de la llamada), según las preguntas del formulario y el copy de la landing.
- Si el brief distingue perfiles (p. ej. la persona afectada y un familiar, o dueño y gerente), un avatar por perfil. Si no, uno solo.

Si el brief no da datos para un avatar, no se inventan: se escribe `[FALTA]` y la investigación busca en general.

Se escriben al principio de `investigacion/publico.md` (§5) y sus datos rellenan los huecos `[avatar]` de las consultas y las preguntas.

## 1. Herramienta

Usa la que tengas, por este orden:
- **NotebookLM** (si tienes conectado su MCP): crea un cuaderno «<Negocio> · Público y dolores · secuencia email», sube como fuentes los materiales del negocio con título que empiece por **«CLIENTE ·»** (brief, FAQ, transcripciones, `landing/landing.md`) y lanza las búsquedas de §2 con su investigación en modo profundo, importando solo las fuentes citadas. Las preguntas de §4 se hacen al cuaderno, limitadas a los grupos de fuentes que indica la tabla.
- **Búsqueda web** (WebSearch y WebFetch de Claude Code): haz las búsquedas de §2 (varias por bloque, con distintas palabras), abre las páginas que valgan la pena y guarda en `investigacion/fuentes/` un `.md` por fuente con su URL, su título y los fragmentos útiles copiados literal. Los materiales del negocio cuentan como fuentes CLIENTE. Las preguntas de §4 las respondes tú **solo con lo que hay en esas fuentes**, citando cada afirmación.
- **Ninguna**: regla 4 de «Reglas».

Mientras corre la investigación, no esperes en vacío: avanza con la ficha de la oferta y `marca.json` de la Parada 1.

## 2. Investigaciones

Dos bloques de búsqueda (en NotebookLM, dos investigaciones en modo profundo lanzadas a la vez). Las consultas se escriben **en español**, rellenando los huecos con los datos de los avatares (§0) y del brief.

**A · Voz del público**
> Cómo describen con sus propias palabras las personas que [avatar: edad, situación, país] y que [problema del brief] lo que viven: qué sienten, qué miedos y vergüenzas tienen, qué temas les interesan y qué buscan leer sobre su problema, qué quieren saber de [tipo de servicio] antes de contratarlo, qué dudas y objeciones tienen sobre [tipo de servicio] (precio, si funciona, confidencialidad, tiempo, qué pensarán los demás, si es para ellos), en qué momentos del día o de la semana lo pasan peor, qué han probado antes y por qué no funcionó, qué preguntan en foros, reseñas y buscadores. Priorizar el país del negocio y en español.

**B · Conocimiento con autoridad**
> Recomendaciones y evidencia de fuentes con autoridad ([organismos oficiales del país y del sector], colegios profesionales, universidades, guías [clínicas/técnicas], organismos internacionales de referencia) sobre [problema del brief]: qué puede hacer una persona por sí misma antes de [contratar / empezar un tratamiento], preguntas frecuentes sobre [tipo de servicio] y sus respuestas, errores y mitos frecuentes, cómo tomar la decisión y qué preguntar, señales de calidad y señales de alarma al elegir [proveedor / tratamiento / servicio], qué esperar del proceso, costes o factores de coste, y qué no se debe prometer ni aconsejar sin un profesional.

Opcional **C · Decisión de compra**, solo si el brief deja claro que el lead compara proveedores (B2B, reformas, inmobiliaria, legal):
> Cómo elegir [tipo de proveedor] en [país]: comparativas, qué preguntar antes de firmar, reclamaciones y problemas frecuentes, factores de precio, según asociaciones de consumidores, colegios profesionales y organismos oficiales.

En NotebookLM, cuando terminen, se importan solo las fuentes citadas.

## 3. Clasificar las fuentes

Se clasifica cada fuente por su título y URL en **CLIENTE**, **AUTORIDAD**, **PUBLICO** o **DESCARTE**, y se guarda la lista de cada grupo (ids de NotebookLM o nombres de fichero de `investigacion/fuentes/`) en `investigacion/fuentes-clasificadas.md`.

No hace falta borrar las descartadas: cada pregunta se responde **solo con los grupos que indica la tabla** de §4.

## 4. Preguntas fijas

Se hacen en este orden, en español, con las fuentes limitadas a los grupos que indica la tabla. `[avatar]` se sustituye por la descripción corta de cada avatar; si hay varios, se pide la respuesta separada por avatar. A cada pregunta se le añade al final: «Responde en español. Cita cada afirmación. Si algo no está en las fuentes, dilo. Máximo 900 palabras.»

Cada respuesta se guarda en `investigacion/respuestas/pN.md`.

| # | Pregunta | Fuentes |
|---|---|---|
| P1 | ¿Qué sienten, temen y se reprochan [avatar]? Dame frases literales con las que lo describen y agrúpalas por tema. | PUBLICO + CLIENTE |
| P2 | ¿Qué **intereses** tienen [avatar] sobre su problema y su vida alrededor de él? ¿Qué temas buscan, qué quieren entender, qué leen o preguntan? Ordénalos de más a menos frecuentes, con frases literales. | PUBLICO + CLIENTE |
| P3 | ¿Qué **necesitan saber** [avatar] sobre [el servicio] antes de decidirse (cómo funciona, qué incluye, cuánto dura, qué pasa después, quién lo hace, qué resultados esperar)? Lista concreta, con frases literales. | PUBLICO + CLIENTE |
| P4 | ¿Qué **dudas frecuentes** tienen sobre [el servicio]? Escríbelas como preguntas literales tal como las harían, ordenadas de más a menos frecuentes, y di en cuántas fuentes aparece cada una. | PUBLICO + CLIENTE |
| P5 | ¿Qué **objeciones** les frenan a [pedir ayuda / contratar] (precio, desconfianza, vergüenza, falta de tiempo, «no es para mí», «ya lo intenté», qué dirán los demás…)? Frase literal de cada una, ordenadas de más a menos frecuentes, con en cuántas fuentes aparece. | PUBLICO + CLIENTE |
| P6 | Para cada duda y objeción de esta lista: [pegar la lista de P4 y P5]. ¿Qué **responden** las fuentes con autoridad y los materiales del cliente? Una respuesta concreta por punto, con su fuente. Si un punto no tiene respuesta en las fuentes, di «sin respuesta». | AUTORIDAD + CLIENTE |
| P7 | ¿En qué momentos o situaciones concretas lo pasan peor (cuándo, dónde, con quién, qué lo desencadena)? | PUBLICO + AUTORIDAD + CLIENTE |
| P8 | ¿Qué puede hacer una persona **por sí misma, hoy**, que sea seguro y útil según las fuentes con autoridad? Acciones concretas, paso a paso, con fuente. Señala cualquier contradicción con el método del cliente. | AUTORIDAD + CLIENTE |
| P9 | ¿Qué errores y mitos frecuentes hay, y qué dicen los datos? | AUTORIDAD |
| P10 | ¿Cómo se elige bien [el servicio]? Señales de calidad, señales de alarma y preguntas que conviene hacer al proveedor. | AUTORIDAD + CLIENTE |
| P11 | ¿Qué **no** se puede prometer ni aconsejar sin un profesional en este tema? ¿Cuándo hay que derivar (urgencias, médico, abogado…)? | AUTORIDAD |

## 5. Resultado: `investigacion/publico.md`

En la carpeta de la secuencia. Formato fijo, sin prosa:

```markdown
# Investigación del público · <Cliente> · <fecha>
Fuentes: <cuaderno o carpeta> · <n> fuentes (CLIENTE x · AUTORIDAD y · PUBLICO z)

## Avatares
| Id | Perfil | Quién es | Qué quiere | Cómo llega al formulario | Fuente |
|---|---|---|---|---|---|
| A1 | buyer persona | … | … | … | brief p. 4 |

## Hallazgos
| Id | Avatar | Tipo | Hallazgo (1 frase) | Cita literal (≤ 20 palabras) | Fuente (título · grupo) | Choca con el cliente | Validar con el cliente |
|---|---|---|---|---|---|---|---|
| H1 | A1 | dolor | … | «…» | … · PUBLICO | no | no |
| H2 | A1 | interés | … | «…» | … · PUBLICO | no | no |
| H3 | A1 | acción hoy | … | «…» | … · AUTORIDAD | sí: el método dice… | sí |

Tipos: dolor · interés · necesita saber · momento · acción hoy · mito · señal de calidad · límite · respuesta

## Dudas y objeciones (de P4, P5 y P6)
| Id | Avatar | Duda u objeción, con las palabras del lead | Tipo | Frecuencia (nº fuentes) | Respuesta (Hn) | Estado |
|---|---|---|---|---|---|---|
| D1 | A1 | «¿Se va a enterar mi empresa?» | duda | 5 | H14 (CLIENTE) | con respuesta |
| D2 | A1 | «Es caro para lo que es» | objeción | 3 | — | [FALTA: respuesta del cliente] |

## Límites para el copy (de P11)
- …
```

- Entre 20 y 40 hallazgos. Los de tipo **acción hoy**, **mito**, **señal de calidad** y **respuesta** solo pueden venir de AUTORIDAD o CLIENTE.
- Entre 6 y 15 dudas y objeciones, ordenadas por frecuencia. Cada respuesta es un hallazgo de tipo «respuesta» con su fuente. Las que no tienen respuesta van a los datos que faltan de la Parada 1.
- Una cifra solo entra si la fuente es AUTORIDAD o CLIENTE y la cita la contiene.
- Cada hallazgo se apunta también en `fuentes.md`.

## 6. Cómo pasa al plan

Cada email de valor se construye con **cuatro piezas**. La cuarta, la duda u objeción, va también en el E0 y en la invitación:
1. Una **situación** del lead (hallazgos «momento», «dolor», «interés» o «necesita saber»).
2. Un **conocimiento** que la ilumina (hallazgos de AUTORIDAD o CLIENTE).
3. Una **acción para hoy**: algo concreto que el lead puede hacer después de leer, aunque nunca contrate.
4. **Una duda u objeción que derriba** (Dn) con su respuesta con fuente. **Obligatorio**: ver `secuencia.md` §2.

Si falta la acción para hoy, ese email no es de valor: se cambia de ángulo o se quita. Si falta la duda u objeción, el email no se aprueba. En la Parada 1, la tabla del plan cita los ids (`H3 + H12 · D2`), para que el usuario vea de dónde sale cada idea.
