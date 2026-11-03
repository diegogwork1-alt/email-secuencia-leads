"""Textos fijos del email por idioma (pie legal, títulos por defecto, despedida).
Se elige con «idioma» en marca.json (por defecto «es»; también «ca», catalán)."""

TEXTOS = {
    'es': {
        'lang': 'es',
        'privacidad': 'Política de privacidad',
        'baja': 'Darme de baja',
        'comunicacion': 'Comunicación comercial.',
        'resumen': 'Lo que nos has contado',
        'antes': 'Antes',
        'despues': 'Después',
        'despedida': 'Un saludo,',
        'asunto_baja': 'Baja',
    },
    'ca': {
        'lang': 'ca',
        'privacidad': 'Política de privacitat',
        'baja': 'Donar-me de baixa',
        'comunicacion': 'Comunicació comercial.',
        'resumen': "El que ens has explicat",
        'antes': 'Abans',
        'despues': 'Després',
        'despedida': 'Una salutació,',
        'asunto_baja': 'Baixa',
    },
}


def textos(marca):
    return TEXTOS.get((marca or {}).get('idioma', 'es'), TEXTOS['es'])
