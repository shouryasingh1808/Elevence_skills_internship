from datetime import datetime, timedelta

from Task_1 import config as clock
import Task_6.sessions as s

t0 = datetime(2026, 10, 6, 11, 0, tzinfo=clock.TIMEZONE)


def at(minutes):
    clock.set_time(t0 + timedelta(minutes=minutes))


def summarize(session_id):
    return f"summary of {session_id}"


def show(label, r):
    print(f"{label:<24}| {r['session_id']} {r['event']} | {r['summary']}")


s.customers.clear()
at(0);    show("asha first message", s.open_session("asha", summarize))
at(1);    show("ravi first message", s.open_session("ravi", summarize))
at(10);   show("asha after 10 min", s.open_session("asha", summarize))
at(39);   show("asha idle 29 min", s.open_session("asha", summarize))
at(70);   show("asha idle 31 min", s.open_session("asha", summarize))
at(100);  show("asha idle exactly 30", s.open_session("asha", summarize))
at(131);  print(f"{'sweep at +131':<24}|", s.expire_idle_sessions(summarize))
at(140);  show("asha after sweep", s.open_session("asha", summarize))
at(200);  show("tara first message", s.open_session("tara", summarize))
at(1442); show("ravi after 24h+1min", s.open_session("ravi", summarize))
at(1640); show("tara after exactly 24h", s.open_session("tara", summarize))
clock.clear_time()