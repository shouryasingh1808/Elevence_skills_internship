"""Task4 loader:  reads knowledge base files """

from pathlib import Path
from datetime import date
from Task_4.config import KB_FOLDER

def split_document(path):
    raw = Path(path).read_text(encoding="utf-8")
    parts = raw.split("---" , 2)
    return parts[1].strip() , parts[2].strip()

def parse_header(header):
    meta = {}
    for line in header.splitlines():
        if ":" in line:
            key , value = line.split(":" , 1)
            meta[key.strip()] = value.strip()
    return meta

def convert_types(meta):
    meta["version"] = int(meta["version"])
    meta["effective"] = date.fromisoformat(meta["effective"])
    meta["expires"] = None if meta["expires"].lower() == "none" else date.fromisoformat(meta["expires"])
    return meta

def load_documents(folder=KB_FOLDER):
    docs = []
    for path in sorted(Path(folder).glob("*.txt")):
        try:
            header, body = split_document(path)
            meta = convert_types(parse_header(header))
            meta["text"] = body
            meta["file"] = path.name
            docs.append(meta)
        except Exception as e:
            print(f"[skipped {path.name}: {e}]")
    return docs