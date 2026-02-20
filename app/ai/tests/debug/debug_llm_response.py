"""
Debug: Print EXACT LLM response to see what's being returned
"""
import os
import json
from PIL import Image
import io
from app.llm_client import extract_text_from_pdf_bytes, generate_cv_content

input_path = "input/BAD_CV.png"

# Convert PNG to PDF
with open(input_path, "rb") as f:
    png_bytes = f.read()

img = Image.open(io.BytesIO(png_bytes))
if img.mode != 'RGB':
    img = img.convert('RGB')

pdf_buffer = io.BytesIO()
img.save(pdf_buffer, format='PDF')
pdf_bytes = pdf_buffer.getvalue()

print("="*70)
print("DEBUG: Raw LLM Response")
print("="*70)

# Extract text
print("\n[1] Extracting text from PDF...")
text = extract_text_from_pdf_bytes(pdf_bytes, filename="bad_cv.pdf")
print(f"Extracted: {len(text)} characters")

# Generate and inspect RAW response
print("\n[2] Generating CV content...")
content = generate_cv_content(
    input_data={"raw_text": text},
    domain="finance",
    language="fr",
    enrichment_mode=False,
)

print("\n[3] RAW JSON RESPONSE FROM LLM:")
print("="*70)
print(json.dumps(content, indent=2, ensure_ascii=False))
print("="*70)

print("\n[4] KEYS ANALYSIS:")
print(f"Keys in response: {list(content.keys())}")

print("\n[5] EXPERIENCE FIELDS:")
if "work_experience" in content:
    print(f"  'work_experience' key exists: {len(content['work_experience'])} entries")
    if content['work_experience']:
        print(f"  First entry: {content['work_experience'][0]}")
else:
    print(f"  'work_experience' key MISSING")

if "experience" in content:
    print(f"  'experience' key exists: {len(content['experience'])} entries")
    if content['experience']:
        print(f"  First entry: {content['experience'][0]}")
else:
    print(f"  'experience' key MISSING")

print("\n[6] DIAGNOSIS:")
if not content.get('work_experience') and not content.get('experience'):
    print("  [PROBLEM] No experience keys in LLM response")
    print("  The LLM is NOT following the prompt format")
    print("  The updated prompt constraints are being IGNORED")
elif content.get('work_experience') == [] and content.get('experience') == []:
    print("  [PROBLEM] Experience keys exist but are EMPTY []")
    print("  The LLM extracted the structure but NO experiences")
else:
    print("  [OK] Experiences found in response")
