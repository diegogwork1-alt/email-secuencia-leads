# Copy de cada email de la secuencia

Los números están en `parametros.md` §3. Las reglas de escritura de email vienen de `brodie-email.md` (Ian Brodie, *Email Persuasion*) y de los checks de Ogilvy (`ogilvy-email.md` §0). La compuerta obligatoria está en `ogilvy-email.md` §3.

Español de España y tú por defecto; si la landing usa otra variante (Latinoamérica, voseo) o trata de usted, se sigue la landing. Se decide en la Parada 1 y no se mezcla.

## 0. Claridad antes que ingenio (regla que manda sobre todo lo demás)

**Problema que corrige**: el copy de IA sale rebuscado, sin decir qué quería decir, «como si fuese una adivinanza». Ogilvy lo mide: el titular «ciego» rinde un 20 % menos (O3). Brodie lo resume: que el asunto dé *«una buena idea de lo que hay en el email»* (p. 60) y que se escriba *«como hablarías tomando un café»* (p. 70).

Cada email cumple estas siete reglas. Si una falla, se reescribe antes de enseñarlo:

1. **Se entiende de qué va en el asunto.** El asunto nombra el tema o el beneficio con palabras normales. La curiosidad solo se suma a eso, nunca lo sustituye. Test: si alguien lee solo el asunto, ¿sabe de qué trata el email? Si no, se reescribe.
2. **Las dos primeras frases dicen qué es y para qué le sirve leerlo.** Nada de preparar el terreno, crear misterio o empezar por una escena.
3. **Se dice la cosa por su nombre.** Si el email habla de dormir mal, de deudas o de una reforma, lo dice. Nada de «eso», «lo tuyo», «lo que te pasa», «esa sensación», «ya sabes qué».
4. **Palabras de la calle.** Las que usaría el cliente hablando. Nada de metáforas, abstracciones ni frases hechas de copywriter («el precio invisible», «la trampa silenciosa», «lo que nadie ve»).
5. **Una idea por frase y frases cortas**: ≤ 20 palabras de media, ninguna de más de 30. Una pregunta solo si la respuesta viene justo después.
6. **En la bienvenida y en los emails de valor, la P. D. o la última frase dicen qué cuenta el siguiente email**, con su tema concreto y sin enigma: «El jueves te explico cómo apuntar durante una semana a qué hora te despiertas», no «El jueves te cuento lo que pasa a las tres».
7. **Test del café** (Brodie, p. 70): léelo en voz alta. Si no se lo dirías así a alguien sentado delante, se reescribe.
8. **Cada email se sostiene solo.** Nadie recuerda los anteriores, y mucha gente abre el cuarto sin haber leído los tres primeros. Del segundo email en adelante, el copy **no puede apoyarse en lo ya contado**: dentro del propio email se nombra el problema y qué es el servicio, aunque sea en media frase. Nada de «llevamos unos días hablando de lo mismo» sin decir de qué, ni «el programa» sin decir qué programa ni para qué. Test: tapa los emails anteriores; si no se sabe de qué va el servicio, falta una frase.

> **Por qué la regla 8**: es típico que el quinto email compare opciones y el sexto ofrezca una llamada sin que ninguno de los dos diga de qué es el servicio, y que un lector sin contexto entienda otra cosa. Arreglarlo frase a frase no funciona. **Cuando el fallo es «no se entiende de qué va», es reescritura, no retoque.**

**Se tiene que poder escanear.** La mayoría no lee: recorre. Un email de valor se escribe para que, mirándolo 5 segundos, se entienda de qué va y qué hay que hacer:
- **Una frase clave por email**: la idea que se lleva quien solo lee eso. Va en el bloque `destacado`, en cuerpo mayor.
- **Un ancla cada 130 palabras como máximo**: un subtítulo, un punto con sus primeras palabras en negrita, un paso o una fila de tabla (`parametros.md` §3).
- **Los puntos empiezan por lo importante**: «**Mover la toma de agua**: obliga a picar y alicatar de nuevo», no «Hay que tener en cuenta que…».
- **Los subtítulos dicen el contenido**, no son etiquetas: «Mover la toma de agua», no «El factor clave».
- **Una negrita por párrafo como mucho.** Si todo está en negrita, no hay nada destacado.

