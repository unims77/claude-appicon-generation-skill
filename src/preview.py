"""Candidate icon preview HTML generation module."""

from pathlib import Path

from src.config import HYPER_COLORS

STYLE_LABELS = {
    "01": "Flat", "02": "Flat", "03": "Flat",
    "04": "Gradient", "05": "Gradient", "06": "Gradient",
    "07": "Outlined", "08": "Outlined",
    "09": "Bold", "10": "Bold",
    "11": "Emoji", "12": "Emoji",
}


def generate_preview(output_dir: str | Path, app_name: str = "") -> Path:
    """Generate preview.html with inline-embedded SVGs from the candidates/ folder."""
    output_dir = Path(output_dir)
    candidates_dir = output_dir / "candidates"
    svg_files = sorted(candidates_dir.glob("*.svg"))

    if not svg_files:
        raise FileNotFoundError(f"No SVG files found: {candidates_dir}")

    title = f"{app_name} Icon Candidates" if app_name else "Icon Candidates"
    count = len(svg_files)

    cards_html = ""
    for svg in svg_files:
        num = svg.stem
        svg_content = svg.read_text(encoding="utf-8")
        label = STYLE_LABELS.get(num, "")
        badge_class = label.lower() if label else "flat"
        cards_html += f"""      <div class="card" data-num="{num}">
        <div class="icon">{svg_content}</div>
        <div class="info">
          <span class="num">#{num}</span>
          <span class="badge {badge_class}">{label}</span>
        </div>
      </div>
"""

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    :root {{
      --bg: #0f0f1a;
      --card: #1a1a2e;
      --card-hover: #22223a;
      --border: rgba(255,255,255,0.06);
      --accent: #6c63ff;
      --text: #e0e0e0;
      --text-dim: #888;
      --shadow: rgba(0,0,0,0.5);
    }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
    }}

    /* Header */
    .header {{
      text-align: center;
      padding: 3rem 2rem 1rem;
    }}
    .header h1 {{
      font-size: 1.6rem;
      font-weight: 600;
      letter-spacing: -0.02em;
      color: var(--text);
    }}
    .header p {{
      margin-top: 0.4rem;
      font-size: 0.85rem;
      color: var(--text-dim);
    }}

    /* Grid */
    .grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1.25rem;
      max-width: 1100px;
      margin: 0 auto;
      padding: 1.5rem 2rem 4rem;
    }}
    @media (max-width: 900px) {{
      .grid {{ grid-template-columns: repeat(3, 1fr); }}
    }}
    @media (max-width: 600px) {{
      .grid {{ grid-template-columns: repeat(2, 1fr); }}
    }}

    /* Card */
    .card {{
      position: relative;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 0.75rem;
      cursor: pointer;
      transition: transform 0.25s cubic-bezier(0.4,0,0.2,1),
                  box-shadow 0.25s cubic-bezier(0.4,0,0.2,1),
                  border-color 0.25s;
    }}
    .card:hover {{
      transform: translateY(-6px) scale(1.02);
      box-shadow: 0 16px 40px var(--shadow);
      border-color: rgba(108,99,255,0.3);
      background: var(--card-hover);
    }}
    .card.selected {{
      border-color: var(--accent);
      box-shadow: 0 0 0 2px var(--accent), 0 16px 40px var(--shadow);
    }}
    .card.selected::after {{
      content: '';
      position: absolute;
      top: 10px;
      right: 10px;
      width: 24px;
      height: 24px;
      background: var(--accent);
      border-radius: 50%;
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3E%3Cpath d='M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z'/%3E%3C/svg%3E");
      background-size: 16px;
      background-repeat: no-repeat;
      background-position: center;
    }}

    /* Icon */
    .icon {{
      background: #111;
      border-radius: 14px;
      overflow: hidden;
      aspect-ratio: 1;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .icon svg {{
      width: 100%;
      height: 100%;
      display: block;
    }}

    /* Info */
    .info {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: 0.6rem;
      padding: 0 0.25rem;
    }}
    .num {{
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--text);
    }}
    .badge {{
      font-size: 0.65rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 0.15rem 0.5rem;
      border-radius: 6px;
      color: #fff;
    }}
    .badge.flat       {{ background: #2d7d46; }}
    .badge.gradient   {{ background: #1976d2; }}
    .badge.outlined   {{ background: #7b1fa2; }}
    .badge.bold       {{ background: #d32f2f; }}
    .badge.emoji      {{ background: #f57c00; }}
  </style>
</head>
<body>
  <div class="header">
    <h1>{title}</h1>
    <p>{count} variants &middot; click to select</p>
  </div>
  <div class="grid">
{cards_html}  </div>
  <script>
    document.querySelectorAll('.card').forEach(card => {{
      card.addEventListener('click', () => {{
        document.querySelectorAll('.card').forEach(c => c.classList.remove('selected'));
        card.classList.toggle('selected');
      }});
    }});
  </script>
</body>
</html>"""

    preview_path = output_dir / "preview.html"
    preview_path.write_text(html, encoding="utf-8")
    return preview_path


# ── Hyper mode preview ──────────────────────────────────────────────────

_GROUP_LABELS = {
    "A": "Theme A", "B": "Theme B", "C": "Theme C",
    "D": "Theme D", "E": "Theme E",
    "F": "Emoji 1", "G": "Emoji 2",
}


def generate_hyper_preview(
    output_dir: str | Path,
    app_name: str = "",
    concepts: dict[str, str] | None = None,
) -> Path:
    """Generate a hyper mode preview HTML.

    Args:
        output_dir: Output directory (requires variants/ subdirectory structure)
        app_name: Application name
        concepts: Concept names per group {"A": "Lightning Bolt", ...}
    """
    output_dir = Path(output_dir)
    variants_dir = output_dir / "variants"
    concepts = concepts or {}

    if not variants_dir.exists():
        raise FileNotFoundError(f"Variants directory not found: {variants_dir}")

    title = f"{app_name} Hyper Preview" if app_name else "Hyper Icon Preview"

    color_keys = list(HYPER_COLORS.keys())
    color_names = [HYPER_COLORS[k]["name"] for k in color_keys]

    sections_html = ""
    total_count = 0
    seq_num = 0

    for group_dir in sorted(variants_dir.iterdir()):
        if not group_dir.is_dir():
            continue
        base_name = group_dir.name
        group_letter = base_name[0].upper()
        group_label = _GROUP_LABELS.get(group_letter, group_letter)
        concept_name = concepts.get(group_letter, "")
        section_title = f"{group_label}: {concept_name}" if concept_name else group_label

        flat_cards = ""
        grad_cards = ""
        for color_key, color_name in zip(color_keys, color_names):
            for style, container in [("flat", "flat_cards"), ("grad", "grad_cards")]:
                svg_file = group_dir / f"{style}_{color_key}.svg"
                if not svg_file.exists():
                    continue
                svg_content = svg_file.read_text(encoding="utf-8")
                seq_num += 1
                variant_id = f"{base_name}_{style}_{color_key}"
                card = f"""        <div class="card-sm" data-id="{variant_id}" data-num="{seq_num}">
          <div class="icon-sm">{svg_content}</div>
          <div class="variant-num">#{seq_num}</div>
          <div class="info-sm">
            <span class="color-dot" style="background:{HYPER_COLORS[color_key]['hex']}"></span>
            <span class="label-sm">{color_name}</span>
          </div>
        </div>
"""
                if style == "flat":
                    flat_cards += card
                else:
                    grad_cards += card
                total_count += 1

        sections_html += f"""    <div class="section">
      <h2 class="section-title">{section_title} <span class="design-id">{base_name}</span></h2>
      <h3 class="style-label">Flat</h3>
      <div class="color-grid">{flat_cards}</div>
      <h3 class="style-label">Gradient</h3>
      <div class="color-grid">{grad_cards}</div>
    </div>
"""

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    :root {{
      --bg: #0f0f1a; --card: #1a1a2e; --card-hover: #22223a;
      --border: rgba(255,255,255,0.06); --accent: #6c63ff;
      --text: #e0e0e0; --text-dim: #888; --shadow: rgba(0,0,0,0.5);
    }}
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{ font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; background:var(--bg); color:var(--text); }}
    .header {{ text-align:center; padding:2rem 2rem 0.5rem; }}
    .header h1 {{ font-size:1.6rem; font-weight:600; }}
    .header p {{ font-size:0.85rem; color:var(--text-dim); margin-top:0.3rem; }}
    .section {{ max-width:1400px; margin:0 auto; padding:1rem 2rem; }}
    .section-title {{ font-size:1.2rem; font-weight:700; margin:1.5rem 0 0.3rem; border-bottom:1px solid var(--border); padding-bottom:0.4rem; }}
    .design-id {{ font-size:0.75rem; color:var(--text-dim); font-weight:400; }}
    .style-label {{ font-size:0.8rem; color:var(--accent); margin:0.6rem 0 0.3rem; text-transform:uppercase; letter-spacing:0.05em; }}
    .color-grid {{ display:grid; grid-template-columns:repeat(10,1fr); gap:0.5rem; margin-bottom:0.5rem; }}
    @media(max-width:1200px){{ .color-grid {{ grid-template-columns:repeat(5,1fr); }} }}
    @media(max-width:600px){{ .color-grid {{ grid-template-columns:repeat(3,1fr); }} }}
    .card-sm {{ background:var(--card); border:1px solid var(--border); border-radius:12px; padding:0.4rem; cursor:pointer; transition:transform 0.2s,border-color 0.2s; }}
    .card-sm:hover {{ transform:translateY(-3px); border-color:rgba(108,99,255,0.3); background:var(--card-hover); }}
    .card-sm.selected {{ border-color:var(--accent); box-shadow:0 0 0 2px var(--accent); }}
    .icon-sm {{ background:#111; border-radius:8px; overflow:hidden; aspect-ratio:1; display:flex; align-items:center; justify-content:center; }}
    .icon-sm svg {{ width:100%; height:100%; display:block; }}
    .variant-num {{ font-size:0.7rem; font-weight:800; color:var(--accent); margin-top:0.25rem; text-align:center; }}
    .info-sm {{ display:flex; align-items:center; gap:0.25rem; margin-top:0.15rem; padding:0 0.1rem; }}
    .color-dot {{ width:8px; height:8px; border-radius:50%; flex-shrink:0; }}
    .label-sm {{ font-size:0.55rem; color:var(--text-dim); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
  </style>
</head>
<body>
  <div class="header">
    <h1>{title}</h1>
    <p>{total_count} variants &middot; 7 directions &times; 10 colors &times; 2 styles</p>
  </div>
{sections_html}
  <script>
    document.querySelectorAll('.card-sm').forEach(c => {{
      c.addEventListener('click', () => c.classList.toggle('selected'));
    }});
  </script>
</body>
</html>"""

    preview_path = output_dir / "preview.html"
    preview_path.write_text(html, encoding="utf-8")
    return preview_path
