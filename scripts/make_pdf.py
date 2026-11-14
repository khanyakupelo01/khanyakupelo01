"""Builds assets/khanya-profile.pdf from scripts/print.html using the locally installed Chrome (headless).

Usage:
    python3 scripts/cards.py     # refresh the card images first, if they changed
    python3 scripts/make_pdf.py

Fails (and writes nothing) if the print page has drifted from README.md: the introduction text is taken
from the README, and every link in the print page must also appear in the README. Set CHROME to use a
different browser binary. Standard library only.
"""
import html, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
ASSETS = os.path.join(ROOT, "assets")
OUT = os.path.join(ASSETS, "khanya-profile.pdf")
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

def die(msg):
    sys.exit("make_pdf.py: " + msg)

def intro_from_readme(readme):
    m = re.search(r'\n\n(I\'m a senior software engineer[^\n]*(?:\n[^\n<#][^\n]*)*)\n', readme)
    if not m:
        die("could not find the introduction paragraph in README.md")
    return " ".join(m.group(1).split())

def main():
    if not os.path.exists(CHROME):
        die(f"Chrome not found at {CHROME} (set CHROME=...)")
    readme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
    page = open(os.path.join(HERE, "print.html"), encoding="utf-8").read()

    # Links in the print page must also be in the README (no PDF-only claims).
    for href in sorted(set(re.findall(r'href="(https?://[^"]+)"', page))):
        if href not in readme:
            die(f"link in print.html is not in README.md: {href}")
    # Images used by the print page must exist.
    for img in re.findall(r'\{\{ASSETS\}\}/([^"]+)"', page):
        if not os.path.exists(os.path.join(ASSETS, img)):
            die(f"missing image: assets/{img} (run python3 scripts/cards.py)")

    page = page.replace("{{INTRO}}", html.escape(intro_from_readme(readme), quote=False))
    page = page.replace("{{ASSETS}}", "file://" + ASSETS)
    if "{{" in page:
        die("unfilled placeholder left in print.html")

    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "print.html")
        open(src, "w", encoding="utf-8").write(page)
        out_tmp = os.path.join(tmp, "out.pdf")
        r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                            "--allow-file-access-from-files", f"--print-to-pdf={out_tmp}", "file://" + src],
                           capture_output=True, text=True, timeout=120)
        if not os.path.exists(out_tmp) or os.path.getsize(out_tmp) < 1000:
            die("Chrome did not produce a PDF:\n" + r.stderr[-500:])
        data = open(out_tmp, "rb").read()
    open(OUT, "wb").write(data)
    pages = len(re.findall(rb"/Type\s*/Page[^s]", data))
    print(f"wrote {os.path.relpath(OUT, ROOT)} ({len(data)//1024} KB, {pages} pages)")

if __name__ == "__main__":
    main()
