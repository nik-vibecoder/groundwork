#!/usr/bin/env python3
"""
Groundwork static builder.

Takes the page bodies in src/ and wraps each one in the shared shell
(sidebar, <head>, structured data), writing plain HTML to the repo root.
Pure standard library. Run it after editing anything in src/:

    python3 tools/build.py

The generated .html files are committed, so GitHub Pages serves them
directly with no CI step.
"""

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

# ---------------------------------------------------------------------------
# Change this to your own URL before publishing, then re-run the build.
# It drives canonical links, Open Graph tags, the sitemap and structured data.
# ---------------------------------------------------------------------------
BASE = "https://nik-vibecoder.github.io/groundwork"

SITE = "Groundwork"
TAGLINE = "Fitness fundamentals, ranked by what actually matters"
AUTHOR = "Groundwork"
UPDATED = "2026-09-21"

I = {  # nav icons, 1.6 stroke, currentColor
    "start": '<path d="M3 10.2 12 3l9 7.2"/><path d="M5 9.4V20h14V9.4"/><path d="M9.5 20v-6h5v6"/>',
    "nutrition": '<path d="M12 8.2c-1.4-1.3-4-1.6-5.6.2-1.9 2.1-1.3 5.9.4 8.4 1 1.5 2.3 2.6 3.4 2.6.9 0 1.3-.4 1.8-.4s.9.4 1.8.4c1.1 0 2.4-1.1 3.4-2.6 1.7-2.5 2.3-6.3.4-8.4-1.6-1.8-4.2-1.5-5.6-.2Z"/><path d="M12 8.2V5.6A2.6 2.6 0 0 1 14.6 3"/>',
    "training": '<path d="M6.5 6.5v11"/><path d="M17.5 6.5v11"/><path d="M3.5 9.5v5"/><path d="M20.5 9.5v5"/><path d="M6.5 12h11"/>',
    "exercises": '<path d="M9 6h11"/><path d="M9 12h11"/><path d="M9 18h11"/><path d="M4.2 6h.01"/><path d="M4.2 12h.01"/><path d="M4.2 18h.01"/>',
    "calculators": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 7h8"/><path d="M8.5 12h.01"/><path d="M12 12h.01"/><path d="M15.5 12h.01"/><path d="M8.5 16h.01"/><path d="M12 16h.01"/><path d="M15.5 16h.01"/>',
    "planner": '<rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 10h17"/><path d="M8 3.5v3"/><path d="M16 3.5v3"/>',
    "downloads": '<path d="M12 3.5v11"/><path d="m8 10.5 4 4 4-4"/><path d="M4.5 16.5v2a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2v-2"/>',
    "sources": '<path d="M4 5.5A2 2 0 0 1 6 3.5h6v17H6a2 2 0 0 1-2-2Z"/><path d="M20 5.5a2 2 0 0 0-2-2h-6v17h6a2 2 0 0 0 2-2Z"/>',
}

# (label, icon, href or None, [(sub label, sub href), ...])
NAV = [
    ("Start here", "start", "index.html", []),
    ("Nutrition", "nutrition", None, [
        ("The nutrition pyramid", "nutrition.html"),
        ("Calories and the deficit", "nutrition.html#calories"),
        ("Protein", "nutrition.html#protein"),
        ("Food quality and fibre", "nutrition.html#quality"),
        ("Supplements", "nutrition.html#supplements"),
        ("Common questions", "nutrition.html#faq"),
    ]),
    ("Training", "training", None, [
        ("The training pyramid", "training.html"),
        ("Effort and progression", "training.html#progression"),
        ("Volume and frequency", "training.html#volume"),
        ("Cardio and steps", "training.html#cardio"),
        ("Common questions", "training.html#faq"),
    ]),
    ("Exercises", "exercises", None, [
        ("Full library", "exercises.html"),
        ("Squat", "exercises.html#squat"),
        ("Hinge", "exercises.html#hinge"),
        ("Push", "exercises.html#push"),
        ("Pull", "exercises.html#pull"),
        ("Arms and shoulders", "exercises.html#arms"),
        ("Core and calves", "exercises.html#core"),
    ]),
    ("Calculators", "calculators", None, [
        ("Calories and macros", "calculators.html"),
        ("Training volume", "calculators.html#volume"),
        ("One rep max", "calculators.html#onerm"),
    ]),
    ("Planner", "planner", None, [
        ("Pick your split", "planner.html"),
        ("2 days a week", "planner.html#d2"),
        ("3 days a week", "planner.html#d3"),
        ("4 days a week", "planner.html#d4"),
        ("5 days a week", "planner.html#d5"),
    ]),
    ("Free templates", "downloads", "downloads.html", []),
    ("Sources", "sources", "sources.html", []),
]

