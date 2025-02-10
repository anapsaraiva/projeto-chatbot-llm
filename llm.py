import ollama

def generate_response(query, context):
    if not context or len(context) == 0:
        return "Não encontrei informações suficientes no repositório para responder sua pergunta."

    # Filtra e garante que todos os valores em context sejam strings, substituindo None por uma string vazia
    context_text = "\n".join(
        [str(doc) if doc is not None else "" for doc in context]
    )

    prompt = f"""
    Contexto: {context_text}
    Pergunta: {query}
    Resposta:
    """

    response = ollama.chat(model="llama3-chatqa", messages=[{"role": "user", "content": prompt}])

    return response["message"]["content"]

