# Design tokens

Source of truth is the `:root` block at the top of `assets/css/style.css`. This file records the
intent behind the values. When you change one, change both.

## Principles

- **White surface only.** No dark mode, no tinted page backgrounds.
- **Traffic-light colour is meaning, not decoration.** Green = foundation, amber = worth tuning,
  red = ignore until the rest is automatic. Do not use these three for anything else.
- **Blue is for action only** (links, primary emphasis). Black (`--tx`) is the primary button.
- **Quiet chrome.** Hairline borders and very light shadows. Colour comes from the tiers.

## Surfaces

| Token | Value | Use |
| --- | --- | --- |
| `--bg` | `#FFFFFF` | Page and cards |
| `--bg-subtle` | `#FAFBFC` | Hover on white rows |
| `--bg-sunken` | `#F4F6F8` | Inset areas |
| `--bg-hover` | `#EFF2F5` | Hover on controls |

## Text

| Token | Value | Use |
| --- | --- | --- |
| `--tx` | `#0B0D0E` | Headings, body |
| `--tx-2` | `#3F464D` | Secondary body |
| `--tx-3` | `#6F7780` | Captions, metadata |
| `--tx-4` | `#9AA1A9` | Icons, disabled |

## Lines

`--line #E5E8EC` (default border), `--line-2 #D3D8DE` (stronger, on controls).

## Traffic light

Each colour has four roles: solid (`--green`), ink for text on a tint (`--green-ink`), tint
background (`--green-bg`), tint border (`--green-line`).

| | solid | ink | bg | line |
| --- | --- | --- | --- | --- |
| Green | `#0F8A54` | `#0A6640` | `#E7F6EE` | `#BCE5CF` |
| Amber | `#D98014` | `#96540A` | `#FEF4E6` | `#F6DCB4` |
| Red | `#D92D20` | `#A11F16` | `#FDECEA` | `#F7C9C4` |

Use the **ink** value for any text on a tint. Solid colours are for borders, icons and dots.

## Action

`--blue #1257C4`, `--blue-ink #0E459C`, `--blue-bg #EAF1FD`.

## Type

- `--sans`: Inter, then system UI fonts. Body 16px, line-height 1.62, tracking -0.011em.
- `--mono`: IBM Plex Mono, for numbers and labels.
- Only Inter (400 to 700) and IBM Plex Mono (500, 600) are loaded, from Google Fonts. Adding a
  weight or family means editing the `<link>` in `tools/build.py`.

## Metrics

| Token | Value |
| --- | --- |
| `--r-sm` / `--r` / `--r-lg` | 6px / 8px / 12px |
| `--pad` | 24px |
| `--side` | 268px (sidebar width) |
| `--head-h` | 56px (mobile top bar) |
| `--shadow-sm` | 0 1px 2px, 5% |
| `--shadow` | 0 1px 3px plus 8px 24px soft lift |

## Accessibility notes

- Colour is never the only signal. Tier colours always come with a label ("Tier 1", "Green:
  foundation").
- `prefers-reduced-motion` is honoured globally in `style.css`.
- Keep ink-on-tint pairs for text. Check contrast if you add a new tint.
