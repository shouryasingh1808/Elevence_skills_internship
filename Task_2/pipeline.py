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
            customer = info["customer_name"],
            order_id = issue["order_id"],
            
        )