"""Hyper mode - Generate variants of base SVGs in 10 colors x 2 styles (Flat/Gradient)."""

import re
from pathlib import Path

from src.config import HYPER_COLORS

# Background rect pattern: <rect ... rx="1xx" or rx="2xx" ... fill="..." />
_BG_RECT_PATTERN = re.compile(
    r'(<rect[^>]*?)(fill="[^"]*")([^>]*?rx="[12]\d{2}"[^>]*?>)',
    re.DOTALL,
)
_BG_RECT_PATTERN_ALT = re.compile(
    r'(<rect[^>]*?rx="[12]\d{2}"[^>]*?)(fill="[^"]*")([^>]*?>)',
    re.DOTALL,
)

# Prefix to avoid duplicate gradient IDs within defs
_GRAD_ID = "hyper_bg_grad"


def _replace_bg_fill(svg_content: str, new_fill: str) -> str:
    """Replace the fill attribute of the SVG background rect."""
    result = _BG_RECT_PATTERN.sub(
        lambda m: f'{m.group(1)}fill="{new_fill}"{m.group(3)}',
        svg_content,
        count=1,
    )
    if result == svg_content:
        result = _BG_RECT_PATTERN_ALT.sub(
            lambda m: f'{m.group(1)}fill="{new_fill}"{m.group(3)}',
            svg_content,
            count=1,
        )
    return result


def _inject_gradient_def(
    svg_content: str, color_from: str, color_to: str, grad_id: str = "",
) -> str:
    """Inject a linearGradient definition into the SVG and replace the background fill with url(#...)."""
    gid = grad_id or _GRAD_ID
    grad_def = (
        f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0%" stop-color="{color_to}"/>'
        f'<stop offset="100%" stop-color="{color_from}"/>'
        f'</linearGradient></defs>'
    )

    if "<defs>" in svg_content.lower():
        svg_content = re.sub(
            r'(<defs[^>]*>)',
            lambda m: m.group(1) + (
                f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">'
                f'<stop offset="0%" stop-color="{color_to}"/>'
                f'<stop offset="100%" stop-color="{color_from}"/>'
                f'</linearGradient>'
            ),
            svg_content,
            count=1,
            flags=re.IGNORECASE,
        )
    else:
        svg_content = svg_content.replace(
            "<svg ", f"<svg ", 1
        )
        svg_content = re.sub(
            r'(xmlns="[^"]*"[^>]*>)',
            lambda m: m.group(1) + grad_def,
            svg_content,
            count=1,
        )

    return _replace_bg_fill(svg_content, f"url(#{gid})")


def generate_variant(
    base_svg: str,
    color_key: str,
    style: str,
    base_name: str = "",
) -> str:
    """Transform a single base SVG into a specific color/style variant.

    Args:
        base_svg: Base SVG string
        color_key: HYPER_COLORS key (e.g., "deep_navy")
        style: "flat" or "grad"
        base_name: Base SVG name (e.g., "A1") - used to prevent gradient ID collisions
    """
    color_info = HYPER_COLORS[color_key]

    if style == "flat":
        return _replace_bg_fill(base_svg, color_info["hex"])
    else:
        suffix = f"{base_name}_{color_key}" if base_name else color_key
        unique_id = f"{_GRAD_ID}_{suffix}"
        return _inject_gradient_def(
            base_svg, color_info["hex"], color_info["gradient_to"],
            grad_id=unique_id,
        )


def generate_all_variants(base_svg_dir: str | Path, output_dir: str | Path) -> int:
    """Generate 10-color x 2-style variants for all files in the base SVG directory.

    Args:
        base_svg_dir: Base SVG directory (A1.svg ~ G4.svg)
        output_dir: Variant output directory

    Returns:
        Number of variant SVGs generated
    """
    base_dir = Path(base_svg_dir)
    out_dir = Path(output_dir)
    count = 0

    for svg_file in sorted(base_dir.glob("*.svg")):
        base_name = svg_file.stem
        base_content = svg_file.read_text(encoding="utf-8")
        variant_dir = out_dir / base_name
        variant_dir.mkdir(parents=True, exist_ok=True)

        for color_key in HYPER_COLORS:
            for style in ("flat", "grad"):
                variant_svg = generate_variant(
                    base_content, color_key, style, base_name=base_name,
                )
                out_path = variant_dir / f"{style}_{color_key}.svg"
                out_path.write_text(variant_svg, encoding="utf-8")
                count += 1

    return count
