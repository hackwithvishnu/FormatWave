"""
FormatWave Converters
Registry of all supported file format conversions.
"""

from converters.pdf_converter import convert_pdf_to_png
from converters.image_converter import (
    convert_webp_to_png,
    convert_png_to_webp,
    convert_png_to_jpg,
    convert_jpg_to_png,
    convert_bmp_to_png,
    convert_tiff_to_png,
)

# Registry: maps (from_format, to_format) -> converter function
# Each converter function signature: (input_path: str, output_dir: str) -> list[str]
CONVERTERS = {
    ("pdf", "png"): convert_pdf_to_png,
    ("webp", "png"): convert_webp_to_png,
    ("png", "webp"): convert_png_to_webp,
    ("png", "jpg"): convert_png_to_jpg,
    ("jpg", "png"): convert_jpg_to_png,
    ("jpeg", "png"): convert_jpg_to_png,
    ("bmp", "png"): convert_bmp_to_png,
    ("tiff", "png"): convert_tiff_to_png,
    ("tif", "png"): convert_tiff_to_png,
}

# Human-readable conversion options for the frontend
CONVERSION_OPTIONS = [
    {"id": "pdf-to-png", "from": "PDF", "to": "PNG", "from_ext": ["pdf"], "to_ext": "png", "icon": "📄", "description": "Convert PDF pages to PNG images"},
    {"id": "webp-to-png", "from": "WebP", "to": "PNG", "from_ext": ["webp"], "to_ext": "png", "icon": "🖼️", "description": "Convert WebP images to PNG format"},
    {"id": "png-to-webp", "from": "PNG", "to": "WebP", "from_ext": ["png"], "to_ext": "webp", "icon": "🔄", "description": "Convert PNG images to WebP format"},
    {"id": "png-to-jpg", "from": "PNG", "to": "JPG", "from_ext": ["png"], "to_ext": "jpg", "icon": "🎨", "description": "Convert PNG images to JPG format"},
    {"id": "jpg-to-png", "from": "JPG", "to": "PNG", "from_ext": ["jpg", "jpeg"], "to_ext": "png", "icon": "✨", "description": "Convert JPG images to PNG format"},
    {"id": "bmp-to-png", "from": "BMP", "to": "PNG", "from_ext": ["bmp"], "to_ext": "png", "icon": "🗺️", "description": "Convert BMP images to PNG format"},
    {"id": "tiff-to-png", "from": "TIFF", "to": "PNG", "from_ext": ["tiff", "tif"], "to_ext": "png", "icon": "📷", "description": "Convert TIFF images to PNG format"},
]


def get_converter(from_format: str, to_format: str):
    """Get the converter function for a given format pair."""
    key = (from_format.lower(), to_format.lower())
    return CONVERTERS.get(key)


def get_accepted_extensions(conversion_id: str) -> list:
    """Get accepted file extensions for a conversion type."""
    for option in CONVERSION_OPTIONS:
        if option["id"] == conversion_id:
            return option["from_ext"]
    return []


def get_target_extension(conversion_id: str) -> str:
    """Get the target file extension for a conversion type."""
    for option in CONVERSION_OPTIONS:
        if option["id"] == conversion_id:
            return option["to_ext"]
    return ""
