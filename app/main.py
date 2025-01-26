from fastapi import FastAPI
from app.api.v1.endpoints import wallet
from app.core.db import init_db




app = FastAPI()

app.include_router(wallet.router, prefix="/api/v1")

@app.on_event("startup")
async def on_startup():
    await init_db()