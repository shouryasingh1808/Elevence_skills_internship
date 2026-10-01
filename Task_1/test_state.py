from datetime import datetime , timedelta
from Task_1 import config
from Task_1.state import ConversationState

tz = config.TIMEZONE
t0 = datetime(2026, 10,1,12,0,tzinfo=tz)

s = ConversationState("s1")

config.set_time(t0)
s.update_with_analysis({"sentiment": "frustrated"})
print("1:" , s.negative_streak, round(s.minute_negative()
, 1))

config.set_time(t0 + timedelta(minutes=10))
s.update_with_analysis({"sentiment": "negative"})
print("2:" , s.negative_streak, round(s.minute_negative(), 1))

config.set_time(t0 + timedelta(minutes=16))
s.update_with_analysis({"sentiment": "sarcastic"})
print("3:" , s.negative_streak, round(s.minute_negative(), 1))

s.update_with_analysis({"sentiment": "positive"})
print("4:" , s.negative_streak,s.minute_negative(), s.resolved)

config.clear_time()