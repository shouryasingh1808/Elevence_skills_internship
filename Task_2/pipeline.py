from Task_2.extractor import extract_ticket_info , find_missing , question_for

from Task_2.tickets import create_ticket
from Task_2.priority import calculate_priority
from Task_2.duplicates import link_ticket , classify_issue
from Task_2.sla import get_due_time
from Task_2.routing import assign_ticket
from Task_2.handoff import build_handoff

def process_conversation(history , session_id):
    