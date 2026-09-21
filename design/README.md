# design/

The handoff zone between Claude Design (claude.ai/design) and the site. Nothing in here is part of
the build: `tools/build.py` never reads it, and it does not appear in `sitemap.xml`.

Note that GitHub Pages serves the whole repo, so these files are reachable by URL. The previews carry
`noindex`, but do not put anything private here.

```
design/
  README.md        this file
  tokens.md        the design decisions in words, mirrors :root in assets/css/style.css
  components/      one static preview page per component family
  exports/         raw output pulled from Claude Design (references only, never served by the site)
```

## How a design change flows

1. **Explore** in Claude Design. Nothing to do with git yet.
2. **Save** the chosen direction into `exports/` (a screenshot, exported HTML, a short note).
3. **Branch** from `main`, for example `design/refresh-cards`.
4. **Implement** in `assets/css/style.css` and `src/*.html`. Update `tokens.md` if a token changed.
5. **Check** by opening `design/components/index.html` and the real pages
   (`preview_start` with the `groundwork` config, or `python3 -m http.server 4173`).
6. **Build and commit**:

   ```bash
   python3 tools/build.py
   ```

7. **Merge** to `main` before starting other site work.

## Rules

- **`style.css` is the single source of truth.** The previews link to it directly. They never copy
  styles, so they cannot drift from the site.
- **One design branch at a time.** Design lands in cycles, so finish and merge one before opening
  the next.
- **Site fixes during a design branch go on `main`.** Then `git rebase main` on the design branch.
- **Generated HTML conflicts are never hand-resolved.** Take either side, re-run the build, commit.
- **Add a preview when you add a component.** If it has a class in `style.css`, it gets a card in
  `components/`.

## Previews

Open `components/index.html` in a browser (or under the dev server at `/design/components/`).

| Page | Covers |
| --- | --- |
| `tokens.html` | Colours, type, radii, shadows |
| `actions.html` | Buttons, chips, tags |
| `cards-notes.html` | Cards, notes (green / amber / red), stats |
| `accordion.html` | Accordion, tier rows with panels |
