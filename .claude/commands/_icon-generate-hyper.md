---
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task, WebSearch, WebFetch, mcp__fetch__fetch
description: Hyper mode icon design. 7 directions × 4 designs × 10 colors × 2 styles = 560 variations. Includes user feedback loop.
argument-hint: [app name] [--url URL] [--description "app description"]
---

# /_icon-generate-hyper - Hyper Mode Icon Design

Same mass production as `/_icon-auto-hyper` but **includes a user feedback loop**.

## Pipeline

```
[1] Environment setup
[2] Research → research_brief.md
[3] ★ Checkpoint: Request user to select 7 directions ★
[4] Design (hyper_mode) → 28 base SVGs
[5] Light validation
[6] Color/style variation generation → 560 SVGs
[7] Hyper preview HTML
[8] ★ Checkpoint: Request user to review preview and select ★
[9] Package selected variations only (or all)
[10] Final report
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
Request at least 5 or more concepts + emoji candidates.

### [3] User Concept Selection (Checkpoint)

Show the brief to the user and request **7 direction selections**:
- 5 theme directions (A~E)
- 2 emoji/emoticon directions (F~G)

Default: researcher's top 5 + 2 emoji auto-recommended.
User can choose a different combination if preferred.

### [4] Design (icon-designer, hyper_mode)

Invoke the **icon-designer** agent with `hyper_mode=true`.
Generate 28 base SVGs: `{OUTPUT_DIR}/candidates/base/A1.svg` ~ `G4.svg`

### [5] Light Validation

Validate 28 base SVGs with `validate_svg()`. Auto-regenerate on failure.

### [6] Color/Style Variation Generation

```bash
python -c "
from src.hyper import generate_all_variants
count = generate_all_variants('{OUTPUT_DIR}/candidates/base', '{OUTPUT_DIR}/variants')
print(f'{count} variations generated')
"
```

### [7] Hyper Preview HTML

```bash
python -c "
from src.preview import generate_hyper_preview
path = generate_hyper_preview('{OUTPUT_DIR}', '{app_name}', {concepts_dict})
print(f'Preview: {path}')
"
```

### [8] User Selection (Checkpoint)

Provide the preview HTML path and use **AskUserQuestion** to request selection:
- Which variations would you like to package? (e.g., "A2_flat_cobalt_blue, C1_grad_royal_purple")
- Package all? Or selected only?
- If modifications are needed, revise base symbols and regenerate variations

### [9] Packaging

For user-selected variations (or all):
1. SVG → 1024 PNG conversion
2. 5-platform packaging
3. Save under `{OUTPUT_DIR}/icons/`

### [10] Final Report

Same format as `/_icon-auto-hyper`.

## Feedback Loop

When the user requests modifications:
1. Revise base symbols (re-invoke icon-designer)
2. Regenerate variations (src/hyper.py)
3. Refresh preview
4. Return to [8]
