#!/usr/bin/env python3
"""Builds the JLB Studios site into ./site. Run: python3 build.py

Pages live in src/*.html. Each starts with title:, description: and nav: lines,
then a line containing only ---. Shared parts live in src/_layout.html and
src/_form.html.

Posters: save an image as static/assets/posters/<slug>.jpg (for example
studio-c.jpg) and it replaces that title's stand-in card on the next build."""
import html as esc
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "site"
BASE = "https://www.jlbsound.com/"
NAV = [
    ("services.html", "Services"),
    ("credits.html", "Credits"),
    ("bio.html", "About"),
    ("rates.html", "Rates"),
]
POSTERS = [
    ("studio-c", "Studio C", "Series"),
    ("the-fighting-preacher", "The Fighting Preacher", "Film"),
    ("magellan", "Magellan", "Film"),
    ("botched-homes", "Botched Homes", "Series"),
    ("relative-race", "Relative Race", "Series"),
    ("making-good", "Making Good", "Series"),
    ("artful", "Artful", "Series"),
    ("dwight-in-shining-armor", "Dwight in Shining Armor", "Series"),
    ("donkey-king", "Donkey King", "Series"),
    ("nitro-circus-the-movie", "Nitro Circus: The Movie", "Film"),
    ("granite-flats", "Granite Flats", "Series"),
    ("american-ride", "American Ride", "Series"),
    ("the-story-trek", "The Story Trek", "Series"),
    ("show-offs", "Show Offs", "Series"),
    ("curse-of-crom", "Curse of Crom", "Film"),
]
SCHEMA = """{"@context":"https://schema.org","@type":"ProfessionalService","name":"JLB Studios",
"description":"Sound for picture: post-production sound for film and television.","url":"https://www.jlbsound.com/",
"telephone":"+1-801-318-7783","email":"joe@jlbsound.com","foundingDate":"2009",
"image":"https://www.jlbsound.com/assets/joe-belliston-console.jpg",
"founder":{"@type":"Person","name":"Joe Belliston","sameAs":"https://www.imdb.com/name/nm4444316/"},
"address":{"@type":"PostalAddress","addressLocality":"Lindon","addressRegion":"UT","addressCountry":"US"}}"""


def poster_card(slug, title, kind, hidden):
    name = esc.escape(title)
    extra = ' aria-hidden="true"' if hidden else ""
    if (ROOT / "static/assets/posters" / f"{slug}.jpg").exists():
        alt = "" if hidden else f"{name} poster"
        return (f'<li class="poster"{extra}><img src="/assets/posters/{slug}.jpg" '
                f'alt="{alt}" width="500" height="750" loading="lazy"></li>')
    return f'<li class="poster card"{extra}><strong>{name}</strong><span>{kind}</span></li>'


def poster_row():
    first = "".join(poster_card(*p, False) for p in POSTERS)
    second = "".join(poster_card(*p, True) for p in POSTERS)
    return first + second


layout = (ROOT / "src/_layout.html").read_text()
form = (ROOT / "src/_form.html").read_text()
if OUT.exists():
    shutil.rmtree(OUT)
shutil.copytree(ROOT / "static", OUT)

for page in sorted((ROOT / "src").glob("*.html")):
    if page.name.startswith("_"):
        continue
    head, body = page.read_text().split("\n---\n", 1)
    meta = dict(line.split(": ", 1) for line in head.splitlines())
    links = "".join(
        f'<a href="/{href}"{" aria-current=page" if meta.get("nav") == href else ""}>{label}</a>'
        for href, label in NAV
    )
    url = BASE if page.name == "index.html" else BASE + page.name
    body = body.replace("{{posters}}", poster_row()).replace("{{form}}", form)
    body = re.sub(r"(\w)'(\w)", "\\1\u2019\\2", body)  # curly apostrophes
    out = (
        layout.replace("{{title}}", meta["title"])
        .replace("{{description}}", meta["description"])
        .replace("{{url}}", url)
        .replace("{{links}}", links)
        .replace("{{schema}}", SCHEMA)
        .replace("{{body}}", body)
    )
    # Relative links so the site works on a github.io address and on the final domain
    out = re.sub(r'(href|src)="/"', r'\1="./"', out)
    out = re.sub(r'(href|src)="/([^"/][^"]*)"', r'\1="\2"', out)
    (OUT / page.name).write_text(out)
    print("built", page.name)
