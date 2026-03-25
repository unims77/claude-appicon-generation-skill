# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**App Icon Generator** — Create 1024x1024 app icons using SVG code, then package them for Windows/macOS/Android/iOS/Web.

- **Tech Stack**: Python 3.10+ / Playwright Chromium / Pillow
- **Icon Generation**: Claude Code writes SVG XML directly → Playwright Chromium renders to PNG (RGBA, transparent rounded background)
- **Detailed Spec**: See `_SPEC.md` (takes precedence over CLAUDE.md for coding rules)

## Setup & Build

```bash
pip install -r requirements.txt
playwright install chromium   # Required for SVG→PNG rendering
```

## Core API

```python
# SVG → PNG conversion (single)
from src.converter import svg_to_png
svg_to_png("input.svg", "output.png")            # 1024x1024, rounded mask applied

# SVG string → PNG
from src.converter import svg_string_to_png
svg_string_to_png(svg_xml_str, "output.png")

# SVG batch conversion (all SVGs in directory)
from src.converter import batch_convert
batch_convert("svg_dir/", "png_dir/")             # Browser auto-closes after completion

# Full platform packaging (5 platforms)
from src.packager import package_all
package_all("icon_1024.png", "output/dir")

# Hyper mode: base SVG → 10 colors × 2 styles variants
from src.hyper import generate_all_variants
count = generate_all_variants("base_svg_dir/", "variants_dir/")

# Validation
from src.validator import validate_svg, validate_png, validate_package
validate_svg("icon.svg")                           # Checks viewBox 1024x1024, etc.
validate_package("output/dir")                     # Full platform completeness check
```

## Architecture — Data Flow

```
SVG XML (written by Claude)
  ↓ converter.py — Renders via Playwright Chromium singleton browser
  ↓               — 4x supersampled rounded mask alpha compositing (CORNER_RADIUS=200)
  ↓               — Multiply composites existing SVG transparency with mask
icon_1024.png (RGBA, transparent rounded corners)
  ↓ resizer.py — Pillow LANCZOS resize
  ↓ packager.py — Per-platform packaging
  ├── windows/app.ico          (16~256px multi-size ICO)
  ├── macos/icon.iconset/      (16~1024px retina pairs)
  ├── android/mipmap-*/        (48~192px + 512px Play Store)
  ├── ios/AppIcon.appiconset/  (20~1024px + Contents.json)
  └── web/                     (favicon, PWA, apple-touch, OG image, webmanifest)
```

**Key Design Decisions**:
- `converter.py` caches the Playwright browser as a **module-level singleton** — requires `close_browser()` call during batch conversion
- `hyper.py` uses SVG string manipulation (regex) to swap only background colors/gradients — generates SVG variants without PNG conversion
- `preview.py` generates HTML with inline-embedded SVGs — no server needed, opens directly in browser

## SVG Rules (for Designer Agent)

- `viewBox="0 0 1024 1024"` required
- No external resource references (URLs, fonts) — all elements must be inline
- No `<text>` tags — convert text to `<path>`
- Colors: use `MATERIAL_COLORS` from `config.py` (normal mode) or `HYPER_COLORS` (hyper mode)
- Background: `rx="200"` rounded rectangle — converter handles transparent masking, so SVG can have a full background

## Icon Pipeline

### `/_icon-generate [app_name]` — Normal Mode

```
[1] Environment setup → pip install, create output/{timestamp}/candidates/
[2] Research (icon-researcher) → trends/colors/symbols → user selects direction
[3] Design (icon-designer) → 12 SVG variants (Flat×3, Gradient×3, Outlined×2, Bold×2, Emoji×2)
[4] Generate preview.html → Light review
[5] User selection → On confirm: SVG→PNG 1024 + Full review / On revision: repeat
```

### `/_icon-auto-hyper [app_name]` — Hyper Mode

```
[1~3] Research → top 5 themes + 2 emojis = 7 directions auto-selected
[4]   Design → 28 base SVGs (A1~G4, 7 directions × 4 variants)
[5]   src/hyper.py → 28 × 10 colors × 2 styles = 560 SVG variants
[6]   Hyper preview HTML (grouped by direction, 10-column grid)
[7]   Full packaging (560 × 5 platforms)
```

### `/_icon-package <png_path>` — Packaging Only

```
Validate input PNG (1024x1024) → 5-platform packaging (Windows/macOS/Android/iOS/Web)
```

## Agents

| Agent | Model | Role |
|-------|-------|------|
| **icon-researcher** | opus | App analysis, trend/color/symbol research, design brief |
| **icon-designer** | opus | Generate icon variants as SVG code (12 or 28) |
| **icon-reviewer** | sonnet | SVG validity, PNG conversion, small-size rendering verification |
| **icon-packager** | sonnet | 5-platform packaging |

## Key Commands

| Command | Description |
|---------|-------------|
| `/_icon-auto` | One-stop auto (research → 12 designs → 5-platform packaging) |
| `/_icon-auto-hyper` | Hyper mode (7 directions × 560 variants + packaging) |
| `/_icon-generate` | Design + feedback loop |
| `/_icon-generate-hyper` | Hyper design + feedback loop |
| `/_icon-package` | 1024 PNG → 5-platform packaging |
| `/_plan` | Implementation plan (required for 3+ file changes) |

## Core Rules

- **HARD-GATE**: Run `/_plan` first for 3+ file changes, architecture/API/DB changes
- **Evidence-based completion**: No "it should work" — prove with actual build/test output
- **PNG transparent background**: All PNGs are RGBA, transparent outside rounded rectangle (rx=200) (4x supersampling)
- **File size**: 800 line limit, 50 line function limit
