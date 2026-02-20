"""
Test du CV Grader - Validation des scores et conseils
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, ".")

from app.cv_grader import grade_cv, format_client_output, analyze_cv_metadata


def test_cv_parfait():
    """CV parfait style Postulae -> devrait scorer 90+"""
    cv_data = {
        "contact_information": {
            "name": "Jean DUPONT",
            "email": "jean.dupont@email.com",
            "phone": "+33 6 12 34 56 78",
            "location": "Paris, France",
            "linkedin": "linkedin.com/in/jeandupont"
        },
        "work_experience": [
            {
                "company": "McKinsey & Company",
                "role": "Senior Consultant",
                "dates": "2021 - Present",
                "responsibilities": [
                    "Piloté 12 projets de transformation digitale pour des clients CAC40, générant 25M€ d'économies annuelles identifiées",
                    "Développé une méthodologie d'analyse data innovante permettant de réduire de 40% le temps de diagnostic",
                    "Coordonné une équipe de 8 consultants juniors sur des missions stratégiques dans les secteurs banque et assurance",
                    "Négocié et remporté 3 appels d'offres majeurs représentant 2M€ de revenus additionnels pour le cabinet"
                ]
            },
            {
                "company": "Goldman Sachs",
                "role": "Analyst",
                "dates": "2018 - 2021",
                "responsibilities": [
                    "Analysé plus de 50 transactions M&A dans le secteur tech européen pour un volume total de 8Md€",
                    "Créé des modèles financiers DCF et LBO utilisés comme référence par l'équipe (20+ analysts formés)",
                    "Géré les relations avec 15 clients corporate et PE, maintenant un taux de satisfaction de 95%"
                ]
            },
            {
                "company": "BNP Paribas",
                "role": "Stagiaire Analyste",
                "dates": "2017 - 2018",
                "responsibilities": [
                    "Développé un outil d'automatisation VBA réduisant de 60% le temps de reporting mensuel",
                    "Participé à 5 closings de deals représentant 500M€ de valeur totale"
                ]
            },
            {
                "company": "Société Générale",
                "role": "Stage Assistant Trader",
                "dates": "2016",
                "responsibilities": [
                    "Optimisé les processus de réconciliation permettant d'identifier 2M€ d'écarts non détectés"
                ]
            }
        ],
        "education": [
            {
                "institution": "HEC Paris",
                "degree": "Master in Management - Grande École",
                "dates": "2015 - 2018",
                "coursework": ["Corporate Finance", "M&A", "Private Equity", "Strategy", "Financial Modeling", "Valuation"]
            }
        ],
        "language_skills": ["Français (Natif)", "Anglais (C2 - TOEIC 990)", "Espagnol (B2)"],
        "it_skills": ["Excel (Expert)", "VBA", "Python", "SQL", "PowerBI", "Bloomberg", "Capital IQ", "Factset", "PowerPoint"],
        "certifications": ["CFA Level 2 Candidate"],
        "activities_interests": ["Marathon de Paris 2023 (3h45)", "Membre du club Finance HEC"]
    }

    analysis = {
        "page_count": 1,
        "pfr": 91,
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
    print("TEST: CV PARFAIT (style Postulae)")
    print("=" * 60)
    print(f"Score: {output['color_display']} {output['score']}/100")
    print(f"Couleur: {output['color']}")
    print("\nConseils:")
    for i, tip in enumerate(output['tips'], 1):
        print(f"  {i}. {tip}")
    print(f"\nCTA: {output['cta']}")
    print()

    assert result.score >= 85, f"CV parfait devrait scorer 85+, got {result.score}"
    assert result.color in ["light_green", "dark_green"], f"Devrait être vert, got {result.color}"


def test_cv_moyen_externe():
    """CV externe moyen sans format Postulae -> devrait scorer 50-65"""
    cv_data = {
        "contact_information": {
            "name": "Marie Martin",
            "email": "marie.martin@gmail.com",
            "phone": "06 11 22 33 44"
        },
        "work_experience": [
            {
                "company": "Startup XYZ",
                "role": "Chef de projet",
                "dates": "2020 - 2023",
                "responsibilities": [
                    "Gestion de projets",
                    "Management d'équipe",
                    "Reporting"
                ]
            },
            {
                "company": "Agence ABC",
                "role": "Consultant junior",
                "dates": "2018 - 2020",
                "responsibilities": [
                    "Missions de conseil",
                    "Présentations clients"
                ]
            }
        ],
        "education": [
            {
                "institution": "École de Commerce",
                "degree": "Master",
                "dates": "2016 - 2018"
            }
        ],
        "language_skills": ["Français", "Anglais"],
        "it_skills": ["Excel", "Word", "PowerPoint"]
    }

    analysis = {
        "page_count": 1,
        "pfr": 65,
        "has_colors": False,
        "has_charts": False,
        "has_dates": True,
        "has_photo": False,
        "has_column_format": False,
        "mixed_languages": False,
    }

    result = grade_cv(cv_data, analysis)
    output = format_client_output(result)

    print("=" * 60)
    print("TEST: CV MOYEN EXTERNE")
    print("=" * 60)
    print(f"Score: {output['color_display']} {output['score']}/100")
    print(f"Couleur: {output['color']}")
    print("\nConseils:")
    for i, tip in enumerate(output['tips'], 1):
        print(f"  {i}. {tip}")
    print(f"\nCTA: {output['cta']}")
    print()

    assert 40 <= result.score <= 70, f"CV moyen devrait scorer 40-70, got {result.score}"


def test_cv_2_pages():
    """CV sur 2 pages -> plafonné à 20"""
    cv_data = {
        "contact_information": {"email": "test@test.com"},
        "work_experience": [
            {"company": "Company", "role": "Role", "responsibilities": ["Task 1", "Task 2"]}
        ],
        "education": [{"institution": "School", "degree": "Degree"}]
    }

    analysis = {
        "page_count": 2,
        "pfr": 80,
        "has_dates": True,
    }

    result = grade_cv(cv_data, analysis)
    output = format_client_output(result)

    print("=" * 60)
    print("TEST: CV 2 PAGES (hard rule)")
    print("=" * 60)
    print(f"Score: {output['color_display']} {output['score']}/100")
    print(f"Couleur: {output['color']}")
    print("\nConseils:")
    for i, tip in enumerate(output['tips'], 1):
        print(f"  {i}. {tip}")
    print(f"\nCTA: {output['cta']}")
    print()

    assert result.score <= 20, f"CV 2 pages devrait être plafonné à 20, got {result.score}"
    assert result.color == "red"


def test_cv_avec_couleurs():
    """CV avec design coloré -> plafonné à 40"""
    cv_data = {
        "contact_information": {"email": "test@test.com", "phone": "0611223344"},
        "work_experience": [
            {
                "company": "Company",
                "role": "Senior Manager",
                "dates": "2020 - 2023",
                "responsibilities": [
                    "Développé une stratégie commerciale augmentant le CA de 30%",
                    "Piloté une équipe de 10 personnes sur des projets internationaux"
                ]
            }
        ],
        "education": [{"institution": "HEC", "degree": "Master", "dates": "2018"}],
        "language_skills": ["Français (Natif)", "Anglais (C1)"],
        "it_skills": ["Excel", "Python", "SQL", "Tableau"]
    }

    analysis = {
        "page_count": 1,
        "pfr": 85,
        "has_colors": True,  # HARD RULE
        "has_dates": True,
    }

    result = grade_cv(cv_data, analysis)
    output = format_client_output(result)

    print("=" * 60)
    print("TEST: CV AVEC COULEURS (hard rule)")
    print("=" * 60)
    print(f"Score: {output['color_display']} {output['score']}/100")
    print(f"Couleur: {output['color']}")
    print("\nConseils:")
    for i, tip in enumerate(output['tips'], 1):
        print(f"  {i}. {tip}")
    print(f"\nCTA: {output['cta']}")
    print()

    assert result.score <= 40, f"CV coloré devrait être plafonné à 40, got {result.score}"
    assert result.color == "orange", f"Score 40 = orange, got {result.color}"


def test_cv_sans_experience():
    """CV sans expérience -> plafonné à 30"""
    cv_data = {
        "contact_information": {"email": "etudiant@email.com"},
        "work_experience": [],
        "education": [{"institution": "Université", "degree": "Licence"}],
        "language_skills": ["Français"]
    }

    analysis = {
        "page_count": 1,
        "has_dates": True,
    }

    result = grade_cv(cv_data, analysis)
    output = format_client_output(result)

    print("=" * 60)
    print("TEST: CV SANS EXPÉRIENCE (hard rule)")
    print("=" * 60)
    print(f"Score: {output['color_display']} {output['score']}/100")
    print(f"Couleur: {output['color']}")
    print("\nConseils:")
    for i, tip in enumerate(output['tips'], 1):
        print(f"  {i}. {tip}")
    print(f"\nCTA: {output['cta']}")
    print()

    assert result.score <= 30, f"CV sans exp devrait être plafonné à 30, got {result.score}"


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("       TEST CV GRADER - ALGORITHME FREEMIUM")
    print("=" * 60 + "\n")

    test_cv_parfait()
    test_cv_moyen_externe()
    test_cv_2_pages()
    test_cv_avec_couleurs()
    test_cv_sans_experience()

    print("=" * 60)
    print("✅ TOUS LES TESTS PASSENT")
    print("=" * 60)
