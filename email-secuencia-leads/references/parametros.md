# Parámetros de la secuencia, del copy y de los bloques

Los números que comprueban los scripts viven en `assets/limites.json`; este fichero los explica y dice de dónde salen. Si un fichero de la skill dice otra cosa, mandan `limites.json` y este.

Base de cada parámetro:
- **[Investigación]**: práctica documentada de email marketing para secuencias post-formulario y de diseño de email HTML (Validity, Nielsen Norman Group, AEPD, guías de remitentes de Gmail, Yahoo y Microsoft, André Chaperon, Marcus Sheridan). Donde dos fuentes se contradicen, se toma la opción más prudente.
- **[Fundamentos]**: Ogilvy, titulares y Schwartz (`ogilvy-email.md`).
- **[Criterio]**: decisión de esta skill sin dato medido detrás. Se revisa cuando haya resultados propios (clics, respuestas, bajas).

---

## 1. Secuencia según el tipo de oferta [Investigación]

El tipo de oferta se decide en la Parada 1 a partir del brief y la landing, y se explica en una frase.

| Tipo | Ejemplos | Emails (E0 incluido) | Duración | Días de envío | CTA principal |
|---|---|---|---|---|---|
| **A · B2C alta consideración** | reforma, clínica, abogado, programa de salud, formación cara | 8 | 21 días | D0, D1, D3, D5, D8, D12, D16, D21 | cita, visita o valoración |
| **B · B2B alto ticket** | consultoría, agencia, software, servicios a empresas | 9 | 32 días | D0, D1, D3, D5, D8, D12, D18, D25, D32 | llamada de diagnóstico |
| **C · Inmobiliaria** | visita a una propiedad, captación de vendedores | 8 | 30 días | D0, D1, D3, D7, D12, D18, D25, D30 | visita privada o valoración |
| **D · Decisión rápida / bajo ticket** | < 1.000 €, reserva, compra directa | 5 | 7 días | D0, D1, D2, D4, D7 | compra o reserva |

Si en la Parada 1 sobra o falta un email (p. ej. no hay caso real que contar), se quita o se sustituye el tipo y se dice; no se rellena.

- **Proporción valor/venta**: como mínimo 80/20 [Investigación]. Solo piden de forma directa (CTA fuerte) el email de **invitación**, la mini-secuencia de cita y el E0 cuando hay agenda online. El E0 ofrece un paso de baja fricción, no vende. El resto enseña y lleva un CTA suave o medio (§3).
- **Cadencia**: más densa al principio y más espaciada después. **Máximo 5 emails por semana** del mismo remitente (Validity) [Investigación]. Nunca dos emails el mismo día, salvo el E0 y un email de cita.
- **Hora** [Criterio sobre evidencia débil ⚠️, ]: E0 al instante. El resto en día laborable de 9:00 a 11:00, hora de España; si el retraso cae en fin de semana o de noche, se espera a la siguiente franja.
- **Al terminar sin convertir**: pasa a un contacto periódico **solo si dio el consentimiento** para comunicaciones (`legal-y-envio.md` §1). Si no, se para.

## 2. Salidas de la secuencia [Investigación]

La secuencia se detiene en cuanto el lead:
- **agenda** la llamada, visita o cita;
- **responde** a cualquier email (se crea una tarea para que una persona conteste);
- **habla con una persona del cliente** (llamada atendida, WhatsApp) y así lo marca el CRM o el comercial [Criterio: no enviar automatismos a quien ya interactúa con ventas];
- **contrata**;
- **se da de baja, rebota o marca como spam**;
- el cliente lo marca como **lead falso o no apto** [Criterio].

Si agenda, pasa a la **mini-secuencia de cita** (`cita-confirmacion`, `cita-recordatorio`, `no-show`, `no-show-2`; se entrega solo si el formulario o la landing llevan agenda) [Investigación]:

| Momento | Email | Contenido |
|---|---|---|
| Al agendar | `cita-confirmacion` | fecha, hora, lugar o enlace, **una tarea previa de 2 minutos** (una pregunta que pensar o un dato que traer), cómo cambiarla |
| 24 h antes | `cita-recordatorio` | recordatorio + una idea de valor para aprovechar la cita |
| 1-2 h antes | (WhatsApp/SMS, fuera de la skill) | enlace o dirección |
| No se presenta, +15-30 min | `no-show` | tono empático, sin culpa, enlace para reagendar |
| No se presenta, +48 h | `no-show-2` | el «email de 9 palabras»: una sola pregunta corta en texto, del tipo «¿Sigues queriendo revisar lo de [proyecto] esta semana?» |

