from datetime import datetime

from Task_1 import config as clock
from chatbot.engine import handle_message

clock.set_time(datetime(2026, 10, 6, 11, 0, tzinfo=clock.TIMEZONE))

handle_message("s1", "Hello, I noticed two charges of Rs 499 on my statement for the same order. Could you please look into it?")
r = handle_message("s1", "The order is ORD-777 and my email is c@d.com")

t = r["tickets"][0]["ticket"]
print(t.severity, t.priority, t.assigned_to)

clock.clear_time()