from datetime import datetime , timedelta

from Task_1 import config as clock
from Task_2 import config
from Task_2.duplicates import classify_issue , link_ticket 
from Task_2.tickets import tickets , create_ticket

tz = clock.TIMEZONE
t0 = datetime(2026,10,6,11,0,tzinfo=tz)

def start():
    tickets.clear()
    clock.set_time(t0)
    return create_ticket(order_id="ORD-100" , category="delivery" , contact = "A@B.com" , issue  = "Order not delivered")

def incoming(label, hours_later , order_id , category , contact , issue):
    clock.set_time(t0 + timedelta(hours=hours_later))
    info = {"order_id" : order_id , "category" : category , "contact" : contact , "issue" : issue}
    kind , other = classify_issue(info)
    ticket = create_ticket(**info)
    link_ticket(ticket, kind , other)
    print(f"  {label:20} -> {kind:9} {ticket.ticket_id} status={ticket.status:9} "
          f"dup_of={ticket.duplicate_of} group={ticket.group_id}")
    return ticket

print("1. Same order, same category (1h later)")
start()
incoming("repeat message", 1, "ORD-100", "delivery", "a@b.com", "Still not delivered, please help")

print("2. Same order, different category")
first = start()
incoming("billing, same order", 1, "ORD-100", "billing", "a@b.com", "Charged twice for this order")
print("  original ticket group:", first.group_id)

print("3. Different order, same customer")
start()
incoming("different order", 1, "ORD-200", "delivery", "a@b.com", "Order not delivered")

print("4. No order ID, same customer, similar text")
start()
incoming("no order id", 1, None, "delivery", "a@b.com", "Order not delivered yet")

print("5. Same issue after the 24h window")
start()
incoming("30 hours later", 30, "ORD-100", "delivery", "a@b.com", "Order not delivered")

print("6. Original ticket already resolved")
first = start()
first.status = "resolved"
incoming("after resolve", 1, "ORD-100", "delivery", "a@b.com", "Order not delivered")

print("7. Unrelated customer and issue")
start()
incoming("other customer", 1, "ORD-900", "technical", "x@y.com", "App crashes on login")

clock.clear_time()