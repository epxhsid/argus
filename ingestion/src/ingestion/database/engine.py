import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

load_dotenv()

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
