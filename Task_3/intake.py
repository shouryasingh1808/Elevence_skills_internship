"""Task 3 intake: scans the incoming folder, checks each file and quarantines bad ones."""

import Task_3.scanner as scanner
from Task_3.quarantine import quarantine_file
from Task_3.validator import validate_document
from pathlib import Path


def triage_incoming():
    accepted = []
    skipped = []
    quarantined = []

    for item in scanner.scan_incoming():
        if item["status"] in ("unchanged" , "duplicate"):
            skipped.append(item) 
            continue
        path = Path(scanner.INCOMING) / item["file"]
        problems = validate_document(path)
        if problems:
            quarantine_file(path, problems)
            quarantined.append({**item, "problems": problems})
            continue
        accepted.append(item)
    return {"accepted": accepted, "skipped": skipped, "quarantined": quarantined}