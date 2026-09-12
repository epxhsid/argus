import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

current_dir = Path(__file__).resolve().parent
dotenv_path = current_dir.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

DATABASE_URL = os.environ["ASYNCPGDBURL"]

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
