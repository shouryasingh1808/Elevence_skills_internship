"""Task 6 entities: finds order IDs, product codes and numbers that must survive a translation."""

import re

from Task_4.answer import numbers_in

CODE = re.compile(r"\b[A-Z]{1,5}-?\d{2,}\b")
MARKER = re.compile(r"\[\d+\]")
FILE = re.compile(r"\b[\w-]+\.txt\b")


def find_entities(text):
    return {
        "codes": set(CODE.findall(text)),
        "numbers": numbers_in(text),
        "markers": set(MARKER.findall(text)),
        "files": set(FILE.findall(text)),
    }


def check_preserved(original, translated, names=()):
    before = find_entities(original)
    after = find_entities(translated)
    problems = []
    for key in ("codes", "numbers", "markers", "files"):
        for item in sorted(before[key] - after[key]):
            problems.append(f"{key[:-1]} '{item}' was lost or changed")
    for name in names:
        pattern = rf"\b{re.escape(name)}\b"
        if re.search(pattern, original) and not re.search(pattern, translated):
            problems.append(f"name '{name}' was lost or changed")
    return problems