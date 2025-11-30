from usecases.google import embed_documents
from usecases.export_articles import convert_to_markdown
from usecases.arxiv import load_from_xml
from pathlib import Path
from tqdm.auto import tqdm
from usecases.vector import save_to_qdrant, chunk_exists
import pandas as pd

tqdm.pandas(desc="Loading articles")


if __name__ == "__main__":
    with open("data/arxiv_articles_cut.xml", "r", encoding="utf-8") as f:
        xml_data = f.read()
        df = load_from_xml(xml_data)
        df["arxiv_id"] = df["arxiv_id"].astype(str)

    df["local_file_path"] = df["file_path"].apply(
        lambda p: str(Path("data") / "Papers" / Path(p).name)
    )
    df = df.pipe(convert_to_markdown)
    df = df.pipe(embed_documents)
    df = df.pipe(save_to_qdrant)

    check_row = pd.Series({"arxiv_id": df.iloc[0]["arxiv_id"], "chunk_index": 0})
    print("exists_in_qdrant:", bool(chunk_exists(check_row).iloc[0]))

    print("pipeline done")
    print("shape:", df.shape)
