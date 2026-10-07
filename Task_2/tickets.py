"""Task 2 tickets: the ticket card and a simple in-memory store."""

from dataclasses import dataclass , field

from Task_1 import config as clock

@dataclass
class Ticket:
    ticket_id: str
    customer: str | None = None
    order_id: str | None = None
    product: str | None = None
    issue: str | None = None
    category: str = "general"
    evidence: list = field(default_factory=list)
    contact: str | None = None
    severity: str = "medium"
    impact: str = "single_customer"
    priority_score: float = 0.0
    sla_status: str = "ok"
    warned: bool = False
    escalated: bool = False
    events: list = field(default_factory=list)
    sentiment: str = "neutral"
    priority: str = "P3"
    status: str = "open"
    created_at: object = None
    due_at: object = None
    assigned_to: str | None = None
    group_id: str | None = None
    duplicate_of: str | None = None
    session_id: str | None = None

tickets = {}

def create_ticket(**fields):
    ticket_id = f"TCK-{len(tickets) + 1:04d}"
    ticket = Ticket(ticket_id=ticket_id , **fields)
    ticket.created_at = clock.get_now()
    tickets[ticket_id] = ticket
    return ticket