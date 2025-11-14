from pathlib import Path
import pandas as pd

from sqlalchemy.exc import IntegrityError
from models.relational import ScientificArticle, Author
from storage.relational_db import Session


def load_data_from_csv(path: str) -> pd.DataFrame:
    file_path = Path(path)
    df = pd.read_csv(file_path, delimiter=";", dtype="string")
    return df


def insert_article(row: pd.Series) -> pd.Series:
    with Session() as session:
        try:
            author = Author(
                full_name=row["author_full_name"], title=row["author_title"]
            )
            article = ScientificArticle(
                title=row["title"],
                summary=row["summary"][:500],
                file_path=row["file_path"],
                arxiv_id=row["arxiv_id"],
                author=author,
            )
            session.add(article)
            session.commit()
            session.refresh(article)
            print("Inserted:", article.arxiv_id)
            return pd.Series([article.id, author.id], index=["db_id", "author_db_id"])
        except IntegrityError as err:
            print("Duplicate or error:", err)
            return pd.Series([0, 0], index=["db_id", "author_db_id"])


def create_in_relational_db(df: pd.DataFrame) -> pd.DataFrame:
    ids = df.apply(insert_article, axis=1)
    return pd.concat([df, ids], axis=1)
