from datetime import datetime
from Task_1 import config as clock
from Task_2.handoff import build_handoff
from Task_2.tickets import create_ticket
from Task_2.sla import get_due_time

tz = clock.TIMEZONE

def at(day , hour , minute = 0):
    return datetime(2026,10,day , hour, minute, tzinfo=tz)

clock.set_time(at(6,9))

history = [
    {"role" : "customer" , "content" : "My order ORD-4521 has not been arrived yet.. Its been 6 days and my gmail id is shourya@gmail.com and my phone number is 7447495838"},
    {"role" : "bot" , "content": "Sorry about that, We are checking!"},
    {"role": "customer" , "content":"I have been charged twice in same order..My card number is 4111 1111 1111 1111 .. Please check and refund my amount as soon as possible.!"}

]   