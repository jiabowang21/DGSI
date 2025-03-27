import chromadb
import requests
import json
from chromadb.api.types import EmbeddingFunction

# Crear la función de embeddings usando Ollama
class OllamaEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input):
        embeddings = []
        for text in input:
            response = requests.post(
                "http://localhost:11434/api/embeddings",  # Endpoint correcto para embeddings
                json={"model": "nomic-embed-text", "prompt": text}  # Enviar un solo texto a la vez
            )
            response_json = response.json()
            
            if "embedding" in response_json:
                embeddings.append(response_json["embedding"])  # Guardar el embedding
            else:
                raise ValueError(f"Error en la respuesta de Ollama: {response_json}")
        
        return embeddings  # Retorna una lista de embeddings
