from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlmodel import Session, select

from src.database import get_session
from src.models.articulo import Articulo
from src.models.categoria import Categoria
from src.schemas.anidados import ArticuloConCategoria
from src.schemas.articulos import ArticuloEdit

router = APIRouter(
    prefix="/articulos",
    tags=["Artículos"],
)


def _buscar_articulo(articulo_id: int, session: Session) -> Articulo:
    articulo = session.get(Articulo, articulo_id)
    if articulo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un artículo con id {articulo_id}",
        )
    return articulo


def _validar_categoria(categoria_id: int, session: Session) -> None:
    # Evita violar la Foreign Key: avisamos con un error claro en vez de un 500.
    if session.get(Categoria, categoria_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe la categoría con id {categoria_id}",
        )


@router.post(
    "/",
    response_model=ArticuloConCategoria,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo artículo",
    responses={404: {"description": "La categoría indicada no existe"}},
)
def crear_articulo(
    datos: ArticuloEdit, session: Session = Depends(get_session)
) -> Articulo:
    _validar_categoria(datos.categoria_id, session)
    nuevo = Articulo.model_validate(datos)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo


@router.get(
    "/",
    response_model=list[ArticuloConCategoria],
    summary="Listar artículos",
)
def listar_articulos(
    categoria: Annotated[
        str | None,
        Query(
            min_length=2,
            max_length=30,
            description="Filtra los artículos por nombre de categoría (búsqueda exacta, sin distinguir mayúsculas).",
        ),
    ] = None,
    limite: Annotated[
        int,
        Query(gt=0, le=100, description="Cantidad máxima de artículos a devolver."),
    ] = 10,
    session: Session = Depends(get_session),
) -> list[Articulo]:
    consulta = select(Articulo)
    if categoria is not None:
        consulta = consulta.join(Categoria).where(Categoria.nombre.ilike(categoria))
    return list(session.exec(consulta.limit(limite)).all())


@router.get(
    "/{articulo_id}",
    response_model=ArticuloConCategoria,
    summary="Obtener un artículo por id",
    responses={404: {"description": "Artículo no encontrado"}},
)
def obtener_articulo(
    articulo_id: Annotated[int, Path(gt=0, description="Id del artículo que se quiere obtener.")],
    session: Session = Depends(get_session),
) -> Articulo:
    return _buscar_articulo(articulo_id, session)


@router.put(
    "/{articulo_id}",
    response_model=ArticuloConCategoria,
    summary="Actualizar un artículo existente",
    responses={404: {"description": "Artículo o categoría no encontrados"}},
)
def actualizar_articulo(
    articulo_id: Annotated[int, Path(gt=0, description="Id del artículo que se quiere actualizar.")],
    datos: ArticuloEdit,
    session: Session = Depends(get_session),
) -> Articulo:
    articulo = _buscar_articulo(articulo_id, session)
    _validar_categoria(datos.categoria_id, session)
    articulo.sqlmodel_update(datos.model_dump())
    session.add(articulo)
    session.commit()
    session.refresh(articulo)
    return articulo


@router.delete(
    "/{articulo_id}",
    response_model=ArticuloConCategoria,
    summary="Eliminar un artículo",
    responses={404: {"description": "Artículo no encontrado"}},
)
def eliminar_articulo(
    articulo_id: Annotated[int, Path(gt=0, description="Id del artículo que se quiere eliminar.")],
    session: Session = Depends(get_session),
) -> Articulo:
    articulo = _buscar_articulo(articulo_id, session)
    _ = articulo.categoria  # cargamos la categoría antes de borrar, para poder devolverla anidada
    session.delete(articulo)
    session.commit()
    return articulo
