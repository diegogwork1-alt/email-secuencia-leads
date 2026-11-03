# Diseño premium tipo carta: marca, bloques y reglas técnicas

## 1. Dirección de diseño (por qué es así)

Lo que dice la investigación: en secuencias de servicios, los emails **con aspecto de texto escrito por una persona** ganan en clics y respuestas y caen menos en Promociones; se recomienda un **HTML híbrido minimalista**: una columna, tipografía sobria, logo pequeño (120-160 px) o ninguno, enlaces en texto y botón solo en la invitación (regla completa, con la excepción del E0 con agenda, en `parametros.md` §3). El cuaderno de diseño añade cómo hacerlo cuidado sin perder eso: espacio en blanco, jerarquía tipográfica (serif para titulares, sans para cuerpo), paleta de 1-2 acentos, líneas finas. Los dos cuadernos no dicen exactamente lo mismo (uno pide tipografía estándar; el otro admite una serif de marca): esta skill toma el híbrido y lo aplica **por tipo de email** (`parametros.md` §4):

- **Carta pura** (E0, breakup, no-show, cita): sin titular ni imagen; logo pequeño, saludo, texto, firma.
- **Híbrido** (valor e invitación): lo mismo más un titular y, como máximo, tres bloques de apoyo.

Base común:
- **Una columna de 560 px sobre lienzo continuo** (dentro del rango recomendado de 520-560 px), sin tarjeta blanca sobre fondo gris, que delata el envío masivo.
- **Serif para titulares y sans para el cuerpo.** La serif sale de la marca si la landing la usa (Google Fonts con fallback Georgia); si no, Georgia.
- **Paleta sobria**: tinta, cuerpo y gris suave sobre papel, más **un acento de marca** para enlaces, numerales, bordes de cita y botón. Nada más.
- **Líneas finas de 1 px** para separar, radio de 6 px y ninguna sombra.
- **Espacio generoso**: 40 px de margen lateral en escritorio y 24 px en móvil, con cuerpo de 16/26.
- **Fotos solo reales** de la marca (equipo, trabajos, local, propiedad). Sin foto real, el email es tipográfico, que es igual de premium.
- **Botón sobrio**, solo cuando toca (`parametros.md` §3). En valor, enlace subrayado, o botón suave (borde de acento sobre papel) si el enlace se lee flojo.
- **El botón relleno y la banda de color van siempre con texto blanco.** Si el color de marca no da contraste con el blanco, se oscurece el botón; nunca se pone el texto en oscuro.

## 1.1 Señales de diseño hecho por IA (no se hacen)

Base: las guías de diseño anti-IA más usadas con Claude (como *impeccable* y *design-taste-frontend*). Están escritas para webs; aquí van solo las que pueden pasar en un email.

**Prohibido:**
1. **Etiquetas cortas en mayúsculas pequeñas con espaciado** («ANTES DE PEDIR PRESUPUESTO», «PARA HOY», «CASO REAL»), vayan donde vayan. Es la regla más dura de esas guías: ningún encargo la justifica. La plantilla ya no las monta en ningún bloque; el título solo ya dice de qué va.
2. **Recuadros y tarjetas**: caja con fondo de color suave, borde o filete lateral de color para «destacar» algo. Esas guías lo dicen claro: tarjetas solo si la elevación comunica jerarquía real; si no, se agrupa con un filete de 1 px arriba o con espacio. Y un borde de color de más de 1 px está prohibido. Por eso el bloque `destacado` ya no es una caja: es un filete fino, un título y su texto.
3. **Flechas y símbolos decorativos** junto a los enlaces (→), viñetas de emoji, puntos de color. El enlace se reconoce por el subrayado y por lo que dice.
4. **Numerar por decorar.** Los numerales 01, 02, 03 de `pasos` solo si el orden importa de verdad (qué pasa ahora, proceso, cita). Una lista de tres errores no va numerada: va en `seccion`.
5. **Serif de catálogo porque «suena premium»**: Playfair Display, Cormorant, Lora, Fraunces. Si la marca no usa una serif propia, los titulares van con la misma familia que el cuerpo, en peso 600.
6. **Paleta inventada crema + terracota** (o beige + latón + burdeos). Es la paleta por defecto de cualquier IA. Los colores salen de la landing del cliente.
7. **Raya larga (—) en cualquier texto visible.** Punto, coma o dos puntos. El script avisa.
8. **Punto medio (·) por todas partes.** Se reserva para el pie legal y el «Nombre · Marca» del remitente.
9. **Emoji o símbolos haciendo de iconos.**
10. **Texto con degradado**: el énfasis se hace con peso o tamaño.
11. **Tres columnas iguales de beneficios** o filas de tarjetas idénticas.
12. **Nombres y cifras de relleno** (Juan Pérez, Empresa S.L., «99,9 % de satisfacción»).
13. **Verbos de folleto**: impulsa, transforma, revoluciona, potencia, sin fisuras.

