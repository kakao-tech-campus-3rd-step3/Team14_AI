from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = "mysql+asyncmy://admin:festa-server-1234@festapick-db.cjwm4iu0a67l.ap-northeast-2.rds.amazonaws.com:3306/festapick?charset=utf8mb4"


if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in .env")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass

async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
