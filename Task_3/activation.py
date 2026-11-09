"""Task 3 activation: puts an approved version live, only inside the maintenance window."""

from Task_1 import config as clock
from Task_3.config import ACTIVE_KB, MAINTENANCE_END, MAINTENANCE_START
from Task_3.scanner import file_hash, load_manifest, save_manifest
from Task_3.versions import restore_version


def in_maintenance_window(now=None):
    now = (now or clock.get_now()).astimezone(clock.TIMEZONE)
    t = now.time()
    if MAINTENANCE_START <= MAINTENANCE_END:
        return MAINTENANCE_START <= t < MAINTENANCE_END
    return t >= MAINTENANCE_START or t < MAINTENANCE_END


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
    manifest["files"] = {p.name: file_hash(p) for p in sorted(ACTIVE_KB.glob("*.txt"))}
    save_manifest(manifest)
    return {"activated": True, "version": number, "previous": previous}