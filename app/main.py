import streamlit as st
from llm.ollama_client import ask_ollama
import time

st.set_page_config(page_title="Pogon Szczecin Chatbot", layout="wide")
st.title("Pogon Szczecin Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_prompt = st.chat_input("Zadaj pytanie o Pogoń Szczecin...")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("user"):
        st.write(user_prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""

        for chunk in ask_ollama(user_prompt):
            full_text += chunk
            placeholder.markdown(full_text + "▌")
            time.sleep(0.055)

        placeholder.markdown(full_text)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_text})
