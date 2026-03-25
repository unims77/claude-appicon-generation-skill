[English](README.md) | [한국어](README.ko.md)

# AI App Icon Generator

Generate production-ready app icons from SVG code and package them for **all major platforms** — powered by [Claude Code](https://claude.ai/code).

```
SVG Code → 1024x1024 PNG → Windows / macOS / Android / iOS / Web
```

## Features

- **AI-Driven Design** — Claude Code writes SVG XML directly, no design tools needed
- **5-Platform Packaging** — Windows ICO, macOS iconset, Android mipmap, iOS AppIcon, Web (favicon + PWA + OG)
- **Transparent Rounded Corners** — RGBA with 4x supersampled anti-aliased edges
- **Normal Mode** — 12 icon variants with interactive feedback loop
- **Hyper Mode** — 560 variants (7 directions × 4 designs × 10 colors × 2 styles)
- **HTML Preview** — Compare all candidates side-by-side in your browser

## Requirements

- Python 3.10+
- [Claude Code](https://claude.ai/code) CLI

## Installation

```bash
git clone https://github.com/unims77/claude-appicon-generation-skill.git
cd claude-appicon-generation-skill

pip install -r requirements.txt
playwright install chromium
```

## Quick Start

### With Claude Code Commands

```bash
# One-stop: research → design → package (12 variants)
/_icon-auto MyApp

# Hyper mode: 560 variants + 5-platform packaging
/_icon-auto-hyper MyApp

# Design with feedback loop
/_icon-generate MyApp

# Package an existing 1024x1024 PNG
/_icon-package path/to/icon_1024.png
```

### Output

All generated files are saved to the `output/{timestamp}/` folder:

```
output/20260325_143052/
├── candidates/          # SVG & PNG icon candidates
│   ├── *.svg
│   └── *.png
├── preview.html         # Open in browser to compare all candidates
└── package/             # 5-platform packaged icons (after confirmation)
    ├── windows/
    ├── macos/
    ├── android/
    ├── ios/
    └── web/
```

After icon generation, open **`preview.html`** in your browser to compare all candidates side-by-side, then select your preferred icon for packaging.

### With Python API

```python
from src.converter import svg_to_png, svg_string_to_png, batch_convert
from src.packager import package_all
from src.validator import validate_svg, validate_package

# Single SVG → PNG
svg_to_png("icon.svg", "icon.png")

# SVG string → PNG
svg_string_to_png('<svg viewBox="0 0 1024 1024">...</svg>', "icon.png")

# Batch convert all SVGs in a directory
batch_convert("svg_dir/", "png_dir/")

# Package for all 5 platforms
package_all("icon_1024.png", "output/")

# Validate
validate_svg("icon.svg")
validate_package("output/")
```

## Architecture

```
SVG XML (written by Claude Code)
  ↓ converter.py — Playwright Chromium rendering
  ↓               — 4x supersampled rounded mask (CORNER_RADIUS=200)
icon_1024.png (RGBA, transparent rounded corners)
  ↓ resizer.py — Pillow LANCZOS resize
  ↓ packager.py — Per-platform packaging
  ├── windows/app.ico          (16~256px multi-size ICO)
  ├── macos/icon.iconset/      (16~1024px retina pairs)
  ├── android/mipmap-*/        (48~192px + 512px Play Store)
  ├── ios/AppIcon.appiconset/  (20~1024px + Contents.json)
  └── web/                     (favicon, PWA, apple-touch, OG image)
```

## Project Structure

```
AI_AppIcon/
├── src/
│   ├── config.py       # Platform sizes, Material colors, constants
│   ├── converter.py    # SVG → PNG (Playwright Chromium)
│   ├── hyper.py        # Hyper mode variant generation
│   ├── packager.py     # 5-platform packaging
│   ├── preview.py      # HTML preview generation
│   ├── resizer.py      # PNG resizing
│   └── validator.py    # SVG/PNG/package validation
├── .claude/
│   ├── agents/         # AI agent definitions (researcher, designer, reviewer, packager)
│   └── commands/       # Pipeline command definitions
├── CLAUDE.md           # Claude Code project instructions
├── _SPEC.md            # Technical specification
└── requirements.txt
```

## Pipeline Modes

### Normal Mode (`/_icon-generate`)

1. **Research** — AI analyzes app concept, trends, colors, symbols
2. **User Selection** — Choose design direction from research brief
3. **Design** — 12 SVG variants (Flat×3, Gradient×3, Outlined×2, Bold×2, Emoji×2)
4. **Preview** — HTML preview for side-by-side comparison
5. **Feedback Loop** — Refine or confirm → PNG conversion + validation

### Hyper Mode (`/_icon-auto-hyper`)

1. **Research** — Auto-select top 5 themes + 2 emoji directions
2. **Design** — 28 base SVGs (7 directions × 4 variants)
3. **Variant Generation** — 28 × 10 colors × 2 styles = **560 SVG variants**
4. **Preview** — Grouped by direction, 10-column color grid
5. **Packaging** — All variants packaged for 5 platforms

## AI Agents

| Agent | Role |
|-------|------|
| **icon-researcher** | App analysis, trend/color/symbol research, design brief |
| **icon-designer** | Generate icon variants as SVG code |
| **icon-reviewer** | SVG validity, PNG quality, small-size rendering check |
| **icon-packager** | 5-platform packaging |

## SVG Rules

Icons must follow these rules for proper rendering:

- `viewBox="0 0 1024 1024"` — required
- No external resources (URLs, fonts) — all elements inline
- No `<text>` tags — convert text to `<path>`
- Colors from `MATERIAL_COLORS` (normal) or `HYPER_COLORS` (hyper) in `src/config.py`

## License

MIT
