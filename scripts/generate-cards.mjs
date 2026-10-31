// Generates themed SVG stat cards for the profile README.
// Usage: GITHUB_TOKEN=... GH_USER=n0zzzy node scripts/generate-cards.mjs [outDir]
import { mkdirSync, writeFileSync } from "node:fs";

const token = process.env.GITHUB_TOKEN;
const login = process.env.GH_USER || "n0zzzy";
const outDir = process.argv[2] || "dist";
if (!token) throw new Error("GITHUB_TOKEN is required");

const RED = "#dc2626";
const BG = "#0d1117";
const BORDER = "#30363d";
const TEXT = "#e6edf3";
const MUTED = "#8b949e";
const MONO = "'Fira Code', Consolas, monospace";
const FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Sans-Serif";

async function gql(query, variables) {
  const res = await fetch("https://api.github.com/graphql", {
    method: "POST",
    headers: { Authorization: `bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify({ query, variables }),
  });
  const json = await res.json();
  if (json.errors) throw new Error(JSON.stringify(json.errors));
  return json.data;
}

const data = await gql(
  `query($login: String!) {
    user(login: $login) {
      createdAt
      followers { totalCount }
      contributionsCollection {
        contributionCalendar {
          totalContributions
          weeks { contributionDays { date contributionCount } }
        }
        totalCommitContributions
        totalPullRequestContributions
        totalIssueContributions
        restrictedContributionsCount
      }
      repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
        totalCount
        nodes {
          stargazerCount
          languages(first: 10, orderBy: { field: SIZE, direction: DESC }) {
            edges { size node { name color } }
          }
        }
      }
    }
  }`,
  { login }
);

const u = data.user;
const cc = u.contributionsCollection;
const repos = u.repositories.nodes;
const years = Math.max(1, Math.floor((Date.now() - new Date(u.createdAt)) / (365.25 * 864e5)));

const stats = [
  ["Contributions (last year)", cc.contributionCalendar.totalContributions + cc.restrictedContributionsCount],
  ["Commits (last year)", cc.totalCommitContributions],
  ["Pull Requests", cc.totalPullRequestContributions],
  ["Public Repositories", u.repositories.totalCount],
  ["Stars Earned", repos.reduce((s, r) => s + r.stargazerCount, 0)],
  ["Followers", u.followers.totalCount],
].filter(([label, value]) => label !== "Stars Earned" || value > 0);

const langTotals = new Map();
for (const r of repos) {
  for (const e of r.languages.edges) {
    const cur = langTotals.get(e.node.name) || { size: 0, color: e.node.color || MUTED };
    cur.size += e.size;
    langTotals.set(e.node.name, cur);
  }
}
const langs = [...langTotals.entries()].sort((a, b) => b[1].size - a[1].size).slice(0, 6);
const langSum = langs.reduce((s, [, v]) => s + v.size, 0) || 1;

const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

const frame = (w, h, title, body) => `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">
<defs>
  <linearGradient id="cbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#06080c"/><stop offset=".6" stop-color="#0b0a10"/><stop offset="1" stop-color="#1c0609"/></linearGradient>
  <radialGradient id="cglow" cx="1" cy="0" r=".9"><stop offset="0" stop-color="${RED}" stop-opacity=".25"/><stop offset="1" stop-color="${RED}" stop-opacity="0"/></radialGradient>
  <pattern id="cgrid" width="26" height="26" patternUnits="userSpaceOnUse"><path d="M26 0 L0 0 0 26" fill="none" stroke="${RED}" stroke-opacity=".07"/></pattern>
  <pattern id="cscan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" fill-opacity=".35"/></pattern>
  <clipPath id="cclip"><rect width="${w}" height="${h}" rx="10"/></clipPath>
</defs>
<style>
  .t { font: 600 11px ${MONO}; fill: ${RED}; letter-spacing: 2px; text-transform: uppercase; }
  .l { font: 400 13px ${FONT}; fill: ${MUTED}; }
  .v { font: 700 14px ${FONT}; fill: ${TEXT}; }
  .big { font: 800 40px ${FONT}; fill: ${TEXT}; }
  .fade { animation: fade .6s ease-out; }
  .sweep { animation: sweep 5s linear infinite; }
  .pulse { animation: pulse 2.6s ease-in-out infinite; }
  @keyframes fade { from { opacity: 0; transform: translateX(-6px); } to { opacity: 1; transform: none; } }
  @keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
  @keyframes ring { from { stroke-dashoffset: 251; } }
  @keyframes sweep { from { transform: translateY(-40px); } to { transform: translateY(${h + 40}px); } }
  @keyframes pulse { 50% { stroke-opacity: .25; } }
</style>
<g clip-path="url(#cclip)">
  <rect width="${w}" height="${h}" fill="url(#cbg)"/>
  <rect width="${w}" height="${h}" fill="url(#cgrid)"/>
  <rect width="${w}" height="${h}" fill="url(#cglow)"/>
  <rect width="${w}" height="${h}" fill="url(#cscan)"/>
  <rect class="sweep" width="${w}" height="40" fill="${RED}" fill-opacity=".05"/>
</g>
<rect x=".5" y=".5" width="${w - 1}" height="${h - 1}" rx="10" fill="none" stroke="${RED}" stroke-opacity=".45" class="pulse"/>
<g stroke="${RED}" stroke-width="3" fill="none"><path d="M2 20 V2 H20"/><path d="M${w - 20} 2 H${w - 2} V20"/><path d="M2 ${h - 20} V${h - 2} H20"/><path d="M${w - 20} ${h - 2} H${w - 2} V${h - 20}"/></g>
<text x="25" y="32" class="t">${esc(title)}</text>
${body}
</svg>`;

// --- stats card ---
const statRows = stats
  .map(
    ([label, value], i) => `<g class="fade" transform="translate(25, ${62 + i * 25})">
  <rect y="-9" width="6" height="6" rx="1" fill="${RED}"/>
  <text x="16" y="0" class="l">${esc(label)}</text>
  <text x="250" y="0" class="v" text-anchor="end">${value.toLocaleString("en-US")}</text>
</g>`
  )
  .join("\n");
const statsSvg = frame(
  495,
  215,
  `${login} // github stats`,
  `${statRows}
<g transform="translate(395, 115)">
  <circle r="40" fill="none" stroke="${BORDER}" stroke-width="6"/>
  <circle r="40" fill="none" stroke="${RED}" stroke-width="6" stroke-linecap="round"
    stroke-dasharray="251" stroke-dashoffset="${251 - Math.min(1, years / 10) * 251}"
    transform="rotate(-90)" style="animation: ring 1.2s ease-out"/>
  <text y="12" class="big" text-anchor="middle">${years}</text>
  <text y="62" class="l" text-anchor="middle">years on GitHub</text>
</g>`
);

// --- languages card ---
let x = 0;
const barW = 445;
const barSegs = langs
  .map(([, v]) => {
    const w = (v.size / langSum) * barW;
    const seg = `<rect x="${x.toFixed(2)}" y="0" width="${w.toFixed(2)}" height="10" fill="${v.color}"/>`;
    x += w;
    return seg;
  })
  .join("");
const langRows = langs
  .map(([name, v], i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const pct = ((v.size / langSum) * 100).toFixed(1);
    return `<g class="fade" transform="translate(${25 + col * 230}, ${108 + row * 28})">
  <circle cx="5" cy="-4" r="5" fill="${v.color}"/>
  <text x="18" y="0" class="v">${esc(name)}</text>
  <text x="200" y="0" class="l" text-anchor="end">${pct}%</text>
</g>`;
  })
  .join("\n");
const langsSvg = frame(
  495,
  215,
  "most used languages",
  `<defs><clipPath id="bar"><rect width="${barW}" height="10" rx="5"/></clipPath></defs>
<g transform="translate(25, 60)">
  <g clip-path="url(#bar)"><g style="transform-origin: 0 0; animation: grow 1s ease-out">${barSegs}</g></g>
</g>
${langRows}`
);

// --- activity graph (last 31 days) ---
const days = cc.contributionCalendar.weeks.flatMap((w) => w.contributionDays).slice(-31);
const AW = 990, AH = 300, PL = 50, PR = 25, PT = 70, PB = 45;
const maxC = Math.max(4, ...days.map((d) => d.contributionCount));
const step = (AW - PL - PR) / (days.length - 1);
const pts = days.map((d, i) => [PL + i * step, PT + (1 - d.contributionCount / maxC) * (AH - PT - PB)]);
const line = pts.map(([px, py], i) => `${i ? "L" : "M"}${px.toFixed(1)} ${py.toFixed(1)}`).join(" ");
const area = `${line} L${pts.at(-1)[0].toFixed(1)} ${AH - PB} L${PL} ${AH - PB} Z`;
const total31 = days.reduce((s, d) => s + d.contributionCount, 0);
const gridLines = [0, 0.25, 0.5, 0.75, 1]
  .map((f) => {
    const gy = PT + f * (AH - PT - PB);
    return `<line x1="${PL}" y1="${gy}" x2="${AW - PR}" y2="${gy}" stroke="${BORDER}" stroke-dasharray="3 4"/>
<text x="${PL - 10}" y="${gy + 4}" class="l" text-anchor="end">${Math.round(maxC * (1 - f))}</text>`;
  })
  .join("\n");
const xLabels = days
  .map((d, i) => (i % 5 === 0 || i === days.length - 1 ? `<text x="${pts[i][0]}" y="${AH - PB + 22}" class="l" text-anchor="middle">${d.date.slice(5).replace("-", "/")}</text>` : ""))
  .join("");
const dots = pts
  .map(([px, py], i) => (days[i].contributionCount ? `<circle cx="${px}" cy="${py}" r="3.5" fill="${BG}" stroke="${RED}" stroke-width="2"/>` : ""))
  .join("");
const activitySvg = frame(
  AW,
  AH,
  `contribution activity // last 31 days — ${total31} contributions`,
  `<defs><linearGradient id="af" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${RED}" stop-opacity="0.45"/><stop offset="1" stop-color="${RED}" stop-opacity="0"/></linearGradient></defs>
${gridLines}
<path d="${area}" fill="url(#af)"/>
<path d="${line}" fill="none" stroke="${RED}" stroke-width="2.5" stroke-linejoin="round" stroke-dasharray="4000" style="animation: draw 2s ease-out"/>
${dots}
${xLabels}
<style>@keyframes draw { from { stroke-dashoffset: 4000; } to { stroke-dashoffset: 0; } }</style>`
);

// --- trophies ---
const tier = (v, [s, a, b, c]) => (v >= s ? "S" : v >= a ? "A" : v >= b ? "B" : v >= c ? "C" : "?");
const trophies = [
  ["Contributor", "contributions", stats[0][1], [1000, 500, 200, 50]],
  ["Committer", "commits", cc.totalCommitContributions, [500, 200, 100, 30]],
  ["Builder", "public repos", u.repositories.totalCount, [50, 30, 15, 5]],
  ["Polyglot", "languages", langTotals.size, [10, 7, 4, 2]],
  ["Veteran", "years", years, [8, 5, 3, 1]],
  ["Collaborator", "pull requests", cc.totalPullRequestContributions, [100, 30, 10, 1]],
];
const hex = (r) =>
  Array.from({ length: 6 }, (_, i) => {
    const a = (Math.PI / 3) * i - Math.PI / 2;
    return `${(r * Math.cos(a)).toFixed(1)},${(r * Math.sin(a)).toFixed(1)}`;
  }).join(" ");
const tierFill = { S: RED, A: "#b91c1c", B: "#7f1d1d", C: "#450a0a", "?": "#161b22" };
const trophyItems = trophies
  .map(([name, unit, value, th], i) => {
    const t = tier(value, th);
    return `<g transform="translate(${95 + i * 160}, 105)">
  <polygon points="${hex(44)}" fill="none" stroke="${t === "?" ? BORDER : RED}" stroke-width="2" ${t === "S" ? 'class="glow"' : ""}/>
  <polygon points="${hex(36)}" fill="${tierFill[t]}"/>
  <text y="11" text-anchor="middle" style="font: 900 30px ${FONT}; fill: ${t === "?" ? MUTED : "#ffffff"}">${t}</text>
  <text y="68" text-anchor="middle" class="v">${esc(name)}</text>
  <text y="86" text-anchor="middle" class="l">${value.toLocaleString("en-US")} ${esc(unit)}</text>
</g>`;
  })
  .join("\n");
const trophiesSvg = frame(
  990,
  215,
  "trophies",
  `<style>.glow { animation: glow 2.5s ease-in-out infinite; } @keyframes glow { 50% { stroke-opacity: .3; } }</style>
${trophyItems}`
);

// --- streak card (all-time calendar) ---
const allDays = [];
let totalAll = 0;
const startYear = new Date(u.createdAt).getUTCFullYear();
for (let y = startYear; y <= new Date().getUTCFullYear(); y++) {
  const yd = await gql(
    `query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) { contributionsCollection(from: $from, to: $to) {
        restrictedContributionsCount
        contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
      } }
    }`,
    { login, from: `${y}-01-01T00:00:00Z`, to: `${y}-12-31T23:59:59Z` }
  );
  const ycc = yd.user.contributionsCollection;
  totalAll += ycc.contributionCalendar.totalContributions + ycc.restrictedContributionsCount;
  allDays.push(...ycc.contributionCalendar.weeks.flatMap((w) => w.contributionDays));
}
const today = new Date().toISOString().slice(0, 10);
const cal = [...new Map(allDays.filter((d) => d.date <= today).map((d) => [d.date, d.contributionCount])).entries()].sort();
let longest = { len: 0, start: "", end: "" };
let run = { len: 0, start: "" };
for (const [date, c] of cal) {
  if (c > 0) {
    run = run.len ? { len: run.len + 1, start: run.start } : { len: 1, start: date };
    if (run.len > longest.len) longest = { len: run.len, start: run.start, end: date };
  } else run = { len: 0, start: "" };
}
let i = cal.length - 1;
if (i >= 0 && cal[i][1] === 0) i--; // today not counted yet
let current = { len: 0, start: "", end: i >= 0 ? cal[i][0] : "" };
while (i >= 0 && cal[i][1] > 0) {
  current = { ...current, len: current.len + 1, start: cal[i][0] };
  i--;
}
const fmt = (d) => (d ? new Date(`${d}T00:00:00Z`).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric", timeZone: "UTC" }) : "-");
const fmtRange = (a, b) => (a ? (a === b ? fmt(a) : `${fmt(a)} → ${fmt(b)}`) : "no streak yet");
const col = (x, label, value, sub, hi) => `<g transform="translate(${x}, 0)">
  <rect x="-145" y="50" width="290" height="132" rx="8" fill="#0d1117" fill-opacity=".9" stroke="${RED}" stroke-opacity="${hi ? 0.6 : 0.22}"/>
  <text y="${hi ? 126 : 120}" text-anchor="middle" style="font: 800 ${hi ? 48 : 40}px ${FONT}; fill: ${hi ? RED : TEXT}">${value.toLocaleString("en-US")}</text>
  <text y="80" text-anchor="middle" style="font: 600 11px ${MONO}; fill: ${hi ? "#fca5a5" : RED}; letter-spacing: 2px">${esc(label)}</text>
  <text y="160" text-anchor="middle" class="l">${esc(sub)}</text>
</g>`;
const streakSvg = frame(
  990,
  200,
  "contribution streak",
  `${col(170, "TOTAL CONTRIBUTIONS", totalAll, `${fmt(cal[0]?.[0])} → present`)}
${col(495, "🔥 CURRENT STREAK", current.len, fmtRange(current.start, current.end), true)}
${col(820, "LONGEST STREAK", longest.len, fmtRange(longest.start, longest.end))}`
);

mkdirSync(outDir, { recursive: true });
writeFileSync(`${outDir}/stats.svg`, statsSvg);
writeFileSync(`${outDir}/langs.svg`, langsSvg);
writeFileSync(`${outDir}/activity.svg`, activitySvg);
writeFileSync(`${outDir}/trophies.svg`, trophiesSvg);
writeFileSync(`${outDir}/streak.svg`, streakSvg);
console.log(`Wrote stats.svg, langs.svg, activity.svg, trophies.svg, streak.svg to ${outDir}`);