**Test del resumen:** antes de escribir, apunta en una frase de ≤ 15 palabras qué aprende o hace el lector con este email. Si no sale, el email no está claro todavía. Esa frase se guarda en `copy-auditoria.md`.

**Ejemplos del problema** (email sin discreción; con discreción, ver §2):

| Rebuscado (no) | Claro (sí) |
|---|---|
| Asunto «Lo que pasa a las tres de la madrugada» | «Por qué te despiertas a las tres y ya no duermes» |
| Asunto «Por fuera, todo parece bastante normal» | «Rendir en el trabajo no significa que descanses» |
| «¿Miedo a que se enteren?» | «Si empiezas un tratamiento, ¿se entera tu empresa?» |
| P. D. «Pasado mañana te cuento por qué te despiertas siempre a la misma hora» | P. D. «El jueves te explico cómo apuntar durante una semana cuándo te acuestas y cuándo te despiertas» |
| «Tres ideas que te mantienen donde estás» | «Tres creencias sobre el insomnio que las guías médicas desmienten» |

## 1. Anatomía: qué hace cada sección [Investigación· Brodie p. 61-62, p. 77-78]

| Sección | Qué comunica | Cómo |
|---|---|---|
| **Remitente** | Que escribe una persona real de la empresa | «Nombre · Marca». Si el brief no da una persona, se pregunta al usuario en la Parada 1 |
| **Asunto** | De qué va este email y por qué le interesa | Tema o beneficio claro (§0.1). Tipos en §2 |
| **Preheader** | El dato que le falta al asunto | Completa, no repite, tan claro como el asunto |
| **Titular (H1)** | La idea del email en una línea | Solo en emails híbridos (`parametros.md` §4). Dice lo que se aprende |
| **Saludo + apertura** | Que es para él y de qué va | `Hola[[nombre|]]:` y, en las dos primeras frases, qué es y para qué le sirve (§0.2) |
| **Cuerpo** | La explicación, el caso o la respuesta | Una sola idea, con un ejemplo concreto (Brodie p. 72-73). Párrafos de 1-3 frases |
| **Puente** | Por qué el CTA es el paso lógico | Una frase que responde a lo que el lector piensa al terminar (Brodie p. 84) |
| **Duda u objeción** | Que su freno tiene respuesta | La del plan (Dn), dentro del cuerpo, según §4b. Obligatoria salvo en `breakup` y la mini-secuencia de cita |
| **CTA** | Una sola cosa que hacer | Suave, medio o fuerte según `parametros.md` §3 |
| **Firma** | Persona, cargo, marca | Nombre real; foto opcional si la marca la da |
| **P. D.** | Lo segundo más leído | Puede llevar el anuncio del siguiente email (obligatorio en bienvenida y valor, aquí o en la última frase, §0.6), reformular el CTA o responder de pasada una segunda duda (§4b) |
| **Pie** | Quién envía, que es comunicación comercial, por qué lo recibe y cómo darse de baja | Lo genera el script con `marca.json` |

**Orden de redacción** (Brodie p. 96-97): primero la acción que pide el email, después el asunto, después el cuerpo.

## 2. Asuntos

Tipos permitidos (las 2 alternativas cambian de tipo, no de sinónimos). Todos cumplen §0.1: se entiende de qué va.
- **Beneficio concreto**: «Cómo saber si tu reforma cabe en 30.000 €»
- **Cómo hacer algo**: «Cómo preparar la visita técnica en 10 minutos»
- **Pregunta sobre su situación**, con el tema dentro: «¿Primera vez que reformas una cocina?»
- **Lista o número**: «3 errores al pedir presupuesto de reforma»
- **Llevar la contraria a una creencia**, diciendo cuál: «Dormir hasta tarde el domingo no recupera la semana»
- **Personal**, solo con el nombre: `Sobre tu reforma de cocina[[nombre|]]`
- **Noticia real**: «Ya tenemos fecha para tu visita»

