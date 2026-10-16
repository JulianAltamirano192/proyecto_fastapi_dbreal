from sqlmodel import Session, create_engine

DATABASE_URL = "sqlite:///./articulos.db"

# check_same_thread=False es necesario porque FastAPI atiende requests desde varios threads
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def get_session():
    """Dependencia inyectable: abre una Session por request y la cierra al terminar."""
    with Session(engine) as session:
        yield session
