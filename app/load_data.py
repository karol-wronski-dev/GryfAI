import streamlit as st
from supabase import create_client, Client
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings

# Supabase connection (use your secrets from .streamlit/secrets.toml)
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# Config for embeddings
embeddings_model = OllamaEmbeddings(model="nomic-embed-text")

# Your text you want to put into table
raw_text = """

"""

print("Cutting text...")
# Cut text into pieces
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,       # maximum length of a single segment
    chunk_overlap=50,     # overlapping sections to maintain context
    length_function=len,
)
chunks = text_splitter.create_documents([raw_text])
print(f"Text divided to {len(chunks)} pieces.")

# Vector generation and send it to supabase
for i, chunk in enumerate(chunks):
    content = chunk.page_content
    
    print(f"Vector generation for piece: {i+1}...")
    # Text to Vector translation
    vector = embeddings_model.embed_query(content)
    
    # Metadata - where this data came from
    metadata = {
        "source": "",
        "topic": ""
    }
    
    # Write to db (table "knowledge")
    supabase.table('knowledge').insert({
        "content": content,
        "metadata": metadata,
        "embedding": vector
    }).execute()

print("✅ Ready! Data written has been written to database!")