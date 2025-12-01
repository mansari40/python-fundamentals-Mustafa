import os

import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def embed(text: str, task_type: str = "SEMANTIC_SIMILARITY") -> np.ndarray:
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=[text],
        config=types.EmbedContentConfig(
            output_dimensionality=768,
            task_type=task_type,
        ),
    )
    if result.embeddings is None:
        raise ValueError("No embeddings returned")

    return np.array(result.embeddings[0].values)
