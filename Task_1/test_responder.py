from datetime import datetime
from Task_1 import config
from Task_1.responder import generate_reply

config.set_time(datetime(2026, 10, 6,11,0,tzinfo=config.TIMEZONE)) #Tuesday 11 AM

route = {"queue": "agent_queue" , "scheduled_for" : None , "urgent" : False}

cases = [
    ("English", "My order has not arrived for 5 days and I want a refund now!"),
    ("Hinglish", "Mera order 5 din se nahi aaya aur mujhe refund chahiye abhi!"),
]

for language, message in cases:
    for sentiment in ["neutral" , "frustrated" , "sarcastic" , "urgent"]:
        analysis = {"sentiment" : sentiment, "language": language}
        print(f"---{sentiment}---")
        print(generate_reply(message, [] , analysis , route) , "\n")

config.clear_time()
