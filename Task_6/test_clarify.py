from Task_1.analyzer import analyze_message
from Task_6.clarify import clarification_text, needs_clarification

tests = [
    "What is the refund policy?",
    "Hola, ¿cuál es la política de reembolso?",
    "Mera order ORD-4521 abhi tak nahi aaya",
    "Bonjour, ma commande n'est pas arrivée",
    "Guten Tag, wo ist meine Bestellung?",
    "ok",
    "???",
    "hmm",
]
for t in tests:
    a = analyze_message(t, [])
    reason = needs_clarification(a)
    print(f"{t!r} -> {a['language']} ({a['language_confidence']}) | intent {a['intent']} ({a['intent_confidence']}) | {reason}")
    if reason:
        print("    bot:", clarification_text(reason, a))