No se ramifica nunca por aperturas (la protección de privacidad de Apple Mail las falsea) [Investigación]. Solo por clic, respuesta o agenda.

## 3. Copy

| Elemento | Parámetro | Base |
|---|---|---|
| Remitente | Nombre de persona + marca: «Laura · Reformas Ruiz». Reply-To real, nunca no-reply | [Investigación] |
| Asunto | **30-45 caracteres** (en móvil se corta hacia 36-42); lo importante en las 2 primeras palabras; sin punto final; 0 emojis salvo que la marca los use; sin mayúsculas enteras; sin «GRATIS» ni clickbait | [Investigación] + [Fundamentos] |
| Alternativas de asunto | 2, de **tipo distinto** y todas diciendo el tema: beneficio, cómo hacer algo, pregunta con el tema dentro, lista, contraria a una creencia, personal, noticia (`copy-email.md` §2) | [Fundamentos · Brodie p. 58-60] |
| Preheader | 40-90 caracteres; completa el asunto, nunca lo repite | [Investigación] |
| Primeras frases | Las dos primeras dicen de qué va el email y para qué le sirve leerlo (`copy-email.md` §0.2); nada de «espero que estés bien» ni «gracias por…» salvo el agradecimiento del E0 | [Investigación: NN/g] + Brodie p. 61-62 |
| Párrafos | 1-3 frases | [Investigación] |
| Párrafo | ≤ 50 palabras | [Criterio] |
| Frases | ≤ 20 palabras de media; ninguna de más de 30 (el script avisa) | [Criterio] + Brodie p. 62-63 |
| Anclas de lectura | En los emails de valor, **hay un ancla cada 130 palabras como máximo**: un subtítulo (`seccion`), un punto que empieza con 2-4 palabras en negrita, un paso, una fila de tabla o la frase clave. Mínimo 2 por email. Sin anclas, el email no se escanea y se reescribe | [Criterio] + `diseno.md` §1.1 |
| Frase clave | **Una por email de valor** (bloque `destacado`): la idea que el lead se lleva si solo lee eso. Sale en cuerpo mayor, no en una caja. Nunca dos | [Criterio] |
| Negritas | 2-4 palabras al empezar cada punto de una lista, y como mucho **una** negrita por párrafo. La negrita marca lo que hay que recordar, no decora | [Fundamentos] |
| Dudas y objeciones | Al menos una por email, con respuesta con fuente; fuera solo `breakup` y la mini-secuencia de cita (`secuencia.md` §2.1) | Brodie p. 83 + [Criterio] |
| Longitud del cuerpo | E0 y cita: 60-150 palabras · valor: 150-320 · invitación: 150-260 · breakup y no-show: **2-4 frases, 15-90 palabras** · no-show-2: 9-40 palabras | [Criterio] salvo el email de 9 palabras [Investigación] |
| CTA | **Uno por email** (un solo destino); puede repetirse en la P. D. Botón: 2-5 palabras; enlace: 2-7 palabras; los dos con verbo + resultado y pasan el test «Ahora puedes…». Una pregunta para responder no tiene límite de palabras ni ese test | [Investigación] + [Fundamentos] |
| CTA suave | Pregunta para responder, o enlace en texto a algo para leer o ver. Emails de valor | [Investigación] |
| CTA medio | Enlace en texto al siguiente paso con el cliente (pedir valoración, ver cómo trabaja). En `precio`, `comparativa` y `proceso`; en `caso`, medio o suave. No es botón | [Criterio] |
| CTA fuerte (botón) | **Solo** en `invitacion` (obligatorio), `cita-confirmacion`, `cita-recordatorio` y `no-show`, y en `recepcion` solo si la landing o el formulario tienen agenda online. Nunca en `no-show-2`. Esta es la única regla; no hay excepciones en otros ficheros | [Investigación] + [Criterio] |
| CTA suave con forma de botón | Bloque `boton` con `"CTA_SUAVE": true`: papel con borde y texto de acento, no relleno. Para el CTA de poco compromiso de los emails de valor (responder, preguntar, pedir orientación) cuando el enlace subrayado se lee flojo. Admitido en todos los tipos menos `breakup` y `no-show-2` (`limites.json` → `tipos_con_boton_suave`). **El relleno de color sigue siendo solo del CTA fuerte**: si un email de valor lleva botón, va suave | [Criterio] |
| Anuncio del siguiente email | **Obligatorio en `bienvenida` y en los emails de valor**, en la P. D. o en la última frase: dice con claridad qué cuenta el siguiente email, con su dato concreto («El jueves te explico el error que encarece un baño un 20 %»). Nunca deja el tema en el aire (`copy-email.md` §0.6). No va en E0, invitación, breakup ni cita | [Investigación: Chaperon] |
| P. D. | Opcional; ≤ 35 palabras. Puede llevar el anuncio del siguiente email, reformular el CTA o responder de pasada una segunda duda | [Investigación: Chaperon] |
| Tono | Español de España, tú (salvo que la marca trate de usted); de persona a persona; experto y cercano | [Criterio] |
| Personalización | Nombre con fallback en el saludo, escrito **`Hola[[nombre|]]:`** (sin coma antes de la variable: sin nombre da «Hola:»). Al menos un dato del formulario en el cuerpo del E0 y de un email más, salvo que la discreción lo desaconseje (`copy-email.md` §5) [Investigación]. En el **asunto solo el nombre**, nunca otro campo: la síntesis admite datos del formulario en el asunto, pero un dato del lead a la vista en la bandeja compromete la discreción y llega con erratas [Criterio] | ver celda |
| Urgencia | Solo con fecha o plazas reales del brief, y nunca en emails automáticos si caduca | [Fundamentos] |

