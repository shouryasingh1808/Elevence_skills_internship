from datetime import datetime , timedelta
from Task_1 import config
from Task_1.pipeline import check_timeouts , get_state

t0 = datetime(2026 , 10,6,11,0,tzinfo=config.TIMEZONE)

config.set_time(t0)
s = get_state("timeout-demo")
s.add_message("customer" , "Its been 3 days and i didnt get my order")
s.update_with_analysis({"sentiment" : "frustrated"})

config.set_time(t0 + timedelta(minutes=5))
s.add_message("customer" , "I got no reply")
s.update_with_analysis({"sentiment" : "negative"})

for minutes in (10,15,16):
    config.set_time(t0+timedelta(minutes=minutes))
    result  = check_timeouts()
    print(f"+{minutes} min:", [r["conditions"] for r in result])
config.clear_time()