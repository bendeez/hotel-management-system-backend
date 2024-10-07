import pytest
from tools.domain.database import SessionLocal, engine
from tools.domain.base_models import BaseMixin


@pytest.fixture(name="db", scope="session", autouse=True)
async def create_db_session():
    async with SessionLocal() as db:
        yield db


@pytest.fixture(scope="session", autouse=True)
async def create_tables(db):
    async with engine.begin() as conn:
        await conn.run_sync(BaseMixin.metadata.drop_all)
        await conn.run_sync(BaseMixin.metadata.create_all)
