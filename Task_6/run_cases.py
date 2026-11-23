"""Task 6 run_cases: runs multilingual and session test cases and shows PASS/FAIL"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path

from Task_1 import config as clock
from Task_1 import pipeline as task1_pipeline
from Task_1 import records
from Task_2.run_cases import reset as reset_task2
import Task_6.sessions as sessions
from Task_6.summary import summarize_session
from chatbot import engine

DATA_DIR = Path(__file__).resolve().parent.parent / "Data"
CASES_FILE = DATA_DIR / "task6_test_cases.json"
TEST_RECORDS_FILE = DATA_DIR / "task6_test_escalations.jsonl"
DEVANAGARI = re.compile(r"[\u0900-\u097F]")
DEFAULT_START = "2026-10-06T11:00:00"


def reset():
    reset_task2({})
    task1_pipeline.sessions.clear()
    engine.ticketed.clear()
    engine.pending_questions.clear()
    sessions.customers.clear()
    records.RECORDS_FILE = TEST_RECORDS_FILE


def check_step(expect, result):
    problems = []
    language = result["analysis"]["language"]
    kb = result["kb"]
    reply = " ".join(result["reply"].split())
    session = result["session"]
    created = [o for o in result["tickets"] if o["status"] == "created"]

    if "language_in" in expect and language not in expect["language_in"]:
        problems.append(f"language: expected one of {expect['language_in']}, got {language}")
    if "session_event" in expect and session["event"] != expect["session_event"]:
        problems.append(f"session event: expected {expect['session_event']}, got {session['event']}")
    if "kb_status" in expect:
        got = kb["status"] if kb else None
        if got != expect["kb_status"]:
            problems.append(f"kb_status: expected {expect['kb_status']}, got {got}")
    if "clarification_in" in expect and result["clarification"] not in expect["clarification_in"]:
        problems.append(f"clarification: expected one of {expect['clarification_in']}, got {result['clarification']}")
    for word in expect.get("reply_has", []):
        if word not in reply:
            problems.append(f"reply: should contain '{word}'")
    for word in expect.get("reply_lacks", []):
        if word in reply:
            problems.append(f"reply: must not contain '{word}'")
    if "reply_script" in expect:
        has_devanagari = bool(DEVANAGARI.search(result["reply"]))
        if expect["reply_script"] == "devanagari" and not has_devanagari:
            problems.append("reply: should be written in Devanagari")
        if expect["reply_script"] == "roman" and has_devanagari:
            problems.append("reply: must not contain Devanagari")
    if "tickets_created" in expect and len(created) != expect["tickets_created"]:
        problems.append(f"tickets_created: expected {expect['tickets_created']}, got {len(created)}")
    if "ticket_order" in expect:
        orders = [o["ticket"].order_id for o in created]
        if expect["ticket_order"] not in orders:
            problems.append(f"ticket order: expected {expect['ticket_order']}, got {orders}")
    if "summary_has" in expect and expect["summary_has"] not in (session["summary"] or ""):
        problems.append(f"summary: should contain '{expect['summary_has']}', got {session['summary']!r}")
    if expect.get("no_summary") and session["summary"] is not None:
        problems.append("summary: a session after 24 hours must start without a summary")
    return problems


def check_sweep(expect, ended):
    return [f"sessions_ended: {name} should have ended, got {ended}"
            for name in expect.get("sessions_ended_include", []) if name not in ended]


def run_case(case):
    reset()
    start = datetime.fromisoformat(case.get("start", DEFAULT_START)).replace(tzinfo=clock.TIMEZONE)
    problems = []
    for number, step in enumerate(case["steps"], start=1):
        clock.set_time(start + timedelta(minutes=step["minutes"]))
        if step.get("sweep"):
            found = check_sweep(step.get("expect", {}), sessions.expire_idle_sessions(summarize_session))
        else:
            result = engine.handle_message(step["customer"], step["text"])
            found = check_step(step.get("expect", {}), result)
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