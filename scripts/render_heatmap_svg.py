"""data/contributions.json -> contrib-heatmap.svg (53x7 grid, diagonal reveal, then freeze)"""
import json, datetime as dt

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
d = json.load(open("data/contributions.json"))
days = d["days"]
CELL, GAP, LEFT, TOP, W = 13, 3, 36, 44, 860
STEP = CELL + GAP

first = dt.date.fromisoformat(days[0]["date"])
offset = (first.weekday() + 1) % 7            # Sunday = 0
H = TOP + 7 * STEP + 52

# level 5 = neon top end: the busiest ~20% of level-4 days
active = sorted(x["count"] for x in days if x["level"] == 4)
neon = active[int(len(active) * 0.8)] if active else 10**9

o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
     '<style>.c{opacity:0;animation:in .35s ease-out forwards}'
     '@keyframes in{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}'
     'text{font-family:ui-monospace,Menlo,Consolas,monospace;fill:#8b949e;font-size:11px}</style>',
     f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>']

last_m = None
for i, x in enumerate(days):
    wk, dw = divmod(i + offset, 7)
    dd = dt.date.fromisoformat(x["date"])
    if dd.month != last_m and (wk == 0 or dd.day <= 7):
        o.append(f'<text x="{LEFT + wk*STEP}" y="{TOP-10}">{dd.strftime("%b")}</text>')
        last_m = dd.month
    lvl = 5 if x["level"] == 4 and x["count"] >= neon else x["level"]
    delay = (wk + dw) * 0.018
    o.append(f'<rect class="c" style="animation-delay:{delay:.2f}s" x="{LEFT + wk*STEP}" y="{TOP + dw*STEP}" '
             f'width="{CELL}" height="{CELL}" rx="3" fill="{PALETTE[lvl]}"><title>{x["count"]} on {x["date"]}</title></rect>')
for dw, lab in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
    o.append(f'<text x="6" y="{TOP + dw*STEP + 10}">{lab}</text>')

fy = TOP + 7 * STEP + 28
o.append(f'<text x="{LEFT}" y="{fy}">{d["total"]:,} contributions in the last year · streak {d["current_streak"]}d · longest {d["longest_streak"]}d</text>')
lx = W - 200
o.append(f'<text x="{lx}" y="{fy}">Less</text>')
for i, c in enumerate(PALETTE):
    o.append(f'<rect x="{lx+34+i*(CELL+3)}" y="{fy-10}" width="{CELL}" height="{CELL}" rx="3" fill="{c}"/>')
o.append(f'<text x="{lx+34+6*(CELL+3)+4}" y="{fy}">More</text>')
o.append('</svg>')
open("contrib-heatmap.svg", "w", encoding="utf-8").write("\n".join(o))
print("wrote contrib-heatmap.svg")
