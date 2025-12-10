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
    Clasificador de temas optimizado para la campaña de Navidad de Alpina.
    Basado en patrones reales de comentarios de usuarios (2025).
    """

    def classify_topic(comment: str) -> str:
        # Convertimos a minúsculas para facilitar la búsqueda
        comment_lower = str(comment).lower().strip()

        # ------------------------------------------------------------------
        # 1. Valoración de la Campaña (Específico: "No es IA" y Emotividad)
        # ------------------------------------------------------------------
        # Insight: Los usuarios valoran mucho que no se use IA.
        if re.search(
            r'no (es|usaron|hacerlo con) ia|inteligencia artificial|'
            r'real|humano|lindo comercial|buena propuesta|'
            r'hermosa historia|mensaje.*especial|excelente video|'
            r'amo alpina|me encanta alpina|estos si son comerciales',
            comment_lower
        ):
            return 'Recepción Positiva Campaña (No IA / Emotivo)'

        # ------------------------------------------------------------------
        # 2. Precio y Accesibilidad (Punto de dolor crítico)
        # ------------------------------------------------------------------
        if re.search(
            r'costoso|car[oó]|atraco|por las nubes|vale la pena|'
            r'\$|5000|mil pesos|imposible poder comer|'
            r'est[aá]n tan|muy caro|bajenle',
            comment_lower
        ):
            return 'Queja: Precio Elevado'

        # ------------------------------------------------------------------
        # 3. Calidad del Producto / Salud (Crítico / Crisis)
        # ------------------------------------------------------------------
        # Insight: Palabras fuertes como "veneno", "remedio", "pura agua".
        if re.search(
            r'veneno|tóxico|daño|envenenado|remedio|'
            r'pura agua|maicena|sabor a|mala calidad|'
            r'p[eé]simo|p[eé]sima|horrible|gas|vomit|🤢|'
            r'octágono|sellos negros|azúcar|diabetes',
            comment_lower
        ):
            return 'Queja: Calidad o Salud'

        # ------------------------------------------------------------------
        # 4. Política y Contexto Social (Alto volumen en la muestra)
        # ------------------------------------------------------------------
        if re.search(
            r'petro|urib|derecha|izquierda|corrupci[oó]n|pa[ií]s|'
            r'gobierno|policía|patria|firme por|negocios sucios|'
            r'dignidad|verguensa|vergüenza|ambicioso',
            comment_lower
        ):
            return 'Contexto Político/Social'

        # ------------------------------------------------------------------
        # 5. Nostalgia / "Old School"
        # ------------------------------------------------------------------
        if re.search(
            r'infancia|niñez|años 90|noventa|antes|'
            r'cuando eran|recuerdo|antaño|crecí con',
            comment_lower
        ):
            return 'Nostalgia y Recuerdos'

        # ------------------------------------------------------------------
        # 6. Productos Específicos (Menciones directas)
        # ------------------------------------------------------------------
        if re.search(
            r'avena|kumis|bon yurt|bonyort|leche|yogurt|'
            r'queso|arequipe|producto|alpinito',
            comment_lower
        ):
            return 'Mención Producto Específico'

        # ------------------------------------------------------------------
        # 7. Religioso / Buenos Deseos
        # ------------------------------------------------------------------
        if re.search(
            r'am[eé]n|dios|bendiga|bendiciones|jesús|nacimiento|'
            r'navidad|espíritu',
            comment_lower
        ):
            return 'Religioso / Saludos Navideños'

        # ------------------------------------------------------------------
        # 8. Duda / Pregunta (Call to Action)
        # ------------------------------------------------------------------
        # Insight: Alguien preguntó por una "mascarilla de vino".
        if re.search(
            r'por qu[eé]|c[oó]mo|d[oó]nde|expli|receta|'
            r'ingredientes|mascarilla|puedo',
            comment_lower
        ):
            return 'Pregunta / Solicitud de Info'


        # ------------------------------------------------------------------
        # 10. Spam / Ruido / Incoherencias
        # ------------------------------------------------------------------
        # Se filtran secuencias repetitivas, risas solas o textos muy cortos
        is_spam_pattern = re.search(
            r'(.)\1{4,}|'       # Caracteres repetidos (ej: aaaaaa)
            r'tinga linga|'     # Patrón específico detectado
            r'pp\d+|'           # Secuencias tipo Pp099
            r'^[0-9]+$|'        # Solo números
            r'^jajaj?a?+$|'     # Solo risas
            r'^hola$|'          # Saludos vacíos
            r'emoji|🤡',        # Emojis solos (si se pasan como texto)
            comment_lower
        )
        
        # Si es muy corto (menos de 3 letras) y no cayó en categorías anteriores
        if is_spam_pattern or len(comment_lower) < 3:
            return 'Ruido / Spam'

        # ------------------------------------------------------------------
        # DEFAULT
        # ------------------------------------------------------------------
        return 'Otros / Neutro'

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
