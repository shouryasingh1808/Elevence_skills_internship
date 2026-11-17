import uuid
from datetime import datetime

import streamlit as st

from Task_1 import config as clock
from chatbot.engine import handle_message, run_timeouts
from Task_2.tickets import tickets
from Task_4.config import ACCESS_LEVELS  
from Task_4.filters import valid_on , allowed_by_access
from Task_4.loader import load_documents  

from Task_3 import config as t3
from Task_3 import monitor
from Task_3.activation import run_health_check
from Task_3.health import health_check
from Task_3.pipeline import manual_rollback, run_update
from Task_3.scanner import load_manifest
from Task_3.scheduler import tick

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

st.header("Knowledge base admin (Task 3)")
with st.expander("Update pipeline"):
    st.write(f"Acting as role: **{user_level}** (change it in the sidebar)")

    uploaded = st.file_uploader("Add a document to the incoming folder", type=["txt"])
    if uploaded is not None and st.button("Save to incoming"):
        t3.INCOMING.mkdir(parents=True, exist_ok=True)
        (t3.INCOMING / uploaded.name).write_bytes(uploaded.getvalue())
        st.success(f"Saved {uploaded.name} to incoming")

    c1, c2, c3, c4 = st.columns(4)
    if c1.button("Run update"):
        with st.spinner("Running update (about 1-2 minutes)..."):
            st.session_state.admin_result = run_update("demo_user", user_level)
    if c2.button("Scheduler tick"):
        with st.spinner("Running scheduler tick..."):
            st.session_state.admin_result = tick(lambda: run_update("scheduler", "admin"))
    if c3.button("Health check"):
        with st.spinner("Checking..."):
            st.session_state.admin_result = run_health_check(health_check)
    if c4.button("Roll back"):
        st.session_state.admin_result = manual_rollback("demo_user", user_level)

    if st.session_state.get("admin_result"):
        st.write("Result:")
        st.json(st.session_state.admin_result)

    manifest = load_manifest()
    st.write(f"Active version: {manifest['active_version']} | previous: {manifest.get('previous_version')} | "
             f"pending: {manifest.get('pending')} | health: {manifest.get('health', '-')}")
    st.write("Schedule:", manifest.get("schedule", "not started"))
    st.write("Incoming:", sorted(p.name for p in t3.INCOMING.glob("*.txt")) if t3.INCOMING.exists() else [])
    st.write("Quarantine:", sorted(p.name for p in t3.QUARANTINE.glob("*.txt")) if t3.QUARANTINE.exists() else [])

    st.write("Monitoring:")
    st.json(monitor.summary())

    if t3.AUDIT_FILE.exists():
        st.write("Last audit entries:")
        for line in t3.AUDIT_FILE.read_text(encoding="utf-8").splitlines()[-5:]:
            st.code(line)