PAGES = {
    "index.html": {
        "title": "Groundwork: Fitness Fundamentals Ranked by What Actually Matters",
        "h1": "Start here",
        "desc": "Nutrition and training fundamentals sorted into three tiers, so you can tell "
                "the 5% that drives 80% of the result from the noise. Free, no sign-up, no products.",
        "kw": "fitness fundamentals, evidence based fitness, nutrition pyramid, training pyramid, beginner gym guide",
        "type": "WebPage",
    },
    "nutrition.html": {
        "title": "The Nutrition Pyramid: What to Get Right, in Order",
        "h1": "The nutrition pyramid",
        "desc": "Calories and protein first, then macros and fibre, then supplements and timing. "
                "Each tier explained with the evidence behind it and what it is worth.",
        "kw": "nutrition pyramid, calorie deficit, protein intake, macros, fibre, supplements, creatine",
        "type": "Article",
    },
    "training.html": {
        "title": "The Training Pyramid: Consistency, Effort, Volume, in Order",
        "h1": "The training pyramid",
        "desc": "Showing up and training hard beat every programming detail. Volume, frequency and "
                "exercise selection come next. Rest periods and tempo come last.",
        "kw": "training pyramid, progressive overload, training volume, sets per muscle, reps in reserve",
        "type": "Article",
    },
    "exercises.html": {
        "title": "Exercise Library: Cues, Mistakes and Substitutions",
        "h1": "Exercise library",
        "desc": "Around 20 movements worth knowing, each with the two or three cues that change the "
                "lift, the mistakes behind most gym injuries, and a substitute if it hurts.",
        "kw": "exercise form, lifting cues, squat form, deadlift form, bench press form, exercise substitutions",
        "type": "Article",
    },
    "calculators.html": {
        "title": "Calorie, Macro, Volume and One Rep Max Calculators",
        "h1": "Calculators",
        "desc": "Work out your maintenance calories and macro targets, how many weekly sets to run, "
                "and your estimated one rep max. Everything runs in your browser.",
        "kw": "calorie calculator, macro calculator, TDEE calculator, one rep max calculator, training volume calculator",
        "type": "WebApplication",
    },
    "planner.html": {
        "title": "Training Plans for 2, 3, 4 and 5 Days a Week",
        "h1": "Planner",
        "desc": "Complete programmes written out set by set for two, three, four and five days a "
                "week, each with the progression rule attached.",
        "kw": "workout plan, full body workout, upper lower split, push pull legs, 3 day workout plan",
        "type": "Article",
    },
    "downloads.html": {
        "title": "Free Workout Log, Food Diary and Tracker Templates",
        "h1": "Free templates",
        "desc": "Printable workout logs, a 12 week progression tracker, a food and protein diary and "
                "a one page cheat sheet. CSV and print ready, no email required.",
        "kw": "free workout log template, printable workout log, food diary template, training tracker spreadsheet",
        "type": "WebPage",
    },
    "sources.html": {
        "title": "Sources: The Research Behind Every Recommendation",
        "h1": "Sources",
        "desc": "Every number on this site traced to a meta-analysis, position stand or guideline, "
                "with a note on how strong the evidence actually is.",
        "kw": "evidence based fitness sources, resistance training meta analysis, protein meta analysis, ISSN position stand",
        "type": "Article",
    },
}

ORDER = ["index.html", "nutrition.html", "training.html", "exercises.html",
         "calculators.html", "planner.html", "downloads.html", "sources.html"]


def icon(name, cls="navgroup__ico"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[name]}</svg>')


def build_nav():
    caret = ('<svg class="navgroup__caret" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<path d="m9 18 6-6-6-6"/></svg>')
    out = ['<nav class="side__nav" aria-label="Main">']
    for label, ico, href, subs in NAV:
        if href and not subs:
            out.append(f'<a class="side__solo" href="{href}">{icon(ico)}{label}</a>')
            continue
        out.append('<details class="navgroup">')
        out.append(f'<summary>{icon(ico)}{label}{caret}</summary>')
        out.append('<ul class="navgroup__list">')
        for sl, sh in subs:
            out.append(f'<li><a href="{sh}">{sl}</a></li>')
        out.append('</ul></details>')
    out.append('</nav>')
    return "\n".join(out)


MARK = ('<svg class="side__mark" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<path d="M12 3 22 20.5H2Z" fill="#0F8A54"/>'
        '<path d="M12 3 17 11.7H7Z" fill="#D98014"/>'
        '<path d="M12 3 14.2 6.9H9.8Z" fill="#D92D20"/></svg>')


