"""Render layered architecture diagrams as themed, animated SVGs.

Usage: python scripts/diagram.py spec.json out.svg

Spec: {"title": str, "subtitle": str, "footer": str,
       "rows": [{"label": str, "chain": bool, "nodes": [{"t": str, "s": str, "hi": bool}]}]}
"""
import json
import sys
from html import escape

RED, BG, PANEL, BORDER, TEXT, MUTED = "#dc2626", "#0d1117", "#161b22", "#30363d", "#e6edf3", "#8b949e"
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', sans-serif"
MONO = "'Fira Code', Consolas, monospace"

W, PAD_L, PAD_R, TOP = 1000, 150, 30, 96
NODE_H, ROW_GAP, NODE_GAP = 62, 46, 16


def render(spec):
    rows = spec["rows"]
    h = TOP + len(rows) * NODE_H + (len(rows) - 1) * ROW_GAP + (70 if spec.get("footer") else 36)
    out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">
<style>
  .t {{ font: 700 14px {FONT}; fill: {TEXT}; }}
  .s {{ font: 400 11.5px {FONT}; fill: {MUTED}; }}
  .lbl {{ font: 600 11px {MONO}; fill: {RED}; letter-spacing: 1px; }}
  .flow {{ stroke-dasharray: 6 6; animation: flow 1s linear infinite; }}
  @keyframes flow {{ to {{ stroke-dashoffset: -12; }} }}
  .pulse {{ animation: pulse 2.4s ease-in-out infinite; }}
  @keyframes pulse {{ 50% {{ stroke-opacity: .35; }} }}
</style>
<defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{RED}"/></marker></defs>
<rect x="0.5" y="0.5" width="{W - 1}" height="{h - 1}" rx="12" fill="{BG}" stroke="{BORDER}"/>
<rect x="0.5" y="0.5" width="5" height="{h - 1}" rx="2" fill="{RED}"/>
<text x="30" y="42" style="font: 800 22px {FONT}; fill: {TEXT}">{escape(spec["title"])}</text>
<text x="30" y="66" style="font: 400 13px {MONO}; fill: {RED}">{escape(spec.get("subtitle", ""))}</text>''']

    centers = []
    for i, row in enumerate(rows):
        y = TOP + i * (NODE_H + ROW_GAP)
        n = len(row["nodes"])
        avail = W - PAD_L - PAD_R
        nw = (avail - (n - 1) * NODE_GAP) / n
        out.append(f'<text x="30" y="{y + NODE_H / 2 + 4}" class="lbl">{escape(row.get("label", "").upper())}</text>')
        xs = []
        for j, node in enumerate(row["nodes"]):
            x = PAD_L + j * (nw + NODE_GAP)
            xs.append(x + nw / 2)
            hi = node.get("hi")
            out.append(
                f'<rect x="{x:.1f}" y="{y}" width="{nw:.1f}" height="{NODE_H}" rx="8" fill="{"#2a0a0c" if hi else PANEL}" '
                f'stroke="{RED if hi else BORDER}" stroke-width="{2 if hi else 1}" {"class=\"pulse\"" if hi else ""}/>'
            )
            out.append(f'<rect x="{x:.1f}" y="{y}" width="3" height="{NODE_H}" rx="1.5" fill="{RED}"/>')
            out.append(f'<text x="{x + nw / 2:.1f}" y="{y + 27}" class="t" text-anchor="middle">{escape(node["t"])}</text>')
            if node.get("s"):
                out.append(f'<text x="{x + nw / 2:.1f}" y="{y + 46}" class="s" text-anchor="middle">{escape(node["s"])}</text>')
            if row.get("chain") and j:
                out.append(
                    f'<line x1="{x - NODE_GAP + 1:.1f}" y1="{y + NODE_H / 2}" x2="{x - 2:.1f}" y2="{y + NODE_H / 2}" '
                    f'stroke="{RED}" stroke-width="2" marker-end="url(#a)"/>'
                )
        centers.append((y, xs[:1] if row.get("chain") else xs))

    # connectors: bus under each row, single animated drop to next row's bus
    for i, ((y, xs), (ny, nxs)) in enumerate(zip(centers, centers[1:])):
        if rows[i].get("chain"):
            xs = [PAD_L + (W - PAD_L - PAD_R) / 2]
        by, nby = y + NODE_H + ROW_GAP * 0.35, ny - ROW_GAP * 0.35
        mid = (PAD_L + W - PAD_R) / 2
        if len(xs) > 1:
            out.append(f'<line x1="{xs[0]:.1f}" y1="{by:.1f}" x2="{xs[-1]:.1f}" y2="{by:.1f}" stroke="{RED}" stroke-opacity=".6" stroke-width="1.5"/>')
            for x in xs:
                out.append(f'<line x1="{x:.1f}" y1="{y + NODE_H}" x2="{x:.1f}" y2="{by:.1f}" stroke="{RED}" stroke-opacity=".6" stroke-width="1.5"/>')
            top = by
        else:
            top = y + NODE_H
            mid = xs[0]
        if len(nxs) > 1:
            out.append(f'<line x1="{nxs[0]:.1f}" y1="{nby:.1f}" x2="{nxs[-1]:.1f}" y2="{nby:.1f}" stroke="{RED}" stroke-opacity=".6" stroke-width="1.5"/>')
            for x in nxs:
                out.append(f'<line x1="{x:.1f}" y1="{nby:.1f}" x2="{x:.1f}" y2="{ny - 3}" stroke="{RED}" stroke-opacity=".6" stroke-width="1.5" marker-end="url(#a)"/>')
            out.append(f'<line x1="{mid:.1f}" y1="{top:.1f}" x2="{mid:.1f}" y2="{nby:.1f}" stroke="{RED}" stroke-width="2" class="flow"/>')
        else:
            out.append(f'<line x1="{mid:.1f}" y1="{top:.1f}" x2="{mid:.1f}" y2="{nby:.1f}" stroke="{RED}" stroke-width="2" class="flow"/>')
            out.append(f'<line x1="{mid:.1f}" y1="{nby:.1f}" x2="{nxs[0]:.1f}" y2="{nby:.1f}" stroke="{RED}" stroke-width="2"/>')
            out.append(f'<line x1="{nxs[0]:.1f}" y1="{nby:.1f}" x2="{nxs[0]:.1f}" y2="{ny - 3}" stroke="{RED}" stroke-width="2" marker-end="url(#a)"/>')

    if spec.get("footer"):
        out.append(f'<text x="30" y="{h - 26}" style="font: 400 12px {MONO}; fill: {MUTED}">{escape(spec["footer"])}</text>')
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        spec = json.load(f)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(render(spec))
