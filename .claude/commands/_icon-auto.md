---
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task, WebSearch, WebFetch, mcp__fetch__fetch
description: Auto icon generation & full packaging. Research → Design → Validation → one-stop execution packaging all 12 icons for 5 platforms.
argument-hint: [app name] [--url URL] [--description "app description"]
---

# /_icon-auto - Auto Icon Generation & Full Packaging

Just provide app info and it automatically runs everything from research to packaging 12 icons across 5 platforms.
For manual feedback loops, use `/_icon-generate` instead.

## Pipeline Summary

```
[1] Environment setup
[2] Research → research_brief.md
[3] Auto concept selection (top picks adopted)
[4] Design → 12 SVGs + preview.html
[5] Light validation → auto-regenerate on FAIL
[6] Full packaging (passing candidates × 5 platforms)
[7] Final report
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
- App description: --description value, or ask the user
- URL: --url value (if provided)
- Output path: {OUTPUT_DIR}

The agent writes `{OUTPUT_DIR}/research_brief.md`.

### [3] Auto Concept Selection (Top 3)

Read research_brief.md and **automatically adopt the top 3 concepts**.
Distribute 12 variations across 3 concepts:
- Concept A (01~04): 4 variations
- Concept B (05~08): 4 variations
- Concept C (09~12): 4 variations

Notify the user of the 3 selected concepts:

```
Auto-selected concepts:
  A: {concept_name} — {description} (01~04)
  B: {concept_name} — {description} (05~08)
  C: {concept_name} — {description} (09~12)
Starting design...
```

### [4] Design (icon-designer agent)

Invoke the **icon-designer** agent.

Information to pass:
- research_brief.md path
- Auto-selected **3 concept directions** (A, B, C)
- Output path: {OUTPUT_DIR}

The agent generates:
- `{OUTPUT_DIR}/candidates/01~12.svg`
- `{OUTPUT_DIR}/preview.html`

### [5] Light Validation (icon-reviewer agent)

Invoke the **icon-reviewer** agent with `review_mode=light`.

Information to pass:
- `review_mode`: `"light"`
- `{target_dir}`: `{OUTPUT_DIR}/candidates/`

Failed candidates are **auto-regenerated** (up to 3 times).
After regeneration, preview.html is also refreshed.

Brief report to the user:
```
Light validation complete: {N} of 12 passed
```

### [6] Full Packaging (auto-executed)

Execute **sequentially** for each confirmed candidate:

```
FOR EACH confirmed candidate (e.g., 01, 02, ... 12):
```

#### 6-1. Create Individual Output Folder
```bash
mkdir -p '{OUTPUT_DIR}/icons/{number}'
cp '{OUTPUT_DIR}/candidates/{number}.svg' '{OUTPUT_DIR}/icons/{number}/icon.svg'
```

#### 6-2. SVG → 1024 PNG Conversion
```bash
cd D:/AI/AppIcon2
python -c "
from src.converter import svg_to_png
from src.config import FULL_SIZE
svg_to_png('{OUTPUT_DIR}/icons/{number}/icon.svg', '{OUTPUT_DIR}/icons/{number}/icon_1024.png', width=FULL_SIZE, height=FULL_SIZE)
"
```

#### 6-3. Full Validation
Invoke the **icon-reviewer** agent with `review_mode=full`:
- `{target_dir}`: `{OUTPUT_DIR}/icons/{number}/`
- `{OUTPUT_DIR}/research_brief.md`

**On FAIL**: auto-retry (up to 3 times). After 3 failures, exclude the candidate and report to the user.

#### 6-4. 5-Platform Packaging
```bash
cd D:/AI/AppIcon2
python -c "
from src.packager import package_all
results = package_all('{OUTPUT_DIR}/icons/{number}/icon_1024.png', '{OUTPUT_DIR}/icons/{number}')
print(results)
"
```

```
END FOR
```

### [7] Final Report

```
======================================================
  Icon Auto Complete
======================================================
  App: {app name}
  Concepts:
    A: {concept_A_name} (01~04)
    B: {concept_B_name} (05~08)
    C: {concept_C_name} (09~12)
  Output: {OUTPUT_DIR}/icons/

  Packaging results:
    Passed: {N} / Total: 12

    Per icon (icons/{number}/):
      - icon.svg          (SVG original)
      - icon_1024.png     (1024x1024 PNG)
      - windows/app.ico   (7 sizes)
      - macos/icon.iconset/ (10 files)
      - android/mipmap-*/ (5 densities + playstore)
      - ios/AppIcon.appiconset/ (15 files)
      - web/favicon.ico + og-image.png + ...

  Preview: {OUTPUT_DIR}/preview.html
======================================================
```

## Usage Examples

```bash
# Basic usage
/_icon-auto MyApp --description "A to-do management app"

# With URL
/_icon-auto MyApp --url https://myapp.com --description "A to-do management app"
```

## Error Handling

- **Research failure**: Fall back to default colors/styles and proceed with design
- **Design failure**: Report to user with error log, suggest switching to `/_icon-generate` for manual mode
- **3 validation failures**: Exclude the candidate and continue packaging the rest
- **Packaging failure**: Report failed platform with error log, continue with the rest

## Differences from `/_icon-generate`

| Item | `/_icon-generate` | `/_icon-auto` |
|------|-------------------|---------------|
| Concept selection | User chooses manually | Top picks auto-adopted |
| Feedback loop | Unlimited iterations | Single confirmation only |
| Packaging targets | 1 selected icon | All passing icons (default 12) |
| Packaging scope | Separate `/_icon-package` | Included automatically (5 platforms) |
| Use case | Fine-tuned design adjustments | Rapid bulk generation |
