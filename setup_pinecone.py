import os
from pinecone import Pinecone, ServerlessSpec

def ensure_index_exists():
    try:
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        pc.Index("cvopenai").describe_index_stats()
        print("✅ Conectado al índice existente.")
    except Exception:
        print("⚠️ No se pudo verificar el índice. Asumiendo que ya existe.")
