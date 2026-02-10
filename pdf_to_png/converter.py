#!/usr/bin/env python3
"""
PDF to PNG Converter

Converts PDF files to PNG images, one image per page.
Place PDF files in the 'input' folder and run this script.
PNG images will be saved to the 'output' folder.
"""

import os
from pathlib import Path
import fitz  # PyMuPDF


def get_project_dirs():
    """Get input and output directory paths."""
    script_dir = Path(__file__).parent
    input_dir = script_dir / "input"
    output_dir = script_dir / "output"
    return input_dir, output_dir


def ensure_directories_exist():
    """Create input and output directories if they don't exist."""
    input_dir, output_dir = get_project_dirs()
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    return input_dir, output_dir


def convert_pdf_to_png(pdf_path: Path, output_dir: Path, dpi: int = 200):
    """
    Convert a PDF file to PNG images (one per page).
    
    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save PNG images
        dpi: Resolution for output images (default: 200)
    """
    print(f"Converting: {pdf_path.name}")
    
    try:
        # Open PDF document
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"  ❌ Error opening {pdf_path.name}: {e}")
        return 0
    
    # Create a subdirectory for this PDF's images
    pdf_output_dir = output_dir / pdf_path.stem
    pdf_output_dir.mkdir(exist_ok=True)
    
    # Calculate zoom factor for desired DPI (default PDF is 72 DPI)
    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)
    
    # Convert each page to PNG
    page_count = 0
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Render page to image
        pix = page.get_pixmap(matrix=matrix)
        
        # Save as PNG
        output_filename = f"{pdf_path.stem}_page_{page_num + 1:03d}.png"
        output_path = pdf_output_dir / output_filename
        pix.save(output_path)
        
        print(f"  ✅ Saved: {output_filename}")
        page_count += 1
    
    doc.close()
    return page_count


def main():
    """Main function to convert all PDFs in the input folder."""
    print("=" * 50)
    print("PDF to PNG Converter")
    print("=" * 50)
    
    # Ensure directories exist
    input_dir, output_dir = ensure_directories_exist()
    
    # Find all PDF files in input directory
    pdf_files = list(input_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"\n⚠️  No PDF files found in: {input_dir}")
        print(f"   Please add PDF files to the 'input' folder and run again.")
        return
    
    print(f"\nFound {len(pdf_files)} PDF file(s)")
    print("-" * 50)
    
    total_pages = 0
    for pdf_path in pdf_files:
        pages = convert_pdf_to_png(pdf_path, output_dir)
        total_pages += pages
    
    print("-" * 50)
    print(f"\n✨ Done! Converted {len(pdf_files)} PDF(s) → {total_pages} PNG image(s)")
    print(f"   Output saved to: {output_dir}")


if __name__ == "__main__":
    main()
