import json
from types import SimpleNamespace

import Task_1.analyzer as a

captured = {}


class FakeCompletions:
    def create(self, **kw):
        captured["messages"] = kw["messages"]
        content = json.dumps({"sentiment": "neutral", "sentiment_confidence": 0.9, "language": "English",
                              "intent": "question", "is_complaint": False, "risk_type": "none",
                              "risk_confidence": 0.9, "reason": "test"})
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=content))])


a.client = SimpleNamespace(chat=SimpleNamespace(completions=FakeCompletions()))
history = [{"role": "customer", "content": f"message {i}"} for i in range(1, 21)]
a.analyze_message("latest question", history)
prompt = captured["messages"][1]["content"]
print(prompt.count("customer: message"), "history messages sent")
print("message 9 included:", "message 9" in prompt, "| message 8 included:", "message 8" in prompt)