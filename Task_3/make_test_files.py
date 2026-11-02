from pathlib import Path

kb = Path("Data/kb")
inc = Path("Data/incoming")
inc.mkdir(parents=True, exist_ok=True)

(inc / "refund_policy_v2.txt").write_text((kb / "refund_policy_v2.txt").read_text(encoding="utf-8"), encoding="utf-8")
text = (kb / "shipping_faq.txt").read_text(encoding="utf-8").replace("499", "599")
(inc / "shipping_faq.txt").write_text(text, encoding="utf-8")
print("test files ready:", sorted(p.name for p in inc.glob("*.txt")))