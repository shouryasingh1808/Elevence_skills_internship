"""Task 3 access control: only allowed roles may run or change the update pipeline."""
import json
from Task_1 import config as clock
from Task_3 import config
from Task_4.config import ACCESS_LEVELS

def log_audit(user , level , action ,  allowed , reason):
    config.AUDIT_FILE.parent.mkdir(parents=True , exist_ok=True)
    entry = {"time": clock.get_now().isoformat(), "user": user, "level": level,
             "action": action, "allowed": allowed, "reason": reason}
    with open(config.AUDIT_FILE , "a" , encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

def check_access(user , level , action):
    needed = config.ACTION_LEVELS.get(action)
    if needed is None:
        allowed , reason = False , f"unknown action '{action}'"
    elif level not in ACCESS_LEVELS:
        allowed , reason  = False, f"unknown role '{level}'"
    elif ACCESS_LEVELS[level] >= ACCESS_LEVELS[needed]:
        allowed, reason = True, "allowed"
    else:
        allowed , reason = False , f"'{action}' needs the {needed} role, got {level}"
    log_audit(user , level , action , allowed , reason)
    return {"allowed" : allowed , "reason" : reason}
