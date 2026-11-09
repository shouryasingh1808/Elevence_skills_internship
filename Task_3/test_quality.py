import shutil
from pathlib import Path

from Task_3.quality import evaluate, quality_gate

root = Path("Data/test_quality")
shutil.rmtree(root, ignore_errors=True)
good = root / "good"
bad = root / "bad"
shutil.copytree("Data/kb", good)
shutil.copytree("Data/kb", bad)

path = bad / "refund_policy_v2.txt"
path.write_text(path.read_text(encoding="utf-8").replace("10 days", "30 days"), encoding="utf-8")

base = evaluate("Data/kb")
print("baseline:", round(base["accuracy"], 2), round(base["grounding"], 2), [f["question"] for f in base["failures"]])

for name, folder in [("good", good), ("bad", bad)]:
    r = quality_gate(folder, baseline=base)
    print(name, "->", "APPROVED" if r["approved"] else "REJECTED", r["reasons"])

shutil.rmtree(root)