#!/usr/bin/env python3
"""
OCR extraction script for BCB annual reports (Memorias BCB 1981-1989).
Extracts text from scanned PDFs using PyMuPDF + Tesseract.
"""

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import sys
import os
import json

def extract_pdf_text_ocr(pdf_path, lang="spa", dpi=200, start_page=0, end_page=None):
    """Extract text from a scanned PDF using OCR."""
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    if end_page is None:
        end_page = total_pages
    
    results = []
    print(f"Processing {os.path.basename(pdf_path)}: {total_pages} pages total, processing {start_page}-{end_page}", flush=True)
    
    for page_num in range(start_page, min(end_page, total_pages)):
        page = doc[page_num]
        # Render at specified DPI
        mat = fitz.Matrix(dpi/72, dpi/72)
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csGRAY)
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        
        # OCR with tesseract
        text = pytesseract.image_to_string(img, lang=lang, config='--psm 6')
        results.append({
            "page": page_num + 1,
            "text": text
        })
        if (page_num - start_page + 1) % 10 == 0:
            print(f"  Processed page {page_num + 1}/{total_pages}", flush=True)
    
    doc.close()
    return results


def save_results(results, output_path):
    """Save OCR results to JSON."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Saved to {output_path}", flush=True)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ocr_extract.py <pdf_path> <output_json>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_path = sys.argv[2]
    
    results = extract_pdf_text_ocr(pdf_path)
    save_results(results, output_path)
    print("Done!")
