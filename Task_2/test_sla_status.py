from datetime import datetime

from Task_1 import config as clock
from Task_2 import config
from Task_2.tickets import create_ticket , tickets
from Task_2.sla import check_all_tickets , check_sla

tz = clock.TIMEZONE

def at(day, hour , minute = 0):
    return datetime(2026,10,day,hour,minute, tzinfo=tz)

def new_ticket(when,priority = "P2"):
    tickets.clear()
    clock.set_time(when)
    return create_ticket(priority=priority)

def show(label , ticket , when):
    clock.set_time(when)
    events = check_all_tickets()
    info = check_sla(ticket)
    names = [e["event"] for e in events]
    print(f"{label:22} {info['percent']:6}%  {ticket.sla_status:9} {ticket.status:10} {names}")

# A: Tuesday 9:00 ko P2 ticket (8h SLA), deadline Tue 17:00
t = new_ticket(at(6,9))
show("A 14:59", t, at(6, 14, 59))
show("A 15:00", t, at(6, 15))
show("A 17:00", t, at(6, 17))
show("A 17:01", t, at(6, 17, 1))
show("A 17:48", t, at(6, 17, 48))
print()

# B: Saturday at 17:00 ticket, Sunday
t = new_ticket(at(3, 17))
show("B Sun 12:00", t, at(4, 12))
show("B Mon 14:00", t, at(5, 14))
print()

# C: change runtime on SLA(P2: 8h --> 4h)
t = new_ticket(at(6,9))
config.SLA_HOURS["P2"] = 4
show("C 12:00 (P2=4h)", t, at(6, 12))
config.SLA_HOURS["P2"] = 8
show("C 12:00 (P2=8h)", t, at(6, 12))

clock.clear_time()