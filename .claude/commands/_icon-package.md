---
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
description: Packages a confirmed icon PNG for Windows/macOS/Android/iOS platforms.
argument-hint: <icon_1024.png path> [--output <output directory>]
---

# /_icon-package - Icon Platform Packaging

Packages a confirmed 1024x1024 PNG icon for 4 platforms (Windows, macOS, Android, iOS).

## Input

- Extract icon PNG path from `$ARGUMENTS`
- If `--output` option is provided, output to that directory
- Without the option, use the directory containing the PNG file (typically `{timestamp}/output/`)

## Output Structure

```
{output_dir}/
├── icon.svg          (original SVG — already exists)
├── icon_1024.png     (original PNG — already exists)
├── windows/
│   └── app.ico       (7 sizes: 16,24,32,48,64,128,256)
├── macos/
│   └── icon.iconset/ (10 retina pair files)
├── android/
│   ├── mipmap-mdpi/     (48x48)
│   ├── mipmap-hdpi/     (72x72)
│   ├── mipmap-xhdpi/    (96x96)
│   ├── mipmap-xxhdpi/   (144x144)
│   ├── mipmap-xxxhdpi/  (192x192)
│   └── playstore-icon.png (512x512)
├── ios/
│   └── AppIcon.appiconset/
│       ├── Contents.json
│       └── icon_*.png  (15 sizes)
└── web/
    ├── favicon.ico           (16+32+48 multi-size)
    ├── favicon-16.png
    ├── favicon-32.png
    ├── favicon-48.png
    ├── favicon-96.png
    ├── apple-touch-icon.png  (180x180)
    ├── icon-192.png          (PWA)
    ├── icon-512.png          (PWA)
    ├── og-image.png          (1200x630)
    └── site.webmanifest
```

## Execution Flow

### [1] Input Validation

```bash
cd D:/AI/AppIcon2
python -c "
from src.validator import validate_png
result = validate_png('$ARGUMENTS_PNG_path', 1024)
print(result)
"
```

- Verify it is PNG format
- Verify it is 1024x1024 square
- On failure, output error message and terminate

### [2] Packaging (icon-packager agent)

Invoke the **icon-packager** agent.

Information to pass:
- Input PNG path
- Output directory path (directory containing the PNG)

The agent packages for 4 platforms:
```bash
cd D:/AI/AppIcon2
python -c "
from src.packager import package_all
results = package_all('{PNG_PATH}', '{OUTPUT_DIR}')
print(results)
"
```

### [3] Completion Report

```
======================================================
  Packaging Complete
======================================================
  Input: {PNG path}
  Output: {OUTPUT_DIR}

  Per-platform results:
    [1] Windows   app.ico (7 sizes)
    [2] macOS     icon.iconset/ (10 files)
    [3] Android   mipmap-*/ (5 densities + playstore)
    [4] iOS       AppIcon.appiconset/ (15 files + Contents.json)
    [5] Web       favicon + PWA icons + OG image + manifest

  Total files: {count}
======================================================
```

## Usage Examples

```bash
# Package an icon generated with _icon-generate
/_icon-package output/2026-03-25_DriveMap/output/icon_1024.png

# Specify output directory
/_icon-package my_icon.png --output dist/icons

# Package an externally sourced PNG
/_icon-package D:/assets/logo_1024.png
```

## Error Handling

- **File not found**: Display a message to check the path
- **Size mismatch**: If not 1024x1024, ask the user whether to resize
- **Packaging failure**: Report failed platform with error log
