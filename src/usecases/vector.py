import pandas as pd
from models.chunk import ScientificArticleChunk
from storage.vector import COLLECTION_NAME, client
from qdrant_client.models import PointStruct
import uuid


def make_point_id(article_chunk: pd.Series) -> uuid.UUID:
    return uuid.uuid5(
        uuid.NAMESPACE_URL,
        f"{article_chunk.arxiv_id}_chunk_{article_chunk.chunk_index}",
    )


def chunk_exists(article_chunk: pd.Series) -> pd.Series:
    point_id = make_point_id(article_chunk)
    records = client.retrieve(COLLECTION_NAME, ids=[point_id])
    return pd.Series([len(records) > 0], index=["exists_in_qdrant"], dtype=bool)


def insert_embeddings(article: pd.Series) -> pd.Series:
    i = 0
    for text, emb in zip(article.chunk_texts, article.embeddings):
        point = PointStruct(
            id=uuid.uuid5(uuid.NAMESPACE_URL, f"{article.arxiv_id}_chunk_{i}"),
            vector=emb,
            payload=ScientificArticleChunk(
                title=article.title,
                summary=article.summary,
                arxiv_id=article.arxiv_id,
                author_full_name=article.author_full_name,
                chunk_text=text,
                chunk_index=i,
            ).model_dump(),
        )
        client.upsert(collection_name=COLLECTION_NAME, points=[point])
        i += 1

    return pd.Series([], index=[])


def save_to_qdrant(df: pd.DataFrame) -> pd.DataFrame:
    df.apply(insert_embeddings, axis=1)
    return df
