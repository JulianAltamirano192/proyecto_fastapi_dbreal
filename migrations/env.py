from logging.config import fileConfig

from alembic import context

# Usamos el mismo engine y los mismos modelos que la aplicación,
# así la API y las migraciones siempre apuntan a la misma base de datos.
from sqlmodel import SQLModel

from src.database import DATABASE_URL, engine
import src.models  # noqa: F401  (registra Categoria y Articulo en SQLModel.metadata)

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata de SQLModel: de acá Alembic compara el estado de los modelos vs. la DB
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Modo 'offline': genera el SQL sin conectarse a la DB (alembic upgrade head --sql)."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,  # SQLite no soporta ALTER TABLE completo -> modo batch
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Modo 'online': se conecta a la DB y aplica las migraciones."""
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,  # SQLite no soporta ALTER TABLE completo -> modo batch
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
