from datetime import datetime
from Task_1 import config 

tz = config.TIMEZONE

def at(y,m,d,h,mi):
    config.set_time(datetime(y,m,d,h,mi, tzinfo=tz))

at(2026, 10, 6, 11, 0);  print("Tue 11:00 ->", config.is_business_hours())
at(2026, 10, 6, 22, 30); print("Tue 22:30 ->", config.is_business_hours())
at(2026, 10, 4, 11, 0);  print("Sun 11:00 ->", config.is_business_hours())
at(2026, 10, 3, 17, 59); print("Sat 17:59 ->", config.is_business_hours())
at(2026, 10, 3, 18, 0);  print("Sat 18:00 ->", config.is_business_hours())

print("--Next working day start--")
at(2026, 10, 3, 19, 0);  print("Sat 19:00 -> next:", config.next_working_day_start())
at(2026, 10, 5, 7, 0);   print("Mon 07:00 -> next:", config.next_working_day_start())
at(2026, 10, 6, 22, 30); print("Tue 22:30 -> next:", config.next_working_day_start())

config.clear_time()