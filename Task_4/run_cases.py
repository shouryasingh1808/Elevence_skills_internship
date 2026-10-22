"""Task 4 run_cases: runs the knowledge assistant test cases and shows PASS/FAIL"""

import json 
from datetime import datetime
from pathlib import Path
from Task_1 import config as clock
from Task_4.assistant import answer_question
CASES_FILE = Path(__file__).resolve().parent.parent / "Data" / "task4_test_cases.json"
DEFAULT_TODAY = "2026-10-22"