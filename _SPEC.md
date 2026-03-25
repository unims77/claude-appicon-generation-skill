# _SPEC.md - App Icon Generator Project Spec

## Project Purpose

Generate app icons using SVG code and package them for Windows/macOS/Android/iOS/Web platforms.

## Tech Stack

- **Language**: Python 3.10+
- **Image Libraries**: Pillow (resize, ICO generation), Playwright Chromium (SVG→PNG rendering)
- **Icon Generation**: Claude Code writes SVG XML directly → Playwright Chromium converts to PNG

## Source Structure

```
src/
├── config.py      # Per-platform sizes, Material colors, output paths
├── converter.py   # SVG → PNG conversion (Playwright Chromium)
├── resizer.py     # PNG resize (Pillow LANCZOS)
├── packager.py    # Per-platform packaging (ICO, iconset, mipmap, appiconset, web)
├── preview.py     # HTML preview generation
├── hyper.py       # Hyper mode SVG variant generation
└── validator.py   # SVG/PNG/package validation
```

## SVG Rules

- viewBox: must be `0 0 1024 1024`
- No external resource references (URLs, fonts) — all elements must be inline
- No `<text>` tags — convert text to `<path>`
- Colors: prefer MATERIAL_COLORS from `src/config.py`

## Output Rules

- All output is generated under the `output/` directory in timestamped folders
- Timestamp format: `YYYY-MM-DD_HHMMSS_app_name`
- `output/` is included in .gitignore

## PNG Output Rules

- icon_1024.png is saved in **RGBA mode** (with alpha channel)
- Areas outside the rounded rectangle (rx=200) are **transparent**
- 4x supersampled mask for anti-aliased smooth edges
- Corner radius: `CORNER_RADIUS` in `src/config.py` (default 200, based on 1024)

## Team Composition (Claude Code Agents)

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| icon-researcher | Research | App name/description/URL | research_brief.md |
| icon-designer | SVG design | Brief + user selection | 10 SVGs + PNG |
| icon-reviewer | Validation | SVG + PNG | PASS/FAIL report |
| icon-packager | Packaging | Confirmed PNG | 5-platform packages |

## Pipeline

```
/_icon-generate → Research → [User selection] → Design → [User selection] → Validation → Packaging
```
