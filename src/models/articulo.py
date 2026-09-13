from sqlalchemy import Column, Integer, String, Float
from src.database import Base

class Articulo(Base):
    __tablename__ = "articulos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    precio = Column(Float, nullable=False)
    categoria = Column(String(30), nullable=False, index=True)