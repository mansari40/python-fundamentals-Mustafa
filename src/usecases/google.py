from google import genai
from google.genai import types  # noqa: F401
from dotenv import load_dotenv
import os
import pandas as pd  # noqa: F401
import numpy as np


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def apply_chunking(
    article: pd.Series, chunk_size: int = 1200, overlap: int = 250
) -> pd.Series:
    text = str(article.md_text)
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

    return pd.Series(
        [chunks, list(range(len(chunks)))], index=["chunk_text", "chunk_index"]
    )


def chunk_documents(df: pd.DataFrame) -> pd.DataFrame:
    chunks = df.apply(apply_chunking, axis=1)
    return pd.concat([df, chunks], axis=1).explode(
        ["chunk_index", "chunk_text"], ignore_index=True
    )


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

    contents = chunks[:2]
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=contents,
        config=types.EmbedContentConfig(
            output_dimensionality=768,
            task_type="SEMANTIC_SIMILARITY",
        ),
    )

    embeddings = np.array(
        [np.array(embedding.values) for embedding in result.embeddings or []]
    )
    return pd.Series([contents, embeddings], index=["chunk_texts", "embeddings"])


def embed_documents(df: pd.DataFrame) -> pd.DataFrame:
    result = df.apply(embed_article, axis=1)
    df = pd.concat([df, result], axis=1)
    return df
