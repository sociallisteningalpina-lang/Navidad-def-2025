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
    Retorna una función de clasificación de temas personalizada para
    la campaña de Navidad de Alpina.
    """
    
    def classify_topic(comment: str) -> str:
        comment_lower = str(comment).lower()
        
        # CATEGORÍA 1: Opinión positiva del producto / campaña
        if re.search(
            r'\bme gusta\b|lindo|hermos[oa]|bonito|delicia|delicioso|'
            r'encanta|muy bueno|🥰|😊|❤️|que bello|que bonito|'
            r'me gusta que no es ia',
            comment_lower
        ):
            return 'Opinión Positiva del Producto'
        
        # CATEGORÍA 2: Opinión negativa del producto
        if re.search(
            r'mala|p[eé]simo|feo|horrible|sabor a|'
            r'pura agua|cambi[oó] mucho|no sirve|vomit|🤢',
            comment_lower
        ):
            return 'Opinión Negativa del Producto'
        
        # CATEGORÍA 3: Precio y accesibilidad
        if re.search(
            r'costoso|caro|vale la pena|atraco|'
            r'por las nubes|\bprecio\b|\b$|c[uú]anto vale',
            comment_lower
        ):
            return 'Precio y Accesibilidad'
        
        # CATEGORÍA 4: Nostalgia / pasado
        if re.search(
            r'infancia|antes|cuando eran|noventa|90|'
            r'tra[ií]an m[aá]s|como los de mi infancia|producto de los 90',
            comment_lower
        ):
            return 'Nostalgia / Pasado'
        
        # CATEGORÍA 5: Religioso / bendiciones
        if re.search(
            r'am[eé]n|amen|bendiga|bendiciones|gracias señor',
            comment_lower
        ):
            return 'Religioso'
        
        # CATEGORÍA 6: Política
        if re.search(
            r'petro|urib|ultraderecha|corrupci[oó]n|pa[ií]s',
            comment_lower
        ):
            return 'Política'
        
        # CATEGORÍA 7: Insultos / ataques
        if re.search(
            r'verg[uü]enza|aprovechado|ambicioso|viejo|cacorro|'
            r'insulto|imb[eé]cil|idiota',
            comment_lower
        ):
            return 'Insultos / Ataques'
        
        # CATEGORÍA 8: Fuera de tema / aleatorio / spam
        if (
            re.search(
                r'tinga linga|pp\d+|hola te ves bn|gracias|emoji|☺️|'
                r'jajaja|jaja|tuuu|sin sentido|spam',
                comment_lower
            )
            or len(comment_lower.split()) < 3
        ):
            return 'Fuera de Tema / No Relevante'
        
        # CATEGORÍA 9: Solicitudes o preguntas
        if re.search(
            r'por qu[eé]|c[oó]mo se|explique|qu[eé] ingredientes|'
            r'puedo|d[oó]nde|pregunta|ayuda',
            comment_lower
        ):
            return 'Preguntas / Solicitudes'
        
        # CATEGORÍA 10: Apariencia / halagos personales
        if re.search(
            r'te ves bien|buena imagen|bonit[oa] persona|guap[oa]',
            comment_lower
        ):
            return 'Apariencia / Halagos'
        
        # CATEGORÍA 11: Mascotas / animales
        if re.search(
            r'perritos|mascotas|gatos|perros|polic[ií]a.*perritos',
            comment_lower
        ):
            return 'Mascotas / Animales'
        
        # DEFAULT
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
