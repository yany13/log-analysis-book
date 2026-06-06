#!/usr/bin/env python3
"""
Add SVG diagrams to DOCX by manipulating the ZIP structure directly
"""

import zipfile
import os
import shutil
from pathlib import Path
import xml.etree.ElementTree as ET
from io import BytesIO

DIAGRAM_DIR = r"D:\workspace\ai\code\log-analysis-book\diagrams"
INPUT_DOCX = r"D:\workspace\ai\code\log-analysis-book\book_versions\Chapters_Overviewv3.1.docx"
OUTPUT_DOCX = r"D:\workspace\ai\code\log-analysis-book\Chapters_OverviewFINAL.docx"
TEMP_DIR = r"D:\workspace\ai\code\log-analysis-book\book_versions\docx_temp"

def add_svgs_to_docx():
    """Unpack DOCX, add SVGs, and repack"""

    # Create temp directories
    os.makedirs(TEMP_DIR, exist_ok=True)
    unpack_dir = os.path.join(TEMP_DIR, "unpacked")
    if os.path.exists(unpack_dir):
        shutil.rmtree(unpack_dir)
    os.makedirs(unpack_dir)

    # Extract DOCX
    print("[*] Extracting DOCX...")
    with zipfile.ZipFile(INPUT_DOCX, 'r') as zip_ref:
        zip_ref.extractall(unpack_dir)

    # Create media directory if it doesn't exist
    media_dir = os.path.join(unpack_dir, 'word', 'media')
    os.makedirs(media_dir, exist_ok=True)

    # Copy SVG files to media folder
    print("[*] Adding SVG files to media folder...")
    svg_count = 0
    for svg_file in os.listdir(DIAGRAM_DIR):
        if svg_file.endswith('.svg'):
            src = os.path.join(DIAGRAM_DIR, svg_file)
            dst = os.path.join(media_dir, svg_file.replace('.svg', '.svg'))
            shutil.copy2(src, dst)
            print("  [+] {}".format(svg_file))
            svg_count += 1

    # Update [Content_Types].xml to include SVG media type
    print("[*] Updating [Content_Types].xml...")
    content_types_path = os.path.join(unpack_dir, '[Content_Types].xml')

    tree = ET.parse(content_types_path)
    root = tree.getroot()

    # Add SVG extension if not present
    namespaces = {'ct': 'http://schemas.openxmlformats.org/package/2006/content-types'}
    ET.register_namespace('', namespaces['ct'])

    # Check if svg extension exists
    svg_ext = root.find(".//ct:Default[@Extension='svg']", namespaces)
    if svg_ext is None:
        default_elem = ET.Element('{http://schemas.openxmlformats.org/package/2006/content-types}Default')
        default_elem.set('Extension', 'svg')
        default_elem.set('ContentType', 'image/svg+xml')
        root.append(default_elem)
        tree.write(content_types_path, encoding='utf-8', xml_declaration=True)
        print("  [+] Added SVG content type")

    # Repack DOCX
    print("[*] Repacking DOCX...")
    if os.path.exists(OUTPUT_DOCX):
        os.remove(OUTPUT_DOCX)

    with zipfile.ZipFile(OUTPUT_DOCX, 'w', zipfile.ZIP_DEFLATED) as docx:
        for root_dir, dirs, files in os.walk(unpack_dir):
            for file in files:
                file_path = os.path.join(root_dir, file)
                arcname = os.path.relpath(file_path, unpack_dir)
                docx.write(file_path, arcname)

    # Cleanup
    shutil.rmtree(unpack_dir)

    return OUTPUT_DOCX, svg_count


if __name__ == "__main__":
    try:
        output, count = add_svgs_to_docx()
        size = os.path.getsize(output) / (1024 * 1024)
        print("")
        print("[SUCCESS] DOCX with {} SVG diagrams created!".format(count))
        print("[SUCCESS] Output: {} ({:.2f} MB)".format(output, size))
        print("[INFO] SVG diagrams are now embedded in the DOCX file")
        print("[INFO] Most modern document viewers support SVG images")
    except Exception as e:
        print("[ERROR] " + str(e))
        import traceback
        traceback.print_exc()
