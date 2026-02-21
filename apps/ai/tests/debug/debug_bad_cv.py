"""
Debug BAD_CV.png generation
"""
import os
from PIL import Image
import io
from app.llm_client import extract_text_from_pdf_bytes, generate_cv_content
from app.density import DensityCalculator
from app.layout import LayoutEngine

input_path = "input/BAD_CV.png"

# Load and convert PNG to PDF
with open(input_path, "rb") as f:
    png_bytes = f.read()

print("="*70)
print("DEBUG: BAD_CV.png")
print("="*70)

print(f"\n[1] Converting PNG to PDF...")
img = Image.open(io.BytesIO(png_bytes))
if img.mode != 'RGB':
    img = img.convert('RGB')

pdf_buffer = io.BytesIO()
img.save(pdf_buffer, format='PDF')
pdf_bytes = pdf_buffer.getvalue()

print(f"PNG: {len(png_bytes)} bytes -> PDF: {len(pdf_bytes)} bytes")

# Extract text
print("\n[2] Extracting text from PDF...")
text = extract_text_from_pdf_bytes(pdf_bytes, filename="bad_cv.pdf")
print(f"Extracted: {len(text)} characters")

print("\nExtracted text preview (first 2000 chars):")
print("-"*70)
print(text[:2000])
print("-"*70)

# Generate FR content
print("\n[3] Generating FR content...")
content_fr = generate_cv_content(
    input_data={"raw_text": text},
    domain="finance",
    language="fr",
    enrichment_mode=False,
)

print(f"\nFR Content structure:")
print(f"  Name: {content_fr.get('name', 'N/A')}")
print(f"  Email: {content_fr.get('email', 'N/A')}")
print(f"  Phone: {content_fr.get('phone', 'N/A')}")
print(f"  Experiences: {len(content_fr.get('experience', []))}")
print(f"  Education: {len(content_fr.get('education', []))}")
print(f"  Skills: {len(content_fr.get('it_skills', []))}")
print(f"  Languages: {len(content_fr.get('languages', []))}")

if content_fr.get('experience'):
    print(f"\nExperiences details:")
    for i, exp in enumerate(content_fr['experience']):
        title = exp.get('title', 'N/A')
        company = exp.get('company', 'N/A')
        location = exp.get('location', 'N/A')
        date_range = exp.get('date_range', 'N/A')
        bullets = exp.get('bullets', [])
        print(f"\n  [{i+1}] {title}")
        print(f"      Company: {company}")
        print(f"      Location: {location}")
        print(f"      Date: {date_range}")
        print(f"      Bullets: {len(bullets)}")
        for j, b in enumerate(bullets):
            print(f"        {j+1}. {b}")
else:
    print("\n  [!] NO EXPERIENCES GENERATED")

if content_fr.get('education'):
    print(f"\nEducation details:")
    for i, edu in enumerate(content_fr['education']):
        degree = edu.get('degree', 'N/A')
        school = edu.get('school', 'N/A')
        print(f"  [{i+1}] {degree} - {school}")

# Measure PFR
print("\n[4] Measuring FR PFR...")
layout = LayoutEngine()
density = DensityCalculator()

pdf_fr = layout.generate_pdf_from_data(content_fr, trim=False)
metrics_fr = density.calculate_pfr(pdf_fr)

print(f"  PFR: {metrics_fr.fill_percentage}%")
print(f"  Pages: {metrics_fr.page_count}")
print(f"  Characters: {metrics_fr.char_count}")

print("\n" + "="*70)
print("DIAGNOSIS")
print("="*70)

if metrics_fr.fill_percentage < 65:
    print(f"[BLOCKED] PFR {metrics_fr.fill_percentage}% < 65% minimum")
    print(f"\nReasons for low PFR:")
    if len(content_fr.get('experience', [])) == 0:
        print("  - 0 experiences generated (CRITICAL)")
    elif len(content_fr.get('experience', [])) < 3:
        print(f"  - Only {len(content_fr.get('experience', []))} experiences (need 3-4)")

    total_bullets = sum(len(exp.get('bullets', [])) for exp in content_fr.get('experience', []))
    if total_bullets < 10:
        print(f"  - Only {total_bullets} total bullets (need 12-15)")

    print(f"\nThis is a LLM content generation quality issue, not a hardening issue.")
    print(f"The hardening is working correctly by blocking insufficient content.")
else:
    print(f"[OK] PFR {metrics_fr.fill_percentage}% >= 65% minimum")