## 4. Bloques de la plantilla [Criterio]

El formato «carta» (saludo, cuerpo, enlace o botón, firma, P. D., pie) sale de la investigación. **El resto de bloques no sale de la investigación**: son herencia del formato de boletín y se usan solo cuando el contenido lo pide y con datos reales. **Cada email tiene que verse distinto del anterior.** El defecto que hay que evitar es la secuencia de cartas iguales: saludo, cinco párrafos, firma. Por eso:

1. **Maqueta obligatoria por tipo** (la comprueba el script, `limites.json` → `bloques_obligatorios`):

| `tipo` | Esqueleto obligatorio | Cómo se ve |
|---|---|---|
| `recepcion` | `carta` + `pasos` | carta corta y tres pasos numerados |
| `bienvenida` | `carta` + (`pasos` o `seccion`) | carta y la lista de lo que va a recibir |
| `leccion` | `titular` + `carta` + (`seccion`, `destacado` o `pasos`) | titular, entrada y el desarrollo con subtítulo o recuadro |
| `errores` | `titular` + `carta` + (`pasos` o `seccion`) | los errores numerados, uno por bloque |
| `precio` | `titular` + `carta` + (`tabla`, `cifras` o `faq`) | tabla de qué sube y qué baja el precio |
| `comparativa` | `titular` + `carta` + (`tabla` o `caso`) | tabla de opciones, una columna por opción |
| `caso` | `carta` + (`caso` o `cita`) | historia con el antes y el después |
| `objeciones` | `carta` + `faq` | preguntas y respuestas |
| `proceso` | `carta` + `pasos` | paso a paso numerado |
| `invitacion` | `titular` + `carta` + (`cierre` o `boton`) | titular, resumen corto y la banda de color con el botón |
| `breakup` | `carta` | 2-4 frases, sin nada más |

2. **Máximo 3 bloques opcionales por email**; los obligatorios del tipo no cuentan. En carta pura, solo los que indica la tabla de abajo.
3. **Ningún email repite el esqueleto de otro** de la misma secuencia (el script avisa comparando las fichas ya montadas). Las cartas puras entre sí sí pueden parecerse.
4. **Los emails de valor largos (más de 200 palabras) se parten en secciones** con `seccion`, `pasos` o `destacado`: nunca seis párrafos seguidos.

