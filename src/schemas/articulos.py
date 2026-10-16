from sqlmodel import Field, SQLModel


class ArticuloEdit(SQLModel):
    """
    Schema para crear / actualizar artículos.
    No incluye 'id' (lo genera la DB). La categoría se referencia por 'categoria_id' (FK).
    """

    nombre: str = Field(
        min_length=2,
        max_length=50,
        description="Nombre del artículo",
        schema_extra={"examples": ["Teclado mecánico"]},
    )
    precio: float = Field(
        gt=0,
        description="Precio del artículo en pesos. Debe ser mayor a 0.",
        schema_extra={"examples": [15999.99]},
    )
    categoria_id: int = Field(
        gt=0,
        description="Id de la categoría a la que pertenece el artículo",
        schema_extra={"examples": [1]},
    )


class ArticuloResumen(SQLModel):
    """Artículo 'plano' (sin categoría). Se usa anidado dentro de CategoriaConArticulos."""

    id: int = Field(description="Identificador único del artículo", schema_extra={"examples": [1]})
    nombre: str
    precio: float
    categoria_id: int
