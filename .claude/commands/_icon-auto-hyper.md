---
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task, WebSearch, WebFetch, mcp__fetch__fetch
description: Hyper mode auto icon generation. 7 directions × 4 designs × 10 colors × 2 styles = 560 variations + 5-platform packaging.
argument-hint: [app name] [--url URL] [--description "app description"]
---

# /_icon-auto-hyper - Hyper Mode Auto Icon Generation

Automatically generates mass icon variations.
- **7 directions** (5 themes + 2 emoji) × **4 designs** = 28 unique symbols
- 28 × **10 premium colors** × **2 styles** (Flat/Gradient) = **560 SVG variations**
- Full 5-platform packaging

## Pipeline Summary

```
[1] Environment setup
[2] Research → research_brief.md (5+ concepts)
[3] Auto-select top 5 themes + 2 emoji
[4] Design (hyper_mode) → 28 base SVGs
[5] Light validation
[6] Color/style variation generation (src/hyper.py) → 560 SVGs
[7] Hyper preview HTML
[8] Full packaging (560 × 5 platforms)
[9] Final report
```

## Execution Flow

### [1] Environment Setup

```bash
cd D:/AI/AppIcon2
pip install -r requirements.txt --quiet
```

```bash
python -c "
from src.config import create_output_dir
output_dir = create_output_dir('$ARGUMENTS_app_name')
print(f'OUTPUT_DIR={output_dir}')
"
```

### [2] Research (icon-researcher agent)

Invoke the **icon-researcher** agent.

Information to pass:
- App name: extracted from $ARGUMENTS
- App description: --description value
- URL: --url value (if provided)
- Output path: {OUTPUT_DIR}
- **Important**: Request at least 5 or more concept suggestions

The agent writes `{OUTPUT_DIR}/research_brief.md`.

### [3] Auto Concept Selection (5 themes + 2 emoji)

Read research_brief.md and **automatically adopt the top 5 theme concepts + 2 emoji concepts**.

```
Auto-selected concepts (hyper mode):
  A: {theme1} (A1~A4)
  B: {theme2} (B1~B4)
  C: {theme3} (C1~C4)
  D: {theme4} (D1~D4)
  E: {theme5} (E1~E4)
  F: {emoji1} (F1~F4)
  G: {emoji2} (G1~G4)
Starting design... (28 base symbols)
```

### [4] Design (icon-designer agent, hyper_mode)

Invoke the **icon-designer** agent with `hyper_mode=true`.

Information to pass:
- research_brief.md path
- 7 concept directions (A~G)
- Output path: {OUTPUT_DIR}
- **hyper_mode**: true

The agent generates 28 base SVGs: `{OUTPUT_DIR}/candidates/base/A1.svg` ~ `G4.svg`.

### [5] Light Validation

Run `validate_svg()` on all 28 base SVGs.
Auto-regenerate on failure (up to 3 times).

### [6] Color/Style Variation Generation

```bash
cd D:/AI/AppIcon2
python -c "
from src.hyper import generate_all_variants
count = generate_all_variants('{OUTPUT_DIR}/candidates/base', '{OUTPUT_DIR}/variants')
print(f'{count} variations generated')
"
```

28 × 10 × 2 = 560 SVGs auto-generated.

### [7] Hyper Preview HTML

```bash
python -c "
from src.preview import generate_hyper_preview
concepts = {'A': '...', 'B': '...', 'C': '...', 'D': '...', 'E': '...', 'F': '...', 'G': '...'}
path = generate_hyper_preview('{OUTPUT_DIR}', '{app_name}', concepts)
print(f'Preview: {path}')
"
```

### [8] Full Packaging

For each of the 560 variation SVGs:

```
FOR EACH variant SVG in {OUTPUT_DIR}/variants/*/*.svg:
  1. SVG → 1024 PNG conversion (src/converter.svg_to_png)
  2. 5-platform packaging (src/packager.package_all)
  3. Save results to {OUTPUT_DIR}/icons/{base}_{style}_{color}/
END FOR
```

### [9] Final Report

```
======================================================
  Hyper Icon Auto Complete
======================================================
  App: {app name}
  Concepts:
    A: {theme1}  B: {theme2}  C: {theme3}
    D: {theme4}  E: {theme5}
    F: {emoji1}  G: {emoji2}
  Output: {OUTPUT_DIR}/

  Generation results:
    Base symbols: 28 (7 directions × 4 designs)
    Color/style variations: 560 (28 × 10 colors × 2 styles)
    Packaging: 560 × 5 platforms

  Preview: {OUTPUT_DIR}/preview.html
======================================================
```

## Premium 10-Color Palette

| Color | HEX | Use Case |
|-------|-----|----------|
| Deep Navy | #0F172A | Finance/Business |
| Cobalt Blue | #2563EB | General purpose |
| Royal Purple | #6D28D9 | AI/Productivity |
| Teal Blue | #0F766E | Tech/Health |
| Emerald Green | #059669 | Health/Eco-friendly |
| Charcoal Black | #1F2937 | Premium/Simple |
| Burgundy | #7F1D1D | Premium |
| Warm Orange | #EA580C | Action/Tools |
| Mustard Gold | #CA8A04 | Premium/Unique |
| Soft Indigo | #4F46E5 | Trendy |
