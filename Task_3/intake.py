"""Task 3 intake: scans the incoming folder, checks each file and quarantines bad ones."""

from Task_3.scanner import scan_incoming

def triage_incoming():
    accepted = []
    skipped = []
    quarantined = []

    for item in scan_incoming():
        if item["status"] in ("unchanged" , "duplicate"):
            skipped.append(item) 
            continue
        accepted.append(item)  # temporary: validation comes in the next step
    return {"accepted": accepted, "skipped": skipped, "quarantined": quarantined}