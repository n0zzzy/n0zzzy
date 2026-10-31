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
<style>
  .t { font: 600 16px ${FONT}; fill: ${RED}; }
  .l { font: 400 13px ${FONT}; fill: ${MUTED}; }
  .v { font: 700 14px ${FONT}; fill: ${TEXT}; }
  .big { font: 800 40px ${FONT}; fill: ${TEXT}; }
  .fade { animation: fade .6s ease-out; }
  @keyframes fade { from { opacity: 0; transform: translateX(-6px); } to { opacity: 1; transform: none; } }
  @keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
  @keyframes ring { from { stroke-dashoffset: 251; } }
</style>
<rect x="0.5" y="0.5" width="${w - 1}" height="${h - 1}" rx="10" fill="${BG}" stroke="${BORDER}"/>
<rect x="0.5" y="0.5" width="4" height="${h - 1}" rx="2" fill="${RED}"/>
<text x="25" y="34" class="t">${esc(title)}</text>
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

mkdirSync(outDir, { recursive: true });
writeFileSync(`${outDir}/stats.svg`, statsSvg);
writeFileSync(`${outDir}/langs.svg`, langsSvg);
writeFileSync(`${outDir}/activity.svg`, activitySvg);
console.log(`Wrote stats.svg, langs.svg, activity.svg to ${outDir}`);
