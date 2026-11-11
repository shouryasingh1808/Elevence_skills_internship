"""Task 3 scheduler: runs the update at a set time and retries failures after 15, 30 and 60 minutes."""

from datetime import datetime, timedelta

from Task_1 import config as clock
from Task_3.config import RETRY_DELAYS, SCHEDULE_TIME
from Task_3.scanner import load_manifest, save_manifest

NEW_STATE = {"next_run": None, "attempt": 0, "last_run_date": None, "status": "idle"}


def get_state(manifest):
    return manifest.setdefault("schedule", dict(NEW_STATE))


def due_time(state, now):
    if state["next_run"]:
        return datetime.fromisoformat(state["next_run"])
    if state["last_run_date"] == now.date().isoformat():
        return None
    return datetime.combine(now.date(), SCHEDULE_TIME, tzinfo=clock.TIMEZONE)


def tick(job):
    now = clock.get_now()
    state = get_state(load_manifest())
    due = due_time(state, now)
    if due is None or now < due:
        return {"ran": False, "status": state["status"]}

    try:
        result = job()
    except Exception as e:
        result = {"success": False, "error": f"job crashed: {e}"}

    manifest = load_manifest()
    state = get_state(manifest)
    today = now.date().isoformat()
    if result.get("success"):
        state.update(next_run=None, attempt=0, last_run_date=today, status="done")
        outcome = {"ran": True, "success": True}
    elif state["attempt"] < len(RETRY_DELAYS):
        delay = RETRY_DELAYS[state["attempt"]]
        state["attempt"] += 1
        state["next_run"] = (now + timedelta(minutes=delay)).isoformat()
        state["status"] = "retrying"
        outcome = {"ran": True, "success": False, "retry_in": delay,
                   "attempt": state["attempt"], "error": result.get("error")}
    else:
        state.update(next_run=None, attempt=0, last_run_date=today, status="gave_up")
        outcome = {"ran": True, "success": False, "gave_up": True, "error": result.get("error")}
    save_manifest(manifest)
    return outcome