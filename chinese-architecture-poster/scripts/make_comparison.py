#!/usr/bin/env python3
"""Create a lossless original/poster comparison collage."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageColor


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Place a portrait pair side by side or a landscape pair top to bottom."
    )
    parser.add_argument("original", type=Path)
    parser.add_argument("poster", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--direction",
        choices=("auto", "horizontal", "vertical"),
        default="auto",
        help="auto uses horizontal for portrait originals and vertical for landscape originals",
    )
    parser.add_argument("--gap", type=int, default=24, help="gap in pixels")
    parser.add_argument("--background", default="#EDE4D2")
    return parser.parse_args()


def flatten(image: Image.Image, background: tuple[int, int, int]) -> Image.Image:
    image = image.convert("RGBA")
    canvas = Image.new("RGBA", image.size, background + (255,))
    canvas.alpha_composite(image)
    return canvas.convert("RGB")


def resize_to_height(image: Image.Image, height: int) -> Image.Image:
    width = max(1, round(image.width * height / image.height))
    return image.resize((width, height), Image.Resampling.LANCZOS)


def resize_to_width(image: Image.Image, width: int) -> Image.Image:
    height = max(1, round(image.height * width / image.width))
    return image.resize((width, height), Image.Resampling.LANCZOS)


def main() -> None:
    args = parse_args()
    if args.gap < 0:
        raise SystemExit("--gap must be non-negative")

    background = ImageColor.getrgb(args.background)
    original = flatten(Image.open(args.original), background)
    poster = flatten(Image.open(args.poster), background)

    direction = args.direction
    if direction == "auto":
        direction = "horizontal" if original.height >= original.width else "vertical"

    if direction == "horizontal":
        target_height = max(original.height, poster.height)
        original = resize_to_height(original, target_height)
        poster = resize_to_height(poster, target_height)
        canvas = Image.new(
            "RGB", (original.width + args.gap + poster.width, target_height), background
        )
        canvas.paste(original, (0, 0))
        canvas.paste(poster, (original.width + args.gap, 0))
    else:
        target_width = max(original.width, poster.width)
        original = resize_to_width(original, target_width)
        poster = resize_to_width(poster, target_width)
        canvas = Image.new(
            "RGB", (target_width, original.height + args.gap + poster.height), background
        )
        canvas.paste(original, (0, 0))
        canvas.paste(poster, (0, original.height + args.gap))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    save_options: dict[str, object] = {}
    if args.output.suffix.lower() in {".jpg", ".jpeg"}:
        save_options = {"quality": 95, "subsampling": 0}
    canvas.save(args.output, **save_options)
    print(f"saved {canvas.width}x{canvas.height} comparison to {args.output}")


if __name__ == "__main__":
    main()
