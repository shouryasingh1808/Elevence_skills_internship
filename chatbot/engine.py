from Task_1.pipeline import handle_message , get_state
from Task_2.pipeline import process_conversation

def handel_message(session_id, message):
    result = handle_message(session_id , message)
    state = get_state(session_id)
    
