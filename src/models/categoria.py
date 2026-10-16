from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.articulo import Articulo


class Categoria(SQLModel, table=True):
    """Tabla 'categorias'. Una categoría tiene muchos artículos (1 -> N)."""

    __tablename__ = "categorias"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=30, unique=True, index=True)
    descripcion: str | None = Field(default=None, max_length=200)

    articulos: list["Articulo"] = Relationship(back_populates="categoria")
