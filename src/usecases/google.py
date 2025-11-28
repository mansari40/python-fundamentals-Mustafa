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
    segments: list[str] = []

    while start < len(text):
        end = start + chunk_size
        segment = text[start:end]

        if end < len(text):
            last_period = segment.rfind(".")
            if last_period > chunk_size // 2:
                end = start + last_period + 1
                segment = text[start:end]

        segments.append(segment.strip())
        start = end - overlap

    print(segments)

    embeddings: list[str] = []
    return pd.Series({"chunk_text": segments, "embeddings": embeddings})


def embed_documents(df: pd.DataFrame) -> pd.DataFrame:
    df[["chunk_text", "embeddings"]] = df.progress_apply(embed_article, axis=1)
    return df
