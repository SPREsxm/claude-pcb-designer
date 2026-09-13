#!/usr/bin/env python3
"""Generate the repository social preview image with Pillow.

This is a maintainer utility, not part of the runtime skill. It keeps the
preview reproducible when the project name or tagline changes.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH = 1280
HEIGHT = 640
BG = "#071C18"
PANEL = "#0C2B25"
TRACE = "#1E7A5C"
TRACE_DIM = "#145743"
TEXT = "#F2F7F4"
MUTED = "#A7C8BC"
ACCENT = "#F2A65A"
BLUE = "#5BA7D1"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ),
        Path(
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
            if bold
            else "/System/Library/Fonts/Supplemental/Arial.ttf"
        ),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default(size=size)


def draw_board(draw: ImageDraw.ImageDraw) -> None:
    x0, y0, x1, y1 = 760, 110, 1175, 530
    draw.rectangle((x0, y0, x1, y1), fill=PANEL, outline=TRACE, width=5)

    traces = [
        ((800, 160), (930, 160), (970, 200), (1130, 200)),
        ((800, 245), (875, 245), (910, 280), (1080, 280), (1110, 310), (1130, 310)),
        ((800, 345), (900, 345), (940, 385), (1130, 385)),
        ((800, 445), (875, 445), (910, 410), (1040, 410), (1075, 445), (1130, 445)),
    ]
    for trace in traces:
        draw.line(trace, fill=TRACE, width=7, joint="curve")

    pads = [
        (800, 160),
        (1130, 200),
        (800, 245),
        (1130, 310),
        (800, 345),
        (1130, 385),
        (800, 445),
        (1130, 445),
    ]
    for index, (x, y) in enumerate(pads):
        color = ACCENT if index in {1, 6} else BLUE
        draw.ellipse((x - 11, y - 11, x + 11, y + 11), fill=color)
        draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=BG)

    draw.rectangle((885, 175, 960, 230), fill="#11382F", outline=TRACE_DIM, width=4)
    draw.rectangle((985, 330, 1065, 365), fill="#11382F", outline=TRACE_DIM, width=4)
    for row in range(4):
        for column in range(4):
            px = 895 + column * 16
            py = 185 + row * 10
            draw.rectangle((px, py, px + 7, py + 7), fill=ACCENT)
    for row in range(2):
        for column in range(3):
            px = 995 + column * 20
            py = 338 + row * 14
            draw.rectangle((px, py, px + 9, py + 8), fill=BLUE)


def generate(output: Path) -> None:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, WIDTH, 18), fill=ACCENT)
    draw.rectangle((0, 18, 14, HEIGHT), fill=TRACE)
    draw_board(draw)

    draw.text((72, 76), "OPEN AGENT SKILL", font=font(26, True), fill=ACCENT)
    draw.text((72, 126), "PCB", font=font(96, True), fill=TEXT)
    draw.text((72, 218), "DESIGNER", font=font(88, True), fill=TEXT)
    draw.text(
        (76, 340),
        "Design. Review. Calculate. Release.",
        font=font(38, True),
        fill=MUTED,
    )
    draw.text(
        (76, 402),
        "Deterministic tools for schematics, layout,\nDFM, fabrication packages, and bring-up.",
        font=font(28),
        fill=MUTED,
        spacing=10,
    )
    draw.rectangle((76, 510, 620, 568), fill="#11382F", outline=TRACE, width=3)
    draw.text(
        (100, 523),
        "v3.0.0   |   Codex + Claude + Agent Skills",
        font=font(25, True),
        fill=TEXT,
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, format="PNG", optimize=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default="assets/social-preview.png",
        help="output PNG path",
    )
    args = parser.parse_args()
    generate(Path(args.output))
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
