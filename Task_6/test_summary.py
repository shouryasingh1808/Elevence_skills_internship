from datetime import datetime, timedelta

from Task_1 import config as clock
from Task_1 import pipeline as task1
from Task_1.pipeline import get_state
import Task_6.sessions as sessions
from Task_6.summary import begin_session, summarize_history

history = [
    {"role": "customer", "content": "My order ORD-4521 has not arrived for 5 days. My email is rahul.sharma@gmail.com and my phone is 9876543210."},
    {"role": "bot", "content": "Sorry about that, a support agent will look into it."},
    {"role": "customer", "content": "Also I was charged twice for the same order. Please refund me."},
]
summary = summarize_history(history)
print(summary)
for secret in ["rahul.sharma@gmail.com", "9876543210"]:
    print("LEAK" if secret in summary else "SAFE", "-", secret)
print("order id kept:", "ORD-4521" in summary)

sessions.customers.clear()
task1.sessions.clear()
t0 = datetime(2026, 10, 6, 11, 0, tzinfo=clock.TIMEZONE)


def at(minutes):
    clock.set_time(t0 + timedelta(minutes=minutes))


at(0)
first = begin_session("asha")
for m in history:
    get_state(first["session_id"]).add_message(m["role"], m["content"])
at(1)
other = begin_session("ravi")
get_state(other["session_id"]).add_message("customer", "What is your refund policy?")

at(45)
back = begin_session("asha")
print(back["session_id"], back["event"])
print(get_state(back["session_id"]).history[0]["content"][:75])
print("ravi untouched:", len(get_state(other["session_id"]).history), "message(s)")
clock.clear_time()