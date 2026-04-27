import requests
import json
import streamlit as st
from supabase import create_client, Client
from langchain_ollama import OllamaEmbeddings


@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

@st.cache_resource
def init_embeddings():
    return OllamaEmbeddings(model="nomic-embed-text")

OLLAMA_URL = "http://localhost:11434/api/chat"


def ask_ollama(user_input: str, chat_history: list, model: str = "gemma3:4b"):

    supabase = init_supabase()
    embeddings_model = init_embeddings()

    # Searching for knowledge in db
    query_vector = embeddings_model.embed_query(user_input)
    db_response = supabase.rpc(
        'match_knowledge',
        {'query_embedding': query_vector, 'match_threshold': 0.3, 'match_count': 3}
    ).execute()

    # Building context
    context = ""
    if db_response.data:
        for doc in db_response.data:
            context += doc['content'] + "\n\n"

    print("\n--- ZNALEZIONY KONTEKST Z SUPABASE ---")
    print(context if context else "PUSTO - Baza nic nie zwróciła!")
    print("--------------------------------------\n")

    # 4. System Prompt
    system_prompt = f"""Jesteś asystentem kibica Pogoni Szczecin o imieniu GryfAI.
    Twoim zadaniem jest odpowiadanie na pytania na podstawie PONIŻSZEGO KONTEKSTU.
    Jeśli w kontekście nie ma odpowiedzi, powiedz: "Nie mam w bazie informacji na ten temat.", nie zmyślaj.

    KONTEKST:
    {context}
    """

    # Building history for model
    messages = [{"role": "system", "content": system_prompt}]

    for msg in chat_history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # Sending to Ollama
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "messages": messages,
            "stream": True
        },
        stream=True
    )

    # Write response in chunks
    for line in response.iter_lines():
        if line:
            data = json.loads(line)
            yield data["message"]["content"]
