"""OG image generation following brand book v1.0 slides 21 + 23.

Renders 1200×630 PNGs entirely with Pillow + the bundled Manrope and
JetBrains Mono variable fonts in core/static/fonts/. No external deps,
no headless browser.

The default OG (render_og_default) is for the home/marketing pages.
The per-professional OG (render_og_for_professional) is shown when
someone shares /p/{slug}.
"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont

# --- Brand tokens (subset; the rest live in DESIGN paleta de colores.md) ---
COBALT = (0, 71, 171)        # #0047AB
WHITE = (255, 255, 255)

WIDTH, HEIGHT = 1200, 630

_FONTS_DIR = Path(__file__).resolve().parent / 'static' / 'fonts'
_MANROPE_VF = _FONTS_DIR / 'Manrope-VF.ttf'
_JETBRAINS_VF = _FONTS_DIR / 'JetBrainsMono-VF.ttf'


# ---------------------------------------------------------------------------
# Font helpers
# ---------------------------------------------------------------------------

def _font(path: Path, size: int, weight: int = 500) -> ImageFont.FreeTypeFont:
    """Load a variable font and set its weight axis.

    Pillow 9.2+ supports OpenType variation axes. We swallow errors so
    that a malformed font file falls back to the default instance rather
    than crashing the OG view.
    """
    font = ImageFont.truetype(str(path), size=size)
    try:
        font.set_variation_by_axes([weight])
    except (OSError, ValueError):
        pass
    return font


def _rgba(rgb: tuple[int, int, int], alpha: float) -> tuple[int, int, int, int]:
    return (rgb[0], rgb[1], rgb[2], int(round(alpha * 255)))


# ---------------------------------------------------------------------------
# Drawing primitives
# ---------------------------------------------------------------------------

def _draw_grid(img: Image.Image, step: int = 80, alpha: float = 0.06) -> None:
    """Decorative 80px grid overlay (slide 21)."""
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    color = _rgba(WHITE, alpha)
    for x in range(0, img.width, step):
        draw.line([(x, 0), (x, img.height)], fill=color, width=1)
    for y in range(0, img.height, step):
        draw.line([(0, y), (img.width, y)], fill=color, width=1)
    img.alpha_composite(overlay)


def _draw_lockup_inverted(
    img: Image.Image, x: int, y: int, iso_size: int, text_size: int,
) -> int:
    """Inverted lockup: white outlined isotype + wordmark with white dot.

    Returns the total width drawn so callers can right-align if needed.
    """
    draw = ImageDraw.Draw(img, 'RGBA')

    # Isotype: 80-unit canvas with 68×68 outer rounded rect (8px corner, 10px
    # stroke) and a 36×8 horizontal segment at (22, 36). Everything scales.
    s = iso_size / 80
    pad = 6 * s
    stroke = max(2, int(round(10 * s)))
    rect_w = 68 * s
    draw.rounded_rectangle(
        [x + pad, y + pad, x + pad + rect_w, y + pad + rect_w],
        radius=int(round(8 * s)),
        outline=WHITE,
        width=stroke,
    )
    seg_x, seg_y = x + 22 * s, y + 36 * s
    draw.rectangle(
        [seg_x, seg_y, seg_x + 36 * s, seg_y + 8 * s], fill=WHITE,
    )

    # Wordmark
    gap = int(round(14 * s))
    font = _font(_MANROPE_VF, text_size, 600)
    word = 'consulte.'
    word_bbox = draw.textbbox((0, 0), word, font=font)
    word_h = word_bbox[3] - word_bbox[1]
    word_w = word_bbox[2] - word_bbox[0]
    text_x = x + iso_size + gap
    text_y = y + (iso_size - word_h) // 2 - word_bbox[1]
    # Tighten letter-spacing slightly to mimic -0.045em from the brand spec.
    _draw_text_with_tracking(draw, word, text_x, text_y, font, WHITE, tracking_em=-0.045)
    return iso_size + gap + word_w


def _measure_tracked(text: str, font: ImageFont.FreeTypeFont, tracking_em: float) -> int:
    if not text:
        return 0
    spacing = font.size * tracking_em
    total = 0
    for ch in text:
        bbox = font.getbbox(ch)
        total += (bbox[2] - bbox[0]) + spacing
    return int(round(total - spacing))


def _draw_text_with_tracking(
    draw: ImageDraw.ImageDraw, text: str, x: int, y: int,
    font: ImageFont.FreeTypeFont, fill, tracking_em: float = 0.0,
) -> int:
    """Draw text char by char with explicit letter-spacing."""
    spacing = font.size * tracking_em
    cursor = x
    for ch in text:
        draw.text((cursor, y), ch, font=font, fill=fill)
        bbox = font.getbbox(ch)
        cursor += (bbox[2] - bbox[0]) + spacing
    return int(round(cursor - spacing))


def _wrap_text(
    text: str, font: ImageFont.FreeTypeFont, max_width: int,
) -> list[str]:
    """Greedy word-wrap. Returns lines that fit within max_width."""
    words = text.split()
    lines: list[str] = []
    line: list[str] = []
    for word in words:
        candidate = ' '.join(line + [word])
        bbox = font.getbbox(candidate)
        if (bbox[2] - bbox[0]) <= max_width or not line:
            line.append(word)
        else:
            lines.append(' '.join(line))
            line = [word]
    if line:
        lines.append(' '.join(line))
    return lines


def _draw_multiline(
    draw: ImageDraw.ImageDraw, lines: Iterable[str], x: int, y: int,
    font: ImageFont.FreeTypeFont, fill, line_height: float,
) -> None:
    """Draws multiple lines from top-left x,y."""
    step = int(round(font.size * line_height))
    for i, line in enumerate(lines):
        draw.text((x, y + i * step), line, font=font, fill=fill)


def _initials(name: str) -> str:
    parts = [p for p in name.split() if p]
    if not parts:
        return '·'
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


# ---------------------------------------------------------------------------
# Public renderers
# ---------------------------------------------------------------------------

def render_og_default() -> bytes:
    """Brand book slide 21 — default OG, 1200×630."""
    img = Image.new('RGBA', (WIDTH, HEIGHT), COBALT + (255,))
    _draw_grid(img)
    draw = ImageDraw.Draw(img, 'RGBA')

    # Top-left lockup (iso 48 + wordmark 32, gap 14)
    _draw_lockup_inverted(img, x=64, y=48, iso_size=48, text_size=32)

    # Top-right mono meta — uppercase, tracking 0.14em, white 60%
    meta_font = _font(_JETBRAINS_VF, 13, 500)
    meta = 'CONSULTE.APP · V1.0'
    meta_w = _measure_tracked(meta, meta_font, 0.14)
    _draw_text_with_tracking(
        draw, meta, x=WIDTH - 64 - meta_w, y=64,
        font=meta_font, fill=_rgba(WHITE, 0.6), tracking_em=0.14,
    )

    # Big copy — bottom-aligned to 64px safe area, max-width 980, line-height 0.95
    headline_font = _font(_MANROPE_VF, 96, 600)
    headline_lines = _wrap_text(
        'Tu landing, tu agenda y tu alta. En una sola plataforma.',
        headline_font, max_width=980,
    )

    sub_font = _font(_MANROPE_VF, 18, 400)
    sub_text = 'Para profesionales independientes que reciben consultas.'

    cta_font = _font(_JETBRAINS_VF, 14, 500)
    cta_text = '→ EMPEZAR GRATIS'
    cta_w = _measure_tracked(cta_text, cta_font, 0.14)

    # Calculate vertical layout from the bottom up.
    bottom = HEIGHT - 64
    sub_h = sub_font.size + 4
    sub_y = bottom - sub_h
    gap_after_headline = 28
    headline_line_h = int(round(headline_font.size * 0.95))
    headline_total_h = headline_line_h * len(headline_lines)
    headline_y = sub_y - gap_after_headline - headline_total_h

    _draw_multiline(
        draw, headline_lines, x=64, y=headline_y,
        font=headline_font, fill=WHITE, line_height=0.95,
    )

    draw.text((64, sub_y), sub_text, font=sub_font, fill=_rgba(WHITE, 0.7))

    _draw_text_with_tracking(
        draw, cta_text, x=WIDTH - 64 - cta_w, y=sub_y,
        font=cta_font, fill=_rgba(WHITE, 0.7), tracking_em=0.14,
    )

    return _png(img)


def render_og_for_professional(professional) -> bytes:
    """Brand book slide 23 — per-professional OG for /p/{slug}, 1200×630.

    Layout (scaled up from the brand book preview to native 1200×630):
      - Cobalt background, decorative grid.
      - Top-right small inverted lockup.
      - Bottom-left: 160px white avatar (initials in cobalt) + eyebrow
        "{SPECIALTY}" mono uppercase + headline "Agendá con {Nombre}".
      - Bottom-right: mono "→ /p/{slug}".
    """
    img = Image.new('RGBA', (WIDTH, HEIGHT), COBALT + (255,))
    _draw_grid(img)
    draw = ImageDraw.Draw(img, 'RGBA')

    # Top-right small lockup (iso 36 + wordmark 26)
    iso_size, text_size = 36, 26
    lockup_font = _font(_MANROPE_VF, text_size, 600)
    word_bbox = draw.textbbox((0, 0), 'consulte.', font=lockup_font)
    word_w = word_bbox[2] - word_bbox[0]
    gap = 12
    lockup_w = iso_size + gap + word_w
    _draw_lockup_inverted(
        img, x=WIDTH - 64 - lockup_w, y=48,
        iso_size=iso_size, text_size=text_size,
    )

    # Bottom-left: avatar + eyebrow + headline
    avatar_size = 160
    avatar_x, avatar_y = 64, HEIGHT - 64 - avatar_size
    draw.ellipse(
        [avatar_x, avatar_y, avatar_x + avatar_size, avatar_y + avatar_size],
        fill=WHITE,
    )
    initials = _initials(professional.professional_name)
    init_font = _font(_MANROPE_VF, 64, 700)
    init_bbox = draw.textbbox((0, 0), initials, font=init_font)
    init_w = init_bbox[2] - init_bbox[0]
    init_h = init_bbox[3] - init_bbox[1]
    draw.text(
        (avatar_x + (avatar_size - init_w) // 2 - init_bbox[0],
         avatar_y + (avatar_size - init_h) // 2 - init_bbox[1]),
        initials, font=init_font, fill=COBALT,
    )

    # Text column to the right of avatar
    text_x = avatar_x + avatar_size + 28
    text_right = WIDTH - 64 - 280  # leave room for bottom-right url stamp
    text_max_w = text_right - text_x

    # Eyebrow: specialty in uppercase, mono, tracking 0.14em, white 70%
    eyebrow_font = _font(_JETBRAINS_VF, 22, 500)
    eyebrow = _truncate(
        (professional.specialty or '').upper(),
        eyebrow_font, text_max_w, tracking_em=0.14,
    )

    # Headline: "Agendá con {Nombre}"
    headline_font = _font(_MANROPE_VF, 76, 600)
    headline_text = f'Agendá con {professional.professional_name}'
    headline_lines = _wrap_text(headline_text, headline_font, max_width=text_max_w)
    # Cap to 2 lines for safety.
    if len(headline_lines) > 2:
        head = ' '.join(headline_lines[:2])
        # Truncate the second-line excess with an ellipsis.
        while _measure_tracked(head + '…', headline_font, 0) > text_max_w * 2:
            head = head[:-1]
        headline_lines = _wrap_text(head + '…', headline_font, max_width=text_max_w)[:2]

    headline_line_h = int(round(headline_font.size * 1.05))
    headline_total_h = headline_line_h * len(headline_lines)

    # Align the eyebrow-headline block to the avatar bottom.
    avatar_bottom = avatar_y + avatar_size
    headline_baseline_y = avatar_bottom - headline_total_h
    eyebrow_y = headline_baseline_y - eyebrow_font.size - 8

    _draw_text_with_tracking(
        draw, eyebrow, x=text_x, y=eyebrow_y,
        font=eyebrow_font, fill=_rgba(WHITE, 0.7), tracking_em=0.14,
    )
    _draw_multiline(
        draw, headline_lines, x=text_x, y=headline_baseline_y,
        font=headline_font, fill=WHITE, line_height=1.05,
    )

    # Bottom-right: "→ /p/{slug}" mono, tracking 0.14em, white 60%
    url_font = _font(_JETBRAINS_VF, 22, 500)
    url_text = f'→ /p/{professional.slug}'
    url_w = _measure_tracked(url_text, url_font, 0.14)
    _draw_text_with_tracking(
        draw, url_text, x=WIDTH - 64 - url_w, y=HEIGHT - 64 - url_font.size,
        font=url_font, fill=_rgba(WHITE, 0.6), tracking_em=0.14,
    )

    return _png(img)


def _truncate(
    text: str, font: ImageFont.FreeTypeFont, max_width: int, tracking_em: float = 0,
) -> str:
    if _measure_tracked(text, font, tracking_em) <= max_width:
        return text
    while text and _measure_tracked(text + '…', font, tracking_em) > max_width:
        text = text[:-1]
    return text + '…'


def _png(img: Image.Image) -> bytes:
    buf = BytesIO()
    img.convert('RGB').save(buf, format='PNG', optimize=True)
    return buf.getvalue()
