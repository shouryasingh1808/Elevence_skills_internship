import shutil
from pathlib import Path

import Task_3.intake as intake
import Task_3.quarantine as quarantine
import Task_3.scanner as scanner

root = Path("Data/test_intake")
incoming = root / "incoming"
incoming.mkdir(parents=True, exist_ok=True)

# Test ke liye saare raste temp folder pe
scanner.INCOMING = incoming
scanner.MANIFEST_FILE = root / "manifest.json"
quarantine.QUARANTINE = root / "quarantine"

kb = Path("Data/kb")

NEW_DOC = """---
doc_id: return_shipping
title: Return Shipping
version: 1
product: all
region: global
access: public
effective: 2026-01-01
expires: none
---
Return shipping is free for damaged items. For other returns the customer pays a shipping cost of Rs 99.
"""


def write(name, text):
    (incoming / name).write_text(text, encoding="utf-8")


def read_kb(name):
    return (kb / name).read_text(encoding="utf-8")


write("refund_policy_v2.txt", read_kb("refund_policy_v2.txt"))                 # unchanged
write("shipping_faq.txt", read_kb("shipping_faq.txt").replace("499", "599"))   # modified, valid
write("laptop_guide_copy.txt", read_kb("laptop_troubleshooting.txt"))          # duplicate
write("return_shipping.txt", NEW_DOC)                                          # new, valid
write("broken_policy.txt", "This file has no header at all.")                  # new, invalid
write("bad_access.txt", NEW_DOC.replace("return_shipping", "extra").replace("access: public", "access: agnet"))  # new, invalid

result = intake.triage_incoming()
for key in ("accepted", "skipped", "quarantined"):
    print(key, "->", [(i["file"], i["status"]) for i in result[key]])
    
print("problems ->", [(i["file"], i["problems"]) for i in result["quarantined"]])
print("incoming now:", sorted(p.name for p in incoming.glob("*.txt")))
print("quarantine:", sorted(p.name for p in quarantine.QUARANTINE.iterdir()))

shutil.rmtree(root)