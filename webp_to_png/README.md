# 🖼️ WebP to PNG Converter

A simple and efficient Python tool to convert WebP images to PNG format. Supports single file conversion, batch processing, and recursive directory scanning.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## ✨ Features

- **Single File Conversion** - Convert individual WebP files to PNG
- **Batch Processing** - Convert all WebP files in a directory
- **Recursive Scanning** - Process subdirectories recursively
- **Transparency Support** - Preserves alpha channel for transparent images
- **Custom Output Paths** - Specify custom output file names and directories
- **CLI Interface** - Easy-to-use command line interface

---

## 📋 Requirements

- Python 3.7 or higher
- Pillow library

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/webptppng.git
cd webptppng
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📖 Usage

### Convert a Single File

```bash
# Basic conversion (output will be same name with .png extension)
python app.py image.webp

# Specify custom output filename
python app.py image.webp output.png
```

### Convert All Files in a Directory

```bash
# Convert all WebP files in a directory
python app.py --dir ./images

# Convert with custom output directory
python app.py --dir ./input -o ./output

# Convert recursively (including subdirectories)
python app.py --dir ./images -r
```

### Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `input` | - | Input WebP file path |
| `output` | - | Output PNG file path (optional) |
| `--dir` | `-d` | Convert all WebP files in a directory |
| `--output-dir` | `-o` | Output directory for converted files |
| `--recursive` | `-r` | Search subdirectories recursively |
| `--version` | `-v` | Show version number |
| `--help` | `-h` | Show help message |

---

## 💻 Programmatic Usage

You can also use the converter as a Python module:

```python
from app import convert_webp_to_png, convert_directory

# Convert single file
output_path = convert_webp_to_png('image.webp', 'output.png')
print(f"Converted to: {output_path}")

# Convert directory
converted_files = convert_directory('./images', './output', recursive=True)
print(f"Converted {len(converted_files)} files")
```

---

## 📁 Project Structure

```
webptppng/
├── app.py              # Main application
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── venv/               # Virtual environment (after setup)
```

---

## 🔧 API Reference

### `convert_webp_to_png(input_path, output_path=None, quality=100)`

Convert a single WebP image to PNG format.

**Parameters:**
- `input_path` (str): Path to the input WebP file
- `output_path` (str, optional): Path for the output PNG file
- `quality` (int): Quality of the output PNG (1-100, default: 100)

**Returns:** Path to the converted PNG file

---

### `convert_directory(input_dir, output_dir=None, recursive=False)`

Convert all WebP images in a directory.

**Parameters:**
- `input_dir` (str): Path to the input directory
- `output_dir` (str, optional): Path to the output directory
- `recursive` (bool): Whether to search subdirectories recursively

**Returns:** List of paths to converted PNG files

---

## 📝 Examples

### Example 1: Basic Conversion

```bash
$ python app.py photo.webp

🔄 Converting: photo.webp
✅ Saved to: photo.png
```

### Example 2: Batch Conversion

```bash
$ python app.py --dir ./webp_images

🔄 Converting WebP files in: ./webp_images
--------------------------------------------------
✓ Converted: image1.webp → image1.png
✓ Converted: image2.webp → image2.png
✓ Converted: image3.webp → image3.png
--------------------------------------------------
✅ Successfully converted 3 file(s)
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Pillow](https://pillow.readthedocs.io/) - The friendly PIL fork for image processing
- Python community for amazing tools and libraries

---

<p align="center">Made with ❤️ by You</p>