**Prohibido:** asuntos que no dicen el tema («Lo que nadie te cuenta», «Esto te va a sorprender», «Una cosa más», «Lo que pasa a las siete»), asuntos trampa que el cuerpo no cumple, «GRATIS», mayúsculas, exclamaciones, «Re:» o «Fwd:» falsos, y repetir el mismo tipo en emails seguidos (Brodie p. 60).

**Discreción** (§5): el asunto y el preheader pueden evitar la palabra sensible («insomnio», «deudas»), pero **siguen diciendo el tema** con otra palabra clara («Si empiezas un tratamiento, ¿se entera tu empresa?», «3 señales de que tu descanso ha cambiado»). Discreción no es misterio. Qué palabra se evita la confirma el usuario en la Parada 1.

## 3. Tono y voz

- **De persona a persona, como tomando un café** (Brodie p. 70). Se escribe como el especialista que atendería al lead: seguro, claro, sin jerga ni tono institucional.
- **Un ejemplo concreto por idea**: un caso real, una pregunta que hace la gente, una situación del día a día (Brodie p. 72-74).
- **Invitar a responder** en al menos 2 emails, con una pregunta fácil y un motivo (Brodie p. 75).
- **Honestidad que da autoridad**: decir para quién no es, qué no incluye o qué no se puede prometer.
- **Especificidad** (Ogilvy O2): cifras, plazos, nombres de procesos del brief o de la investigación. Nunca se inventa la cifra.
- **Prueba social sin sonar a venta**: una frase de caso real antes del CTA; testimonios literales con autor.
- **Palabras y giros prohibidos** (suenan a IA, a folleto o a enigma): «sumérgete», «descubre la magia», «experiencia única/inolvidable», «de ensueño», «un mundo de posibilidades», «increíble», «sin igual», «a otro nivel», «en el vertiginoso mundo de», «no es solo X, es Y», «¡Te esperamos!», «lo que nadie te cuenta», «el secreto», «la trampa», «invisible», «silencioso», «esa sensación», «ya sabes de qué hablo», «sin fisuras», «impulsa tu…», «transforma tu…», «revoluciona», exclamaciones en cadena, frases enteras en mayúsculas.
- **Signos**: nada de raya larga (—) en el texto; se usa punto, coma o dos puntos. El punto medio (·) se reserva para el pie legal y el remitente (`diseno.md` §1.1).
- **Nada de nombres ni cifras de relleno**: ni «Juan Pérez», ni «Empresa S.L.», ni «99,9 % de satisfacción». O es real y con fuente, o no va.

## 4. Ángulos de valor

**Un ángulo no es un formato, es una situación con solución.** Se construye con cuatro piezas, según `references/investigacion-publico.md` §6:
1. **Situación**: un momento, interés o algo que necesita saber el lead («a las tres de la madrugada», «la noche antes de la llamada»).
2. **Conocimiento**: lo que dicen las fuentes con autoridad o el cliente sobre esa situación.
3. **Acción para hoy**: qué puede hacer después de leer.
4. **Duda u objeción que derriba** (Dn), con su respuesta con fuente (§4b). Obligatoria.

El ángulo se escribe en el plan **con palabras claras**, igual que irá en el email: «Por qué te despiertas de madrugada y cómo apuntarlo una semana», no «Las tres de la madrugada».

Ejemplo débil: «Errores al elegir un programa» (formato vacío, vale para cualquier sector).
Ejemplo fuerte: «Qué preguntar en la primera llamada para saber si una clínica del sueño es seria» (situación: está a punto de hablar con alguien · conocimiento: señales de calidad · acción: llevar 3 preguntas apuntadas).

El banco de abajo son **formatos** para dar forma a un ángulo que ya existe. Nunca se elige un formato y se busca después con qué llenarlo. Uno por email; ninguno se repite [Investigación· Brodie p. 57-58]:

