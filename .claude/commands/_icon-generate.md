---
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task, WebSearch, WebFetch, mcp__fetch__fetch
description: App icon design pipeline. Runs research → design → validation → user feedback loop.
argument-hint: [app name] [--url URL] [--description "app description"]
---

# /_icon-generate - App Icon Design Pipeline

Designs app icons. Iterates with user feedback until satisfaction.
Packaging is run separately with `/_icon-package`.

## Execution Flow

### [1] Environment Setup

1. Check Python dependencies:
```bash
cd D:/AI/AppIcon2
pip install -r requirements.txt --quiet
```

2. Create output folder (only candidates/, no source/):
```bash
python -c "
from src.config import create_output_dir
output_dir = create_output_dir('$ARGUMENTS_app_name')
print(f'OUTPUT_DIR={output_dir}')
"
```

Use the generated `OUTPUT_DIR` in all subsequent steps.

### [2] Research (icon-researcher agent)

Invoke the **icon-researcher** agent.

Information to pass:
- App name: extracted from $ARGUMENTS
- App description: --description value, or ask the user
- URL: --url value (if provided)
- Output path: {OUTPUT_DIR}

The agent writes `{OUTPUT_DIR}/research_brief.md`.

**Checkpoint**: Show the design brief to the user and have them **select 3 concept directions**.
- Default: researcher's top 3 auto-recommended
- User can choose a different combination (e.g., "concepts 1, 3, 5" or "color from 2 + shape from 4")
- 12 variations are distributed across 3 concepts: A(01~04), B(05~08), C(09~12)

### [3] Design (icon-designer agent)

Invoke the **icon-designer** agent.

Information to pass:
- research_brief.md path
- User-selected **3 concept directions** (A, B, C)
- Output path: {OUTPUT_DIR}

The agent generates:
- `{OUTPUT_DIR}/candidates/01~12.svg` (3 concepts × 4 styles)
- `{OUTPUT_DIR}/preview.html` (browser preview)

**No PNG conversion** — SVGs are verified directly in the browser.

### [4] Light Validation (icon-reviewer agent)

Invoke the **icon-reviewer** agent with `review_mode=light`.

Information to pass:
- `review_mode`: `"light"`
- `{target_dir}`: `{OUTPUT_DIR}/candidates/`

**Light review**: SVG validity check only (no PNG validation).

Failed candidates are auto-regenerated (up to 3 times). Only passing candidates are kept.
After regeneration, preview.html is also refreshed.

### [5] Present Candidates to User

Provide the preview.html path to the user:
```
Check the candidates in your browser:
{OUTPUT_DIR}/preview.html
```

Use **AskUserQuestion** to request user selection:
- Which icon number would you like to select?
- Any modifications needed? (color change, shape adjustment, style change, etc.)

### [6] Feedback Loop (repeat until user is satisfied)

Branch based on the user's response:

#### A. "Confirm as-is" → Create output/ + Full validation

1. Create output/ folder and copy SVG:
```bash
mkdir -p '{OUTPUT_DIR}/output'
cp '{OUTPUT_DIR}/candidates/{selected_number}.svg' '{OUTPUT_DIR}/output/icon.svg'
```

2. Convert selected SVG to 1024x1024 PNG:
```bash
cd D:/AI/AppIcon2
python -c "
from src.converter import svg_to_png
from src.config import FULL_SIZE
svg_to_png('{OUTPUT_DIR}/output/icon.svg', '{OUTPUT_DIR}/output/icon_1024.png', width=FULL_SIZE, height=FULL_SIZE)
print('1024x1024 conversion complete')
"
```

3. Invoke the **icon-reviewer** agent with `review_mode=full`:
   - `review_mode`: `"full"`
   - `{target_dir}`: `{OUTPUT_DIR}/output/`
   - `{OUTPUT_DIR}/research_brief.md`

4. Handle full review results:
   - **PASS** → Confirmation complete
   - **FAIL** → Report failed items to user, request choice to fix or accept

5. On confirmation complete, output:
```
======================================================
  Icon Design Complete
======================================================
  App: {app name}
  Output: {OUTPUT_DIR}/output/

  Confirmed files:
    - icon.svg      (SVG original)
    - icon_1024.png  (1024x1024 PNG)

  For packaging:
    /_icon-package {OUTPUT_DIR}/output/icon_1024.png
======================================================
```

Pipeline ends.

#### B. Modification request → Revise design and re-display

1. Re-invoke the **icon-designer** agent.
   Information to pass:
   - Selected candidate SVG path
   - User's modification request (color change, shape adjustment, etc.)
   - Output path: `{OUTPUT_DIR}/candidates/` (overwrite existing number or new number)

2. Regenerate preview.html:
```bash
cd D:/AI/AppIcon2
python -c "
from src.preview import generate_preview
generate_preview('{OUTPUT_DIR}', '{app_name}')
print('preview.html refreshed')
"
```

3. Re-validate modified results with **icon-reviewer** at `review_mode=light`

4. Present preview.html to user again

5. **Return to [6]** — repeat until user is satisfied

## Usage Examples

```bash
# Basic usage
/_icon-generate MyApp --description "A to-do management app"

# With URL
/_icon-generate MyApp --url https://myapp.com --description "A to-do management app"
```

## Error Handling

- **Dependency installation failure**: cairosvg/pycairo requires Cairo runtime. Display guidance message
- **SVG conversion failure**: SVG code error. Request redesign from the design team
- **3 validation failures**: Exclude the candidate and display remaining candidates only
