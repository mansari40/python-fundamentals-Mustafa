from pathlib import Path
from sqlalchemy.orm import joinedload
from storage.relational_db import Session
from models.relational import ScientificArticle as SQLArticle
from models.mongo import ScientificArticle as MongoArticle, Author as MongoAuthor
import storage.mongo  # noqa: F401
import fitz
import markdownify


def export_articles_to_mongo(papers_dir: Path) -> None:
    with Session() as session:
        articles = (
            session.query(SQLArticle).options(joinedload(SQLArticle.author)).all()
        )

        for article in articles:
            if not article.author:
                continue

            pdf_path = papers_dir / Path(article.file_path).name
            try:
                with fitz.open(pdf_path) as pdf:
                    text = "\n".join(page.get_text("text") for page in pdf)
            except Exception:
                continue

            text_md = markdownify.markdownify(text)

            author_doc = MongoAuthor(
                db_id=article.author.id,
                full_name=article.author.full_name or "",
                title=article.author.title or "",
            )

            mongo_doc = MongoArticle(
                db_id=article.id,
                title=article.title or "",
                summary=article.summary or "",
                file_path=str(pdf_path),
                arxiv_id=article.arxiv_id or "",
                created_at=article.created_at,
                author=author_doc,
                text=text_md or "",
            )

            mongo_doc.save(validate=False)


if __name__ == "__main__":
    export_articles_to_mongo(Path("data/Papers"))
