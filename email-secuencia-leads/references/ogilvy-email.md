# Ogilvy aplicado a la secuencia · compuerta obligatoria del copy

**Todo el copy de estos emails sigue los fundamentos de David Ogilvy (*Ogilvy on Advertising*), sin excepción.** Ningún email se entrega sin pasar esta compuerta.

| Para qué | Dónde |
|---|---|
| Redactar (email) | `copy-email.md` §0 (claridad) y `brodie-email.md` (Ian Brodie, *Email Persuasion*) |
| Auditar (manda ante cualquier contradicción) | Checks O1-O16, abajo |
| Nivel de consciencia del lead | §2 (Eugene Schwartz, *Breakthrough Advertising*) |
| Lo que suena a IA o a folleto | `copy-email.md` §3 y `diseno.md` §1.1 |

## 0. Checks O1-O16

Cada check da **OK**, **n/a** (con motivo) o un fallo: **REESCRIBIR** (se corrige antes de seguir), **MEJORAR** (se corrige si no rompe otra regla) o **RECHAZAR** (fuera, sin discusión).

| # | Check | Falla si… | Si falla |
|---|---|---|---|
| O1 | El asunto (y el H1) promete un beneficio o dice qué se aprende, no describe el servicio | Asunto sin beneficio ni tema | REESCRIBIR |
| O2 | Es específico: un dato, una cifra, un plazo, un proceso con nombre | «Mejora tus resultados», «la mejor opción» | REESCRIBIR |
| O3 | No es un titular «ciego»: se entiende de qué va sin abrirlo (el titular ciego rinde menos) | Hay que adivinar de qué va | REESCRIBIR |
| O4 | Sin juegos de palabras ni dobles sentidos | Ingenio que no dice el mensaje | REESCRIBIR |
| O5 | Segmenta: habla de la situación concreta del lead, no vale para cualquier negocio del sector | Tapas la marca y le sirve a cualquiera | REESCRIBIR |
| O6 | La marca es identificable (remitente, logo o firma) | No se sabe quién escribe | REESCRIBIR |
| O7 | Las citas van entre comillas y son literales | Testimonio sin comillas o retocado | MEJORAR |
| O8 | La imagen, si la hay, cuenta algo (despierta curiosidad o enseña el resultado) | Foto decorativa | REESCRIBIR |
| O9 | Fotografía real de la marca, no ilustración, vector ni stock | Ilustración, vector o stock | REESCRIBIR |
| O10 | Un antes y después enseña el resultado del servicio | Comparación abstracta | REESCRIBIR |
| O11 | Si la imagen es protagonista, el titular va debajo | Titular encima sin motivo | MEJORAR |
| O12 | Toda foto protagonista lleva pie con información, no decoración | Foto sin pie o pie vacío | MEJORAR |
| O13 | Testimonio de un cliente o un experto real, nunca de un famoso ni una cara de catálogo | Famoso o modelo de stock | RECHAZAR |
| O14 | Los emails de valor parecen una nota útil de un experto, no un folleto | Parece un anuncio disfrazado | REESCRIBIR |
| O15 | Si hay oferta, el precio, el «desde X» o de qué depende está visible | Oferta sin precio ni condición | REESCRIBIR |
| O16 | KISS: una idea, un CTA; el diseño no compite con el mensaje | Ruido, varias ideas, varios destinos | RECHAZAR |

## 1. Equivalencias en un email de secuencia

| Ogilvy | En el email | Consecuencia |
|---|---|---|
| Titular (5× más lectores que el cuerpo) | **Asunto** + preheader; **H1** si lo hay | El asunto decide la apertura: pasa O1-O5. En `recepcion`, cita y asuntos de noticia, O1 y O5 pueden ir «n/a» con motivo |
| Imagen → titular → texto | Bloque `imagen` antes del `titular` | Solo fotos reales de la marca (O9). Sin foto real, email tipográfico |
| Pie de foto | `PIE` de la imagen | Lleva información, no decoración (O12) |
| Marca identificable | Remitente + logo de cabecera + firma | O6 se cumple sin meter la marca en el asunto |
| Precio visible | Solo en `precio` e `invitacion` si el brief da precio o rango | Si no hay precio en el brief, se explica de qué depende; nunca se inventa (O15 n/a con motivo) |
| Parecer editorial | Emails de valor | Se leen como una nota útil de un experto, no como un folleto (O14) |
| Testimonios reales | Bloques `cita` y `caso` | Literales, con autor, del brief o la landing (O7, O13) |
| KISS | Una idea y un CTA por email | Si no se puede decir en una frase de qué va el email, sobra algo (O16) |

