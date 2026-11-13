from datetime import datetime
from pathlib import Path

from Task_1 import config as clock
from Task_3 import config, monitor

config.METRICS_FILE = Path("Data/test_metrics.jsonl")
if config.METRICS_FILE.exists():
    config.METRICS_FILE.unlink()
clock.set_time(datetime(2026, 10, 7, 11, 0, tzinfo=clock.TIMEZONE))


def fake(conf, failed=False, record=None, kb=None):
    return {"analysis": {"sentiment_confidence": conf, "analyzer_failed": failed}, "kb": kb, "record": record}


monitor.record_message(fake(0.9), 1200)
monitor.record_message(fake(0.8), 1500)
monitor.record_message(fake(0.4), 2000)
monitor.record_message(fake(0.0, failed=True), 9000)
monitor.record_message(fake(0.95, record={"conditions": ["repeated_negative"]}), 1800)
monitor.record_message(fake(0.9, kb={"status": "answered"}), 1000)
monitor.record("escalation", conditions=["unresolved_negative_timeout"])
monitor.record("update", ok=False, detail="candidate rejected by quality gate")

for key, value in monitor.summary().items():
    print(key, "->", value)

clock.clear_time()
config.METRICS_FILE.unlink()