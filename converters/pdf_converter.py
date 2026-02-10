"""
PDF to PNG Converter
Converts PDF files to PNG images, one image per page.
Refactored from the original pdf_to_png/converter.py for web usage.
"""

import os
from pathlib import Path
import fitz  # PyMuPDF


def convert_pdf_to_png(input_path: str, output_dir: str, dpi: int = 200) -> list:
    """
    Convert a PDF file to PNG images (one per page).

    Args:
        input_path: Path to the input PDF file
        output_dir: Directory to save PNG images
        dpi: Resolution for output images (default: 200)

    Returns:
        List of paths to converted PNG files
    """
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    converted_files = []

    try:
        doc = fitz.open(input_path)
    except Exception as e:
        raise ValueError(f"Failed to open PDF: {e}")

    # Calculate zoom factor for desired DPI (default PDF is 72 DPI)
    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)

    try:
        for page_num in range(len(doc)):
            page = doc[page_num]

            # Render page to image
            pix = page.get_pixmap(matrix=matrix)

            # Save as PNG
            output_filename = f"{input_path.stem}_page_{page_num + 1:03d}.png"
            output_path = output_dir / output_filename
            pix.save(str(output_path))

            converted_files.append(str(output_path))
    finally:
        doc.close()

    return converted_files
