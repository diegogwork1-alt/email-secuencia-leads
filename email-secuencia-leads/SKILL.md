---
name: email-secuencia-leads
description: Diseña y maqueta la SECUENCIA DE EMAILS HTML que se dispara cuando un lead rellena el formulario de una landing (se envía desde n8n o desde una plataforma de email marketing como ActiveCampaign, Brevo o Mailchimp). Le pasas en un mismo mensaje el brief del negocio y la landing (URL o HTML); la skill lee la oferta, el formulario y la identidad visual, comprueba la casilla legal de comunicaciones (RGPD y LSSI), investiga al público, propone la secuencia completa (email de recepción inmediato + emails de valor + invitación + cierre, con días de envío según el tipo de oferta) y, tras tu OK, redacta y monta cada email con diseño tipo carta de marca, copy claro y directo (sin adivinanzas) con los fundamentos de Ogilvy y de Email Persuasion de Ian Brodie, variables del formulario, versión en texto plano, modo oscuro y control de calidad. Valor antes que venta; no inventa datos. Úsala siempre que alguien pida emails de seguimiento, nurturing, secuencia de bienvenida, autorespuesta o emails post-formulario para sus leads, o diga «haz la secuencia de emails de mi negocio», «emails para los leads de mi landing» o cite esta skill, aunque no diga «secuencia». No es para newsletters ni campañas sueltas.
---

# Secuencia de emails para leads · post-formulario

**Quién es quién:** el *usuario* es quien te habla y aprueba. El *negocio* (o *cliente*) es la empresa para la que se hacen los emails: puede ser el propio negocio del usuario o uno al que le lleva el marketing. El *lead* es la persona que rellenó el formulario y recibirá los emails. En este fichero, «tú» eres el modelo.

Tú preparas; **el usuario decide y aprueba**. Hay tres paradas y en cada una te detienes y esperas. No hay modo «sigue sin parar»: si el usuario lo pide, le dices que la skill para en cada email y sigues con la siguiente parada.

**Qué cuenta como OK:** «OK», «aprobado», «adelante», «siguiente» o «sí» sin pedir cambios. Cualquier respuesta con un cambio, una duda o un «bien, pero…» **no** es OK: aplicas el cambio, vuelves a mostrar la misma parada y vuelves a preguntar.

**Idioma.** Los emails van en español. Por defecto, español de España y tuteo; si la landing del negocio usa otra variante (español de Latinoamérica, voseo) o trata de usted, se sigue la landing. Se confirma en la Parada 1.

**Dónde están los scripts.** En la carpeta de esta skill, normalmente `~/.claude/skills/email-secuencia-leads/`. Si la instalaste en otro sitio (por ejemplo en `.claude/skills/` de un proyecto), cambia esa ruta en los comandos.

## Las tres reglas
1. **No inventes datos del negocio.** Precios, plazos, garantías, casos, cifras, testimonios, nombres y URLs salen solo del brief, la landing, las respuestas del formulario y los materiales que pase el usuario. Si falta, escribes `[FALTA: qué]` y lo preguntas; `build_email.py` no monta un email con `[FALTA`.
2. **Valor antes que venta, y sin dudas sin resolver.** El lead ya pidió que le contactaran. Cada email de valor pasa el test de `secuencia.md` §2 (qué sabe después · acción para hoy · qué queda para el servicio). Mínimo 80/20. **Además, cada email derriba al menos una duda u objeción frecuente sobre el servicio**, con respuesta con fuente (`secuencia.md` §2.1). Es obligatorio.
3. **Jerarquía de fuentes** (`secuencia.md` §5): datos del negocio → solo sus materiales; conocimiento sobre el público → la investigación del Paso 2, con cita y solo de fuentes con autoridad para consejos y cifras; práctica de email → `parametros.md`; ley y sentido común (RGPD, LSSI, teléfonos de emergencia, normativa del sector) → permitido, etiquetado `[General]` y confirmado por el usuario en la Parada 1. Si algo de la investigación choca con el negocio, manda el negocio. Si el brief y la landing se contradicen, manda el brief y se avisa.