| Diseño | Tipos | Bloques permitidos |
|---|---|---|
| **Carta pura** | `recepcion`, `breakup`, `no-show`, `no-show-2`, `cita-*` | `carta`, `enlace`, `firma`, `pie`; `pasos` (solo «qué pasa ahora» en E0 y cita); `resumen` (solo E0, si no hay razón de discreción); `boton` solo en E0 con agenda, `cita-*` y `no-show`; `cierre` solo en `cita-confirmacion` y `cita-recordatorio`. `breakup` y `no-show-2`: solo `carta` y `firma`. Sin `titular` ni `imagen` |
| **Híbrido** | `bienvenida`, `leccion`, `errores`, `precio`, `comparativa`, `caso`, `objeciones`, `proceso`, `invitacion` | `carta`, `enlace`, `firma`, `pie` + `seccion` + `titular` (proporciones en §5) + `boton` o `cierre`, solo en `invitacion` (uno de los dos, obligatorio) + hasta 3 de: `tabla`, `imagen` (solo foto real de la marca), `destacado`, `cita`, `caso`, `faq`, `cifras`, `pasos` |

**Qué comprueba el script y qué se revisa a mano.** `build_email.py` comprueba:
- los bloques obligatorios del tipo;
- el botón según el tipo;
- que la carta pura no lleve titular ni imagen;
- el máximo de opcionales;
- que el esqueleto no se repita respecto a los emails ya montados.

El resto de esta tabla se revisa a mano en el montaje, antes de ejecutarlo:
- `resumen` solo en E0;
- `pasos` en carta pura solo en E0 y cita;
- `breakup` y `no-show-2` solo con `carta` y `firma`;
- botón en E0 solo si hay agenda.

Límites por campo (los comprueba `build_email.py` desde `limites.json`):

| Bloque | Campo | Límite |
|---|---|---|
| `titular` | `H1` / `LEAD` | 3-10 palabras, ≤ 60 caracteres, sin punto / ≤ 30 palabras. Sin antetítulo (`diseno.md` §1.1) |
| `imagen` | `IMG` / `ALT` / `PIE` | foto real de la marca (https, JPG/PNG, 1120 px de ancho) / alt descriptivo / ≤ 14 palabras |
| `carta` | `SALUDO` / `parrafos` / `puntos` | ≤ 6 palabras / 1-7 párrafos de ≤ 50 palabras / 0-5 puntos de ≤ 22 palabras |
| `resumen` | `filas` | 2-5 filas; etiqueta ≤ 3 palabras; valor = variable del formulario |
| `pasos` | `pasos` | 3-4 pasos; título ≤ 6 palabras; texto ≤ 24 palabras |
| `seccion` | `TITULO` / `parrafos` | 2-9 palabras, ≤ 60 caracteres / 1-4 párrafos de ≤ 50 palabras |
| `tabla` | `COL_A`, `COL_B` / `filas` | ≤ 4 palabras cada cabecera / 2-5 filas: etiqueta ≤ 5 palabras, cada celda ≤ 12 |
| `destacado` | `TITULO` / `parrafos` | ≤ 9 palabras / 1-2 párrafos. Sin etiqueta encima ni caja (`diseno.md` §1.1) |
| `cita` | `CITA` / `AUTOR` | ≤ 45 palabras, **literal y real** / como aparece publicado |
| `caso` | `ANTES` / `DESPUES` | ≤ 35 palabras cada uno; solo casos reales del brief o la landing |
| `cifras` | `cifras` | 2-3 cifras reales; `VALOR` ≤ 7 caracteres; `ETIQUETA` ≤ 4 palabras |
| `faq` | `preguntas` | 2-4; pregunta ≤ 12 palabras; respuesta ≤ 45 palabras |
| `cierre` | `TITULO` / `TEXTO` / `CTA_TEXTO` | 2-9 palabras / ≤ 30 palabras / 2-5 palabras. Solo en `invitacion`, `cita-confirmacion` y `cita-recordatorio` (lo comprueba el script) |
| `tabla` | `COL_0` | ≤ 4 palabras: cabecera de la primera columna |
| `caso` | `ANTES_ETIQUETA` / `DESPUES_ETIQUETA` | 1-2 palabras cada una (por defecto «Antes» y «Después») |
| `resumen` | `TITULO` | 2-6 palabras |
| `imagen` | `ALT` | 2-16 palabras, descriptivo |
| `boton` | `CTA_TEXTO` / `CTA_NOTA` | 2-5 palabras / ≤ 16 palabras |
| `enlace` | `ENLACE_TEXTO` | 2-7 palabras |
| `firma` | `PD` | ≤ 35 palabras |

