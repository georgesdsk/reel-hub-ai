from fastapi import FastAPI
from src.api.routes import videos, search, stats, import_instagram, jobs, telegram, health
from src.config.settings import settings

app = FastAPI(title="Personal Video Search API")

app.include_router(health.router)
app.include_router(videos.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")
app.include_router(stats.router, prefix="/api/v1")
app.include_router(import_instagram.router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")
app.include_router(telegram.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"app": "Personal Video Search API", "status": "running"}
