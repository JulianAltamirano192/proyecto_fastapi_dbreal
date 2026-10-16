from sqlmodel import Field, SQLModel


class CategoriaEdit(SQLModel):
    """Schema para crear / actualizar categorías. No incluye 'id' (lo genera la DB)."""

    nombre: str = Field(
        min_length=2,
        max_length=30,
        description="Nombre de la categoría (único)",
        schema_extra={"examples": ["Periféricos"]},
    )
    descripcion: str | None = Field(
        default=None,
        max_length=200,
        description="Descripción opcional de la categoría",
        schema_extra={"examples": ["Teclados, mouses y otros accesorios"]},
    )


class CategoriaResponse(CategoriaEdit):
    """Respuesta simple de una categoría (sin sus artículos)."""

    id: int = Field(description="Identificador único de la categoría", schema_extra={"examples": [1]})
