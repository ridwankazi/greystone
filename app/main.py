from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base  # noqa: F401 - ensure models are imported
from app.api.v1.routers.users import router as users_router
from app.api.v1.routers.loans import router as loans_router
from app.core.config import get_settings
import os

app = FastAPI(title="Greystone API", version="0.1.0")


@app.on_event("startup")
def on_startup() -> None:
    # Ensure SQLite data directory exists for local dev
    settings = get_settings()
    if settings.database_url.startswith("sqlite"):
        # e.g., sqlite:///./data/app.db -> path after 'sqlite:///'
        prefix = "sqlite:///"
        path = (
            settings.database_url[len(prefix) :]
            if settings.database_url.startswith(prefix)
            else ""
        )
        if path:
            dir_path = os.path.dirname(path)
            if dir_path and not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)

    # Create tables on startup for demo/dev.
    # In production, use migrations (e.g., Alembic).
    from app.db.base import Base  # ensure models registry is loaded

    Base.metadata.create_all(bind=engine)


app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(loans_router, prefix="/api/v1/loans", tags=["loans"])
