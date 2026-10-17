import uuid
from datetime import datetime

import streamlit as st

from Task_1 import config as clock
from chatbot.engine import handle_message, run_timeouts
from Task_2.tickets import tickets

st.title("CUSTOMER SUPPORT CHATBOT 🤖")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.chat = []
    st.session_state.last = None

# Sidebar: demo ke liye fake time aur timeouts
with st.sidebar:
    use_fake = st.checkbox("Use fake time")
    if use_fake:
        day = st.date_input("Date", datetime(2026, 10, 6))
        hour = st.time_input("Time", datetime(2026, 10, 6, 11, 0).time())
        clock.set_time(datetime.combine(day, hour).replace(tzinfo=clock.TIMEZONE))
    else:
        clock.clear_time()
    st.write("Now:", clock.get_now().strftime("%a %d %b %Y, %I:%M %p"))

    if st.button("Run timeouts"):
        out = run_timeouts()
        st.write(f"Timeouts: {len(out['timeouts'])} | New tickets: {len(out['tickets'])}")
        for e in out["sla_events"]:
            st.write(f"{e['ticket']}: {e['event']}")

message = st.text_input("Customer message: ")
btn = st.button("Send")

if btn and message:
    try:
        with st.spinner("Thinking..."):
            result = handle_message(st.session_state.session_id, message)
        st.session_state.chat.append({"role": "Customer", "content": message})
        st.session_state.chat.append({"role": "Bot", "content": result["reply"]})
        st.session_state.last = result
    except Exception as e:
        st.error(f"Error: {e}")

st.header("Chat")
for m in st.session_state.chat:
    st.write(f"**{m['role']}:** {m['content']}")

last = st.session_state.last
if last:
    with st.expander("Details", expanded=True):
        a = last["analysis"]
        st.write(f"Mood: {a['sentiment']} ({a['sentiment_confidence']})")
        st.write(f"Language: {a['language']}")
        st.write(f"Risk: {a['risk_type']} ({a['risk_confidence']})")
        st.write(f"Queue: {last['route']['queue']}")
        if last["triggers"]:
            st.write("Escalation: " + ", ".join(t["condition"] for t in last["triggers"]))

st.header("All tickets")
for tk in tickets.values():
    st.write(f"{tk.ticket_id} | {tk.priority} | {tk.category} | {tk.status} | {tk.assigned_to or tk.queue}")