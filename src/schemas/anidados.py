"""
Schemas con datos ANIDADOS (un schema dentro de otro).

Viven en un archivo aparte porque se referencian mutuamente
(artículo -> categoría y categoría -> artículos) y así evitamos imports circulares.
"""
from sqlmodel import Field

from src.schemas.articulos import ArticuloResumen
from src.schemas.categorias import CategoriaResponse


class ArticuloConCategoria(ArticuloResumen):
    """Artículo con su categoría anidada como objeto: { ..., "categoria": {...} }"""

    categoria: CategoriaResponse


class CategoriaConArticulos(CategoriaResponse):
    """Categoría con la lista de sus artículos anidada: { ..., "articulos": [...] }"""

    articulos: list[ArticuloResumen] = Field(default_factory=list)
