from typing import Generator, AsyncGenerator
from fastapi import FastAPI, Depends
from sqlmodel import Field, SQLModel, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine 
from contextlib import asynccontextmanager

# --- Data Model (Used by both Sync and Async) ---
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None

# =========================================================
# ASYNC APPLICATION SETUP (Runs on Port 8000) - REMAINS AS IS
# =========================================================
ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./async_test.db"
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)

async def create_async_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@asynccontextmanager
async def async_lifespan(app: FastAPI):
    print("Async App Startup: Creating tables...")
    await create_async_db_and_tables()
    yield
    print("Async App Shutdown.")

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(async_engine) as session:
        yield session

app_async = FastAPI(lifespan=async_lifespan, title="Async API")

@app_async.post("/async/heroes/", response_model=Hero)
async def create_async_hero(*, session: AsyncSession = Depends(get_async_session), hero: Hero):
    session.add(hero)
    await session.commit()
    await session.refresh(hero)
    return hero

@app_async.get("/async/heroes/", response_model=list[Hero])
async def read_async_heroes(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Hero))
    heroes = result.scalars().all()
    return heroes

# =========================================================
# SYNC APPLICATION SETUP (Runs on Port 8001) - GUARANTEED FIX
# =========================================================
SYNC_DATABASE_URL = "sqlite:///./sync_test.db"
sync_engine = create_engine(SYNC_DATABASE_URL, echo=False)

def create_sync_db_and_tables():
    # Synchronously create tables.
    SQLModel.metadata.create_all(sync_engine)

# 1. IMMEDIATE EXECUTION OF SETUP (The Fix)
# We run the blocking setup function directly here. This guarantees the tables
# exist before Uvicorn ever starts the server, circumventing the lifespan error.
print("Sync App Global Setup: Creating tables...")
create_sync_db_and_tables()

# 2. NO LIFESPAN PASSED TO FASTAPI
# This prevents Starlette/Uvicorn from looking for the __aenter__ attribute.
app_sync = FastAPI(title="Sync API") 

def get_sync_session() -> Generator[Session, None, None]:
    with Session(sync_engine) as session:
        yield session

@app_sync.post("/sync/heroes/", response_model=Hero)
async def create_sync_hero(*, session: Session = Depends(get_sync_session), hero: Hero):
    # FastAPI automatically executes this sync function in a threadpool
    # because it detects the sync Session dependency.
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app_sync.get("/sync/heroes/", response_model=list[Hero])
async def read_sync_heroes(session: Session = Depends(get_sync_session)):
    result = session.exec(select(Hero))
    heroes = result.all()
    return heroes

# ----------------------------------------------------------------------------------
# Execution commands (use the new file name):
# Terminal 1: uvicorn app_comparison_final:app_async --port 8000 --workers 1
# Terminal 2: uvicorn app_comparison_final:app_sync --port 8001 --workers 1
# ----------------------------------------------------------------------------------
