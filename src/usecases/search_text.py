import storage.mongo  # noqa: F401
from models.mongo import ScientificArticle


def search_text(keyword: str) -> None:
    results = ScientificArticle.objects.search_text(keyword)
    for a in results:
        print(f"{a.arxiv_id}: {a.title}")


def search_icontains(keyword: str) -> None:
    results = ScientificArticle.objects(text__icontains=keyword)
    for a in results:
        print(f"{a.arxiv_id}: {a.title}")


if __name__ == "__main__":
    search_icontains("Africa")
    search_text("Africa")
