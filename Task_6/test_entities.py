from Task_6.entities import check_preserved

tests = [
    ("My order ORD-4521 arrived on 15 February 2026 and I paid Rs 499",
     "Mi pedido ORD-4521 llegó el 15 de febrero de 2026 y pagué Rs 499", ()),
    ("My order ORD-4521 arrived on 15 February 2026",
     "Mi pedido ORD-4512 llegó el 15 de febrero de 2026", ()),
    ("Refunds take 10 days [1]. Sources: refund_policy_v2.txt",
     "Los reembolsos tardan 10 días [1]. Fuentes: refund_policy_v2.txt", ()),
    ("Refunds take 10 days [1].", "Los reembolsos tardan diez días.", ()),
    ("Hello Priya, your code is E102", "Hola Priyaa, su código es E102", ("Priya",)),
]
for original, translated, names in tests:
    print(check_preserved(original, translated, names))