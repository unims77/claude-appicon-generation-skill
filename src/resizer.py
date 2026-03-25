"""PNG resize module - high-quality Pillow LANCZOS resizing."""

from pathlib import Path

from PIL import Image


def resize_png(source_png: str | Path, output_path: str | Path, target_size: int) -> Path:
    """Resize a PNG to a square of target_size."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(source_png) as img:
        resized = img.resize((target_size, target_size), Image.LANCZOS)
        resized.save(str(output_path), "PNG")
    return output_path


def generate_platform_sizes(
    source_png: str | Path,
    platform: str,
    output_dir: str | Path,
) -> list[Path]:
    """Generate all sizes for a given platform."""
    from src.config import ICON_SIZES

    source_png = Path(source_png)
    output_dir = Path(output_dir)
    results = []

    spec = ICON_SIZES[platform]

    if platform == "windows":
        for size in spec["sizes"]:
            out = output_dir / f"icon_{size}.png"
            resize_png(source_png, out, size)
            results.append(out)

    elif platform == "macos":
        iconset_dir = output_dir / spec["output_dir"]
        iconset_dir.mkdir(parents=True, exist_ok=True)
        for pixel_size, filename in spec["retina_pairs"]:
            out = iconset_dir / filename
            resize_png(source_png, out, pixel_size)
            results.append(out)

    elif platform == "android":
        for density_dir, size in spec["densities"].items():
            out = output_dir / density_dir / spec["icon_filename"]
            resize_png(source_png, out, size)
            results.append(out)
        # Play Store icon
        out = output_dir / "playstore-icon.png"
        resize_png(source_png, out, spec["playstore_size"])
        results.append(out)

    elif platform == "ios":
        appiconset_dir = output_dir / "AppIcon.appiconset"
        appiconset_dir.mkdir(parents=True, exist_ok=True)
        seen_pixels = set()
        for entry in spec["contents"]:
            pixels = entry["pixels"]
            filename = f"icon_{pixels}.png"
            if pixels not in seen_pixels:
                out = appiconset_dir / filename
                resize_png(source_png, out, pixels)
                results.append(out)
                seen_pixels.add(pixels)

    elif platform == "web":
        web_dir = output_dir
        web_dir.mkdir(parents=True, exist_ok=True)
        for size in spec["favicon_sizes"]:
            out = web_dir / f"favicon-{size}.png"
            resize_png(source_png, out, size)
            results.append(out)
        # Apple Touch Icon
        out = web_dir / "apple-touch-icon.png"
        resize_png(source_png, out, spec["apple_touch_size"])
        results.append(out)
        # PWA icons
        for size in spec["pwa_sizes"]:
            out = web_dir / f"icon-{size}.png"
            resize_png(source_png, out, size)
            results.append(out)

    return results
