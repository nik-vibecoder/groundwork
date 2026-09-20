# Groundwork

**Fitness fundamentals, ranked by what actually matters.**

A static site that sorts nutrition and training into three tiers, colour coded like a traffic light,
so a working professional can learn the essentials without a coach or a chatbot and can tell which
5% of the advice drives 80% of the result.

Green is the foundation. Amber is worth tuning next. Red is the noise you can ignore until the rest
is automatic.

---

## Pages

| Page | Contents |
| --- | --- |
| `index.html` | Start here. The tier system, set-up, first four weeks, week five review |
| `nutrition.html` | Calories, protein, macros, fibre, supplements, FAQs |
| `training.html` | Consistency, effort, progression, volume, frequency, cardio, FAQs |
| `exercises.html` | ~20 movements with cues, mistakes and substitutions, filterable by pattern |
| `calculators.html` | Calories and macros, training volume, one rep max |
| `planner.html` | Complete 2, 3, 4 and 5 day programmes, set by set |
| `downloads.html` | Free printable logs, CSV trackers, one page cheat sheet |
| `sources.html` | 20 references with an honest note on evidence strength |

## Stack

Plain HTML, one CSS file, one JS file. No framework, no runtime dependencies, no tracking, no
analytics, no cookies. Two Google Fonts and nothing else leaves the visitor's browser. All three
calculators run client side.

```
src/              page bodies (edit these)
tools/build.py    wraps bodies in the shared shell, writes the root HTML
assets/css        design system
assets/js         behaviour
downloads/        the free templates
*.html            generated, committed, served by GitHub Pages
```

## Editing

Edit the page bodies in `src/`, then rebuild:

```bash
python3 tools/build.py
```

That regenerates the eight root `.html` files plus `sitemap.xml` and `robots.txt`. Standard library
only, so there is nothing to install.

- **Sidebar, nav order, page titles and meta descriptions** live in `tools/build.py`.
- **Colours, fonts and spacing** live in the `:root` block at the top of `assets/css/style.css`.
- **FAQ structured data** is generated automatically from any `<details class="acc" data-faq>` block,
  so adding a question to a page also adds it to the `FAQPage` schema.
- To rename the site, change `SITE` in `tools/build.py`.

Generated HTML is committed so GitHub Pages needs no CI step.

## Before you publish

Set your real URL in `tools/build.py`, then rebuild. It drives canonical links, Open Graph tags,
the sitemap and structured data.

```python
BASE = "https://yourname.github.io/groundwork"
```

## Deploy to GitHub Pages

```bash
gh repo create groundwork --public --source=. --remote=origin --push
```

Then in the repo: **Settings → Pages → Source: Deploy from a branch → `main` / `(root)`**.
Live at `https://<username>.github.io/groundwork/` in a minute or two. `.nojekyll` is included so
GitHub serves the files as-is.

## Run locally

Open `index.html` in a browser, or serve it:

```bash
python3 -m http.server 4173
```

## Search and answer engine optimisation

- Unique title, meta description and canonical URL per page
- Open Graph and Twitter card tags
- JSON-LD: `Article` / `WebPage` / `WebApplication`, `BreadcrumbList`, and `FAQPage` where relevant
- `sitemap.xml` and a `robots.txt` that explicitly welcomes AI crawlers
- One `h1` per page, logical heading order, semantic tables with captions and scoped headers
- Every substantive section opens with a short direct answer block, which is the format answer
  engines quote from
- Inline citations link to a sources page, which is what both readers and models use to judge
  whether a claim is trustworthy

## Content

No products, no affiliate links, no email capture. Every recommendation points at a meta-analysis,
position stand or public health guideline listed on `sources.html`, and where the evidence is weak
the page says so.

The templates in `downloads/` are released into the public domain.

## Disclaimer

General educational content for healthy adults. Not medical, dietetic or physiotherapeutic advice,
not a diagnosis, and not a substitute for a qualified professional. Calculator output is an estimate
from a population formula and can be off by 15% for any individual.