**Cómo se destaca una idea sin caja** (lo que dicen esas guías):
- **Peso y tamaño**, no color ni adorno: el énfasis se hace subiendo el peso o un escalón de tamaño.
- **Aire**: lo importante se separa del resto; lo que va junto, junto. Más espacio encima del título que debajo.
- **Un filete de 1 px arriba** del grupo cuando de verdad hace falta separarlo. Nunca a la izquierda y nunca de color.
- **La cita** se destaca con un tamaño mayor y aire, no con un filete de color.
- **El paso** se titula con lo que hay que hacer («Mide el baño»), no con una etiqueta genérica.

**Lo que se hace en su lugar:**
- **Prueba de entornar los ojos**: con la vista borrosa se ve primero el titular y después el CTA. Si compiten, sobra peso en alguno.
- **Más aire encima de un titular que debajo**, y alternar zonas apretadas con zonas holgadas: eso es ritmo.
- **Agrupar por proximidad** antes que meter cajas, bordes o fondos.
- **Escala de espaciado en múltiplos de 4** (4, 8, 12, 16, 24, 40); nada de valores sueltos.
- **Un solo acento** en todo el email, y que mande en una zona (el botón o el enlace), no salpicado.
- **Modo oscuro compuesto, no invertido**: el script da un punto de partida, pero se mira `preview-oscuro.png` y se corrige. En oscuro el cuerpo lleva algo más de espaciado entre letras.
- **Contraste de verdad en el texto**: los mínimos por elemento están en `parametros.md` §5 y el script sube el color de la marca hasta alcanzarlos. El gris suave se reserva para el pie y las etiquetas de datos: un email todo en gris medio no tiene jerarquía.
- **Escalones grandes**: titular 2,25-2,6× el cuerpo, subtítulo 1,4-1,5×, y salto mínimo de 1,25× entre niveles contiguos. La tabla completa está en `parametros.md` §5; aquí no se repiten números.
- **Un golpe de tono por secuencia**: la invitación cierra con el bloque `cierre`, una banda del color de la marca a todo el ancho con el botón en claro. Es el contraste fuerte del email; por eso no se usa en los demás.
- **La frase clave a mayor tamaño**: el bloque `destacado` sale en cuerpo mayor y más oscuro, precedido de un filete fino. Es lo que se lee cuando se escanea.
- **Detalle real antes que adorno**: una foto de una obra del cliente vale más que cinco recursos gráficos.

Errores que abaratan (no se hacen):
- Emails hechos de imágenes.
- Más de dos familias tipográficas.
- Colores chillones fuera de la marca.
- Texto justificado o centrado en bloques largos.
- Mayúsculas y negritas en exceso.
- Iconos decorativos.
- Stock genérico con personas sonriendo.
- GIFs.

## 2. `marca.json`: la identidad del cliente

Se crea en la Parada 1 a partir de `landing/landing.md` y del brief. Formato en `assets/ejemplo-marca.json`.

