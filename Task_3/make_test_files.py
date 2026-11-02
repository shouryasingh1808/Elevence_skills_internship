from pathlib import Path

kb = Path("Data/kb")
inc = Path("Data/incoming")
inc.mkdir(parents=True, exist_ok=True)

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


def read_kb(name):
    return (kb / name).read_text(encoding="utf-8")


def write(name, text):
    (inc / name).write_text(text, encoding="utf-8")


write("refund_policy_v2.txt", read_kb("refund_policy_v2.txt"))                  # unchanged
write("shipping_faq.txt", read_kb("shipping_faq.txt").replace("499", "599"))    # modified
write("laptop_guide_copy.txt", read_kb("laptop_troubleshooting.txt"))           # duplicate of a KB file
write("return_shipping.txt", NEW_DOC)                                           # new
write("return_shipping_copy.txt", NEW_DOC)                                      # duplicate of a new file
print("test files ready:", sorted(p.name for p in inc.glob("*.txt")))