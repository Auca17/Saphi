"""Generate the PWA icons committed under static/icons/.

Draws the Saphi leaf mark (same path as the prototype's i-leaf symbol) on a
forest tile. Run once when the brand changes:

    uv run python scripts/generate_pwa_icons.py
"""

from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent.parent / "static" / "icons"

FOREST = (31, 74, 52, 255)  # --forest
PAPER = (244, 248, 243, 255)  # --forest-ink

# i-leaf outline: two cubic segments, from prototype/saphi-prototype.html.
LEAF_SEGMENTS = [
    ((5, 19.5), (5, 11), (10, 5), (19.5, 4.5)),
    ((19.5, 4.5), (19.5, 14), (14, 19), (5, 19.5)),
]
VEIN = ((5, 19.5), (13.5, 11))
VIEWBOX = 24.0


def cubic(p0, p1, p2, p3, t):
    mt = 1 - t
    return (
        mt**3 * p0[0] + 3 * mt * mt * t * p1[0] + 3 * mt * t * t * p2[0] + t**3 * p3[0],
        mt**3 * p0[1] + 3 * mt * mt * t * p1[1] + 3 * mt * t * t * p2[1] + t**3 * p3[1],
    )


def leaf_polygon(steps=48):
    points = []
    for seg in LEAF_SEGMENTS:
        points += [cubic(*seg, i / steps) for i in range(steps)]
    points.append(LEAF_SEGMENTS[-1][3])
    return points


def render(size, leaf_scale, rounded=False):
    ss = 4  # supersample for smooth edges
    img = Image.new("RGBA", (size * ss, size * ss), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    radius = size * ss * (0.22 if rounded else 0)
    draw.rounded_rectangle([0, 0, size * ss, size * ss], radius=radius, fill=FOREST)

    margin = (size * ss) * (1 - leaf_scale) / 2
    span = size * ss * leaf_scale

    def pt(x, y):
        return (margin + x / VIEWBOX * span, margin + y / VIEWBOX * span)

    draw.polygon([pt(x, y) for x, y in leaf_polygon()], fill=PAPER)
    draw.line([pt(*VEIN[0]), pt(*VEIN[1])], fill=FOREST, width=max(2, int(size * ss * 0.012)))

    return img.resize((size, size), Image.LANCZOS)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    render(192, leaf_scale=0.72, rounded=True).save(OUT / "icon-192.png")
    render(512, leaf_scale=0.72, rounded=True).save(OUT / "icon-512.png")
    # Maskable: full-bleed square, mark inside the 80% safe zone.
    render(512, leaf_scale=0.58, rounded=False).save(OUT / "icon-maskable-512.png")
    for path in sorted(OUT.iterdir()):
        print(f"wrote {path.name} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
