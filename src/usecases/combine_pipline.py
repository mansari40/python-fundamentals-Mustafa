from usecases.google import embed_documents
from usecases.export_articles import convert_to_markdown
from pathlib import Path
import pandas as pd
from tqdm.auto import tqdm

tqdm.pandas(desc="Loading local papers")

if __name__ == "__main__":
    files = list(Path("data/Papers").glob("*.pdf"))
    df = pd.DataFrame({"local_file_path": [str(f) for f in files]})

    df = df.pipe(convert_to_markdown).pipe(embed_documents)

    print("shape:", df.shape)

    with pd.option_context("display.max_colwidth", 200):
        print(df.head())
