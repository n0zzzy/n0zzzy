"""Generate the cyberpunk-styled README panels in assets/.

Usage: python scripts/panels.py
"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
RED, TEXT, MUTED, PINK = "#dc2626", "#f0f6fc", "#9aa4b2", "#fca5a5"
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', sans-serif"
MONO = "'Fira Code', Consolas, 'Courier New', monospace"


def wrap(text, width):
    lines, cur = [], ""
    for word in text.split():
        if len(cur) + len(word) + 1 > width and cur:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return lines + [cur] if cur else lines


def frame(w, h, tag, body, uid):
    b = 20  # corner bracket length
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs>
  <linearGradient id="bg{uid}" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#06080c"/><stop offset="0.6" stop-color="#0b0a10"/><stop offset="1" stop-color="#1c0609"/>
  </linearGradient>
  <radialGradient id="glow{uid}" cx="1" cy="0" r="0.9">
    <stop offset="0" stop-color="{RED}" stop-opacity="0.28"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="grid{uid}" width="26" height="26" patternUnits="userSpaceOnUse">
    <path d="M26 0 L0 0 0 26" fill="none" stroke="{RED}" stroke-opacity="0.07"/>
  </pattern>
  <pattern id="scan{uid}" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="#000" fill-opacity="0.35"/>
  </pattern>
  <clipPath id="clip{uid}"><rect width="{w}" height="{h}" rx="10"/></clipPath>
  <style>
    .t{uid} {{ font: 700 17px {FONT}; fill: {TEXT}; }}
    .b{uid} {{ font: 400 13.5px {FONT}; fill: {MUTED}; }}
    .m{uid} {{ font: 500 13px {MONO}; }}
    .tag{uid} {{ font: 600 11px {MONO}; fill: {RED}; letter-spacing: 2px; }}
    .sweep{uid} {{ animation: sw{uid} 5s linear infinite; }}
    @keyframes sw{uid} {{ from {{ transform: translateY(-40px); }} to {{ transform: translateY({h + 40}px); }} }}
    .blink{uid} {{ animation: bl{uid} 1s steps(1) infinite; }}
    @keyframes bl{uid} {{ 50% {{ opacity: 0; }} }}
    .pulse{uid} {{ animation: pu{uid} 2.6s ease-in-out infinite; }}
    @keyframes pu{uid} {{ 50% {{ stroke-opacity: 0.25; }} }}
  </style>
</defs>
<g clip-path="url(#clip{uid})">
  <rect width="{w}" height="{h}" fill="url(#bg{uid})"/>
  <rect width="{w}" height="{h}" fill="url(#grid{uid})"/>
  <rect width="{w}" height="{h}" fill="url(#glow{uid})"/>
  <rect width="{w}" height="{h}" fill="url(#scan{uid})"/>
  <rect class="sweep{uid}" width="{w}" height="40" fill="{RED}" fill-opacity="0.05"/>
  {body}
</g>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="10" fill="none" stroke="{RED}" stroke-opacity="0.45" class="pulse{uid}"/>
<g stroke="{RED}" stroke-width="3" fill="none" stroke-linecap="square">
  <path d="M2 {b} V2 H{b}"/><path d="M{w - b} 2 H{w - 2} V{b}"/>
  <path d="M2 {h - b} V{h - 2} H{b}"/><path d="M{w - b} {h - 2} H{w - 2} V{h - b}"/>
</g>
<text x="22" y="28" class="tag{uid}">{escape(tag)}</text>
</svg>'''


def whoami():
    w, h, u = 1000, 410, "w"
    yaml = [
        ("name", '"Russel Carlo"'), ("handle", '"n0zzzy"'), ("based_in", '"Philippines"'),
        ("school", '"NU Fairview · Information Technology"'), ("", ""),
        ("certified", None), ("-", "AWS Certified AI Practitioner"), ("-", "Microsoft Fabric Data Engineer Assoc."), ("", ""),
        ("building", None), ("-", "AI agents on Bedrock AgentCore"), ("-", "Azure AI Foundry agents"),
        ("-", "Cloud infra with Terraform + EKS"), ("-", "Full-stack & mobile apps"),
    ]
    rows = []
    y = 104
    for k, v in yaml:
        if k == "-":
            rows.append(f'<text x="74" y="{y}" class="m{u}"><tspan fill="{RED}">- </tspan><tspan fill="{TEXT}">{escape(v)}</tspan></text>')
        elif k:
            val = "" if v is None else f'<tspan fill="{PINK}"> {escape(v)}</tspan>'
            rows.append(f'<text x="56" y="{y}" class="m{u}"><tspan fill="{RED}">{k}</tspan><tspan fill="{MUTED}">:</tspan>{val}</text>')
        y += 19 if k else 10
    rows.append(f'<text x="56" y="{y + 6}" class="m{u}"><tspan fill="{RED}">philosophy</tspan><tspan fill="{MUTED}">:</tspan><tspan fill="{PINK}"> "I have no enemies."</tspan></text>')
    rows.append(f'<rect class="blink{u}" x="318" y="{y - 7}" width="9" height="16" fill="{RED}"/>')

    current = [
        ("🥇", "Rank 1 Overall", " · AWS QuickQuest Finale"),
        ("🎓", "AWS AI & ML Scholar", " · top 4,500 globally"),
        ("🤖", "Shipping multi-agent systems", " on AWS"),
        ("☸️", "Running AI agents", " on Kubernetes (EKS)"),
        ("⚡", "Agentic coding", " with Claude, Codex & Kiro"),
        ("📱", "Building web + mobile", " (PWA) apps"),
    ]
    cur = [f'<text x="580" y="78" class="tag{u}">// CURRENTLY</text>']
    for i, (icon, bold, rest) in enumerate(current):
        cy = 120 + i * 44
        cur.append(f'<rect x="580" y="{cy - 22}" width="390" height="34" rx="6" fill="#0d1117" fill-opacity="0.85" stroke="{RED}" stroke-opacity="0.18"/>')
        cur.append(f'<text x="594" y="{cy}" style="font: 15px {FONT}">{icon}</text>')
        cur.append(f'<text x="624" y="{cy}" style="font: 14px {FONT}"><tspan fill="{TEXT}" font-weight="700">{escape(bold)}</tspan><tspan fill="{MUTED}">{escape(rest)}</tspan></text>')

    body = f'''
  <rect x="30" y="50" width="520" height="335" rx="8" fill="#0d1117" fill-opacity="0.92" stroke="{RED}" stroke-opacity="0.3"/>
  <rect x="30" y="50" width="520" height="30" rx="8" fill="#161b22"/>
  <rect x="30" y="72" width="520" height="8" fill="#161b22"/>
  <circle cx="50" cy="65" r="5" fill="{RED}"/><circle cx="68" cy="65" r="5" fill="#7f1d1d"/><circle cx="86" cy="65" r="5" fill="#3f0d10"/>
  <text x="290" y="70" text-anchor="middle" class="m{u}" fill="{MUTED}" style="font-size:12px">~/n0zzzy/whoami.yaml</text>
  {"".join(rows)}
  {"".join(cur)}'''
    return frame(w, h, "SYS://WHOAMI", body, u)


def medal(cx, cy, label, u):
    pts = " ".join(f"{cx + 34 * c:.1f},{cy + 34 * s:.1f}" for c, s in
                   [(0, -1), (0.866, -0.5), (0.866, 0.5), (0, 1), (-0.866, 0.5), (-0.866, -0.5)])
    inner = " ".join(f"{cx + 27 * c:.1f},{cy + 27 * s:.1f}" for c, s in
                     [(0, -1), (0.866, -0.5), (0.866, 0.5), (0, 1), (-0.866, 0.5), (-0.866, -0.5)])
    return f'''<polygon points="{pts}" fill="none" stroke="{RED}" stroke-width="2" class="pulse{u}"/>
  <polygon points="{inner}" fill="{RED}"/>
  <text x="{cx}" y="{cy + 8}" text-anchor="middle" style="font: 900 22px {FONT}; fill: #fff">{label}</text>'''


def win(n, place, title, sub, event, desc):
    w, h, u = 330, 340, f"v{n}"
    lines = [f'<text x="{w / 2}" y="{140 + i * 22}" text-anchor="middle" class="t{u}">{escape(t)}</text>' for i, t in enumerate([title, sub] if sub else [title])]
    y = 140 + (2 if sub else 1) * 22 + 8
    for t in wrap(event, 40):
        lines.append(f'<text x="{w / 2}" y="{y}" text-anchor="middle" class="m{u}" fill="{PINK}" style="font-size:11.5px">{escape(t)}</text>')
        y += 17
    y += 8
    for t in wrap(desc, 44):
        lines.append(f'<text x="{w / 2}" y="{y}" text-anchor="middle" class="b{u}">{escape(t)}</text>')
        y += 19
    body = f'''
  <rect x="16" y="44" width="{w - 32}" height="{h - 60}" rx="8" fill="#0d1117" fill-opacity="0.9" stroke="{RED}" stroke-opacity="0.22"/>
  {medal(w / 2, 86, place, u)}
  {"".join(lines)}
  <rect x="{w / 2 - 62}" y="{h - 50}" width="124" height="28" rx="14" fill="#1a0507" stroke="{RED}"/>
  <text x="{w / 2}" y="{h - 31}" text-anchor="middle" class="m{u}" fill="{PINK}" style="font-size:12px; font-weight:700">VIEW POST ▸</text>'''
    return frame(w, h, f"WIN://0{n}", body, u)


ICONS = {
    "cloud": '<path d="M6.5 20a4.5 4.5 0 0 1-.7-8.95A6.2 6.2 0 0 1 17.7 9.3 5.4 5.4 0 0 1 18 20z" fill="#fff"/>',
    "ms": '<rect x="2" y="2" width="9.5" height="9.5" fill="#fff"/><rect x="12.5" y="2" width="9.5" height="9.5" fill="#fff"/><rect x="2" y="12.5" width="9.5" height="9.5" fill="#fff"/><rect x="12.5" y="12.5" width="9.5" height="9.5" fill="#fff"/>',
    "u": '<path d="M5 3v10a7 7 0 0 0 14 0V3h-4v10a3 3 0 0 1-6 0V3z" fill="#fff"/>',
}


def cert(key, icon, issuer, title, code, desc):
    w, h, u = 490, 150, f"c{key}"
    body = f'''
  <rect x="16" y="40" width="{w - 32}" height="{h - 56}" rx="8" fill="#0d1117" fill-opacity="0.9" stroke="{RED}" stroke-opacity="0.22"/>
  <rect x="32" y="54" width="66" height="66" rx="10" fill="{RED}" class="pulse{u}" stroke="{PINK}" stroke-opacity="0.6"/>
  <g transform="translate(44, 66) scale(1.75)">{ICONS[icon]}</g>
  <text x="116" y="66" class="tag{u}">{escape(issuer)}</text>
  <text x="116" y="90" class="t{u}">{escape(title)}</text>
  <text x="116" y="111" class="b{u}"><tspan fill="{PINK}" font-weight="700">{escape(code)}</tspan>  ·  {escape(desc)}</text>
  <text x="{w - 30}" y="66" text-anchor="end" class="m{u}" fill="{PINK}" style="font-size:11px; font-weight:700">VERIFY ▸</text>'''
    return frame(w, h, f"CERT://{key.upper()}", body, u)


def heading(key, title, num):
    w, h, u = 1000, 64, f"h{key}"
    tw = sum(10 if ch == " " else 23 for ch in title)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs>
  <linearGradient id="ln{u}" x1="0" x2="1"><stop offset="0" stop-color="{RED}"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient>
  <linearGradient id="shine{u}" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <style>
    .sh{u} {{ animation: sh{u} 4s ease-in-out infinite; }}
    @keyframes sh{u} {{ from {{ transform: translateX(-120px); }} to {{ transform: translateX({w}px); }} }}
    .bl{u} {{ animation: bl{u} 1.2s steps(1) infinite; }}
    @keyframes bl{u} {{ 50% {{ opacity: 0; }} }}
  </style>
</defs>
<rect x="0" y="14" width="8" height="36" fill="{RED}"/>
<rect x="12" y="14" width="3" height="36" fill="{RED}" fill-opacity=".5"/>
<text x="30" y="43" style="font: 800 28px {FONT}; fill: {TEXT}; letter-spacing: 3px">{escape(title.upper())}</text>
<rect class="bl{u}" x="{30 + tw + 10}" y="22" width="12" height="24" fill="{RED}"/>
<rect x="{30 + tw + 40}" y="33" width="{w - 130 - tw}" height="2" fill="url(#ln{u})"/>
<rect class="sh{u}" x="0" y="32" width="120" height="4" fill="url(#shine{u})" opacity=".55"/>
<text x="{w - 4}" y="40" text-anchor="end" style="font: 600 12px {MONO}; fill: {RED}; letter-spacing: 2px">// {num}</text>
</svg>'''


def build(n, repo, desc, chips, featured=False):
    w, h, u = 490, 220, f"b{n}"
    lines = "".join(f'<text x="34" y="{110 + i * 20}" class="b{u}">{escape(t)}</text>' for i, t in enumerate(wrap(desc, 58)[:3]))
    x, chip_svg = 34, ""
    for c in chips:
        cw = len(c) * 7.4 + 22
        chip_svg += (f'<rect x="{x:.0f}" y="{h - 52}" width="{cw:.0f}" height="24" rx="12" fill="#1a0507" stroke="{RED}" stroke-opacity=".7"/>'
                     f'<text x="{x + cw / 2:.0f}" y="{h - 36}" text-anchor="middle" class="m{u}" fill="{PINK}" style="font-size:11.5px; font-weight:600">{escape(c)}</text>')
        x += cw + 8
    crown = (f'<rect x="{w - 132}" y="16" width="112" height="22" rx="4" fill="{RED}"/>'
             f'<text x="{w - 76}" y="31" text-anchor="middle" style="font: 800 11px {MONO}; fill: #fff; letter-spacing: 1.5px">★ FLAGSHIP</text>') if featured else ""
    body = f'''
  <rect x="16" y="44" width="{w - 32}" height="{h - 60}" rx="8" fill="#0d1117" fill-opacity="0.9" stroke="{RED}" stroke-opacity="{.6 if featured else .22}"/>
  <text x="34" y="80" style="font: 700 18px {MONO}; fill: {TEXT}">{escape(repo)}</text>
  {lines}
  {chip_svg}
  <text x="{w - 34}" y="{h - 36}" text-anchor="end" class="m{u}" fill="{PINK}" style="font-size:11px; font-weight:700">OPEN ▸</text>
  {crown}'''
    return frame(w, h, f"BUILD://0{n}", body, u)


ARSENAL = [
    ("CLOUD / DEVOPS", ["aws", "azure", "docker", "kubernetes", "terraform", "githubactions", "linux"]),
    ("LANGUAGES", ["python", "ts", "js", "kotlin", "html", "css"]),
    ("FRONTEND / MOBILE", ["react", "nextjs", "tailwind", "androidstudio", "figma"]),
    ("BACKEND / DATA", ["nodejs", "express", "postgres", "mongodb", "firebase", "vercel"]),
]


AI_TOOLS = [
    ("Claude Code", "si", "claude", None),
    ("Codex", "glyph", '<path d="M4 7l5 5-5 5" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 17h8" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>', None),
    ("Gemini", "si", "googlegemini", None),
    ("Antigravity", "glyph", '<path d="M5 14l7-7 7 7M5 20l7-7 7 7" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>', None),
    ("Ollama", "si", "ollama", "ffffff"),
    ("OpenRouter", "si", "openrouter", "ffffff"),
    ("OpenCode", "si", "opencode", "ffffff"),
    ("OmniRoute", "glyph", '<path d="M12 12L5 6M12 12l7-6M12 12v8" stroke="#fff" stroke-width="2"/><circle cx="12" cy="12" r="3" fill="#dc2626" stroke="#fff" stroke-width="1.5"/><circle cx="5" cy="6" r="2.4" fill="#fff"/><circle cx="19" cy="6" r="2.4" fill="#fff"/><circle cx="12" cy="20" r="2.4" fill="#fff"/>', None),
    ("VS Code", "sk", "vscode", None),
    ("Kiro", "glyph", '<path d="M6 21V10a6 6 0 0 1 12 0v11l-2-1.6-2 1.6-2-1.6-2 1.6-2-1.6z" fill="#fff"/><circle cx="10" cy="11" r="1.4" fill="#0d1117"/><circle cx="14" cy="11" r="1.4" fill="#0d1117"/>', None),
]

ARSENAL = [
    ("CLOUD / DEVOPS", ["aws", "azure", "docker", "kubernetes", "terraform", "githubactions", "linux"]),
    ("LANGUAGES", ["python", "ts", "js", "kotlin", "html", "css"]),
    ("FRONTEND / MOBILE", ["react", "nextjs", "tailwind", "androidstudio", "figma"]),
    ("BACKEND / DATA", ["nodejs", "express", "postgres", "mongodb", "firebase", "vercel"]),
]


def _fetch(url):
    import base64
    import urllib.request
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return base64.b64encode(urllib.request.urlopen(req, timeout=20).read()).decode()


def arsenal():
    w, u = 1000, "ars"
    size, gap, top, row_h, ai_h = 52, 14, 62, 78, 104
    h = top + ai_h + len(ARSENAL) * row_h + 10
    rows = []
    # AI / agentic row: labeled tiles
    rows.append(f'<rect x="24" y="{top}" width="{w - 48}" height="{ai_h - 12}" rx="8" fill="#14070a" fill-opacity="0.95" stroke="{RED}" stroke-opacity="0.6" class="pulse{u}"/>')
    rows.append(f'<text x="44" y="{top + 40}" class="tag{u}" style="font-size:12px">AI / AGENTIC</text>')
    rows.append(f'<text x="44" y="{top + 58}" class="m{u}" fill="{MUTED}" style="font-size:10.5px">agentic coding stack</text>')
    for j, (label, kind, data, color) in enumerate(AI_TOOLS):
        x, y = 230 + j * 72, top + 10
        rows.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="12" fill="#1c2128" stroke="{RED}" stroke-opacity="0.35"/>')
        if kind == "sk":
            src = _fetch(f"https://skillicons.dev/icons?i={data}&theme=dark")
            rows.append(f'<image x="{x}" y="{y}" width="{size}" height="{size}" href="data:image/svg+xml;base64,{src}"/>')
        elif kind == "si":
            src = _fetch(f"https://cdn.simpleicons.org/{data}" + (f"/{color}" if color else ""))
            rows.append(f'<image x="{x + 12}" y="{y + 12}" width="28" height="28" href="data:image/svg+xml;base64,{src}"/>')
        else:
            rows.append(f'<g transform="translate({x + 12}, {y + 12}) scale(1.1667)">{data}</g>')
        rows.append(f'<text x="{x + size / 2}" y="{y + size + 18}" text-anchor="middle" class="m{u}" fill="{TEXT}" style="font-size:10.5px">{label}</text>')
    for i, (label, icons) in enumerate(ARSENAL):
        y = top + ai_h + i * row_h
        rows.append(f'<rect x="24" y="{y}" width="{w - 48}" height="{row_h - 12}" rx="8" fill="#0d1117" fill-opacity="0.9" stroke="{RED}" stroke-opacity="0.2"/>')
        rows.append(f'<text x="44" y="{y + row_h / 2}" class="tag{u}" style="font-size:12px">{label}</text>')
        for j, name in enumerate(icons):
            data = _fetch(f"https://skillicons.dev/icons?i={name}&theme=dark")
            x = 250 + j * (size + gap)
            rows.append(f'<image x="{x}" y="{y + (row_h - 12 - size) / 2}" width="{size}" height="{size}" href="data:image/svg+xml;base64,{data}"/>')
    return frame(w, h, "SYS://ARSENAL", "".join(rows), u)


def workflow():
    w, h, u = 1000, 275, "flw"
    stages = [
        ("01 · SPEC", "Kiro · VS Code", "specs · steering · tasks"),
        ("02 · BUILD", "Claude Code · Codex", "OpenCode · Antigravity"),
        ("03 · MODELS", "OpenRouter · Ollama", "OmniRoute · Gemini"),
        ("04 · TEST", "Playwright · pytest", "evals · security review"),
        ("05 · SHIP", "GitHub Actions", "Terraform → AWS"),
    ]
    bw, gap, x0, y0, bh = 168, 28, 30, 92, 104
    parts = []
    line_y = y0 + bh / 2
    track_y = y0 + bh + 18
    parts.append(f'<line x1="{x0 + bw / 2}" y1="{track_y}" x2="{x0 + 4 * (bw + gap) + bw / 2}" y2="{track_y}" stroke="{RED}" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="4 6"/>')
    for i, (tag, main, sub) in enumerate(stages):
        x = x0 + i * (bw + gap)
        hi = i == 1
        parts.append(f'<rect x="{x}" y="{y0}" width="{bw}" height="{bh}" rx="8" fill="{"#2a0a0c" if hi else "#0d1117"}" fill-opacity="0.95" stroke="{RED}" stroke-opacity="{0.8 if hi else 0.35}" {"class=\"pulse" + u + "\"" if hi else ""}/>')
        parts.append(f'<rect x="{x}" y="{y0}" width="{bw}" height="4" rx="2" fill="{RED}"/>')
        parts.append(f'<text x="{x + bw / 2}" y="{y0 + 30}" text-anchor="middle" class="tag{u}">{escape(tag)}</text>')
        parts.append(f'<text x="{x + bw / 2}" y="{y0 + 58}" text-anchor="middle" style="font: 700 14px {FONT}; fill: {TEXT}">{escape(main)}</text>')
        parts.append(f'<text x="{x + bw / 2}" y="{y0 + 80}" text-anchor="middle" class="b{u}" style="font-size:12px">{escape(sub)}</text>')
        parts.append(f'<line x1="{x + bw / 2}" y1="{y0 + bh}" x2="{x + bw / 2}" y2="{track_y}" stroke="{RED}" stroke-opacity="0.45" stroke-width="1.5"/>')
        if i:
            ax = x - gap
            parts.append(f'<path d="M{ax + 6} {line_y} L{x - 4} {line_y}" stroke="{RED}" stroke-width="2.5"/><path d="M{x - 10} {line_y - 5} L{x - 3} {line_y} L{x - 10} {line_y + 5}" fill="none" stroke="{RED}" stroke-width="2.5"/>')
    # travelling packets
    total = 4 * (bw + gap)
    for k in range(3):
        parts.append(f'<circle cx="{x0 + bw / 2}" cy="{track_y}" r="5" fill="#fff" class="pk{u}" style="animation-delay:{k * 1.5}s"/>')
    parts.append(f'''<style>.pk{u} {{ opacity: 0; animation: pk{u} 4.5s linear infinite; filter: drop-shadow(0 0 6px {RED}); }}
@keyframes pk{u} {{ 0% {{ transform: translateX(0); opacity: 0; }} 5% {{ opacity: 1; }} 95% {{ opacity: 1; }} 100% {{ transform: translateX({total}px); opacity: 0; }} }}</style>''')
    parts.append(f'<text x="30" y="66" style="font: 400 13px {MONO}; fill: {MUTED}">$ how n0zzzy ships: <tspan fill="{PINK}">spec-driven, agent-built, human-approved</tspan><tspan class="blink{u}" fill="{RED}"> █</tspan></text>')
    parts.append(f'<text x="30" y="{h - 22}" style="font: 400 12px {MONO}; fill: {MUTED}">humans own the spec and the approve-deploy gate · agents do the rest</text>')
    return frame(w, h, "SYS://AGENTIC_WORKFLOW", "".join(parts), u)


def harness():
    w, h, u = 1000, 470, "hrn"
    left = [
        ("GUARDRAILS", "Bedrock Guardrails", "prompt-injection defense · PII"),
        ("HUMAN-IN-THE-LOOP", "approval gates", "APPROVE DEPLOY · review queues"),
        ("EVALUATION", "LLM-as-a-Judge", "AgentCore evals · eval datasets"),
        ("OBSERVABILITY", "OpenTelemetry · Langfuse", "CloudWatch · X-Ray traces"),
    ]
    right = [
        ("TOOLS / MCP", "AgentCore Gateway · MCP", "Code Interpreter · Browser"),
        ("MEMORY", "session state", "semantic facts · summaries"),
        ("KNOWLEDGE / RAG", "Bedrock KB · S3 Vectors", "Milvus · parallel retrieval"),
        ("PERMISSIONS", "per-agent boundaries", "least-privilege IAM · JWT/OAuth"),
    ]
    tw, th, ty0, tgap = 300, 74, 92, 14
    cx, cy = w / 2, ty0 + 2 * (th + tgap) - tgap / 2
    parts = [f'<text x="30" y="62" style="font: 400 13px {MONO}; fill: {MUTED}">$ harness engineering: <tspan fill="{PINK}">what turns a chatbot into a production agent</tspan></text>']

    def tile(x, y, tag, main, sub, side):
        ex = x + tw if side == "L" else x
        bend = -60 if side == "L" else 60
        end = -92 if side == "L" else 92
        parts.append(f'<path d="M{ex} {y + th / 2} C {cx + bend} {y + th / 2}, {cx + bend} {cy}, {cx + end} {cy}" fill="none" stroke="{RED}" stroke-opacity="0.4" stroke-width="1.5" class="flow{u}"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="8" fill="#0d1117" fill-opacity="0.95" stroke="{RED}" stroke-opacity="0.3"/>')
        parts.append(f'<rect x="{x if side == "L" else x + tw - 4}" y="{y}" width="4" height="{th}" rx="2" fill="{RED}"/>')
        parts.append(f'<text x="{x + 18}" y="{y + 24}" class="tag{u}">{escape(tag)}</text>')
        parts.append(f'<text x="{x + 18}" y="{y + 46}" style="font: 700 14px {FONT}; fill: {TEXT}">{escape(main)}</text>')
        parts.append(f'<text x="{x + 18}" y="{y + 64}" class="b{u}" style="font-size:12px">{escape(sub)}</text>')

    for i, t in enumerate(left):
        tile(28, ty0 + i * (th + tgap), *t, "L")
    for i, t in enumerate(right):
        tile(w - 28 - tw, ty0 + i * (th + tgap), *t, "R")
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="96" fill="none" stroke="{RED}" stroke-opacity="0.3" stroke-dasharray="3 7" class="spin{u}" style="transform-origin:{cx}px {cy}px"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="78" fill="#2a0a0c" stroke="{RED}" stroke-width="2" class="pulse{u}"/>')
    parts.append(f'<text x="{cx}" y="{cy - 30}" text-anchor="middle" class="tag{u}">AGENT CORE</text>')
    for k, line in enumerate(["↻ plan", "act · tools", "observe", "reflect"]):
        parts.append(f'<text x="{cx}" y="{cy - 8 + k * 17}" text-anchor="middle" style="font: 600 13px {MONO}; fill: {TEXT if k % 2 == 0 else PINK}">{escape(line)}</text>')
    parts.append(f'<text x="{cx}" y="{cy + 116}" text-anchor="middle" class="m{u}" fill="{MUTED}" style="font-size:11.5px">model via LiteLLM / OpenRouter</text>')
    parts.append(
        f"<style>.flow{u} {{ stroke-dasharray: 5 6; animation: fl{u} 1.2s linear infinite; }} @keyframes fl{u} {{ to {{ stroke-dashoffset: -11; }} }}"
        f" .spin{u} {{ animation: sp{u} 18s linear infinite; }} @keyframes sp{u} {{ to {{ transform: rotate(360deg); }} }}</style>"
    )
    return frame(w, h, "SYS://HARNESS", "".join(parts), u)


ROLES = [
    ("Orchestrator / Router", "Claude Haiku 4.5", "fast, cheap routing + workflow state", "novamart"),
    ("Specialist workers", "Claude Sonnet 4.5", "tool use · reasoning · temp 0.1", "novamart"),
    ("LLM-as-a-Judge", "Claude Sonnet 4.5", "scores agent outputs in evals", "eks"),
    ("Managed agent backbone", "Amazon Nova Lite", "low-cost Bedrock serving", "eks"),
    ("Self-hosted agent", "Qwen 2.5 3B · vLLM", "open-source on AWS Inferentia", "eks"),
    ("Tool-calling assistant", "gpt-4.1-mini", "Azure AI Foundry multi-tool", "azure"),
    ("Embeddings / RAG", "Titan Embed v2 · MiniLM", "vector search & retrieval", "novamart · eks"),
    ("Coding agents", "Claude Code · Codex", "agentic software delivery", "daily driver"),
]


def roles():
    w, u = 1000, "rol"
    rh, top = 40, 92
    h = top + len(ROLES) * rh + 40
    cols = [(40, "AGENT ROLE"), (300, "MODEL"), (540, "WHY THIS MODEL"), (850, "WHERE")]
    parts = [f'<text x="30" y="62" style="font: 400 13px {MONO}; fill: {MUTED}">$ right model for the right role: <tspan fill="{PINK}">cost · latency · reasoning</tspan></text>']
    parts.append(f'<rect x="24" y="{top - 8}" width="{w - 48}" height="30" rx="6" fill="#2a0a0c"/>')
    for x, t in cols:
        parts.append(f'<text x="{x}" y="{top + 12}" class="tag{u}">{t}</text>')
    for i, (role, model, why, where) in enumerate(ROLES):
        y = top + 28 + i * rh
        parts.append(f'<rect x="24" y="{y}" width="{w - 48}" height="{rh - 6}" rx="6" fill="#0d1117" fill-opacity="{0.95 if i % 2 else 0.75}" stroke="{RED}" stroke-opacity="0.15"/>')
        parts.append(f'<text x="40" y="{y + 22}" style="font: 600 14px {FONT}; fill: {TEXT}">{escape(role)}</text>')
        parts.append(f'<rect x="294" y="{y + 7}" width="{len(model) * 7.8 + 22:.0f}" height="20" rx="10" fill="#1a0507" stroke="{RED}" stroke-opacity="0.7"/>')
        parts.append(f'<text x="305" y="{y + 21}" class="m{u}" fill="{PINK}" style="font-size:12px; font-weight:700">{escape(model)}</text>')
        parts.append(f'<text x="540" y="{y + 22}" class="b{u}">{escape(why)}</text>')
        parts.append(f'<text x="850" y="{y + 22}" class="m{u}" fill="{MUTED}" style="font-size:11.5px">{escape(where)}</text>')
    return frame(w, h, "SYS://ROLES_X_MODELS", "".join(parts), u)


def _glyph(kind):
    c, r_ = "#fca5a5", "#dc2626"

    def n(x, y, r=5, f=r_):
        return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{f}"/>'

    def ln(x1, y1, x2, y2):
        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="1.5"/>'

    if kind == "sup":
        return ln(30, 8, 10, 36) + ln(30, 8, 30, 36) + ln(30, 8, 50, 36) + n(30, 8, 7) + n(10, 36, 4, c) + n(30, 36, 4, c) + n(50, 36, 4, c)
    if kind == "a2a":
        return ln(10, 22, 30, 6) + ln(30, 6, 50, 22) + ln(10, 22, 30, 38) + ln(30, 38, 50, 22) + ln(10, 22, 50, 22) + n(10, 22) + n(50, 22) + n(30, 6, 4, c) + n(30, 38, 4, c)
    if kind == "par":
        return ln(6, 22, 28, 6) + ln(6, 22, 28, 38) + ln(28, 6, 54, 22) + ln(28, 38, 54, 22) + n(6, 22) + n(28, 6, 4, c) + n(28, 38, 4, c) + n(54, 22)
    if kind == "evt":
        return f'<rect x="4" y="18" width="52" height="8" rx="4" fill="{r_}"/>' + ln(14, 6, 14, 18) + ln(30, 26, 30, 38) + ln(46, 6, 46, 18) + n(14, 6, 4, c) + n(30, 38, 4, c) + n(46, 6, 4, c)
    if kind == "rtr":
        return ln(6, 22, 26, 22) + ln(26, 22, 52, 6) + ln(26, 22, 52, 22) + ln(26, 22, 52, 38) + f'<polygon points="26,12 36,22 26,32 16,22" fill="{r_}"/>' + n(6, 22, 4, c) + n(52, 6, 4, c) + n(52, 22, 4, c) + n(52, 38, 4, c)
    return ln(4, 22, 56, 22) + n(8, 22, 4, c) + n(20, 22, 4, c) + f'<rect x="27" y="10" width="16" height="24" rx="3" fill="{r_}"/><path d="M32 16 v12 M38 16 v12" stroke="#fff" stroke-width="2.5"/>' + n(52, 22, 4, c)


PATTERNS = [
    ("sup", "Supervisor → Specialists", "orchestrator routes to workers", "novamart · kiro-sdlc-harness"),
    ("a2a", "Agent-to-Agent (A2A)", "distributed agents over A2A + MCP", "production-ready-ai-agents-eks"),
    ("par", "Parallel Fan-out / Fan-in", "parallel RAG · parallel Lambdas", "novamart · step-functions"),
    ("evt", "Event-driven Choreography", "agents react to bus events", "aws-multi-agent-choreography"),
    ("rtr", "Router / Classifier", "classify → route to a handler", "bedrock-customer-support-flow"),
    ("hitl", "Human-gated Pipeline", "agents pause for human approval", "kiro-sdlc · step-functions"),
]


def patterns():
    w, h, u = 1000, 330, "pat"
    tw, th = 306, 104
    parts = [f'<text x="30" y="62" style="font: 400 13px {MONO}; fill: {MUTED}">$ orchestration patterns I have shipped:</text>']
    for i, (g, name, desc, where) in enumerate(PATTERNS):
        x, y = 28 + (i % 3) * (tw + 13), 84 + (i // 3) * (th + 14)
        parts.append(f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="8" fill="#0d1117" fill-opacity="0.95" stroke="{RED}" stroke-opacity="0.3"/>')
        parts.append(f'<rect x="{x + 14}" y="{y + 14}" width="76" height="76" rx="8" fill="#14070a" stroke="{RED}" stroke-opacity="0.4"/>')
        parts.append(f'<g transform="translate({x + 22}, {y + 30})">{_glyph(g)}</g>')
        parts.append(f'<text x="{x + 104}" y="{y + 36}" style="font: 700 14px {FONT}; fill: {TEXT}">{escape(name)}</text>')
        parts.append(f'<text x="{x + 104}" y="{y + 58}" class="b{u}" style="font-size:12px">{escape(desc)}</text>')
        parts.append(f'<text x="{x + 104}" y="{y + 82}" class="m{u}" fill="{PINK}" style="font-size:10.5px">{escape(where)}</text>')
    return frame(w, h, "SYS://ORCHESTRATION", "".join(parts), u)


ACH_GLYPHS = {
    "trophy": '<path d="M7 3h10v4a5 5 0 0 1-10 0z" fill="#fff"/><path d="M5 4H3v2a3 3 0 0 0 4 2.8M19 4h2v2a3 3 0 0 1-4 2.8" fill="none" stroke="#fff" stroke-width="1.6"/><rect x="10.5" y="12" width="3" height="4" fill="#fff"/><rect x="7" y="16" width="10" height="3" rx="1" fill="#fff"/>',
    "cloud": ICONS["cloud"],
    "ms": ICONS["ms"],
    "cap": '<path d="M12 4L1 9l11 5 9-4.1V16h2V9z" fill="#fff"/><path d="M5 12.2V16c0 1.7 3.1 3 7 3s7-1.3 7-3v-3.8l-7 3.2z" fill="#fff"/>',
    "nodes": '<path d="M12 6v5M12 11L5 18M12 11l7 7M12 11v7" stroke="#fff" stroke-width="1.8"/><circle cx="12" cy="5" r="3" fill="#fff"/><circle cx="5" cy="19" r="2.4" fill="#fff"/><circle cx="12" cy="19" r="2.4" fill="#fff"/><circle cx="19" cy="19" r="2.4" fill="#fff"/>',
    "term": '<rect x="2" y="4" width="20" height="16" rx="2" fill="none" stroke="#fff" stroke-width="1.8"/><path d="M6 9l3 3-3 3M11 15h6" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>',
}

ACHIEVEMENTS = [
    ("trophy", "Hackathon Champion", "Rank 1 · AWS QuickQuest", "LEGENDARY"),
    ("cloud", "AWS Certified", "AI Practitioner", "EPIC"),
    ("ms", "Microsoft Certified", "Fabric Data Engineer", "EPIC"),
    ("cap", "AWS AI & ML Scholar", "top 4,500 globally", "EPIC"),
    ("nodes", "Multi-Agent Architect", "6 orchestration patterns", "RARE"),
    ("term", "Agentic Coder", "Claude Code · Codex · Kiro", "RARE"),
]


def achievements():
    w, h, u = 1000, 190, "ach"
    tw, gap = 152, 9
    parts = []
    for i, (g, title, sub, rarity) in enumerate(ACHIEVEMENTS):
        x, y = 24 + i * (tw + gap), 48
        legendary = rarity == "LEGENDARY"
        cls = f'class="pulse{u}"' if legendary else ""
        fill = "#2a0a0c" if legendary else "#0d1117"
        parts.append(f'<rect x="{x}" y="{y}" width="{tw}" height="124" rx="8" fill="{fill}" fill-opacity="0.95" stroke="{RED}" stroke-opacity="{0.9 if legendary else 0.3}" {cls}/>')
        parts.append(f'<polygon points="{x + tw / 2},{y + 10} {x + tw / 2 + 24},{y + 24} {x + tw / 2 + 24},{y + 52} {x + tw / 2},{y + 66} {x + tw / 2 - 24},{y + 52} {x + tw / 2 - 24},{y + 24}" fill="{RED}"/>')
        parts.append(f'<g transform="translate({x + tw / 2 - 12}, {y + 26})">{ACH_GLYPHS[g]}</g>')
        parts.append(f'<text x="{x + tw / 2}" y="{y + 86}" text-anchor="middle" style="font: 700 12.5px {FONT}; fill: {TEXT}">{escape(title)}</text>')
        parts.append(f'<text x="{x + tw / 2}" y="{y + 102}" text-anchor="middle" class="b{u}" style="font-size:10.5px">{escape(sub)}</text>')
        parts.append(f'<text x="{x + tw / 2}" y="{y + 117}" text-anchor="middle" class="m{u}" fill="{PINK if legendary else RED}" style="font-size:9.5px; font-weight:700; letter-spacing:1.5px">◆ {rarity}</text>')
    parts.append(f'<text x="{w - 24}" y="28" text-anchor="end" class="m{u}" fill="{MUTED}" style="font-size:11px">6 / 6 unlocked</text>')
    return frame(w, h, "ACHIEVEMENTS://UNLOCKED", "".join(parts), u)


WOLF = "M28 -4 C 46 4, 62 18, 72 28 L 78 25 L 90 8 L 94 24 L 97 36 C 104 44, 108 52, 112 60 L 120 64 L 117 70 L 126 76 L 121 81 L 130 90 C 150 120, 172 160, 172 200 C 190 204, 206 222, 206 252 C 190 246, 176 246, 162 254 L 160 258 L 84 258 C 72 258, 70 248, 82 246 C 84 220, 84 196, 82 176 C 80 156, 74 138, 66 122 L 70 116 L 62 110 L 66 104 L 58 98 C 54 86, 52 76, 50 66 C 46 54, 40 44, 32 34 L 14 14 L 40 24 L 24 2 Z"


def mini(n, title, sub):
    w, h, u = 320, 92, f"m{n}"
    body = f'''
  <rect x="12" y="38" width="{w - 24}" height="{h - 50}" rx="6" fill="#0d1117" fill-opacity="0.9" stroke="{RED}" stroke-opacity="0.22"/>
  <text x="26" y="60" style="font: 700 14px {FONT}; fill: {TEXT}">{escape(title)}</text>
  <text x="26" y="76" class="b{u}" style="font-size:11.5px">{escape(sub)}</text>
  <text x="{w - 24}" y="60" text-anchor="end" class="m{u}" fill="{PINK}" style="font-size:11px; font-weight:700">▸</text>'''
    return frame(w, h, f"MORE://0{n}", body, u)


def footer():
    w, h, u = 1000, 190, "ft"
    body = f'''
  <g clip-path="url(#mclipft)"><rect x="780" y="50" width="160" height="160" fill="url(#moonft)"/>
  <rect x="780" y="112" width="160" height="4" fill="#06080c"/><rect x="780" y="126" width="160" height="6" fill="#06080c"/><rect x="780" y="142" width="160" height="8" fill="#06080c"/></g>
  <path d="M700 190 L760 166 L800 176 L840 160 L900 170 L950 158 L1000 168 L1000 190 Z" fill="#05070a"/>
  <g transform="translate(822, 66) scale(0.4)"><path fill="#05070a" d="{WOLF}"/></g>
  <text x="40" y="84" style="font: 800 30px {FONT}; fill: {TEXT}; letter-spacing: 1px">"I have no enemies."</text>
  <text x="40" y="114" class="m{u}" fill="{PINK}">n0zzzy@ph:~$ exit 0<tspan class="blink{u}" fill="{RED}"> █</tspan></text>
  <text x="40" y="150" class="m{u}" fill="{MUTED}" style="font-size:12px">Cloud · DevOps · Full-Stack · AI Agents  //  Philippines</text>'''
    svg = frame(w, h, "EOF://N0ZZZY", body, u)
    moon = f'<radialGradient id="moonft" cx=".5" cy=".3" r=".7"><stop offset="0" stop-color="#f87171"/><stop offset="1" stop-color="#991b1b"/></radialGradient><clipPath id="mclipft"><circle cx="860" cy="128" r="70"/></clipPath>'
    return svg.replace("<defs>", "<defs>" + moon, 1)


def main():
    files = {
        "footer.svg": footer(),
        "more-1.svg": mini(1, "EKS + Karpenter Lab", "Gateway API · Karpenter · EBS · Fluent Bit"),
        "more-2.svg": mini(2, "Azure AI Foundry Agent", "Code Interpreter · Web Search · streaming"),
        "more-3.svg": mini(3, "Bedrock Flows Router", "classify · FAQ · bug tickets · guardrails"),
        "more-4.svg": mini(4, "PH Flood Control Dashboard", "DuckDB-WASM · sub-100 ms · React"),
        "more-5.svg": mini(5, "Step Functions Orchestration", "parallel agents · human-in-the-loop"),
        "more-6.svg": mini(6, "EventBridge Choreography", "event-driven agents · pub/sub"),
        "h-wins.svg": heading("wins", "Wins", "01"),
        "h-certs.svg": heading("certs", "Certifications", "02"),
        "h-arsenal.svg": heading("ars", "Arsenal", "03"),
        "h-agentic.svg": heading("agentic", "Agentic Engineering", "04"),
        "panel-achievements.svg": achievements(),
        "panel-harness.svg": harness(),
        "panel-roles.svg": roles(),
        "panel-patterns.svg": patterns(),
        "h-builds-v2.svg": heading("builds", "Featured Builds", "05"),
        "h-stats-v2.svg": heading("stats", "Stats", "06"),
        "panel-arsenal-v4.svg": arsenal(),
        "panel-flow-v2.svg": workflow(),
        "build-1.svg": build(1, "kiro-sdlc-agent-harness", "An orchestrator drives 7 specialist AI agents through the full SDLC, from a plain-English request to a live, deployed AWS app, with human approval gates.", ["Kiro", "Multi-Agent", "AWS", "Terraform"], True),
        "build-2.svg": build(2, "novamart-multi-agent-agentcore", "5-agent customer support with parallel multi-agent RAG, guardrails, shared state, and CloudWatch/X-Ray observability on Bedrock AgentCore.", ["Python", "AgentCore", "Strands", "RAG"]),
        "build-3.svg": build(3, "production-ready-ai-agents-eks", "Enterprise AI agent platform on EKS + Bedrock: self-managed vs managed tracks behind a model-agnostic LiteLLM plane.", ["EKS", "Kubernetes", "LiteLLM", "Terraform"]),
        "build-4.svg": build(4, "cloudops-sentry", "Autonomous DevOps & SRE agent that prevents incidents before they happen. Built for the DevKada x Clanker Cloud challenge.", ["Python", "AI Agent", "SRE"]),
        "build-5.svg": build(5, "ai-customer-support-agent", "Support agent with order tracking & refunds via Gateway/Lambda, RAG, Code Interpreter, web browsing, and long-term memory.", ["Strands", "AgentCore", "Lambda"]),
        "build-6.svg": build(6, "pawfeed-smart-pet-feeder", "Smart pet feeder web + installable PWA with Playwright tests, Allure reports, and CI/CD to Vercel. Live demo available.", ["PWA", "Playwright", "Allure", "Vercel"]),
        "panel-whoami-v2.svg": whoami(),
        "win-1.svg": win(1, "1ST", "RANK 1 OVERALL", "+ Best in Technical Solution",
                         "QuickQuest Finale: Build Responsibly · AWS Office, BGC",
                         "Team EPIC 2 built an AI-powered Deployment Checklist Bot on Amazon Quick Suite: 50+ checkpoints across 9 release domains"),
        "win-2.svg": win(2, "2ND", "2ND PLACE", "Kiro Agent Orchestration",
                         "AI Playgrounds · eCloudvalley Philippines, BGC",
                         "Built software end-to-end with agent orchestration using Kiro, from SDLC to AIDLC"),
        "win-3.svg": win(3, "4TH", "4TH PLACE", "EdTek Con 2026 AI Hackathon",
                         "Mission LearnPossible 2 · representing NU Fairview",
                         "Built Linaw, an AI-powered, privacy-first anti-bullying companion for students"),
        "cert-aws.svg": cert("aws", "cloud", "AWS CERTIFIED", "AI Practitioner", "AIF-C01", "GenAI · Bedrock · Responsible AI"),
        "cert-ms.svg": cert("ms", "ms", "MICROSOFT CERTIFIED", "Fabric Data Engineer Associate", "DP-700", "ETL/ELT · Lakehouse · RTI"),
        "cert-udacity.svg": cert("udacity", "u", "UDACITY NANODEGREE", "Future AWS Agent Engineer", "AWS AI & ML Scholar", "top 4,500 globally"),
        "cert-besa.svg": cert("besa", "cloud", "BESA CLOUD ACADEMY", "Agentic AI: PoC → Production", "6 weeks", "production agents on AWS"),
    }
    for name, svg in files.items():
        (OUT / name).write_text(svg, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
