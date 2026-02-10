"""
Image Format Converter
Handles all image-to-image conversions using Pillow.
Supports: WebP↔PNG, PNG↔JPG, BMP→PNG, TIFF→PNG
"""

from pathlib import Path
from PIL import Image


def _convert_image(input_path: str, output_dir: str, target_format: str, target_ext: str, **save_kwargs) -> list:
    """
    Generic image conversion function.

    Args:
        input_path: Path to the input image file
        output_dir: Directory to save the converted image
        target_format: PIL format string (e.g., 'PNG', 'JPEG', 'WEBP')
        target_ext: File extension for output (e.g., '.png', '.jpg')
        **save_kwargs: Additional keyword arguments for PIL save

    Returns:
        List of paths to converted files
    """
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_filename = input_path.stem + target_ext
    output_path = output_dir / output_filename

    try:
        with Image.open(input_path) as img:
            # Handle transparency
            if target_format == 'JPEG':
                # JPEG doesn't support transparency, convert to RGB
                if img.mode in ('RGBA', 'LA', 'PA', 'P'):
                    # Create white background for transparent images
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    if img.mode in ('RGBA', 'LA'):
                        background.paste(img, mask=img.split()[-1])
                        img = background
                    else:
                        img = img.convert('RGB')
                else:
                    img = img.convert('RGB')
            elif target_format in ('PNG', 'WEBP'):
                # Preserve transparency if present
                if img.mode in ('RGBA', 'LA', 'PA') or (img.mode == 'P' and 'transparency' in img.info):
                    img = img.convert('RGBA')
                else:
                    img = img.convert('RGB')
            else:
                img = img.convert('RGB')

            img.save(str(output_path), target_format, **save_kwargs)

    except Exception as e:
        raise ValueError(f"Failed to convert image: {e}")

    return [str(output_path)]


def convert_webp_to_png(input_path: str, output_dir: str) -> list:
    """Convert a WebP image to PNG format."""
    return _convert_image(input_path, output_dir, 'PNG', '.png', optimize=True)


def convert_png_to_webp(input_path: str, output_dir: str) -> list:
    """Convert a PNG image to WebP format."""
    return _convert_image(input_path, output_dir, 'WEBP', '.webp', quality=90, method=6)


def convert_png_to_jpg(input_path: str, output_dir: str) -> list:
    """Convert a PNG image to JPG format."""
    return _convert_image(input_path, output_dir, 'JPEG', '.jpg', quality=95, optimize=True)


def convert_jpg_to_png(input_path: str, output_dir: str) -> list:
    """Convert a JPG image to PNG format."""
    return _convert_image(input_path, output_dir, 'PNG', '.png', optimize=True)


def convert_bmp_to_png(input_path: str, output_dir: str) -> list:
    """Convert a BMP image to PNG format."""
    return _convert_image(input_path, output_dir, 'PNG', '.png', optimize=True)


def convert_tiff_to_png(input_path: str, output_dir: str) -> list:
    """Convert a TIFF image to PNG format."""
    return _convert_image(input_path, output_dir, 'PNG', '.png', optimize=True)
