import re
from html import unescape

def strip_html(html: str) -> str:
    clean = re.sub(r"<.*?>", "", html)
    return unescape(clean.strip())