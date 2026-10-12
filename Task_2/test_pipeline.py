from datetime import datetime , timedelta

from Task_1 import config as clock
from Task_2.pipeline import process_conversation
from Task_2.tickets import tickets

tz = clock.TIMEZONE
t0 = datetime(2026,10,6,11,0,tzinfo=tz)

def chat(text):
    return [{"role" : "customer" , "content" : text}]

def show(title , results):
    print(title)
    for r in results:
        t = r.get("tickets")
        if t:
            print(f" {r['status']:10} {t.ticket_id} {t.category:9} {t.priority}")
            f"{t.queue:8} {str(t.assigned_to):6} group={t.group_id} dup_of{t.duplicate_of}"

        else:
            print(f"  {r['status']:10} missing={r.get('missing')} | {r.get('question')}")
    print()

tickets.clear()
clock.set_time(t0)

show("1. Two problems in one message", process_conversation(
    chat("My order ORD-4521 has not arrived for 5 days. I was also charged twice for the same order. My email is rahul@gmail.com."),
    "s1"))

show("2. Missing information", process_conversation(
    chat("My app keeps crashing with error E102."), "s2"))

clock.set_time(t0 + timedelta(hours=1))
show("3. Same request again, 1 hour later", process_conversation(
    chat("ORD-4521 is still not delivered, please help. My email is rahul@gmail.com."), "s1"))

clock.clear_time()