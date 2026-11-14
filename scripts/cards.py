"""Generates the profile's card images (light + dark). Edit CONFIG, then run:
    python3 scripts/cards.py
"""
import math, os

CONFIG = {
    "projects": [
        {"slug": "api", "title": "api", "lang": "TypeScript",
         "desc": ["Typed REST API with role-based access,", "Zod validation and OpenAPI docs."],
         "tags": ["Hono", "Drizzle", "Neon Postgres"]},
    ],
    "principles": [
        ("Types end to end", ["Strict TypeScript and schema", "validation at every boundary."]),
        ("Data you can audit", ["Append-only records and explicit", "corrections. No silent changes."]),
        ("Contracts first", ["Specs and OpenAPI before code,", "so teams build in parallel."]),
        ("Secure by default", ["Least-privilege roles, minimal", "personal data, clean logs."]),
    ],
}

THEMES = {
    "light": dict(card="#FFFFFF", border="#E5E5EA", text="#1D1D1F", sub="#6E6E73",
                  pill="#F5F5F7", pilltext="#1D1D1F", accent="#0071E3", shadow="0.08"),
    "dark":  dict(card="#1C1C1E", border="#2C2C2E", text="#F5F5F7", sub="#A1A1A6",
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
for name, t in THEMES.items():
    for p in CONFIG["projects"]:
        open(f"{root}/project-{p['slug']}-{name}.svg", "w").write(project(p, t))
    open(f"{root}/principles-{name}.svg", "w").write(principles(CONFIG["principles"], t))
print("cards written to assets/")
