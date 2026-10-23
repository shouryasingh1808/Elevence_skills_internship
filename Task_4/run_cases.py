"""Task 4 run_cases: runs the knowledge assistant test cases and shows PASS/FAIL"""

import json 
from datetime import datetime
from pathlib import Path
from Task_1 import config as clock
from Task_4.assistant import answer_question
CASES_FILE = Path(__file__).resolve().parent.parent / "Data" / "task4_test_cases.json"
DEFAULT_TODAY = "2026-10-22"

def check_result(expect , result):
    problems = []
    text = " ".join((result["answer"] or "").lower().split())
    sources = result["sources"]
    if "status" in expect and result["status"] != expect["status"]:
        problems.append(f"status: expected {expect["status"]}, got: {result["status"]}")
    if "status_in" in expect and result["status"] not in expect["status_in"]:
        problems.append(f"status: expected one of {expect['status_in']}, got {result['status']}")
    if "sources" in expect and sources != expect["sources"]:
        problems.append(f"sources: expected {expect['sources']}, got {sources}")

    for name in expect.get("sources_include", []):
        if name not in sources:
            problems.append(f"sources: {name} should be used, got {sources}")
    
    for name in expect.get("sources_exclude", []):
        if name in sources:
            problems.append(f"sources: {name} must not be used")

    for word in expect.get("answer_has", []):
        if word.lower() not in text:
            problems.append(f"answer: should contain '{word}'")
    for word in expect.get("answer_lacks", []):
        if word.lower() in text:
            problems.append(f"answer: must not contain '{word}'")

    return problems

def run_case(case):
    today = datetime.fromisoformat(case.get("today" , DEFAULT_TODAY)).replace(tzinfo=clock.TIMEZONE)
    clock.set_time(today)
    result = answer_question(
        case["question"],
        user_level=case.get("user_level", "customer"),
        region=case.get("region"))
    
    return check_result(case["expect"], result)

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