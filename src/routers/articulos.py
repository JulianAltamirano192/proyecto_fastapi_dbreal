from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.articulo import Articulo
from src.schemas.articulos import ArticuloEdit, ArticuloResponse

router = APIRouter(
    prefix="/articulos",
    tags=["Artículos"],
)


def _buscar_articulo(articulo_id: int, db: Session) -> Articulo:
    # Busca un artículo por ID en la base de datos o retorna 404.
    articulo = db.get(Articulo, articulo_id)
    if articulo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un artículo con id {articulo_id}",
        )
    return articulo


@router.post(
    "/",
    response_model=ArticuloResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo artículo",
)
def crear_articulo(articulo: ArticuloEdit, db: Session = Depends(get_db)) -> Articulo:
    nuevo_articulo = Articulo(**articulo.model_dump())
    db.add(nuevo_articulo)
    db.commit()
    db.refresh(nuevo_articulo)
    return nuevo_articulo


@router.get(
    "/",
    response_model=list[ArticuloResponse],
    summary="Listar artículos",
)
def listar_articulos(
    categoria: Annotated[
        str | None,
        Query(
            min_length=2,
            max_length=30,
            description="Filtra los artículos por categoría (búsqueda exacta).",
        ),
    ] = None,
    limite: Annotated[
        int,
        Query(
            gt=0,
            le=100,
            description="Cantidad máxima de artículos a devolver.",
        ),
    ] = 10,
    db: Session = Depends(get_db),
) -> list[Articulo]:
    query = db.query(Articulo)
    if categoria is not None:
        query = query.filter(Articulo.categoria.ilike(categoria))
    return query.limit(limite).all()


@router.get(
    "/{articulo_id}",
    response_model=ArticuloResponse,
    summary="Obtener un artículo por id",
    responses={404: {"description": "Artículo no encontrado"}},
)
def obtener_articulo(
    articulo_id: Annotated[
        int,
        Path(gt=0, description="Id del artículo que se quiere obtener."),
    ],
    db: Session = Depends(get_db),
) -> Articulo:
    return _buscar_articulo(articulo_id, db)


@router.put(
    "/{articulo_id}",
    response_model=ArticuloResponse,
    summary="Actualizar un artículo existente",
    responses={404: {"description": "Artículo no encontrado"}},
)
def actualizar_articulo(
    articulo_id: Annotated[
        int,
        Path(gt=0, description="Id del artículo que se quiere actualizar."),
    ],
    datos: ArticuloEdit,
    db: Session = Depends(get_db),
) -> Articulo:
    articulo_existente = _buscar_articulo(articulo_id, db)
    articulo_existente.nombre = datos.nombre
    articulo_existente.precio = datos.precio
    articulo_existente.categoria = datos.categoria
    db.commit()
    db.refresh(articulo_existente)
    return articulo_existente


@router.delete(
    "/{articulo_id}",
    response_model=ArticuloResponse,
    summary="Eliminar un artículo",
    responses={404: {"description": "Artículo no encontrado"}},
)
def eliminar_articulo(
    articulo_id: Annotated[
        int,
        Path(gt=0, description="Id del artículo que se quiere eliminar."),
    ],
    db: Session = Depends(get_db),
) -> Articulo:
    articulo = _buscar_articulo(articulo_id, db)
    db.delete(articulo)
    db.commit()
    return articulo