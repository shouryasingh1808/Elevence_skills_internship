import uuid
from datetime import datetime

import streamlit as st

from Task_1 import config as clock
from chatbot.engine import handle_message, run_timeouts
from Task_2.tickets import tickets
from Task_4.config import ACCESS_LEVELS  
from Task_4.filters import valid_on , allowed_by_access
from Task_4.loader import load_documents  

st.title("CUSTOMER SUPPORT CHATBOT 🤖")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.chat = []
    st.session_state.last = None

with st.sidebar:
    st.header("Demo controls")  
    user_level = st.selectbox("User level", list(ACCESS_LEVELS), index=1)  
    region = st.selectbox("Region", ["(not set)", "india", "usa"])  

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

region_value = None if region == "(not set)" else region  

message = st.text_input("Customer message: ")
btn = st.button("Send")

if btn and message:
    try:
        with st.spinner("Thinking..."):
            result = handle_message(
                st.session_state.session_id, message,
                user_level=user_level, region=region_value,
            )  
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
        kb = last["kb"]  
        st.write(f"Mood: {a['sentiment']} ({a['sentiment_confidence']})")
        st.write(f"Language: {a['language']}")
        st.write(f"Risk: {a['risk_type']} ({a['risk_confidence']})")
        st.write(f"Queue: {last['route']['queue']}")
        st.write("Answered by: " + (f"Knowledge base ({kb['status']})" if kb is not None else "Support rules (Task 1)"))  
        if kb is not None and kb.get("problems"):  
            st.write("Rejected because: " + ", ".join(kb["problems"]))  
        if last["triggers"]:
            st.write("Escalation: " + ", ".join(t["condition"] for t in last["triggers"]))

st.header("All tickets")
for tk in tickets.values():
    st.write(f"{tk.ticket_id} | {tk.priority} | {tk.category} | {tk.status} | {tk.assigned_to or tk.queue}")

with st.expander("Knowledge base (demo view)"):
    today = clock.get_now().date()
    for d in load_documents():
        if not allowed_by_access(d, user_level):
            continue
        ok = "valid" if valid_on(d, today) else "not valid"
        st.write(f"{d['file']} | v{d['version']} | {d['access']} | {d['region']} | {d['product']} | {ok} today")