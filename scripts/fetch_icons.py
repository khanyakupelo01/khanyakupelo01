"""Builds scripts/icons.json from an extracted `simple-icons` npm package.

Usage:
    python3 scripts/fetch_icons.py <path to extracted package directory>

The package is fetched into a temporary directory and only data is read from it (nothing is run).
Only the icons listed in ICONS below are kept. See scripts/ICONS.md for source and licence.
"""
import json, os, re, sys

SOURCE = "simple-icons 16.37.0"

# key -> simple-icons file stem
ICONS = {
    "typescript": "typescript", "react": "react", "tanstack": "tanstack", "tailwindcss": "tailwindcss",
    "shadcnui": "shadcnui", "vite": "vite", "nodedotjs": "nodedotjs", "hono": "hono",
    "openapiinitiative": "openapiinitiative", "swagger": "swagger", "zod": "zod",
    "postgresql": "postgresql", "neon": "neon", "drizzle": "drizzle", "vitest": "vitest",
    "biome": "biome", "eslint": "eslint", "prettier": "prettier", "githubactions": "githubactions",
    "cloudflareworkers": "cloudflareworkers",
}

# Original generic glyphs (24x24, filled), used where no brand logo exists.
GENERIC = {
    "migrations": {"title": "Schema migrations",
                   "path": "M3 5h12a1 1 0 0 1 0 2H3a1 1 0 0 1 0-2zM3 11h8a1 1 0 0 1 0 2H3a1 1 0 0 1 0-2zM3 17h12a1 1 0 0 1 0 2H3a1 1 0 0 1 0-2zM16.5 9l4.5 3-4.5 3z"},
    "fetch": {"title": "Typed fetch client",
              "path": "M3 6.5h12v-3L21 8l-6 4.5v-3H3zM21 14.5H9v-3L3 16l6 4.5v-3h12z"},
}

def main(pkg):
    out = {}
    for key, stem in ICONS.items():
        svg = open(os.path.join(pkg, "icons", stem + ".svg"), encoding="utf-8").read()
        title = re.search(r"<title>([^<]*)</title>", svg).group(1)
        d = re.search(r'<path d="([^"]+)"', svg).group(1)
        out[key] = {"title": title, "source": SOURCE, "path": d}
    for key, g in GENERIC.items():
        out[key] = {"title": g["title"], "source": "generic", "path": g["path"]}
    dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons.json")
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print(f"wrote {len(out)} icons to {dest}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
