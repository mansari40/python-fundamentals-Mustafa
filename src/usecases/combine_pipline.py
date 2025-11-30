from usecases.google import chunk_documents, embed_documents
from usecases.export_articles import convert_to_markdown
from usecases.arxiv import load_from_xml
from pathlib import Path

from usecases.vector import save_to_qdrant
import pandas as pd


if __name__ == "__main__":
    with open("data/arxiv_articles_cut.xml", "r", encoding="utf-8") as f:
        xml_data = f.read()

    df = load_from_xml(xml_data)

    df["local_file_path"] = df["file_path"].apply(
        lambda p: str(Path("data") / "Papers" / Path(p).name)
    )

    df = df.pipe(convert_to_markdown)
    df = df.pipe(embed_documents)
    df = df.pipe(save_to_qdrant)

    df_chunks = df.pipe(chunk_documents)

    print(df.shape)
    print(df_chunks.shape)

    view_cols = ["arxiv_id", "chunk_index", "chunk_text"]
    with pd.option_context("display.max_colwidth", 140):
        print(df_chunks[view_cols].head(8))
