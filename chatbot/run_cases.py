"""Chatbot run_cases: runs the combined Task 1 + Task 2 test cases and shows PASS/FAIL"""

import json
from datetime import datetime, timedelta
from pathlib import Path

from Task_1 import config as clock
from Task_1 import pipeline as task1_pipeline
from Task_1 import records
from Task_2.run_cases import reset as reset_task2
from chatbot import engine
from chatbot.engine import handle_message, run_timeouts

DATA_DIR = Path(__file__).resolve().parent.parent / "Data"
CASES_FILE = DATA_DIR / "chatbot_test_cases.json"
TEST_RECORDS_FILE = DATA_DIR / "chatbot_test_escalations.jsonl"


def reset(setup):
    reset_task2(setup)
    task1_pipeline.sessions.clear()
    engine.ticketed.clear()
    records.RECORDS_FILE = TEST_RECORDS_FILE


def check_step(expect, created, reply, out):
    problems = []

    if "tickets_created" in expect and len(created) != expect["tickets_created"]:
        problems.append(f"tickets_created: expected {expect['tickets_created']}, got {len(created)}")

    if "priority" in expect:
        got = created[0].priority if created else None
        if got != expect["priority"]:
            problems.append(f"priority: expected {expect['priority']}, got {got}")

    if "queue" in expect:
        got = created[0].queue if created else None
        if got != expect["queue"]:
            problems.append(f"queue: expected {expect['queue']}, got {got}")

    if "reply_has" in expect and expect["reply_has"] not in reply:
        problems.append(f"reply: expected it to contain '{expect['reply_has']}'")

    if "timeouts" in expect:
        got = len(out.get("timeouts", []))
        if got != expect["timeouts"]:
            problems.append(f"timeouts: expected {expect['timeouts']}, got {got}")

    if "sla_events" in expect:
        got = [e["event"] for e in out.get("sla_events", [])]
        if got != expect["sla_events"]:
            problems.append(f"sla_events: expected {expect['sla_events']}, got {got}")

    return problems


def run_case(case):
    reset(case.get("setup", {}))
    start = datetime.fromisoformat(case["start"]).replace(tzinfo=clock.TIMEZONE)
    problems = []

    for number, step in enumerate(case["steps"], start=1):
        clock.set_time(start + timedelta(minutes=step["minutes"]))

        if "text" in step:
            result = handle_message(step.get("session", "s1"), step["text"])
            created = [o["ticket"] for o in result["tickets"] if o["status"] == "created"]
            reply = result["reply"]
            out = {}
        else:
            out = run_timeouts()
            created = [o["ticket"] for o in out["tickets"] if o["status"] == "created"]
            reply = ""

        found = check_step(step.get("expect", {}), created, reply, out)
        problems += [f"step {number}: {p}" for p in found]

    return problems


def main():
    with open(CASES_FILE, encoding="utf-8") as f:
        cases = json.load(f)

    passed = 0
    for case in cases:
        try:
            problems = run_case(case)
        except Exception as e:
            problems = [f"crashed: {e}"]

        if problems:
            print(f"FAIL  {case['name']}")
            for p in problems:
                print(f"      - {p}")
        else:
            print(f"PASS  {case['name']}")
            passed += 1

    clock.clear_time()
    print(f"\n{passed}/{len(cases)} passed")


if __name__ == "__main__":
    main()