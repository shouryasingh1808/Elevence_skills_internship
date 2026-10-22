"""Task 4 query: reads the date and the product from a customer question."""

import re
from datetime import date

MONTHS = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
          "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}

def make_date(year , month , day):
    try:
        return date(int(year), int(month), int(day))
    except ValueError:
        return None

def extract_date(question):
    iso = re.search(r"(\d{4})-(\d{2})-(\d{2})", question)
    if iso:
        return make_date(*iso.groups())

    for m in re.finditer(r"(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+),?\s+(\d{4})", question):
        month = MONTHS.get(m.group(2)[:3].lower())
        if month:
            return make_date(m.group(3), month, m.group(1))

    for m in re.finditer(r"([A-Za-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})", question):
        month = MONTHS.get(m.group(1)[:3].lower())
        if month:
            return make_date(m.group(3), month, m.group(2))

    return None

def extract_product(question, docs):
    products = {d["product"].lower() for d in docs} - {"all"}
    found = [p for p in sorted(products) if re.search(rf"\b{re.escape(p)}s?\b", question.lower())]
    return found[0] if len(found) == 1 else None