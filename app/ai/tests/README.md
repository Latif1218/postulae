# Tests CV Enhancer

## Structure

```
tests/
├── test_extraction.py              # Test extraction PDF
├── test_enrichment_debug.py        # Test enrichissement
├── test_hardening.py               # Test robustesse pipeline
├── test_extraction_validation.py   # Validation extraction work_experience
├── test_with_experiences.py        # Test CVs avec expériences
├── test_bad_cv.py                  # Test CVs faibles
├── test_bad_cv_enriched.py         # Test enrichissement CVs faibles
├── test_financial_analyst.py       # Test CV finance
├── test_lorenzo.py                 # Test CV Lorenzo
├── test_enriched.py                # Test enrichissement complet
└── debug/                          # Scripts de debug
    ├── debug_bad_cv.py
    ├── debug_financial_analyst.py
    └── debug_llm_response.py
```

## Tests principaux

### `test_extraction.py`
Test d'extraction de texte depuis PDF.

### `test_enrichment_debug.py`
Validation du processus d'enrichissement avec contraintes PFR.

### `test_hardening.py`
Test de robustesse du pipeline complet (extraction → génération → enrichissement → export).

## Tests spécifiques

### `test_extraction_validation.py`
Validation critique de l'extraction work_experience (bug résolu 09/01/2026).

### `test_with_experiences.py`
Test CVs avec expériences professionnelles complètes.

### `test_bad_cv.py` / `test_bad_cv_enriched.py`
Test CVs avec contenu insuffisant (PFR < 65%).

## Scripts de debug

Fichiers dans `debug/` pour investigation ponctuelle de problèmes.

## Exécution

```bash
# Depuis la racine du projet
python tests/test_extraction.py
python tests/test_enrichment_debug.py
python tests/test_hardening.py
```
