from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field


class ArticuloEdit(BaseModel):
    """
    Schema usado para las vistas de edición (create / update).
    No incluye 'id' porque ese valor lo genera/administra el servidor.
    """
    nombre: Annotated[
        str,
        Field(
            min_length=2,
            max_length=50,
            description="Nombre del artículo",
            examples=["Teclado mecánico"],
        ),
    ]
    precio: Annotated[
        float,
        Field(
            gt=0,
            description="Precio del artículo en pesos. Debe ser mayor a 0.",
            examples=[15999.99],
        ),
    ]
    categoria: Annotated[
        str,
        Field(
            min_length=2,
            max_length=30,
            description="Categoría a la que pertenece el artículo",
            examples=["Periféricos"],
        ),
    ]


class ArticuloResponse(ArticuloEdit):
    """
    Schema usado para las respuestas generales.
    Hereda los campos de ArticuloEdit y agrega el 'id'.
    model_config con from_attributes=True permite construir este schema
    directamente desde un objeto SQLAlchemy (la clase Articulo del ORM).
    """
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[
        int,
        Field(
            description="Identificador único del artículo",
            examples=[1],
        ),
    ]