| Campo | De dónde sale | Regla |
|---|---|---|
| `logo.url_claro` | Logos candidatos de la landing | **PNG o JPG https** (no SVG ni WebP). Si solo hay SVG o WebP, se pide un PNG al usuario (o al negocio); mientras tanto, `logo_texto` |
| `logo.url_oscuro` | Versión blanca si existe | Opcional. Sin ella, el logo claro debe verse sobre fondo oscuro o el logo debe tener placa |
| `logo.ancho` / `alto` | Proporción real | 120-160 px de ancho (logos cuadrados: 56-64 px), alto ≤ 64 px |
| `colores.acento` | Variable CSS principal o color de marca más usado en botones | El script lo ajusta a contraste AA para texto y botón, y avisa |
| `colores.tinta`, `cuerpo`, `suave`, `papel`, `linea` | Neutros de la landing | Papel `#FFFFFE`. Un papel cálido solo si la landing lo usa: no se inventa una crema para «dar calidez» (§1.1) |
| `tipografia.estilo` | Decisión de la Parada 1, según la tipografía de la marca | `editorial` (proporciones amplias), `moderno` (compactas) o `display` (titular en mayúsculas). Solo cambia proporciones y radio, nunca el color ni la fuente (`parametros.md` §5). Si falta, se deduce: serif → editorial; sans → moderno |
| `tipografia.titulares` | La familia de titulares **de la landing** | Stack con fallback, p. ej. `'Tiempos Text',Georgia,serif`. Si la marca no tiene una propia, la misma familia que el cuerpo. Nunca Playfair, Cormorant, Lora ni Fraunces (§1.1) |
| `tipografia.texto` | Sans de la landing | Stack de sistema: `'Helvetica Neue',Helvetica,Arial,sans-serif` (las webfonts de cuerpo no aportan: Gmail y Outlook las ignoran) |
| `tipografia.google_fonts` | Solo si la marca usa esa fuente en su web | `family=<la de la marca>:wght@600`; vacío si no hay |
| `tipografia.peso_titular` | 400 para Georgia o serif fina; 600 para display | — |
| `tipografia.titulares_mayusculas` | `true` si la marca titula con una display en mayúsculas (Bebas Neue, Oswald…) | H1 a 38/42 px en mayúsculas; el fallback (Gmail, Outlook) también sale en mayúsculas |
| `tipografia.cita_cursiva` | `false` si la guía de marca prohíbe cursivas | Por defecto las citas van en cursiva |
| `colores.boton` | Color de CTA de la guía si es distinto del acento | El script elige texto claro u oscuro con contraste ≥ 4,5:1 |
| `remitente` | Brief (nombre, cargo, email; foto si la hay) | Persona real; si no hay, se pregunta |
| `legal` | Aviso legal y política de la landing | Razón social, NIF, dirección, `privacidad_url`; `url_baja` si n8n tiene una |
| `motivo` | Servicio y web | «Recibes este email porque pediste información sobre … en …» |
| `campos_formulario` | `landing.md` → formulario | `{"campo_n8n": "Pregunta tal cual"}` |
| `lead_muestra` | Inventado verosímil, **solo para las vistas previas** | Nunca se usa en el email real |
| `dominios_utm`, `utm_campaign`, `n8n_prefijo`, `claims_prohibidos`, `tratamiento` | Brief y decisiones | — |

## 3. Bloques de la plantilla (`assets/plantilla-carta.html`)

El script añade siempre `cabecera` arriba y `firma` + `pie` abajo. Las listas van como arrays en el bloque (ver `assets/ejemplo-ficha.json`). Qué bloques admite cada tipo de email y cuántos: `parametros.md` §4 (allí se dice qué comprueba el script y qué se revisa a mano). Los bloques de apoyo (`resumen`, `pasos`, `destacado`, `cita`, `caso`, `cifras`, `faq`, `imagen`) **no salen de la investigación**: se usan solo cuando el contenido real lo pide.

