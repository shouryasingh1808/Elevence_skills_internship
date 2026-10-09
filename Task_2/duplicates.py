"""Task 2 duplicates: finds duplicate requests and groups related issues."""

from difflib import SequenceMatcher

from Task_1 import config as clock
from Task_2 import config
from Task_2.tickets import tickets

def similarity(a,b):
    if not a or not b:
        return 0.0
    return SequenceMatcher(None,a.lower() , b.lower()).ratio()

def same_value(a,b):
    return bool(a) and bool(b) and a.lower() == b.lower()

def open_recent_tickets():
    result = []
    for t in tickets.values():
        if t.status in ("resolved" , "closed" , "duplicate"):
            continue
        hours = (clock.get_now() - t.created_at).total_seconds() / 3600
        if hours <= config.DUPLICATE_WINDOW_HOURS:
            result.append(t)
    return result

def is_same_issue(info , t):
    if info["category"] != t.category:
        return False
    if info["order_id"] and t.order_id:
        return same_value(info["order_id"] , t.order_id)
    return (same_value(info["contact"] , t.contact)
                       and similarity(info["issue"] , t.issue) >= config.SIMILARITY_LIMMIT)

def is_related(info, t):
    return same_value(info["order_id"] , t.order_id) and info["category"] != t.category

def classify_issue(info):
    candidates =  open_recent_tickets()
    for t in candidates:
        if is_same_issue(info,t):
            return "duplicate" , t
    for t in candidates:
        if is_related(info , t):
            return "related" , t
    return "new" , None

def new_group_id():
    used = {t.group_id for t in tickets.values() if t.group_id}
    return f"GRP-{len(used) + 1:04d}"

def link_ticket(ticket , kind , other):
    if kind == "duplicate":
        ticket.status = "duplicate"
        ticket.duplicate_of = other.ticket_id
        other.events.append({
            "time" :clock.get_now().isoformat(),
            "event" : "duplicate_received",
            "detail" : f"{ticket.ticket_id} was the same request",
        })
    elif kind == "related":
        group = other.group_id or new_group_id()
        other.group_id = group
        ticket.group_id = group
    return ticket


