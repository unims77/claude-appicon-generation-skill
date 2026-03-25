"""Icon validation module - SVG validity, PNG size, and package completeness checks."""

from pathlib import Path
from xml.etree import ElementTree

from PIL import Image

from src.config import ICON_SIZES


def validate_svg(svg_path: str | Path) -> dict:
    """Validate an SVG file."""
    svg_path = Path(svg_path)
    errors = []

    if not svg_path.exists():
        return {"valid": False, "errors": ["File does not exist"]}

    content = svg_path.read_text(encoding="utf-8")

    # XML parsing
    try:
        root = ElementTree.fromstring(content)
    except ElementTree.ParseError as e:
        return {"valid": False, "errors": [f"XML parsing failed: {e}"]}

    # SVG tag check
    tag = root.tag.lower()
    if not tag.endswith("svg"):
        errors.append(f"Root tag is not svg: {tag}")

    # viewBox check
    viewbox = root.get("viewBox") or root.get("viewbox")
    if viewbox:
        parts = viewbox.replace(",", " ").split()
        if len(parts) == 4:
            w, h = float(parts[2]), float(parts[3])
            if w != 1024 or h != 1024:
                errors.append(f"viewBox is not 1024x1024: {w}x{h}")
        else:
            errors.append(f"Invalid viewBox format: {viewbox}")
    else:
        errors.append("Missing viewBox attribute")

    # Check for child elements (prevent empty SVG)
    if len(root) == 0:
        errors.append("SVG has no child elements (empty icon)")

    # Check for external resource references
    svg_str = content.lower()
    if "xlink:href" in svg_str and ("http://" in svg_str or "https://" in svg_str):
        errors.append("Contains external resource references (only inline allowed)")

    return {"valid": len(errors) == 0, "errors": errors}


def validate_png(png_path: str | Path, expected_size: int | None = None) -> dict:
    """Validate a PNG file."""
    png_path = Path(png_path)
    errors = []

    if not png_path.exists():
        return {"valid": False, "errors": ["File does not exist"]}

    try:
        with Image.open(png_path) as img:
            if img.format != "PNG":
                errors.append(f"Not PNG format: {img.format}")
            w, h = img.size
            if w != h:
                errors.append(f"Not square: {w}x{h}")
            if expected_size and (w != expected_size or h != expected_size):
                errors.append(f"Size mismatch, expected {expected_size}x{expected_size}: {w}x{h}")
    except Exception as e:
        errors.append(f"Failed to open image: {e}")

    return {"valid": len(errors) == 0, "errors": errors}


def validate_package(output_dir: str | Path) -> dict:
    """Validate the completeness of the entire package."""
    output_dir = Path(output_dir)
    results = {}

    # Source (in output/ structure, icon.svg and icon_1024.png are at root level)
    source_svg = output_dir / "icon.svg"
    source_png = output_dir / "icon_1024.png"
    if not source_svg.exists():
        source_svg = output_dir / "source" / "icon.svg"
    if not source_png.exists():
        source_png = output_dir / "source" / "icon_1024.png"
    results["source_svg"] = validate_svg(source_svg)
    results["source_png"] = validate_png(source_png, 1024)

    # Windows ICO + UWP tiles
    win_errors = []
    ico_path = output_dir / "windows" / "app.ico"
    if not ico_path.exists():
        win_errors.append("app.ico missing")
    for name in ICON_SIZES["windows"]["tile_sizes"]:
        tile_path = output_dir / "windows" / f"{name}.png"
        if not tile_path.exists():
            win_errors.append(f"{name}.png missing")
    results["windows"] = {"valid": len(win_errors) == 0, "errors": win_errors}

    # macOS iconset
    iconset_dir = output_dir / "macos" / "icon.iconset"
    macos_errors = []
    for _, filename in ICON_SIZES["macos"]["retina_pairs"]:
        if not (iconset_dir / filename).exists():
            macos_errors.append(f"{filename} missing")
    results["macos"] = {"valid": len(macos_errors) == 0, "errors": macos_errors}

    # Android
    android_errors = []
    for density_dir, size in ICON_SIZES["android"]["densities"].items():
        icon_file = output_dir / "android" / density_dir / ICON_SIZES["android"]["icon_filename"]
        if not icon_file.exists():
            android_errors.append(f"{density_dir}/{ICON_SIZES['android']['icon_filename']} missing")
    playstore = output_dir / "android" / "playstore-icon.png"
    if not playstore.exists():
        android_errors.append("playstore-icon.png missing")
    results["android"] = {"valid": len(android_errors) == 0, "errors": android_errors}

    # iOS
    ios_errors = []
    appiconset_dir = output_dir / "ios" / "AppIcon.appiconset"
    contents_json = appiconset_dir / "Contents.json"
    if not contents_json.exists():
        ios_errors.append("Contents.json missing")
    seen_pixels = set()
    for entry in ICON_SIZES["ios"]["contents"]:
        pixels = entry["pixels"]
        if pixels not in seen_pixels:
            icon_file = appiconset_dir / f"icon_{pixels}.png"
            if not icon_file.exists():
                ios_errors.append(f"icon_{pixels}.png missing")
            seen_pixels.add(pixels)
    results["ios"] = {"valid": len(ios_errors) == 0, "errors": ios_errors}

    # Web
    web_errors = []
    web_dir = output_dir / "web"
    web_spec = ICON_SIZES["web"]
    for size in web_spec["favicon_sizes"]:
        if not (web_dir / f"favicon-{size}.png").exists():
            web_errors.append(f"favicon-{size}.png missing")
    if not (web_dir / "favicon.ico").exists():
        web_errors.append("favicon.ico missing")
    if not (web_dir / "apple-touch-icon.png").exists():
        web_errors.append("apple-touch-icon.png missing")
    for size in web_spec["pwa_sizes"]:
        if not (web_dir / f"icon-{size}.png").exists():
            web_errors.append(f"icon-{size}.png missing")
    if not (web_dir / "og-image.png").exists():
        web_errors.append("og-image.png missing")
    if not (web_dir / "site.webmanifest").exists():
        web_errors.append("site.webmanifest missing")
    results["web"] = {"valid": len(web_errors) == 0, "errors": web_errors}

    # Overall summary
    all_valid = all(r["valid"] for r in results.values())
    return {"valid": all_valid, "platforms": results}
