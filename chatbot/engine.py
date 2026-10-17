from Task_1.pipeline import handle_message as task1_message , get_state , check_timeouts
from Task_2.pipeline import process_conversation
from Task_2.sla import check_all_tickets

ticketed = set()

def create_tickets_for(session_id , sentiment):
    state = get_state(session_id)
    lines = []
    outcomes = process_conversation(state.history , session_id , sentiment)
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

def handle_message(session_id, message):
    result = task1_message(session_id , message)
    state = get_state(session_id)
    
    extra = []
    outcomes = []

    if state.escalated and session_id not in ticketed:
        outcomes = process_conversation(state.history , session_id , result["analysis"]["sentiment"])

    reply = result["reply"]
    if extra:
        reply = reply + "\n\n" + "\n".join(extra)

    return {**result, "reply": reply, "tickets": outcomes}

def run_timeouts():
    records = check_timeouts()
    made = []
    for record in records:
        session_id = record["session_id"]
        if session_id in ticketed:
            continue
        _, outcomes = create_tickets_for(session_id, "negative")
        made += outcomes

    sla_events = check_all_tickets()
    return {"timeouts": records, "tickets": made, "sla_events": sla_events}