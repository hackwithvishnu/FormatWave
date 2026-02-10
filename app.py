#!/usr/bin/env python3
"""
FormatWave — File Conversion Web Application
A premium web app for converting files between formats.
"""

import os
import uuid
import shutil
import zipfile
import time
import threading
from pathlib import Path
from flask import Flask, request, jsonify, send_file, send_from_directory

from converters import CONVERTERS, CONVERSION_OPTIONS, get_accepted_extensions, get_target_extension

# ─── Configuration ───────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
CONVERTED_DIR = BASE_DIR / "converted"
STATIC_DIR = BASE_DIR / "static"

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB per file
MAX_FILES_PER_BATCH = 20
CLEANUP_AGE_SECONDS = 3600  # 1 hour

# Ensure directories exist
UPLOAD_DIR.mkdir(exist_ok=True)
CONVERTED_DIR.mkdir(exist_ok=True)

# ─── Flask App ───────────────────────────────────────────────────────────────

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE * MAX_FILES_PER_BATCH


# ─── Cleanup Thread ─────────────────────────────────────────────────────────

def cleanup_old_files():
    """Periodically remove old upload and converted files."""
    while True:
        time.sleep(600)  # Run every 10 minutes
        now = time.time()
        for directory in [UPLOAD_DIR, CONVERTED_DIR]:
            if not directory.exists():
                continue
            for item in directory.iterdir():
                try:
                    age = now - item.stat().st_mtime
                    if age > CLEANUP_AGE_SECONDS:
                        if item.is_dir():
                            shutil.rmtree(item)
                        else:
                            item.unlink()
                except Exception:
                    pass


cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
cleanup_thread.start()


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the main frontend page."""
    return send_from_directory(STATIC_DIR, "index.html")


@app.route("/api/conversions", methods=["GET"])
def get_conversions():
    """Return the list of supported conversion types."""
    return jsonify({"conversions": CONVERSION_OPTIONS})


@app.route("/api/convert", methods=["POST"])
def convert_files():
    """
    Upload and convert files.

    Expects multipart form data with:
    - conversion_id: string (e.g., "pdf-to-png")
    - files: one or more files
    """
    conversion_id = request.form.get("conversion_id", "").strip()
    if not conversion_id:
        return jsonify({"error": "Missing conversion_id parameter"}), 400

    # Parse conversion_id to get from/to formats
    parts = conversion_id.split("-to-")
    if len(parts) != 2:
        return jsonify({"error": f"Invalid conversion_id: {conversion_id}"}), 400

    from_format = parts[0].lower()
    to_format = parts[1].lower()

    # Check if converter exists
    converter = CONVERTERS.get((from_format, to_format))
    if converter is None:
        # Try alternate extensions (e.g., jpeg for jpg)
        if from_format == "jpg":
            converter = CONVERTERS.get(("jpeg", to_format))
        elif from_format == "tiff":
            converter = CONVERTERS.get(("tif", to_format))

    if converter is None:
        return jsonify({"error": f"Unsupported conversion: {from_format} → {to_format}"}), 400

    # Get uploaded files
    files = request.files.getlist("files")
    if not files or all(f.filename == "" for f in files):
        return jsonify({"error": "No files uploaded"}), 400

    if len(files) > MAX_FILES_PER_BATCH:
        return jsonify({"error": f"Too many files. Maximum {MAX_FILES_PER_BATCH} files per batch."}), 400

    # Get accepted extensions
    accepted_exts = get_accepted_extensions(conversion_id)

    # Create session directory
    session_id = str(uuid.uuid4())[:12]
    session_upload_dir = UPLOAD_DIR / session_id
    session_output_dir = CONVERTED_DIR / session_id
    session_upload_dir.mkdir(parents=True, exist_ok=True)
    session_output_dir.mkdir(parents=True, exist_ok=True)

    results = []
    errors = []

    for file in files:
        if file.filename == "":
            continue

        # Validate extension
        file_ext = Path(file.filename).suffix.lower().lstrip(".")
        if accepted_exts and file_ext not in accepted_exts:
            errors.append({
                "filename": file.filename,
                "error": f"Invalid file type '.{file_ext}'. Expected: {', '.join(accepted_exts)}"
            })
            continue

        # Save uploaded file
        safe_filename = f"{uuid.uuid4().hex[:8]}_{file.filename}"
        upload_path = session_upload_dir / safe_filename
        file.save(str(upload_path))

        # Check file size
        if upload_path.stat().st_size > MAX_FILE_SIZE:
            upload_path.unlink()
            errors.append({
                "filename": file.filename,
                "error": f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"
            })
            continue

        # Convert
        try:
            output_paths = converter(str(upload_path), str(session_output_dir))

            for output_path in output_paths:
                output_path = Path(output_path)
                file_size = output_path.stat().st_size

                # Build a clean display name from the original filename
                original_stem = Path(file.filename).stem
                display_name = output_path.name
                # Strip internal UUID prefix for user-facing name
                if "_" in output_path.stem:
                    # For PDF multi-page output, keep page numbers
                    parts = output_path.stem.split("_", 1)
                    if len(parts) > 1:
                        display_name = parts[1] + output_path.suffix
                    else:
                        display_name = original_stem + output_path.suffix

                # Check if it's an image for preview
                is_previewable = output_path.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp", ".bmp"]

                results.append({
                    "original_name": file.filename,
                    "converted_name": display_name,
                    "file_id": output_path.name,
                    "size": file_size,
                    "size_human": _human_size(file_size),
                    "previewable": is_previewable,
                    "preview_url": f"/api/preview/{session_id}/{output_path.name}" if is_previewable else None,
                    "download_url": f"/api/download/{session_id}/{output_path.name}",
                })

        except Exception as e:
            errors.append({
                "filename": file.filename,
                "error": str(e)
            })

    return jsonify({
        "session_id": session_id,
        "results": results,
        "errors": errors,
        "total_converted": len(results),
        "total_errors": len(errors),
        "download_all_url": f"/api/download-all/{session_id}" if results else None,
    })


@app.route("/api/preview/<session_id>/<filename>", methods=["GET"])
def preview_file(session_id, filename):
    """Serve a converted file for preview."""
    file_path = CONVERTED_DIR / session_id / filename
    if not file_path.exists():
        return jsonify({"error": "File not found"}), 404
    return send_file(str(file_path))


@app.route("/api/download/<session_id>/<filename>", methods=["GET"])
def download_file(session_id, filename):
    """Download a single converted file."""
    file_path = CONVERTED_DIR / session_id / filename
    if not file_path.exists():
        return jsonify({"error": "File not found"}), 404
    return send_file(str(file_path), as_attachment=True, download_name=filename)


@app.route("/api/download-all/<session_id>", methods=["GET"])
def download_all(session_id):
    """Download all converted files as a ZIP archive."""
    session_dir = CONVERTED_DIR / session_id
    if not session_dir.exists():
        return jsonify({"error": "Session not found"}), 404

    # Create ZIP file
    zip_filename = f"FormatWave_{session_id}.zip"
    zip_path = CONVERTED_DIR / zip_filename

    try:
        with zipfile.ZipFile(str(zip_path), "w", zipfile.ZIP_DEFLATED) as zf:
            for file_path in session_dir.iterdir():
                if file_path.is_file():
                    zf.write(str(file_path), file_path.name)

        return send_file(str(zip_path), as_attachment=True, download_name=zip_filename)
    except Exception as e:
        return jsonify({"error": f"Failed to create ZIP: {e}"}), 500


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _human_size(num_bytes: int) -> str:
    """Convert bytes to human-readable size string."""
    for unit in ["B", "KB", "MB", "GB"]:
        if abs(num_bytes) < 1024:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} TB"


# ─── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n🌊 FormatWave — File Conversion Web App")
    print("=" * 45)
    print(f"📂 Uploads:    {UPLOAD_DIR}")
    print(f"📂 Converted:  {CONVERTED_DIR}")
    print(f"🌐 Server:     http://localhost:5000")
    print("=" * 45 + "\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
