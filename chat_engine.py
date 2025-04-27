import os
from pinecone import Pinecone
from langchain_groq import ChatGroq
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate

pinecone_api_key = os.getenv("PINECONE_API_KEY")
index_name = "testhug"
namespace = "cv-space"

class ChatBot:
    def __init__(self):
        self.embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.llm = ChatGroq(model="llama3-8b-8192", api_key=os.getenv("GROQ_API_KEY"))

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Eres un asistente que responde preguntas sobre un currículum en español. "
                       "Solo debes usar el contexto proporcionado. Si no sabes la respuesta, dilo claramente. "
                       "Responde de manera breve, clara y profesional. Contexto:\n\n{context}"),
            ("human", "{input}")
        ])

        try:
            pc = Pinecone(api_key=pinecone_api_key)
            self.index = pc.Index(index_name)
            print("✅ Conectado al índice 'testhug'")
        except Exception as e:
            print("❌ No se pudo conectar al índice:", e)
            raise RuntimeError("Error de conexión con Pinecone.")

    def chat(self, query: str):
        try:
            query_embedding = self.embed_model.embed_query(query)
            results = self.index.query(vector=query_embedding, top_k=7, namespace=namespace, include_metadata=True)
            context = "\n\n".join([match["metadata"].get("text", "") for match in results["matches"]])
            print("🔍 Contexto pasado al modelo:")
            print(context[:500] + "\n..." if len(context) > 500 else context)
        except Exception as e:
            print("❌ Error al consultar Pinecone:", e)
            context = "No se pudo recuperar contexto del CV."

        full_prompt = self.prompt.invoke({"input": query, "context": context})
        return self.llm.invoke(full_prompt)
