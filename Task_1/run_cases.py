"""Runs the Task 1 test cases and prints PASS/FAIL for each one."""

import json
from datetime import datetime , timedelta
from pathlib import Path
from Task_1 import config , pipeline , records

DATA_DIR = Path(__file__).resolve().parent.parent/"Data"
CASES_FILE = DATA_DIR / "task1_test_cases.json"

records.RECORDS_FILE = DATA_DIR / "test_escalation.jsonl"

def run_case(case):
    pipeline.sessions.clear()
    start = datetime.fromisoformat(case["start"]).replace(tzinfo=config.TIMEZONE)

    result = None
    for minutes , text in case["messages"]:
        config.set_time(start + timedelta(minutes=minutes))
        result = pipeline.handle_message(case["name"] , text)

    problems = []

    sentiment = result["analysis"]["sentiment"]
    triggers = sorted(t["condition"] for t in result["triggers"])
    queue = result["route"]["queue"]
    scheduled = result["route"]["scheduled_for"] or ""

    if "expected_sentiment" in case and sentiment != case["expected_sentiment"]:
        problems.append(f"sentiment: expected {case['expected_sentiment']} , got {sentiment}")
    if "expected_triggers" in case and triggers != sorted(case["expected_triggers"]):
        problems.append(f"triggers: expected {case["expected_triggers"]}, got {triggers}")
    if "expected_queue" in case and queue != case["expected_queue"]:
        problems.append(f"queue: expected {case['expected_queue']} , got {queue}")
    if "expected_scheduled_prefix" in case and not scheduled.startswith(case["expected_scheduled_prefix"]):
        problems.append(f"scheduled_for: expected {case['expected_scheduled_prefix']}..., got {scheduled or None}")

    if "timeout_check_at" in case:
        config.set_time(start + timedelta(minutes = case["timeout_check_at"]))
        timed_out = len(pipeline.check_timeouts()) > 0
        if timed_out != case["expected_timeout"]:
            problems.append(f"timeout: expected{case["expected_timeout"]} , got {timed_out}")
    return problems

def main():
    with open(CASES_FILE , encoding="utf-8") as f:
        cases = json.load(f)

    passed = 0
    for case in cases :
        try:
            problems = run_case(case)
        except Exception as e:
            problems= [f"crashed: {e}"]
        
        if problems:
            print(f"FAIL  {case['name']}")
            for p in problems:
                print(f" -{p}")
        else:
            print(f"PASS  {case['name']}")
            passed += 1
    config.clear_time()
    print(f"\n{passed}/{len(cases)} passed")

if __name__ == "__main__":
    main()