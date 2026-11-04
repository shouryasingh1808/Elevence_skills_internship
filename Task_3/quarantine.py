"""Task 3 quarantine: keeps invalid documents away from the knowledge base."""

import json
import shutil
from pathlib import Path

from Task_1 import config as clock
from Task_3.config import QUARANTINE

def unique_path(folder , name):
    target = folder / name
    number = 2
    while target.exists():
        target = folder / f"{Path(name).stem}_{number}{Path(name).suffix}"
        number += 1
    return target

def quarantine_file(path , problems):
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    target = unique_path(QUARANTINE, Path(path).name)
    shutil.move(str(path), str(target))
    reason = {"file" : target.name , "problems" : problems , "time" : clock.get_now().isoformat()}
    (QUARANTINE / (target.name + ".reason.json")).write_text(json.dumps(reason, indent=2) , encoding="utf-8")
    return target

