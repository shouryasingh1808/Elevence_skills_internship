from datetime import datetime, time , timedelta
from zoneinfo import ZoneInfo

TIMEZONE = ZoneInfo("Asia/Kolkata")

# BUSSINESS HOURS -->
BUSINESS_DAYS = {0,1,2,3,4,5}  # Monday to saturday 
BUSINESS_START = time(9, 0)  # 9:00 AM
BUSINESS_END = time(18, 0)  # 6:00 PM

# Escalation thresholds
REPEATED_NEGATIVE_LIMIT = 3  # Number of repeated negative responses before escalation
UNRESOLVED_MINUTES_LIMIT = 15  # Time in minutes before escalation for unresolved issues
LOW_CONFIDENCE_THRESHOLD = 0.5  # Confidence threshold for escalation
NEGATIVE_LABELS = {"negative", "frustrated", "sarcastic", "poor"}  # Labels indicating negative sentiment

# simulated clock
_time_override = None

def set_time(dt):
    global _time_override
    _time_override = dt

def clear_time():
    global _time_override
    _time_override = None

def get_now():
    return _time_override or datetime.now(TIMEZONE) 

# --- Business hours helpers ---
def is_business_hours(dt=None):
    dt = (dt or get_now()).astimezone(TIMEZONE)
    return dt.weekday() in BUSINESS_DAYS and BUSINESS_START <= dt.time() < BUSINESS_END

# next working day start  -->
def next_working_day_start(dt=None):
    dt =(dt or get_now()).astimezone(TIMEZONE)
    candidate = dt.replace(
        hour = BUSINESS_START.hour , minute = BUSINESS_START.minute, second=0, microsecond=0)
    if dt.weekday() not in BUSINESS_DAYS or dt.time() >= BUSINESS_START:
        candidate += timedelta(days=1)
    while candidate.weekday() not in BUSINESS_DAYS: 
        candidate += timedelta(days=1)
    return candidate