Texto real total: **≥ 500 caracteres** en todos los emails salvo `breakup` y `no-show*` [Investigación].

## 5. Jerarquía y contraste [Criterio, a partir de guías de diseño anti-IA]

**La estética es de la marca; los parámetros son de la skill.** Colores, tipografías y logo salen siempre de la landing del cliente (`diseno.md` §2). Lo que fija la skill es la **relación entre los elementos**, y eso vale para cualquier marca. Los números viven en `limites.json` → `jerarquia`.

**Escala: cada nivel es una proporción del cuerpo, no un tamaño fijo.**

| Nivel | Proporción sobre el cuerpo | Con cuerpo de 16 px |
|---|---|---|
| Cuerpo | 1 (16 px, interlineado 26) | 16 px |
| Entradilla (`LEAD`) | 1,15-1,2 | 18-19 px |
| Frase clave (`destacado`) | 1,25-1,3, en negrita | 20-21 px |
| Subtítulo (`H2`) | 1,4-1,5 | 22-24 px |
| Titular (`H1`) | **2,25-2,6** | 36-42 px |
| Pie y notas | 0,75-0,85 | 12-13 px |

- **Salto mínimo entre niveles contiguos: 1,25×.** Si dos niveles quedan más cerca, uno sobra: se elimina, no se maquilla.
- **Máximo 3 niveles tipográficos por email**, sin contar el pie.
- El interlineado se deriva del tamaño: titular ×1,10-1,15 · subtítulo ×1,33 · frase clave ×1,48 · cuerpo ×1,63.
- **En móvil el titular baja al 85 %** del de escritorio y sigue cumpliendo el mínimo de 2,25× el cuerpo. El resto de niveles no cambia.

**Contraste mínimo sobre el papel de la marca** (el script corrige el color hacia arriba si la marca se queda corta):

| Elemento | Mínimo |
|---|---|
| Titular | 10:1 |
| Cuerpo | 8:1 |
| Texto suave (pie, etiquetas de datos) | 4,6:1 |
| Acento sobre papel (enlaces) | 4,5:1 |
| Texto sobre el botón o la banda | 4,5:1. **Siempre blanco**: si el color de marca no llega, se oscurece el botón hasta que cumple (nunca texto oscuro sobre un botón de color) |

**Estructura:**
- **Un único golpe de color** por email: la banda `cierre` de la invitación y de la cita, o el botón relleno del E0 con agenda. En los demás, el color solo está en el enlace o en el borde del botón suave.
- **Un ancla de lectura cada 130 palabras** como máximo, mínimo 2 por email de valor (§3).
- **Ritmo del espacio**: escala de 4 px; el hueco entre secciones es al menos 1,5× el hueco entre párrafos; encima de un título va más aire que debajo.
- **Maqueta obligatoria por tipo** y prohibición de repetir esqueleto: §4.

**Direcciones** (`marca.json` → `tipografia.estilo`): `editorial` (proporciones amplias), `moderno` (compactas) o `display` (titular en mayúsculas). Solo cambian las proporciones y el radio; la tipografía y el color siguen siendo los de la marca. Si no se indica, se deduce: serif de marca → `editorial`; sans → `moderno`.

## 6. Técnicos [Investigación]

| Parámetro | Valor |
|---|---|
| Ancho | contenedor 560 px (dentro del rango recomendado de 520-560; texto útil 480 px, 55-70 caracteres por línea) |
| Peso HTML | **AVISO > 85 KB; ERROR > 90 KB** (Gmail corta a ~102 KB y el envío engorda el código) |
| Cuerpo | 16 px con interlineado 26 px [Criterio dentro del 1,4-1,6 recomendado, que da 16/24 como ejemplo]. El resto de tamaños y el radio salen de las proporciones de §5, no de aquí |
| Botón | alto ≥ 48 px (lo recomendado es ≥ 44) [Criterio] |
| Contraste | mínimos por elemento en §5 (el suelo legal sigue siendo 4,5:1 en texto y 3:1 en texto grande) |
| Imágenes | https pública, `width` y `alt` siempre, nunca SVG ni WebP, ≤ 250 KB |
| Versión texto plano | obligatoria para cada email (`email.txt`) |
| `<style>` | < 8.192 caracteres, sin `url()` |
