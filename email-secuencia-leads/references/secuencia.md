# Secuencia: tipos de email, qué comunica cada uno y cómo se encadenan

Los números (cuántos emails, qué días, longitudes) están en `parametros.md`. Aquí se explica **para qué sirve cada email** y cómo se decide su contenido para que aporte valor de verdad.

## 1. La idea que manda [Investigación]

El lead ya levantó la mano: pidió que le contactaran. No hay que convencerle de que existe el problema, sino de que **esta empresa es la que mejor lo va a resolver** y de que dar el siguiente paso no tiene riesgo. Eso se consigue enseñando, no repitiendo la oferta.

Cada email deposita confianza o la gasta (Chaperon). Un email que solo empuja a comprar la gasta. Un email que resuelve una duda real la deposita. La secuencia deposita durante varios emails y solo después pide.

Cadena lógica de la secuencia completa:
1. **Recibido y siguiente paso claro** (E0): baja la ansiedad y confirma que ha elegido bien.
2. **Quién te escribe y qué vas a recibir** (bienvenida).
3. **Enseñar el qué y el porqué** (lección, errores, precio): el lead entiende su problema mejor que antes. El «cómo hacerlo bien» queda para el servicio.
4. **Demostrar** (caso, cifras reales, cita): alguien como él lo consiguió con esta empresa.
5. **Quitar el riesgo** (objeciones, proceso): plazos, garantías, qué pasa si algo sale mal.
6. **Invitar** (invitación): el siguiente paso es la conclusión natural, no un salto.
7. **Cerrar con elegancia** (breakup): corto, humano, deja la puerta abierta.

## 2. El test de valor (obligatorio en la Parada 1)

Los ángulos salen de la investigación del Paso 2 (`investigacion/publico.md`), no de la landing. La tabla del plan lleva estas cinco columnas. Son el detector de relleno y de venta:
- **Emails de valor** (`bienvenida`, `leccion`, `errores`, `precio`, `comparativa`, `caso`, `objeciones`, `proceso`): las cinco columnas, obligatorias.
- **`recepcion` e `invitacion`**: solo la de duda u objeción; el resto lleva «—».
- **`breakup` y mini-secuencia de cita**: todas «—».

| Columna | Qué se escribe | Si queda vacía |
|---|---|---|
| **Situación del lead (Hn)** | Un momento, dolor, interés o algo que necesita saber, con el id del hallazgo | No hay email: se busca otra situación o se quita el email |
| **Duda u objeción que derriba (Dn → Hn)** | La duda u objeción frecuente, con las palabras del lead, y el hallazgo que la responde | **No se aprueba**: ver §2.1 |
| **Qué sabe después (Hn)** | Una frase: qué entiende tras leerlo, con el hallazgo de AUTORIDAD o CLIENTE que lo respalda | **Relleno**: se reescribe el ángulo |
| **Acción para hoy (Hn)** | Algo concreto que puede hacer después de leer aunque nunca contrate | **No es de valor**: se cambia de ángulo o se quita |
| **Qué queda para el servicio** | Qué parte del «cómo» solo puede darle la empresa | **Venta**: el email intenta cerrar en lugar de enseñar; se reescribe |

### 2.1 Dudas y objeciones: obligatorio

Educar no basta: el lead no contrata mientras le quede una duda o un freno sin resolver. Brodie lo plantea así: repartir la venta en la secuencia, **un beneficio u objeción por email** (p. 83).

- **Todos los emails** derriban al menos una duda u objeción de la tabla «Dudas y objeciones» de `investigacion/publico.md`, con una respuesta con fuente. Sobre el servicio del cliente (precio, plazos, garantías, proceso, confidencialidad), la fuente es solo CLIENTE; sobre el problema, CLIENTE o AUTORIDAD. Solo quedan fuera el `breakup` y la mini-secuencia de cita (`cita-confirmacion`, `cita-recordatorio`, `no-show`, `no-show-2`).
- **E0**: se elige la duda de la tabla que más pesa justo después de enviar el formulario. Por ejemplo: qué pasa ahora, si me van a presionar, si la llamada cuesta, si es confidencial.
- **Una principal por email**. Puede tocar una segunda de pasada, en una frase o en la P. D. Excepción: en el tipo D, la invitación puede responder varias de pasada.
- **Ninguna es la principal en dos emails.**
- **Cobertura**: las **5 más frecuentes** (o todas, si son menos) quedan respondidas antes de la `invitacion`, como principal o de pasada. Si la secuencia es corta (tipo D) y no caben, la invitación responde las que quedan.
- La **invitación** tiene como principal la última duda u objeción que frena a pedir la llamada. Repasa en 1-2 líneas las ya resueltas.
- **Sin respuesta con fuente**: la duda se pregunta al cliente en la Parada 1 (`[FALTA: respuesta del cliente]`). El email que la tiene como principal queda pendiente hasta tener la respuesta; los demás siguen.
- Cómo se escribe en el email: `copy-email.md` §4b.

