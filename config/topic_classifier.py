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
    Clasificador V3 (Navidad): 
    - Reduce 'Otros' capturando críticas a los actores/influencers (Lalo & Cota).
    - Mejora detección de Spam complejo (letras repetidas, secuencias random).
    - Refina quejas de sabor/calidad.
    """

    def classify_topic(comment: str) -> str:
        # Limpieza básica
        comment_lower = str(comment).lower().strip()
        
        # Si el comentario es vacío
        if not comment_lower:
            return 'Ruido / Spam'

        # ------------------------------------------------------------------
        # 1. Valoración: "No IA" y Autenticidad (Insight Clave)
        # ------------------------------------------------------------------
        if re.search(
            r'no (es|usaron|hacerlo con) ia|inteligencia artificial|'
            r'me gusta que no|real|humano|milagro.*no.*ia|'
            r'no la ocultan.*oct[oó]gonos', # Respuesta específica sobre transparencia
            comment_lower
        ):
            return 'Valoración: Autenticidad (No IA)'

        # ------------------------------------------------------------------
        # 2. Crítica: Casting, Actores y Ejecución (NUEVO - Reduce Otros)
        # ------------------------------------------------------------------
        # Captura quejas sobre "Lalo y Cota", "familia falsa", "enchufados"
        if re.search(
            r'lalo|cota|señoras|pasivo|enchufados|fritos|tutis|'
            r'familia de verdad|casado|actores|comercial|falsos|'
            r'mentiras|l[áa]mpara|contenido|esconda|pareja|'
            r'quienes son|no había una familia|semejante empresa',
            comment_lower
        ):
            return 'Crítica Influencer'

        # ------------------------------------------------------------------
        # 3. Desigualdad Social (Contexto País)
        # ------------------------------------------------------------------
        if re.search(
            r'estrato|soacha|30m2|30 m2|clase alta|clase baja|'
            r'ricos|pobres|barrio|apartamento|realidad es otra|'
            r'gente.*navidad',
            comment_lower
        ):
            return 'Crítica Social / Desigualdad'

        # ------------------------------------------------------------------
        # 4. Política Dura
        # ------------------------------------------------------------------
        if re.search(
            r'petro|urib|derecha|izquierda|corrupci[oó]n|pa[ií]s|'
            r'gobierno|policía|patria|firme por|negocios sucios|'
            r'dignidad|verguensa|vergüenza|ambicioso|borregos|'
            r'libertad|socialis|capitalis',
            comment_lower
        ):
            return 'Política y Gobierno'

        # ------------------------------------------------------------------
        # 5. Salud, Calidad y Sabor (Reforzado)
        # ------------------------------------------------------------------
        if re.search(
            r'veneno|t[óo]xico|daño|envenenado|remedio|qu[íi]mico|'
            r'pura agua|maicena|sabor a|mala calidad|est[áa] muy mala|'
            r'p[eé]simo|p[eé]sima|horrible|gas|vomit|🤢|'
            r'oct[áa]gono|sello|az[úu]car|diabetes|diab[eé]tico|'
            r'no nutre|enferma|lacto suero|c[áa]ncer|muerte',
            comment_lower
        ):
            return 'Queja: Salud, Calidad y Sabor'

        # ------------------------------------------------------------------
        # 6. Precio Elevado
        # ------------------------------------------------------------------
        if re.search(
            r'costoso|car[oó]|atraco|nubes|vale la pena|'
            r'\$|5000|mil pesos|imposible poder comer|'
            r'est[aá]n tan|muy caro|bajenle|subieron|plata',
            comment_lower
        ):
            return 'Queja: Precio Elevado'

        # ------------------------------------------------------------------
        # 7. Cultura Pop, Memes y Random
        # ------------------------------------------------------------------
        if re.search(
            r'one piece|happy wheels|terrifier|eggman|master plan|'
            r'mapa|sonido de|blusa de|jojojo|risa|teoría|lógica',
            comment_lower
        ):
            return 'Cultura Pop / Memes / Random'

        # ------------------------------------------------------------------
        # 8. Navidad y Religión
        # ------------------------------------------------------------------
        if re.search(
            r'am[eé]n|dios|bendiga|bendiciones|jesús|nacimiento|'
            r'navidad|nabida|neveded|espíritu|fe |creador|'
            r'noche buena|diciembre',
            comment_lower
        ):
            return 'Religioso / Saludos Navideños'

        # ------------------------------------------------------------------
        # 9. Nostalgia y Tradición
        # ------------------------------------------------------------------
        if re.search(
            r'infancia|niñez|años 90|noventa|antes|'
            r'cuando eran|recuerdo|antaño|crecí con|tradición|'
            r'historia|siempre',
            comment_lower
        ):
            return 'Nostalgia y Tradición'

        # ------------------------------------------------------------------
        # 10. Aprobación General / Brand Love
        # ------------------------------------------------------------------
        if re.search(
            r'genial|hermos[oa]|bell[oa]|divino|lindo|bonito|'
            r'me gusta|me encanta|ame\b|amé|amo\b|'
            r'excelente|increíble|delicia|rico|'
            r'buena imagen|te ves bn|alpinista|mejor marca|'
            r'conecta|ternura|te amoooo|buenas vibras|'
            r'bienestar|top|orgullosa|fan',
            comment_lower
        ):
            return 'Aprobación General / Brand Love'

        # ------------------------------------------------------------------
        # 11. Productos Específicos
        # ------------------------------------------------------------------
        if re.search(
            r'avena|kumis|bon yurt|bonyort|leche|yogurt|'
            r'queso|arequipe|producto|alpinito|finesse',
            comment_lower
        ):
            return 'Mención Producto Específico'
        
        # ------------------------------------------------------------------
        # 12. Preguntas / Call to Action
        # ------------------------------------------------------------------
        if re.search(
            r'por qu[eé]|c[oó]mo|d[oó]nde|expli|receta|'
            r'ingredientes|mascarilla|puedo',
            comment_lower
        ):
            return 'Pregunta / Solicitud'

        # ------------------------------------------------------------------
        # 13. Animales
        # ------------------------------------------------------------------
        if re.search(
            r'perr(o|ito)|gat(o|ico)|mascota|animal',
            comment_lower
        ):
            return 'Tema: Animales'

        # ------------------------------------------------------------------
        # 14. Ruido / Spam (Filtro Mejorado)
        # ------------------------------------------------------------------
        is_spam_pattern = re.search(
            r'tinga linga|'      # Patrón específico spam
            r'[pP]+0*9+|'        # Secuencias tipo Pp099, p99
            r'^[0-9]+$|'         # Solo números (ej: "6")
            r'(.)\1{4,}|'        # Letras repetidas mas de 4 veces (vuuuuuu)
            r'^jajaj?a?+$|'      # Solo risas sin texto
            r'^hola$|'           # Saludos vacíos
            r'emoji|🤡|'        # Emojis ofensivos solos
            r'%%%%|'             # Caracteres especiales solos
            r'^[a-zA-Z]$',       # Una sola letra (ej: "P")
            comment_lower
        )
        
        if is_spam_pattern:
            return 'Ruido / Spam'
        
        # Palabras muy cortas que NO son spam
        valid_shorts = ['ty', 'si', 'no', 'ok', 'top', 'wow']
        if comment_lower in valid_shorts:
             return 'Aprobación General / Brand Love' if comment_lower in ['ty', 'top', 'wow'] else 'Otros / Neutro'

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