## Glosario (léelo antes de empezar)
- **Ficha**: `eN/ficha.json`, el contenido de un email; el script lo convierte en HTML y TXT.
- **`eN/`**: carpeta de cada email dentro de la secuencia: `e0/`, `e1/`, `e2/`…
- **Bloque**: pieza de la plantilla (`carta`, `pasos`, `cita`…), lista en `parametros.md` §4.
- **Variable**: dato del formulario dentro del texto, `[[nombre]]` o `[[nombre|fallback]]`; en n8n se convierte en `{{ $json.nombre }}`.
- **CTA suave / medio / fuerte**: pregunta para responder o enlace a algo para leer / enlace en texto al siguiente paso con el negocio / botón. El botón solo en la invitación, en la mini-secuencia de cita (salvo `no-show-2`) y en el E0 si hay agenda online (regla completa en `parametros.md` §3).
- **Mini-secuencia de cita**: `cita-confirmacion`, `cita-recordatorio`, `no-show` y `no-show-2`; solo si hay agenda online.
- **Breakup**: último email, 2-4 frases, cierra con elegancia.
- **Compuerta de copy**: revisión obligatoria del copy antes de montar (`ogilvy-email.md` §3). Se guarda en `eN/copy-auditoria.md`.
- **`fuentes.md`**: lista de cada dato usado con su fuente y cita; se crea en la Parada 1 y se amplía en cada email.
- **`estado.md`**: qué emails están aprobados y en qué parada estás; permite retomar una sesión cortada.

## Paso 0 · Qué hace falta
Lo normal es recibir en un mensaje el **brief** y la **landing**. Comprueba qué tienes:
- **Brief**: PDF, Word, texto pegado en el mensaje o ruta a un archivo. Vale un brief corto en el propio mensaje (qué vende, a quién, precio o de qué depende, proceso, garantías, quién atiende). Si hay un `brief.md` en la carpeta, léelo.
- **Landing**: URL publicada o archivo HTML. Si te dan una carpeta, busca dentro `index.html` o `dist/index.html`.
- **Opcional**: quién firma (nombre, cargo, email, foto), agenda online, materiales extra (guía de estilos, preguntas frecuentes, transcripciones de llamadas, reseñas), qué destacar o evitar.

Si falta el brief o la landing, tu primera respuesta es **solo** pedir lo que falta, en una línea:
> Para preparar la secuencia me falta **[el brief del negocio / la landing con el formulario]**. Pásamelo y arranco.

No pidas lo que ya tienes. Si te pasan varios materiales, léelos todos y cítalos por su nombre en la ficha de la oferta.

## Paso 1 · Leer (sin parada)
Carpeta de trabajo: `emails/secuencia-<AAAA-MM-DD de hoy>/` dentro de la carpeta del proyecto (la fecha, con `date +%F`). Si ya existe una secuencia del negocio con `estado.md`, léelo y **retoma donde se quedó** en lugar de empezar de cero.
- **Brief** → `brief.txt`. PDF: Read con `pages`, o `python3 -c "import fitz,sys;print('\n'.join(p.get_text() for p in fitz.open(sys.argv[1])))" archivo.pdf`. Word: `textutil -convert txt -stdout archivo.docx` en Mac, o `python3 -c "import docx,sys;print('\n'.join(p.text for p in docx.Document(sys.argv[1]).paragraphs))" archivo.docx`. Texto del mensaje: se guarda tal cual y la fuente se cita «brief (mensaje)».
- **Landing** → `python3 ~/.claude/skills/email-secuencia-leads/scripts/leer_landing.py "<URL o archivo>" --salida <carpeta>/landing` y abre `landing/landing.md`. Lee formularios nativos y de Tally (embebidos o en ventana emergente). Si el formulario es de otro proveedor, pide al usuario las preguntas y las casillas. Si la URL da error, pide el HTML. Guarda siempre una copia del HTML leído.
- Abre `parametros.md`, `secuencia.md`, `legal-y-envio.md` §1 y `diseno.md` §1-§3 (las señales de diseño de IA están en §1.1).

## Paso 2 · Investigar el público (sin parada)
Sigue `references/investigacion-publico.md` al pie de la letra. En resumen:
1. Define los avatares (buyer persona y lead prototipo) con el brief y la landing.
2. Reúne fuentes: con la búsqueda web (WebSearch y WebFetch) o, si tienes conectado NotebookLM, en un cuaderno con los materiales del negocio.
3. Busca la voz del público y el conocimiento con autoridad.
4. Clasifica las fuentes.
5. Responde las 11 preguntas fijas: sentimientos, intereses, qué necesita saber del servicio, dudas, objeciones, respuestas a cada una, momentos, acciones para hoy, mitos, cómo elegir y límites.
6. Escribe `investigacion/publico.md` con los avatares (A1…), los hallazgos (H1…) y la tabla de dudas y objeciones (D1…).

