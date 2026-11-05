"""Task 3 security: finds prompt injection in documents and masks sensitive data."""

import re

INJECTION_PATTERNS = [
    r"ignore (all |any |the )?(previous|prior|above|earlier) (instructions|rules|messages)",
    r"disregard (all |any |the )?(previous|prior|above|earlier)",
    r"do not follow (the |any )?(previous|prior|above|earlier|these)",
    r"(tell|say to|inform) (every|all|each) customers?",
    r"you are now (a|an|the) ",
    r"(reveal|show|print) (your|the) (system )?(prompt|instructions)",
    r"pretend (to be|you are)",
]

def find_injection(text):
    normalized = " ".join(text.lower().split())
    return [p for p in INJECTION_PATTERNS if re.search(p, normalized)]