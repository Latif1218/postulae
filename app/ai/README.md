# Postulae CV Generator - Core Module

**Production-ready CV generation engine for elite one-page CVs.**

Optimized for finance, consulting, and selective roles with exact layout control and intelligent density optimization.

---

## 📋 Product Philosophy

Postulae produces **elite CVs** for competitive roles. A Postulae CV must:

- ✅ Be **exactly ONE page**
- ✅ Be **sober** (no design, colors, or icons)
- ✅ Be **dense but readable**
- ✅ Target **85-90% Page Fill Rate (PFR)**
- ✅ **NEVER** be delivered below 80% PFR

The generator is not just a rewriter—it's an **optimizer of density, structure, and impact**.

---

## 🏗️ Architecture

Clean, modular, production-ready structure:

```
/app
  ├── generator.py        # Main CV generation pipeline (orchestrator)
  ├── enrichment.py       # Intelligent content expansion
  ├── density.py          # Page Fill Rate (PFR) calculation
  ├── llm_client.py       # All LLM interactions (OpenAI GPT)
  ├── layout.py           # HTML template rendering & exact layout preservation
  ├── models.py           # Internal data models (Pydantic)
  ├── prompts/            # LLM prompt templates (.txt files)
  │   ├── base_system.txt
  │   ├── enrich_content.txt
  │   └── extract_from_pdf.txt
  └── templates/
      └── grid_template.html  # EXACT layout template (DO NOT MODIFY)
```

### Key Design Principles

- **Stateless**: No file persistence, no cloud storage, no logs
- **Pure functions**: Input → CV bytes (PDF + DOCX)
- **Separation of concerns**: Each module has one clear responsibility
- **Layout preservation**: The template encodes the "Fayed Hanafi" reference layout—**NEVER modify layout rules**

---

## 🚀 Usage

### Installation

```bash
pip install -r requirements.txt
```

Set your OpenAI API key in `.env`:

```
OPENAI_API_KEY=your_key_here
```

### Basic Usage

#### Generate CV from PDF

```python
from app import generate_cv_from_pdf

# Read PDF
with open("input_resume.pdf", "rb") as f:
    pdf_bytes = f.read()

# Generate CV
results = generate_cv_from_pdf(
    pdf_bytes=pdf_bytes,
    domain="finance",  # or "consulting", "startup", "government"
    languages=["en", "fr"]  # Output languages
)

# Save results
with open("output_cv.pdf", "wb") as f:
    f.write(results["en"].pdf_bytes)

with open("output_cv.docx", "wb") as f:
    f.write(results["en"].docx_bytes)

# Check metrics
print(f"Page Fill Rate: {results['en'].fill_percentage}%")
print(f"Character Count: {results['en'].char_count}")
```

#### Generate CV from Structured Data

```python
from app import generate_cv_from_data, CVContent
from app.models import ContactInformation, EducationEntry, WorkExperienceEntry

# Build structured data
cv_data = CVContent(
    contact_information=[ContactInformation(
        name="John Doe",
        email="john.doe@example.com",
        phone="+33 6 12 34 56 78",
        address="Paris, France"
    )],
    education=[EducationEntry(
        date="2019-2023",
        institution="HEC Paris",
        location="Paris, France",
        degree="Master in Management",
        major="Finance",
        honors="Dean's List",
        coursework=["Corporate Finance", "Financial Markets", "Valuation"]
    )],
    work_experience=[WorkExperienceEntry(
        date="Jan 2023-Jul 2023",
        company="Bain & Company",
        location="Paris, France",
        position="Associate Consultant Intern",
        duration="6 months",
        bullets=[
            "Conducted strategic benchmarks on European market trends",
            "Analyzed profitability of international expansion (+3 pts EBIT margin)",
            "Presented findings to VP Strategy, driving key business decisions"
        ]
    )],
    languages=["French (native)", "English (fluent)", "Spanish (intermediate)"],
    it_skills=["Excel", "PowerPoint", "Python", "Tableau"],
    domain="finance"
)

# Generate
results = generate_cv_from_data(cv_data, languages=["en"])
```

---

## 📊 Generation Pipeline

The generator follows this workflow:

1. **Input Processing**
   - Extract text from PDF (if PDF input) using GPT-4 Vision
   - Parse structured data (if data input)

2. **Base CV Generation**
   - Generate structured content via LLM
   - Apply domain-specific formatting (finance/consulting/startup/government)

3. **Page Fill Rate Measurement**
   - Render to PDF
   - Calculate PFR (vertical text coverage %)
   - Count characters

4. **Intelligent Optimization**
   - **If PFR < 85%**: Enrich content (expand bullets, add detail)
   - **If PFR > 90% or overflow**: Trim content (reduce bullets, remove entries)
   - **Iterate** until optimal density (85-90%)

