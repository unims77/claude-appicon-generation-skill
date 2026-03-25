"""Platform-specific icon packaging module."""

import json
from pathlib import Path

from PIL import Image

from src.config import ICON_SIZES
from src.resizer import generate_platform_sizes


def package_windows(source_png: str | Path, output_dir: str | Path) -> Path:
    """Generate a Windows ICO file + UWP tile PNGs."""
    source_png = Path(source_png)
    output_dir = Path(output_dir)
    win_dir = output_dir / "windows"
    win_dir.mkdir(parents=True, exist_ok=True)

    spec = ICON_SIZES["windows"]
    ico_path = win_dir / spec["output_file"]

    with Image.open(source_png) as img:
        # ICO (multi-size)
        icon_images = []
        for size in spec["sizes"]:
            resized = img.resize((size, size), Image.LANCZOS)
            icon_images.append(resized)

        icon_images[0].save(
            str(ico_path),
            format="ICO",
            sizes=[(s, s) for s in spec["sizes"]],
            append_images=icon_images[1:],
        )

        # UWP tile PNGs
        for name, size in spec["tile_sizes"].items():
            tile_path = win_dir / f"{name}.png"
            resized = img.resize((size, size), Image.LANCZOS)
            resized.save(str(tile_path), "PNG")

    return win_dir


def package_macos(source_png: str | Path, output_dir: str | Path) -> Path:
    """Generate a macOS .iconset folder. (ICNS conversion not available on Windows)"""
    output_dir = Path(output_dir)
    macos_dir = output_dir / "macos"
    generate_platform_sizes(source_png, "macos", macos_dir)
    return macos_dir / ICON_SIZES["macos"]["output_dir"]


def package_android(source_png: str | Path, output_dir: str | Path) -> Path:
    """Generate the Android mipmap directory structure."""
    output_dir = Path(output_dir)
    android_dir = output_dir / "android"
    generate_platform_sizes(source_png, "android", android_dir)
    return android_dir


def package_ios(source_png: str | Path, output_dir: str | Path) -> Path:
    """Generate iOS AppIcon.appiconset + Contents.json."""
    output_dir = Path(output_dir)
    ios_dir = output_dir / "ios"
    generate_platform_sizes(source_png, "ios", ios_dir)

    # Generate Contents.json
    spec = ICON_SIZES["ios"]
    appiconset_dir = ios_dir / "AppIcon.appiconset"
    appiconset_dir.mkdir(parents=True, exist_ok=True)

    images = []
    for entry in spec["contents"]:
        pixels = entry["pixels"]
        images.append({
            "filename": f"icon_{pixels}.png",
            "idiom": "universal",
            "platform": _ios_platform(entry["size"]),
            "scale": entry["scale"],
            "size": entry["size"],
        })

    contents = {
        "images": images,
        "info": {"author": "appicon-generator", "version": 1},
    }

    contents_path = appiconset_dir / "Contents.json"
    contents_path.write_text(json.dumps(contents, indent=2, ensure_ascii=False), encoding="utf-8")
    return appiconset_dir


def _ios_platform(size_str: str) -> str:
    """Infer the platform from an iOS size string."""
    size_val = float(size_str.split("x")[0])
    if size_val == 1024:
        return "ios"
    if size_val in (76, 83.5):
        return "ios"  # iPad
    return "ios"


def package_web(source_png: str | Path, output_dir: str | Path) -> Path:
    """Generate web favicon, PWA icons, and OG image."""
    source_png = Path(source_png)
    output_dir = Path(output_dir)
    web_dir = output_dir / "web"
    web_dir.mkdir(parents=True, exist_ok=True)

    spec = ICON_SIZES["web"]

    # favicon PNG + apple-touch + PWA icons
    generate_platform_sizes(source_png, "web", web_dir)

    # favicon.ico (multi-size)
    with Image.open(source_png) as img:
        ico_images = []
        for size in spec["favicon_ico_sizes"]:
            ico_images.append(img.resize((size, size), Image.LANCZOS))
        ico_images[0].save(
            str(web_dir / "favicon.ico"),
            format="ICO",
            sizes=[(s, s) for s in spec["favicon_ico_sizes"]],
            append_images=ico_images[1:],
        )

    # OG image (1200x630, icon centered)
    og_w, og_h = spec["og_size"]["width"], spec["og_size"]["height"]
    icon_size = spec["og_icon_size"]
    with Image.open(source_png) as img:
        # Extract background color from upper center (corners may be transparent)
        bg_color = img.getpixel((img.width // 2, img.height // 4))
        if isinstance(bg_color, tuple) and len(bg_color) == 4:
            bg_color = bg_color[:3]
        canvas = Image.new("RGB", (og_w, og_h), bg_color)
        icon = img.resize((icon_size, icon_size), Image.LANCZOS)
        x = (og_w - icon_size) // 2
        y = (og_h - icon_size) // 2
        if icon.mode == "RGBA":
            canvas.paste(icon, (x, y), icon)
        else:
            canvas.paste(icon, (x, y))
        canvas.save(str(web_dir / "og-image.png"), "PNG")

    # site.webmanifest
    manifest = {
        "name": "",
        "short_name": "",
        "icons": [
            {"src": f"icon-{s}.png", "sizes": f"{s}x{s}", "type": "image/png"}
            for s in spec["pwa_sizes"]
        ],
        "theme_color": "#ffffff",
        "background_color": "#ffffff",
        "display": "standalone",
    }
    manifest_path = web_dir / "site.webmanifest"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    return web_dir


def package_all(source_png: str | Path, output_dir: str | Path) -> dict[str, Path]:
    """Package for all platforms."""
    results = {
        "windows": package_windows(source_png, output_dir),
        "macos": package_macos(source_png, output_dir),
        "android": package_android(source_png, output_dir),
        "ios": package_ios(source_png, output_dir),
        "web": package_web(source_png, output_dir),
    }
    return results
