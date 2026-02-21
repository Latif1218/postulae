"""
Batch CV processing for Postulae.
Processes all PDFs from Input/ directory.

TWO MODES:
1. Standard mode: Generate BOTH FR and EN at once
2. Two-phase mode (SaaS optimized): Generate FR first (fast), then EN (deferred)

Set TWO_PHASE_MODE = True to use optimized two-phase generation.
"""

import os
import time
from pathlib import Path
from app import generate_cv_from_pdf, generate_cv_phase1_from_pdf, generate_cv_phase2_from_pdf

# Set to True for SaaS-optimized two-phase generation (FR first, EN deferred)
# Set to False for standard generation (both languages at once)
TWO_PHASE_MODE = True


def sanitize_message(text):
    """Remove or replace Unicode characters for Windows console compatibility."""
    # Replace common Unicode box-drawing characters with ASCII equivalents
    replacements = {
        '━': '=',
        '─': '-',
        '│': '|',
        '┌': '+',
        '┐': '+',
        '└': '+',
        '┘': '+',
        '├': '+',
        '┤': '+',
        '┬': '+',
        '┴': '+',
        '┼': '+',
    }

    for unicode_char, ascii_char in replacements.items():
        text = text.replace(unicode_char, ascii_char)

    # Fallback: encode to ASCII, replacing unknown characters
    try:
        text = text.encode('ascii', errors='replace').decode('ascii')
    except Exception:
        pass

    return text


def main():
    input_dir = "Input"
    output_dir = "Output"

    os.makedirs(output_dir, exist_ok=True)

    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]

    if not pdf_files:
        print("No PDF files found in Input/ directory.")
        return

    print(f"\nMode: {'TWO-PHASE (FR first, EN deferred)' if TWO_PHASE_MODE else 'STANDARD (both languages at once)'}")

    for pdf_file in pdf_files:
        input_path = os.path.join(input_dir, pdf_file)
        input_base = Path(pdf_file).stem

        print(f"\n{'='*60}")
        print(f"Processing: {pdf_file}")
        print(f"{'='*60}")

        try:
            with open(input_path, "rb") as f:
                pdf_bytes = f.read()

            if TWO_PHASE_MODE:
                # TWO-PHASE GENERATION (SaaS optimized)
                # PHASE 1: FR only (fast, show to user immediately)
                print("\n[PHASE 1] Generating FR (fast, synchronous)...")
                phase1_start = time.time()
                phase1_results = generate_cv_phase1_from_pdf(
                    pdf_bytes=pdf_bytes,
                    domain="finance"
                )
                phase1_time = time.time() - phase1_start

                # Save FR immediately
                result_fr = phase1_results["fr"]
                output_pdf_fr = os.path.join(output_dir, f"output_{input_base}_fr.pdf")
                output_docx_fr = os.path.join(output_dir, f"output_{input_base}_fr.docx")

                print(f"\n[FR] (completed in {phase1_time:.1f}s)")
                print(f"page_count: {result_fr.page_count}")
                print(f"fill_percentage: {result_fr.fill_percentage}")
                print(f"char_count: {result_fr.char_count}")

                if result_fr.warnings:
                    print("warnings:")
                    for warning in result_fr.warnings:
                        print(f"  - {sanitize_message(warning)}")

                with open(output_pdf_fr, "wb") as f:
                    f.write(result_fr.pdf_bytes)

                with open(output_docx_fr, "wb") as f:
                    f.write(result_fr.docx_bytes)

                print(f"Files saved:")
                print(f"  - {output_pdf_fr}")
                print(f"  - {output_docx_fr}")

                # PHASE 2: EN (deferred, can be async in production)
                print("\n[PHASE 2] Generating EN (deferred, can be async)...")
                phase2_start = time.time()
                phase2_results = generate_cv_phase2_from_pdf(
                    pdf_bytes=pdf_bytes,
                    domain="finance"
                )
                phase2_time = time.time() - phase2_start

                # Save EN
                result_en = phase2_results["en"]
                output_pdf_en = os.path.join(output_dir, f"output_{input_base}_en.pdf")
                output_docx_en = os.path.join(output_dir, f"output_{input_base}_en.docx")

                print(f"\n[EN] (completed in {phase2_time:.1f}s)")
                print(f"page_count: {result_en.page_count}")
                print(f"fill_percentage: {result_en.fill_percentage}")
                print(f"char_count: {result_en.char_count}")

                if result_en.warnings:
                    print("warnings:")
                    for warning in result_en.warnings:
                        print(f"  - {sanitize_message(warning)}")

                with open(output_pdf_en, "wb") as f:
                    f.write(result_en.pdf_bytes)

                with open(output_docx_en, "wb") as f:
                    f.write(result_en.docx_bytes)

                print(f"Files saved:")
                print(f"  - {output_pdf_en}")
                print(f"  - {output_docx_en}")

                print(f"\nTotal time: {phase1_time + phase2_time:.1f}s (Phase 1: {phase1_time:.1f}s, Phase 2: {phase2_time:.1f}s)")
                print(f"User perceived wait: {phase1_time:.1f}s (Phase 1 only)")

            else:
                # STANDARD GENERATION (both languages at once)
                print("\n[STANDARD] Generating both FR and EN...")
                start_time = time.time()
                results = generate_cv_from_pdf(
                    pdf_bytes=pdf_bytes,
                    domain="finance"
                )
                total_time = time.time() - start_time

                # Process both languages
                for lang in ["fr", "en"]:
                    result = results[lang]

                    output_pdf = os.path.join(output_dir, f"output_{input_base}_{lang}.pdf")
                    output_docx = os.path.join(output_dir, f"output_{input_base}_{lang}.docx")

                    print(f"\n[{lang.upper()}]")
                    print(f"page_count: {result.page_count}")
                    print(f"fill_percentage: {result.fill_percentage}")
                    print(f"char_count: {result.char_count}")

                    if result.warnings:
                        print("warnings:")
                        for warning in result.warnings:
                            print(f"  - {sanitize_message(warning)}")

                    with open(output_pdf, "wb") as f:
                        f.write(result.pdf_bytes)

                    with open(output_docx, "wb") as f:
                        f.write(result.docx_bytes)

                    print(f"Files saved:")
                    print(f"  - {output_pdf}")
                    print(f"  - {output_docx}")

                print(f"\nTotal time: {total_time:.1f}s")

        except Exception as e:
            error_message = sanitize_message(str(e))
            print(f"ERROR processing {pdf_file}:")
            print(f"  {error_message}")
            continue

    print(f"\n{'='*60}")
    print("Batch processing completed.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