## 2. Nivel de consciencia (Schwartz)

El lead que rellena un formulario suele estar **consciente de la solución** (sabe que necesita el servicio y está eligiendo quién). Por eso:
- E0 y bienvenida: entran por **su solicitud** y por quién le va a atender.
- Valor: entran por **la duda o el miedo concreto** que frena la decisión (consciente del problema dentro de la solución).
- Invitación: entra por **el producto**: qué es la cita, qué se lleva, por qué ahora.
- Mercado sofisticado (todos prometen «calidad y confianza»): hace falta un mecanismo concreto del brief (método, garantía, proceso), no adjetivos.

## 3. Compuerta (Parada 2, antes de montar el HTML)

**Paso A · Test de claridad (bloqueante, antes que todo lo demás).** Las siete reglas de `copy-email.md` §0 sobre el asunto, el preheader, las dos primeras frases, cada párrafo y la P. D. Se anota en `copy-auditoria.md` la frase del test del resumen y cualquier regla que haya obligado a reescribir.

**Paso B · Lector sin contexto (obligatorio).** La nota del panel la pone el mismo agente que escribió, así que no detecta lo que solo está claro en su cabeza. Por eso, antes del panel, se lanza un subagente (herramienta Agent) que **no ha visto el brief ni el plan**, con este encargo literal y solo el copy del email:

> Eres una persona de la calle que recibe este email. Lee solo el texto. Responde en cuatro líneas: 1) ¿De qué trata este email, en una frase? 2) ¿Qué te pide que hagas? 3) ¿Qué duda o miedo sobre el servicio te resuelve, si alguno? 4) Copia literal cualquier frase que no hayas entendido a la primera, que te suene rebuscada o que parezca una adivinanza. Si todo se entiende, escribe «ninguna». No opines de nada más.

- Si su respuesta 1 no coincide con la frase del test del resumen, o la 2 no es el CTA, o la 3 no es la duda u objeción del plan (salvo en `breakup` y la mini-secuencia de cita), o la 4 no es «ninguna», **se reescribe** lo señalado y se repite el paso B (máximo 3 veces; si sigue fallando, el copy se enseña en la Parada 2 marcado `_PEND` con el motivo).
- **Qué se arregla retocando y qué obliga a reescribir.** Si lo que señala es una frase concreta —un pronombre sin referente, jerga, una metáfora—, se cambia esa frase. Pero si dice que **no se entiende de qué va el email, qué es el servicio o para qué sirve**, eso no es una frase: es el email. Se reescribe entero con ese criterio. Retocar palabras sueltas ahí gasta pasadas y no arregla nada.
- **El límite de 3 pasadas es un límite de verdad, y no por pereza.** A partir de la tercera, el lector empieza a contradecirse (pide quitar algo y dos pasadas después pregunta por ello). Cuando las respuestas 1, 2 y 3 son correctas y solo quedan preferencias de redacción, se para, se anota en `copy-auditoria.md` **qué se decidió no cambiar y por qué**, y se lleva a la Parada 2.
- Si una pega del lector **choca con una regla del negocio** (una fórmula que la marca usa a propósito, por ejemplo), manda la regla del negocio y se deja escrito.
- Se guarda su respuesta literal en `copy-auditoria.md`.
- Si la herramienta Agent no está disponible, se dice al usuario en la Parada 2 que el paso B no se ha podido hacer.

