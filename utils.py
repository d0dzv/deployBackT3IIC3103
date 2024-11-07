import requests
import json

def embed_text(text: str) -> list:
    url = "http://tormenta.ing.puc.cl/api/embed"
    payload = {
        "model": "nomic-embed-text",
        "input": json.dumps(text)[1:-1]
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()["embeddings"][0]
    else:
        raise Exception(f"Error al obtener embedding: {response.status_code}")
