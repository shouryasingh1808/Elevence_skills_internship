"""Task 3 validator: checks a document before it may enter the knowledge base."""

from Task_4.loader import parse_header , split_document
from Task_4.config import ACCESS_LEVELS
from Task_3.security import find_injection
from datetime import date

REQUIRED_FIELDS = ["doc_id", "title", "version", "product", "region", "access", "effective", "expires"]

def parse_date(text):
    try:
        return date.fromisoformat(text)
    except ValueError:
        None

def validate_document(path):
    problems = []
    try:
        header , body = split_document(path)
    except UnicodeDecodeError:
        return ["File is not valid UTF-8 text"]
    except IndexError:
        return ["missing or broken header (needs --- lines)"]

    meta = parse_header(header)
    for field in REQUIRED_FIELDS:
        if not meta.get(field):
            problems.append(f"missing field: {field}")
    if problems:
        return problems

    if not meta["version"].isdigit() or int(meta["version"]) < 1:
        problems.append(f"version must be a whole number of 1 or more, got '{meta['version']}'")

    effective = parse_date(meta["effective"])
    if effective is None:
        problems.append(f"effective is not a valid date (YYYY-MM-DD): '{meta['effective']}'")

    if meta["expires"].lower() != "none":
        expires = parse_date(meta["expires"])
        if expires is None:
            problems.append(f"expires is not a valid date (YYYY-MM-DD): '{meta['expires']}'")
        elif effective is not None and expires < effective:
            problems.append("expires is before effective")

    if meta["access"] not in ACCESS_LEVELS:
        problems.append(f"access must be one of {', '.join(ACCESS_LEVELS)}, got '{meta['access']}'")

    if not body:
        problems.append("document type is empty")
    
    found = find_injection(meta["title"] + " " + body)
    if found :
        problems.append(f"possible prompt injection: {len(found)} suspicious phrase pattern(s) matched")

    return problems