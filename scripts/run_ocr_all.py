#!/usr/bin/env python3
"""
Master extraction script for BCB annual reports 1981-1989.
Runs OCR on all PDFs and saves results.
"""

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import json
import os
import sys
from pathlib import Path

BASE_DIR = "/home/navi/projects/proyectomacro"
PDF_DIR = f"{BASE_DIR}/raw_data/memorias"
OCR_DIR = f"{BASE_DIR}/data/ocr"

os.makedirs(OCR_DIR, exist_ok=True)

YEARS = list(range(1981, 1990))

def extract_pdf_text_ocr(pdf_path, year, lang="spa+eng", dpi=200):
    """Extract text from a scanned PDF using OCR page by page."""
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    results = []
    
    print(f"\n[{year}] Processing {os.path.basename(pdf_path)}: {total_pages} pages", flush=True)
    
    for page_num in range(total_pages):
        page = doc[page_num]
        # Render page as image
        mat = fitz.Matrix(dpi/72, dpi/72)
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csGRAY)
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        
        # OCR
        text = pytesseract.image_to_string(img, lang=lang, config='--psm 6 --oem 3')
        results.append({
            "page": page_num + 1,
            "text": text
        })
        
        if (page_num + 1) % 20 == 0:
            print(f"  [{year}] Page {page_num+1}/{total_pages}", flush=True)
    
    doc.close()
    print(f"  [{year}] Done!", flush=True)
    return results


def process_year(year):
    pdf_path = f"{PDF_DIR}/MemoriaBCB_{year}.pdf"
    output_path = f"{OCR_DIR}/bcb_{year}_ocr.json"
    
    if os.path.exists(output_path):
        print(f"[{year}] Already processed, skipping.", flush=True)
        return True
    
    if not os.path.exists(pdf_path):
        print(f"[{year}] PDF not found: {pdf_path}", flush=True)
        return False
    
    try:
        results = extract_pdf_text_ocr(pdf_path, year)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"[{year}] Saved to {output_path}", flush=True)
        return True
    except Exception as e:
        print(f"[{year}] ERROR: {e}", flush=True)
        return False


if __name__ == "__main__":
    # Process specific year if provided
    if len(sys.argv) > 1:
        year = int(sys.argv[1])
        process_year(year)
    else:
        for year in YEARS:
            process_year(year)
