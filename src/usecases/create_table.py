from storage.relational_db import Base, engine
from models.relational import ScientificArticle, Author  # noqa: F401

Base.metadata.create_all(engine)
