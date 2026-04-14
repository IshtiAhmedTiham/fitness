from fastapi import FastAPI
from src.routes.v1.router import router as router_v1
from src.config.v1.database import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router_v1,prefix="/api/v1")


