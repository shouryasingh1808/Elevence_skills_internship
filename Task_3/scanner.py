"""Task 3 scanner: finds new, changed and duplicate documents."""

import hashlib
from pathlib import Path

def file_hash(path):
    text = Path(path).read_text(encoding="utf-8").replace("\r\n", "\n").strip()  # This is only because i regularly shifts on Mac and PC..
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
