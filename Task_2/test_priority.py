from datetime import datetime , timedelta

from Task_1 import config as clock
from Task_2.tickets import Ticket
from Task_2.priority import calculate_priority

t0 = datetime(2026,10,6,11,0,tzinfo=clock.TIMEZONE)

def make(severity , sentiment , impact , hours_waited):
    clock.set_time(t0)
    ticket = Ticket(ticket_id="T" , severity=severity , sentiment=sentiment , impact=impact)
    ticket.created_at = t0
    clock.set_time(t0+timedelta(hours= hours_waited))
    return ticket

cases = [ 
     ("critical, neutral, single, fresh", "critical", "neutral", "single_customer", 0),
    ("medium, neutral, single, fresh", "medium", "neutral", "single_customer", 0),
    ("medium, frustrated, single, 12h", "medium", "frustrated", "single_customer", 12),
    ("high, frustrated, multiple, 24h", "high", "frustrated", "multiple_customers", 24),
    ("low, positive, single, fresh", "low", "positive", "single_customer", 0),
]

for name, sev,sent,imp,hrs in cases:
    score , priority , parts = calculate_priority(make(sev , sent,imp,hrs))
    print(f"{name:35} -> score{score:5} -> {priority}")

clock.clear_time()