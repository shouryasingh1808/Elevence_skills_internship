from datetime import datetime, timedelta

from Task_1 import config as clock
from Task_2 import config
from chatbot.engine import handle_message, run_timeouts

t0 = datetime(2026, 10, 6, 11, 0, tzinfo=clock.TIMEZONE)
config.SLA_HOURS.update({"P1": 1, "P2": 1, "P3": 1, "P4": 1})


def at(minutes):
    clock.set_time(t0 + timedelta(minutes=minutes))


at(0)
handle_message("s1", "My order ORD-4521 has not arrived for 3 days, I am very disappointed. My email is a@b.com")
at(5)
handle_message("s1", "Still no reply, this is bad service")

for minutes in (10, 16, 17, 62, 77):
    at(minutes)
    r = run_timeouts()
    print(f"+{minutes:>2} min | timeouts: {[x['conditions'] for x in r['timeouts']]}"
          f" | tickets: {[(o['status'], getattr(o.get('ticket'), 'ticket_id', None)) for o in r['tickets']]}"
          f" | sla: {[e['event'] for e in r['sla_events']]}")

clock.clear_time()