Test rápido: si el email podría estar en la landing del cliente tal cual, no es de valor. Si solo describe el servicio, el equipo o el proceso de compra, es venta.

El **Big 5 de Marcus Sheridan** [Investigación] sirve para comprobar que la secuencia cubre lo que el lead necesita para decidir: coste (de qué depende) · problemas y limitaciones (para quién NO es) · comparativas (opciones reales) · reseñas (prueba real) · «los mejores» (cómo elegir bien). Cada casilla que ni el brief ni la investigación respalden se marca `[FALTA]` y no genera email.

## 3. Catálogo de tipos

`tipo` es el valor que lleva la ficha. La **maqueta obligatoria de cada tipo** y el resto de bloques permitidos están en `parametros.md` §4; las composiciones completas, en `diseno.md` §3. Cada tipo se ve distinto de los demás y ningún email repite el esqueleto de otro: lo comprueba `build_email.py`.

| `tipo` | Función | Qué comunica | Bloques obligatorios | Opcionales habituales | CTA |
|---|---|---|---|---|---|
| `recepcion` (E0) | Confirmar y ordenar el siguiente paso [Investigación] | Hemos recibido tu solicitud · qué pasa ahora, quién te contacta, cuándo y por qué canal · un paso opcional de baja fricción · quién firma. **Sin venta, sin presupuesto, sin varios CTA** | `carta`, `pasos` | `resumen` (sus datos, si no hay razón de discreción), `boton` (solo si hay agenda) | Agendar ya / responder |
| `bienvenida` | Autoridad y expectativas | Quién está detrás y por qué se dedica a esto · qué va a recibir estos días (anticipa los temas) · un primer consejo útil · **para quién no es** el servicio, en una línea honesta | `carta`, `pasos` o `seccion` | `titular`, `imagen` (equipo o taller reales), `cita` | Suave: responder con su situación |
| `leccion` | Resolver la duda nº 1 del avatar | Una sola idea útil, con ejemplo concreto y un paso aplicable hoy | `titular`, `carta`, y `seccion`, `destacado` o `pasos` | `imagen`, `puntos` de la carta | Suave: leer o responder |
| `errores` | Aversión a la pérdida | 3 errores que cuestan dinero, tiempo o tranquilidad al contratar este servicio, y cómo evitarlos | `titular`, `carta`, y `pasos` o `seccion` (un error por bloque) | `destacado` | Suave |
| `precio` | Transparencia (Big 5: coste) | De qué depende el precio, qué lo encarece y qué lo abarata; rangos o cifras solo si el brief los da; **coste de esperar** solo con datos reales | `titular`, `carta`, y `tabla`, `cifras` o `faq` | `destacado` | Medio: pedir valoración |
| `comparativa` | Ayudar a decidir | Opciones reales (hacerlo uno mismo, opción barata, esta empresa) con pros y contras honestos; para quién NO es | `titular`, `carta`, y `tabla` (una columna por opción) o `caso` | `destacado` | Medio |
| `caso` | Prueba con historia | Un caso real con arco: situación de partida → punto de quiebre → qué cambió → resultado [Investigación: Soap Opera / antes-después-puente]. Solo con caso o testimonio real | `carta`, `caso` o `cita` | `imagen`, `cifras` | Suave («¿Te pasa algo parecido? Respóndeme») o medio (enlace a cómo trabajan) |
| `objeciones` | Quitar frenos | 3-4 dudas reales (plazos, garantías, qué pasa si…) con respuesta directa | `carta`, `faq` | `cita` | Responder con su duda |
| `proceso` | Quitar la ansiedad del «¿y ahora qué?» | Paso a paso real de lo que pasa desde el primer contacto hasta el final; **checklist** de lo que conviene tener antes | `carta`, `pasos` | `destacado` | Medio |
| `invitacion` | Pedir el siguiente paso | Resumen en 2-3 líneas de lo que ya sabe · qué es exactamente la cita/llamada/visita, cuánto dura, qué se lleva · cómo reservar | `titular`, `carta`, y `cierre` (recomendado) o `boton` | `pasos`, `cita` | **Fuerte** |
| `breakup` | Cierre humano | **2-4 frases**: «¿lo dejamos aquí o seguimos?», sin culpa ni presión | `carta` | — | Responder |
| `cita-confirmacion` · `cita-recordatorio` · `no-show` · `no-show-2` | Mini-secuencia de cita | `parametros.md` §2 | `carta` | `pasos`, `boton` (no en `no-show-2`) | Según momento |

