from pathlib import Path

from usecases.import_articles import import_articles
from usecases.export_articles import export_articles_to_mongo
from usecases.search_text import search_text

DATA_PATH = Path("data/articles.csv")
PAPERS_PATH = Path("data/Papers")


def main() -> None:
    import_articles(DATA_PATH)
    export_articles_to_mongo(PAPERS_PATH)

    keyword = input("\nEnter a search keyword: ").strip()
    search_text(keyword)


if __name__ == "__main__":
    main()
