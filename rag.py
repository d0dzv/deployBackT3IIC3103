from database import query_similar_embeddings
from utils import embed_text

def retrieve_relevant_fragments(question: str):
    question_embedding = embed_text(question)
    results = query_similar_embeddings(question_embedding, top_k=5)
    context = " ".join(
        match['metadata']['text'] for match in results['matches']
        if match.get('metadata') and 'text' in match['metadata']
    )
    
    return context
