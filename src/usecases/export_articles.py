from pathlib import Path
import requests
import pandas as pd
from urllib.parse import urlparse
import pymupdf4llm
from models.mongo import ScientificArticle as MongoArticle, Author as MongoAuthor
import storage.mongo  # noqa: F401
from mongoengine import DoesNotExist


def download_file(article: pd.Series) -> pd.Series:
    parsed = urlparse(article.file_path)
    if parsed.scheme:
        filename = Path(parsed.path).stem
        new_path = f"data/articles/{filename}.pdf"
        if not Path(new_path).exists():
            response = requests.get(article.file_path)
            with open(new_path, "wb") as f:
                f.write(response.content)
    else:
        new_path = article.file_path
    return pd.Series([new_path], index=["local_file_path"])


def convert_article_to_markdown(article: pd.Series) -> pd.Series:
    text = pymupdf4llm.to_markdown(article.local_file_path)
    with open(f"{article.local_file_path}.md", "w") as f:
        f.write(text)
    return pd.Series([text], index=["md_text"], dtype="string")


def store_article(article: pd.Series) -> pd.Series:
    try:
        m_author = MongoAuthor(
            db_id=article.author_db_id,
            full_name=article.author_full_name,
            title=article.author_title,
        )
        data = dict(
            db_id=article.db_id,
            title=article.title,
            summary=article.summary,
            file_path=article.file_path,
            arxiv_id=article.arxiv_id,
            author=m_author,
            text=article.md_text,
        )
        try:
            existing = MongoArticle.objects.get(arxiv_id=article.arxiv_id)
            existing.update(**data)
        except DoesNotExist:
            MongoArticle(**data).save()
        mongo_id = str(MongoArticle.objects.get(arxiv_id=article.arxiv_id).id)
        return pd.Series([mongo_id], index=["mongo_db_id"])
    except Exception:
        return pd.Series([""], index=["mongo_db_id"])


def create_in_mongo(df: pd.DataFrame) -> pd.DataFrame:
    ids = df.apply(store_article, axis=1)
    return pd.concat([df, ids], axis=1)


def download_files(df: pd.DataFrame) -> pd.DataFrame:
    filenames = df.apply(download_file, axis=1)
    return pd.concat([df, filenames], axis=1)


def convert_to_markdown(df: pd.DataFrame) -> pd.DataFrame:
    texts = df.apply(convert_article_to_markdown, axis=1)
    return pd.concat([df, texts], axis=1)
