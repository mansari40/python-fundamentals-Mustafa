from qdrant_client.models import ScoredPoint

from storage.vector import COLLECTION_NAME, client
from utils.embed import embed


def search_qdrant(query: str, limit: int = 5) -> list[ScoredPoint]:
    query_vector = embed(query, task_type="RETRIEVAL_QUERY")
    res = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
        with_payload=True,
    )
    return list(res.points)


if __name__ == "__main__":
    results = search_qdrant(
        (
            "According to the abstract, Mauritius reduced the cost of starting a "
            "business by 71.7%. "
            "Additionally, it saw inward FDI increases of 167.6%. "
            "What are the corresponding numbers for South Africa?"
        ),
        limit=5,
    )
    for p in results:
        payload = p.payload or {}
        print(f"Score: {p.score}")
        print(payload.get("chunk_text", ""))
        print("-" * 50)
