from google import genai
from google.genai import types  # noqa: F401
from dotenv import load_dotenv
import os
import pandas as pd  # noqa: F401

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def embed_article(
    article: pd.Series, chunk_size: int = 1200, overlap: int = 250
) -> pd.Series:
    text = article.md_text
    start = 0
    chunks: list[str] = []

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if end < len(text):
            last_period = chunk.rfind(".")
            if last_period > chunk_size // 2:
                end = start + last_period + 1
                chunk = text[start:end]

        chunks.append(chunk.strip())
        start = end - overlap

    avg = sum(len(c) for c in chunks) / len(chunks)

    print(article.local_file_path, len(chunks), avg)

    embeddings: list[str] = []

    return pd.Series({"chunk_text": chunks, "embeddings": embeddings})


def embed_documents(df: pd.DataFrame) -> pd.DataFrame:
    df = df.progress_apply(embed_article, axis=1)
    return df.explode("chunk_text")
