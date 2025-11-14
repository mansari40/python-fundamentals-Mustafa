from usecases.arxiv import fetch_arxiv_articles
from usecases.import_articles import create_in_relational_db
from usecases.export_articles import create_in_mongo
from usecases.search_text import search_text_index


def main() -> None:
    df = fetch_arxiv_articles("economics")
    df = create_in_relational_db(df)
    df = create_in_mongo(df)

    keyword = input("Enter keyword to search: ").strip()
    results = search_text_index(keyword)

    print(f"\nFound {len(results)} results for '{keyword}':")
    for a in results:
        print(f"- {a.arxiv_id}: {a.title}")


if __name__ == "__main__":
    main()

    # from pathlib import Path

    # from usecases.import_articles import import_articles
    # from usecases.export_articles import export_articles_to_mongo
    # from usecases.search_text import search_text

    # DATA_PATH = Path("data/articles.csv")
    # PAPERS_PATH = Path("data/Papers")

    # def main() -> None:
    #     import_articles(DATA_PATH)
    #     export_articles_to_mongo(PAPERS_PATH)

    #     keyword = input("\nEnter a search keyword: ").strip()
    #     search_text(keyword)

    # if __name__ == "__main__":
    #     main()
