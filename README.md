Ferramentas necessárias:
- Python 3.12 (ou compatível)
- FastAPI (Framework web)
- Uvicorn (Servidor ASGI)
- Git (Para clonar repositórios)
- Pydriller (Para extrair dados de commits)
- ChromaDB (Banco vetorial)
- SentenceTransformers (Modelo de embeddings)
- Ollama (Para rodar o Llama3-ChatQA localmente)

Para iniciar o servidor da API, execute:
uvicorn app:app --host 0.0.0.0 --port 8000

Em seguida, teste no navegador:
http://127.0.0.1:8000/docs
