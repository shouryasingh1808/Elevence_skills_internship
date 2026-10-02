"""Task 1 escalation: plain-Python rules that decide whether to escalate."""

from Task_1 import config

HIGH_RISK_TYPES = {"account_compromise", "duplicate_payment", "legal_threat"}

def check_escalation(state,analysis):
    triggers = []

    if state.negative_streak >= config.REPEATED_NEGATIVE_LIMIT:
        triggers.append({
            "condition" : "repeated_negative",
            "reason": f"{state.negative_streak} negative messages in a row "
                      f"(limit {config.REPEATED_NEGATIVE_LIMIT})",
        })

    risk = analysis["risk_type"]
    if risk in HIGH_RISK_TYPES:
        triggers.append({
            "condition" : "high_risk_issue",
            "reason": f"High-risk issue detected: {risk} "
                      f"(confidence {analysis['risk_confidence']})",
        })

    minutes = state.minutes_negative()
    if not state.resolved and minutes > config.UNRESOLVED_MINUTES_LIMIT:
        triggers.append({
            "condition" : "unresolved_negative_timeout",
            "reason": f"Negative conversation unresolved for {minutes:.0f} minutes "
                      f"(limit {config.UNRESOLVED_MINUTES_LIMIT})",
        })

    return triggers

#  ROUTE COMPLAINTS -->

def route_complaint(analysis , triggers):
    if not analysis["is_complaint"] and not triggers:
        return {"queue" : "none" , "scheduled_for" : None , "urgent" : False}

    urgent = analysis["sentiment"] == "urgent"  or any(t["condition"] == "high_risk_issue" for t in triggers)

    if config.is_business_hours():
        return {"queue" : "agent_queue" , "scheduled_for" : None , "urgent" : urgent}

    if urgent:
        return {"queue" : "on_call_queue" , "scheduled_for" : None , "urgent" : True}

    return {
        "queue": "next_working_day",
        "scheduled_for": config.next_working_day_start().isoformat(),
        "urgent": False,
    }