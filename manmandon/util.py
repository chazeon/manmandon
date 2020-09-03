from pathlib import Path
from urllib.parse import urlparse, unquote

def parse_url_fname(url: str) -> str:
    return unquote(Path(urlparse(url).path).name)
