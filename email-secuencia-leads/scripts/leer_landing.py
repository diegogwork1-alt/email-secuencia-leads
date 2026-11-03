#!/usr/bin/env python3
"""Lee la landing de un cliente y saca lo que necesita la secuencia de emails.

Uso: python3 leer_landing.py <URL o archivo.html> --salida <carpeta> [--base https://dominio/ruta]
     (--base: con un archivo local, para resolver rutas relativas de logos, enlaces y CSS)

Deja en <carpeta>:
  landing.json  datos estructurados
  landing.md    resumen legible: textos, formulario, casillas legales, identidad visual

Qué extrae:
- Textos: title, description, H1-H3, párrafos, listas (para contenido de valor, FAQ, testimonios, proceso).
- Formulario: <form> nativo y formularios Tally embebidos (los descarga de tally.so y lee preguntas,
  opciones, campos ocultos y casillas). Typeform, HubSpot y otros se detectan pero no se leen.
- Casillas legales: si hay casilla de comunicaciones comerciales independiente, combinada con la de
  privacidad, no encontrada o no verificable (legal-y-envio.md §1).
- Agenda y contacto: Calendly/Cal.com/TidyCal, wa.me, tel:, mailto:, enlace a política de privacidad.
- Identidad visual: candidatos a logo, variables CSS de color, colores más usados, fuentes y Google Fonts.
Solo lectura. No inventa nada: lo que no encuentra lo deja vacío.
"""
import json
import re
import sys
import unicodedata
import urllib.parse
import urllib.request
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

# Windows: que tildes, eñes y emojis no rompan la salida (la consola usa cp1252).
for _flujo in (sys.stdout, sys.stderr):
    try:
        _flujo.reconfigure(encoding='utf-8')
    except Exception:
        pass


UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36'}
RX_COMERCIAL = re.compile(r'comunicaciones? comercial|informaci[oó]n comercial|publicidad|promocion|newsletter|bolet[ií]n|novedades|ofertas|'
                          r'enviar(me|te|le)? (informaci|comunicaci|contenido|emails?|correos?)|recibir (informaci|comunicaci|contenido|emails?|correos?|novedades)', re.I)
RX_PRIVACIDAD = re.compile(r'privacidad|protecci[oó]n de datos|aviso legal|t[eé]rminos', re.I)


def fetch(url, timeout=25):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            enc = r.headers.get_content_charset() or 'utf-8'
        return raw.decode(enc, errors='ignore')
    except Exception:
        # algunos hostings (Squarespace, Cloudflare) rechazan urllib: segundo intento con curl
        import subprocess
        out = subprocess.run(['curl', '-sL', '-m', str(timeout), '-A', UA['User-Agent'], '-w', '\n%{http_code}', url],
                             capture_output=True, timeout=timeout + 5)
        body, _, code = out.stdout.decode('utf-8', errors='ignore').rpartition('\n')
        if code.strip() != '200':
            raise RuntimeError(f'{url} responde {code.strip() or "sin respuesta"}')
        return body


VACIAS = {'que', 'de', 'la', 'el', 'los', 'las', 'tu', 'tus', 'en', 'con', 'a', 'y', 'o', 'es', 'esta', 'este', 'esto', 'un', 'una', 'para',
          'por', 'como', 'cual', 'cuanto', 'cuanta', 'ahora', 'mismo', 'te', 'se', 'lo', 'al', 'del', 'si', 'ha', 'has', 'hay', 'mas'}
_usados = set()

def slug(txt, maxlen=24):
    """Nombre de campo corto para n8n: 'nombre', 'email', 'telefono' para los datos de contacto;
    para las preguntas, las 2-3 palabras con contenido ('deuda_acumulas', 'situacion_consumo')."""
    t = unicodedata.normalize('NFKD', txt).encode('ascii', 'ignore').decode().lower()
    t = re.sub(r'[^a-z0-9]+', ' ', t).strip()
    fijos = [('empresa', r'\b(empresa|compania|negocio)\b'), ('nombre', r'^(nombre|name)( completo| y apellidos?)?$'),
             ('email', r'\b(correo|e ?mail)\b'), ('telefono', r'\b(telefono|movil|phone|whatsapp)\b'),
             ('ciudad', r'\b(ciudad|localidad|poblacion|municipio)\b'), ('provincia', r'\bprovincia\b')]
    out = None
    for nombre, rx in fijos:
        if re.search(rx, t):
            out = nombre
            break
    if not out:
        palabras = [w for w in t.split() if w not in VACIAS and len(w) > 2]
        out = '_'.join(palabras[:3])[:maxlen].strip('_') or 'campo'
    base, n = out, 2
    while out in _usados:
        out, n = f'{base}_{n}', n + 1
    _usados.add(out)
    return out


