"""Task 3 activation: puts an approved version live (inside the maintenance window) and rolls back if it is unhealthy."""

from datetime import datetime

from Task_1 import config as clock
from Task_3.config import ACTIVE_KB, HEALTH_WINDOW_MINUTES, MAINTENANCE_END, MAINTENANCE_START
from Task_3.scanner import file_hash, load_manifest, save_manifest
from Task_3.versions import restore_version


def in_maintenance_window(now=None):
    now = (now or clock.get_now()).astimezone(clock.TIMEZONE)
    t = now.time()
    if MAINTENANCE_START <= MAINTENANCE_END:
        return MAINTENANCE_START <= t < MAINTENANCE_END
    return t >= MAINTENANCE_START or t < MAINTENANCE_END


def current_hashes():
    return {p.name: file_hash(p) for p in sorted(ACTIVE_KB.glob("*.txt"))}


def activate_version(number):
    if not in_maintenance_window():
        window = f"{MAINTENANCE_START:%H:%M}-{MAINTENANCE_END:%H:%M}"
        return {"activated": False, "waiting": True, "reason": f"outside maintenance window ({window})"}

    manifest = load_manifest()
    previous = manifest["active_version"]
    restore_version(number)

    manifest["previous_version"] = previous
    manifest["active_version"] = number
    manifest["activated_at"] = clock.get_now().isoformat()
    manifest["health"] = "pending"
    manifest["health_passes"] = 0
    manifest["files"] = current_hashes()
    save_manifest(manifest)
    return {"activated": True, "version": number, "previous": previous}


def rollback(reason):
    manifest = load_manifest()
    previous = manifest.get("previous_version")
    if previous is None:
        return {"rolled_back": False, "reason": "no previous version to go back to"}

    restore_version(previous)
    manifest["rolled_back_from"] = manifest["active_version"]
    manifest["active_version"] = previous
    manifest["previous_version"] = None
    manifest["health"] = "rolled_back"
    manifest["rollback_reason"] = reason
    manifest["files"] = current_hashes()
    save_manifest(manifest)
    return {"rolled_back": True, "version": previous, "reason": reason}


def run_health_check(check):
    manifest = load_manifest()
    if manifest.get("health") != "pending":
        return {"state": manifest.get("health", "none")}

    activated = datetime.fromisoformat(manifest["activated_at"])
    minutes = (clock.get_now() - activated).total_seconds() / 60
    if minutes > HEALTH_WINDOW_MINUTES:
        manifest["health"] = "healthy" if manifest.get("health_passes", 0) > 0 else "unverified"
        save_manifest(manifest)
        return {"state": manifest["health"]}

    try:
        result = check()
    except Exception as e:
        result = {"healthy": False, "failures": [f"health check crashed: {e}"]}

    if not result["healthy"]:
        outcome = rollback(f"health check failed {minutes:.0f} minute(s) after activation: {result['failures']}")
        return {"state": "rolled_back", **outcome}

    manifest["health_passes"] = manifest.get("health_passes", 0) + 1
    save_manifest(manifest)
    return {"state": "ok", "passes": manifest["health_passes"]}