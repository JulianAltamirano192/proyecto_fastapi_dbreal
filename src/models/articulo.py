from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.categoria import Categoria


class Articulo(SQLModel, table=True):
    """Tabla 'articulos'. Cada artículo pertenece a una categoría (FK -> categorias.id)."""

    __tablename__ = "articulos"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50)
    precio: float
    categoria_id: int = Field(foreign_key="categorias.id", index=True)

    categoria: "Categoria" = Relationship(back_populates="articulos")
