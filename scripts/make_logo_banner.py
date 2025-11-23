#!/usr/bin/env python3
"""
make_logo_banner.py

Create a 4:1 banner image from a logo image file using Pillow (PIL).

Usage:
    python scripts/make_logo_banner.py -i logo_small.jpg

This script will:
 - Read the input logo image
 - Create a new image with a 4:1 aspect ratio (width = 4 * logo_height)
 - Use a black background
 - Place the logo on the left area (resizing it to fit if needed)
 - Add the two-line text `topology in` / `condensed matter` in white on the right side, centered vertically
 - Save the output image

The script tries to use a commonly available TrueType font (DejaVu), falling back
to Pillow's default font if no TTF is found.
"""

from __future__ import annotations

import argparse
import os
from typing import Optional, Tuple

from PIL import Image, ImageDraw, ImageFont


def find_font(preferred: Tuple[str, ...] = None) -> Optional[str]:
    """Try to find a TrueType font installed on the system.

    Returns the TTF path if found, otherwise None.
    """
    if preferred is None:
        # Prefer non-bold fonts (thinner letters) where available
        preferred = (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        )

    for p in preferred:
        if os.path.exists(p):
            return p
    return None


def create_banner(
    input_path: str,
    output_path: str,
    text: str = "topology in\ncondensed matter",
    background_color: Tuple[int, int, int] = (0, 0, 0),
    text_color: Tuple[int, int, int] = (255, 255, 255),
    padding_ratio: float = 0.06,
    left_area_fraction: float = 1.0 / 4.0,
    font_path: Optional[str] = None,
    logo_height_ratio: float = 0.8,
):
    """Builds and saves the banner image.

    The result will have width = 4 * logo_height and the same height as the logo.
    The logo is scaled to fill a fraction of the banner height (default 80%).
    """
    logo = Image.open(input_path).convert("RGBA")
    logo_width, logo_height = logo.size

    # Output size: width = 4 * height, same height as logo
    out_height = logo_height
    out_width = int(out_height * 4)

    # Basic geometry
    padding = max(6, int(out_height * padding_ratio))
    desired_left_area_width = int(out_width * left_area_fraction)

    # Scale logo to a fraction of banner height (logo_height_ratio)
    new_logo_height = max(1, int(out_height * logo_height_ratio))
    scale_h = new_logo_height / logo_height if logo_height > 0 else 1
    new_logo_width = int(logo_width * scale_h)

    # Ensure left area is large enough to host the logo with padding.
    left_area_width = max(desired_left_area_width, new_logo_width + 2 * padding)
    # compute text area based on left_area_width; may be zero or negative if logo is very large
    text_area_x0 = left_area_width + padding
    text_area_x1 = out_width - padding
    text_area_width = max(0, text_area_x1 - text_area_x0)
    text_area_height = out_height - 2 * padding

    # Create background
    banner = Image.new("RGB", (out_width, out_height), color=background_color)

    # Resize logo to fill the calculated height (new_logo_height <= out_height)
    logo = logo.resize((new_logo_width, new_logo_height), Image.LANCZOS)
    logo_width, logo_height = logo.size

    # Place logo left and vertically centered within the banner (no vertical padding; fill the height when possible)
    x_logo = padding
    y_logo = int((out_height - logo_height) / 2)
    # Composite with alpha if present
    if logo.mode in ("RGBA", "LA"):
        banner.paste(logo, (x_logo, y_logo), logo)
    else:
        banner.paste(logo, (x_logo, y_logo))

    # Prepare to draw text
    draw = ImageDraw.Draw(banner)

    # If the text area width is zero or negative, skip text drawing
    if text_area_width <= 0 or not text.strip():
        # Save output immediately without text
        out_dir = os.path.dirname(output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        ext = os.path.splitext(output_path)[1].lower()
        if ext in (".jpg", ".jpeg"):
            banner = banner.convert("RGB")
            banner.save(output_path, format="JPEG", quality=95)
        else:
            banner.save(output_path, format="PNG")
        return output_path

    # Find font
    if font_path is None:
        font_path = find_font()

    if font_path:
        # initial font size estimate: give each line a portion of the text area
        # Use a slightly larger initial size and more vertical spacing for a bold-looking presence
        n_lines = max(1, len(text.splitlines()))
        initial_line_factor = 1.05  # fewer lines -> larger font
        enlarge_factor = 1.15  # bump initial size a bit
        font_size = max(
            8,
            int(
                enlarge_factor
                * text_area_height
                / max(1, n_lines * initial_line_factor)
            ),
        )
        font = ImageFont.truetype(font_path, font_size)
    else:
        # Fallback to default pillow font if no truetype available
        font = ImageFont.load_default()
        # The default font has a tiny size; we'll not change it.
        font_size = None

    # Compute final font size that fits horizontally and vertically
    # For multiline text, use multiline_textbbox and per-line spacing
    # splitlines used earlier for font size estimate if necessary
    if isinstance(font, ImageFont.FreeTypeFont):
        while True:
            # larger spacing between lines (thinner letters look better with more space)
            spacing = max(2, int(font_size * 0.32))
            text_bbox = draw.multiline_textbbox(
                (0, 0), text, font=font, spacing=spacing
            )
            text_w = text_bbox[2] - text_bbox[0]
            text_h = text_bbox[3] - text_bbox[1]
            if (text_w <= text_area_width) and (text_h <= text_area_height):
                break
            font_size -= 2
            if font_size <= 6:
                # give up and use the smallest font
                break
            font = ImageFont.truetype(font_path, font_size)
        spacing = max(2, int(font_size * 0.32))
        text_bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]
    else:
        spacing = 4
        text_bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]

    # Compute position to center text in the right area
    x_text = text_area_x0 + (text_area_width - text_w) // 2
    y_text = padding + (text_area_height - text_h) // 2

    # Render multiline text - white by default, each line centered
    draw.multiline_text(
        (x_text, y_text),
        text,
        fill=text_color,
        font=font,
        spacing=spacing,
        align="center",
    )

    # Save output
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    # Choose format based on extension
    ext = os.path.splitext(output_path)[1].lower()
    format = None
    if ext in (".jpg", ".jpeg"):
        format = "JPEG"
        # convert to RGB if needed
        banner = banner.convert("RGB")
        banner.save(output_path, format=format, quality=95)
    else:
        # Save with PNG as default
        format = "PNG"
        banner.save(output_path, format=format)

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a 4:1 banner from a logo image"
    )
    parser.add_argument(
        "-i", "--input", default="logo_small.jpg", help="Input logo image path"
    )
    parser.add_argument(
        "-t",
        "--text",
        default="topology in\ncondensed matter",
        help="Text to render on the right",
    )
    parser.add_argument(
        "--font", default=None, help="Path to a .ttf font to use for the text"
    )
    parser.add_argument(
        "--logo-height-ratio",
        type=float,
        default=0.8,
        help="Fraction of banner height to fill with logo (0-1)",
    )
    args = parser.parse_args()

    # Fixed output filename: per request, don't change the output filename
    fixed_output = "logo_banner.png"
    out_path = create_banner(
        args.input,
        fixed_output,
        text=args.text,
        font_path=args.font,
        logo_height_ratio=args.logo_height_ratio,
    )
    print(f"Wrote banner to: {out_path}")


if __name__ == "__main__":
    main()
