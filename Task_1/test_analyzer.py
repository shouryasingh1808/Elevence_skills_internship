from Task_1.analyzer import analyze_message

history = [
    {"role" : "customer" , "content" : " I didnt get my order from 2 days ago. I want my money back"},
    {"role" : "agent" , "content" : "I am sorry to hear that. Can you please provide your order number so I can look into this for you?"},
]


tests = [
    "What a wonderful service! I am waiting for my order since 2 days and I am very happy about it.",
    "Payment has been 2 times from my account. Please check it!",
    "Someone logged into my account from another country.",
    "The problem hass ben solved. Thank you for your help.",
    "I will take legal action if this is not fixed today.",
]

for t in tests:
    print("MSG:", t)
    print(analyze_message(t, history), "\n")