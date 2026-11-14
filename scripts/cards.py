"""Generates the profile's card images. Every card uses one dark, theme-neutral design (constitution II).
Edit CONFIG, then run:
    python3 scripts/cards.py
Icons come from scripts/icons.json (see scripts/ICONS.md).
"""
import json, math, os

ICONS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons.json"), encoding="utf-8"))

CONFIG = {
    "projects": [
        {"slug": "api", "title": "ubuntu api", "lang": "TypeScript",
         "desc": ["Typed REST API with role-based access,", "Zod validation and OpenAPI docs."],
         "tags": ["Hono", "Drizzle", "Neon Postgres"]},
        {"slug": "ubuntu", "title": "ubuntu ui", "lang": "TypeScript",
         "desc": ["Web app for a communal ceremony-support", "scheme, built on TanStack Start."],
         "tags": ["React", "TanStack Start", "Tailwind CSS"]},
    ],
    # Skills. EVIDENCE RULE (constitution III): a badge may be listed only if it is used in the
    # source of the `api` or `ubuntu` project, and it must appear in the audit table of
    # specs/001-resume-skills-section/research.md. One badge, one category.
    "skills": [
        {"slug": "languages-frontend", "title": "Languages & Frontend", "projects": ["ubuntu api", "ubuntu ui"],
         "badges": [("TypeScript", "typescript"), ("React", "react"), ("TanStack Start", "tanstack"),
                    ("Tailwind CSS", "tailwindcss"), ("shadcn/ui", "shadcnui"), ("Vite", "vite")]},
        {"slug": "backend", "title": "Backend", "projects": ["ubuntu api", "ubuntu ui"],
         "badges": [("Node.js", "nodedotjs"), ("Hono", "hono"), ("OpenAPI", "openapiinitiative"),
                    ("Swagger UI", "swagger"), ("Zod", "zod"), ("openapi-fetch", "fetch")]},
        {"slug": "data", "title": "Data", "projects": ["ubuntu api", "ubuntu ui"],
         "badges": [("PostgreSQL", "postgresql"), ("Neon", "neon"), ("Drizzle ORM", "drizzle"),
                    ("Schema migrations", "migrations")]},
        {"slug": "tooling-delivery", "title": "Tooling & Delivery", "projects": ["ubuntu api", "ubuntu ui"],
         "badges": [("Vitest", "vitest"), ("Biome", "biome"), ("ESLint", "eslint"), ("Prettier", "prettier"),
                    ("GitHub Actions", "githubactions"), ("Cloudflare Workers", "cloudflareworkers")]},
    ],
    "principles": [
        ("Types end to end", ["Strict TypeScript and schema", "validation at every boundary."]),
        ("Data you can audit", ["Append-only records and explicit", "corrections. No silent changes."]),
        ("Contracts first", ["Specs and OpenAPI before code,", "so teams build in parallel."]),
        ("Secure by default", ["Least-privilege roles, minimal", "personal data, clean logs."]),
    ],
}

THEMES = {
    "dark": dict(card="#1C1C1E", border="#3A3A3C", text="#F5F5F7", sub="#A1A1A6",
                 pill="#2C2C2E", pilltext="#F5F5F7", accent="#2997FF", shadow="0.0"),
}
FONT = '-apple-system,BlinkMacSystemFont,"SF Pro Text","Inter","Segoe UI",Helvetica,Arial,sans-serif'

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;")
def tw(s, size, w=0.56): return len(s) * size * w  # rough text width

def frame(w, h, t, body, label):
    pad = 12  # room for the shadow
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">
<defs><filter id="s" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#000" flood-opacity="{t['shadow']}"/></filter></defs>
<style>
  text {{ font-family: {FONT}; }}
  .title {{ font-size: 26px; font-weight: 600; letter-spacing: -0.4px; fill: {t['text']}; }}
  .h {{ font-size: 21px; font-weight: 600; letter-spacing: -0.3px; fill: {t['text']}; }}
  .sub {{ font-size: 17px; fill: {t['sub']}; }}
  .eyebrow {{ font-size: 13px; font-weight: 600; letter-spacing: 1.6px; fill: {t['sub']}; }}
  .pill {{ font-size: 14px; font-weight: 500; fill: {t['pilltext']}; }}
