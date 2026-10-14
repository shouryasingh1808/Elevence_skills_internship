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

def check_message(expect , results):
    problems = []
    statuses = [r["status"] for r in results]
    created = [r["ticket"] for r in results if r["status"] == "created"]    
    if "statuses" in expect and statuses != expect["statuses"]:
        problems.append(f"statuses: expected = {expect['statuses']} , got = {statuses}")

    if "queues" in expect:
        got = [t.queue for t in created]
        if got != expect["queues"]:
            problems.append(f"queues: expected = {expect['queues']} , got = {got}")
    if "queues_in" in expect:
        got = [t.queue for t in created]
        if not got or any(q not in expect["queues_in"] for q in got):
            problems.append(f"queues: expected each in {expect['queues_in']}, got {got}")
    if "assigned" in expect:
        got = [t.assigned_to for t in created]
        if got != expect["assigned"]:
            problems.append(f"assigned: expected {expect['assigned']}, got {got}")
    if "same_group" in expect:
        groups = {t.group_id for t in created}
        if expect["same_group"] and (len(created) < 2 or len(groups) != 1 or None in groups):
            problems.append(f"group: expected one shared group, got {groups}")
        if not expect["same_group"] and groups != {None}:
            problems.append(f"group: expected no group, got {groups}")
    if "duplicate_of" in expect:
        got = [r.get("duplicate_of") for r in results if r["status"] == "duplicate" ]
        if got != [expect["duplicate_of"]]:
            problems.append(f"duplicate_of: expected {expect['duplicate_of']}, got {got}")

    return problems
