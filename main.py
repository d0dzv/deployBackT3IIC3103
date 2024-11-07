from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag import retrieve_relevant_fragments
from api_client import get_llm_response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

@app.post("/query", response_model=QueryResponse)
async def query_movie_explanation(request: QueryRequest):
    try:
        print(f"Recibida pregunta: {request.question}")
        context = retrieve_relevant_fragments(request.question)
        answer = get_llm_response(request.question, context)
        return QueryResponse(answer=answer)
    except Exception as e:
        print(f"Error en /query: {e}")
        raise HTTPException(status_code=500, detail="Error interno en el servidor")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
