from datetime import datetime

from Task_1 import config as clock
from chatbot.engine import handle_message

clock.set_time(datetime(2026, 10, 6, 11, 0, tzinfo=clock.TIMEZONE))


def run(session, text):
    r = handle_message(session, text)
    print(f"> {text}")
    print("  mood:", r["analysis"]["sentiment"], "| triggers:", [t["condition"] for t in r["triggers"]])
    print("  tickets:", [(x["status"], getattr(x.get("ticket"), "ticket_id", None)) for x in r["tickets"]])
    print("  reply:", r["reply"], "\n")


print("--- Scenario 1: repeated negative ---")
run("s1", "My order ORD-4521 has not arrived for 3 days")
run("s1", "No reply from you, this is terrible service")
run("s1", "This is the worst support ever, I am very angry. My email is a@b.com")

print("--- Scenario 2: calm high-risk, info missing ---")
run("s2", "Hello, I noticed two charges of Rs 499 on my statement for the same order. Could you please look into it?")
run("s2", "The order is ORD-777 and my email is c@d.com")

clock.clear_time()