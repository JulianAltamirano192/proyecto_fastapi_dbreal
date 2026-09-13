# API de Artículos — TP Evaluativo PP1 Python

Proyecto desarrollado con **FastAPI** para el TP Evaluativo de PP1 - Python (ITEC Río Cuarto).

## Estructura del proyecto

```
proyecto_fastapi/
├── requirements.txt
└── src/
    ├── main.py              # Punto de entrada
    ├── schemas/
    │   └── articulos.py     # Modelos de Pydantic (ArticuloEdit, ArticuloResponse)
    └── routers/
        └── articulos.py     # Path operations (CRUD)
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

   (Esto instala `fastapi[standard]`, que incluye `uvicorn` y demás extras.)

## Ejecución

Desde la **raíz del proyecto** (donde está `requirements.txt`, al mismo nivel que `src/`):

```bash
fastapi dev src/main.py
```

o alternativamente:

```bash
uvicorn src.main:app --reload
```

## Documentación interactiva

Una vez levantado el servidor, abrir en el navegador:

- Swagger UI: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc

## Endpoints disponibles

| Método | Ruta                    | Descripción                              |
|--------|--------------------------|-------------------------------------------|
| POST   | `/articulos/`            | Crear un nuevo artículo                  |
| GET    | `/articulos/`             | Listar artículos (filtros: `categoria`, `limite`) |
| GET    | `/articulos/{articulo_id}` | Obtener un artículo por id (404 si no existe) |
| PUT    | `/articulos/{articulo_id}` | Actualizar un artículo (404 si no existe) |
| DELETE | `/articulos/{articulo_id}` | Eliminar un artículo (404 si no existe) |

## Notas sobre el cumplimiento de la consigna

- **CORS**: configurado en `main.py` para permitir la conexión con el front del TP01 de PP1 - JavaScript (orígenes de `localhost` típicos de Vite/Live Server).
- **Modelos Pydantic**: `ArticuloEdit` (sin `id`, usado para crear/editar) y `ArticuloResponse` (con `id`, usado como `response_model`). Todos los campos usan `Annotated` + `Field()` con metadatos.
- **"Tabla" simulada**: lista `db_articulos` en `routers/articulos.py`, validada con `ArticuloResponse` (id + 3 campos: `nombre`, `precio`, `categoria`).
- **5 Path operations** en `routers/articulos.py`: 1 create, 2 read (listado + por id), 1 update, 1 delete.
- **Parámetros tipados**: `Path()` para `articulo_id`, `Query()` para los filtros del listado.
- **Errores 404**: se documentan en `/docs` mediante el parámetro `responses` de cada path operation y se levantan con `HTTPException`.
