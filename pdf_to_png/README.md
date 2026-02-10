# PDF to PNG Converter

A simple Python tool that converts PDF files to PNG images, one image per page.

## Installation

Install Python dependency:
```bash
pip install -r requirements.txt
```

Or directly:
```bash
pip install PyMuPDF
```

## Usage

1. Place your PDF files in the `input` folder
2. Run the converter:
```bash
python converter.py
```
3. Find your PNG images in the `output` folder

## Folder Structure

```
pdf_to_png/
├── converter.py      # Main script
├── requirements.txt  # Python dependencies
├── README.md         # This file
├── input/            # Place PDF files here
└── output/           # PNG images saved here
    └── <pdf_name>/   # Each PDF gets its own subfolder
        ├── <pdf_name>_page_001.png
        ├── <pdf_name>_page_002.png
        └── ...
```

## Example

If you have `document.pdf` with 3 pages:

**Input:** `input/document.pdf`

**Output:**
```
output/document/
├── document_page_001.png
├── document_page_002.png
└── document_page_003.png
```
