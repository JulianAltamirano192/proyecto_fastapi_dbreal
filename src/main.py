from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import Base, engine
from src.models import articulo  
from src.routers import articulos

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Artículos - TP Evaluativo PP1 Python",
    description="API desarrollada con FastAPI para el TP Evaluativo de PP1 - Python (ITEC Río Cuarto).",
    version="2.0.0",
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(articulos.router)


@app.get("/", tags=["Root"])
def read_root():
    return {"mensaje": "API de Artículos funcionando correctamente. Visitar /docs para la documentación."}