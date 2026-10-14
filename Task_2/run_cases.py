"""Task 2 run_cases: To test the test_cases and show PASS/FAIL"""

import copy
import json
from datetime import datetime , timedelta
from pathlib import Path
from Task_1 import config as clock
from Task_2 import config
from Task_2.pipeline import process_conversation
from Task_2.sla import check_all_tickets
from Task_2.tickets import tickets

CASES_FILES = Path(__file__).resolve().parent.parent / "Data"/ "task2_test_cases.json"

DEFAULT_SLA = dict(config.SLA_HOURS)

DEFAULT_AGENTS = copy.deepcopy(config.AGENTS)

def reset(setup):
    tickets.clear()
    config.SLA_HOURS.clear()
    config.SLA_HOURS.update(DEFAULT_SLA)
    config.AGENTS[:] = copy.deepcopy(DEFAULT_AGENTS)
    config.SLA_HOURS.update(setup.get("sla_hours" , {}))
    for agent in config.AGENTS:
        if setup.get("all_unavailable") or agent["name"] in setup.get("unavailable" , []):
            agent["available"] = False
        if agent["name"] in setup.get("max_load" , {}):
            agent["max_load"] = setup["max_load"][agent["name"]]