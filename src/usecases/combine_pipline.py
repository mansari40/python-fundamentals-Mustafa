from usecases.google import embed_documents
from usecases.export_articles import convert_to_markdown
from usecases.arxiv import load_from_xml
from pathlib import Path
from tqdm.auto import tqdm

tqdm.pandas(desc="Loading articles")


if __name__ == "__main__":
    with open("data/arxiv_articles_cut.xml", "r", encoding="utf-8") as f:
        xml_data = f.read()
        df = load_from_xml(xml_data)

    df["local_file_path"] = df["file_path"].apply(
        lambda p: str(Path("data") / "Papers" / Path(p).name)
    )
    df = df.pipe(convert_to_markdown)
    df = df.pipe(embed_documents)

    print("pipeline done")
    print("shape:", df.shape)
