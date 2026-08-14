from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.auth.router import router as auth_router
from api.jobs.router import router as jobs_router
from api.label_studio.router import router as label_studio_router
from api.storage.router import router as storage_router
from api.users.router import router as users_router
from core.config import settings
from db.database import create_database_schema

tags_metadata = [
    {"name": "auth", "description": "Authentication — register, login, JWT token"},
    {"name": "users", "description": "User CRUD operations"},
    {"name": "storage", "description": "MinIO object storage — buckets, upload, download"},
    {"name": "label-studio", "description": "Label Studio — projects & tasks"},
    {"name": "jobs", "description": "Job queue — enqueue work to Redis / ARQ worker"},
    {"name": "system", "description": "Health check & system info"},
]


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Convenient for a new project; replace with Alembic migrations in production.
    await create_database_schema()
    yield


app = FastAPI(
    title="AI Ecosystem API",
    description="Central API Server for AI Ecosystem — จัดการ users, storage, annotation, และ job queue",
    version="0.1.0",
    debug=settings.DEBUG_MODE,
    lifespan=lifespan,
    docs_url="/",
    redoc_url="/redoc",
    openapi_tags=tags_metadata,
)

app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(storage_router, prefix="/api")
app.include_router(label_studio_router, prefix="/api")
app.include_router(jobs_router, prefix="/api")


@app.get("/health", tags=["system"], summary="Health Check", description="ตรวจสอบว่า API server ทำงานปกติ")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}



if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)