from google import genai
from google.genai import types
from dotenv import load_dotenv
import os


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

result = client.models.embed_content(
    model="models/gemini-embedding-001",
    contents=[
        "Machine learning is a subset of AI that trains computers to learn from data.",
        "Deep learning is a subset of machine learning that uses neural networks.",
        "LLMs can measure similarity and generate new content.",
        "LLMs can do complex tasks like understanding context.",
    ],
    config=types.EmbedContentConfig(output_dimensionality=768),
)


print(result.embeddings)
