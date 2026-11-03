# email-secuencia-leads

Skill gratis para Claude Code: la secuencia de emails que recibe un lead después de rellenar el formulario de tu landing.

**Qué hace:** le pasas el brief de tu negocio y tu landing (URL o HTML), y Claude:

1. Lee tu oferta, tu formulario y tu identidad visual (logo, colores, tipografías).
2. Comprueba si tu formulario tiene la casilla legal para mandar emails comerciales (RGPD y LSSI). Si no la tiene, te lo dice y prepara solo el email de recepción.
3. Investiga a tu público: qué le preocupa, qué necesita saber y qué dudas y objeciones tiene antes de contratar.
4. Te propone la secuencia completa: email de recepción al instante, emails de valor, invitación a la llamada y cierre, con los días de envío según tu tipo de oferta. Cada email derriba una duda real del lead.
5. Con tu OK, redacta cada email (claro y directo, con los fundamentos de Ogilvy y de *Email Persuasion* de Ian Brodie) y lo maqueta en HTML con aspecto de carta de tu marca, versión en texto plano, modo oscuro y control de calidad.

Para en cada paso a pedir tu aprobación y no inventa datos: lo que falta lo marca y te lo pregunta.

**Qué te deja:** por cada email, `email.html` (listo para n8n, o en versión ActiveCampaign), `email.txt` y las vistas previas en PNG. Al final, `calendario.md` con qué email sale cada día, su asunto, sus variables y la lista de control antes de activar.

## Instalación

```bash
git clone https://github.com/diegogwork1-alt/email-secuencia-leads.git
mkdir -p ~/.claude/skills
cp -r email-secuencia-leads/email-secuencia-leads ~/.claude/skills/
```

Si solo la quieres en un proyecto, cópiala en la carpeta `.claude/skills/` de ese proyecto (y cambia la ruta de los scripts que aparece en `SKILL.md`).

**Necesitas:** Python 3, Pillow (`pip install pillow`) y Google Chrome o Chromium para las vistas previas. Para investigar al público usa la búsqueda web de Claude Code; si tienes conectado NotebookLM, también lo aprovecha.

## Cómo se usa

Abre Claude Code en la carpeta de tu proyecto y pídelo con tus palabras, por ejemplo:

> Hazme la secuencia de emails para los leads de mi landing. El brief está en `brief.pdf` y la landing es https://tuweb.com/landing

Claude te enseña primero el diagnóstico y el plan de la secuencia. Cuando lo apruebes, va email por email: primero el texto, después el email montado.
