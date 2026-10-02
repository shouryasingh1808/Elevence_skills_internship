from datetime import datetime
import json
from Task_1 import config
from Task_1.state import ConversationState
from Task_1.escalation import check_escalation, route_complaint
from Task_1.records import build_record, save_record

config.set_time(datetime(2026, 10, 4, 22, 30, tzinfo=config.TIMEZONE))

s = ConversationState("demo-1")
s.add_message("customer", "I am very upset about the duplicate payment issue.")
s.add_message("bot" , "I understand your concern. Let me check your account.")
s.add_message("customer", "This is unacceptable. I want a refund immediately.")

analysis = {
    "sentiment": "urgent", "is_complaint": True,
    "risk_type": "duplicate_payment", "risk_confidence": 0.9,
}

triggers = check_escalation(s, analysis)
route = route_complaint(analysis, triggers)
record = build_record(s, triggers, route)
save_record(record)

print(json.dumps(record, indent=2 , ensure_ascii=False))
config.clear_time()