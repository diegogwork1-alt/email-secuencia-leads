#!/usr/bin/env python3
"""Convierte los emails montados a la versión que se pega en ActiveCampaign.

Uso:
  python3 version_activecampaign.py <carpeta de la secuencia> [e3 e4 …]

Sin lista de emails, hace todas las carpetas `eN/` que tengan `email.html`.
Lee `marca.json` de la carpeta de la secuencia para saber la dirección postal,
el correo de baja y el prefijo de variables.

Por qué existe
--------------
`build_email.py` monta el email para **n8n**: el saludo lleva una expresión
`{{ $json.nombre }}`, la baja es un `mailto:` y la dirección postal va escrita.
Si el cliente envía con ActiveCampaign hay que cambiar tres cosas y una cuarta
que es fácil de olvidar:

  Hola{{ $json.nombre … }}:   →  Hola %FIRSTNAME%:
  dirección postal literal    →  %SENDER-INFO-SINGLELINE%
  mailto de baja              →  %UNSUBSCRIBELINK%
  utm_source=n8n              →  utm_source=activecampaign

Con `%UNSUBSCRIBELINK%` y `%SENDER-INFO-SINGLELINE%` presentes, ActiveCampaign
**no añade su propio pie**, así que no sale duplicado.

La cuarta (las UTM) se arregla mejor en el origen: pon `"utm_source": "activecampaign"`
en `marca.json` y `build_email.py` ya las monta bien. Este script las corrige también,
por si la secuencia se montó antes de saber la plataforma.

Verifica lo que ha hecho: un marcador de cada, ningún resto de n8n y el número de
líneas que deben cambiar. Si algo no cuadra, lo dice y no se queda callado.
"""
import json, pathlib, re, sys

# Windows: que tildes, eñes y emojis no rompan la salida (la consola usa cp1252).
for _flujo in (sys.stdout, sys.stderr):
    try:
        _flujo.reconfigure(encoding='utf-8')
    except Exception:
        pass


MARCADORES = ('%FIRSTNAME%', '%UNSUBSCRIBELINK%', '%SENDER-INFO-SINGLELINE%')


def convertir(carpeta: pathlib.Path, marca: dict) -> str:
    direccion = (marca.get('legal') or {}).get('direccion', '')
    nif = (marca.get('legal') or {}).get('nif', '')
    correo = (marca.get('remitente') or {}).get('email', '')
    pre = marca.get('n8n_prefijo', '$json')
    saludo_n8n = "Hola{{ %s.nombre ? ' ' + %s.nombre : '' }}:" % (pre, pre)
    baja = f'mailto:{correo}?subject=Baja'
    cola = f'NIF {nif} · {direccion}' if nif else direccion

    utm_html = 0
    for ext, sep in (('html', '&middot;'), ('txt', '·')):
        origen = carpeta / f'email.{ext}'
        if not origen.exists():
            return f'falta email.{ext}'
        s = origen.read_text(encoding='utf-8')
        s = s.replace(saludo_n8n, 'Hola %FIRSTNAME%:')
        if cola:
            s = s.replace(cola, f'NIF {nif} {sep} %SENDER-INFO-SINGLELINE%' if nif else '%SENDER-INFO-SINGLELINE%')
        s = s.replace(f'href="{baja}"', 'href="%UNSUBSCRIBELINK%"') if ext == 'html' \
            else s.replace(f'Darme de baja: {baja}', 'Darme de baja: %UNSUBSCRIBELINK%')
        if ext == 'html':
            utm_html = s.count('utm_source=n8n')
        s = s.replace('utm_source=n8n', 'utm_source=activecampaign')
        (carpeta / f'email-activecampaign.{ext}').write_text(s, encoding='utf-8')

    fallos = []
    for ext in ('html', 'txt'):
        t = (carpeta / f'email-activecampaign.{ext}').read_text(encoding='utf-8')
        for m in MARCADORES:
            if t.count(m) != 1:
                fallos.append(f'{ext}: {m} aparece {t.count(m)} veces')
        for resto in (f'{pre}.nombre', direccion, baja, 'utm_source=n8n'):
            if resto and resto in t:
                fallos.append(f'{ext}: queda sin sustituir «{resto[:30]}»')
    a = re.sub(r'><', '>\n<', (carpeta / 'email.html').read_text(encoding='utf-8')).splitlines()
    b = re.sub(r'><', '>\n<', (carpeta / 'email-activecampaign.html').read_text(encoding='utf-8')).splitlines()
    distintas = sum(1 for x, y in zip(a, b) if x != y)
    esperadas = 3 + utm_html          # saludo + dirección + baja, más un enlace por cada utm
    if distintas != esperadas:
        fallos.append(f'html: cambian {distintas} líneas, deberían ser {esperadas}')
    return 'OK' + (f' · utm corregidas: {utm_html}' if utm_html else '') if not fallos \
        else 'FALLA → ' + ' · '.join(fallos)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    base = pathlib.Path(sys.argv[1]).expanduser()
    marca_path = base / 'marca.json'
    if not marca_path.exists():
        print(f'No encuentro marca.json en {base}')
        return 1
    marca = json.loads(marca_path.read_text(encoding='utf-8'))
    emails = sys.argv[2:] or sorted(d.name for d in base.glob('e[0-9]*') if (d / 'email.html').exists())
    if not emails:
        print('No hay ninguna carpeta eN/ con email.html montado.')
        return 1
    malo = False
    for e in emails:
        r = convertir(base / e, marca)
        malo |= r.startswith('FALLA') or r.startswith('falta')
        print(f'{e}: {r}')
    return 1 if malo else 0


if __name__ == '__main__':
    sys.exit(main())
