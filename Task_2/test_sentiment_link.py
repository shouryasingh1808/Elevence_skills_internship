from Task_2.pipeline import process_conversation

for mood, order in [("neutral", "ORD-9001"), ("frustrated", "ORD-9002")]:
    history = [{"role": "customer", "content": f"My order {order} arrived damaged. My email is a@b.com."}]
    results = process_conversation(history, "x", mood)
    t = results[0]["ticket"]
    print(mood, "->", t.sentiment, t.priority_score, t.priority)