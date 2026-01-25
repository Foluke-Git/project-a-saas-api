from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.router import api_router
from app.core.config import get_settings

settings = get_settings()

from app.db.deps import get_db
from app.db.init_db import init_db


import os
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Only initialize DB in normal app runs (not tests)
    if os.getenv("SKIP_DB_INIT") != "1":
        init_db()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)


def custom_openapi():
    return get_openapi(
        title=app.title,
        version="0.1.0",
        routes=app.routes,
    )

app.openapi = custom_openapi


@app.get("/")
def root():
    return {"message": "SaaS API is running. Go to /docs"}


@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.environment}


@app.get("/health/db")
def db_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "ok"}


app.include_router(api_router)
