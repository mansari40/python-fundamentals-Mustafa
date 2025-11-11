import csv
from pathlib import Path

from models.relational import ScientificArticle, Author
from storage.relational_db import Session


def import_articles(path: Path) -> None:
    with open(path, "r", encoding="utf-8") as f, Session() as session:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            author = Author(
                full_name=row["author_full_name"],
                title=row["author_title"],
            )
            article = ScientificArticle(
                title=row["title"],
                summary=row["summary"],
                file_path=row["file_path"],
                arxiv_id=row["arxiv_id"],
                author=author,
            )
            session.add(article)
        session.commit()


if __name__ == "__main__":
    import_articles(Path("data/articles.csv"))
