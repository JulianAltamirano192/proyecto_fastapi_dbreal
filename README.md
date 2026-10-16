# API de Artículos — TP5 PP1 Python (SQLModel + Alembic)

Proyecto desarrollado con **FastAPI**, **SQLModel** y **Alembic** para el TP5 de PP1 - Python (ITEC Río Cuarto).

Parte del TP4 (FastAPI + SQLAlchemy) y lo actualiza con:

- **SQLModel** en lugar de SQLAlchemy (modelos, sesiones y consultas).
- **Alembic** para versionar el esquema de la base de datos (migraciones).
- **2 modelos relacionados** por Foreign Key: `Categoria` (1) → (N) `Articulo`.
- **Schemas anidados**: el artículo devuelve su categoría embebida y la categoría devuelve sus artículos.

## Estructura del proyecto

```
proyecto_fastapi/
├── alembic.ini                  # Configuración de Alembic
├── requirements.txt
├── .gitignore
├── migrations/
│   ├── env.py                   # Conecta Alembic con el engine y los modelos de SQLModel
│   ├── script.py.mako           # Plantilla de migraciones (importa sqlmodel)
│   └── versions/
│       └── ..._migracion_inicial_categorias_y_articulos.py   # Migración inicial
└── src/
    ├── main.py                  # Punto de entrada (ya NO crea tablas: eso lo hace Alembic)
    ├── database.py              # engine de SQLModel + dependencia get_session
    ├── models/                  # Tablas (SQLModel con table=True)
    │   ├── categoria.py         #   Categoria  -> tabla "categorias"
    │   └── articulo.py          #   Articulo   -> tabla "articulos" (FK categoria_id)
    ├── schemas/                 # Schemas de entrada/salida (SQLModel sin table=True)
    │   ├── categorias.py        #   CategoriaEdit, CategoriaResponse
    │   ├── articulos.py         #   ArticuloEdit, ArticuloResumen
    │   └── anidados.py          #   ArticuloConCategoria, CategoriaConArticulos
    └── routers/
        ├── categorias.py        # CRUD de categorías
        └── articulos.py         # CRUD de artículos
```

## Instalación

1. Crear y activar un entorno virtual:

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux / Mac:
source venv/bin/activate
```

2. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Base de datos y migraciones (Alembic)

Las tablas **no se crean al arrancar la app**. Antes de levantar el servidor por primera vez
hay que aplicar las migraciones (desde la raíz del proyecto):

```bash
alembic upgrade head
```

Esto crea el archivo `articulos.db` (SQLite) con las tablas `categorias`, `articulos` y `alembic_version`.

> Si venís del TP4 y tenés un `articulos.db` viejo (con la columna `categoria` como texto),
> borralo antes de correr `alembic upgrade head`: el esquema cambió.

Comandos útiles:

| Comando | Para qué sirve |
|---|---|
| `alembic upgrade head` | Aplica todas las migraciones pendientes |
| `alembic downgrade -1` | Revierte la última migración |
| `alembic downgrade base` | Revierte todas (deja la DB sin tablas) |
| `alembic current` | Muestra la versión actual de la DB |
| `alembic history` | Lista las migraciones |
| `alembic revision --autogenerate -m "mensaje"` | Genera una nueva migración comparando los modelos con la DB |
| `alembic check` | Verifica que los modelos y la DB estén sincronizados |

**Flujo para cambiar el esquema:** modificar el modelo en `src/models/` → `alembic revision --autogenerate -m "..."`
→ revisar el archivo generado en `migrations/versions/` → `alembic upgrade head`.

> Si se agrega un modelo nuevo, hay que importarlo en `src/models/__init__.py`
> para que Alembic lo detecte.

## Ejecución

```bash
fastapi dev src/main.py
```

o alternativamente:

```bash
uvicorn src.main:app --reload
```

## Documentación interactiva

- Swagger UI: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc

## Endpoints disponibles

### Categorías (`/categorias`)

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST   | `/categorias/` | Crear una categoría (409 si el nombre ya existe) |
| GET    | `/categorias/` | Listar categorías |
| GET    | `/categorias/{categoria_id}` | Obtener una categoría **con sus artículos anidados** (404 si no existe) |
| PUT    | `/categorias/{categoria_id}` | Actualizar una categoría (404 / 409) |
| DELETE | `/categorias/{categoria_id}` | Eliminar una categoría (409 si todavía tiene artículos) |

### Artículos (`/articulos`)

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST   | `/articulos/` | Crear un artículo (404 si la `categoria_id` no existe) |
| GET    | `/articulos/` | Listar artículos (filtros: `categoria` por nombre, `limite`) |
| GET    | `/articulos/{articulo_id}` | Obtener un artículo **con su categoría anidada** (404 si no existe) |
| PUT    | `/articulos/{articulo_id}` | Actualizar un artículo (404 si no existe el artículo o la categoría) |
| DELETE | `/articulos/{articulo_id}` | Eliminar un artículo (404 si no existe) |

### Ejemplo de uso

```bash
# 1) Crear una categoría
curl -X POST http://127.0.0.1:8000/categorias/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Periféricos", "descripcion": "Teclados y mouses"}'

# 2) Crear un artículo que apunta a esa categoría (FK)
curl -X POST http://127.0.0.1:8000/articulos/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Teclado mecánico", "precio": 15999.99, "categoria_id": 1}'
```

Respuesta de `GET /articulos/1` (categoría **anidada**):

```json
{
  "id": 1,
  "nombre": "Teclado mecánico",
  "precio": 15999.99,
  "categoria_id": 1,
  "categoria": { "id": 1, "nombre": "Periféricos", "descripcion": "Teclados y mouses" }
}
```

Respuesta de `GET /categorias/1` (artículos **anidados**):

```json
{
  "id": 1,
  "nombre": "Periféricos",
  "descripcion": "Teclados y mouses",
  "articulos": [
    { "id": 1, "nombre": "Teclado mecánico", "precio": 15999.99, "categoria_id": 1 }
  ]
}
```

## Notas sobre el cumplimiento de la consigna (TP5)

- **Solo SQLModel**: `requirements.txt` ya no lista SQLAlchemy y el código de `src/` no lo importa;
  se usan `SQLModel`, `Field`, `Relationship`, `Session`, `create_engine` y `select` de `sqlmodel`.
  (SQLAlchemy sigue instalado como dependencia interna de SQLModel/Alembic, y los archivos
  de migración que genera Alembic usan `import sqlalchemy as sa` por diseño de la herramienta.)
- **Alembic**: configurado en `migrations/env.py` con `SQLModel.metadata` como `target_metadata`
  y `render_as_batch=True` (necesario para modificar tablas en SQLite). Incluye la migración inicial
  `migracion_inicial_categorias_y_articulos`, con `upgrade()` y `downgrade()`.
- **Modelos y Foreign Key**: `Categoria` y `Articulo`. `Articulo.categoria_id` es una FK a `categorias.id`
  y ambos modelos se vinculan con `Relationship` (`back_populates`).
  Como SQLite no hace cumplir las FK por defecto, la API valida que la categoría exista antes de
  guardar (404) y no deja borrar categorías con artículos (409).
- **Schemas anidados** (`src/schemas/anidados.py`): `ArticuloConCategoria` (tiene un campo
  `categoria: CategoriaResponse`) y `CategoriaConArticulos` (tiene `articulos: list[ArticuloResumen]`).
- **Separación tabla / schema**: los modelos con `table=True` son las tablas; los schemas
  son clases `SQLModel` sin `table=True`, por lo que se validan como Pydantic pero no crean tablas.
