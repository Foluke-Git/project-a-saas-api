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


def _wait_for_db(db_url: str, timeout_seconds: int = 30) -> None:
    engine = create_engine(db_url, pool_pre_ping=True)
    start = time.time()
    last_exc = None
    while time.time() - start < timeout_seconds:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except Exception as e:
            last_exc = e
            time.sleep(0.5)
    raise RuntimeError(f"DB not reachable within {timeout_seconds}s: {last_exc!r}")


def _reset_schema(db_url: str) -> None:
    """
    Make the database deterministic for every test session.
    This avoids "Can't locate revision ..." and stale tables.
    """
    engine = create_engine(db_url, pool_pre_ping=True)
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))


def _run_migrations(db_url: str) -> None:
    alembic_cfg = _make_alembic_cfg(db_url)
    command.upgrade(alembic_cfg, "head")


@pytest.fixture(scope="session", autouse=True)
def _set_test_env():
    # If CI/docker provides DATABASE_URL, use it. Otherwise default to Windows mapping.
    db_url = os.getenv("DATABASE_URL") or (
        "postgresql+psycopg://postgres:postgres@localhost:55433/saas_test_db?connect_timeout=3"
    )
    os.environ["DATABASE_URL"] = db_url

    os.environ.setdefault("JWT_SECRET_KEY", "test-secret")
    os.environ.setdefault("JWT_ALGORITHM", "HS256")
    os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    os.environ.setdefault("SKIP_DB_INIT", "1")

    _wait_for_db(db_url)
    _reset_schema(db_url)
    _run_migrations(db_url)


@pytest.fixture()
def client():
    from app.main import app
    with TestClient(app) as c:
        yield c
