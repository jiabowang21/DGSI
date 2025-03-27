from ollamaEmbedding import OllamaEmbeddingFunction  # Importamos la clase desde el archivo ollamaEmbedding.py
import chromadb
import requests
import json
from chromadb.api.types import EmbeddingFunction
import re

def load_markdown_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def chunk_text(text, chunk_size=300):
    sentences = re.split(r'\n\n+', text)  # Separar por párrafos (mejor para Markdown)
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        current_length += len(sentence)
        current_chunk.append(sentence)

        if current_length >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def procesar_datos():
    embedding_function = OllamaEmbeddingFunction()
    chroma_client = chromadb.PersistentClient(path="./chroma_db")

    # Crear la colección con Ollama como generador de embeddings
    collection = chroma_client.get_or_create_collection(
        name="markdown_collection",
        embedding_function=embedding_function  # Pasamos la función de embeddings personalizada
    )
    file_path = "/Users/jiabowang/Desktop/dgsi/DGSI/reto2/pagina.md"

    text = load_markdown_file(file_path)

    # Dividir el texto en chunks
    chunks = chunk_text(text, chunk_size=300)

    # Insertar los chunks en ChromaDB
    collection.upsert(
        documents=chunks,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )

    print(f"Se han insertado {len(chunks)} chunks en ChromaDB.")
    return chunks

