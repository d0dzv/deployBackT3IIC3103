import os
import re
from database import store_embedding
from utils import embed_text

FRAGMENT_SIZE = 500
SCRIPT_FOLDER = "movies/"

def clean_text(text):
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ,.?!\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def split_script_into_fragments(text, fragment_size=FRAGMENT_SIZE):
    words = text.split()
    fragments = [" ".join(words[i:i + fragment_size]) for i in range(0, len(words), fragment_size)]
    return fragments

def process_and_store_script(script_text, script_id):
    clean_script_text = clean_text(script_text)
    fragments = split_script_into_fragments(clean_script_text)
    for i, fragment in enumerate(fragments):
        embedding = embed_text(fragment)
        fragment_id = f"{script_id}_{i}"
        store_embedding(fragment_id, embedding, fragment)
        print(f"Fragmento {fragment_id} almacenado correctamente.")


def fill_database():
    for filename in os.listdir(SCRIPT_FOLDER):
        if filename.endswith(".txt"):
            with open(os.path.join(SCRIPT_FOLDER, filename), "r") as file:
                script_text = file.read()
                script_id = filename.split(".")[0]
                print(f"Procesando guion: {script_id}")
                process_and_store_script(script_text, script_id)

if __name__ == "__main__":
    fill_database()
