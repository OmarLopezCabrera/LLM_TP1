import streamlit as st
import os
from chat_engine import ChatBot
from ingest import ingest_pdf_to_pinecone
import tempfile

st.title("🧠 Chat con tu CV (HuggingFace + testhug index)")

pinecone_api_key = os.getenv("PINECONE_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

with st.sidebar:
    st.markdown("### 🔐 Estado de API Keys")
    st.success("✅ Pinecone API Key OK" if pinecone_api_key else "❌ Pinecone API Key NO encontrada")
    st.success("✅ Groq API Key OK" if groq_api_key else "❌ Groq API Key NO encontrada")

st.text("🔍 Pinecone key usada: " + (pinecone_api_key or "NO DETECTADA")[:10])

uploaded_file = st.file_uploader("📄 Sube tu CV en PDF", type="pdf")
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    try:
        ingest_pdf_to_pinecone(tmp_path)
        st.success("✅ ¡Documento indexado en Pinecone!")
    except Exception as e:
        st.error(f"⚠️ Error al procesar el PDF: {str(e)}")

bot = ChatBot()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_query = st.chat_input("Escribí tu pregunta sobre el CV...")
if user_query:
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        try:
            answer = bot.chat(user_query)
        except Exception as e:
            st.markdown(f"⚠️ Error: {str(e)}")
            answer_content = str(e)
        else:
            st.markdown(answer.content)
            answer_content = answer.content

        st.session_state.chat_history.append((user_query, answer_content))

else:
    for q, a in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(q)
        with st.chat_message("assistant"):
            st.markdown(a)
