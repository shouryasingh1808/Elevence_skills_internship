from Task_1.analyzer import analyze_message
from Task_2.extractor import extract_ticket_info, find_contact
from Task_6.translate import fix_spelling

for t in ["What is the refund policy?", "My order ORD-4521 is late and what is your refund policy?",
          "My order ORD-4521 is late", "Thanks!"]:
    a = analyze_message(t, [])
    print(a["intent"], a["has_question"], "|", t)

print(find_contact("my email is old@x.com. Sorry, the right one is new@y.com"))
print(find_contact("call me on 9876543210"), find_contact("no contact here"))

history = [
    {"role": "customer", "content": "My order ORD-55 has not arrived for 5 days. My email is a@b.com."},
    {"role": "customer", "content": "Sorry, I made a mistake, my order is ORD-77, not ORD-55. The correct email is c@d.com."},
]
info = extract_ticket_info(history)
print(info["contact"], [i["order_id"] for i in info["issues"]])

print(fix_spelling("wat is the refnd polcy for ordr ORD-4521"))
print(fix_spelling("What is the refund policy?"))