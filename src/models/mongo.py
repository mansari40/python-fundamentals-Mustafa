from datetime import datetime
from mongoengine import (
    EmbeddedDocument,
    IntField,
    StringField,
    DateTimeField,
    EmbeddedDocumentField,
    Document,
)


class Author(EmbeddedDocument):  # type: ignore[misc]
    db_id = IntField(required=True)
    full_name = StringField()
    title = StringField()


class ScientificArticle(Document):  # type: ignore[misc]
    meta = {
        "collection": "articles",
        "indexes": ["db_id", "arxiv_id", "$text"],
    }

    db_id: int = IntField(required=True)
    title: str = StringField()
    summary: str = StringField()
    file_path: str = StringField()
    created_at: datetime = DateTimeField()
    arxiv_id: str = StringField()
    author: Author = EmbeddedDocumentField(Author)
    text: str = StringField()
