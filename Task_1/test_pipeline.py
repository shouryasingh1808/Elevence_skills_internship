from datetime import datetime  , timedelta
from Task_1 import config
from Task_1.pipeline import handle_message

t0 = datetime(2026 , 10 , 6 , 11 , 0 , tzinfo=config.TIMEZONE)  # Tue 11 am

conversation = [
    (0 , "Its been 3 days and i didnt recieve my order"),
    (5 , "Koi reply nahi mila, bahut bura service hai"),
    (10 , "What a wonderfull service , I am still waiting"),
    (12 , "Ab bhi koi jawab nahi, bahut gussa aa raha hai"),
]

for minutes , text in conversation:
    config.set_time(t0 + timedelta(minutes=minutes))
    result = handle_message("demo-1" , text)
    print(f"[+{minutes} min] {text}")
    print("  sentiment:", result["analysis"]["sentiment"])
    print("  triggers :", [t["condition"] for t in result["triggers"]])
    print("  queue    :", result["route"]["queue"])
    print("  record   :", "saved" if result["record"] else "-")
    print("  reply    :", result["reply"], "\n")

config.clear_time()