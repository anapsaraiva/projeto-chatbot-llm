from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from data_processing import process_repository
from retrieval import retrieve_relevant_docs
from llm import generate_response

app = FastAPI()
repo_data_store = {}  # Armazena temporariamente os dados do repositório processado

class RepoRequest(BaseModel):
    repo_url: HttpUrl  # Garante que a URL fornecida é válida

class QuestionRequest(BaseModel):
    repo_url: HttpUrl
    question: str

@app.post("/process_repo")
def process_repo(request: RepoRequest):
    repo_url = str(request.repo_url)

    # Verifica se a URL pertence ao GitHub e é pública
    if not repo_url.startswith("https://github.com/"):
        raise HTTPException(status_code=400, detail="Apenas repositórios públicos do GitHub são permitidos.")

    try:
        repo_data = process_repository(repo_url)
        repo_data_store[repo_url] = repo_data  # Armazena os dados temporariamente
        return {"message": "Repositório processado com sucesso!", "data": repo_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
def ask_question(request: QuestionRequest):
    repo_url = str(request.repo_url)
    
    if repo_url not in repo_data_store:
        raise HTTPException(status_code=400, detail="Repositório não processado. Primeiro envie a URL para /process_repo.")

    docs = retrieve_relevant_docs(request.question, repo_data_store[repo_url])  # Busca dados relevantes
    response = generate_response(request.question, docs)  # Gera resposta com o Llama3-ChatQA

    return {"response": response}