</style>
<rect x="{pad}" y="{pad-4}" width="{w-2*pad}" height="{h-2*pad}" rx="22" fill="{t['card']}" stroke="{t['border']}" filter="url(#s)"/>
{body}
</svg>'''

def pills(x, y, items, t, size=14):
    out, cx = "", x
    for it in items:
        pw = tw(it, size) + 28
        out += f'<rect x="{cx:.0f}" y="{y}" width="{pw:.0f}" height="32" rx="16" fill="{t["pill"]}"/>'
        out += f'<text class="pill" x="{cx+pw/2:.0f}" y="{y+21}" text-anchor="middle">{esc(it)}</text>'
        cx += pw + 10
    return out

def project(p, t):
    w, h = 600, 260
    b = f'<text class="eyebrow" x="44" y="58">PROJECT</text>'
    b += f'<text class="title" x="44" y="96">{esc(p["title"])}</text>'
    # arrow
    b += f'<path d="M540 56 l12 0 l0 12 M552 56 l-14 14" fill="none" stroke="{t["sub"]}" stroke-width="2" stroke-linecap="round"/>'
    for i, line in enumerate(p["desc"]):
        b += f'<text class="sub" x="44" y="{132+i*24}">{esc(line)}</text>'
    b += f'<circle cx="52" cy="{h-60}" r="6" fill="{t["accent"]}"/>'
    b += f'<text class="pill" x="66" y="{h-55}">{esc(p["lang"])}</text>'
    b += pills(66 + tw(p["lang"], 14) + 22, h - 76, p["tags"], t)
    return frame(w, h, t, b, f'{p["title"]}: ' + " ".join(p["desc"]))

SKILL_W, SKILL_PAD = 600, 44

def badge_rows(items, size=14):
    """Greedy wrap of pill badges into rows that fit inside the card."""
    rows, cur, cx = [], [], 0
    limit = SKILL_W - 2 * SKILL_PAD
    for name, icon in items:
        pw = tw(name, size) + 28 + 24  # 24px for the 16px icon and its gap
        if cur and cx + pw > limit:
            rows.append(cur); cur, cx = [], 0
        cur.append((name, icon, pw)); cx += pw + 10
    if cur: rows.append(cur)
    return rows

def skills_card(cat, t, rows_total):
    """Card for one skill category. rows_total keeps every card the same height."""
    w = SKILL_W
    h = 168 + rows_total * 42 + 30
    b = f'<text class="eyebrow" x="{SKILL_PAD}" y="58">SKILLS</text>'
    b += f'<text class="title" x="{SKILL_PAD}" y="96">{esc(cat["title"])}</text>'
    cx = SKILL_PAD
    for proj in cat["projects"]:
        b += f'<circle cx="{cx+5}" cy="126" r="4" fill="{t["accent"]}"/>'
        b += f'<text class="sub" x="{cx+16}" y="132" style="font-size:15px">{esc(proj)}</text>'
        cx += 16 + tw(proj, 15) + 22
    y = 160
    for row in badge_rows(cat["badges"]):
        x = SKILL_PAD
        for name, icon, pw in row:
            b += f'<rect x="{x:.0f}" y="{y}" width="{pw:.0f}" height="32" rx="16" fill="{t["pill"]}"/>'
            b += f'<path d="{ICONS[icon]["path"]}" transform="translate({x+14:.0f},{y+8}) scale(0.667)" fill="{t["pilltext"]}"/>'
            b += f'<text class="pill" x="{x+14+16+8:.0f}" y="{y+21}">{esc(name)}</text>'
            x += pw + 10
        y += 42
    label = f'{cat["title"]} skills from {" and ".join(cat["projects"])}: ' + ", ".join(n for n, _ in cat["badges"])
    return frame(w, h, t, b, label)

def principles(items, t):
    w, h = 1200, 440
    b = '<text class="eyebrow" x="52" y="66">HOW I WORK</text>'
    cw, ch, gx, gy = 532, 130, 32, 24
    for i, (title, lines) in enumerate(items):
        x = 52 + (i % 2) * (cw + gx); y = 96 + (i // 2) * (ch + gy)
        b += f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="{t["pill"]}"/>'
        b += f'<circle cx="{x+30}" cy="{y+38}" r="6" fill="{t["accent"]}"/>'
        b += f'<text class="h" x="{x+48}" y="{y+45}">{esc(title)}</text>'
        for j, line in enumerate(lines):
            b += f'<text class="sub" x="{x+30}" y="{y+80+j*23}">{esc(line)}</text>'
    return frame(w, h, t, b, "How I work: " + "; ".join(f"{a}. {' '.join(l)}" for a, l in items))

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
t = THEMES["dark"]
for p in CONFIG["projects"]:
    open(f"{root}/project-{p['slug']}-dark.svg", "w").write(project(p, t))
rows_total = max(len(badge_rows(c["badges"])) for c in CONFIG["skills"])
for c in CONFIG["skills"]:
    open(f"{root}/skills-{c['slug']}-dark.svg", "w").write(skills_card(c, t, rows_total))
open(f"{root}/principles-dark.svg", "w").write(principles(CONFIG["principles"], t))
print("cards written to assets/")
