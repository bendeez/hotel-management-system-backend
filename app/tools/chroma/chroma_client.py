from chromadb import AsyncHttpClient
from app.config import settings


async def get_chroma_client():
    async with AsyncHttpClient(
        host=settings.host_chromadb, port=settings.vector_db_port
    ) as client:
        yield client