1. **Checks O1-O16** de §0 sobre asunto, preheader, H1, cuerpo, prueba, CTA e imagen, con las equivalencias de §1. Lo que no aplica se marca «n/a» con motivo. Cualquier REESCRIBIR o RECHAZAR se corrige antes de seguir.
2. **Panel de expertos**: relee el email cuatro veces, cada una con la mirada de uno: **Ogilvy** (claridad, especificidad, prueba), **Schwartz** (¿entra por donde está el lead según §2?), **Gary Halbert** (¿se lee de un tirón, como una carta de persona a persona?) y, de disidente, **Rory Sutherland** (¿qué parte es lógica de marketing que a una persona real no le importa?). Cada silla: nota 1-10 + la frase citada literal + qué cambiar. **Aprobado solo con todas ≥ 7 y media ≥ 8.** Ante la duda, la nota baja. Máximo 4 pasadas; si no aprueba, se entrega marcado `_PEND` con el motivo.
   ⚠️ **La nota la pone quien escribió: sirve para corregir, no como prueba de calidad, y no se le enseña al usuario como argumento.** Es fácil que varias versiones seguidas de un mismo email se autopuntúen cada vez más alto mientras el usuario las rechaza todas: la nota mide la confianza del que escribe, no si el email sirve. En la línea de resumen de la entrega va el resultado de los controles, no la nota.
3. **Tests de secuencia** (propios de esta skill):
   - **Test de valor** (`secuencia.md` §2): con el copy ya escrito, se comprueba que el email contiene de verdad la situación, el conocimiento y la **acción para hoy** del plan, con los mismos ids de hallazgo. Si la acción no está escrita de forma que el lead pueda hacerla hoy, es relleno; si el email describe el servicio más que la situación del lead, es venta. Se reescribe.
   - **Duda u objeción (obligatorio salvo en `breakup` y la mini-secuencia de cita, `secuencia.md` §2.1)**: el email nombra la duda del plan (Dn) con las palabras del lead y la responde con el hallazgo con fuente, según `copy-email.md` §4b. Si no está o se queda en adjetivos, se reescribe. Se anota en `copy-auditoria.md` qué Dn derriba y la frase que lo hace.
   - **Test de la landing**: si el email podría pegarse en la landing del cliente sin cambiar nada, no es de valor.
   - **Un CTA**: un destino por email (el mismo puede repetirse en la P. D.).
   - **Encadenado**: la P. D. o el cierre dicen con claridad qué cuenta el siguiente email real, con su dato concreto (`parametros.md` §3). Nada inventado ni dejado en el aire.
   - **Sin repetir ángulo** respecto a los emails ya aprobados de la secuencia.
   - **Datos**: cada cifra, plazo, precio, garantía o testimonio tiene su línea en `fuentes.md`.
4. **Tests mecánicos**: «Ahora puedes…» en el CTA de botón o enlace (no en preguntas ni asuntos); barrido «¿y qué?»; barrido de especificidad; AI-tells de `copy-email.md` §3.
5. Se guarda `eN/copy-auditoria.md`: tabla O1-O16 (pieza · check · resultado · cita), notas del panel con cita, tests de secuencia y cambios hechos. En la entrega se resume en una línea: «Ogilvy: O1-O16 OK · secuencia OK · build 0 avisos · QA 0 errores».
   **Las cifras de la auditoría se copian de la salida del script, nunca se cuentan a ojo.** Contado a ojo, es fácil afirmar «todos los campos dentro de límite» con el cuerpo en 338 palabras sobre un máximo de 320, o «tres frases» en un `breakup` que tiene cinco. Si un número no lo ha dicho `build_email.py` o `qa_email.py`, o no se ha medido con un comando, no se escribe. Decir «0 avisos» solo significa que cumple las reglas, no que el email funcione: eso se ve en la bandeja.

## 4. Lo que la compuerta no puede saltarse

- No se inventa ningún dato para ser específico. Sin cifra en el brief, se busca otra forma concreta con lo que sí hay.
- Urgencia y escasez solo si son reales y están en el brief.
- Las promesas que la ley limita en el sector (salud, estética, legal, financiero, inmobiliario) se escriben con la prudencia de la landing del cliente; si la landing no promete un resultado, el email tampoco.