Tarda unos 10 minutos. Mientras corre, di al usuario en una línea qué estás haciendo. Si no tienes ninguna herramienta de búsqueda, díselo y pide material del experto del negocio (preguntas frecuentes de sus llamadas, reseñas, transcripciones); no lo sustituyas con conocimiento propio.

## Parada 1 · Diagnóstico y plan → OK
Crea `marca.json` (formato `assets/ejemplo-marca.json`, reglas `diseno.md` §2), `fuentes.md` y `plan.md`. Muestra en el chat, en este orden:

1. **Legal, arriba del todo**: 🟢 casilla de comunicaciones independiente, o 🔴 ausente/combinada/no verificable, con el texto literal de las casillas. Si es 🔴, el aviso exacto de `legal-y-envio.md` §1: se entrega **solo el E0** (y la cita si hay agenda); el plan completo se propone para que el usuario sepa qué viene, pero los emails de valor no se redactan hasta que confirme la casilla. Si el formulario recoge datos sensibles (art. 9 RGPD), se dice aquí como `[General]`. Si el negocio no está en España ni en la UE, se dice que estas reglas son de España y la UE y que debe confirmar las de su país.
2. **Discreción**: si el avatar oculta el problema a su entorno (`copy-email.md` §5), lo propones: asunto y preheader sin la palabra sensible, pero diciendo igualmente de qué va el email, y sin repetir sus respuestas del formulario. El cuerpo sí nombra el tema. El usuario confirma.
3. **Ficha de la oferta** (tabla, cada dato con su fuente: «brief p. 3», «landing», «FAQ l. 120», «brief (mensaje)»): servicio y promesa · avatares (A1…, definidos en el Paso 2) · diferenciales · prueba disponible (solo la que existe y es verificable) · proceso · precio o de qué depende · siguiente paso real y su URL · quién firma.
4. **Formulario → variables y plataforma de envío**: cada pregunta con su campo (`[[campo]]`), sus opciones y en qué email se usa (o «en ninguno, por discreción»). Y **pregunta con qué se envía**: n8n, ActiveCampaign, Brevo, Mailchimp… No es un detalle para el final: cambia el fichero que se entrega, las variables del saludo y el `utm_source` de `marca.json` (`legal-y-envio.md` §3.1). Si el negocio ya paga una plataforma, se envía desde ahí. Saberlo a mitad de la secuencia obliga a rehacer los enlaces de todos los emails.
5. **Tipo de oferta** (A/B/C/D de `parametros.md` §1) y por qué, en una frase.
6. **Lo que hemos aprendido del público** (de `investigacion/publico.md`):
   - los avatares (A1…), en una línea cada uno;
   - los 5-8 hallazgos más útiles (intereses y qué necesita saber incluidos), con id, cita corta y grupo de la fuente (AUTORIDAD, PUBLICO o CLIENTE);
   - **las dudas y objeciones más frecuentes** (D1…), con las palabras del lead, la respuesta (Hn) o `[FALTA: respuesta del cliente]`, y en qué email se derriba cada una.
   
   Los que chocan con el negocio o hay que validar, marcados.
7. **Plan de la secuencia** (tabla): email · día · `tipo` · **situación del lead (Hn)** · **duda u objeción que derriba (Dn → Hn)** · **qué sabe después (Hn)** · **acción para hoy (Hn)** · **qué queda para el servicio** · asunto provisional · CTA (suave/medio/fuerte y destino) · bloques. Qué columnas son obligatorias en cada tipo de email: `secuencia.md` §2 y §2.1. Si una obligatoria queda vacía, ese email cambia de ángulo o se quita. Las 5 dudas u objeciones más frecuentes tienen que quedar cubiertas antes de la invitación (en el tipo D, las que no quepan las responde la invitación). Se añade la mini-secuencia de cita solo si hay agenda.
8. **Identidad visual**: logo (URL PNG/JPG o «falta PNG»), acento, botón, tipografía de titulares, papel, y si los titulares van en mayúsculas o las citas sin cursiva según la guía de la marca.
9. **Idioma y trato**: variante del español y tú, vos o usted, según la landing.
10. **Datos que faltan**, lista corta y numerada. Aquí van también las decisiones `[General]` y los hallazgos marcados «validar con el cliente» que el usuario debe confirmar.

