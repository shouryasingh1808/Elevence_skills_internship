"""Task 3 pipeline: one run of the knowledge base update, from incoming files to a live version."""

from pathlib import Path

import Task_3.scanner as scanner
from Task_3 import monitor
from Task_3.access import check_access
from Task_3.activation import activate_version, rollback, run_health_check
from Task_3.config import MIN_BASELINE_ACCURACY, ensure_folders
from Task_3.health import health_check
from Task_3.intake import triage_incoming
from Task_3.quality import quality_gate
from Task_3.quarantine import quarantine_file
from Task_3.versions import build_candidate


def finish(state, success, **extra):
    ok = success and state != "rejected"
    monitor.record("update", ok=ok, detail=f"{state}: {extra.get('error') or extra.get('reasons') or ''}")
    return {"state": state, "success": success, **extra}


def clear_incoming(names):
    for name in names:
        path = Path(scanner.INCOMING) / name
        if path.exists():
            path.unlink()


def run_update(user="scheduler", level="admin"):
    access = check_access(user, level, "run_update")
    if not access["allowed"]:
        return finish("denied", False, error=access["reason"])

    ensure_folders()
    manifest = scanner.load_manifest()
    pending = manifest.get("pending")

    if pending is None:
        triage = triage_incoming()
        clear_incoming([i["file"] for i in triage["skipped"]])
        accepted = [i["file"] for i in triage["accepted"]]
        quarantined = [i["file"] for i in triage["quarantined"]]
        if not accepted:
            return finish("nothing_to_update", True, quarantined=quarantined)

        manifest = scanner.load_manifest()
        number, folder = build_candidate(manifest["active_version"], accepted)
        gate = quality_gate(folder)
        if gate["baseline"]["accuracy"] < MIN_BASELINE_ACCURACY:
            return finish("failed", False, error="baseline check failed, the service may be down")
        if not gate["approved"]:
            for name in accepted:
                quarantine_file(Path(scanner.INCOMING) / name, gate["reasons"])
            return finish("rejected", True, reasons=gate["reasons"], quarantined=quarantined + accepted)

        manifest["pending"] = {"version": number, "files": accepted}
        scanner.save_manifest(manifest)
        pending = manifest["pending"]

    activation = activate_version(pending["version"])
    if not activation["activated"]:
        return finish("waiting_for_window", True, reason=activation["reason"], version=pending["version"])

    manifest = scanner.load_manifest()
    manifest.pop("pending", None)
    scanner.save_manifest(manifest)

    health = run_health_check(health_check)
    if health["state"] == "rolled_back":
        return finish("rolled_back", False, error=health["reason"])

    clear_incoming(pending["files"])
    return finish("activated", True, version=pending["version"], files=pending["files"])


def manual_rollback(user, level):
    access = check_access(user, level, "rollback")
    if not access["allowed"]:
        return {"rolled_back": False, "reason": access["reason"]}
    return rollback(f"manual rollback by {user}")