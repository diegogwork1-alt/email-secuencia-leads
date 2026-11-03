#!/usr/bin/env python3
"""Monta un email de la secuencia a partir de su ficha JSON, la marca del cliente y la plantilla carta.

Uso: python3 build_email.py eN/ficha.json eN/email.html [--marca ruta/marca.json] [--variante nombre]

Genera, junto al HTML:
  email.html          el que se pega en n8n (variables del lead como expresiones {{ $json.campo }})
  email.txt           versión en texto plano para el campo "Text" del nodo de email
  email-muestra.html  el mismo email con los datos de "lead_muestra" (solo para las vistas previas)

Formato de la ficha: assets/ejemplo-ficha.json · de la marca: assets/ejemplo-marca.json.
Límites y reglas: references/parametros.md y references/secuencia.md §3.
Si hay ERROR no genera nada: corrige la ficha o la marca y vuelve a ejecutar.

Qué hace por ti:
- ensambla los bloques en el orden de la ficha (cabecera arriba, firma y pie abajo si faltan);
- saca colores de claro y oscuro de la marca y ajusta el acento hasta cumplir contraste (WCAG AA);
- rellena el texto escapándolo; admite **negrita**, [enlace](https://…) y variables [[campo]] / [[campo|fallback]];
- botón con VML para Outlook, UTM en los enlaces a los dominios del cliente, pie legal y baja;
- comprueba bloques obligatorios por tipo, límites de palabras, un solo destino de CTA, asunto y preheader.
"""
import colorsys
import html
import json
import re
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from textos_idioma import textos  # noqa: E402  (pie y títulos fijos por idioma)

# Windows: que tildes, eñes y emojis no rompan la salida (la consola usa cp1252).
for _flujo in (sys.stdout, sys.stderr):
    try:
        _flujo.reconfigure(encoding='utf-8')
    except Exception:
        pass


SKILL = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL / 'assets' / 'plantilla-carta.html'
WARN, ERRORES = [], []

# Todos los números salen de assets/limites.json (explicados en references/parametros.md)
LIM = json.loads((SKILL / 'assets' / 'limites.json').read_text(encoding='utf-8'))
OBLIGATORIOS = LIM['bloques_obligatorios']
CON_BOTON = set(LIM['tipos_con_boton'])
CON_BOTON_SUAVE = set(LIM.get('tipos_con_boton_suave', []))
CON_CIERRE = set(LIM['tipos_con_cierre'])
CARTA_PURA = set(LIM['tipos_carta_pura'])
OPCIONALES = set(LIM['bloques_opcionales'])
LIMITES = {tuple(k.split('.')): (tuple(v['palabras']) if 'palabras' in v else None, v.get('max_caracteres')) for k, v in LIM['campos'].items()}
CUENTAS = {tuple(k.split('.')): tuple(v) for k, v in LIM['listas'].items()}
RX_VAR = re.compile(r'\[\[([A-Za-z_][\w.-]*)(\|([^\]]*))?\]\]')
RX_LINK = re.compile(r'\[([^\[\]]+)\]\(((?:https://|mailto:|tel:)[^)\s]+)\)')
RAW = ('IMG', 'URL', 'FOTO', '_HTML')

# Jerarquía: no hay tamaños fijos. Cada nivel es una proporción del cuerpo (limites.json → jerarquia).
JER = LIM['jerarquia']
ESTILOS = JER['estilos']

def escala(estilo):
    """Tamaños en px derivados del cuerpo y de las proporciones del estilo."""
    c, e = JER['cuerpo_px'], ESTILOS[estilo]
    h1, h2 = round(c * e['h1']), round(c * e['h2'])
    clave, lead = round(c * e['clave']), round(c * e['lead'])
    return {'TIT_H1': f'{h1}px', 'TIT_H1_LH': f'{round(h1 * (1.10 if e["mayusculas"] else 1.15))}px',
            'TIT_TRACK': e['track_h1'],
            'TIT_TRANSFORM': 'uppercase' if e['mayusculas'] else 'none',
            'TIT_CLASE': 'h1m' if e['mayusculas'] else '',
            'H2_TAM': f'{h2}px', 'H2_LH': f'{round(h2 * 1.33)}px',
            'CLAVE_TAM': f'{clave}px', 'CLAVE_LH': f'{round(clave * 1.48)}px',
            'LEAD_TAM': f'{lead}px', 'LEAD_LH': f'{round(lead * 1.56)}px',
            'H1_MOVIL': f'{round(h1 * 0.85)}px', 'H1_MOVIL_LH': f'{round(h1 * 0.85 * (1.12 if e["mayusculas"] else 1.18))}px',
            'RADIO': e['radio'], 'CAB_PAD': e['cab_pad'], 'SEC_PAD': e['sec_pad']}

# ---------- color ----------
def hx(c):
    c = c.strip().lstrip('#')
    if len(c) == 3:
        c = ''.join(x * 2 for x in c)
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))

def to_hex(rgb):
    return '#%02X%02X%02X' % tuple(max(0, min(255, round(v))) for v in rgb)

def lum(c):
    v = [x / 255 for x in hx(c)]
    v = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in v]
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]

def contraste(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)

def mezcla(a, b, t):
    ra, rb = hx(a), hx(b)
    return to_hex([ra[i] * t + rb[i] * (1 - t) for i in range(3)])