def faq_schema(body):
    """Pull <details class="acc" data-faq> blocks into FAQPage structured data."""
    qs = re.findall(
        r'<details class="acc" data-faq>\s*<summary>(.*?)</summary>(.*?)</details>',
        body, re.S)
    items = []
    for q, a in qs:
        q = re.sub(r"<[^>]+>", "", q).strip()
        a = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", a)).strip()
        if q and a:
            items.append({
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a[:1200]},
            })
    if not items:
        return None
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items}


def breadcrumbs(fname, h1):
    crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"}]
    if fname != "index.html":
        crumbs.append({"@type": "ListItem", "position": 2, "name": h1,
                       "item": f"{BASE}/{fname}"})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumbs}


def page_schema(fname, meta):
    url = f"{BASE}/" if fname == "index.html" else f"{BASE}/{fname}"
    base = {
        "@context": "https://schema.org",
        "@type": meta["type"],
        "name": meta["title"],
        "headline": meta["title"],
        "description": meta["desc"],
        "url": url,
        "inLanguage": "en",
        "dateModified": UPDATED,
        "isPartOf": {"@type": "WebSite", "name": SITE, "url": f"{BASE}/"},
        "publisher": {"@type": "Organization", "name": SITE, "url": f"{BASE}/"},
    }
    if meta["type"] == "WebApplication":
        base["applicationCategory"] = "HealthApplication"
        base["operatingSystem"] = "Any"
        base["offers"] = {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    if meta["type"] == "Article":
        base["author"] = {"@type": "Organization", "name": AUTHOR}
        base["datePublished"] = UPDATED
    return base


SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{kw}">
<meta name="author" content="{author}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{site}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="en">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="theme-color" content="#ffffff">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 3 22 20.5H2Z' fill='%230F8A54'/%3E%3Cpath d='M12 3 17 11.7H7Z' fill='%23D98014'/%3E%3Cpath d='M12 3 14.2 6.9H9.8Z' fill='%23D92D20'/%3E%3C/svg%3E">
{schema}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<div class="topbar">
  <button class="burger" data-burger aria-expanded="false" aria-label="Open navigation" aria-controls="sidebar">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
  </button>
  <a class="topbar__brand" href="index.html">{mark} {site}</a>
</div>
<div class="scrim" data-scrim></div>

<div class="app">
  <aside class="side" id="sidebar" data-side>
    <a class="side__brand" href="index.html">{mark} {site} <span class="side__tag">Free</span></a>
    {nav}
    <div class="side__foot">
      Educational content for healthy adults. Not medical advice.<br>
      Last reviewed {updated}.
    </div>
  </aside>

  <main class="main" id="main">
    <div class="page">
{body}
    </div>
  </main>
</div>

<script src="assets/js/site.js"></script>
</body>
</html>
"""


def build():
    if not SRC.is_dir():
        sys.exit("src/ not found")
    nav = build_nav()
    written = []

    for fname in ORDER:
        meta = PAGES[fname]
        src = SRC / fname
        if not src.is_file():
            sys.exit(f"missing src/{fname}")
        body = src.read_text(encoding="utf-8")
        url = f"{BASE}/" if fname == "index.html" else f"{BASE}/{fname}"

        blocks = [page_schema(fname, meta), breadcrumbs(fname, meta["h1"])]
        fq = faq_schema(body)
        if fq:
            blocks.append(fq)
        schema = "\n".join(
            '<script type="application/ld+json">' +
            json.dumps(b, ensure_ascii=False, separators=(",", ":")) + "</script>"
            for b in blocks)

        html = SHELL.format(
            title=meta["title"], desc=meta["desc"], kw=meta["kw"], url=url,
            site=SITE, author=AUTHOR, updated=UPDATED, mark=MARK,
            nav=nav, body=body, schema=schema)
        (ROOT / fname).write_text(html, encoding="utf-8")
        written.append(fname)

    # sitemap
    urls = []
    for fname in ORDER:
        u = f"{BASE}/" if fname == "index.html" else f"{BASE}/{fname}"
        pri = "1.0" if fname == "index.html" else "0.8"
        urls.append(f"  <url><loc>{u}</loc><lastmod>{UPDATED}</lastmod>"
                    f"<changefreq>monthly</changefreq><priority>{pri}</priority></url>")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")

    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        "# Answer engines and AI crawlers are welcome to use this content.\n"
        "User-agent: GPTBot\nAllow: /\n"
        "User-agent: ClaudeBot\nAllow: /\n"
        "User-agent: PerplexityBot\nAllow: /\n"
        "User-agent: Google-Extended\nAllow: /\n\n"
        f"Sitemap: {BASE}/sitemap.xml\n", encoding="utf-8")

    print(f"built {len(written)} pages + sitemap.xml + robots.txt")
    if "USERNAME" in BASE:
        print("NOTE: set BASE in tools/build.py to your real URL, then re-run.")


if __name__ == "__main__":
    build()
