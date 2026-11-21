"""Chatbot engine: sessions and languages (Task 6), mood and escalation (Task 1), tickets (Task 2) and knowledge base answers (Task 4)."""

import time

from Task_1.pipeline import handle_message as task1_message, get_state, check_timeouts
from Task_2.pipeline import process_conversation
from Task_2.sla import check_all_tickets
from Task_3 import monitor
from Task_4.assistant import answer_question
from Task_4.config import DEFAULT_USER_LEVEL
from Task_6.clarify import canonical_language, clarification_text, needs_clarification
from Task_6.config import BASE_LANGUAGE, FOLLOWUP_MAX_WORDS
from Task_6.sessions import expire_idle_sessions
from Task_6.summary import begin_session, summarize_session
from Task_6.translate import fix_spelling, localize_kb, translate_answer, translate_question

ticketed = set()
pending_questions = {}


def create_tickets_for(session_id, sentiment):
    state = get_state(session_id)
    lines = []
    outcomes = process_conversation(state.history, session_id, sentiment, state.risk_type)
    for r in outcomes:
        if r["status"] == "created":
            t = r["ticket"]
            lines.append(f"Ticket {t.ticket_id} created | priority {t.priority} | {t.assigned_to or t.queue}")
            ticketed.add(session_id)
        elif r["status"] == "duplicate":
            lines.append(f"This looks like a repeat of {r['duplicate_of']}, we are already working on it.")
            ticketed.add(session_id)
        elif r["status"] == "needs_info":
            lines.append(r["question"])
    return lines, outcomes


def localize_text(text, language):
    if language == BASE_LANGUAGE:
        return text
    translated = translate_answer(text, language)
    return translated["text"] if translated["ok"] else text


def run_knowledge_base(message, language, user_level, region, prefix=None):
    translated = translate_question(message, language)
    if not translated["ok"]:
        return {"status": "error", "answer": None, "sources": []}, None
    english = f"{prefix} {translated['text']}" if prefix else translated["text"]
    kb = answer_question(english, user_level=user_level, region=region)
    if kb["status"] == "refused":
        fixed = fix_spelling(english)
        if fixed != english:
            retry = answer_question(fixed, user_level=user_level, region=region)
            if retry["status"] != "refused":
                kb, english = retry, fixed
    return kb, english


def handle_message(customer_id, message, user_level=DEFAULT_USER_LEVEL, region=None):
    started = time.perf_counter()
    session = begin_session(customer_id)
    session_id = session["session_id"]

    result = task1_message(session_id, message)
    state = get_state(session_id)
    analysis = result["analysis"]
    escalating = bool(result["triggers"]) or analysis["risk_type"] != "none"

    pending = pending_questions.pop(session_id, None)
    is_followup = pending is not None and not escalating and len(message.split()) <= FOLLOWUP_MAX_WORDS
    language = pending["language"] if is_followup else canonical_language(analysis["language"])

    reason = None if (escalating or is_followup) else needs_clarification(analysis)
    wants_kb = analysis["intent"] == "question" or analysis.get("has_question", False)

    kb = None
    if is_followup:
        kb, english = run_knowledge_base(message, language, user_level, region, prefix=pending["english"])
    elif wants_kb and not escalating and reason is None:
        kb, english = run_knowledge_base(message, language, user_level, region)
    if kb is not None and kb["status"] == "clarify" and english:
        pending_questions[session_id] = {"english": english, "language": language}

    if reason is not None:
        reply = clarification_text(reason, analysis)
    elif kb is None:
        reply = result["reply"]
    elif analysis["intent"] == "question" or is_followup:
        reply = localize_kb(kb, language)
    else:
        reply = result["reply"] + "\n\n" + localize_kb(kb, language)

    extra, outcomes = [], []
    if state.escalated and session_id not in ticketed:
        extra, outcomes = create_tickets_for(session_id, analysis["sentiment"])
    if extra:
        reply = reply + "\n\n" + localize_text("\n".join(extra), language)

    output = {**result, "reply": reply, "tickets": outcomes, "kb": kb,
              "session": session, "clarification": reason}
    monitor.record_message(output, (time.perf_counter() - started) * 1000)
    return output


def run_timeouts():
    records = check_timeouts()
    made = []
    for record in records:
        session_id = record["session_id"]
        if session_id in ticketed:
            continue
        _, outcomes = create_tickets_for(session_id, "negative")
        made += outcomes

    ended = expire_idle_sessions(summarize_session)
    sla_events = check_all_tickets()
    return {"timeouts": records, "tickets": made, "sessions_ended": ended, "sla_events": sla_events}