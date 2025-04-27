import os
from pinecone import Pinecone
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

pinecone_api_key = os.getenv("PINECONE_API_KEY")
index_name = "testhug"
namespace = "cv-space"

def ingest_pdf_to_pinecone(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
    split_docs = splitter.split_documents(docs)

    texts = [d.page_content for d in split_docs]
    metadatas = [{"text": d.page_content} for d in split_docs]

    embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectors = embed_model.embed_documents(texts)

    pc = Pinecone(api_key=pinecone_api_key)
    index = pc.Index(index_name)

    index.delete(delete_all=True, namespace=namespace)

    pinecone_vectors = [
        {"id": f"doc-{i}", "values": vectors[i], "metadata": metadatas[i]}
        for i in range(len(vectors))
    ]
    index.upsert(vectors=pinecone_vectors, namespace=namespace)
