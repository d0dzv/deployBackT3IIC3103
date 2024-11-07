from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="pcsk_5F822j_35CR13RqGyTffrTDrn9kyQVHKezhr1dVYs4Jv6obu22cZzEeP2AhgQRLPGj1vnw")

index_name = "movie-scripts"
if index_name not in [index.name for index in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=768, 
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

index = pc.Index(index_name)

def store_embedding(id: str, embedding: list, text: str):
    index.upsert([{
        "id": id,
        "values": embedding,
        "metadata": {"text": text}
    }])

def query_similar_embeddings(embedding, top_k=5):
    results = index.query(
        vector=embedding,
        top_k=top_k,
        include_metadata=True,
        include_values=True
    )
    return results
