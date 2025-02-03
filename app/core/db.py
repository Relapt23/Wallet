from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "wallet_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "wallet_pass")
DB_NAME = os.getenv("DB_NAME", "wallet_db")

engine = create_async_engine(f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)
sess = async_sessionmaker(engine)
