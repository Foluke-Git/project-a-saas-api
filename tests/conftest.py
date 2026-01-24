import sys
from pathlib import Path
import os
import pytest
from fastapi.testclient import TestClient

from alembic import command
from alembic.config import Config

# Add project root to PYTHONPATH so `import app...` works
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

def run_migrations():
    """
    Apply Alembic migrations to the test database.
    """
    # Alembic reads alembic.ini from project root
    alembic_cfg = Config(str(ROOT / "alembic.ini"))

    # Setting Alembic script location (so it always finds migrations)
    alembic_cfg.set_main_option("script_location", str(ROOT / "alembic"))

    # Important: ensure alembic uses the test DB URL
    alembic_cfg.set_main_option("sqlalchemy.url", os.environ["DATABASE_URL"])

    os.environ["DATABASE_URL"] = (
        "postgresql+psycopg://postgres:postgres@localhost:5433/saas_test_db"
        "?connect_timeout=3"
    )

    # Upgrade to latest migration
    command.upgrade(alembic_cfg, "head")


# IMPORTANT:
# We set env vars BEFORE importing app, so settings read the test DB URL.
@pytest.fixture(scope="session", autouse=True)
def _set_test_env():
    os.environ["DATABASE_URL"] = "postgresql+psycopg://postgres:postgres@localhost:5433/saas_test_db"
    os.environ["JWT_SECRET_KEY"] = "test-secret"
    os.environ["JWT_ALGORITHM"] = "HS256"
    os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "60"

    run_migrations()


@pytest.fixture(scope="session")
def client():
    # Import app AFTER env vars set
    from app.main import app

    with TestClient(app) as c:
        yield c
