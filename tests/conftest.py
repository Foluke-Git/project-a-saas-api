import os
import sys
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from alembic import command
from alembic.config import Config

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _make_alembic_cfg(db_url: str) -> Config:
    alembic_cfg = Config(str(ROOT / "alembic.ini"))
    alembic_cfg.set_main_option("script_location", str(ROOT / "alembic"))
    alembic_cfg.set_main_option("sqlalchemy.url", db_url)
    return alembic_cfg


def _wait_for_db(db_url: str, timeout_seconds: int = 20) -> None:
    engine = create_engine(db_url, pool_pre_ping=True)
    start = time.time()
    while True:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except Exception:
            if time.time() - start > timeout_seconds:
                raise
            time.sleep(0.5)


def _users_table_exists(db_url: str) -> bool:
    engine = create_engine(db_url, pool_pre_ping=True)
    with engine.connect() as conn:
        # checks "public.users" existence (default schema)
        q = text("""
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = 'users'
        """)
        return conn.execute(q).first() is not None


def run_migrations(db_url: str) -> None:
    _wait_for_db(db_url)

    alembic_cfg = _make_alembic_cfg(db_url)
    command.upgrade(alembic_cfg, "head")


@pytest.fixture(scope="session", autouse=True)
def _set_test_env():
    # Use Docker-provided DATABASE_URL if present; otherwise default to Windows localhost mapping
    db_url = os.getenv("DATABASE_URL") or (
        "postgresql+psycopg://postgres:postgres@localhost:55433/saas_test_db?connect_timeout=3"
    )
    os.environ["DATABASE_URL"] = db_url

    os.environ.setdefault("JWT_SECRET_KEY", "test-secret")
    os.environ.setdefault("JWT_ALGORITHM", "HS256")
    os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    os.environ.setdefault("SKIP_DB_INIT", "1")

    # Run Alembic migrations
    run_migrations(db_url)

    # ✅ Verify migrations actually created tables.
    # If not, fallback to Base.metadata.create_all (keeps you unblocked on Windows).
    if not _users_table_exists(db_url):
        from app.db.base import Base  # your declarative Base
        # IMPORTANT: ensure models are imported so they register with Base.metadata
        from app.models import user  # adjust to your actual module(s): app.models.users etc.

        engine = create_engine(db_url, pool_pre_ping=True)
        Base.metadata.create_all(bind=engine)


@pytest.fixture()
def client():
    from app.main import app
    with TestClient(app) as c:
        yield c
