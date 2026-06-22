#!/usr/bin/env python3
"""
Analysis script for BCB annual reports.
Searches OCR text for fiscal data: ingresos, egresos, deficit/superavit,
deuda interna del sector publico no financiero.
"""

import json
import re
import os
import sys

# Keywords to search
KEYWORDS = [
    "ingresos", "egresos", "egreso", "ingreso",
    "deficit", "déficit", "superavit", "superávit",
    "deuda interna", "sector publico no financiero",
    "financiamiento", "gasto", "recaudacion",
    "corriente", "capital", "resultado"
]

TABLE_KEYWORDS = [
    "millones", "miles", "bolivianos", "pesos",
    "total", "subtotal"
]

def search_relevant_pages(ocr_data, year):
    """Find pages with relevant fiscal data."""
    relevant = []
    for page_data in ocr_data:
        page_num = page_data["page"]
        text = page_data["text"].lower()
        
        score = 0
        matched = []
        for kw in KEYWORDS:
            if kw in text:
                score += 1
                matched.append(kw)
        
        if score >= 2:
            relevant.append({
                "year": year,
                "page": page_num,
                "score": score,
                "keywords": matched,
                "text": page_data["text"]
            })
    
    return sorted(relevant, key=lambda x: x["score"], reverse=True)


def extract_numbers_from_text(text):
    """Extract numeric values from text."""
    # Match numbers like 1,234.56 or 1.234,56 or 1234
    patterns = [
        r'[\d]{1,3}(?:[,\.\s]\d{3})*(?:[,\.]\d+)?',
    ]
    numbers = []
    for pat in patterns:
        matches = re.findall(pat, text)
        for m in matches:
            # Clean and try to parse
            clean = m.replace(' ', '').replace(',', '')
            try:
                val = float(clean)
                if val > 0:
                    numbers.append(val)
            except:
                pass
    return numbers


def analyze_year(json_path, year):
    """Analyze OCR data for a specific year."""
    with open(json_path, 'r', encoding='utf-8') as f:
        ocr_data = json.load(f)
    
    print(f"\n{'='*60}")
    print(f"YEAR: {year}")
    print(f"Total pages: {len(ocr_data)}")
    
    relevant = search_relevant_pages(ocr_data, year)
    print(f"Relevant pages found: {len(relevant)}")
    
    # Show top pages
    for page_info in relevant[:20]:
        print(f"\n  Page {page_info['page']} (score={page_info['score']}, kw={page_info['keywords'][:5]})")
        # Show snippet
        text = page_info['text']
        lines = text.split('\n')
        for line in lines[:30]:
            if any(kw in line.lower() for kw in KEYWORDS + TABLE_KEYWORDS):
                print(f"    > {line.strip()}")
    
    return relevant


if __name__ == "__main__":
    base_dir = "/home/navi/projects/proyectomacro/data/ocr"
    
    for year in range(1981, 1990):
        json_path = os.path.join(base_dir, f"bcb_{year}_ocr.json")
        if os.path.exists(json_path):
            analyze_year(json_path, year)
        else:
            print(f"Missing OCR data for {year}: {json_path}")
