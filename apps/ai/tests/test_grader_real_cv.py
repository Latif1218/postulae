"""
Test du grader sur de vrais CVs
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, ".")

from app.cv_grader import grade_cv, format_client_output, analyze_cv_metadata


def test_fayed_cv():
    """Test avec le CV Fayed HANAFI - devrait scorer 85+"""

    # Données extraites du CV Fayed (référence finance élite)
    cv_data = {
        "contact_information": {
            "name": "Fayed HANAFI",
            "email": "fayed.hanafi@gmail.com",
            "phone": "+33 6 12 34 56 78",
            "location": "Paris, France",
            "linkedin": "linkedin.com/in/fayedhanafi"
        },
        "work_experience": [
            {
                "company": "Rothschild & Co",
                "role": "Analyst M&A",
                "dates": "2022 - Present",
                "location": "Paris",
                "responsibilities": [
                    "Executed 8 M&A transactions totaling €2.5B in enterprise value across industrials and consumer sectors",
                    "Built complex financial models (DCF, LBO, merger models) for Fortune 500 clients with 99% accuracy",
                    "Led due diligence workstreams coordinating 15+ advisors across legal, tax, and commercial teams",
                    "Prepared investment memoranda and management presentations for C-suite executives and board members"
                ]
            },
            {
                "company": "Lazard",
                "role": "Summer Analyst",
                "dates": "2021",
                "location": "Paris",
                "responsibilities": [
                    "Supported senior bankers on 3 live M&A mandates in the TMT sector worth €800M combined",
                    "Conducted comprehensive industry research and competitive analysis for strategic advisory projects"
                ]
            },
            {
                "company": "BNP Paribas CIB",
                "role": "Off-cycle Intern",
                "dates": "2020",
                "location": "Paris",
                "responsibilities": [
                    "Developed automated reporting tools in VBA reducing weekly reporting time by 60%",
                    "Analyzed credit risk metrics for a €500M leveraged finance portfolio"
                ]
            }
        ],
        "education": [
            {
                "institution": "HEC Paris",
                "degree": "Master in Management - Grande École",
                "dates": "2019 - 2022",
                "location": "Paris",
                "coursework": ["Corporate Finance", "M&A", "Private Equity", "Valuation", "Financial Modeling", "Strategy"]
            },
            {
                "institution": "London School of Economics",
                "degree": "Exchange Program - Finance",
                "dates": "2021",
                "location": "London"
            }
        ],
        "language_skills": [
            "French (Native)",
            "English (C2 - TOEIC 990)",
            "Arabic (Native)",
            "Spanish (B1)"
        ],
        "it_skills": [
            "Excel (Expert - VBA)",
            "PowerPoint",
            "Capital IQ",
            "Bloomberg Terminal",
            "Factset",
            "Python",
            "SQL",
            "Word"
        ],
        "certifications": ["CFA Level 2 Candidate"],
        "activities_interests": [
            "Marathon de Paris 2023 (3h42)",
            "Volunteer at Restos du Coeur (200+ hours)",
            "HEC Finance Club - Vice President"
        ]
    }

    analysis = {
        "page_count": 1,
        "pfr": 89,
        "has_colors": False,
        "has_charts": False,
        "has_dates": True,
        "has_photo": False,
        "has_column_format": True,
        "mixed_languages": False,
    }

    result = grade_cv(cv_data, analysis)
    output = format_client_output(result)

    print("=" * 60)
    print("CV: Fayed HANAFI (Finance Elite)")
    print("=" * 60)
    print(f"\nScore: {output['color_display']} {output['score']}/100")
    print(f"Couleur: {output['color']}")

    if output['tips']:
        print("\nConseils:")
        for i, tip in enumerate(output['tips'], 1):
            print(f"  {i}. {tip}")
    else:
        print("\nConseils: Aucun - CV excellent!")

    print(f"\nCTA: {output['cta']}")
    print()

    return result.score


def test_bad_cv():
    """Test avec un CV faible"""

    cv_data = {
        "contact_information": {
            "email": "test@email.com"
        },
        "work_experience": [
            {
                "company": "Startup",
                "role": "Stagiaire",
                "responsibilities": [
                    "Diverses tâches",
                    "Support équipe"
                ]
            }
        ],
        "education": [
            {
                "institution": "Université",
                "degree": "Licence"
            }
        ],
        "language_skills": ["Français"],
        "it_skills": ["Word", "Excel"]
    }

    analysis = {
        "page_count": 1,
        "pfr": 55,
        "has_colors": False,
        "has_dates": True,
    }

    result = grade_cv(cv_data, analysis)
    output = format_client_output(result)

    print("=" * 60)
    print("CV: Faible (test upsell)")
    print("=" * 60)
    print(f"\nScore: {output['color_display']} {output['score']}/100")
    print(f"Couleur: {output['color']}")
    print("\nConseils:")
    for i, tip in enumerate(output['tips'], 1):
        print(f"  {i}. {tip}")
    print(f"\nCTA: {output['cta']}")
    print()

    return result.score


def test_cv_externe_canva():
    """Test CV externe style Canva avec couleurs"""

    cv_data = {
        "contact_information": {
            "name": "Marie Dupont",
            "email": "marie.dupont@gmail.com",
            "phone": "06 12 34 56 78"
        },
        "work_experience": [
            {
                "company": "Agence Marketing",
                "role": "Chef de projet",
                "dates": "2020 - 2023",
                "responsibilities": [
                    "Gestion de projets digitaux",
                    "Coordination d'équipe",
                    "Suivi des KPIs"
                ]
            },
            {
                "company": "Startup Tech",
                "role": "Assistante marketing",
                "dates": "2018 - 2020",
                "responsibilities": [
                    "Community management",
                    "Création de contenu"
                ]
            }
        ],
        "education": [
            {
                "institution": "IAE Paris",
                "degree": "Master Marketing Digital",
                "dates": "2016 - 2018"
            }
        ],
        "language_skills": ["Français", "Anglais courant"],
        "it_skills": ["Suite Adobe", "Canva", "Mailchimp", "Google Analytics"]
    }

    analysis = {
        "page_count": 1,
        "pfr": 75,
        "has_colors": True,  # HARD RULE - Canva coloré
        "has_charts": True,  # HARD RULE - Barres de compétences
        "has_dates": True,
        "has_column_format": False,
    }

    result = grade_cv(cv_data, analysis)
    output = format_client_output(result)

    print("=" * 60)
    print("CV: Externe Canva (coloré + graphiques)")
    print("=" * 60)
    print(f"\nScore: {output['color_display']} {output['score']}/100")
    print(f"Couleur: {output['color']}")
    print("\nConseils:")
    for i, tip in enumerate(output['tips'], 1):
        print(f"  {i}. {tip}")
    print(f"\nCTA: {output['cta']}")
    print()

    return result.score


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("       TEST CV GRADER - VRAIS CVS")
    print("=" * 60 + "\n")

    score_fayed = test_fayed_cv()
    score_bad = test_bad_cv()
    score_canva = test_cv_externe_canva()

    print("=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    print(f"Fayed HANAFI (finance élite): {score_fayed}/100")
    print(f"CV faible (upsell):           {score_bad}/100")
    print(f"CV Canva (coloré):            {score_canva}/100")
    print("=" * 60)

    # Validations
    assert score_fayed >= 85, f"Fayed devrait scorer 85+, got {score_fayed}"
    assert score_bad < 60, f"CV faible devrait scorer <60, got {score_bad}"
    assert score_canva <= 40, f"CV Canva coloré devrait être plafonné, got {score_canva}"

    print("\n✅ Tous les tests passent!")
