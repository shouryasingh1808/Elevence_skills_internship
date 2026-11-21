from datetime import datetime, timedelta

from Task_1 import config as clock
from Task_1 import pipeline as task1
import Task_6.sessions as sessions
import chatbot.engine as engine

sessions.customers.clear()
task1.sessions.clear()
engine.ticketed.clear()
engine.pending_questions.clear()
t0 = datetime(2026, 10, 6, 11, 0, tzinfo=clock.TIMEZONE)


def say(customer, minutes, text):
    clock.set_time(t0 + timedelta(minutes=minutes))
    r = engine.handle_message(customer, text)
    kb = r["kb"]["status"] if r["kb"] else None
    print(f"[{customer} +{minutes}] {text}")
    print(f"   {r['session']['session_id']} {r['session']['event']} | {r['analysis']['language']} | kb: {kb} | clarify: {r['clarification']}")
    print("   bot:", r["reply"].replace("\n", " | ")[:230])


say("sofia", 0, "¿Cuál es la política de reembolso?")
say("marc", 1, "Combien de temps dure la garantie ?")
say("riya", 2, "Mera order ORD-4521 abhi tak nahi aaya, aur refund policy kya hai?")
say("tara", 3, "How do I fix a fast draining battery?")
say("tara", 4, "laptop")
say("zed", 5, "ok")
say("asha", 6, "My order ORD-4521 has not arrived for 3 days")
say("asha", 51, "Any update on my order?")
say("asha", 51 + 25 * 60, "Hello again")
clock.clear_time()