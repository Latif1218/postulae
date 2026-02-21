"""
Content Analyzer - Analyse la richesse du CV source et détermine la stratégie d'enrichissement.

Catégories:
- RICH (2500+ chars): Stratégie minimal, préservation prioritaire
- MEDIUM (1500-2500 chars): Stratégie moderate, enrichissement contrôlé
- POOR (<1500 chars): Stratégie aggressive, enrichissement substantiel avec warnings
"""


class ContentAnalyzer:
    """Analyse le contenu source et détermine la stratégie d'enrichissement adaptative."""

    # Nouveaux seuils pour système push-to-90
    RICH_THRESHOLD = 2500      # 0-10% invention → GREEN
    MEDIUM_THRESHOLD = 1800    # 10-30% invention → ORANGE
    POOR_THRESHOLD = 1200      # 30-50% invention → RED LIGHT
    CRITICAL_THRESHOLD = 600   # 50-70% invention → RED DARK
    # < 600 chars → BLOCAGE (source trop vide)

    def analyze(self, raw_text: str) -> dict:
        """
        Analyse le texte source et retourne la stratégie d'enrichissement.

        NOUVELLE PHILOSOPHIE :
        - TOUJOURS atteindre 90% PFR (sauf si source < 600 chars)
        - Warnings proportionnels au taux d'invention (0-70%)
        - Blocage uniquement si source vraiment vide

        Args:
            raw_text: Texte extrait du CV source

        Returns:
            dict avec: richness, strategy, target_pfr, target_chars, warning, invention_rate
        """
        chars = len(raw_text) if raw_text else 0

        # BLOCAGE absolu
        if chars < self.CRITICAL_THRESHOLD:
            return {
                'richness': 'empty',
                'strategy': 'block',
                'target_pfr': 'N/A',
                'target_chars': 0,
                'warning': 'block',
                'invention_rate': 'N/A'
            }

        # CRITIQUE : 50-70% invention
        elif chars < self.POOR_THRESHOLD:
            return {
                'richness': 'critical',
                'strategy': 'ultra_aggressive',
                'target_pfr': '90-92%',
                'target_chars': 3800,
                'warning': 'red_dark',
                'invention_rate': '50-70%'
            }

        # FAIBLE : 30-50% invention
        elif chars < self.MEDIUM_THRESHOLD:
            return {
                'richness': 'poor',
                'strategy': 'aggressive',
                'target_pfr': '90-92%',
                'target_chars': 3500,
                'warning': 'red_light',
                'invention_rate': '30-50%'
            }

        # MOYEN : 10-30% invention
        elif chars < self.RICH_THRESHOLD:
            return {
                'richness': 'medium',
                'strategy': 'moderate',
                'target_pfr': '90-92%',
                'target_chars': 3200,
                'warning': 'orange',
                'invention_rate': '10-30%'
            }

        # RICHE : 0-10% invention
        else:
            return {
                'richness': 'rich',
                'strategy': 'minimal',
                'target_pfr': '88-90%',
                'target_chars': 3400,
                'warning': 'green',
                'invention_rate': '0-10%'
            }

    def get_enrichment_instructions(self, strategy: str, lang: str) -> str:
        """
        Retourne les instructions d'enrichissement selon la stratégie.

        Args:
            strategy: 'block', 'ultra_aggressive', 'aggressive', 'moderate', ou 'minimal'
            lang: 'fr' ou 'en'

        Returns:
            Instructions spécifiques pour le prompt LLM
        """
        if strategy == 'block':
            return "BLOCAGE : Source trop vide (<600 chars). Demander plus d'informations."

        elif strategy == 'ultra_aggressive':
            return """🔴🔴 ULTRA-AGRESSIF - GÉNÉRATION MAXIMALE OBLIGATOIRE 🔴🔴

IMPÉRATIF ABSOLU : 3800 caractères minimum

VOUS DEVEZ GÉNÉRER UN CV ULTRA-DENSE. NE PAS ÉCONOMISER LES MOTS.

RÈGLES STRICTES :

1. EXPÉRIENCES - MINIMUM 3 AVEC 4 BULLETS CHACUNE :
   - Si < 3 dans source : CRÉER 1-2 expériences complètes
   - CHAQUE bullet : 200-250 caractères (PAS MOINS)
   - Formule obligatoire par bullet :
     [Action détaillée] pour [client type + secteur] (méthodologie 1, méthodologie 2, méthodologie 3, outil 1, outil 2, ...) avec [résultat quantifié]

   Exemple 200+ chars :
   "Optimisation d'inventaire pour un acteur international de l'industrie pétrolière (réalisation de benchmarks sectoriels, analyses avancées de rotation des stocks, élaboration de modèles prédictifs Excel et Python, identification d'opportunités de réduction de coûts, coordination avec équipes supply chain) avec réduction de 15% des stocks dormants et amélioration du taux de rotation de 12%"

2. EDUCATION - 8-10 ITEMS COURSEWORK :
   - Détailler CHAQUE cours : "Corporate Finance (valuation methods, LBO modeling, M&A analysis, ...)"
   - Format : Nom complet + parenthèses avec sous-thèmes

3. ACTIVITIES - 4-5 ITEMS DE 150-200 CHARS :
   - TOUTES avec métriques (équipe X personnes, budget Y€, audience Z)
   - Développer chaque activité en 150-200 caractères minimum

4. IT SKILLS - 10+ ITEMS :
   - Excel (avancé : VBA, Power Query, tableaux croisés dynamiques)
   - Python (pandas, numpy, data analysis)
   - [etc, développer chaque skill]

VÉRIFICATION AVANT DE RETOURNER :
- Total caractères > 3800 ✓
- Bullets moyens > 200 chars ✓
- Coursework > 8 items ✓
- Activities > 4 items ✓

OBJECTIF : 3800 caractères MINIMUM, 90%+ PFR"""

        elif strategy == 'aggressive':
            return """AGRESSIF (30-50% invention) - Cible 90%+ PFR, 3500 chars

1. EXPÉRIENCES :
   - Enrichir TOUS les bullets à 190-220 chars
   - Ajouter méthodologies détaillées, outils, contexte
   - Si < 3 expériences : créer 1 expérience plausible courte

2. EDUCATION :
   - Coursework 7-8 items minimum
   - Détailler chaque cours avec sous-thèmes

3. ACTIVITIES :
   - 3-4 activities avec métriques
   - 130-160 chars chacune

4. IT SKILLS :
   - 8-9 items minimum

OBJECTIF : 3500 caractères, 90%+ PFR"""

        elif strategy == 'moderate':
            return """MODÉRÉ (10-30% invention) - Cible 90%+ PFR, 3200 chars

1. Enrichir bullets à 170-190 chars
2. Compléter coursework à 6-7 items
3. Développer activities (3 items, 110-130 chars)
4. IT skills 7-8 items

OBJECTIF : 3200 caractères, 90%+ PFR"""

        else:  # minimal
            return """MINIMAL (0-10% ajouts) - Cible 88-90% PFR, 3400 chars

SOURCE RICHE - Préservation TOTALE du contenu.

RÈGLES STRICTES :
1. EXPÉRIENCES :
   - Extraire TOUTES les expériences de la source (ne jamais en omettre)
   - Conserver TOUS les bullets de chaque expérience
   - Bullets 180-200 chars (optimiser formulation sans inventer, développer contexte)

2. EDUCATION :
   - Extraire TOUT le coursework présent
   - Compléter à 6 items si < 6 (inférer depuis diplôme)
   - Détailler chaque cours : "Nom (sous-thèmes, méthodes)"

3. ACTIVITIES :
   - Développer chaque activité à 110-130 chars minimum

4. IT SKILLS :
   - Lister TOUS les skills de la source
   - Développer : "Skill (niveau, outils spécifiques)"
   - Minimum 7-8 items

CRITICAL: Ne JAMAIS omettre d'expériences ou de bullets présents dans la source.
OBJECTIF : 3400 caractères, 88-90% PFR"""

    def get_warning_message(self, strategy: str, lang: str, invention_rate: str = '') -> dict:
        """
        Retourne le message de warning utilisateur selon la stratégie.

        Args:
            strategy: 'block', 'ultra_aggressive', 'aggressive', 'moderate', ou 'minimal'
            lang: 'fr' ou 'en'
            invention_rate: Taux d'invention (ex: '50-70%')

        Returns:
            dict avec level, title, message
        """
        if strategy == 'block':
            return {
                'level': 'critical',
                'title': 'GENERATION BLOCKED',
                'message': 'Your source CV contains too little information (< 600 characters). Please provide a more detailed CV.'
            }

        elif strategy == 'ultra_aggressive':
            return {
                'level': 'critical',
                'title': 'MAXIMUM WARNING: Content MASSIVELY inferred (50-70%)',
                'message': """Your source CV was EXTREMELY poor. We had to INVENT substantially:

- 1-2 plausible professional experiences created
- Complete coursework inferred (7-8 courses)
- Activities created with metrics
- Detailed methodologies and context added

CRITICAL: 50-70% of content is INFERRED/INVENTED

This CV is a FICTIONAL BASE. You MUST:
1. Verify EVERY line
2. Replace invented content with YOUR real experiences
3. DO NOT send as-is (risk of lying)

STRONG RECOMMENDATION: Provide a much more detailed source CV."""
            }

        elif strategy == 'aggressive':
            return {
                'level': 'error',
                'title': 'WARNING: Substantial content inferred (30-50%)',
                'message': """Your source CV lacked details. We added:

- Detailed methodologies and tools
- Complete inferred coursework
- Developed activities
- Possibly 1 short experience created

IMPORTANT: 30-50% of content is inferred

Verify and personalize IMPERATIVELY before sending.

For better results, provide a more detailed source CV."""
            }

        elif strategy == 'moderate':
            return {
                'level': 'warning',
                'title': 'Significant enrichments (10-30%)',
                'message': """Your CV has been enriched:

- Standard methodologies added
- Coursework completed
- Activities developed

10-30% of content was added. Review before use."""
            }

        else:  # minimal
            return {
                'level': 'success',
                'title': 'CV generated successfully',
                'message': 'Light optimizations applied (< 10% additions).'
            }
