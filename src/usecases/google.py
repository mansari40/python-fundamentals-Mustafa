from google import genai
from google.genai import types  # noqa: F401
from dotenv import load_dotenv
import os
import pandas as pd  # noqa: F401
import numpy as np


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

    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=chunks[:2],
        config=types.EmbedContentConfig(
            output_dimensionality=768,
            task_type="SEMANTIC_SIMILARITY",
        ),
    )

    embeddings_array = np.array(
        [np.array(embedding) for embedding in result.embeddings or []]
    )
    return pd.Series([embeddings_array], index=["embeddings"])


def embed_documents(df: pd.DataFrame) -> pd.DataFrame:
    df["embeddings"] = df.progress_apply(embed_article, axis=1)
    return df
