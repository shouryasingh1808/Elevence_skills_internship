"""Task 3 config: Access_levels , tells location of knowledge base documents , rules of searches.."""

from pathlib import Path

ACCESS_LEVELS = {"public" : 0 , "customer" : 1 , "agent" : 2 , "admin" :3}

DEFAULT_USER_LEVEL = "customer"
KB_FOLDER = Path(__file__).resolve().parent.parent / "Data" / "kb"
MIN_SCORE = 0.1
MAX_CHUNKS = 3