| Bloque | Campos | Uso |
|---|---|---|
| `cabecera` | (automático) logo + línea fina | Siempre |
| `titular` | `H1`, `LEAD` | Emails de valor, invitación. Sin antetítulo (§1.1) |
| `imagen` | `IMG` (1120 px de ancho real), `ALT`, `PIE`, `IMG_URL` | Foto real; se muestra a 480 px |
| `carta` | `SALUDO`, `parrafos[PARRAFO]`, `puntos[PUNTO]` | El cuerpo. Admite `**negrita**`, `[enlace](https://…)` y `[[variables]]` |
| `resumen` | `TITULO`, `filas[ETIQUETA, VALOR]` | E0: lo que el lead nos contó (valores = variables). Filas con filete fino, sin caja |
| `pasos` | `TITULO`, `pasos[PASO_TITULO, PASO_TEXTO]` | Qué pasa ahora, proceso. Numerales serif 01, 02… |
| `seccion` | `TITULO`, `parrafos[PARRAFO]` | Parte el cuerpo en secciones con subtítulo. Lo normal en emails de valor largos |
| `tabla` | `TITULO`, `COL_A`, `COL_B`, `COL_0`, `filas[ETIQUETA, A, B]`, `NOTA` | Comparar dos opciones, o qué sube y qué baja el precio |
| `destacado` | `TITULO`, `parrafos[PARRAFO]` | Consejo clave. Filete fino arriba, título y texto. Sin caja ni fondo (§1.1) |
| `cita` | `CITA`, `AUTOR`, `DETALLE` | Testimonio literal y real. Destaca por tamaño y aire, sin filete lateral |
| `caso` | `TITULO`, `ANTES`, `DESPUES`, `ANTES_ETIQUETA`, `DESPUES_ETIQUETA` | Caso real contado en dos líneas |
| `cifras` | `cifras[VALOR, ETIQUETA]`, `NOTA` | 2-3 datos reales |
| `faq` | `TITULO`, `preguntas[PREGUNTA, RESPUESTA]` | Objeciones |
| `cierre` | `TITULO`, `TEXTO`, `CTA_TEXTO`, `CTA_URL` | Banda de color de la marca a todo el ancho, con el CTA en botón claro. Solo en la invitación y la cita: es el único golpe de color del email |
| `boton` | `CTA_TEXTO`, `CTA_URL`, `CTA_NOTA`, `CTA_SUAVE` | CTA sobre papel. Relleno de acento por defecto (CTA fuerte); con `"CTA_SUAVE": true`, botón secundario de borde y texto de acento para los CTA de poco compromiso de los emails de valor |
| `enlace` | `ENLACE_TEXTO`, `ENLACE_URL` | CTA suave aislado en su línea |
| `firma` | `DESPEDIDA`, `NOMBRE`, `CARGO`, `FOTO` (de `marca.json`), `PD` | Siempre; en la ficha solo hace falta si lleva P. D. |
| `pie` | (automático) «Comunicación comercial», legal, motivo, privacidad, baja | Siempre |

**Composición por tipo.** La maqueta obligatoria de cada tipo está en `parametros.md` §4 y los bloques permitidos también; estas son las composiciones completas que se usan, pensadas para que dos emails seguidos no se parezcan:

- **E0**: `carta` → `pasos` (qué pasa ahora) → (`resumen` si no hay razón de discreción) → (`boton` solo con agenda) → `firma` con P. D.
- **Bienvenida**: `carta` → `pasos` (los temas que vienen) → `enlace` → `firma` con P. D.
- **Lección**: `titular` → `carta` (la entrada) → `seccion` (el desarrollo, con subtítulo) → `destacado` (qué hacer hoy) → `enlace` → `firma`
- **Errores**: `titular` → `carta` corta → `seccion` (un error por sección, sin numerar) → `enlace` → `firma`. Con `pasos` solo si el orden de los errores importa
- **Precio**: `titular` → `carta` → `tabla` (qué sube y qué baja) → (`cifras` si hay datos reales) → `enlace` → `firma`
- **Comparativa**: `titular` → `carta` → `tabla` (una columna por opción) → `enlace` → `firma`
- **Caso**: `carta` (la historia) → `caso` o `cita` → (`cifras` reales) → `enlace` → `firma`
- **Objeciones**: `carta` corta → `faq` → `enlace` → `firma`
- **Proceso**: `carta` → `pasos` → (`destacado` con lo que conviene tener listo) → `enlace` → `firma`
- **Invitación**: `titular` → `carta` → `pasos` (qué es la cita) → `cierre` (banda de color con el botón) → `firma` con P. D.
- **Breakup**: `carta` (2-4 frases) → `firma`

