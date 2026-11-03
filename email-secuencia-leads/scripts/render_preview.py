#!/usr/bin/env python3
"""Genera vistas previas de un email HTML con Chrome headless.

Uso: python3 render_preview.py ruta/email.html
Crea en la carpeta del email:
  preview-hoja.png            claro · oscuro · móvil juntos (visión general). Usa email-muestra.html si existe (variables con datos de ejemplo)
  preview-claro.png / preview-oscuro.png / preview-movil.png   capturas completas
  previews-detalle/claro-01.png…, movil-01.png…               tramos a tamaño real para revisar detalles

- Claro y oscuro se fuerzan explícitamente (Chrome hereda el tema del sistema si no).
- Oscuro = prefers-color-scheme: dark (comportamiento de Apple Mail).
- El móvil se renderiza en un iframe de 390 px (Chrome headless no baja de cierto ancho de ventana).
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

# Windows: que tildes, eñes y emojis no rompan la salida (la consola usa cp1252).
for _flujo in (sys.stdout, sys.stderr):
    try:
        _flujo.reconfigure(encoding='utf-8')
    except Exception:
        pass


CHROME_CANDIDATES = [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/usr/bin/google-chrome', '/usr/bin/chromium',
    os.path.expandvars(r'%ProgramFiles%\Google\Chrome\Application\chrome.exe'),
    os.path.expandvars(r'%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe'),
    os.path.expandvars(r'%LocalAppData%\Google\Chrome\Application\chrome.exe'),
]


def chrome():
    for c in CHROME_CANDIDATES:
        if os.path.exists(c):
            return c
    sys.exit('No encuentro Google Chrome para generar las vistas previas.')


def run_chrome(url, out, width, height, dark):
    args = [chrome(), '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run',
            f'--blink-settings=preferredColorScheme={0 if dark else 1}',
            f'--window-size={width},{height}', '--virtual-time-budget=15000',
            f'--screenshot={out}', url]
    subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=150)


def trim(path, pad=24, crop_w=None):
    im = Image.open(path).convert('RGB')
    if crop_w:
        im = im.crop((0, 0, crop_w, im.size[1]))
    w, h = im.size
    bg = im.getpixel((w - 3, h - 3))
    bottom = h - 1
    while bottom > 0:
        row = [im.getpixel((x, bottom)) for x in range(0, w, 3)]
        if any(sum(abs(a - b) for a, b in zip(px, bg)) > 12 for px in row):
            break
        bottom -= 1
    im.crop((0, 0, w, min(h, bottom + pad))).save(path)


def shot_desktop(html, out, dark):
    run_chrome(html.resolve().as_uri(), out, 680, 8000, dark)
    trim(out)


def shot_mobile(html, out, width=390, height=12000):
    wrapper = Path(tempfile.mkdtemp()) / 'movil.html'
    wrapper.write_text(
        '<!DOCTYPE html><html><head><meta name="color-scheme" content="light">'
        '<style>html,body{margin:0;padding:0;background:#fff}</style></head><body>'
        f'<iframe src="{html.resolve().as_uri()}" width="{width}" height="{height}" '
        'style="border:0;display:block"></iframe></body></html>', encoding='utf-8')
    run_chrome(wrapper.as_uri(), out, 800, height, dark=False)
    trim(out, crop_w=width)


def slices(path, outdir, prefix, seg=1100, overlap=80):
    im = Image.open(path)
    w, h = im.size
    outdir.mkdir(exist_ok=True)
    for old in outdir.glob(f'{prefix}-*.png'):
        old.unlink()
    n, y = 1, 0
    while y < h:
        im.crop((0, y, w, min(h, y + seg))).save(outdir / f'{prefix}-{n:02d}.png')
        n += 1
        y += seg - overlap
    return n - 1


def sheet(paths, out, target_h=2400):
    ims = [Image.open(p).convert('RGB') for p in paths]
    h = min(max(i.size[1] for i in ims), target_h)
    scaled = []
    for i in ims:
        r = h / i.size[1]
        scaled.append(i.resize((max(1, int(i.size[0] * r)), h), Image.LANCZOS))
    gap = 24
    W = sum(s.size[0] for s in scaled) + gap * (len(scaled) + 1)
    canvas = Image.new('RGB', (W, h + gap * 2), (200, 205, 212))
    x = gap
    for s in scaled:
        canvas.paste(s, (x, gap))
        x += s.size[0] + gap
    canvas.save(out)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    html = Path(sys.argv[1])
    d = html.parent
    if html.name == 'email.html' and (d / 'email-muestra.html').exists():
        html = d / 'email-muestra.html'
        print('Vista previa con los datos de ejemplo del lead (email-muestra.html)')
    claro, oscuro, movil = d / 'preview-claro.png', d / 'preview-oscuro.png', d / 'preview-movil.png'
    shot_desktop(html, claro, dark=False)
    shot_desktop(html, oscuro, dark=True)
    shot_mobile(html, movil)
    sheet([claro, oscuro, movil], d / 'preview-hoja.png')
    det = d / 'previews-detalle'
    nc = slices(claro, det, 'claro')
    nm = slices(movil, det, 'movil')
    for p in (claro, oscuro, movil, d / 'preview-hoja.png'):
        print(p, Image.open(p).size)
    print(f'{det}: {nc} tramos claro, {nm} tramos móvil (tamaño real)')


if __name__ == '__main__':
    main()