Tipos de CTA, definidos en `parametros.md` §3:
- **suave**: pregunta para responder, o enlace a algo para leer;
- **medio**: enlace en texto al siguiente paso con el cliente;
- **fuerte**: botón.

## 4. Plantillas de secuencia por tipo de oferta [Investigación]

Punto de partida. Se adapta en la Parada 1 según lo que tenga el brief: si un tipo no se puede respaldar (p. ej. no hay caso real), se sustituye por `proceso`, `comparativa` u `objeciones` y se dice.

**A · B2C alta consideración (8 emails, 21 días)**
D0 `recepcion` · D1 `bienvenida` · D3 `leccion` · D5 `errores` · D8 `caso` · D12 `precio` · D16 `invitacion` · D21 `breakup`

**B · B2B alto ticket (9 emails, 32 días)**
D0 `recepcion` · D1 `bienvenida` · D3 `leccion` · D5 `errores` · D8 `caso` · D12 `comparativa` · D18 `precio` · D25 `invitacion` · D32 `breakup`

**C · Inmobiliaria (8 emails, 30 días)**
D0 `recepcion` · D1 `bienvenida` (la zona y la promoción) · D3 `leccion` (gastos reales de compra, financiación) · D7 `proceso` (cómo es una visita y una reserva) · D12 `caso` · D18 `objeciones` · D25 `invitacion` · D30 `breakup`

**D · Decisión rápida (5 emails, 7 días)**
D0 `recepcion` · D1 `leccion` · D2 `caso` · D4 `invitacion` · D7 `breakup`

## 5. De dónde sale el contenido de valor (jerarquía de fuentes)

1. **Datos del cliente** (precios, plazos, garantías, casos, cifras, nombres, URLs): **solo** del brief, la landing, las respuestas del formulario y los materiales que pase el usuario. Nunca de la memoria ni de «lo que suele pasar en el sector».
2. **Conocimiento sobre el público** (dolores, momentos difíciles, preguntas, acciones útiles, mitos, cómo elegir): la investigación de NotebookLM del Paso 2 (`investigacion/publico.md`), con el id del hallazgo. Consejos, acciones y cifras solo de fuentes AUTORIDAD o CLIENTE; las fuentes PUBLICO solo para saber qué siente y cómo lo dice. Si choca con el cliente, manda el cliente.
3. **Práctica de email** (cadencia, estructura, copy): `parametros.md`, con la etiqueta de cada parámetro.
4. **Ley y conocimiento general** (RGPD, LSSI, datos de salud, normativa del sector, teléfonos de emergencia): permitido y necesario, pero se etiqueta `[General]` en el plan y en `fuentes.md`, y el usuario lo confirma en la Parada 1.

Nunca se usa conocimiento propio del modelo para dar un consejo, un dato o una acción en un email.

**Cómo encontrar el ángulo** (`copy-email.md` §4): situación del lead de la investigación → conocimiento que la ilumina → acción para hoy → duda u objeción que derriba. Las objeciones del brief, la FAQ de la landing y las preguntas del formulario se suman a las de la investigación y sirven para priorizar.

## 6. Encadenado [Investigación: Chaperon]

- La bienvenida y cada email de valor dicen, en la P. D. o en la última frase, **qué cuenta el siguiente email, con su dato concreto** («El jueves te cuento el error que encarece un baño un 20 %»). Solo si el siguiente email existe y trata eso. Se nombra el tema con palabras claras, sin dejarlo en el aire para crear intriga (`copy-email.md` §0.6).
- La bienvenida anticipa el recorrido (3-4 temas en una frase o en `puntos`).
- La invitación resume lo aprendido en 2-3 líneas antes de pedir.
- Ningún email repite el ángulo de otro de la misma secuencia.
