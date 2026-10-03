"""Task 1 pipeline: runs one customer message through all the steps."""

from Task_1 import config
from Task_1.analyzer import analyze_message
from Task_1.state import ConversationState
from Task_1.escalation import check_escalation, route_complaint
from Task_1.records import build_record, save_record
from Task_1.responder import generate_reply

sessions = {}

def get_state(session_id):
    if session_id not in sessions:
        sessions[session_id] = ConversationState(session_id)
    return sessions[session_id]

def handle_message(session_id , message):
    state = get_state(session_id)
    history_before = list(state.history)

    analysis = analyze_message(message , history_before)
    state.add_message("customer" , message)
    state.update_with_analysis(analysis)

    triggers = check_escalation(state , analysis)
    route = route_complaint(analysis , triggers)

    record = None
    if triggers and not state.escalated:
        record = build_record(state , triggers , route)
        save_record(record)
        state.escalated = True
    
    reply = generate_reply(message , history_before , analysis , route)
    state.add_message("bot" , reply)
    return {
        "analysis" : analysis,
        "triggers": triggers,
        "route": route,
        "record": record,
        "reply": reply,
    }

def check_timeouts():
    """Escalate sessions that stayed negative too long, even without a new message."""
    escalated_now = []
    for state in sessions.values():
        if state.resolved or state.escalated:
            continue
        minutes = state.minutes_negative()
        if minutes> config.UNRESOLVED_MINUTES_LIMIT:
            triggers = [{
                "condition": "unresolved_negative_timeout",
                "reason": f"Negative conversation unresolved for {minutes:.0f} minutes "
                          f"(limit {config.UNRESOLVED_MINUTES_LIMIT})",
            }]
            analysis = {"sentiment" : "negative" , "is_complaint": True}
            route = route_complaint(analysis,triggers)
            record = build_record(state, triggers , route)
            save_record(record)
            state.escalated = True
            escalated_now.append(record)
    return escalated_now 