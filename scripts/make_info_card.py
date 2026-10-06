"""Hand-authored neofetch-style info card. STATIC=1 emits a frozen frame."""
import os
from html import escape

STATIC = os.environ.get("STATIC") == "1"
W, PAD, LH = 490, 22, 22
USER, HOST = "shubham", "github"

ROWS = [
    ("Now",        "Computer Engineering student, going deep on DevOps", "#7ee787"),
    ("Prev",       "Web & Java projects, Python scripting, AWS sandboxes", "#79c0ff"),
    ("Stack",      "Java · Python · JS · MySQL · MongoDB", "#d2a8ff"),
    ("DevOps",     "AWS · Docker · Kubernetes · Terraform · Jenkins", "#ffa657"),
    ("Highlights", "docker-workbench · k8s-manifests · linux-engine", "#ff7b72"),
    ("Goal",       "Scalable apps, CI/CD pipelines, open source", "#e3b341"),
]

lines = []
y = 90
lines.append((f'<tspan fill="#a78bfa">{USER}</tspan><tspan fill="#8b949e">@</tspan><tspan fill="#a78bfa">{HOST}</tspan>', y)); y += LH
lines.append(('<tspan fill="#30363d">' + "─" * 28 + '</tspan>', y)); y += LH
for k, v, c in ROWS:
    lines.append((f'<tspan fill="{c}" font-weight="700">{escape(k)}</tspan><tspan fill="#8b949e">: </tspan>'
                  f'<tspan fill="#c9d1d9">{escape(v)}</tspan>', y)); y += LH
H = y + 24

o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
     f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>',
     f'<rect width="{W}" height="34" rx="10" fill="#161b22"/><rect y="24" width="{W}" height="10" fill="#161b22"/>',
     '<circle cx="20" cy="17" r="6" fill="#ff5f56"/><circle cx="40" cy="17" r="6" fill="#ffbd2e"/><circle cx="60" cy="17" r="6" fill="#27c93f"/>',
     f'<text x="{W/2}" y="22" text-anchor="middle" font-size="12" fill="#8b949e" font-family="ui-monospace,Menlo,Consolas,monospace">neofetch</text>',
     f'<text x="{PAD}" y="62" font-size="13" fill="#7ee787" font-family="ui-monospace,Menlo,Consolas,monospace">$ neofetch</text>',
     '<g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="13" xml:space="preserve">']
for i, (markup, yy) in enumerate(lines):
    if STATIC:
        o.append(f'<text x="{PAD}" y="{yy}">{markup}</text>')
    else:
        b = 0.5 + i * 0.25
        o.append(f'<g opacity="0"><text x="{PAD}" y="{yy}">{markup}</text>'
                 f'<animate attributeName="opacity" from="0" to="1" begin="{b:.2f}s" dur="0.4s" fill="freeze"/>'
                 f'<animateTransform attributeName="transform" type="translate" from="-10 0" to="0 0" begin="{b:.2f}s" dur="0.4s" fill="freeze"/></g>')
o.append('</g></svg>')
open("info-card.svg", "w", encoding="utf-8").write("\n".join(o))
print("wrote info-card.svg")
