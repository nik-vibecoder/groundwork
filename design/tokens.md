# Design tokens

Source of truth is the `:root` block at the top of `assets/css/style.css`. This file records the
intent behind the values. When you change one, change both.

Direction: **graphite page, lime pop, white sheets.** Chosen for busy working professionals who
want a credible, high-energy reference rather than a soft wellness site.

## Principles

- **Graphite is the page, and it dominates.** `#1C1D22` end to end. Cards lift off it by tone, not
  by outlines. No light grey page tints anywhere.
- **Chrome is lighter than content.** The sidebar and mobile top bar are `#3A3C45`, above both the
  page and the cards, so navigation reads as a frame around the content.
- **Lime is the only brand colour.** Buttons, pills, active nav, markers, the numbers that matter.
- **Lime is a fill, never text on light.** Lime on white is 1.3:1. It sits behind ink text, or is
  used as text on graphite (10.8:1) where it is very legible.
- **White is a signal, not a default.** A white `.sheet` is reserved for the blocks that state the
  idea: the hero's "whole idea" panel and the short-answer box. If everything is white, nothing is
  ranked, which would be an odd look for a site about ranking things.
- **Tier colour carries data, never decoration.** Each tier card shows a weight bar sized to its
  actual share of the result (80%, 18%, 4%). No coloured card outlines.

## Two contexts

Every component works on graphite and inside a white sheet, because `.sheet` (and `.answer`)
redefine the same token names locally. Nothing needs a light-mode variant of its own.

```css
.sheet, .answer { --tx: #0B0B0F; --tx-2: #454852; --line: #EBEDF0; ... }
```

Put `class="sheet"` on any block that should be a white card. `.answer` gets it automatically.

## Page and surfaces (dark context)

| Token | Value | Use |
| --- | --- | --- |
| `--bg` | `#1C1D22` | Page |
| `--surface` | `#292B32` | Elevated card: tier cards, notes, tables, accordions |
| `--side-bg` | `#3A3C45` | Sidebar and mobile top bar. Lighter than the page, so the chrome sits above the content rather than behind it |
| `--bg-subtle` | `#23242A` | Hover on page rows |
| `--bg-sunken` | `#16171B` | Inputs, table headers, inset areas |
| `--bg-hover` | `#33353D` | Hover on controls |

## Brand

| Token | Value | Use |
| --- | --- | --- |
| `--ink` | `#0B0B0F` | Text on lime, dark stat tiles, buttons inside a sheet |
| `--lime` | `#C6F135` | Buttons, pills, markers, active nav. 10.8:1 on `--surface` |
| `--lime-hover` | `#B5E020` | Button hover |

## Text (dark context)

| Token | Value | Use |
| --- | --- | --- |
| `--tx` | `#FFFFFF` | Headings, emphasis (14.1:1 on card) |
| `--tx-2` | `#B4B6C0` | Body (7.0:1 on card) |
| `--tx-3` | `#A3A7B2` | Captions, mono labels (5.9:1) |
| `--tx-4` | `#7C8090` | Icons, disabled. Never for text |
| `--link` | `var(--lime)` | Links on graphite; ink inside a sheet |

## Lines

`--line #33353D` (default border), `--line-2 #43454F` (stronger, on controls),
`--track #3A3D46` (weight-bar track).

## Traffic light

The tier colours are pitched at lime's chroma so they belong to the same palette. The muted site
colours read as a different design language on graphite, so each tier has a **dark-context** value
and a **sheet** value; the token names are identical and switch automatically.

| | dark solid / ink | dark bg | dark line | sheet solid | sheet ink | sheet bg |
| --- | --- | --- | --- | --- | --- | --- |
| Green | `#2BE58B` | `#1B2F26` | `#2C4A3A` | `#0F8A54` | `#0A6640` | `#E7F6EE` |
| Amber | `#FFB020` | `#33291A` | `#4D3F22` | `#D98014` | `#96540A` | `#FEF4E6` |
| Red | `#FF6B57` | `#331F1C` | `#4D2F2A` | `#D92D20` | `#A11F16` | `#FDECEA` |

Dark-context contrast on `--surface`: green 8.5:1, amber 7.7:1, red 5.0:1.

Lime is yellow-green and Tier 1 is blue-green, so they stay distinguishable. Tier colour still
always comes with a label ("Tier 1 · foundation"), so colour is never the only signal.

## Type

- `--sans`: **Figtree**, then system UI fonts. Body 16px, line-height 1.62, tracking -0.005em.
- Headings weight **640**, tracking about -0.03em, tight line-height. Body stays 400 to 500 so the
  weight contrast does the work.
- `--mono`: IBM Plex Mono, for numbers, labels and eyebrows.
- Loaded from Google Fonts: Figtree variable (`wght@400..800`) and IBM Plex Mono (500, 600).
  Changing families or weights means editing the `<link>` in `tools/build.py`.

## Components introduced by this direction

| Class | What it is |
| --- | --- |
| `.sheet` | White card that flips every token to its light value |
| `.hero` | Split home hero: type left, `.idea` sheet right |
| `.idea` | The "whole idea" panel: 5% / 95% with what each covers |
| `.pill` | Lime label pill; `.answer__k` is the ink-on-lime variant |
| `.mark` | Solid lime highlight on graphite, true marker inside a sheet |
| `.card--tier` | Tier card: mono label, big coloured number, weight bar |
| `.card__bar > i` | The bar itself; its `width` is the tier's share of the result |

## Two states in the sidebar

`[aria-current="page"]` (the page you are on) is the lime pill. `.is-active` (the section you
have scrolled to, set by `site.js`) is `--bg-hover` with a 2px inset lime rail. They are different
questions, so they get different weights of signal; giving both the lime pill put two shouting
blocks in the sidebar at once.

## Metrics

| Token | Value |
| --- | --- |
| `--r-sm` / `--r` / `--r-lg` / `--r-xl` | 8px / 14px / 22px / 28px |
| `--pad` | 24px |
| `--side` | 268px (sidebar width) |
| `--head-h` | 56px (mobile top bar) |
| `--shadow-sm` / `--shadow` | Deeper than a light theme; shadows read weakly on graphite |

Buttons, pills and chips are fully rounded (99px).

## Accessibility notes

- Every text pairing on all eight built pages passes WCAG AA. Re-run the check after a colour
  change; a scripted audit over the built pages is the quickest way.
- `.mark` is a **solid** fill on graphite. A partial gradient marker would leave ink-coloured text
  sitting on the dark page, which is how it first shipped and why it is now explicit.
- Colour is never the only signal. Tier colour always pairs with a label and a weight bar.
- Focus ring is a 2px lime outline, switching to ink inside a sheet.
- Touch targets are at least 44px, including the mobile menu button.
- The sidebar is the lightest surface, so text on it has the least headroom on the page. The
  disclaimer in `.side__foot` uses `--tx-2` (5.4:1), not `--tx-3`, which would land at 4.6:1 for
  12px text. If `--side-bg` is lightened further, re-check both.
- `prefers-reduced-motion` is honoured globally.
- `@media print` flips every token back to a light theme, so printed pages stay on white paper.
