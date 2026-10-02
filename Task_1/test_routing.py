from datetime import datetime 
from Task_1 import config
from Task_1.escalation import route_complaint

tz = config.TIMEZONE

def at(y,m,d,h,mi):
    config.set_time(datetime(y,m,d,h,mi,tzinfo=tz))

urgent = {"sentiment" : "urgent", "is_complaint" : True, "risk_type" : "none"}
normal = {"sentiment" : "negative", "is_complaint" : True, "risk_type" : "none"}
thanks = {"sentiment" : "positive", "is_complaint" : False, "risk_type" : "none"}
calm = {"sentiment" : "neutral", "is_complaint" : True, "risk_type" : "duplicate_payment"}
risk_trigger = [{"condition" : "high_risk_issue", "reason" : "duplicate_payment"}]

at(2026 , 10 , 4 , 22 , 30)  # SUnday night 
print("A urgent , sun night: " , route_complaint(urgent , []))
print("B normal , sun night: " , route_complaint(normal , []))
print("C calm high_risk , Sun: " , route_complaint(calm , risk_trigger))

at(2026 , 10 , 6, 11 , 0)  # Tuesday 11 AM
print("D urgent, Tue 11:00:  " , route_complaint(urgent , []))

print("E thanks :   " , route_complaint(thanks , []))

config.clear_time()