5. **Final Generation**
   - Generate final PDF with exact layout
   - Convert PDF → DOCX (preserves layout)
   - Validate quality constraints

6. **Output**
   - Return PDF bytes, DOCX bytes, metrics, warnings

---

## ⚙️ Configuration

### Supported Domains

- `finance`: Finance/banking roles (quantitative, metrics-focused)
- `consulting`: Strategy consulting (impact-driven, project-focused)
- `startup`: Startup/tech roles (growth-oriented, versatile)
- `government`: Government/public sector (French-optimized)

### Supported Languages

- `en`: English
- `fr`: French

### Quality Constraints

| Metric | Target | Critical Threshold |
|--------|--------|-------------------|
| Page Count | **1** | Must be 1 |
| Page Fill Rate | **85-90%** | Minimum 80% |
| Character Count | **2200+** | Minimum 2000 |

---

## 🎯 Layout Preservation

**CRITICAL**: The HTML template in `app/templates/grid_template.html` contains **exact layout rules** tuned to match the "Fayed Hanafi" reference CV.

### Layout Constraints (DO NOT MODIFY):

- **Margins**: 0.45in on all sides
- **Font**: Times New Roman
- **Base font size**: 9.25pt
- **Name**: 14pt bold
- **Section titles**: 10.5pt bold uppercase
- **Line height**: 1.1
- **Spacing**: Precise margins between sections (15px/5px/etc.)
- **Bullet style**: Circle bullets with 0.5px spacing

These are **product constraints**, not suggestions. Changing them breaks the one-page guarantee.

---

## 🔧 Module Responsibilities

| Module | Responsibility |
|--------|---------------|
| `generator.py` | Main orchestrator, pipeline coordination |
| `enrichment.py` | Content expansion when PFR < 85% |
| `density.py` | Page Fill Rate calculation and validation |
| `llm_client.py` | All OpenAI API interactions |
| `layout.py` | HTML rendering, date/location normalization, PDF generation |
| `models.py` | Pydantic data models for type safety |
| `prompts/` | LLM prompt templates (separated for clarity) |

---

## 🚫 What This Module Does NOT Do

- ❌ Store files (stateless, no persistence)
- ❌ Upload to cloud (no Google Drive, no S3)
- ❌ Provide a UI (core module only)
- ❌ Handle authentication (API key via env var only)
- ❌ Log data (no logging by default)
- ❌ Support multi-page CVs (strict one-page constraint)

---

## 🧪 Testing

```python
from app import generate_cv_from_pdf

# Test with sample PDF
with open("tests/sample_cv.pdf", "rb") as f:
    results = generate_cv_from_pdf(f.read(), domain="finance")

assert results["en"].page_count == 1
assert results["en"].fill_percentage >= 85.0
assert results["en"].char_count >= 2200
```

---

## 📝 Example Output Metrics

```python
CVGenerationResult(
    pdf_bytes=b'%PDF-1.4...',
    docx_bytes=b'PK...',
    page_count=1,
    fill_percentage=87.3,
    char_count=2456,
    warnings=[]
)
```

---

## 🛠️ Development

### Adding a New Domain

1. Add prompt template to `app/prompts/domain_<name>.txt`
2. Update `llm_client.py` to load domain-specific prompts
3. Test PFR with sample CVs for that domain

### Adjusting PFR Targets

Edit constants in `app/density.py`:

```python
TARGET_PFR_MIN = 85.0  # Minimum target
TARGET_PFR_MAX = 90.0  # Maximum target
CRITICAL_THRESHOLD = 80.0  # Reject below this
```

---

## 📦 Dependencies

- **openai**: GPT-4 API for content generation
- **pydantic**: Data validation and type safety
- **pdfplumber**: PDF analysis and text extraction
- **xhtml2pdf**: HTML to PDF conversion
- **pdf2docx**: PDF to DOCX conversion
- **Jinja2**: HTML template rendering

---

## 🔐 Security

- No file persistence (stateless)
- No network calls except OpenAI API
- No user data stored
- API key via environment variable only

---

## 📄 License

Proprietary - Postulae Internal Use Only

---

## ✅ Product Checklist

Before releasing a CV:
- [ ] Exactly 1 page
- [ ] PFR between 85-90%
- [ ] Character count ≥ 2200
- [ ] No colors, icons, or design elements
- [ ] Times New Roman font throughout
- [ ] Professional finance/consulting tone
- [ ] No invented facts (only reasonable extrapolation)
- [ ] Passes layout preservation test

---

**Version**: 2.0.0
**Status**: Production-Ready
**Maintainer**: Postulae Team
