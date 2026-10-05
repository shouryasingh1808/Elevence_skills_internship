"""Task 2 masking: hides emails, phone numbers and card numbers."""

import re
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")  # format to read email
CARD = re.compile(r"\b\d(?:[ -]?\d){12,18}\b") # format to read Card 
PHONE = re.compile(r"(?<!\d)(?:\+?91[ -]?)?[6-9]\d{9}(?!\d)")# format to read phone number

def _mask_email(match):
    name, domain = match.group(0).split("@" , 1)
    return name[0] + "******@" + domain

def _mask_card(match):
    digits = re.sub(r"\D" , "" , match.group(0))
    return "**** **** **** " + digits[-4:]

def _mask_phone(match):
    digits = re.sub(r"\D" , "" , match.group(0))[-10:]
    return digits[:2] + "******" + digits[-2:]

def mask_text(text):
    text = EMAIL.sub(_mask_email , text)
    text = CARD.sub(_mask_card,  text)
    text = PHONE.sub(_mask_phone , text)
    return text
