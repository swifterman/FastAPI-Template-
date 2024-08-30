from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import importlib
import os
os.environ["ALEMBIC_RUN_MIGRATION"] = "true"


# Import your models here
from database.database import Base
from api.user_management.models import User
from api.payment.models import Payment

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# Set up target metadata from all your models
target_metadata = Base.metadata


def import_all_models(package_names):
    import pkgutil
    import sys

    for package_name in package_names:
        if package_name not in sys.modules:
            importlib.import_module(package_name)
        package = sys.modules[package_name]
        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            importlib.import_module(f"{package_name}.{module_name}")


# Import all models from the models package
import_all_models(['api.user_management', 'api.payment'])


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
