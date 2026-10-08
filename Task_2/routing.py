"""Task 2 routing: picks an agent using skill, availability, workload and business hours."""

from Task_1 import config as clock
from Task_2 import config

def find_agent(category):
    candidates = [
        a for a in config.AGENTS
        if category in a["skills"] and a["available"] and a["workload"] < a["max_load"]
    ]
    if not candidates:
        return None
    return min(candidates , key = lambda a: a["workload"])

def assign_ticket(ticket):
    if not clock.is_business_hours():
        if ticket.priority == "P1":
            ticket.queue = "on_call_queue"
            ticket.routing_reason = "outside business hours, P1 goes to on-call"
        else:
            ticket.queue = "next_working_day"
            ticket.scheduled_for = clock.next_working_day_start().isoformat()
            ticket.routing_reason = "outside business hours, scheduled for next working day"
        return ticket

    agent = find_agent(ticket.category)
    reason = f"{ticket.category} skills , lowest workload"

    if agent is None and ticket.category != "general":
        agent = find_agent("general")
        reason = f"no {ticket.category} agent available, fell back to general"

    if agent is None:
        ticket.queue = "supervisor_queue" if ticket.priority == "P1" else "waiting_queue"
        ticket.routing_reason =  f"no available agent for {ticket.category}"
        return ticket

    agent["workload"] += 1
    ticket.assigned_to = agent["name"]
    ticket.queue = "agent"
    ticket.routing_reason = reason
    return ticket

def release_ticket(ticket):
    for a in config.AGENTS:
        if a["name"] == ticket.assigned_to and a["workload"] > 0:
            a["workload"] -= 1
        ticket.status = "resolved"

