"""Task3 config: folders and settings of the knowledge base update pipeline."""

from pathlib import Path
from datetime import time
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

GOLDEN_FILE = DATA / "golden_questions.json"
GOLDEN_TODAY = "2026-10-22"     
MAX_ACCURACY_DROP = 0.0         
MAX_GROUNDING_DROP = 0.0
MAINTENANCE_START = time(2, 0)
MAINTENANCE_END = time(4, 0)
HEALTH_WINDOW_MINUTES = 5
HEALTH_SAMPLE = 3
HEALTH_MIN_ACCURACY = 0.66
SCHEDULE_TIME = time(2,0)
RETRY_DELAYS = [15, 30 , 60]