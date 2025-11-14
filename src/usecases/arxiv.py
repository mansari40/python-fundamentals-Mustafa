import io
import requests
import pandas as pd

ARXIV_URL = "http://export.arxiv.org/api/query"


def fetch_arxiv_articles(query: str, max_results: int = 10) -> pd.DataFrame:
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
    }
    response = requests.get(ARXIV_URL, params=dict(params), timeout=15)  # type: ignore[arg-type]
    xml_data = response.text
    df = parse_xml_data(xml_data)
    df = add_html_content(df)
    return df


def parse_xml_data(xml_data: str) -> pd.DataFrame:
    file_like = io.StringIO(xml_data)
    df = pd.read_xml(
        file_like,
        xpath="/atom:feed/atom:entry",
        namespaces={"atom": "http://www.w3.org/2005/Atom"},
    )[["id", "title", "summary"]]

    df["author_title"] = "PhD"

    file_like = io.StringIO(xml_data)
    links = pd.read_xml(
        file_like,
        xpath="/atom:feed/atom:entry/atom:link[@title='pdf']",
        namespaces={"atom": "http://www.w3.org/2005/Atom"},
    )["href"]

    file_like = io.StringIO(xml_data)
    authors = pd.read_xml(
        file_like,
        xpath="/atom:feed/atom:entry/atom:author[1]",
        namespaces={"atom": "http://www.w3.org/2005/Atom"},
    )["name"]

    return pd.concat(
        [
            df.rename(columns={"id": "arxiv_id"}),
            links.rename("file_path"),
            authors.rename("author_full_name"),
        ],
        axis=1,
    )


def fetch_html_content(url: str) -> str:
    try:
        html_url = url.replace("/pdf/", "/abs/").replace(".pdf", "")
        r = requests.get(html_url, timeout=10)
        if r.status_code == 200:
            return str(r.text)
        else:
            return ""
    except Exception:
        return ""


def add_html_content(df: pd.DataFrame) -> pd.DataFrame:
    html_data = df["file_path"].apply(fetch_html_content)
    df["html_content"] = html_data
    return df
