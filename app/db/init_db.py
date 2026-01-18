from app.db.base import Base
from app.db.session import engine

# Import models so Base knows them
#import app.models  # noqa: F401
from app.models import User  # noqa: F401


#def init_db() -> None:
    # Base.metadata.create_all(bind=engine)

def init_db() -> None:
    """
    Initialize application data.

    Database schema is managed by Alembic migrations.
    This function is reserved for optional data seeding.
    """
    pass