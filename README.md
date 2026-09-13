# API de Artículos — TP4 PP1 Python (Integración con SQLAlchemy)

Proyecto desarrollado con **FastAPI** y **SQLAlchemy** para el TP4 de PP1 - Python (ITEC Río Cuarto).

Parte del TP Evaluativo anterior, que usaba un CRUD en memoria, y ahora persiste los datos
en una base de datos real (**SQLite**) usando SQLAlchemy como ORM.

## Estructura del proyecto

proyecto_fastapi/
├── requirements.txt
├── .gitignore
└── src/
├── main.py # Punto de entrada, crea las tablas al arrancar
├── database.py # Configuración de SQLAlchemy: engine, SessionLocal, get_db
├── models/
│ └── articulo.py # Modelo ORM (tabla "articulos")
├── schemas/
│ └── articulos.py # Modelos de Pydantic (ArticuloEdit, ArticuloResponse)
└── routers/
└── articulos.py # Path operations (CRUD) sobre la base de datos real

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

   (Esto instala `fastapi[standard]`, `SQLAlchemy` y demás dependencias.)

## Ejecución

Desde la **raíz del proyecto** (donde está `requirements.txt`, al mismo nivel que `src/`):

```bash
fastapi dev src/main.py
```

o alternativamente:

```bash
uvicorn src.main:app --reload
```

Al arrancar por primera vez se crea automáticamente el archivo `articulos.db` (SQLite)
en la raíz del proyecto, junto con la tabla `articulos`.

## Documentación interactiva

Una vez levantado el servidor, abrir en el navegador:

- Swagger UI: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc

## Endpoints disponibles

| Método | Ruta                        | Descripción                                        |
|--------|------------------------------|-----------------------------------------------------|
| POST   | `/articulos/`                | Crear un nuevo artículo (persiste en SQLite)        |
| GET    | `/articulos/`                | Listar artículos (filtros: `categoria`, `limite`)   |
| GET    | `/articulos/{articulo_id}`   | Obtener un artículo por id (404 si no existe)       |
| PUT    | `/articulos/{articulo_id}`   | Actualizar un artículo (404 si no existe)           |
| DELETE | `/articulos/{articulo_id}`   | Eliminar un artículo (404 si no existe)             |

## Notas sobre el cumplimiento de la consigna (TP4)

- **SQLAlchemy en requirements**: `SQLAlchemy==2.0.36` en `requirements.txt`.
- **`database.py`**: define `engine` (SQLite, `check_same_thread=False`), `SessionLocal`
  (sessionmaker) y `get_db()` como dependencia inyectable con `Depends()`.
- **Modelo**: `Articulo` en `src/models/articulo.py`, mapeado a la tabla `articulos`
  (`id`, `nombre`, `precio`, `categoria`).
- **CRUD real**: los 5 path operations en `routers/articulos.py` ya no usan una lista en
  memoria — cada uno abre una `Session` vía `Depends(get_db)` y hace `db.add()`,
  `db.query()`, `db.get()`, `db.commit()`, `db.delete()`, según corresponda.
- **Schemas Pydantic**: `ArticuloResponse` usa `model_config = ConfigDict(from_attributes=True)`
  para poder construirse directamente desde un objeto SQLAlchemy.
- **Errores 404**: se levantan con `HTTPException` cuando el `articulo_id` no existe en la DB.