from sentence_transformers import SentenceTransformer
import chromadb

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection("repository_docs")
model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_relevant_docs(query, repo_data):
    if not repo_data:
        return ["Nenhuma informação encontrada sobre este repositório."]

    query_embedding = model.encode(query).tolist()

    # Criar listas para adicionar ao ChromaDB no formato correto
    ids = []
    embeddings = []
    metadatas = []

    for doc in repo_data:
        ids.append(str(doc["hash"]))  # IDs devem ser strings
        embeddings.append(model.encode(doc["message"]).tolist())  # Criar embedding

        # Converte lista de arquivos modificados em uma string separada por vírgula
        modified_files_str = ", ".join(doc["modified_files"]) if doc["modified_files"] else "Nenhum arquivo modificado"

        # Criar dicionário de metadados compatível com o ChromaDB
        metadata = {
            "hash": doc["hash"],
            "author": doc["author"],
            "date": doc["date"],
            "message": doc["message"],
            "modified_files": modified_files_str  # Agora é uma string, não uma lista
        }

        metadatas.append(metadata)

    # Adiciona os dados ao banco vetorial ChromaDB
    if ids:  # Evita erro ao tentar adicionar lista vazia
        collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)

    # Busca os documentos mais relevantes
    results = collection.query(query_embeddings=[query_embedding], n_results=4)

    if not results or "documents" not in results or not results["documents"]:
        return ["Nenhuma informação relevante foi encontrada para essa pergunta."]

    return results["documents"]

