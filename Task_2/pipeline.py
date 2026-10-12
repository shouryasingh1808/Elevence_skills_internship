from Task_2.extractor import extract_ticket_info , find_missing , question_for

from Task_2.tickets import create_ticket
from Task_2.priority import calculate_priority
from Task_2.duplicates import link_ticket , classify_issue
from Task_2.sla import get_due_time
from Task_2.routing import assign_ticket
from Task_2.handoff import build_handoff

def process_conversation(history , session_id):
    info = extract_ticket_info(history)
    if info["failed"]:
        return [{
            "status" : "extraction_failed" , "error" : info.get("error")
        }]
    results = []
    for issue in info["issues"]:
        missing = find_missing(info["contact"] , issue)
        if missing:
            results.append({
                "status" : "needs_info",
                "missing" : missing,
                "question" : question_for(missing)
            })
            continue

        kind , other = classify_issue({
            "order_id" : issue["order_id"],
            "category" : issue["category"],
            "contact" : info["contact"],
            "issue" : issue["issue"],
        })

        ticket = create_ticket(
            customer=info["customer_name"],
            order_id=issue["order_id"],
            product=issue["product"],
            issue=issue["issue"],
            category=issue["category"],
            evidence=issue["evidence"],
            contact=info["contact"],
            severity=issue["severity"],
            impact=issue["impact"],
            session_id=session_id,
        )
        link_ticket(kind,other,ticket)

        if kind == "duplicate":
            results.append({"status":"duplicate" , "ticket" : ticket , "duplicate_of" : other.ticket_id})
            continue

        score , priority , parts = calculate_priority(ticket)
        ticket.priority_score = score
        ticket.priority = priority
        ticket.due_at = get_due_time(ticket)
        assign_ticket(ticket)

        results.append({
            "status" : "created",
            "ticket" : ticket,
            "handoff" : build_handoff(ticket , history),
        })
    return results