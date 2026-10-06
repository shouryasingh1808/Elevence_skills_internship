"""Task 2 priority: turns severity, sentiment, waiting time and impact into P1-P4."""

from Task_1 import config as clock
from Task_2 import config

ORDER = ["P1", "P2" , "P3" , "P4" ]

def waiting_hours(ticket):
    if ticket.created_at is None:
        return 0.0
    seconds = (clock.get_now() - ticket.created_at).total_seconds()
    return max(seconds / 3600 , 0.0)

def calculate_priority(ticket):
    w = config.PRIORITY_WEIGHTS
    parts = {
        "severity" : w["severity"] * config.SEVERITY_LEVELS.get(ticket.severity , 0.4),
        "sentiment" : w["sentiment"] * config.SENTIMENT_LEVELS.get(ticket.sentiment , 0.1),
        "waiting"  : w["waiting"] * min(waiting_hours(ticket) / config.WAITING_FULL_HOURS , 1) , 
        "impact": w["impact"] * config.IMPACT_LEVELS.get(ticket.impact, 0.25),
    }
    score = round(sum(parts.values()) , 1)

    cutoffs = config.PRIORITY_CUTOFFS
    if score >= cutoffs["P1"]:
        priority  = "P1"
    elif score >= cutoffs["P2"]:
        priority = "P2"
    elif score >= cutoffs["P3"]:
        priority = "P3"
    else:
        priority = "P4"

    floor = config.PRIORITY_FLOOP.get(ticket.severity)
    if floor and ORDER.index(floor) < ORDER.index(priority):
        priority= floor

    return score , priority , parts
