from Task_1.pipeline import handle_message as task1_message , get_state
from Task_2.pipeline import process_conversation

ticketed = set()

def handel_message(session_id, message):
    result = task1_message(session_id , message)
    state = get_state(session_id)
    
    extra = []
    outcomes = []

    if state.escalated and session_id not in ticketed:
        outcomes = process_conversation(state.history , session_id , results["analysis"]["sentiment"])
    
        for r in outcomes:
            if r["status"] == "created":
                t = r["ticket"]
                extra.append(f"Ticket {t.ticket_id} created | priority {t.priority} | {t.assigned_to or t.queue}")
                ticketed.add(session_id)
            elif r["status"] == "duplicate":
                extra.append(f"This looks like a repeat of {r['duplicate_of']}, we are already working on it.")
                ticketed.add(session_id)
            elif r["status"] == "needs_info":
                extra.append(r["question"])

    reply = result["reply"]
    if extra:
        reply = reply + "\n\n" + "\n".join(extra)

    return {**result, "reply": reply, "tickets": outcomes}