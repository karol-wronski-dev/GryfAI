OLLAMA_URL = "http://localhost:11434/api/generate"


def ask_ollama(prompt, model="gemma3:4b"):
    import requests
    import json

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": True
        },
        stream=True
    )

    for line in response.iter_lines():
        if line:
            data = json.loads(line)
            yield data["response"]
