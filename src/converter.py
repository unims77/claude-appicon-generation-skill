"""SVG to PNG conversion module (Playwright Chromium + Pillow post-processing)."""

import io
import logging
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw
from playwright.sync_api import sync_playwright

from src.config import CORNER_RADIUS

logger = logging.getLogger(__name__)

# Module-level cache for reusing the Playwright browser instance
_browser_context = {"browser": None, "playwright": None}


def _get_browser():
    """Get the Playwright Chromium browser (singleton)."""
    if _browser_context["browser"] is None:
        pw = sync_playwright().start()
        _browser_context["playwright"] = pw
        _browser_context["browser"] = pw.chromium.launch()
    return _browser_context["browser"]


def close_browser():
    """Close the module-level browser. Call after batch operations are complete."""
    if _browser_context["browser"] is not None:
        _browser_context["browser"].close()
        _browser_context["browser"] = None
    if _browser_context["playwright"] is not None:
        _browser_context["playwright"].stop()
        _browser_context["playwright"] = None


def _create_rounded_mask(size: int, radius: int) -> Image.Image:
    """Create a rounded rectangle alpha mask (with anti-aliasing).

    Uses 4x supersampling followed by LANCZOS downscale for smooth edges.
    """
    scale = 4
    large = Image.new("L", (size * scale, size * scale), 0)
    draw = ImageDraw.Draw(large)
    draw.rounded_rectangle(
        [0, 0, size * scale - 1, size * scale - 1],
        radius=radius * scale,
        fill=255,
    )
    return large.resize((size, size), Image.LANCZOS)


def _render_svg_to_rgba(svg_path: Path, width: int, height: int) -> Image.Image:
    """Render an SVG to an RGBA image using Playwright Chromium.

    Accurately handles all SVG attributes including opacity, fill-opacity, filter, mask, etc.
    """
    svg_content = svg_path.read_text(encoding="utf-8")

    browser = _get_browser()
    page = browser.new_page(viewport={"width": width, "height": height})
    try:
        html = (
            "<!DOCTYPE html>"
            "<html><head><style>"
            "* { margin:0; padding:0; }"
            "body { overflow:hidden; }"
            "svg { display:block; width:100%; height:100%; }"
            "</style></head>"
            f"<body>{svg_content}</body></html>"
        )
        page.set_content(html, wait_until="load")
        screenshot = page.screenshot(type="png", omit_background=True)
    finally:
        page.close()

    return Image.open(io.BytesIO(screenshot)).convert("RGBA")


def svg_to_png(
    svg_path: str | Path,
    png_path: str | Path,
    width: int = 1024,
    height: int = 1024,
) -> Path:
    """Convert an SVG file to PNG.

    Renders via Playwright Chromium to accurately reflect all SVG attributes including opacity.
    Multiplies a rounded rectangle mask with existing alpha to make corners transparent.
    """
    svg_path = Path(svg_path)
    png_path = Path(png_path)
    png_path.parent.mkdir(parents=True, exist_ok=True)

    img = _render_svg_to_rgba(svg_path, width, height)

    # Multiply-composite existing alpha (SVG internal transparency) with rounded mask
    mask = _create_rounded_mask(width, CORNER_RADIUS)
    existing_alpha = img.split()[3]
    combined_alpha = ImageChops.multiply(existing_alpha, mask)
    img.putalpha(combined_alpha)

    img.save(str(png_path), format="PNG")
    return png_path


def svg_string_to_png(
    svg_content: str,
    png_path: str | Path,
    width: int = 1024,
    height: int = 1024,
) -> Path:
    """Convert an SVG string to PNG."""
    png_path = Path(png_path)
    png_path.parent.mkdir(parents=True, exist_ok=True)

    tmp_svg = png_path.parent / "_tmp_convert.svg"
    tmp_svg.write_text(svg_content, encoding="utf-8")
    try:
        svg_to_png(tmp_svg, png_path, width, height)
    finally:
        tmp_svg.unlink(missing_ok=True)
    return png_path


def batch_convert(svg_dir: str | Path, png_dir: str | Path, size: int = 1024) -> list[Path]:
    """Convert all SVGs in a directory to PNG."""
    svg_dir = Path(svg_dir)
    png_dir = Path(png_dir)
    png_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for svg_file in sorted(svg_dir.glob("*.svg")):
        png_file = png_dir / f"{svg_file.stem}.png"
        svg_to_png(svg_file, png_file, width=size, height=size)
        results.append(png_file)

    close_browser()
    return results
