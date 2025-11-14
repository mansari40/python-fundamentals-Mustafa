from pathlib import Path
import pandas as pd
import pymupdf4llm
from models.mongo import ScientificArticle as MongoArticle, Author as MongoAuthor
import storage.mongo  # noqa: F401


def store_article(row: pd.Series) -> pd.Series:
    try:
        m_author = MongoAuthor(
            db_id=row["author_db_id"],
            full_name=row["author_full_name"],
            title=row["author_title"],
        )
        pdf_path = Path(row["file_path"])
        text_md = pymupdf4llm.to_markdown(pdf_path)
        m_article = MongoArticle(
            db_id=row["db_id"],
            title=row["title"],
            summary=row["summary"],
            file_path=str(pdf_path),
            arxiv_id=row["arxiv_id"],
            author=m_author,
            text=text_md,
        )
        m_article.save()
        print("Stored in Mongo:", row["arxiv_id"])
        return pd.Series([str(m_article.id)], index=["mongo_db_id"])
    except Exception as e:
        print("Mongo insert failed:", e)
        return pd.Series([""], index=["mongo_db_id"])


def create_in_mongo(df: pd.DataFrame) -> pd.DataFrame:
    ids = df.apply(store_article, axis=1)
    return pd.concat([df, ids], axis=1)
