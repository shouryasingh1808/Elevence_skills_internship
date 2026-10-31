"""Task3 config: folders and settings of the knowledge base update pipeline."""

from pathlib import Path
from Task_4.config import KB_FOLDER

DATA = Path(__file__).resolve().parent.parent / "Data"

ACTIVE_KB = KB_FOLDER
INCOMING = DATA/"incoming"
QUARANTINE = DATA/"quarantine"
VERSIONS = DATA/"versions"
MANIFEST_FILE = (DATA / "pipeline_manifest.json")

def ensure_folders():
    for folder in (INCOMING , QUARANTINE , VERSIONS):
        folder.mkdir(parents=True , exist_ok=True)