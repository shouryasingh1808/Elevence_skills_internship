from datetime import datetime

from Task_1 import config as clock
from Task_2 import config
from Task_2.tickets import create_ticket ,tickets
from Task_2.routing import assign_ticket , release_ticket

tz = clock.TIMEZONE

def at(day, hour , minute = 0):
    return datetime(2026,10,day,hour,minute,tzinfo=tz)

def reset(when):
    tickets.clear()
    clock.set_time(when)
    for a in config.AGENTS:
        a["available"] = True
        a["workload"] = 0
        a["max_load"] = 5

def route(category,priority):
    t = assign_ticket(create_ticket(category = category , priority = priority))
    print(f"  {category:9} {priority} -> {t.queue:17} {str(t.assigned_to):6} | {t.routing_reason}")
    return t

print("1. Normal(Tue 11.00)")
reset(at(6,11))
route("billing" , "P2")
route("delivery" , "P3")
route("technical" , "P1")

print("2. Workload balance (3 general tickets)")
reset(at(6, 11))
for _ in range(3):
    route("general", "P4")

print("3. Billing agent unavailable")
reset(at(6, 11))
config.AGENTS[1]["available"] = False
route("billing", "P2")

print("4. Nobody available")
reset(at(6, 11))
for a in config.AGENTS:
    a["available"] = False
route("billing", "P2")
route("billing", "P1")

print("5. Max load reached (Priya max_load = 1)")
reset(at(6, 11))
config.AGENTS[1]["max_load"] = 1
route("billing", "P2")
route("billing", "P2")

print("6. After hours (Sun 22:30)")
reset(at(4, 22, 30))
route("billing", "P1")
t = route("billing", "P3")
print("  scheduled_for:", t.scheduled_for)

print("7. Release")
reset(at(6, 11))
t = route("billing", "P2")
print("  Priya workload:", config.AGENTS[1]["workload"])
release_ticket(t)
print("  after release:", config.AGENTS[1]["workload"], t.status)

reset(at(6, 11))
clock.clear_time()