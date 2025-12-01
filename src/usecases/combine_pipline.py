from usecases.google import chunk_documents, embed_documents
from usecases.export_articles import convert_to_markdown
from usecases.arxiv import load_from_xml
from pathlib import Path
from usecases.vector import check_chunks_in_qdrant, save_to_qdrant
from storage.vector import COLLECTION_NAME, client

if __name__ == "__main__":
    with open("data/arxiv_articles_cut.xml", "r", encoding="utf-8") as f:
        xml_data = f.read()

    df = load_from_xml(xml_data)

    df["local_file_path"] = df["file_path"].apply(
        lambda p: str(Path("data") / "Papers" / Path(p).name)
    )

    df = df.pipe(convert_to_markdown)
    # df = df.pipe(embed_documents)
    df = df.pipe(chunk_documents)
    df = df.pipe(check_chunks_in_qdrant)

    missing = df[~df["exists_in_qdrant"]].head(1).copy()
    missing = missing.pipe(embed_documents)

    df["embedding"] = None
    df.loc[missing.index, "embedding"] = missing["embedding"]

    df = df.pipe(save_to_qdrant)

    print("points in qdrant:", client.count(collection_name=COLLECTION_NAME).count)
    print("embeddings computed:", df["embedding"].notna().sum())
