import pandas as pd
from models.chunk import ScientificArticleChunk
from storage.vector import COLLECTION_NAME, client
from qdrant_client.models import PointStruct
import uuid


def make_point_id(row: pd.Series) -> uuid.UUID:
    return uuid.uuid5(uuid.NAMESPACE_URL, f"{row.arxiv_id}_chunk_{row.chunk_index}")


def chunk_exists(row: pd.Series) -> pd.Series:
    point_id = make_point_id(row)
    records = client.retrieve(COLLECTION_NAME, ids=[point_id])
    return pd.Series([len(records) > 0], index=["exists_in_qdrant"], dtype=bool)


def insert_embedding(row: pd.Series) -> pd.Series:
    point_id = make_point_id(row)

    if row.embedding is None:
        return pd.Series([point_id], index=["point_id"])

    point = PointStruct(
        id=point_id,
        vector=row.embedding,
        payload=ScientificArticleChunk(
            title=row.title,
            summary=row.summary,
            arxiv_id=row.arxiv_id,
            author_full_name=row.author_full_name,
            chunk_text=row.chunk_text,
            chunk_index=int(row.chunk_index),
        ).model_dump(),
    )

    client.upsert(collection_name=COLLECTION_NAME, points=[point])
    return pd.Series([point_id], index=["point_id"])


def save_to_qdrant(df: pd.DataFrame) -> pd.DataFrame:
    point_ids = df.apply(insert_embedding, axis=1)
    return pd.concat([df, point_ids], axis=1)


def check_chunks_in_qdrant(df: pd.DataFrame) -> pd.DataFrame:
    exists = df.apply(chunk_exists, axis=1)
    return pd.concat([df, exists], axis=1)
