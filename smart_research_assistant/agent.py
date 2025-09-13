import os
import json
import requests
from dotenv import load_dotenv
from search import search_papers

load_dotenv()
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_MODEL = "sshleifer/distilbart-cnn-12-6"
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}


def summarize_text(text):
    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    payload = {"inputs": text}
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    data = response.json()
    if isinstance(data, list) and "summary_text" in data[0]:
        return data[0]["summary_text"]
    elif isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"]
    else:
        return str(data)


def ask_agent(query, top_k=3):
    results = search_papers(query, top_k=top_k)

    if not results:
        return "Sorry, no relevant documents found."

    if results[0][3] < 0.3:
        return "Sorry, I don't have enough information on that topic in my database."

    combined_text = " ".join([r[2] for r in results])
    try:
        return summarize_text(combined_text)
    except Exception as e:
        return f"Error in summarization: {e}"
