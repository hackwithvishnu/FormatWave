#!/usr/bin/env python3
"""
WebP to PNG Converter
A simple and efficient tool to convert WebP images to PNG format.
"""

import os
import sys
import argparse
from pathlib import Path
from PIL import Image


def convert_webp_to_png(input_path: str, output_path: str = None, quality: int = 100) -> str:
    """
    Convert a WebP image to PNG format.
    
    Args:
        input_path: Path to the input WebP file
        output_path: Path for the output PNG file (optional)
        quality: Quality of the output PNG (1-100, default: 100)
    
    Returns:
        Path to the converted PNG file
    
    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If input file is not a valid WebP image
    """
    input_path = Path(input_path)
    
    # Validate input file exists
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Validate input file is a WebP
    if input_path.suffix.lower() != '.webp':
        raise ValueError(f"Input file must be a WebP image: {input_path}")
    
    # Generate output path if not provided
    if output_path is None:
        output_path = input_path.with_suffix('.png')
    else:
        output_path = Path(output_path)
    
    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Open and convert the image
    try:
        with Image.open(input_path) as img:
            # Convert to RGBA if the image has transparency, otherwise RGB
            if img.mode in ('RGBA', 'LA', 'PA') or (img.mode == 'P' and 'transparency' in img.info):
                img = img.convert('RGBA')
            else:
                img = img.convert('RGB')
            
            # Save as PNG
            img.save(output_path, 'PNG', optimize=True)
            
    except Exception as e:
        raise ValueError(f"Failed to convert image: {e}")
    
    return str(output_path)


def convert_directory(input_dir: str, output_dir: str = None, recursive: bool = False) -> list:
    """
    Convert all WebP images in a directory to PNG format.
    
    Args:
        input_dir: Path to the input directory
        output_dir: Path to the output directory (optional)
        recursive: Whether to search subdirectories recursively
    
    Returns:
        List of paths to converted PNG files
    """
    input_dir = Path(input_dir)
    
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input path is not a directory: {input_dir}")
    
    # Find all WebP files
    if recursive:
        webp_files = list(input_dir.rglob('*.webp'))
    else:
        webp_files = list(input_dir.glob('*.webp'))
    
    if not webp_files:
        print(f"No WebP files found in: {input_dir}")
        return []
    
    converted_files = []
    
    for webp_file in webp_files:
        try:
            # Calculate output path
            if output_dir:
                output_dir_path = Path(output_dir)
                relative_path = webp_file.relative_to(input_dir)
                output_path = output_dir_path / relative_path.with_suffix('.png')
            else:
                output_path = webp_file.with_suffix('.png')
            
            result = convert_webp_to_png(str(webp_file), str(output_path))
            converted_files.append(result)
            print(f"✓ Converted: {webp_file.name} → {Path(result).name}")
            
        except Exception as e:
            print(f"✗ Failed to convert {webp_file.name}: {e}")
    
    return converted_files


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Convert WebP images to PNG format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python app.py image.webp                    Convert single file
  python app.py image.webp output.png         Convert with custom output name
  python app.py --dir ./images                Convert all WebP files in directory
  python app.py --dir ./images -r             Convert recursively in subdirectories
  python app.py --dir ./input -o ./output     Convert to a different output directory
        """
    )
    
    parser.add_argument(
        'input',
        nargs='?',
        help='Input WebP file path'
    )
    
    parser.add_argument(
        'output',
        nargs='?',
        help='Output PNG file path (optional)'
    )
    
    parser.add_argument(
        '--dir', '-d',
        dest='directory',
        help='Convert all WebP files in a directory'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        dest='output_dir',
        help='Output directory for converted files'
    )
    
    parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        help='Search subdirectories recursively (used with --dir)'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='WebP to PNG Converter v1.0.0'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.input and not args.directory:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.directory:
            # Directory mode
            print(f"\n🔄 Converting WebP files in: {args.directory}")
            print("-" * 50)
            
            converted = convert_directory(
                args.directory,
                args.output_dir,
                args.recursive
            )
            
            print("-" * 50)
            print(f"✅ Successfully converted {len(converted)} file(s)\n")
            
        else:
            # Single file mode
            print(f"\n🔄 Converting: {args.input}")
            result = convert_webp_to_png(args.input, args.output)
            print(f"✅ Saved to: {result}\n")
            
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)
    except ValueError as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
        sys.exit(1)


if __name__ == '__main__':
    main()
