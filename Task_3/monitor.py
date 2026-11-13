"""Task 3 monitor: records latency, failures, confidence and escalations, and raises alerts."""

import json
import math
from collections import Counter

from Task_1 import config as clock
from Task_3 import config


def record(kind, **data):
    entry = {"time": clock.get_now().isoformat(), "kind": kind, **data}
    try:
        config.METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(config.METRICS_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def record_message(result, latency_ms):
    analysis = result["analysis"]
    kb = result.get("kb")
    rec = result.get("record")
    failed = bool(analysis.get("analyzer_failed")) or (kb is not None and kb["status"] in ("error", "rejected"))
    record("message", latency_ms=round(latency_ms), failed=failed,
           sentiment_confidence=analysis["sentiment_confidence"],
           escalated=rec is not None,
           conditions=rec["conditions"] if rec else [])


def load_records():
    if not config.METRICS_FILE.exists():
        return []
    lines = config.METRICS_FILE.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def summary(records=None):
    records = records if records is not None else load_records()
    messages = [r for r in records if r["kind"] == "message"]
    n = len(messages)
    latencies = sorted(r["latency_ms"] for r in messages)
    confidences = [r["sentiment_confidence"] for r in messages if not r["failed"]]
    escalations = [r for r in records if r["kind"] == "escalation" or (r["kind"] == "message" and r["escalated"])]
    failed_updates = [r for r in records if r["kind"] == "update" and not r["ok"]]

    failed_messages = sum(1 for r in messages if r["failed"])
    failure_rate = failed_messages / n if n else 0.0
    p95 = latencies[max(0, math.ceil(0.95 * n) - 1)] if n else 0
    avg_confidence = sum(confidences) / len(confidences) if confidences else None

    alerts = []
    if p95 > config.LATENCY_ALERT_MS:
        alerts.append(f"p95 latency {p95} ms is above {config.LATENCY_ALERT_MS} ms")
    if failure_rate > config.FAILURE_RATE_ALERT:
        alerts.append(f"failure rate {failure_rate:.2f} is above {config.FAILURE_RATE_ALERT}")
    if avg_confidence is not None and avg_confidence < config.LOW_CONFIDENCE_LEVEL:
        alerts.append(f"average confidence {avg_confidence:.2f} is below {config.LOW_CONFIDENCE_LEVEL}")
    for r in failed_updates:
        alerts.append(f"failed update: {r['detail']}")

    return {
        "messages": n,
        "avg_latency_ms": round(sum(latencies) / n) if n else 0,
        "p95_latency_ms": p95,
        "failed_messages": failed_messages,
        "failure_rate": round(failure_rate, 2),
        "avg_confidence": round(avg_confidence, 2) if avg_confidence is not None else None,
        "low_confidence": sum(1 for c in confidences if c < config.LOW_CONFIDENCE_LEVEL),
        "escalations": len(escalations),
        "by_condition": dict(Counter(c for r in escalations for c in r["conditions"])),
        "failed_updates": len(failed_updates),
        "alerts": alerts,
    }