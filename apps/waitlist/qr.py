"""Counter-card QR codes for nurseries, generated with segno + Pillow.

The QR encodes the absolute /v/<slug>/ URL; the nursery name is printed
below so the PNG/SVG works as a printed counter card.
"""

import io
import xml.sax.saxutils as saxutils
from urllib.parse import urljoin

import segno

CARD_WIDTH = 480  # px of the printable PNG card


def visit_url(nursery, base_url: str) -> str:
    """Absolute URL the counter QR points to."""
    return urljoin(base_url.rstrip("/") + "/", f"v/{nursery.slug}/")


def qr_svg(nursery, base_url: str) -> str:
    """SVG counter card: QR on top, nursery name below."""
    qr = segno.make(visit_url(nursery, base_url))
    body = qr.svg_inline(omitsize=True, border=2, light="#FFFFFF")
    name = saxutils.escape(nursery.name)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 340">'
        '<rect width="300" height="340" fill="#FFFFFF" rx="12"/>'
        f'<svg x="10" y="10" width="280" height="280">{body}</svg>'
        f'<text x="150" y="326" text-anchor="middle" font-family="Figtree, sans-serif"'
        f' font-size="17" font-weight="600" fill="#1B2620">{name}</text>'
        "</svg>"
    )


def qr_png(nursery, base_url: str) -> bytes:
    """PNG counter card: QR on top, nursery name below."""
    from PIL import Image, ImageDraw, ImageFont

    qr = segno.make(visit_url(nursery, base_url))
    qr_img = io.BytesIO()
    qr.save(qr_img, kind="png", scale=12, border=2, light="#FFFFFF", dark="#1B2620")
    qr_img.seek(0)
    qr_image = Image.open(qr_img).convert("RGB")

    side = qr_image.width
    card = Image.new("RGB", (CARD_WIDTH, side + 64), "white")
    card.paste(qr_image, ((CARD_WIDTH - side) // 2, 0))

    font = ImageFont.load_default(size=26)
    draw = ImageDraw.Draw(card)
    text_w = draw.textlength(nursery.name, font=font)
    draw.text(((CARD_WIDTH - text_w) / 2, side + 22), nursery.name, fill="#1B2620", font=font)

    out = io.BytesIO()
    card.save(out, format="PNG")
    return out.getvalue()
