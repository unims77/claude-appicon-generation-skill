"""App icon generator configuration - platform-specific sizes, Material colors, output paths."""

import os
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"

# ── Icon generation sizes ──────────────────────────────────────────────

PREVIEW_SIZE = 256   # Quick preview for candidate selection
FULL_SIZE = 1024     # Final output size
CORNER_RADIUS = 200  # Corresponds to SVG rx="200", rounded corner radius at 1024x1024

# ── Platform-specific icon sizes ──────────────────────────────────────────

ICON_SIZES = {
    "windows": {
        "description": "Windows ICO + UWP tile icons",
        "format": "ico",
        "sizes": [16, 24, 32, 48, 64, 128, 256],
        "output_file": "app.ico",
        "tile_sizes": {
            "Square44x44Logo": 44,
            "Square71x71Logo": 71,
            "Square150x150Logo": 150,
            "Square310x310Logo": 310,
            "StoreLogo": 50,
        },
    },
    "macos": {
        "description": "macOS iconset folder (for iconutil)",
        "format": "iconset",
        "retina_pairs": [
            (16, "icon_16x16.png"),
            (32, "icon_16x16@2x.png"),
            (32, "icon_32x32.png"),
            (64, "icon_32x32@2x.png"),
            (128, "icon_128x128.png"),
            (256, "icon_128x128@2x.png"),
            (256, "icon_256x256.png"),
            (512, "icon_256x256@2x.png"),
            (512, "icon_512x512.png"),
            (1024, "icon_512x512@2x.png"),
        ],
        "output_dir": "icon.iconset",
    },
    "android": {
        "description": "Android adaptive icon mipmap",
        "format": "png",
        "densities": {
            "mipmap-mdpi": 48,
            "mipmap-hdpi": 72,
            "mipmap-xhdpi": 96,
            "mipmap-xxhdpi": 144,
            "mipmap-xxxhdpi": 192,
        },
        "playstore_size": 512,
        "icon_filename": "ic_launcher.png",
    },
    "ios": {
        "description": "iOS AppIcon.appiconset",
        "format": "appiconset",
        "contents": [
            {"size": "20x20", "scale": "1x", "pixels": 20},
            {"size": "20x20", "scale": "2x", "pixels": 40},
            {"size": "20x20", "scale": "3x", "pixels": 60},
            {"size": "29x29", "scale": "1x", "pixels": 29},
            {"size": "29x29", "scale": "2x", "pixels": 58},
            {"size": "29x29", "scale": "3x", "pixels": 87},
            {"size": "40x40", "scale": "1x", "pixels": 40},
            {"size": "40x40", "scale": "2x", "pixels": 80},
            {"size": "40x40", "scale": "3x", "pixels": 120},
            {"size": "60x60", "scale": "2x", "pixels": 120},
            {"size": "60x60", "scale": "3x", "pixels": 180},
            {"size": "76x76", "scale": "1x", "pixels": 76},
            {"size": "76x76", "scale": "2x", "pixels": 152},
            {"size": "83.5x83.5", "scale": "2x", "pixels": 167},
            {"size": "1024x1024", "scale": "1x", "pixels": 1024},
        ],
    },
    "web": {
        "description": "Web favicon, PWA icons, OG image",
        "format": "mixed",
        "favicon_sizes": [16, 32, 48, 96],
        "favicon_ico_sizes": [16, 32, 48],
        "apple_touch_size": 180,
        "pwa_sizes": [192, 512],
        "og_size": {"width": 1200, "height": 630},
        "og_icon_size": 400,
    },
}

# ── Material Design color palette ──────────────────────────────────────

MATERIAL_COLORS = {
    "red":         {"500": "#F44336", "700": "#D32F2F"},
    "pink":        {"500": "#E91E63", "700": "#C2185B"},
    "purple":      {"500": "#9C27B0", "700": "#7B1FA2"},
    "deep_purple": {"500": "#673AB7", "700": "#512DA8"},
    "indigo":      {"500": "#3F51B5", "700": "#303F9F"},
    "blue":        {"500": "#2196F3", "700": "#1976D2"},
    "light_blue":  {"500": "#03A9F4", "700": "#0288D1"},
    "cyan":        {"500": "#00BCD4", "700": "#0097A7"},
    "teal":        {"500": "#009688", "700": "#00796B"},
    "green":       {"500": "#4CAF50", "700": "#388E3C"},
    "light_green": {"500": "#8BC34A", "700": "#689F38"},
    "lime":        {"500": "#CDDC39", "700": "#AFB42B"},
    "yellow":      {"500": "#FFEB3B", "700": "#FBC02D"},
    "amber":       {"500": "#FFC107", "700": "#FFA000"},
    "orange":      {"500": "#FF9800", "700": "#F57C00"},
    "deep_orange": {"500": "#FF5722", "700": "#E64A19"},
    "brown":       {"500": "#795548", "700": "#5D4037"},
    "grey":        {"500": "#9E9E9E", "700": "#616161"},
    "blue_grey":   {"500": "#607D8B", "700": "#455A64"},
}

# ── Hyper mode premium color palette (10 colors) ────────────────────────────

HYPER_COLORS = {
    "deep_navy":      {"hex": "#0F172A", "gradient_to": "#334155", "name": "Deep Navy"},
    "cobalt_blue":    {"hex": "#2563EB", "gradient_to": "#60A5FA", "name": "Cobalt Blue"},
    "royal_purple":   {"hex": "#6D28D9", "gradient_to": "#A78BFA", "name": "Royal Purple"},
    "teal_blue":      {"hex": "#0F766E", "gradient_to": "#2DD4BF", "name": "Teal Blue"},
    "emerald_green":  {"hex": "#059669", "gradient_to": "#6EE7B7", "name": "Emerald Green"},
    "charcoal_black": {"hex": "#1F2937", "gradient_to": "#4B5563", "name": "Charcoal Black"},
    "burgundy":       {"hex": "#7F1D1D", "gradient_to": "#DC2626", "name": "Burgundy"},
    "warm_orange":    {"hex": "#EA580C", "gradient_to": "#FB923C", "name": "Warm Orange"},
    "mustard_gold":   {"hex": "#CA8A04", "gradient_to": "#FACC15", "name": "Mustard Gold"},
    "soft_indigo":    {"hex": "#4F46E5", "gradient_to": "#818CF8", "name": "Soft Indigo"},
}


def create_output_dir(app_name: str = "") -> Path:
    """Create a timestamp-based output folder."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    suffix = f"_{app_name}" if app_name else ""
    folder_name = f"{timestamp}{suffix}"
    output_path = OUTPUT_DIR / folder_name

    (output_path / "candidates").mkdir(parents=True, exist_ok=True)

    return output_path
