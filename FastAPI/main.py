from fastapi import FastAPI, Depends
from typing import Generator, AsyncGenerator
from sqlmodel import SQLModel, Field, Session, select, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from contextlib import asynccontextmanager

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None

#ASYNC APP
ASYNC_DATABASE_URL = 'sqlite+aiosqlite:///./test_async.db'
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)

async def create_async_db_and_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@asynccontextmanager
async def async_lifespan(app: FastAPI):
    print('Starting Async App: creating tables')
    await create_async_db_and_table()
    yield
    print('shutting down Async app')

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(async_engine) as session:
        yield session

app_async = FastAPI(lifespan=async_lifespan, title='Async API')

@app_async.post('/async/heroes', response_model=Hero)
async def create_hero(*, session: AsyncSession = Depends(get_async_session), hero: Hero):
    session.add(hero)
    await session.commit()
    await session.refresh(hero)
    return hero

@app_async.get('/async/heroes', response_model=list[Hero])
async def create_hero(*, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Hero))
    heroes = result.scalars().all()
    return heroes

########### SYNC APP ####
SYNC_DATABASE_URL = 'sqlite:///./test_sync.db'
sync_engine = create_engine(SYNC_DATABASE_URL, echo=False)

print('Starting sync app: creating table')
SQLModel.metadata.create_all(sync_engine)

app_sync = FastAPI(title='Sync API')

def get_sync_session() -> Generator[Session, None, None]:
    with Session(sync_engine) as session:
        yield session

@app_sync.post('/sync/heroes', response_model=Hero)
def create_hero(*, session: Session = Depends(get_sync_session), hero: Hero):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app_sync.get('/sync/heroes', response_model=list[Hero])
def create_hero(*, session: Session = Depends(get_sync_session)):
    result = session.execute(select(Hero))
    heroes = result.all()
    return heroes