def ajusta_luz(c, fondo, minimo=4.5):
    """Oscurece o aclara c (manteniendo tono) hasta el contraste mínimo con el fondo."""
    r, g, b = [x / 255 for x in hx(c)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    oscuro_fondo = lum(fondo) < 0.2
    for _ in range(60):
        cand = to_hex([x * 255 for x in colorsys.hls_to_rgb(h, l, s)])
        if contraste(cand, fondo) >= minimo:
            return cand
        l = min(1, l + 0.02) if oscuro_fondo else max(0, l - 0.02)
    return '#F4F2EE' if oscuro_fondo else '#141414'

def tokens(marca):
    col = marca.get('colores', {})
    papel = col.get('papel', '#FFFFFE').upper()
    if papel == '#FFFFFF':
        papel = '#FFFFFE'
    acento = col.get('acento', '#1F3A5F')
    t = {'C_PAPEL': papel, 'C_TINTA': col.get('tinta', '#1A1A1A'), 'C_CUERPO': col.get('cuerpo', '#3F3F46'),
         'C_SUAVE': col.get('suave', '#65656D'), 'C_LINEA': col.get('linea', '#E7E5E4'), 'C_ACENTO': acento}
    # Contraste mínimo por papel (limites.json → jerarquia.contraste_minimo): un gris medio se lee flojo y quita jerarquía
    cmin = JER['contraste_minimo']
    for clave, campo in (('titular', 'C_TINTA'), ('cuerpo', 'C_CUERPO'), ('suave', 'C_SUAVE')):
        if contraste(t[campo], papel) < cmin[clave]:
            t[campo] = ajusta_luz(t[campo], papel, cmin[clave])
    t['C_ACENTO_TXT'] = ajusta_luz(acento, papel, cmin['acento'])
    tx = textos(marca)
    t['LANG'], t['TXT_PRIVACIDAD'], t['TXT_BAJA'] = tx['lang'], tx['privacidad'], tx['baja']
    # Botón relleno y banda de color: SIEMPRE texto blanco (un CTA de color con texto negro se ve
    # barato). Si el color de marca no llega al contraste mínimo con el blanco, se oscurece el botón
    # hasta que cumple (mismo tono, más oscuro, igual que los enlaces).
    # Un cliente con un color muy claro puede forzar otro texto con colores.boton_texto.
    boton = col.get('boton', acento)
    txt = col.get('boton_texto', '#FFFFFE')
    if contraste(txt, boton) < cmin['boton']:
        boton = ajusta_luz(boton, txt, cmin['boton'])
    t['C_BOTON'], t['C_BOTON_TXT'] = boton, txt
    # Color de detalle: viñetas de los puntos y numerales de los pasos. Sin «detalle» en la marca,
    # cada uno sigue con su color de siempre (viñeta = acento, numeral = botón). Con él, los dos lo usan
    # (p. ej. el color del logo en los detalles y otro color para la acción).
    det = col.get('detalle')
    if det and contraste(txt, det) < cmin['boton']:
        det = ajusta_luz(det, txt, cmin['boton'])
    t['C_DETALLE_PUNTO'] = det or acento
    t['C_DETALLE_NUM'] = det or boton
    d = marca.get('colores_oscuro', {})
    t['D_PAPEL'] = d.get('papel', '#16171B')
    t['D_TINTA'] = d.get('tinta', '#F4F2EE')
    t['D_CUERPO'] = d.get('cuerpo', '#D2CEC7')
    t['D_SUAVE'] = d.get('suave', '#A29E97')
    t['D_LINEA'] = d.get('linea', '#2E3036')
    t['D_TINTE'] = d.get('tinte', mezcla(acento, t['D_PAPEL'], 0.14))
    t['D_ACENTO'] = ajusta_luz(acento, t['D_TINTE'])
    t['D_BOTON'], t['D_BOTON_TXT'] = boton, txt
    t['D_DETALLE'] = det or boton
    for k in ('C_TINTA', 'C_CUERPO', 'C_SUAVE'):
        if contraste(t[k], papel) < 4.5:
            WARN.append(f'Color {k} {t[k]} con contraste {contraste(t[k], papel):.2f}:1 sobre el papel: se oscurece.')
            t[k] = ajusta_luz(t[k], papel)
    return t

# ---------- texto ----------
class Ctx:
    marca, tok, utm, email_id, carpeta, estilo = {}, {}, '', 'e0', '.', 'editorial'

def expr(campo, fb, tiene_fb, prefijo):
    acc = f'{prefijo}.{campo}' if re.fullmatch(r'[A-Za-z_]\w*', campo) else f'{prefijo}["{campo}"]'
    if not tiene_fb:
        return '{{ %s }}' % acc
    if fb == '':
        return "{{ %s ? ' ' + %s : '' }}" % (acc, acc)
    return "{{ %s || '%s' }}" % (acc, fb.replace("'", "\\'"))

def vars_a_expr(txt, escapar):
    pre = Ctx.marca.get('n8n_prefijo', '$json')
    def r(m):
        fb = m.group(3) or ''
        if escapar:
            fb = fb.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return expr(m.group(1), fb, m.group(2) is not None, pre)
    return RX_VAR.sub(r, txt)

def vars_a_muestra(txt):
    muestra = Ctx.marca.get('lead_muestra', {})
    def r(m):
        v = str(muestra.get(m.group(1), '')).strip()
        if m.group(2) is None:
            return v or m.group(1)
        if (m.group(3) or '') == '':
            return (' ' + v) if v else ''
        return v or m.group(3)
    return RX_VAR.sub(r, txt)

def add_utm(url, bloque):
    doms = Ctx.marca.get('dominios_utm') or [urllib.parse.urlparse(Ctx.marca.get('web', '')).netloc.replace('www.', '')]
    host = urllib.parse.urlparse(url).netloc.replace('www.', '')
    if not url.startswith('http') or not host or not any(d and host.endswith(d) for d in doms) or 'utm_source=' in url:
        return url
    frag = ''
    if '#' in url:
        url, frag = url.split('#', 1)
        frag = '#' + frag
    sep = '&' if '?' in url else '?'
    return f'{url}{sep}{Ctx.utm}&utm_content={Ctx.email_id}-{bloque}{frag}'

def esc(key, value, bloque, modo):
    """modo: 'html' (n8n), 'muestra' (preview) o 'txt'."""
    value = '' if value is None else str(value)
    if key.endswith(RAW) or key in ('COL_W', 'NUM'):
        return value
    tok = Ctx.tok
    guard = {}
    def proteger(txt):
        return f'\x00{len(guard)}\x00'
    # variables
    def pv(m):
        k = f'\x00{len(guard)}\x00'
        guard[k] = vars_a_expr(m.group(0), True) if modo == 'html' else html.escape(vars_a_muestra(m.group(0)))
        return k
    v = RX_VAR.sub(pv, value)
    # enlaces
    def pl(m):
        k = f'\x00{len(guard)}\x00'
        url = add_utm(m.group(2), bloque)
        guard[k] = (f'<a class="t-acento" href="{html.escape(url, quote=True)}" style="color:{tok["C_TINTA"]};text-decoration:underline;">'
                    f'{html.escape(m.group(1))}</a>')
        return k
    v = RX_LINK.sub(pl, v)
    v = html.escape(v, quote=False)
    v = re.sub(r'\*\*(.+?)\*\*', lambda m: f'<strong class="t-tinta" style="color:{tok["C_TINTA"]};font-weight:600;">{m.group(1)}</strong>', v)
    # Estrellas de una valoración real (★): en dorado (#B8860B, 3,25:1 sobre blanco, pasa el QA). Color en marca.json → colores.estrellas.
    estrellas = (Ctx.marca.get('colores') or {}).get('estrellas') or '#B8860B'
    v = re.sub(r'★+', lambda m: f'<span style="color:{estrellas};letter-spacing:1px;">{m.group(0)}</span>', v)
    for k, g in guard.items():
        v = v.replace(k, g)
    return v

def txt_plano(value):
    value = RX_LINK.sub(lambda m: f'{m.group(1)} ({add_utm(m.group(2), "texto")})', str(value or ''))
    value = re.sub(r'\*\*(.+?)\*\*', r'\1', value)
    return vars_a_expr(value, False)

def palabras(v):
    return len(re.sub(r'\*\*|\[\[[^\]]*\]\]|\[([^\]]*)\]\([^)]*\)', r'\1', v).split())

# ---------- plantilla ----------
def blocks(text, kind):
    return {m.group(1): m.group(2) for m in re.finditer(r'<!-- %s: ([\w-]+) -->\n?(.*?)<!-- /%s: \1 -->\n?' % (kind, kind), text, re.S)}

def apply_si(text, data, lists):
    def repl(m):
        name, inner = m.group(1), m.group(2)
        present = bool(lists.get(name)) if (name in lists or name.islower()) else bool(str(data.get(name, '')).strip())
        return inner if present else ''
    prev = None
    while prev != text:
        prev = text
        text = re.sub(r'<!-- SI: ([\w-]+) -->\n?((?:(?!<!-- SI: ).)*?)<!-- /SI: \1 -->\n?', repl, text, flags=re.S)
    return text

def fill(text, data, bloque, modo):
    def repl(m):
        k = m.group(1)
        if k in Ctx.tok:
            return Ctx.tok[k]
        if k in data:
            return esc(k, data[k], bloque, modo)
        return m.group(0)
    return re.sub(r'\{\{([A-Z0-9_]+)\}\}', repl, text)

def url_final(url, bloque, modo):
    """UTM + variables del lead dentro de la URL (p. ej. calendly.com/x?email=[[email]])."""
    url = add_utm(url, bloque)
    return vars_a_expr(url, False) if modo == 'html' else vars_a_muestra(url)

def boton(texto, url, modo, inverso=False, suave=False):
    """Botón del CTA. `inverso`: claro sobre la banda del bloque «cierre».
    `suave`: botón secundario (papel con borde y texto de acento) para los CTA de poco compromiso
    en emails de valor, cuando el enlace subrayado se queda corto (ficha: "CTA_SUAVE": true)."""
    tok = dict(Ctx.tok)
    if inverso:  # botón claro sobre la banda de color del bloque "cierre"
        tok['C_BOTON'], tok['C_BOTON_TXT'] = tok['C_PAPEL'], tok['C_TINTA']
    t = esc('CTA_TEXTO', texto, 'boton', modo)
    url = html.escape(url_final(url, 'boton', modo), quote=True)
    ancho = max(200, min(480, int(len(re.sub(r'\[\[[^\]]*\]\]', 'xxxxxx', texto)) * 9.6 + 70)))
    f = Ctx.marca.get('_F_TXT')
    radio = tok.get('RADIO', '6px')
    if suave:
        borde = tok['C_ACENTO_TXT']
        return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" class="btn-block" style="border-collapse:separate;"><tr>\n'
                f'<td class="bg-papel bd-acento" align="center" bgcolor="{tok["C_PAPEL"]}" style="background-color:{tok["C_PAPEL"]};border:2px solid {borde};border-radius:{radio};">\n'
                f'<!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="{url}" style="height:48px;v-text-anchor:middle;width:{ancho}px;" arcsize="12%" strokecolor="{borde}" strokeweight="2px" fillcolor="{tok["C_PAPEL"]}"><w:anchorlock/><center style="color:{borde};font-family:Arial,sans-serif;font-size:16px;font-weight:bold;">{t}</center></v:roundrect><![endif]-->\n'
                f'<!--[if !mso]><!--><a class="t-acento" href="{url}" style="display:inline-block;padding:13px 28px;font-family:{f};font-size:16px;line-height:20px;font-weight:600;letter-spacing:0.2px;color:{borde};text-decoration:none;border-radius:{radio};">{t}</a><!--<![endif]-->\n'
                f'</td>\n</tr></table>')
    clase = '' if inverso else ' class="bg-boton"'
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" class="btn-block" style="border-collapse:separate;"><tr>\n'
            f'<td{clase} align="center" bgcolor="{tok["C_BOTON"]}" style="background-color:{tok["C_BOTON"]};border-radius:{radio};">\n'
            f'<!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="{url}" style="height:50px;v-text-anchor:middle;width:{ancho}px;" arcsize="12%" stroke="f" fillcolor="{tok["C_BOTON"]}"><w:anchorlock/><center style="color:{tok["C_BOTON_TXT"]};font-family:Arial,sans-serif;font-size:16px;font-weight:bold;">{t}</center></v:roundrect><![endif]-->\n'
            f'<!--[if !mso]><!--><a class="{"" if inverso else "t-boton"}" href="{url}" style="display:inline-block;padding:15px 30px;font-family:{f};font-size:16px;line-height:20px;font-weight:600;letter-spacing:0.2px;color:{tok["C_BOTON_TXT"]};text-decoration:none;border-radius:{radio};">{t}</a><!--<![endif]-->\n'
            f'</td>\n</tr></table>')

