from Task_2 import config
from Task_2.tickets import tickets , create_ticket

print("SLA: " , config.SLA_HOURS)
print("Agents: " , [a["name"] for a in config.AGENTS])

t1 = create_ticket(customer = "Shourya" , order_id = "ORD-4521" , issue = "Delivery late" , category = "delivery")
print(t1.ticket_id , t1.status, t1.priority , t1.created_at)

t2 = create_ticket(issue= "Payment deducted")
print(t2.ticket_id , t2.order_id , len(tickets))