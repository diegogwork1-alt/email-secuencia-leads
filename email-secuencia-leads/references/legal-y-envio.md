# Legal (RGPD + LSSI) y envío desde n8n

Etiquetas: [Investigación] = práctica documentada (AEPD, TJUE, guías de Gmail, Yahoo y Microsoft para remitentes) · [General] = ley o práctica conocida; se confirma con el usuario en la Parada 1 · ⚠️ = sin fuente firme, verificar en la plataforma antes de darlo por hecho.

**Ámbito**: España y la UE (RGPD y LSSI). Si el negocio está en otro país, las ideas (consentimiento, baja, identidad del remitente) valen igual, pero los artículos y requisitos se comprueban con la ley de ese país.

## 1. Comprobación legal del formulario (Parada 1)

`leer_landing.py` lee las casillas del formulario (HTML nativo y Tally). El modelo confirma leyendo `landing/landing.md`.

| Qué se envía | Base legal | ¿Hace falta casilla aparte? |
|---|---|---|
| **E0 `recepcion`** y la mini-secuencia de **cita** | Atender lo que el lead ha pedido: medidas precontractuales (art. 6.1.b RGPD) [Investigación] | No |
| **Emails de valor, invitación y breakup** | Son comunicaciones comerciales por email: el **art. 21.1 LSSI** exige que el lead las haya **solicitado o autorizado expresamente**. La LSSI no distingue B2B de B2C [Investigación] | **Sí** |
| Contacto periódico posterior | Igual que los de valor | **Sí** |

La excepción del art. 21.2 LSSI (cliente con contrato previo y productos similares) **no aplica** a un lead que solo ha rellenado un formulario [Investigación].

**Qué debe tener el formulario** [Investigación: AEPD, Planet49, art. 7 RGPD]:
- Información básica junto al botón: responsable, finalidad, base, derechos y enlace a la política de privacidad.
- **Una casilla sin marcar e independiente** del tipo «Acepto recibir información y comunicaciones sobre [servicio] por email». No vale la misma casilla que la de aceptar la privacidad.
- [General] Si el formulario pregunta por salud, adicciones, situación económica, orientación, religión o similares (categorías especiales, art. 9 RGPD), hace falta además consentimiento explícito para tratar esos datos. Se avisa en la Parada 1.

**Qué hace la skill**:
- **Casilla independiente presente**: se entrega la secuencia completa.
- **Casilla ausente, combinada o no verificable**: se entrega **solo el E0** (y la mini-secuencia de cita si hay agenda) y, arriba del todo en la Parada 1 y en `calendario.md`, este aviso: «🔴 **Legal: el formulario no tiene la casilla independiente de comunicaciones comerciales (art. 21 LSSI). Se entrega solo el E0. Cuando la casilla esté añadida, se preparan los emails de valor.**» El plan de la secuencia completa se propone igual en la Parada 1, para que el usuario sepa qué viene, pero no se redacta ni se monta hasta que confirme que la casilla existe.

**Pie de cada email** (lo monta el script desde `marca.json`) [Investigación]:
- La frase «Comunicación comercial.» (el email tiene que ser reconocible como tal).
- Identidad del remitente: razón social o nombre comercial, NIF si el brief o el aviso legal lo dan, y dirección.
- Motivo de recepción: «Recibes este email porque pediste información sobre [servicio] en [web].»
- Baja sencilla y gratuita en todos los emails: enlace de baja si `marca.json` trae `url_baja`; si no, `mailto:` al remitente con asunto «Baja».
- Enlace a la política de privacidad si la landing la tiene.

## 2. Variables del formulario en n8n

En la ficha se escriben `[[campo]]` o `[[campo|fallback]]`. El script las convierte en expresiones de n8n que el nodo de email evalúa al enviar:

| En la ficha | En el HTML y el TXT |
|---|---|
| `[[nombre]]` | `{{ $json.nombre }}` |
| `Hola[[nombre\|]]:` | `Hola{{ $json.nombre ? ' ' + $json.nombre : '' }}:` → «Hola Laura:» o «Hola:» |
| `[[servicio\|tu proyecto]]` | `{{ $json.servicio \|\| 'tu proyecto' }}` |

- El nombre del campo (`nombre`, `servicio`…) es el que llega del formulario a n8n. `leer_landing.py` propone los nombres; se confirman en la Parada 1 y se guardan en `marca.json` → `campos_formulario`. `build_email.py` da ERROR si una ficha usa un campo que no está ahí.
- ⚠️ El webhook de Tally entrega las respuestas como una lista (`data.fields[]`), no como `$json.nombre`. Antes del envío hace falta un nodo **Set / Edit Fields** que cree `nombre`, `email`, etc. con los nombres de `campos_formulario`. Se recuerda en `calendario.md`.
- ⚠️ En el nodo de email, los campos Asunto, HTML y Text tienen que estar en modo **Expression** (no Fixed); si no, las llaves `{{ }}` salen literales.
- Si el flujo cambia la ruta de los datos (p. ej. tras un nodo Wait se usa `$('Webhook').item.json`), se cambia una vez `marca.json` → `n8n_prefijo` (por defecto `$json`) y se vuelve a montar.
- Las variantes por respuesta se montan como HTML separados y en n8n se elige con un nodo IF o Switch.