def logo_html():
    m, tok = Ctx.marca, Ctx.tok
    lg = m.get('logo') or {}
    href = html.escape(add_utm(m.get('web', ''), 'logo'), quote=True)
    alt = html.escape(lg.get('alt') or m.get('cliente', ''))
    if lg.get('url_claro'):
        w, h = int(lg.get('ancho', 150)), int(lg.get('alto', 40))
        clase = ' class="logo-claro"' if lg.get('url_oscuro') else ''  # sin versión oscura, el logo claro no se oculta
        out = f'<a href="{href}" style="text-decoration:none;"><img{clase} src="{lg["url_claro"]}" width="{w}" height="{h}" alt="{alt}" style="display:block;width:{w}px;height:auto;border:0;font-family:Arial,sans-serif;font-size:16px;font-weight:bold;color:{tok["C_TINTA"]};">'
        if lg.get('url_oscuro'):
            out += (f'<!--[if !mso]><!--><div class="logo-oscuro" style="display:none;width:0;max-height:0;overflow:hidden;mso-hide:all;">'
                    f'<img src="{lg["url_oscuro"]}" width="{w}" height="{h}" alt="{alt}" style="display:block;width:{w}px;height:auto;border:0;"></div><!--<![endif]-->')
        return out + '</a>'
    texto = html.escape(m.get('logo_texto') or m.get('cliente', ''))
    return (f'<a class="t-tinta f-tit" href="{href}" style="font-family:{m.get("_F_TIT")};font-size:20px;line-height:26px;font-weight:{m.get("_PESO")};'
            f'letter-spacing:0.4px;color:{tok["C_TINTA"]};text-decoration:none;">{texto}</a>')

