"""Task 6 sessions: one session per customer, ended after idle time, summary restored on return."""

from datetime import timedelta

from Task_1 import config as clock
from Task_6.config import SESSION_IDLE_MINUTES, SESSION_RESTORE_HOURS

customers = {}


def start_record(customer_id, number, carried=None):
    return {"session_id": f"{customer_id}-s{number}", "number": number, "last_active": clock.get_now(),
            "status": "active", "summary": None, "carried_summary": carried}


def idle_minutes(record, now):
    return (now - record["last_active"]).total_seconds() / 60


def end_session(record, summarize):
    if record["status"] == "ended":
        return
    record["summary"] = summarize(record["session_id"]) if summarize else None
    record["status"] = "ended"


def open_session(customer_id, summarize=None):
    now = clock.get_now()
    record = customers.get(customer_id)

    if record is None:
        record = customers[customer_id] = start_record(customer_id, 1)
        return {"session_id": record["session_id"], "event": "new", "summary": None}

    if record["status"] == "active" and idle_minutes(record, now) >= SESSION_IDLE_MINUTES:
        end_session(record, summarize)

    if record["status"] == "active":
        record["last_active"] = now
        return {"session_id": record["session_id"], "event": "continuing", "summary": record["carried_summary"]}

    hours_away = (now - record["last_active"]).total_seconds() / 3600
    within = hours_away <= SESSION_RESTORE_HOURS
    carried = record["summary"] if within else None
    fresh = customers[customer_id] = start_record(customer_id, record["number"] + 1, carried)
    return {"session_id": fresh["session_id"], "event": "restored" if within else "new_after_expiry", "summary": carried}


def expire_idle_sessions(summarize=None):
    now = clock.get_now()
    ended = []
    for record in customers.values():
        if record["status"] == "active" and idle_minutes(record, now) >= SESSION_IDLE_MINUTES:
            end_session(record, summarize)
            ended.append(record["session_id"])
    return ended