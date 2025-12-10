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
    Clasificador V2: Optimizado para reducir la tasa de 'Otros'.
    Incluye categorías de Desigualdad Social, Cultura Pop y Aprobación General.
    """

    def classify_topic(comment: str) -> str:
        # Limpieza básica
        comment_lower = str(comment).lower().strip()
        
        # Si el comentario es vacío
        if not comment_lower:
            return 'Ruido / Spam'

        # ------------------------------------------------------------------
        # 1. Valoración: "No IA" y Autenticidad (High Value)
        # ------------------------------------------------------------------
        if re.search(
            r'no (es|usaron|hacerlo con) ia|inteligencia artificial|'
            r'me gusta que no|real|humano|milagro.*no.*ia',
            comment_lower
        ):
            return 'Valoración: Autenticidad (No IA)'

        # ------------------------------------------------------------------
        # 2. Desigualdad Social y Estratificación (Nuevo - Insight Social)
        # ------------------------------------------------------------------
        # Diferente a política. Habla de ricos/pobres, estratos, locaciones.
        if re.search(
            r'estrato|soacha|30m2|30 m2|clase alta|clase baja|'
            r'ricos|pobres|barrio|apartamento|realidad es otra|'
            r'gente.*navidad',
            comment_lower
        ):
            return 'Crítica Social / Desigualdad'

        # ------------------------------------------------------------------
        # 3. Política Dura (Petro / Gobierno)
        # ------------------------------------------------------------------
        if re.search(
            r'petro|urib|derecha|izquierda|corrupci[oó]n|pa[ií]s|'
            r'gobierno|policía|patria|firme por|negocios sucios|'
            r'dignidad|verguensa|vergüenza|ambicioso|borregos',
            comment_lower
        ):
            return 'Política y Gobierno'

        # ------------------------------------------------------------------
        # 4. Salud, Octógonos y Calidad (Gestión de Crisis)
        # ------------------------------------------------------------------
        if re.search(
            r'veneno|tóxico|daño|envenenado|remedio|'
            r'pura agua|maicena|sabor a|mala calidad|'
            r'p[eé]simo|p[eé]sima|horrible|gas|vomit|🤢|'
            r'octágono|sello|azúcar|diabetes|diabético',
            comment_lower
        ):
            return 'Queja: Salud y Calidad'

        # ------------------------------------------------------------------
        # 5. Precio (Queja Recurrente)
        # ------------------------------------------------------------------
        if re.search(
            r'costoso|car[oó]|atraco|nubes|vale la pena|'
            r'\$|5000|mil pesos|imposible poder comer|'
            r'est[aá]n tan|muy caro|bajenle|subieron de precio',
            comment_lower
        ):
            return 'Queja: Precio Elevado'

        # ------------------------------------------------------------------
        # 6. Cultura Pop, Memes y Random (Nuevo - Limpia "Otros")
        # ------------------------------------------------------------------
        # Referencias a juegos, animes o chistes internos de internet
        if re.search(
            r'one piece|happy wheels|terrifier|eggman|master plan|'
            r'mapa|sonido de|blusa de|jojojo|risa',
            comment_lower
        ):
            return 'Cultura Pop / Memes / Random'

        # ------------------------------------------------------------------
        # 7. Nostalgia
        # ------------------------------------------------------------------
        if re.search(
            r'infancia|niñez|años 90|noventa|antes|'
            r'cuando eran|recuerdo|antaño|crecí con|tradición',
            comment_lower
        ):
            return 'Nostalgia y Tradición'

        # ------------------------------------------------------------------
        # 8. Navidad y Religión (Incluye errores ortográficos)
        # ------------------------------------------------------------------
        if re.search(
            r'am[eé]n|dios|bendiga|bendiciones|jesús|nacimiento|'
            r'navidad|nabida|neveded|espíritu|fe |creador',
            comment_lower
        ):
            return 'Religioso / Saludos Navideños'

        # ------------------------------------------------------------------
        # 9. Aprobación General / Brand Love (Categoría Ampliada)
        # ------------------------------------------------------------------
        # Captura "Genial", "Divinoooo", "Me encanta", "Alpinista"
        if re.search(
            r'genial|hermos[oa]|bell[oa]|divino|lindo|bonito|'
            r'me gusta|me encanta|ame\b|amé|amo\b|'
            r'excelente|increíble|delicia|rico|'
            r'buena imagen|te ves bn|alpinista|mejor marca|'
            r'conecta|ternura|te amoooo',
            comment_lower
        ):
            return 'Aprobación General / Brand Love'

        # ------------------------------------------------------------------
        # 10. Productos Específicos
        # ------------------------------------------------------------------
        if re.search(
            r'avena|kumis|bon yurt|bonyort|leche|yogurt|'
            r'queso|arequipe|producto|alpinito',
            comment_lower
        ):
            return 'Mención Producto Específico'
        
        # ------------------------------------------------------------------
        # 11. Preguntas / Call to Action
        # ------------------------------------------------------------------
        if re.search(
            r'por qu[eé]|c[oó]mo|d[oó]nde|expli|receta|'
            r'ingredientes|mascarilla|puedo',
            comment_lower
        ):
            return 'Pregunta / Solicitud'

        # ------------------------------------------------------------------
        # 12. Animales (Patrón específico detectado)
        # ------------------------------------------------------------------
        if re.search(
            r'perr(o|ito)|gat(o|ico)|mascota|animal',
            comment_lower
        ):
            return 'Tema: Animales'

        # ------------------------------------------------------------------
        # 13. Ruido / Spam (Filtro ajustado)
        # ------------------------------------------------------------------
        is_spam_pattern = re.search(
            r'tinga linga|'     # Patrón específico spam
            r'pp\d+|'           # Secuencias tipo Pp099
            r'^[0-9]+$|'        # Solo números (ej: "6")
            r'^jajaj?a?+$|'     # Solo risas sin texto
            r'^hola$|'          # Saludos vacíos
            r'emoji|🤡|'        # Emojis ofensivos solos
            r'%%%%',
            comment_lower
        )
        
        # Solo marcamos como spam si es muy corto Y NO es una palabra válida positiva (ej: "Ty", "Ame")
        # Y si cumple el patrón de spam explícito.
        if is_spam_pattern:
            return 'Ruido / Spam'
        
        # "Ty" (Thank you) es común, lo salvamos del filtro de longitud
        if comment_lower in ['ty', 'si', 'no', 'ok']:
             return 'Otros / Neutro'

        if len(comment_lower) < 3: 
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