def revisa(ficha):
    tipo = ficha.get('tipo')
    if tipo not in OBLIGATORIOS:
        ERRORES.append(f'La ficha necesita "tipo" válido ({", ".join(OBLIGATORIOS)}): secuencia.md §3.')
        return
    tipos = [m['tipo'] for m in ficha['modulos']]
    for req in OBLIGATORIOS[tipo]:
        if not any(t in tipos for t in req.split('|')):
            ERRORES.append(f'El tipo "{tipo}" necesita el bloque {req.replace("|", " o ")} (secuencia.md §3).')
    if 'cierre' in tipos and tipo not in CON_CIERRE:
        ERRORES.append(f'Banda "cierre" en un email de tipo "{tipo}": solo va en {", ".join(CON_CIERRE)} (parametros.md §4).')
    botones = [m for m in ficha['modulos'] if m['tipo'] == 'boton']
    if any(not (m.get('datos') or {}).get('CTA_SUAVE') for m in botones) and tipo not in CON_BOTON:
        ERRORES.append(f'Botón sólido en un email de tipo "{tipo}": va solo en invitación, cita-confirmacion, cita-recordatorio, no-show y E0 con agenda (parametros.md §3). Usa "CTA_SUAVE": true (botón suave) o el bloque "enlace".')
    if any((m.get('datos') or {}).get('CTA_SUAVE') for m in botones) and tipo not in CON_BOTON_SUAVE:
        ERRORES.append(f'Botón suave en un email de tipo "{tipo}": los de carta pura corta ({", ".join(sorted(set(OBLIGATORIOS) - CON_BOTON_SUAVE))}) van solo con texto (parametros.md §3).')
    if tipo in CARTA_PURA and any(t in tipos for t in ('imagen', 'titular')):
        ERRORES.append(f'El tipo "{tipo}" es carta pura: sin titular ni imagen (parametros.md §4).')
    requeridos = {t for req in OBLIGATORIOS[tipo] for t in req.split('|')}
    opc = [t for t in tipos if t in OPCIONALES and t not in requeridos]
    if tipo not in CARTA_PURA and len(opc) > LIM['max_bloques_opcionales_por_email']:
        WARN.append(f'{len(opc)} bloques opcionales ({", ".join(opc)}): máximo {LIM["max_bloques_opcionales_por_email"]} por email (parametros.md §4).')
    for m in ficha['modulos']:
        if (m.get('datos') or {}).get('EYEBROW'):
            WARN.append(f'{m["tipo"]}: las etiquetas tipo antetítulo no se usan en ningún bloque y no se montan (diseno.md §1.1). El título solo ya categoriza.')
    # variedad: el email no puede tener el mismo esqueleto que otro ya montado (parametros.md §4)
    mio = [t for t in tipos if t not in ('cabecera', 'firma', 'pie')]
    for otra in sorted(Path(Ctx.carpeta).glob('../e*/ficha.json')):
        try:
            v = json.loads(otra.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            continue
        if v.get('email') == ficha.get('email') or v.get('tipo') in CARTA_PURA and tipo in CARTA_PURA:
            continue
        suyo = [m['tipo'] for m in v.get('modulos', []) if m.get('tipo') not in ('cabecera', 'firma', 'pie')]
        if suyo == mio:
            WARN.append(f'Mismo esqueleto que {v.get("email", otra.parent.name)} ({" → ".join(mio)}): cambia la maqueta (parametros.md §4).')
    campos_ok = set(Ctx.marca.get('campos_formulario', {}).keys())
    destinos = set()
    for m in ficha['modulos']:
        b = m['tipo']
        campos = [(k, v) for k, v in m.get('datos', {}).items()]
        for k, v in m.items():
            if isinstance(v, list):
                lo, hi = CUENTAS.get((b, k), (0, 99))
                if not lo <= len(v) <= hi:
                    WARN.append(f'{b}: {len(v)} elementos en "{k}" (parametros.md §4: {lo}-{hi}).')
                for it in v:
                    campos += list(it.items())
        for k, v in campos:
            if not isinstance(v, str):
                continue
            for u in RX_LINK.findall(v):
                if u[1].startswith('http'):
                    destinos.add(u[1].split('?')[0].split('#')[0].rstrip('/'))
            if k in ('CTA_URL', 'ENLACE_URL') and v.startswith('http'):
                destinos.add(v.split('?')[0].split('#')[0].rstrip('/'))
            if re.search(r'\[FALTA', v):
                ERRORES.append(f'{b}.{k} tiene un dato pendiente: {v[:60]}')
            for var in RX_VAR.finditer(v):
                if campos_ok and var.group(1) not in campos_ok:
                    ERRORES.append(f'{b}.{k} usa [[{var.group(1)}]] y ese campo no está en marca.json → campos_formulario.')
            if re.search(r',\s*\[\[\w+\|\]\]', v):
                WARN.append(f'{b}.{k}: coma antes de una variable con fallback vacío; sin dato saldrá «Hola,:». Escribe «Hola[[nombre|]]:».')
            lim = LIMITES.get((b, k))
            if not lim:
                continue
            n = palabras(v)
            rango, maxc = lim
            if rango and not rango[0] <= n <= rango[1]:
                WARN.append(f'{b}.{k}: {n} palabras (parametros.md §4: {rango[0]}-{rango[1]}): "{v[:50]}"')
            if maxc and len(v) > maxc:
                WARN.append(f'{b}.{k}: {len(v)} caracteres (máx. {maxc}): "{v[:50]}"')
            if k in ('H1', 'TITULO', 'PASO_TITULO') and v.strip().endswith('.'):
                WARN.append(f'{b}.{k} con punto final: "{v[:50]}"')
    if len(destinos) > 1:
        WARN.append('Más de un destino de CTA en el email (uno por email, parametros.md §3): ' + ' | '.join(sorted(destinos)))
    total = sum(palabras(v) for m in ficha['modulos'] for k, v in list(m.get('datos', {}).items()) + [kv for x in m.values() if isinstance(x, list) for it in x for kv in it.items()] if isinstance(v, str) and not k.endswith(RAW))
    rango = tuple(LIM['cuerpo_palabras'].get(tipo, [150, 320]))
    if not rango[0] <= total <= rango[1]:
        WARN.append(f'Cuerpo de {total} palabras para un "{tipo}" (parametros.md §3: {rango[0]}-{rango[1]}).')
    # Tipos que se miden en frases, no solo en palabras (el breakup son 2-4). Antes solo se
    # contaban las palabras y un breakup de cinco frases pasaba el control.
    fr = LIM.get('frases_cuerpo', {}).get(tipo)
    if fr:
        n = sum(len([f for f in re.split(r'(?<=[.!?])\s+', p.get('PARRAFO', '').replace('**', '')) if f.strip()])
                for mo in ficha['modulos'] if mo['tipo'] == 'carta' for p in mo.get('parrafos', []))
        if not fr[0] <= n <= fr[1]:
            WARN.append(f'{n} frases en el cuerpo de un "{tipo}" (secuencia.md §3: {fr[0]}-{fr[1]}).')
    # La firma cae al nombre del remitente si la ficha no la fija: media secuencia acaba
    # firmando «Marta» y un email suelto «Marta Ruiz».
    rem = ((getattr(Ctx, 'marca', {}) or {}).get('remitente') or {}).get('nombre', '')
    firma = next((mo for mo in ficha['modulos'] if mo['tipo'] == 'firma'), None)
    if firma is not None and not (firma.get('datos') or {}).get('NOMBRE') and ' ' in rem.strip():
        WARN.append(f'Sin firma.NOMBRE en la ficha, la carta firmará «{rem}» (de marca.json). '
                    'Si los demás emails firman solo con el nombre de pila, ponlo aquí también.')

def render(tipo, spec, raw, idx, glob, modo):
    data = dict(glob)
    data.update(spec.get('datos', {}))
    lists = {k: [dict(x) for x in v] for k, v in spec.items() if isinstance(v, list)}
    bloque = tipo if idx == 1 else f'{tipo}{idx}'
    m = Ctx.marca
    if tipo == 'cabecera':
        data['LOGO_HTML'] = logo_html()
    if tipo == 'firma':
        r = m.get('remitente', {})
        data.setdefault('DESPEDIDA', r.get('despedida', textos(m)['despedida']))
        data.setdefault('NOMBRE', r.get('nombre', ''))
        data.setdefault('CARGO', r.get('cargo', ''))
        if r.get('foto'):
            data.setdefault('FOTO', r['foto'])
    if tipo == 'pie':
        lg = m.get('legal', {})
        partes = [lg.get('razon_social') or m.get('cliente', ''), ('NIF ' + lg['nif']) if lg.get('nif') else '', lg.get('direccion', '')]
        data['LEGAL'] = ' · '.join(p for p in partes if p)
        data['MOTIVO'] = textos(m)['comunicacion'] + ' ' + m.get('motivo', '')
        data['PRIVACIDAD_URL'] = lg.get('privacidad_url', '')
        baja = lg.get('url_baja') or (('mailto:' + m['remitente']['email'] + '?subject=' + textos(m)['asunto_baja']) if m.get('remitente', {}).get('email') else '')
        data['BAJA_URL'] = vars_a_expr(baja, False) if modo == 'html' else vars_a_muestra(baja)
    if tipo == 'boton' and data.get('CTA_TEXTO') and data.get('CTA_URL'):
        data['BOTON_HTML'] = boton(data['CTA_TEXTO'], data['CTA_URL'], modo, suave=bool(data.get('CTA_SUAVE')))
    if tipo == 'cierre' and data.get('CTA_TEXTO') and data.get('CTA_URL'):
        data['BOTON_HTML'] = boton(data['CTA_TEXTO'], data['CTA_URL'], modo, inverso=True)
    if tipo in ('enlace',) and data.get('ENLACE_URL'):
        data['ENLACE_URL'] = html.escape(url_final(data['ENLACE_URL'], bloque, modo), quote=True)
    if tipo == 'imagen' and data.get('IMG_URL'):
        data['IMG_URL'] = html.escape(url_final(data['IMG_URL'], bloque, modo), quote=True)
    if tipo == 'resumen':
        data.setdefault('TITULO', textos(m)['resumen'])
    if tipo == 'caso':
        data.setdefault('ANTES_ETIQUETA', textos(m)['antes'])
        data.setdefault('DESPUES_ETIQUETA', textos(m)['despues'])
    if tipo == 'pasos':
        for n, p in enumerate(lists.get('pasos', []), 1):
            p.setdefault('NUM', f'{n:02d}')
    if tipo == 'tabla':
        data.setdefault('COL_0', '')

    text = raw
    protegidos = {}
    def proteger(mm):
        k = f'@@REP{len(protegidos)}@@'
        protegidos[k] = mm.group(0)
        return k
    text = re.sub(r'<!-- REPETIR: ([\w-]+) -->\n?.*?<!-- /REPETIR: \1 -->\n?', proteger, text, flags=re.S)
    text = apply_si(text, data, lists)
    for k, v in protegidos.items():
        text = text.replace(k, v)
    for name, inner in blocks(text, 'REPETIR').items():
        items = lists.get(name, [])
        partes = []
        for it in items:
            d = dict(data)
            d.update(it)
            if '{{COL_W}}' in inner:
                d['COL_W'] = str(480 // max(1, len(items)))
            partes.append(fill(apply_si(inner, d, {}), d, bloque, modo))
        text = re.sub(r'<!-- REPETIR: %s -->\n?.*?<!-- /REPETIR: %s -->\n?' % (re.escape(name), re.escape(name)), lambda _: ''.join(partes), text, flags=re.S)
    return fill(text, data, bloque, modo)

def texto_plano(specs):
    L = []
    m = Ctx.marca
    for s in specs:
        t, d = s['tipo'], s.get('datos', {})
        ls = {k: v for k, v in s.items() if isinstance(v, list)}
        if t == 'titular':
            L += [txt_plano(d.get('H1', ''))] + ([txt_plano(d['LEAD'])] if d.get('LEAD') else []) + ['']
        elif t == 'imagen' and d.get('PIE'):
            L += [f'[{txt_plano(d["PIE"])}]', '']
        elif t == 'carta':
            if d.get('SALUDO'):
                L += [txt_plano(d['SALUDO']), '']
            for p in ls.get('parrafos', []):
                L += [txt_plano(p.get('PARRAFO', '')), '']
            if ls.get('puntos'):
                L += [f'- {txt_plano(p.get("PUNTO", ""))}' for p in ls['puntos']] + ['']
        elif t == 'resumen':
            L += [txt_plano(d.get('TITULO', textos(m)['resumen'])).upper()] + [f'{txt_plano(f.get("ETIQUETA", ""))}: {txt_plano(f.get("VALOR", ""))}' for f in ls.get('filas', [])] + ['']
        elif t == 'pasos':
            if d.get('TITULO'):
                L.append(txt_plano(d['TITULO']))
            for n, p in enumerate(ls.get('pasos', []), 1):
                L.append(f'{n}. {txt_plano(p.get("PASO_TITULO", ""))}' + (f': {txt_plano(p["PASO_TEXTO"])}' if p.get('PASO_TEXTO') else ''))
            L.append('')
        elif t == 'seccion':
            L += [txt_plano(d.get('TITULO', '')), ''] + [x for p in ls.get('parrafos', []) for x in (txt_plano(p.get('PARRAFO', '')), '')]
        elif t == 'tabla':
            L += ([txt_plano(d['TITULO'])] if d.get('TITULO') else [])
            L += [' | '.join(txt_plano(f.get(k, '')) for k in ('ETIQUETA', 'A', 'B')) for f in ls.get('filas', [])]
            L += ([txt_plano(d['NOTA'])] if d.get('NOTA') else []) + ['']
        elif t == 'destacado':
            L += ([txt_plano(d['TITULO'])] if d.get('TITULO') else []) + [txt_plano(p.get('PARRAFO', '')) for p in ls.get('parrafos', [])] + ['']
        elif t == 'cita':
            L += [f'«{txt_plano(d.get("CITA", ""))}»', f'— {txt_plano(d.get("AUTOR", ""))}' + (f', {txt_plano(d["DETALLE"])}' if d.get('DETALLE') else ''), '']
        elif t == 'caso':
            L += ([txt_plano(d['TITULO'])] if d.get('TITULO') else []) + [f'{d.get("ANTES_ETIQUETA", "Antes")}: {txt_plano(d.get("ANTES", ""))}', f'{d.get("DESPUES_ETIQUETA", "Después")}: {txt_plano(d.get("DESPUES", ""))}', '']
        elif t == 'cifras':
            L += [f'{txt_plano(c.get("VALOR", ""))} {txt_plano(c.get("ETIQUETA", ""))}' for c in ls.get('cifras', [])] + ['']
        elif t == 'faq':
            if d.get('TITULO'):
                L += [txt_plano(d['TITULO']), '']
            for q in ls.get('preguntas', []):
                L += [txt_plano(q.get('PREGUNTA', '')), txt_plano(q.get('RESPUESTA', '')), '']
        elif t == 'cierre':
            L += ([txt_plano(d['TITULO'])] if d.get('TITULO') else []) + ([txt_plano(d['TEXTO'])] if d.get('TEXTO') else [])
            L += [f'{txt_plano(d.get("CTA_TEXTO", ""))}: {url_final(d.get("CTA_URL", ""), "cierre", "html")}', '']
        elif t == 'boton':
            L += [f'{txt_plano(d.get("CTA_TEXTO", ""))}: {url_final(d.get("CTA_URL", ""), "boton", "html")}'] + ([txt_plano(d['CTA_NOTA'])] if d.get('CTA_NOTA') else []) + ['']
        elif t == 'enlace':
            L += [f'{txt_plano(d.get("ENLACE_TEXTO", ""))}: {url_final(d.get("ENLACE_URL", ""), "enlace", "html")}', '']
        elif t == 'firma':
            r = m.get('remitente', {})
            L += [d.get('DESPEDIDA', r.get('despedida', textos(m)['despedida'])), d.get('NOMBRE', r.get('nombre', '')), d.get('CARGO', r.get('cargo', '')), '']
            if d.get('PD'):
                L += [f'P. D. {txt_plano(d["PD"])}', '']
        elif t == 'pie':
            lg = m.get('legal', {})
            baja = lg.get('url_baja') or (('mailto:' + m['remitente']['email'] + '?subject=' + textos(m)['asunto_baja']) if m.get('remitente', {}).get('email') else '')
            L += ['--', ' · '.join(p for p in [lg.get('razon_social') or m.get('cliente', ''), ('NIF ' + lg['nif']) if lg.get('nif') else '', lg.get('direccion', '')] if p),
                  textos(m)['comunicacion'] + ' ' + m.get('motivo', '')] + ([f'{textos(m)["privacidad"]}: {lg["privacidad_url"]}'] if lg.get('privacidad_url') else []) + [f'{textos(m)["baja"]}: {vars_a_expr(baja, False)}']
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(L)).strip() + '\n'

def busca_marca(ficha_path):
    if '--marca' in sys.argv:
        return Path(sys.argv[sys.argv.index('--marca') + 1])
    for d in [ficha_path.parent, ficha_path.parent.parent, ficha_path.parent.parent.parent]:
        if (d / 'marca.json').exists():
            return d / 'marca.json'
    return None

def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    fpath, out = Path(sys.argv[1]), Path(sys.argv[2])
    ficha = json.loads(fpath.read_text(encoding='utf-8'))
    mpath = busca_marca(fpath)
    if not mpath or not mpath.exists():
        sys.exit('ERROR   No encuentro marca.json (junto a la ficha, en la carpeta de la secuencia o con --marca).')
    marca = json.loads(mpath.read_text(encoding='utf-8'))
    variante = sys.argv[sys.argv.index('--variante') + 1] if '--variante' in sys.argv else None
    if variante:
        ficha.update(ficha.get('variantes', {}).get(variante, {}))
        ficha['modulos'] = [x for x in ficha['modulos'] if x.get('solo') in (None, variante)]
    elif any('solo' in x for x in ficha['modulos']):
        WARN.append('La ficha tiene bloques por variante ("solo") y no se pasó --variante: se incluyen todos.')

    tip = marca.get('tipografia', {})
    marca['_F_TIT'] = tip.get('titulares', "Georgia,'Times New Roman',serif")
    marca['_F_TXT'] = tip.get('texto', "'Helvetica Neue',Helvetica,Arial,sans-serif")
    marca['_PESO'] = str(tip.get('peso_titular', 400))
    Ctx.marca, Ctx.tok = marca, tokens(marca)
    Ctx.email_id = str(ficha.get('email', 'e0')).lower()
    Ctx.carpeta = fpath.parent
    # De dónde sale el envío. No siempre es n8n: si el cliente envía con ActiveCampaign, Brevo
    # o Mailchimp y esto se queda fijo en «n8n», el cliente ve en sus analíticas todo el tráfico
    # atribuido a una herramienta que no usa. Se pone en marca.json → utm_source.
    Ctx.utm = ('utm_source=' + urllib.parse.quote(marca.get('utm_source', 'n8n')) +
               '&utm_medium=email&utm_campaign=' + urllib.parse.quote(marca.get('utm_campaign', 'secuencia')))
    Ctx.tok.update({'F_TIT': marca['_F_TIT'], 'F_TXT': marca['_F_TXT'], 'TIT_PESO': marca['_PESO'],
                    'F_TIT_MSO': tip.get('titulares_mso', 'Georgia,serif'),
                    'CITA_ESTILO': 'italic' if tip.get('cita_cursiva', True) else 'normal'})
    # Dirección de diseño (parametros.md §5): cambia las proporciones de la escala, el ritmo y el radio.
    estilo = tip.get('estilo') or ('display' if tip.get('titulares_mayusculas') else
                                   ('editorial' if 'serif' in marca['_F_TIT'].lower() else 'moderno'))
    if estilo not in ESTILOS:
        WARN.append(f'tipografia.estilo "{estilo}" no existe: se usa "editorial" ({", ".join(ESTILOS)}).')
        estilo = 'editorial'
    Ctx.tok.update(escala(estilo))
    Ctx.tok.update({'F_CITA': marca['_F_TXT'], 'CITA_TAM': '18px', 'CITA_PESO': '500'} if estilo == 'display'
                   else {'F_CITA': marca['_F_TIT'], 'CITA_TAM': '19px', 'CITA_PESO': '400'})
    Ctx.estilo = estilo
    gf = tip.get('google_fonts')
    Ctx.tok['FUENTES_HTML'] = (f'<!--[if !mso]><!--><link href="https://fonts.googleapis.com/css2?{gf}&display=swap" rel="stylesheet"><!--<![endif]-->' if gf else '')

    if not marca.get('legal', {}).get('url_baja') and not marca.get('remitente', {}).get('email'):
        ERRORES.append('Sin forma de baja: marca.json necesita legal.url_baja o remitente.email (legal-y-envio.md §1).')
    if not marca.get('remitente', {}).get('nombre'):
        ERRORES.append('marca.json sin remitente.nombre: la secuencia la firma una persona (copy-email.md §1).')
    # [FALTA] solo bloquea en lo que se imprime en cada email: remitente, legal, motivo, logo. En el resto, aviso.
    obligatorios = json.dumps({k: marca.get(k) for k in ('remitente', 'legal', 'motivo', 'logo', 'logo_texto', 'web')}, ensure_ascii=False)
    pendientes = sorted(set(re.findall(r'\[FALTA[^\]]*\]', obligatorios)))
    if pendientes:
        ERRORES.append('marca.json con datos pendientes que salen en el email: ' + ', '.join(pendientes))
    otros = sorted(set(re.findall(r'\[FALTA[^\]]*\]', json.dumps(marca, ensure_ascii=False))) - set(pendientes))
    if otros:
        WARN.append('marca.json con datos pendientes (no salen en el email): ' + ', '.join(otros))
    if not marca.get('motivo'):
        ERRORES.append('marca.json sin "motivo" (por qué recibe el email): es obligatorio en el pie (legal-y-envio.md §1).')
    if not marca.get('campos_formulario'):
        WARN.append('marca.json sin campos_formulario: no se pueden comprobar las variables [[campo]].')
    revisa(ficha)

    tpl = TEMPLATE.read_text(encoding='utf-8')
    mods = list(re.finditer(r'<!-- MODULO: ([\w-]+) -->\n?(.*?)<!-- /MODULO: \1 -->\n?', tpl, re.S))
    raw = {x.group(1): x.group(2) for x in mods}
    head, wrap, tail = tpl[:mods[0].start()], tpl[mods[0].end():mods[1].start()], tpl[mods[-1].end():]

    specs = [s for s in ficha['modulos'] if s['tipo'] not in ('cabecera', 'pie')]
    if not any(s['tipo'] == 'firma' for s in specs):
        specs.append({'tipo': 'firma'})
    else:
        firmas = [s for s in specs if s['tipo'] == 'firma']
        specs = [s for s in specs if s['tipo'] != 'firma'] + firmas[:1]
    specs = [{'tipo': 'cabecera'}] + specs + [{'tipo': 'pie'}]
    for s in specs:
        if s['tipo'] not in raw:
            ERRORES.append(f'Bloque desconocido: {s["tipo"]} (diseno.md §3).')

    asunto, pre = ficha.get('asunto', ''), ficha.get('preheader', '')
    def largo(t):
        return len(RX_VAR.sub('xxxxxx', t))
    a_min, a_max = LIM['asunto']['min'], LIM['asunto']['max']
    p_min, p_max = LIM['preheader']['min'], LIM['preheader']['max']
    for nombre, t in [('Asunto', asunto)] + [(f'Alternativa {i}', a) for i, a in enumerate(ficha.get('asunto_alternativas', []), 1)]:
        if not a_min <= largo(t) <= a_max:
            WARN.append(f'{nombre} de {largo(t)} caracteres ({a_min}-{a_max}): "{t}"')
        if t.rstrip().endswith('.') or t.count('!') > 0 or re.search(r'\b[A-ZÁÉÍÓÚÑ]{5,}\b', t):
            WARN.append(f'{nombre} con punto final, exclamación o mayúsculas: "{t}"')
        for var in RX_VAR.finditer(t):
            if var.group(1) != 'nombre':
                ERRORES.append(f'{nombre} usa [[{var.group(1)}]]: en el asunto solo va el nombre (parametros.md §3).')
    if not p_min <= largo(pre) <= p_max:
        WARN.append(f'Preheader de {largo(pre)} caracteres ({p_min}-{p_max}).')
    # claridad (copy-email.md §0): frases de enigma y frases demasiado largas
    enigmas = (r'lo que nadie|nadie te cuenta|el secreto|la trampa|invisible|silencios[oa]|esa sensaci[oó]n|ya sabes (qu[eé]|de qu[eé])|'
               r'lo que pasa (a|cuando)|esto te va a|te sorprender|una cosa m[aá]s|adivina|lo tuyo\b|eso que\b')
    piezas = [('Asunto', asunto), ('Preheader', pre)] + [(f"{m['tipo']}.{k}", v) for m in ficha['modulos']
              for k, v in list(m.get('datos', {}).items()) + [kv for x in m.values() if isinstance(x, list) for it in x for kv in it.items()]
              if isinstance(v, str) and not k.endswith(RAW)]
    for nombre, t in piezas:
        # Los ** de la negrita se quitan ANTES de partir en frases: si el punto final queda
        # dentro («…no funcione.**»), detrás del punto no hay espacio, las dos frases se cuentan
        # como una y salta un aviso falso de frase larga.
        limpio = RX_VAR.sub('', RX_LINK.sub(r'\1', t)).replace('**', '')
        e = re.search(enigmas, limpio, re.I)
        if e:
            WARN.append(f'{nombre}: «{e.group(0)}» suena a enigma; di la cosa por su nombre (copy-email.md §0): "{limpio[:60]}"')
        if '—' in limpio or '–' in limpio:
            WARN.append(f'{nombre}: raya larga; usa punto, coma o dos puntos (diseno.md §1.1): "{limpio[:60]}"')
        # La ela geminada del catalán (l·l, «excel·lent», «sol·licitud») es ortografía, no un separador.
        if re.sub(r'(?i)l·l', 'll', limpio).count('·') > 1:
            WARN.append(f'{nombre}: varios «·»; se reservan para el pie legal (diseno.md §1.1).')
        for frase in re.split(r'(?<=[.!?])\s+', limpio):
            if len(frase.split()) > 30:
                WARN.append(f'{nombre}: frase de {len(frase.split())} palabras (máx. 30, copy-email.md §0.5): "{frase[:60]}…"')
    if asunto and pre and asunto.lower()[:22] in pre.lower():
        WARN.append('El preheader repite el asunto: tiene que completarlo.')

    if ERRORES:
        for e in ERRORES:
            print('ERROR  ', e)
        for w in WARN:
            print('AVISO  ', w)
        print('No se ha generado nada: corrige la ficha o la marca y vuelve a ejecutar.')
        sys.exit(1)

    docs = {}
    for modo in ('html', 'muestra'):
        glob = {'PREHEADER': ficha.get('preheader', ''), 'ASUNTO': ficha.get('asunto', '').replace('"', '”')}
        cuenta, cuerpo = {}, []
        for s in specs:
            cuenta[s['tipo']] = cuenta.get(s['tipo'], 0) + 1
            cuerpo.append(render(s['tipo'], s, raw[s['tipo']], cuenta[s['tipo']], glob, modo))
        doc = fill(head, glob, 'head', modo) + fill(raw['preheader'], glob, 'pre', modo) + fill(wrap, glob, 'wrap', modo) + ''.join(cuerpo) + fill(tail, glob, 'tail', modo)
        doc = re.sub(r'<!-- (?:/?(?:MODULO|SI|REPETIR): [\w-]+) -->\n?', '', doc)
        doc = re.sub(r'\n{2,}', '\n', doc)
        docs[modo] = doc
    left = sorted(set(re.findall(r'\{\{[A-Z0-9_]+\}\}', docs['html'])))
    if left:
        print('ERROR   Marcadores sin rellenar: ' + ', '.join(left))
        sys.exit(1)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(docs['html'], encoding='utf-8')
    (out.parent / 'email-muestra.html').write_text(docs['muestra'], encoding='utf-8')
    (out.parent / 'email.txt').write_text(texto_plano(specs), encoding='utf-8')
    kb = len(docs['html'].encode('utf-8')) / 1024
    print(f'Email montado: {out} ({kb:.1f} KB) · tipo {ficha.get("tipo")} · bloques: ' + ' → '.join(s['tipo'] for s in specs))
    print(f'Asunto: {vars_a_expr(asunto, False)}\nPreheader: {vars_a_expr(pre, False)}')
    print(f'Texto plano: {out.parent / "email.txt"} · muestra para previews: {out.parent / "email-muestra.html"}')
    print(f'Colores: acento texto {Ctx.tok["C_ACENTO_TXT"]} · botón {Ctx.tok["C_BOTON"]}/{Ctx.tok["C_BOTON_TXT"]} · oscuro acento {Ctx.tok["D_ACENTO"]}')
    for w in WARN:
        print('AVISO  ', w)

if __name__ == '__main__':
    main()
