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
        ("🔁", "Automating everything", " with GitHub Actions"),
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


def arsenal():
    import base64
    import urllib.request
    w, u = 1000, "ars"
    size, gap, top, row_h = 52, 14, 62, 78
    h = top + len(ARSENAL) * row_h + 10
    rows = []
    for i, (label, icons) in enumerate(ARSENAL):
        y = top + i * row_h
        rows.append(f'<rect x="24" y="{y}" width="{w - 48}" height="{row_h - 12}" rx="8" fill="#0d1117" fill-opacity="0.9" stroke="{RED}" stroke-opacity="0.2"/>')
        rows.append(f'<text x="44" y="{y + row_h / 2}" class="tag{u}" style="font-size:12px">{label}</text>')
        for j, name in enumerate(icons):
            req = urllib.request.Request(f"https://skillicons.dev/icons?i={name}&theme=dark", headers={"User-Agent": "Mozilla/5.0"})
            data = base64.b64encode(urllib.request.urlopen(req, timeout=20).read()).decode()
            x = 250 + j * (size + gap)
            rows.append(f'<image x="{x}" y="{y + (row_h - 12 - size) / 2}" width="{size}" height="{size}" href="data:image/svg+xml;base64,{data}"/>')
    return frame(w, h, "SYS://ARSENAL", "".join(rows), u)


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
        "h-builds.svg": heading("builds", "Featured Builds", "04"),
        "h-stats.svg": heading("stats", "Stats", "05"),
        "panel-arsenal.svg": arsenal(),
        "build-1.svg": build(1, "kiro-sdlc-agent-harness", "An orchestrator drives 7 specialist AI agents through the full SDLC, from a plain-English request to a live, deployed AWS app, with human approval gates.", ["Kiro", "Multi-Agent", "AWS", "Terraform"], True),
        "build-2.svg": build(2, "novamart-multi-agent-agentcore", "5-agent customer support with parallel multi-agent RAG, guardrails, shared state, and CloudWatch/X-Ray observability on Bedrock AgentCore.", ["Python", "AgentCore", "Strands", "RAG"]),
        "build-3.svg": build(3, "production-ready-ai-agents-eks", "Enterprise AI agent platform on EKS + Bedrock: self-managed vs managed tracks behind a model-agnostic LiteLLM plane.", ["EKS", "Kubernetes", "LiteLLM", "Terraform"]),
        "build-4.svg": build(4, "cloudops-sentry", "Autonomous DevOps & SRE agent that prevents incidents before they happen. Built for the DevKada x Clanker Cloud challenge.", ["Python", "AI Agent", "SRE"]),
        "build-5.svg": build(5, "ai-customer-support-agent", "Support agent with order tracking & refunds via Gateway/Lambda, RAG, Code Interpreter, web browsing, and long-term memory.", ["Strands", "AgentCore", "Lambda"]),
        "build-6.svg": build(6, "pawfeed-smart-pet-feeder", "Smart pet feeder web + installable PWA with Playwright tests, Allure reports, and CI/CD to Vercel. Live demo available.", ["PWA", "Playwright", "Allure", "Vercel"]),
        "panel-whoami.svg": whoami(),
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
