from datetime import datetime , timedelta
from Task_1 import config
from Task_1.state import ConversationState
from Task_1.escalation import check_escalation

tz = config.TIMEZONE
t0 = datetime(2026 , 10 , 6 , 11 , 0 , tzinfo=tz)
calm  = {"sentiment" : "neutral", "risk_type" : "none", "risk_confidence" : 0.0}

def names(triggers):
    return [t["condition"] for t in triggers]

# A: 3 negative message in a row
s = ConversationState("a")
s.negative_streak = 3
print("A:", names(check_escalation(s, calm)))

# B: Calm high_risk message
s = ConversationState("b")
ridk = {"sentiment" : "neutral", "risk_type" : "duplicate_payment", "risk_confidence" : 0.9}
print("B:", names(check_escalation(s, ridk)))

# C: negative for 16 minutes
s = ConversationState("c")
s.negative_streak = 1
s.negative_since = t0
config.set_time(t0 + timedelta(minutes=16))
print("C:", names(check_escalation(s, calm)))

# D: negative for exactly 15 minutes
config.set_time(t0 + timedelta(minutes=15))
print("D:", names(check_escalation(s, calm)))

# E: nothing wrong
s = ConversationState("e")
print("E:", names(check_escalation(s, calm)))

config.clear_time()