from datetime import datetime

from Task_1 import config as clock
from Task_2 import config
from Task_2.sla import add_business_hours , business_minutes_between

tz = clock.TIMEZONE

def at(day,hour,minute = 0):
    return datetime(2026,10,day,hour,minute,tzinfo=tz)

print("1 - Tue 11:00 +8h ->", add_business_hours(at(6, 11), 8))
print("2 - Sat 17:00 +8h ->", add_business_hours(at(3, 17), 8))
print("3 - Tue 22:00 +4h ->", add_business_hours(at(6, 22), 4))
print("4 - Sat 17:00 to Mon 10:00 minutes ->", business_minutes_between(at(3, 17), at(5, 10)))
print("5 - Sat 17:00 +8h (Oct 12 holiday) ->", add_business_hours(at(10, 17), 8))

config.HOLIDAYS.add("2026-10-05")  # routine change- monday is a holiday
print("6 - Sat 17:00 + 8h (Oct 5 also holiday) ->" , add_business_hours(at(3,17) , 8))
config.HOLIDAYS.discard("2026-10-05")