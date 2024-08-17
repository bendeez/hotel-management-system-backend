from fastapi import Depends
from chromadb import Documents, EmbeddingFunction, Embeddings, AsyncHttpClient
from sentence_transformers import SentenceTransformer
from app.tools.chroma.chroma_client import get_chroma_client
import uuid




class BGELargeEN(EmbeddingFunction):

    def __call__(self, texts: Documents) -> Embeddings:
        model = SentenceTransformer('BAAI/bge-large-en-v1.5')
        return model.encode(texts)

class ChromaService:

    def __init__(self, chroma_client: AsyncHttpClient = Depends(get_chroma_client)):
        self.chroma_client = chroma_client
        self.model = SentenceTransformer('BAAI/bge-large-en-v1.5')


    def upsert_chromadb(self, embeddings, ids, collection, metadatas):
        collection.upsert(embeddings=embeddings, ids=ids, metadatas=metadatas)

    def delete_chroma_collection(self, collection_name):
        self.chroma_client.delete_collection(name=collection_name)

    def get_chroma_collection(self, collection_name):
        collection = self.chroma_client.get_or_create_collection(name=collection_name)
        return collection