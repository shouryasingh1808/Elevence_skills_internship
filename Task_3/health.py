"""Task 3 health: a small check that the live knowledge base still answers correctly."""

from Task_3.config import ACTIVE_KB , HEALTH_MIN_ACCURACY , HEALTH_SAMPLE
from Task_3.quality import load_questions , evaluate

def health_check(folder=None):
    folder = folder if folder is not None else ACTIVE_KB
    result = evaluate(folder, load_questions()[:HEALTH_SAMPLE])
    return {"healthy": result["accuracy"] >= HEALTH_MIN_ACCURACY,
            "accuracy": result["accuracy"], "failures": result["failures"]}