## 3. Envío desde n8n

Lo que dice la investigación  y lo que hay que verificar:

- **multipart/alternative obligatorio** [Investigación]: cada email va con su HTML y su texto plano (`email.txt`). Si el nodo elegido no admite las dos partes, hay que cambiar de nodo o de proveedor; no se envía solo HTML.
- **Cabeceras de baja en un clic** (`List-Unsubscribe` + `List-Unsubscribe-Post`, RFC 8058) [Investigación]: con el nodo SMTP básico de n8n **no siempre** se pueden añadir; con un proveedor por API (Resend, Brevo, SES) sí. **La investigación recomienda enviar por API.** Mientras se envíe por SMTP o Gmail, el enlace de baja del pie es la única baja, y por eso es obligatorio en todos los emails.
- **Dominio de envío** [Investigación]: subdominio propio para la secuencia (p. ej. `hola.cliente.com`) separado del correo transaccional, con SPF + DKIM alineados + DMARC (mínimo `p=none`). Sin autenticación, Microsoft rechaza desde mayo de 2025 y los requisitos de Gmail y Yahoo no se cumplen.
- **Quejas de spam** por debajo del 0,1 %; nunca ≥ 0,3 % [Investigación].
- **Remitente**: nombre de persona + marca; Reply-To real [Investigación].
- ⚠️ El nodo Gmail de n8n añade por defecto una coletilla «This email was sent automatically with n8n»: desactivarla en las opciones del nodo.
- ⚠️ «Responde → se para» necesita en n8n un disparador de correo entrante (IMAP o Gmail Trigger) que marque al lead como «respondió» antes del siguiente envío. Sin eso, la salida por respuesta no existe.
- ⚠️ Con volumen alto (muchos leads al día), Gmail o el SMTP del cliente pueden limitar los envíos: verificar los límites del proveedor antes de activar.

## 3.1 Envío desde una plataforma de email marketing (ActiveCampaign y similares)

**n8n no es la única opción, y conviene preguntarlo en la Parada 1**, antes de montar: cambia el fichero que se entrega y las variables. Si el cliente ya paga ActiveCampaign, Brevo, Mailchimp o Klaviyo, se envía desde ahí y no desde n8n: gestionan la baja, las cabeceras RFC 8058, el multipart y la reputación del dominio sin montar nada.

**Qué se entrega entonces.** Además de `email.html` (el intermedio del montador, con las expresiones de n8n), cada email lleva su `email-activecampaign.html` y `.txt`. Los genera y **los verifica**:

```
python3 ~/.claude/skills/email-secuencia-leads/scripts/version_activecampaign.py <carpeta de la secuencia>
```

Cambia tres cosas y comprueba que no queda ningún resto:

| En el montaje (n8n) | En ActiveCampaign |
|---|---|
| `Hola{{ $json.nombre ? … }}:` | `Hola %FIRSTNAME%:` |
| dirección postal escrita en el pie | `%SENDER-INFO-SINGLELINE%` |
| `mailto:…?subject=Baja` | `%UNSUBSCRIBELINK%` |

Con `%UNSUBSCRIBELINK%` y `%SENDER-INFO-SINGLELINE%` presentes, ActiveCampaign **no añade su propio pie**: si falta alguno, el email sale con dos pies.

**`marca.json` → `utm_source`.** Por defecto es `n8n`. Si se envía desde otra plataforma hay que ponerlo (`"utm_source": "activecampaign"`), o el cliente verá en sus analíticas todo el tráfico del email atribuido a una herramienta que no usa. Es fácil que pase sin que nadie lo vea hasta el final.

⚠️ **Lo que sigue siendo responsabilidad de alguien, no de la plataforma**: el consentimiento del formulario (§1), que los leads sin casilla reciban solo el E0, y las condiciones de salida. Una automatización con esperas no se para sola porque el lead responda: hay que montar esa salida.

## 4. Medición [Investigación]

- UTM en los enlaces a la web del cliente: `utm_source=n8n&utm_medium=email&utm_campaign=<cliente>-secuencia&utm_content=<eN>-<bloque>`. Los pone el script.
- Métricas que valen: clics, respuestas, agendas y ventas en el CRM. Las aperturas no son fiables por la protección de privacidad de Apple Mail.
- Referencias orientativas ⚠️ (rangos mezclados de varias fuentes): clic 2-3,5 %, respuesta 1,5-3 %, baja < 0,3 % por envío. Si un email pasa del 0,5 % de bajas, es demasiado comercial o llega demasiado pronto.

## 5. Lista de control antes de activar (va en `calendario.md`)

1. Casilla de comunicaciones en el formulario, o solo E0 y cita activos.
2. Dominio del remitente con SPF, DKIM y DMARC.
3. Nodo Set con los campos de `campos_formulario`; asunto, HTML y texto en modo Expression.
4. Envío de prueba real a un buzón propio (Gmail, Outlook e iPhone): claro, oscuro, variables rellenas y variables vacías. **Se hace con el E0 antes de aprobarlo.**
5. Peso real en Gmail («Mostrar original») < 102 KB.
6. Enlace de baja probado y coletilla de n8n desactivada.
7. Condiciones de salida montadas: agenda, respuesta (trigger de correo), contacto humano, contratación y baja.
