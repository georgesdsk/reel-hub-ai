from fastapi import FastAPI
from src.api.routes import health

app = FastAPI(title="VideoMind API")

app.include_router(health.router)

@app.get("/")
async def root():
    return {"message": "Welcome to VideoMind API"}
