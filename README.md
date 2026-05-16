# ⚽ GryfAI - Pogoń Szczecin Chatbot

GryfAI is AI assistant designed for fans of **Pogoń Szczecin**. It provides an interactive way to get information about the club, its players, history, and upcoming matches.

---

## 🌟 Key Features

- **🏠 Modern Web Interface:** Built with [Streamlit](https://streamlit.io/), offering a clean, chat-focused UI with persistent history and quick-start suggestions.
- **🧠 Local LLM Power:** Leverages [Ollama](https://ollama.com/) to run models locally (default: `gemma3:4b`). Your conversations stay on your machine.
- **📚 Retrieval-Augmented Generation (RAG):** Enhances model accuracy by retrieving relevant club facts from a **Supabase Vector Database** before answering.
- **⚡ Streaming Responses:** Real-time message generation for a snappy and natural conversation experience.
- **🔍 Smart Context:** Automatically injects verified club knowledge into the conversation context to prevent "hallucinations".

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **LLM Backend:** Ollama API
- **Vector DB:** Supabase (with `pgvector`)
- **Orchestration:** LangChain & LangGraph
- **Embeddings:** `nomic-embed-text`

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.14+**
- **Ollama** installed and running.
- Pull the required models:
  ```bash
  ollama pull gemma3:4b
  ollama pull nomic-embed-text
  ```

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/GryfAI.git
   cd GryfAI
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   # source .venv/bin/activate # Linux/macOS
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration:**
   Create a `.streamlit/secrets.toml` file with your Supabase credentials:
   ```toml
   SUPABASE_URL = "your_supabase_url"
   SUPABASE_KEY = "your_supabase_anon_key"
   ```

### 🗄️ Database Setup (Supabase)

To use the RAG features, you need to configure your Supabase database. Run the following SQL in the **Supabase SQL Editor**:

```sql
-- 1. Enable the pgvector extension
create extension if not exists vector;

-- 2. Create the knowledge table
create table knowledge (
  id bigserial primary key,
  content text,
  metadata jsonb,
  embedding vector(768) -- nomic-embed-text uses 768 dimensions
);

-- 3. Create the similarity search function
create or replace function match_knowledge (
  query_embedding vector(768),
  match_threshold float,
  match_count int
)
returns table (
  id bigint,
  content text,
  metadata jsonb,
  similarity float
)
language sql stable
as $$
  select
    knowledge.id,
    knowledge.content,
    knowledge.metadata,
    1 - (knowledge.embedding <=> query_embedding) as similarity
  from knowledge
  where 1 - (knowledge.embedding <=> query_embedding) > match_threshold
  order by (knowledge.embedding <=> query_embedding) asc
  limit match_count;
$$;
```

### Running the Application

Start the Streamlit server:
```bash
streamlit run app/main.py
```

---

## 🏗️ Data Ingestion

To populate the knowledge base, edit the `raw_text` in `app/load_data.py` and run:
```bash
python app/load_data.py
```
This will chunk the text, generate embeddings, and upload them to your Supabase instance.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*GryfAI is a fan-made project and is not officially affiliated with Pogoń Szczecin S.A.*
