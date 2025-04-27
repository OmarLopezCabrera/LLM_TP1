# 🧠 Chatbot Multi-CV (TP1) - HuggingFace + Pinecone + Groq

Este proyecto implementa un chatbot que responde preguntas sobre un CV cargado en formato PDF, utilizando las tecnologías más recientes de:

- **LangChain** para la orquestación de componentes de IA
- **Pinecone** como base de datos vectorial
- **Groq** con modelo **Llama3-8b-8192** para generación de respuestas
- **Streamlit** como frontend web

---

## 📋 Tabla de Contenidos

- [Introducción](#introducción)
- [Arquitectura](#arquitectura)
- [Requerimientos](#requerimientos)
- [Inicialización de la Base de Datos](#inicialización-de-la-base-de-datos)
- [Aplicación Web](#aplicación-web)
- [Despliegue](#despliegue)

---

## 🚀 Introducción

Este proyecto demuestra un sistema de **Retrieval-Augmented Generation (RAG)** adaptado a la consulta de contenidos de un CV personal.  
Utiliza la combinación de:

- **Embeddings** de HuggingFace `sentence-transformers/all-MiniLM-L6-v2`
- **Vector storage** en Pinecone
- **Generación natural** con Llama3 via Groq API
- **Orquestación** con LangChain y Streamlit para experiencia interactiva.

El modelo se alimenta únicamente del contexto recuperado desde el índice vectorial, **sin inventar información**.

---

## 🛠️ Arquitectura

- **Carga de PDF** ➔ División en chunks ➔ Vectorización con HuggingFace ➔ Almacenado en Pinecone
- **Consulta** ➔ Embedding de pregunta ➔ Búsqueda top_k en Pinecone ➔ Generación de respuesta con contexto limitado

Diagrama del flujo:

![Arquitectura LLM](/llm_diagram.jpg)

---

## 📋 Requerimientos

Antes de correr el proyecto es necesario:

- Tener cuenta en [Pinecone.io](https://www.pinecone.io/)
- Tener cuenta en [Groq](https://groq.com/)
- Tener API Keys cargadas como variables de entorno:

```bash
export PINECONE_API_KEY="TU_API_KEY"
export GROQ_API_KEY="TU_API_KEY"
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## 🗂️ Inicialización de la Base de Datos

Antes de usar el chatbot, es necesario crear o asegurar la existencia del índice en Pinecone.

Ejecutar:

```bash
python setup_pinecone.py
```

Luego, al subir un PDF desde la app, los datos se procesarán y almacenarán automáticamente en el índice `testhug`, bajo el namespace `cv-space`.

---

## 💬 Aplicación Web

Para correr el chatbot:

```bash
streamlit run main.py
```

Desde el navegador podrás:

- Subir tu propio CV en PDF
- Consultarlo libremente en español
- Recibir respuestas adaptadas al contenido cargado

---

## 🚀 Despliegue

**Modo local:**

- Usamos `Streamlit` ejecutado localmente en Anaconda o un entorno virtual.


---

## 📜 Créditos

Proyecto desarrollado por Omar López Cabrera como parte de la Especialización en Inteligencia Artificial.

---
