from Task_1.analyzer import analyze_message

cases = [
    ("What is your refund policy?", "question"),
    ("How long does standard delivery take?", "question"),
    ("Do you offer a warranty on laptops?", "question"),
    ("Is shipping free above Rs 499?", "question"),
    ("Can you tell me how to fix a laptop battery drain?", "question"),
    ("My order has not arrived for 5 days", "complaint"),
    ("Thanks, my problem is solved!", "complaint"),
    ("I was charged twice for my order", "complaint"),
    ("My order is late and I want to know what your refund policy is", "complaint"),
    ("This is the worst service ever", "complaint"),
    ("How do I fix a fast draining battery?", "question"),
    ("How can I set up my new phone?", "question"),
    ("My laptop battery drains fast", "complaint"),
    ("I was charged twice, how do I get my money back?", "complaint"),
]

right = 0
total = 0
for text, expected in cases:
    for _ in range(3):
        got = analyze_message(text, [])["intent"]
        total += 1
        if got == expected:
            right += 1
        else:
            print("WRONG:", got, "|", text)

print(f"{right}/{total} correct")