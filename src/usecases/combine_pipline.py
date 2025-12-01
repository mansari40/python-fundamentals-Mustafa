from usecases.google import chunk_documents, embed_documents
from usecases.export_articles import convert_to_markdown
from usecases.arxiv import load_from_xml
from pathlib import Path
from usecases.vector import check_chunks_in_qdrant

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
    # df = df.pipe(save_to_qdrant)
    df = df.pipe(check_chunks_in_qdrant)

    df["embedding"] = None

    idx = df.index[~df["exists_in_qdrant"]][0]
    one = embed_documents(df.loc[[idx]].copy())
    df.at[idx, "embedding"] = one["embedding"].iloc[0]

    print(df["exists_in_qdrant"].value_counts())
    print("embeddings computed for missing chunks:", df["embedding"].notna().sum())
