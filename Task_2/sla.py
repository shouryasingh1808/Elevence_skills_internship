"""Task 2 SLA: counts only working time (no weekends, no holidays)."""

from datetime import datetime , timedelta

from Task_1 import config as clock
from Task_2 import config

def is_working_day(day):
    return day.weekday() not in config.WEEKEND_DAYS and day.isoformat() not in config.HOLIDAYS

def day_window(day):
    start = datetime.combine(day , clock.BUSINESS_START , tzinfo=clock.TIMEZONE)
    end = datetime.combine(day , clock.BUSINESS_END , tzinfo=clock.TIMEZONE)
    return start, end

def next_day_start(day):
   return datetime.combine(day+timedelta(days=1) , clock.BUSINESS_START , tzinfo=clock.TIMEZONE)

def business_minutes_between(start , end):
    start = start.astimezone(clock.TIMEZONE)
    end = end.astimezone(clock.TIMEZONE)
    if end<=start:
        return 0.0

    total = 0.0
    day = start.date()
    while day<= end.date():
        if is_working_day(day):
            day_start , day_end = day_window(day)
            overlap_start = max(start, day_start)
            overlap_end = min(end, day_end)
            if overlap_end>overlap_start:
                total += (overlap_end - overlap_start).total_seconds()/60
        day += timedelta(days = 1)
    return total

def add_business_hours(start , hours):
    current = start.astimezone(clock.TIMEZONE)
    remaining = hours*60

    for _ in range(366):
        day = current.date()
        if not is_working_day(day):
            current = next_day_start(day)
            continue

        day_start , day_end = day_window(day)
        if current < day_start:
            current = day_start
        if current >= day_end:
            current = next_day_start(day)
            continue

        available = (day_end - current).total_seconds() / 60
        if remaining <= available:
            return current + timedelta(minutes=remaining)
        remaining -= available
        current = next_day_start(day)

    return current
            