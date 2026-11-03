#!/usr/bin/env python3
"""Control de calidad de un email de la secuencia (HTML para n8n).

Uso: python3 qa_email.py eN/email.html [--offline] [--tecnico]
--offline: no comprueba que las imágenes respondan.
--tecnico: omite copy-auditoria.md y fuentes.md (solo para probar la plantilla).
Sale con código 1 si hay algún ERROR.
"""
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from textos_idioma import textos  # noqa: E402

# Windows: que tildes, eñes y emojis no rompan la salida (la consola usa cp1252).
for _flujo in (sys.stdout, sys.stderr):
    try:
        _flujo.reconfigure(encoding='utf-8')
    except Exception:
        pass


ERR, WARN, OK = [], [], []
def err(m): ERR.append(m)
def warn(m): WARN.append(m)
def ok(m): OK.append(m)

def _hex(c):
    m = re.fullmatch(r'#([0-9a-f]{3}|[0-9a-f]{6})', (c or '').strip().lower())
    if not m:
        return None
    h = m.group(1)
    return ''.join(x * 2 for x in h) if len(h) == 3 else h

def _lum(h):
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    rgb = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in rgb]
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]

def contrast(a, b):
    la, lb = sorted([_lum(a), _lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)

def sget(style, prop):
    m = re.findall(r'(?:^|;)\s*' + re.escape(prop) + r'\s*:\s*([^;]+)', style or '', re.I)
    return m[-1].strip() if m else None

VOID = {'img', 'br', 'hr', 'meta', 'link', 'input', 'source', 'col', 'area', 'base', 'wbr'}

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.imgs, self.links, self.text, self.pairs, self.meta = [], [], [], [], {}, {}
        self.tables = self.tables_bad = 0
        self.html_lang = None
        self.forbidden, self.pure = set(), set()
        self._a = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        st = a.get('style', '') or ''
        if tag == 'html':
            self.html_lang = a.get('lang')
        if tag == 'meta' and a.get('name'):
            self.meta[a['name'].lower()] = a.get('content', '')
        if tag == 'table':
            self.tables += 1
            self.tables_bad += a.get('role') not in ('presentation', 'none')
        if tag == 'img':
            self.imgs.append(a)
        if tag == 'a' and 'href' in a:
            self._a = {'href': a['href'], 'text': ''}
            self.links.append(self._a)
        for bad in ('display:flex', 'display:grid', 'position:absolute', 'position:fixed', 'box-shadow'):
            if bad in st.replace(' ', '').lower():
                self.forbidden.add(bad)
        bg = sget(st, 'background-color') or a.get('bgcolor')
        if bg and _hex(bg) in ('ffffff', '000000'):
            self.pure.add(bg)
        if tag not in VOID:
            self.stack.append({'tag': tag, 'color': sget(st, 'color'), 'bg': bg, 'size': sget(st, 'font-size'),
                               'weight': sget(st, 'font-weight'), 'hidden': 'display:none' in st.replace(' ', '').lower()})

    def handle_endtag(self, tag):
        if tag == 'a':
            self._a = None
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]['tag'] == tag:
                del self.stack[i:]
                break

    def near(self, k):
        for n in reversed(self.stack):
            if n.get(k):
                return n[k]

    def handle_data(self, data):
        t = data.strip()
        if not t or any(n['hidden'] for n in self.stack) or any(n['tag'] in ('style', 'title') for n in self.stack):
            return
        self.text.append(t)
        if self._a is not None:
            self._a['text'] += t
        col, bg = _hex(self.near('color')), _hex(self.near('bg'))
        if not col or not bg:
            return
        try:
            px = float(re.sub(r'[^0-9.]', '', self.near('size') or '16') or 16)
        except ValueError:
            px = 16
        w = self.near('weight') or '400'
        bold = w in ('bold', 'bolder') or (w.isdigit() and int(w) >= 700)
        need = 3.0 if (px >= 24 or (bold and px >= 18.66) or not re.search(r'[0-9A-Za-zÀ-ÿ]', t)) else 4.5
        cr = contrast(col, bg)
        if cr < need:
            self.pairs.setdefault((col, bg, px, bold), (cr, need, t[:40]))


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = Path(sys.argv[1])
    d = path.parent
    raw = path.read_text(encoding='utf-8')
    kb = len(raw.encode('utf-8')) / 1024
    ficha = json.loads((d / 'ficha.json').read_text(encoding='utf-8')) if (d / 'ficha.json').exists() else {}
    marca = {}
    for x in (d, d.parent, d.parent.parent):
        if (x / 'marca.json').exists():
            marca = json.loads((x / 'marca.json').read_text(encoding='utf-8'))
            break
    tipo = ficha.get('tipo', '')

    LIM = json.loads((Path(__file__).resolve().parent.parent / 'assets' / 'limites.json').read_text(encoding='utf-8'))
    if kb > LIM['peso_kb']['error']:
        err(f'Peso {kb:.1f} KB: máximo {LIM["peso_kb"]["error"]} KB (Gmail recorta a ~102 KB). parametros.md §6.')
    elif kb > LIM['peso_kb']['aviso']:
        warn(f'Peso {kb:.1f} KB: por encima de {LIM["peso_kb"]["aviso"]} KB.')
    else:
        ok(f'Peso {kb:.1f} KB')

    if '--tecnico' not in sys.argv:
        if not (d / 'copy-auditoria.md').exists():
            err('Falta copy-auditoria.md junto al email (compuerta Ogilvy, ogilvy-email.md §3).')
        if not ((d / 'fuentes.md').exists() or (d.parent / 'fuentes.md').exists()):
            err('Falta fuentes.md en la carpeta de la secuencia (secuencia.md §5).')
    txt = d / 'email.txt'
    if not txt.exists():
        err('Falta email.txt (versión en texto plano): vuelve a montar con build_email.py.')
    else:
        t = txt.read_text(encoding='utf-8')
        if '<' in re.sub(r'«|»|<https?://[^>]+>', '', t) and re.search(r'</?[a-z]+[ >]', t):
            err('email.txt contiene etiquetas HTML.')
        tx = textos(marca)
        if not re.search(re.escape(tx['baja']) + r':\s*(https://|mailto:|\{\{)', t, re.I):
            err(f'email.txt sin la línea «{tx["baja"]}: <enlace>».')
        if tx['comunicacion'].rstrip('.').lower() not in t.lower():
            err(f'email.txt sin la frase «{tx["comunicacion"]}» en el pie.')
        ok('Versión en texto plano presente')

    # marcadores y variables
    marcadores = sorted(set(re.findall(r'\{\{\s*[A-Z0-9_]+\s*\}\}', raw)))
    if marcadores:
        err('Marcadores sin rellenar: ' + ', '.join(marcadores[:10]))
    if re.search(r'\[\[|\]\]', raw):
        err('Quedan variables [[...]] sin convertir.')
    if re.search(r'\[FALTA[^\]]*\]', raw):
        err('Datos pendientes [FALTA: …] en el email.')
    pre = marca.get('n8n_prefijo', '$json')
    exprs = re.findall(r'\{\{(.*?)\}\}', raw)
    malas = [e for e in exprs if not re.match(r'\s*[$]', e) and not re.match(r'\s*[A-Z0-9_]+\s*$', e)]
    if malas:
        err('Llaves {{ }} que no son expresiones de n8n: ' + ' | '.join(m[:40] for m in malas[:5]))
    if exprs and not any(pre in e for e in exprs):
        warn(f'Las expresiones no usan el prefijo de marca.json ({pre}).')
    if re.search(r'<!--\s*/?(MODULO|SI|REPETIR)', raw):
        warn('Quedan comentarios de desarrollo en el HTML.')

    p = P()
    p.feed(raw)
    tx = textos(marca)
    if p.html_lang != tx['lang']:
        err(f'<html> sin lang="{tx["lang"]}".')
    for m in ('viewport', 'color-scheme', 'supported-color-schemes'):
        if m not in p.meta:
            err(f'Falta <meta name="{m}">.')
    if 'prefers-color-scheme' not in raw:
        err('Sin estilos de modo oscuro.')
    style = ''.join(re.findall(r'<style>(.*?)</style>', raw, re.S))
    if len(style) > 8000:
        err(f'<style> de {len(style)} caracteres: Gmail lo descarta por encima de 8.192.')
    if p.tables_bad:
        err(f'{p.tables_bad} de {p.tables} tablas sin role="presentation".')
    else:
        ok(f'{p.tables} tablas con role="presentation"')

    seen = set()
    for im in p.imgs:
        src = im.get('src', '')
        if 'alt' not in im:
            err(f'Imagen sin alt: {src[:80]}')
        if not im.get('width'):
            err(f'Imagen sin atributo width: {src[:80]}')
        if re.search(r'\.(svg|webp)(\?|$)', src, re.I):
            err(f'Formato no soportado en email (SVG/WebP): {src[:80]}')
        if not src.startswith('https://'):
            err(f'Imagen sin URL https pública: {src[:80]}')
        else:
            seen.add(src)
    if '--offline' not in sys.argv:
        for src in sorted(seen):
            try:
                req = urllib.request.Request(src, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=12) as r:
                    ln = int(r.headers.get('Content-Length') or 0)
                    if r.status != 200:
                        err(f'Imagen responde {r.status}: {src}')
                    elif ln > 250 * 1024:
                        warn(f'Imagen de {ln // 1024} KB (máx. 250): {src}')
            except Exception as e:
                err(f'Imagen no accesible ({str(e)[:40]}): {src}')
        ok(f'{len(seen)} imágenes comprobadas')

    # la baja es el enlace cuyo texto es exactamente «Darme de baja» (lo genera el pie de la plantilla)
    baja = [l for l in p.links if re.fullmatch(r'\s*' + re.escape(tx['baja']) + r'\s*', l['text'], re.I)]
    if not baja:
        err(f'Falta el enlace «{tx["baja"]}» del pie (LSSI art. 21 y legal-y-envio.md §1).')
    elif not re.match(r'(https://|mailto:|\{\{)', baja[0]['href']):
        err(f'Enlace de baja no válido: {baja[0]["href"][:60]}')
    else:
        ok('Enlace de baja presente')
    if tx['comunicacion'].rstrip('.').lower() not in ' '.join(p.text).lower():
        err(f'El pie no dice «{tx["comunicacion"]}» (legal-y-envio.md §1).')
    pie_links = {id(l) for l in baja} | {id(l) for l in p.links if re.fullmatch(r'\s*' + re.escape(tx['privacidad']) + r'\s*', l['text'], re.I)}
    destinos = set()
    doms = marca.get('dominios_utm', [])
    for l in p.links:
        h = l['href'].strip()
        if h in ('', '#') or h.startswith('javascript'):
            err(f'Enlace vacío o "#": {h!r}')
        elif not re.match(r'(https://|mailto:|tel:|\{\{)', h):
            err(f'Enlace no https: {h[:80]}')
        if id(l) in pie_links or 'utm_content=' in h and '-logo' in h:
            continue
        if h.startswith('https://') and not re.search(r'utm_content=e\w*-(logo)\b', h):
            destinos.add(re.sub(r'[?#].*$', '', h).rstrip('/'))
        if doms and h.startswith('https://') and any(x in h for x in doms) and 'utm_source=' not in h:
            warn(f'Enlace al cliente sin UTM: {h[:80]}')
    if len(destinos) > 1:
        warn('Varios destinos de CTA (uno por email): ' + ' | '.join(sorted(destinos)))

    if p.pairs:
        for (c, b, px, bold), (cr, need, s) in p.pairs.items():
            err(f'Contraste {cr:.2f}:1 (mínimo {need}) #{c} sobre #{b} a {px:g}px: "{s}"')
    else:
        ok('Contraste en modo claro OK')

    text = ' '.join(p.text)
    if len(text) < LIM['texto_minimo_caracteres'] and tipo not in LIM['tipos_sin_texto_minimo']:
        warn(f'Solo {len(text)} caracteres de texto visible (≥ {LIM["texto_minimo_caracteres"]}).')
    if re.search(r'\b(vos|tenés|querés|podés|mirá|hacé|contanos|escribinos|reservá|agendá|dejá|sabés)\b', text, re.I):
        err('Voseo detectado: español de España.')
    tells = (r'sumérgete|descubre la magia|experiencia (inolvidable|única|de ensueño)|de ensueño|vive el sueño|un mundo de posibilidades|'
             r'\bincreíble(s)?\b|sin igual|a otro nivel|vertiginoso mundo|no es solo .{1,30}, es |te esperamos!|'
             r'sin fisuras|impulsa tu|transforma tu|revoluciona tu|potencia tu|lleva tu .{1,20} al siguiente nivel')
    for m in sorted(set(x.group(0).lower() for x in re.finditer(tells, text, re.I))):
        err(f'AI-tell o superlativo vacío (copy-email.md §3): "{m}"')
    for c in marca.get('claims_prohibidos', []):
        if re.search(re.escape(c), text, re.I):
            err(f'Claim prohibido en marca.json: "{c}"')
    # jerarquía: el titular tiene que estar a la distancia que fija limites.json (parametros.md §5)
    jer = LIM.get('jerarquia')
    if jer:
        h1s = [int(m) for m in re.findall(r'<h1[^>]*font-size:(\d+)px', raw)]
        cuerpo = jer['cuerpo_px']
        h1_min = min(e['h1'] for e in jer['estilos'].values())
        for n in h1s:
            if n / cuerpo < h1_min:
                warn(f'Titular de {n}px con cuerpo de {cuerpo}px: menos de {h1_min}× (parametros.md §5).')
        # contraste por elemento, no solo el mínimo WCAG
        cmin = jer['contraste_minimo']
        mp = re.search(r'<body[^>]*background-color:(#[0-9A-Fa-f]{3,6})', raw)
        fondo = _hex(mp.group(1)) if mp else None
        if fondo:
            for patron, clave, nombre in ((r'<h1[^>]*;color:(#[0-9A-Fa-f]{3,6})', 'titular', 'Titular'),
                                          (r'class="t-cuerpo"[^>]*;color:(#[0-9A-Fa-f]{3,6})', 'cuerpo', 'Cuerpo'),
                                          (r'class="t-suave"[^>]*;color:(#[0-9A-Fa-f]{3,6})', 'suave', 'Texto suave')):
                m2 = re.search(patron, raw)
                c = _hex(m2.group(1)) if m2 else None
                if c and contrast(c, fondo) < cmin[clave]:
                    warn(f'{nombre} con contraste {contrast(c, fondo):.1f}:1 sobre el papel: mínimo {cmin[clave]}:1 (parametros.md §5).')
        h2s = {int(m) for m in re.findall(r'<h2[^>]*font-size:(\d+)px', raw)}
        for n in h2s:
            if n / cuerpo < jer['salto_minimo']:
                warn(f'Subtítulo de {n}px con cuerpo de {cuerpo}px: salto menor de {jer["salto_minimo"]}× (parametros.md §5).')
            if h1s and n > min(h1s) / jer['salto_minimo']:
                warn(f'Subtítulo de {n}px demasiado cerca del titular de {min(h1s)}px (parametros.md §5).')
    if '—' in text or '–' in text:
        warn('Raya larga en el texto visible: usa punto, coma o dos puntos (diseno.md §1.1).')
    puntos = re.sub(r'(?i)l·l', 'll', text).count('·')   # sin contar la ela geminada del catalán
    if puntos > 3:
        warn(f'{puntos} veces «·» en el email: se reserva para el pie legal y el remitente (diseno.md §1.1).')
    if '!!' in text or re.search(r'\b[A-ZÁÉÍÓÚÑ]{4,}(\s+[A-ZÁÉÍÓÚÑ]{4,}){3,}\b', text):
        warn('Exclamaciones en cadena o frases enteras en mayúsculas.')
    for h in re.findall(r'<h1[^>]*>(.*?)</h1>', raw, re.S):
        if re.sub(r'<[^>]+>', '', h).strip().endswith('.'):
            warn('H1 con punto final.')
    if p.forbidden:
        warn('CSS poco fiable en email: ' + ', '.join(sorted(p.forbidden)))
    if p.pure:
        warn('Fondos blanco/negro puros (usa #FFFFFE / #141414): ' + ', '.join(sorted(p.pure)))

    print(f'\nQA email · {path}')
    print('=' * 60)
    for m in ERR:
        print('ERROR  ', m)
    for m in WARN:
        print('AVISO  ', m)
    for m in OK:
        print('OK     ', m)
    print('=' * 60)
    print(f'{len(ERR)} errores · {len(WARN)} avisos')
    sys.exit(1 if ERR else 0)


if __name__ == '__main__':
    main()
