from fastapi import FastAPI
from app.api.v1.endpoints import wallet
from app.core.db import engine
from app.api.models.models import Base

app = FastAPI()

app.include_router(wallet.router, prefix="/api/v1")


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def on_startup():
    await init_db()