Si un email de valor pasa de 200 palabras y no tiene ni `seccion`, ni `pasos`, ni `destacado`, es un muro de texto: se parte.

## 4. Modo oscuro

- El script calcula la versión oscura: papel `#16171B`, tinta `#F4F2EE` y el acento aclarado hasta 4,5:1.
- Apple Mail y Outlook.com la aplican; Gmail iOS y Outlook clásico invierten a su manera.
- Revisa siempre `preview-oscuro.png`: el logo tiene que verse. Si no se ve, añade `logo.url_oscuro` o usa `logo_texto`.
- El botón conserva su color en oscuro.
- El oscuro **se compone, no se invierte**: lo que da el script es un punto de partida. Si algo queda apagado o el acento pierde fuerza, se ajusta en `marca.json` (§1.1).

## 5. Variantes por respuesta del formulario

Cuando una respuesta cambia el contenido (tipo de servicio, perfil), la ficha lleva `"variantes": {"bano": {"asunto": "…"}, "integral": {…}}` y los bloques propios de cada una llevan `"solo": "bano"`. Se monta una vez por variante:
`build_email.py eN/ficha.json eN/bano/email.html --variante bano`.
En n8n se elige con un nodo IF o Switch. Máximo 2-3 variantes por email: más es difícil de mantener.

## 6. Reglas técnicas (verificadas en la práctica de email HTML)

- **Estructura**:
  - Tablas `role="presentation"`.
  - Contenedor fluid-hybrid de 560 px con ghost table MSO.
  - Columnas `inline-block` dentro de `font-size:0`.
  - Padding en `<td>`.
  - `margin:0` y `mso-line-height-rule:exactly` en textos.
- **Gmail**:
  - Estilos estructurales inline, porque en Android con cuentas no Google borra el `<style>`.
  - `<style>` < 8.192 caracteres, sin errores y sin `url()`.
  - Recorta a ~102 KB: AVISO > 85 KB, ERROR > 90 KB (`limites.json`).
- **Outlook clásico** (motor de Word):
  - `width` en atributos.
  - VML para el botón.
  - Ignora `border-radius` y `max-width`: por eso la ghost table.
  - Fuentes forzadas a Arial y Georgia con `<!--[if mso]>`.
- **Webfonts**:
  - Solo Apple Mail, Outlook Mac y algunos Android las cargan.
  - `<link>` dentro de `<!--[if !mso]>` y siempre con stack de fallback.
- **Oscuro**:
  - Meta `color-scheme` + `:root`.
  - `[data-ogsc]`/`[data-ogsb]` uno por regla.
  - Fondo declarado en cada celda.
  - `#FFFFFE` en lugar de blanco puro.
- **Imágenes**:
  - A 2x, con `width` y `height` en atributos, `display:block` y alt con estilo.
  - JPG para fotos, PNG para logos.
  - Nunca SVG ni WebP.
- **Accesibilidad**:
  - `lang="es"` y `role="article"`.
  - Contraste AA.
  - Texto ≥ 14 px (cuerpo 16).
  - Enlaces con texto que se entiende fuera de contexto.
  - Alineado a la izquierda.
- **Variables del lead**: `word-break:break-word` en las celdas que muestran respuestas del formulario (ya en `resumen`).