1. Desglose de qué determina el precio
2. El error que más dinero cuesta al contratar
3. Un mito del sector, desmontado con datos
4. La pregunta que casi nadie hace antes de firmar
5. Lo que cuesta esperar, solo con datos reales
6. Caso real con arco (partida → quiebre → cambio → resultado)
7. La señal que indica que un trabajo está bien hecho
8. Detrás de escena: cómo se trabaja
9. Historia de un cliente que dudaba
10. Qué pasa si algo sale mal (garantías reales)
11. Para quién NO es este servicio
12. Checklist de lo que conviene tener antes de empezar
13. Comparativa honesta de opciones
14. Paso a paso de lo que ocurre tras contratar
15. Email de 2-4 frases para reabrir la conversación (breakup)

## 4b. Cómo se derriba una duda u objeción en el email [Brodie p. 83-85 · `secuencia.md` §2.1]

Obligatorio en cada email (salvo `breakup` y la mini-secuencia de cita). Va dentro del contenido de valor, no como un anuncio aparte:

1. **Se nombra tal cual la diría el lead**, con sus palabras de la investigación: «Quizá piensas que esto es caro para lo que es». Claro y directo (§0), nunca insinuado.
2. **Se reconoce sin juzgar**, en una frase: por qué es normal pensarlo.
3. **Se responde con un hecho con fuente**: un dato del cliente (plazo, garantía, proceso, precio), una fuente con autoridad o un caso real. Si la duda es sobre el servicio del cliente, la respuesta sale solo de sus materiales. Sin adjetivos («somos los mejores») y sin prometer lo que la landing no promete.
4. **Se enlaza con lo que enseña el email**: la respuesta sale de la explicación, no se pega al final.
5. **Honestidad**: si la objeción es cierta para algunos («no es para ti si…»), se dice.

En el tipo `objeciones` se tratan 3-4 dudas en `faq`. En los demás, una principal en 2-5 frases. La P. D. puede tocar una segunda de pasada.

| Débil | Fuerte |
|---|---|
| «Nuestro tratamiento es totalmente confidencial.» | «Si te preocupa que se entere tu empresa: [qué hace exactamente el cliente para que no pase, tal como lo dice su brief].» (fuente CLIENTE) |
| «Ofrecemos precios competitivos.» | «Mucha gente cree que una reforma de baño baja de 6.000 €. Lo que más sube el precio es mover las tomas de agua…» (con fuente) |

## 5. Personalización con los datos del formulario [Investigación]

Las variables se escriben en la ficha como `[[campo]]` o `[[campo|texto si viene vacío]]`. `build_email.py` las convierte en expresiones de n8n (`legal-y-envio.md` §2) y da ERROR si el campo no está en `marca.json` → `campos_formulario`.

- **Saludo**: `Hola[[nombre|]]:` → «Hola Laura:» o «Hola:». Nunca `Hola, [[nombre|]]:`.
- **Un dato del formulario vale más que el nombre**: servicio, zona, plazo, presupuesto. Se usa en frases que siguen teniendo sentido si el dato llega raro.
- **Discreción**: si el avatar oculta el problema a su entorno (salud, adicciones, deudas, divorcio, estética…), los emails no repiten sus respuestas y el asunto y el preheader evitan la palabra sensible. **El cuerpo sí nombra el tema desde la primera frase**, porque solo lo lee el lead (§0.3). Se decide en la Parada 1.
- **Contenido distinto según una respuesta**: se hacen variantes de la ficha (`diseno.md` §5).
- Nada de personalización que parezca vigilancia («hemos visto que abriste…»).

## 6. CTA [Brodie p. 75, p. 83-85, p. 90]

- Verbo + resultado: «Reservar mi llamada», «Ver cómo trabajamos», «Contarte mi caso».
- Test «Ahora puedes…»: «Ahora puedes reservar tu valoración» pasa; «Ahora puedes saber más» no.
- Se escribe como la respuesta a lo que el lector piensa al terminar de leer, en 1-3 frases, como lo recomendaría un amigo.
- CTA de respuesta: pregunta cerrada y fácil, con motivo («Respóndeme con una palabra, sí o no, y te mando…»).
- En servicios de precio alto, lo que se pide es la llamada, no la compra. La misma llamada en toda la secuencia.
- Destinos permitidos: URL de la landing o de la agenda del cliente, `mailto:` del remitente, `tel:` o WhatsApp del brief. Nunca una URL inventada.
