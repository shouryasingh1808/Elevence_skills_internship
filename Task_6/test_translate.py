from Task_6.translate import localize_kb, translate_question

questions = [
    ("¿Cuál es la política de reembolso del pedido ORD-4521?", "Spanish"),
    ("Quelle était la politique de remboursement le 15 février 2026 ?", "French"),
    ("Mera order ORD-4521 ka refund kitne din mein milta hai?", "Hinglish"),
    ("मेरा ऑर्डर ORD-4521 कब तक आएगा?", "Hindi"),
]
for q, lang in questions:
    r = translate_question(q, lang)
    print(lang, "->", r["ok"], "|", r["text"])

kb = {"status": "answered", "answer": "You can request a refund within 10 days of delivery [1].",
      "sources": ["refund_policy_v2.txt"]}
for lang in ["Spanish", "French", "Hindi", "Hinglish"]:
    print(lang, "->", localize_kb(kb, lang).replace("\n", " | "))
print(localize_kb({"status": "refused", "answer": "I don't have that information.", "sources": []}, "Hinglish"))