Termina con: **«¿Apruebas el plan de la secuencia? No redacto nada sin tu OK.»** Guarda `estado.md`: «Plan pendiente de OK».

## Cada email, en orden (E0 → E1 → …)

### Parada 2 · Copy → OK
Antes de escribir, lee `copy-email.md` (sobre todo §0, claridad antes que ingenio), `brodie-email.md` y los checks de titulares de `ogilvy-email.md` §0 (O1-O5). Redacta con `secuencia.md` §3, dentro de `parametros.md` §3-§4. **Regla que manda: se entiende de qué va el email en el asunto y en las dos primeras frases, y todo se dice con palabras de la calle, sin misterio ni adivinanzas.** Cada dato nuevo va a `fuentes.md`. Pasa la **compuerta de `ogilvy-email.md` §3** y guárdala en `eN/copy-auditoria.md`.

Muestra:
- asunto recomendado y 2 alternativas;
- preheader y remitente;
- el texto de cada bloque en su orden, con las variables como `[[campo]]`;
- **qué duda u objeción derriba (Dn) y la frase que lo hace**;
- CTA y destino;
- **la maqueta**: los bloques en orden (`parametros.md` §4) y en qué se diferencia del email anterior;
- la línea de resumen de la compuerta.

Pregunta: **«¿Apruebas el copy del email N?»**

- **Si la compuerta no aprueba** tras sus intentos, muestras el copy marcado `_PEND` con el motivo. Solo se monta con el OK explícito del usuario o después de aplicar sus cambios.
- **Si falta la respuesta del negocio** a la duda principal del email (`[FALTA: respuesta del cliente]`), no lo redactas. Se lo dices al usuario y, con su OK, lo marcas «pendiente de respuesta» en `estado.md` y pasas al siguiente email. Lo retomas cuando llegue la respuesta, antes del cierre de la secuencia.

### Montaje y control (sin parada, hasta 0 errores)
1. `eN/ficha.json` con el formato de `assets/ejemplo-ficha.json` y **el copy aprobado tal cual**.
2. `python3 ~/.claude/skills/email-secuencia-leads/scripts/build_email.py eN/ficha.json eN/email.html`. Genera `email.html` (para n8n), `email.txt` y `email-muestra.html`.
   - **Si sale un AVISO que obliga a cambiar texto aprobado** (longitud, CTA, asunto), **no lo cambies por tu cuenta**: vuelve a la Parada 2 con la corrección propuesta y pide el OK de nuevo. Los avisos puramente técnicos (colores, peso) se corrigen en `marca.json`.
3. `python3 ~/.claude/skills/email-secuencia-leads/scripts/qa_email.py eN/email.html` hasta 0 errores.
4. `python3 ~/.claude/skills/email-secuencia-leads/scripts/render_preview.py eN/email.html` (necesita Google Chrome o Chromium y Pillow: `pip install pillow`). Mira con Read `preview-hoja.png`, `preview-oscuro.png` y **todos** los tramos de `previews-detalle/`. Criterio: parece una carta de una marca cuidada, respira, el logo se lee en oscuro, el acento es sobrio, nada se descuadra en móvil. **Y no parece una plantilla de IA**: repasa las señales de `diseno.md` §1.1 (antetítulos, serif de catálogo, crema y terracota inventadas, rayas largas, numeración decorativa). Si no hay Chrome, dilo y pide al usuario que abra `email-muestra.html` en el navegador.

### Parada 3 · Email terminado → OK
Muestra `preview-hoja.png` (con SendUserFile si la herramienta existe; si no, da la ruta). Da el asunto y el preheader tal como van en la plataforma de envío (con expresiones) y las rutas de `email.html` y `email.txt`. En Mac, deja el HTML en el portapapeles con `pbcopy < eN/email.html`.

**Solo en el E0**: pide al usuario que haga un envío de prueba real a su buzón desde la plataforma de envío (Gmail, Outlook e iPhone; con nombre y sin nombre) antes de aprobar. Es la única forma de ver el email como lo verá el lead.

Pregunta: **«¿Apruebas el email N? Con tu OK preparo el N+1.»** Actualiza `estado.md`. Si pide cambios, corrige y vuelve a esta parada (o a la Parada 2 si el cambio es de copy).

