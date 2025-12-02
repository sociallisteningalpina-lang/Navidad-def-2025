#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clasificador de Temas para Comentarios de Campañas
Personalizable por campaña/producto
"""
import re
from typing import Callable


def create_topic_classifier() -> Callable[[str], str]:
    """
    Clasificador de temas ajustado específicamente
    a la campaña de Navidad de Alpina y a la muestra real de comentarios.
    """

    def classify_topic(comment: str) -> str:
        comment_lower = str(comment).lower()

        # ------------------------------------------------------------------
        # 1. Opinión positiva del producto o de la campaña (video / historia)
        # ------------------------------------------------------------------
        if re.search(
            r'me gusta|me encanta|delicia|delicioso|'
            r'hermos[oa]|que lindo|que bello|bonito|'
            r'muy bueno|excelente|una delicia|'
            r'mensaje.*especial|hermosa historia|'
            r'propuesta de alpina|me gusta que no es ia',
            comment_lower
        ):
            return 'Opinión Positiva (Producto/Campaña)'

        # ------------------------------------------------------------------
        # 2. Opinión negativa del producto
        # ------------------------------------------------------------------
        if re.search(
            r'est[aá] muy mala|p[eé]simo|p[eé]sima|horrible|feo|'
            r'sabor a remedio|pura agua|cambi[oó] mucho|'
            r'leche.*p[eé]simo|vomit|🤢',
            comment_lower
        ):
            return 'Opinión Negativa del Producto'

        # ------------------------------------------------------------------
        # 3. Comentarios sobre productos específicos Alpina
        # (Avena, Kumis, Bon Yurt, Leche)
        # ------------------------------------------------------------------
        if re.search(
            r'avena|kumis|bon yurt|bonyort|leche|producto alpina|'
            r'productos alpina',
            comment_lower
        ):
            return 'Producto Alpina Específico'

        # ------------------------------------------------------------------
        # 4. Precio / costo / accesibilidad
        # ------------------------------------------------------------------
        if re.search(
            r'costoso|car[oó]|atraco|por las nubes|vale la pena|'
            r'\$|5000|est[aá]n tan costoso',
            comment_lower
        ):
            return 'Precio y Accesibilidad'

        # ------------------------------------------------------------------
        # 5. Nostalgia / referencias al pasado
        # ------------------------------------------------------------------
        if re.search(
            r'infancia|antes|cuando eran|tra[ií]an m[aá]s|'
            r'producto de los 90|noventa',
            comment_lower
        ):
            return 'Nostalgia / Recuerdos'

        # ------------------------------------------------------------------
        # 6. Religioso
        # ------------------------------------------------------------------
        if re.search(
            r'am[eé]n|amen|bendiga|bendiciones|gracias se[nñ]or',
            comment_lower
        ):
            return 'Religioso'

        # ------------------------------------------------------------------
        # 7. Política (muy presente en la muestra)
        # ------------------------------------------------------------------
        if re.search(
            r'petro|urib|ultraderecha|corrupci[oó]n|pa[ií]s',
            comment_lower
        ):
            return 'Política'

        # ------------------------------------------------------------------
        # 8. Insultos / ataques a terceros
        # ------------------------------------------------------------------
        if re.search(
            r'verg[uü]enza|aprovechado|ambicioso|viejo cacorro|'
            r'vergensa|pena!!!',
            comment_lower
        ):
            return 'Insultos / Ataques'

        # ------------------------------------------------------------------
        # 9. Preguntas / solicitudes de explicación
        # ------------------------------------------------------------------
        if re.search(
            r'por qu[eé]|c[oó]mo se|explique|qu[eé] ingredientes|'
            r'qu[eé] clase|d[oó]nde|pregunta|puedo|ayuda',
            comment_lower
        ):
            return 'Preguntas / Solicitudes'

        # ------------------------------------------------------------------
        # 10. Apariencia / halagos personales (presentes en muestra)
        # ------------------------------------------------------------------
        if re.search(
            r'te ves bien|buena imagen|te ves bn|imagen personal',
            comment_lower
        ):
            return 'Apariencia / Halagos Personales'

        # ------------------------------------------------------------------
        # 11. Animales / perritos (muy presentes en la muestra)
        # ------------------------------------------------------------------
        if re.search(
            r'perritos|gatos|mascotas|llamen al polic[ií]a.*perritos',
            comment_lower
        ):
            return 'Mascotas / Animales'

        # ------------------------------------------------------------------
        # 12. Fuera de tema / ruido / spam / expresiones cortas
        # (último para no bloquear categorías anteriores)
        # ------------------------------------------------------------------
        if (
            re.search(
                r'tinga linga|pp\d+|tuuu|jajaja|jaja|hola|'
                r'6$|emoji|☺️|🤢|❤|random',
                comment_lower
            )
            or len(comment_lower.split()) < 3
        ):
            return 'Fuera de Tema / No Relevante'

        # ------------------------------------------------------------------
        # DEFAULT
        # ------------------------------------------------------------------
        return 'Otros'

    return classify_topic


# ============================================================================
# METADATA DE LA CAMPAÑA (OPCIONAL)
# ============================================================================

CAMPAIGN_METADATA = {
    'campaign_name': 'Alpina - Kéfir',
    'product': 'Kéfir Alpina',
    'categories': [
        'Preguntas sobre el Producto',
        'Comparación con Kéfir Casero/Artesanal',
        'Ingredientes y Salud',
        'Competencia y Disponibilidad',
        'Opinión General del Producto',
        'Fuera de Tema / No Relevante',
        'Otros'
    ],
    'version': '1.0',
    'last_updated': '2025-11-20'
}


def get_campaign_metadata() -> dict:
    """Retorna metadata de la campaña"""
    return CAMPAIGN_METADATA.copy()
