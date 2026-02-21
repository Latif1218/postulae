"""
Debug Financial Analyst CV generation
"""
import os
from app.llm_client import extract_text_from_pdf_bytes, generate_cv_content
from app.density import DensityCalculator
from app.layout import LayoutEngine

input_path = "input/Financial-Analyst-CV-Sample.pdf"

with open(input_path, "rb") as f:
    pdf_bytes = f.read()

print("="*70)
print("DEBUG: Financial Analyst CV")
print("="*70)

# Step 1: Extract text
print("\n[1] Extracting text from PDF...")
text = extract_text_from_pdf_bytes(pdf_bytes, filename="financial.pdf")
print(f"Extracted: {len(text)} characters")
print("\nFirst 1500 characters:")
print("-"*70)
print(text[:1500])
print("-"*70)

# Step 2: Generate FR content
print("\n[2] Generating FR content...")
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
    print(f"\nExperiences:")
    for i, exp in enumerate(content_fr['experience']):
        title = exp.get('title', 'N/A')
        company = exp.get('company', 'N/A')
        bullets = exp.get('bullets', [])
        print(f"  [{i+1}] {title} @ {company}")
        print(f"      Bullets: {len(bullets)}")
        for b in bullets[:3]:
            print(f"        - {b[:70]}...")

# Step 3: Measure PFR
print("\n[3] Measuring FR PFR...")
layout = LayoutEngine()
density = DensityCalculator()

pdf_fr = layout.generate_pdf_from_data(content_fr, trim=False)
metrics_fr = density.calculate_pfr(pdf_fr)

print(f"  PFR: {metrics_fr.fill_percentage}%")
print(f"  Pages: {metrics_fr.page_count}")
print(f"  Characters: {metrics_fr.char_count}")
print(f"  Blocked: {metrics_fr.fill_percentage < 65}")

# Step 4: Generate EN content
print("\n[4] Generating EN content...")
content_en = generate_cv_content(
    input_data={"raw_text": text},
    domain="finance",
    language="en",
    enrichment_mode=False,
)

print(f"\nEN Content structure:")
print(f"  Name: {content_en.get('name', 'N/A')}")
print(f"  Experiences: {len(content_en.get('experience', []))}")
print(f"  Education: {len(content_en.get('education', []))}")

if content_en.get('experience'):
    print(f"\nExperiences:")
    for i, exp in enumerate(content_en['experience']):
        title = exp.get('title', 'N/A')
        company = exp.get('company', 'N/A')
        bullets = exp.get('bullets', [])
        print(f"  [{i+1}] {title} @ {company}")
        print(f"      Bullets: {len(bullets)}")

# Step 5: Measure EN PFR
print("\n[5] Measuring EN PFR...")
pdf_en = layout.generate_pdf_from_data(content_en, trim=False)
metrics_en = density.calculate_pfr(pdf_en)

print(f"  PFR: {metrics_en.fill_percentage}%")
print(f"  Pages: {metrics_en.page_count}")
print(f"  Characters: {metrics_en.char_count}")
print(f"  Blocked: {metrics_en.fill_percentage < 65}")

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)
print(f"FR: {metrics_fr.fill_percentage}% PFR - {'BLOCKED' if metrics_fr.fill_percentage < 65 else 'OK'}")
print(f"EN: {metrics_en.fill_percentage}% PFR - {'BLOCKED' if metrics_en.fill_percentage < 65 else 'OK'}")
print(f"\nThe issue is that the LLM-generated content is too sparse.")
print(f"Need to improve base content generation quality.")
