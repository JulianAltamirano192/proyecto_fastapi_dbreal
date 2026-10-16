from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlmodel import Session, select

from src.database import get_session
from src.models.categoria import Categoria
from src.schemas.anidados import CategoriaConArticulos
from src.schemas.categorias import CategoriaEdit, CategoriaResponse

router = APIRouter(
    prefix="/categorias",
    tags=["Categorías"],
)


def _buscar_categoria(categoria_id: int, session: Session) -> Categoria:
    categoria = session.get(Categoria, categoria_id)
    if categoria is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una categoría con id {categoria_id}",
        )
    return categoria


def _validar_nombre_unico(nombre: str, session: Session, excluir_id: int | None = None) -> None:
    existente = session.exec(select(Categoria).where(Categoria.nombre == nombre)).first()
    if existente is not None and existente.id != excluir_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe una categoría llamada '{nombre}'",
        )


@router.post(
    "/",
    response_model=CategoriaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva categoría",
    responses={409: {"description": "Ya existe una categoría con ese nombre"}},
)
def crear_categoria(
    datos: CategoriaEdit, session: Session = Depends(get_session)
) -> Categoria:
    _validar_nombre_unico(datos.nombre, session)
    nueva = Categoria.model_validate(datos)
    session.add(nueva)
    session.commit()
    session.refresh(nueva)
    return nueva


@router.get(
    "/",
    response_model=list[CategoriaResponse],
    summary="Listar categorías",
)
def listar_categorias(session: Session = Depends(get_session)) -> list[Categoria]:
    return list(session.exec(select(Categoria)).all())


@router.get(
    "/{categoria_id}",
    response_model=CategoriaConArticulos,
    summary="Obtener una categoría con sus artículos (datos anidados)",
    responses={404: {"description": "Categoría no encontrada"}},
)
def obtener_categoria(
    categoria_id: Annotated[int, Path(gt=0, description="Id de la categoría.")],
    session: Session = Depends(get_session),
) -> Categoria:
    return _buscar_categoria(categoria_id, session)


@router.put(
    "/{categoria_id}",
    response_model=CategoriaResponse,
    summary="Actualizar una categoría existente",
    responses={
        404: {"description": "Categoría no encontrada"},
        409: {"description": "Ya existe una categoría con ese nombre"},
    },
)
def actualizar_categoria(
    categoria_id: Annotated[int, Path(gt=0, description="Id de la categoría.")],
    datos: CategoriaEdit,
    session: Session = Depends(get_session),
) -> Categoria:
    categoria = _buscar_categoria(categoria_id, session)
    _validar_nombre_unico(datos.nombre, session, excluir_id=categoria_id)
    categoria.sqlmodel_update(datos.model_dump())
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


@router.delete(
    "/{categoria_id}",
    response_model=CategoriaResponse,
    summary="Eliminar una categoría (solo si no tiene artículos)",
    responses={
        404: {"description": "Categoría no encontrada"},
        409: {"description": "La categoría todavía tiene artículos asociados"},
    },
)
def eliminar_categoria(
    categoria_id: Annotated[int, Path(gt=0, description="Id de la categoría.")],
    session: Session = Depends(get_session),
) -> Categoria:
    categoria = _buscar_categoria(categoria_id, session)
    if categoria.articulos:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar una categoría que tiene artículos asociados",
        )
    session.delete(categoria)
    session.commit()
    return categoria
