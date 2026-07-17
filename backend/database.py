import os
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://carbon:carbon@localhost:5432/carbonfootprint",
)

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        yield session


async def init_db():
    # Phase 1: Create tables (in its own transaction)
    async with engine.begin() as conn:
        from backend.models import Vehicle, Destination  # noqa: F401
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)

    # Phase 2: Add missing columns (separate transaction, safe to fail)
    async with engine.begin() as conn:
        for col, col_type in [("lat", "DOUBLE PRECISION"), ("lng", "DOUBLE PRECISION")]:
            try:
                result = await conn.execute(
                    text(f"SELECT column_name FROM information_schema.columns WHERE table_name='destinations' AND column_name='{col}'")
                )
                if not result.scalar():
                    await conn.execute(text(f"ALTER TABLE destinations ADD COLUMN {col} {col_type}"))
            except Exception:
                pass
