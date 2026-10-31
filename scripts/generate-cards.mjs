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
        contributionCalendar { totalContributions }
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

mkdirSync(outDir, { recursive: true });
writeFileSync(`${outDir}/stats.svg`, statsSvg);
writeFileSync(`${outDir}/langs.svg`, langsSvg);
console.log(`Wrote ${outDir}/stats.svg and ${outDir}/langs.svg`);
