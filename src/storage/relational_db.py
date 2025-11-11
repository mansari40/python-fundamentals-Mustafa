from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "mysql+pymysql://root:secret@localhost:3306/python-de"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10,
)


class Base(DeclarativeBase):  # type: ignore[misc]
    pass


Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    from models import relational  # noqa: F401

    Base.metadata.create_all(bind=engine)