## Cierre de la secuencia
Con todos los emails aprobados:
1. **Versión para la plataforma de envío**, si no es n8n. Para ActiveCampaign: `python3 ~/.claude/skills/email-secuencia-leads/scripts/version_activecampaign.py <carpeta>` (`legal-y-envio.md` §3.1). El script verifica solo; si dice FALLA, no se entrega. Para otra plataforma, se cambian a mano sus marcadores de nombre, baja y dirección, con la misma lógica.
2. **Repaso de coherencia de toda la secuencia**, con comandos y no a ojo. Hay que comprobar siempre:
   - **la firma es la misma en todos** (`grep -o '>NombreDeLaFirma<' e*/email.html`): sin `firma.NOMBRE` en la ficha, un email suelto firma con el nombre completo del remitente;
   - **ningún email quedó montado con una versión anterior de la plantilla**: si la skill cambió a mitad, se vuelven a montar todos y se comparan los avisos;
   - **ningún bloque de apoyo se repite en más de dos emails**: `pasos` en tres emails distintos hace que parezcan el mismo correo.
3. **`calendario.md`**, lo que hace falta para montarlo en la plataforma: aviso legal si toca · tabla con email, día y franja, tipo, asunto, preheader, remitente, archivo HTML, archivo TXT, CTA y variables que usa · condiciones de salida · notas de la plataforma y lista de control de `legal-y-envio.md` §3, §3.1 y §5. **Se genera leyendo las fichas**, no copiando asuntos a mano.
4. Muestra `calendario.md` y las rutas de `preview-hoja.png` de cada email.
5. **Para que el negocio la apruebe**: los PNG de las vistas previas, nombrados `E0 - D0 - <asunto>.png`, en una carpeta `para-aprobar/`. Si el usuario se los pasa a otra persona, dile que los PNG son **solo para revisar** y que el correo real se envía en HTML: un email hecho de imágenes carga lento y perjudica la reputación de envío.
6. Escribe en `estado.md` «Secuencia lista (N emails)» con la fecha.

## Lo que no haces
- No envías emails ni montas nada en la plataforma de envío.
- No cambias texto aprobado sin volver a la parada correspondiente.
- No editas `assets/plantilla-carta.html` para un negocio concreto. Si algo no cabe en los bloques, dilo.
- No usas fotos de stock ni imágenes que no sean de la marca.
- No ramificas por aperturas.
- No usas urgencia o escasez que caduque («últimas 4 plazas de septiembre») en emails automáticos.

## Ficheros de la skill
| Fichero | Para qué | Cuándo |
|---|---|---|
| `references/parametros.md` + `assets/limites.json` | Todos los números: secuencia por tipo de oferta, días, copy, bloques, **jerarquía y contraste (§5)**, técnicos | Paradas 1 y 2, montaje |
| `references/investigacion-publico.md` | Cómo investigar el público: avatares, fuentes, búsquedas, clasificación de fuentes, 11 preguntas (intereses, dudas, objeciones y sus respuestas incluidas), formato de hallazgos | Paso 2 |
| `references/secuencia.md` | Test de valor, tipos de email, plantillas por oferta, jerarquía de fuentes, encadenado | Paradas 1 y 2 |
| `references/copy-email.md` | **§0 claridad antes que ingenio**, anatomía, asuntos, tono, banco de ángulos, personalización y discreción, CTA | Parada 2 |
| `references/brodie-email.md` | Reglas de escritura de email de Ian Brodie (*Email Persuasion*), con página | Parada 2 |
| `references/ogilvy-email.md` | Checks de Ogilvy (O1-O16) y compuerta obligatoria del copy | Parada 2 |
| `references/diseno.md` | Dirección de diseño, `marca.json`, bloques, oscuro, variantes, reglas técnicas | Parada 1 y montaje |
| `references/legal-y-envio.md` | RGPD/LSSI, variables de n8n, envío, medición, lista de control | Parada 1 y cierre |
| `assets/plantilla-carta.html`, `ejemplo-marca.json`, `ejemplo-ficha.json` | Plantilla y formatos (los ejemplos son ficticios) | Montaje |
| `scripts/leer_landing.py` · `build_email.py` · `qa_email.py` · `render_preview.py` · `version_activecampaign.py` | Leer landing · montar · controlar · vistas previas · versión para ActiveCampaign | Paso 1, montaje y cierre |
