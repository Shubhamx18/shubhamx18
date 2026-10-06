"""Convert source-prepped.png into a self-typing monochrome ASCII SVG (SMIL, no JS)."""
import sys
from html import escape
from PIL import Image

SRC = sys.argv[1] if len(sys.argv) > 1 else "source-prepped.png"
OUT = "avi-ascii.svg"
RAMP = " .`:-=+*cs#%@"          # bright (sparse) -> dark (dense)
COLS = 100
FS, LH = 7.0, 7.4              # font size, line height
CW = FS * 0.6                  # monospace char width
COLOR = "#c9d1d9"
ROW_DELAY, ROW_DUR = 0.07, 0.45

img = Image.open(SRC).convert("L")
w, h = img.size
rows = max(1, round(h / w * COLS * (CW / LH)))
img = img.resize((COLS, rows), Image.LANCZOS)
px = img.load()

W, H = COLS * CW, rows * LH + 8
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} {H:.1f}" width="{W:.0f}" height="{H:.0f}">',
         '<rect width="100%" height="100%" fill="#0d1117"/>', '<defs>']
for r in range(rows):
    parts.append(f'<clipPath id="c{r}"><rect x="0" y="{r*LH+4:.1f}" width="0" height="{LH:.1f}">'
                 f'<animate attributeName="width" from="0" to="{W:.1f}" begin="{r*ROW_DELAY:.2f}s" '
                 f'dur="{ROW_DUR}s" fill="freeze"/></rect></clipPath>')
parts.append('</defs>')
parts.append(f'<g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="{FS}" fill="{COLOR}" xml:space="preserve">')
for r in range(rows):
    line = "".join(RAMP[min(len(RAMP) - 1, int((255 - px[c, r]) / 256 * len(RAMP)))] for c in range(COLS))
    if line.strip():
        parts.append(f'<text x="0" y="{(r+1)*LH:.1f}" textLength="{W:.1f}" lengthAdjust="spacing" clip-path="url(#c{r})">{escape(line)}</text>')
parts.append('</g>')
for r in range(rows):                     # cursor block riding the wipe edge
    t = r * ROW_DELAY
    parts.append(f'<rect y="{r*LH+4:.1f}" width="{CW:.1f}" height="{LH:.1f}" fill="{COLOR}" opacity="0">'
                 f'<animate attributeName="x" from="0" to="{W:.1f}" begin="{t:.2f}s" dur="{ROW_DUR}s" fill="freeze"/>'
                 f'<set attributeName="opacity" to="0.8" begin="{t:.2f}s"/>'
                 f'<set attributeName="opacity" to="0" begin="{t+ROW_DUR:.2f}s"/></rect>')
parts.append('</svg>')
open(OUT, "w", encoding="utf-8").write("\n".join(parts))
print("wrote", OUT, f"({COLS}x{rows})")
