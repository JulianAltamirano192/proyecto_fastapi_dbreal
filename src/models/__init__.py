# Importar todos los modelos acá asegura que queden registrados en SQLModel.metadata
# (lo necesita Alembic para autogenerar migraciones).
from src.models.categoria import Categoria
from src.models.articulo import Articulo

__all__ = ["Categoria", "Articulo"]
