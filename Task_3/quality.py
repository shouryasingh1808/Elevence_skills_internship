"""Task 3 quality gate: tests a candidate knowledge base against golden questions."""

import json
from datetime import datetime

from Task_1 import config as clock
from Task_3.config import ACTIVE_KB, GOLDEN_FILE, GOLDEN_TODAY, MAX_ACCURACY_DROP, MAX_GROUNDING_DROP
from Task_4.assistant import answer_question
from Task_4.loader import load_documents
from Task_4.run_cases import check_result


def load_questions():
    return json.loads(GOLDEN_FILE.read_text(encoding="utf-8"))


def evaluate(folder, questions=None):
    questions = questions if questions is not None else load_questions()
    docs = load_documents(folder)
    previous = clock.get_override()
    passed = answered = rejected = 0
    failures = []

    for q in questions:
        day = datetime.fromisoformat(q.get("today", GOLDEN_TODAY)).replace(tzinfo=clock.TIMEZONE)
        clock.set_time(day)
        result = answer_question(q["question"], user_level=q.get("user_level", "customer"),
                                 region=q.get("region"), docs=docs)
        problems = check_result(q["expect"], result)
        if problems:
            failures.append({"question": q["question"], "problems": problems})
        else:
            passed += 1
        if result["status"] == "answered":
            answered += 1
        elif result["status"] == "rejected":
            rejected += 1

    if previous is None:
        clock.clear_time()
    else:
        clock.set_time(previous)

    grounding = answered / (answered + rejected) if answered + rejected else 1.0
    return {"accuracy": passed / max(len(questions), 1), "grounding": grounding, "failures": failures}


def compare(baseline, candidate):
    reasons = []
    if candidate["accuracy"] < baseline["accuracy"] - MAX_ACCURACY_DROP:
        reasons.append(f"accuracy dropped from {baseline['accuracy']:.2f} to {candidate['accuracy']:.2f}")
    if candidate["grounding"] < baseline["grounding"] - MAX_GROUNDING_DROP:
        reasons.append(f"grounding dropped from {baseline['grounding']:.2f} to {candidate['grounding']:.2f}")
    return reasons

def quality_gate(candidate_folder, baseline=None, baseline_folder=None):
    baseline_folder = baseline_folder if baseline_folder is not None else ACTIVE_KB
    baseline = baseline if baseline is not None else evaluate(baseline_folder)
    candidate = evaluate(candidate_folder)
    reasons = compare(baseline, candidate)
    return {"approved": not reasons, "reasons": reasons, "baseline": baseline, "candidate": candidate}