class Landing(HTMLParser):
    SKIP = {'script', 'style', 'noscript', 'svg', 'template'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.title = ''
        self.meta = {}
        self.heads = []
        self.parrafos = []
        self.items = []
        self.links = []
        self.imgs = []
        self.forms = []
        self.embeds = []
        self.styles = []
        self.font_links = []
        self._buf = None
        self._buf_tag = None
        self._link = None
        self._form = None
        self._label = None
        self._last_checkbox = None

    def handle_starttag(self, tag, attrs):
        a = {k: (v or '') for k, v in attrs}
        if tag not in ('br', 'img', 'input', 'meta', 'link', 'hr', 'source'):
            self.stack.append(tag)
        if a.get('style'):
            self.styles.append(a['style'])
        if tag == 'meta' and a.get('name'):
            self.meta[a['name'].lower()] = a.get('content', '')
        if tag == 'meta' and a.get('property'):
            self.meta[a['property'].lower()] = a.get('content', '')
        if tag == 'link' and 'fonts.googleapis.com' in a.get('href', ''):
            self.font_links.append(a['href'])
        if tag == 'link' and 'stylesheet' in a.get('rel', '') and a.get('href'):
            self.embeds.append(('css', a['href']))
        if tag in ('h1', 'h2', 'h3', 'p', 'li', 'blockquote', 'figcaption', 'summary', 'dt', 'dd', 'button'):
            self._buf, self._buf_tag = [], tag
        if tag == 'a':
            self._link = {'href': a.get('href', ''), 'text': []}
        if tag == 'img':
            self.imgs.append({'src': a.get('src') or a.get('data-src', ''), 'alt': a.get('alt', ''), 'class': a.get('class', ''),
                              'id': a.get('id', ''), 'width': a.get('width', ''), 'height': a.get('height', ''),
                              'en_header': 'header' in self.stack or 'nav' in self.stack})
        for k in ('data-tally-src', 'data-tally-open', 'src', 'data-src', 'data-url', 'href'):
            v = a.get(k, '')
            if k == 'data-tally-open' and v:
                v = f'https://tally.so/r/{v}'
            mt = re.search(r'#tally-open=([A-Za-z0-9]+)', v)
            if mt:
                v = f'https://tally.so/r/{mt.group(1)}'
            if re.search(r'tally\.so/(embed|r)/|typeform\.com|hsforms|hubspot|calendly\.com|cal\.com/|tidycal\.com|jotform|forms\.gle|google\.com/forms', v):
                self.embeds.append(('embed', v))
        if tag == 'form':
            self._form = {'action': a.get('action', ''), 'campos': [], 'casillas': []}
        if tag == 'label':
            self._label = []
        if tag in ('input', 'select', 'textarea') and self._form is not None:
            t = a.get('type', tag)
            if t in ('hidden', 'submit', 'button'):
                return
            campo = {'tipo': t, 'name': a.get('name', ''), 'placeholder': a.get('placeholder', ''), 'required': 'required' in a}
            if t == 'checkbox':
                self._last_checkbox = campo
                self._form['casillas'].append(campo)
                campo['texto'] = ''
            else:
                self._form['campos'].append(campo)

    def handle_endtag(self, tag):
        if tag in self.stack:
            while self.stack and self.stack.pop() != tag:
                pass
        if self._buf is not None and tag == self._buf_tag:
            txt = re.sub(r'\s+', ' ', ''.join(self._buf)).strip()
            if txt:
                if tag in ('h1', 'h2', 'h3'):
                    self.heads.append((tag, txt))
                elif tag in ('li', 'dt', 'dd', 'summary'):
                    self.items.append(txt)
                elif tag != 'button':
                    self.parrafos.append(txt)
            self._buf = None
        if tag == 'a' and self._link:
            self._link['text'] = re.sub(r'\s+', ' ', ''.join(self._link['text'])).strip()
            self.links.append(self._link)
            self._link = None
        if tag == 'label' and self._label is not None:
            txt = re.sub(r'\s+', ' ', ''.join(self._label)).strip()
            if self._last_checkbox is not None and not self._last_checkbox.get('texto'):
                self._last_checkbox['texto'] = txt
            elif self._form is not None and self._form['campos'] and txt and not self._form['campos'][-1].get('label'):
                self._form['campos'][-1]['label'] = txt
            self._label = None
        if tag == 'form' and self._form is not None:
            self.forms.append(self._form)
            self._form = None
            self._last_checkbox = None

    def handle_data(self, data):
        if any(s in self.SKIP for s in self.stack):
            if self.stack and self.stack[-1] == 'style':
                self.styles.append(data)
            if self.stack and self.stack[-1] == 'title':
                self.title += data
            return
        if self.stack and self.stack[-1] == 'title':
            self.title += data
            return
        if self._buf is not None:
            self._buf.append(data)
        if self._link is not None:
            self._link['text'].append(data)
        if self._label is not None:
            self._label.append(data)


def leer_tally(url):
    m = re.search(r'tally\.so/(?:embed|r)/([A-Za-z0-9]+)', url)
    if not m:
        return None
    fid = m.group(1)
    try:
        html = fetch(f'https://tally.so/r/{fid}')
    except Exception as e:
        return {'id': fid, 'error': str(e)[:80]}
    mm = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    if not mm:
        return {'id': fid, 'error': 'sin __NEXT_DATA__'}
    pp = json.loads(mm.group(1)).get('props', {}).get('pageProps', {})
    preguntas, casillas, ocultos = [], [], []
    actual = None
    for b in pp.get('blocks', []):
        t, p = b.get('type'), b.get('payload', {}) or {}
        if t == 'TITLE':
            txt = ' '.join(''.join(x if isinstance(x, str) else '' for x in seg) for seg in p.get('safeHTMLSchema', [])).strip()
            actual = {'pregunta': txt, 'tipo': None, 'opciones': [], 'obligatoria': False}
            preguntas.append(actual)
        elif t in ('MULTIPLE_CHOICE_OPTION', 'DROPDOWN_OPTION', 'RANKING_OPTION'):
            if actual is not None:
                actual['tipo'] = 'opciones'
                actual['opciones'].append(p.get('text', '').strip())
                actual['obligatoria'] = actual['obligatoria'] or p.get('isRequired', False)
        elif t == 'CHECKBOX':
            casillas.append({'texto': p.get('text', '').strip(), 'obligatoria': p.get('isRequired', False)})
            if actual is not None and not actual['pregunta']:
                preguntas.remove(actual)
                actual = None
        elif t.startswith('INPUT_') or t in ('TEXTAREA', 'RATING', 'LINEAR_SCALE', 'FILE_UPLOAD', 'MATRIX'):
            if actual is not None:
                actual['tipo'] = t.replace('INPUT_', '').lower()
                actual['obligatoria'] = p.get('isRequired', False)
        elif t == 'HIDDEN_FIELDS':
            ocultos = [h.get('name') for h in p.get('hiddenFields', [])]
        elif t == 'HEADING_2' or t == 'HEADING_3':
            pass
    preguntas = [q for q in preguntas if q['pregunta'] and q['tipo']]
    for q in preguntas:
        q['campo_sugerido'] = slug(q['pregunta'])
    return {'id': fid, 'nombre': pp.get('name', ''), 'preguntas': preguntas, 'casillas': casillas, 'campos_ocultos': ocultos}


def analiza_consentimiento(casillas, verificable):
    if not verificable:
        return 'no_verificable', 'El formulario es externo y no se ha podido leer: comprobarlo a mano.'
    comerciales = [c for c in casillas if RX_COMERCIAL.search(c.get('texto', ''))]
    for c in comerciales:
        if not RX_PRIVACIDAD.search(c['texto']) and not c.get('obligatoria'):
            return 'independiente', f'Casilla de comunicaciones independiente: «{c["texto"][:160]}»'
    for c in comerciales:
        return 'combinada', f'La autorización comercial va en la misma casilla que la privacidad u obligatoria: «{c["texto"][:200]}»'
    if casillas:
        return 'no_encontrada', 'Hay casillas pero ninguna pide consentimiento para comunicaciones: ' + ' | '.join(f'«{c["texto"][:120]}»' for c in casillas)
    return 'no_encontrada', 'No hay ninguna casilla en el formulario.'


def colores(css_text):
    vars_ = {}
    for m in re.finditer(r'(--[\w-]+)\s*:\s*(#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\))', css_text):
        vars_.setdefault(m.group(1), m.group(2))
    cuenta = Counter(h.upper() if len(h) == 7 else h.upper() for h in re.findall(r'#[0-9a-fA-F]{6}\b', css_text))
    def gris(h):
        r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
        return max(r, g, b) - min(r, g, b) < 18
    marca = [(h, n) for h, n in cuenta.most_common(40) if not gris(h)][:10]
    neutros = [(h, n) for h, n in cuenta.most_common(40) if gris(h)][:8]
    return vars_, marca, neutros


def main():
    if len(sys.argv) < 2 or '--salida' not in sys.argv:
        sys.exit(__doc__)
    fuente = sys.argv[1]
    out = Path(sys.argv[sys.argv.index('--salida') + 1])
    out.mkdir(parents=True, exist_ok=True)
    base = fuente if fuente.startswith('http') else (sys.argv[sys.argv.index('--base') + 1] if '--base' in sys.argv else '')
    html = fetch(fuente) if fuente.startswith('http') else Path(fuente).read_text(encoding='utf-8', errors='ignore')

    p = Landing()
    p.feed(html)
    css = '\n'.join(p.styles)
    for kind, href in p.embeds:
        if kind == 'css' and base and len(css) < 400000:
            try:
                css += '\n' + fetch(urllib.parse.urljoin(base, href), timeout=12)
            except Exception:
                pass

    def absol(u):
        return urllib.parse.urljoin(base, u) if base and u else u

    links = [{'href': absol(l['href']), 'text': l['text']} for l in p.links if l['href'] and not l['href'].startswith('#')]
    embeds = sorted(set(absol(v) for k, v in p.embeds if k == 'embed'))
    tallies = [t for t in (leer_tally(e) for e in embeds if 'tally.so' in e) if t]
    otros_forms = [e for e in embeds if re.search(r'typeform|hsforms|hubspot|jotform|forms\.gle|google\.com/forms', e)]
    agenda = sorted(set(l['href'] for l in links if re.search(r'calendly\.com|cal\.com/|tidycal\.com|zcal\.co|koalendar', l['href'])) |
                    set(e for e in embeds if re.search(r'calendly|cal\.com|tidycal', e)))
    whatsapp = sorted(set(l['href'] for l in links if re.search(r'wa\.me|api\.whatsapp', l['href'])))
    tels = sorted(set(l['href'] for l in links if l['href'].startswith('tel:')))
    mails = sorted(set(l['href'] for l in links if l['href'].startswith('mailto:')))
    privacidad = sorted(set(l['href'] for l in links if RX_PRIVACIDAD.search(l['text'] + ' ' + l['href'])))

    casillas = [c for f in p.forms for c in f['casillas']] + [c for t in tallies for c in t.get('casillas', [])]
    verificable = bool(p.forms or [t for t in tallies if 'error' not in t]) and not (otros_forms and not p.forms and not tallies)
    estado, detalle = analiza_consentimiento(casillas, verificable)

    logos = [dict(i, src=absol(i['src'])) for i in p.imgs if re.search(r'logo|brand|marca', ' '.join([i['src'], i['alt'], i['class'], i['id']]), re.I)]
    if not logos:
        logos = [dict(i, src=absol(i['src'])) for i in p.imgs if i['en_header']][:2]
    vars_, marca_cols, neutros = colores(css + '\n' + html[:200000])
    gfonts = []
    for fl in p.font_links:
        gfonts += [urllib.parse.unquote_plus(x).split(':')[0] for x in re.findall(r'family=([^&]+)', fl.replace('&amp;', '&'))]
    familias = Counter(re.sub(r'\s+', ' ', m.strip()) for m in re.findall(r'font-family\s*:\s*([^;}"]+)', css))

    datos = {
        'fuente': fuente, 'title': p.title.strip(), 'description': p.meta.get('description', '') or p.meta.get('og:description', ''),
        'og_image': absol(p.meta.get('og:image', '')),
        'titulares': p.heads, 'parrafos': p.parrafos, 'listas': p.items,
        'formularios_html': p.forms, 'tally': tallies, 'formularios_externos_no_leidos': otros_forms,
        'consentimiento': {'estado': estado, 'detalle': detalle},
        'agenda': agenda, 'whatsapp': whatsapp, 'telefonos': tels, 'emails': mails, 'privacidad': privacidad,
        'logos': logos, 'css_variables_color': vars_, 'colores_marca': marca_cols, 'colores_neutros': neutros,
        'google_fonts': gfonts, 'font_families': familias.most_common(6),
        'imagenes': [dict(i, src=absol(i['src'])) for i in p.imgs if i['src'] and not i['src'].startswith('data:')][:40],
        'enlaces': links[:120],
    }
    (out / 'landing.json').write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding='utf-8')

    L = [f'# Landing · {datos["title"]}', f'Fuente: {fuente}', '']
    icono = {'independiente': '🟢', 'combinada': '🔴', 'no_encontrada': '🔴', 'no_verificable': '🟠'}[estado]
    L += ['## Consentimiento para comunicaciones (art. 21 LSSI)', f'{icono} **{estado}** · {detalle}', '']
    L += ['## Formulario']
    for t in tallies:
        if 'error' in t:
            L.append(f'- Tally {t["id"]}: no se pudo leer ({t["error"]})')
            continue
        L.append(f'- Tally `{t["id"]}` {t.get("nombre", "")}')
        for q in t['preguntas']:
            ops = f' → opciones: {" | ".join(q["opciones"])}' if q['opciones'] else ''
            L.append(f'  - **{q["pregunta"]}** ({q["tipo"]}{", obligatoria" if q["obligatoria"] else ""}) · campo sugerido `{q["campo_sugerido"]}`{ops}')
        for c in t['casillas']:
            L.append(f'  - Casilla{" (obligatoria)" if c["obligatoria"] else ""}: «{c["texto"]}»')
        if t['campos_ocultos']:
            L.append(f'  - Campos ocultos: {", ".join(t["campos_ocultos"])}')
    for f in p.forms:
        L.append(f'- Formulario HTML (action: {f["action"] or "—"})')
        for c in f['campos']:
            L.append(f'  - {c.get("label") or c["placeholder"] or c["name"]} ({c["tipo"]}) · campo sugerido `{slug(c["name"] or c.get("label", "") or c["placeholder"])}`')
        for c in f['casillas']:
            L.append(f'  - Casilla: «{c.get("texto", "")}» name={c["name"]}')
    for e in otros_forms:
        L.append(f'- Formulario externo no leído: {e}')
    if not (tallies or p.forms or otros_forms):
        L.append('- No se ha encontrado formulario (¿se carga con JavaScript? pedir los campos).')
    L += ['', '## Contacto y agenda', f'- Agenda: {", ".join(agenda) or "—"}', f'- WhatsApp: {", ".join(whatsapp) or "—"}',
          f'- Teléfono: {", ".join(tels) or "—"}', f'- Email: {", ".join(mails) or "—"}', f'- Privacidad / legal: {", ".join(privacidad) or "—"}', '']
    L += ['## Identidad visual', '- Logos candidatos:'] + [f'  - {l["src"]} (alt «{l["alt"]}», {l["width"]}x{l["height"]})' for l in logos[:5]]
    L += [f'- Variables CSS de color: ' + ', '.join(f'{k}: {v}' for k, v in list(vars_.items())[:14]),
          f'- Colores de marca más usados: ' + ', '.join(f'{h} ({n})' for h, n in marca_cols),
          f'- Neutros más usados: ' + ', '.join(f'{h} ({n})' for h, n in neutros),
          f'- Google Fonts: {", ".join(gfonts) or "—"}', '- font-family más usadas: ' + ' | '.join(f'{f} ({n})' for f, n in familias.most_common(4)),
          f'- Imagen OG: {datos["og_image"] or "—"}', '']
    L += ['## Titulares'] + [f'- {t.upper()}: {x}' for t, x in p.heads]
    L += ['', '## Textos (párrafos)'] + [f'- {x}' for x in p.parrafos[:120]]
    L += ['', '## Listas, FAQ y elementos'] + [f'- {x}' for x in p.items[:120]]
    L += ['', '## Imágenes'] + [f'- {i["src"]} · alt «{i["alt"]}»' for i in datos['imagenes'][:25]]
    (out / 'landing.md').write_text('\n'.join(L), encoding='utf-8')
    print(f'Landing leída: {out / "landing.md"}')
    print(f'Formulario: {len(tallies)} Tally, {len(p.forms)} HTML, {len(otros_forms)} externos no leídos · consentimiento: {estado}')
    print(f'Logos candidatos: {len(logos)} · colores de marca: {", ".join(h for h, _ in marca_cols[:5])} · fuentes: {", ".join(gfonts) or "—"}')


if __name__ == '__main__':
    main()
