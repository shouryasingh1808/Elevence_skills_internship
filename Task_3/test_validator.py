import shutil
from pathlib import Path

from Task_3.validator import validate_document

folder = Path("Data/test_validation")
folder.mkdir(parents=True, exist_ok=True)

GOOD = """---
doc_id: sample
title: Sample
version: 1
product: all
region: global
access: public
effective: 2026-01-01
expires: none
---
This is a sample document.
"""

(folder / "good.txt").write_text(GOOD, encoding="utf-8")
(folder / "missing_fields.txt").write_text("---\ndoc_id: x\ntitle: T\n---\nSome text", encoding="utf-8")
(folder / "empty_value.txt").write_text(GOOD.replace("access: public", "access:"), encoding="utf-8")
(folder / "no_header.txt").write_text("Just some text without a header.", encoding="utf-8")
(folder / "one_line.txt").write_text("---\ndoc_id: x\nSome text", encoding="utf-8")
(folder / "binary.txt").write_bytes(b"\xff\xfe\x00\xfa\xfb")
(folder / "bad_version.txt").write_text(GOOD.replace("version: 1", "version: one"), encoding="utf-8")
(folder / "bad_date.txt").write_text(GOOD.replace("effective: 2026-01-01", "effective: 2026-13-45"), encoding="utf-8")
(folder / "expires_early.txt").write_text(GOOD.replace("expires: none", "expires: 2025-12-31"), encoding="utf-8")
(folder / "bad_access.txt").write_text(GOOD.replace("access: public", "access: agnet"), encoding="utf-8")
(folder / "capital_access.txt").write_text(GOOD.replace("access: public", "access: Public"), encoding="utf-8")
(folder / "empty_body.txt").write_text(GOOD.replace("This is a sample document.", ""), encoding="utf-8")

for path in sorted(folder.glob("*.txt")):
    print(path.name, "->", validate_document(path))

shutil.rmtree(folder)