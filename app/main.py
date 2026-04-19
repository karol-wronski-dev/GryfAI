import streamlit as st
from llm.ollama_client import ask_ollama

st.set_page_config(page_title="GryfAI", layout="centered", page_icon="⚽")

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

user_just_asked_initial_question = "initial_question" in st.session_state and st.session_state.initial_question
user_just_clicked_suggestion = "selected_suggestion" in st.session_state and st.session_state.selected_suggestion

user_first_interaction = user_just_asked_initial_question or user_just_clicked_suggestion
has_message_history = len(st.session_state.messages) > 0

# Show chat input on the middle before asking question:
if not user_first_interaction and not has_message_history:
    st.html("<h1>Pogoń Szczecin AI Assistant</h1>")

    st.session_state.messages = []

    with st.container():
        # Zmieniamy klucz na 'initial_question', by zachować spójność
        st.chat_input("Zadaj pytanie o Pogoń Szczecin...", key="initial_question")

        st.pills(
            label="Sugestie",
            options=["📅 Najbliższy mecz", "📋 Skład Pogoni", "🏆 Historia klubu"],
            label_visibility="collapsed", 
            key="selected_suggestion"
        )
    
    # Stop rendering until user writes something
    st.stop()

# Different UI after starter question
def clear_conversation():
    st.session_state.messages = []
    st.session_state.initial_question = None
    st.session_state.selected_suggestion = None

title_row = st.container(horizontal=True, vertical_alignment="center") 

with title_row:
    st.title("Pogoń Szczecin AI Assistant", anchor=False)
    st.button("Restart", icon="🔄", on_click=clear_conversation)

# Chat input after UI change
user_input = st.chat_input("Zadaj kolejne pytanie...")

# Print first time message
if not user_input:
    if user_just_asked_initial_question:
        user_input = st.session_state.initial_question
    elif user_just_clicked_suggestion:
        user_input = st.session_state.selected_suggestion

# Printing chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# Answer generation
if user_input:

    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):

        with st.spinner("Analizuję..."):
            response = st.write_stream(ask_ollama(user_input))

        st.session_state.messages.append({"role": "assistant", "content": response})