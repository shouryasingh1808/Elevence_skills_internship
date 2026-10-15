import uuid
from datetime import datetime

import streamlit as st

from Task_1 import config as clock
from Task_2 import config
from Task_2.pipeline import process_conversation
from Task_2.sla import check_all_tickets
from Task_2.tickets import tickets

st.title("SUPPORT TICKET SYSTEM 🎫")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.history = []
    st.session_state.results = []
    st.session_state.sla_events = []

# ---------- Sidebar: demo controls ----------
with st.sidebar:
    st.header("Demo controls")

    use_fake = st.checkbox("Use fake time")
    if use_fake:
        d = st.date_input("Date", datetime(2026, 10, 6))
        t = st.time_input("Time", datetime(2026, 10, 6, 9, 0).time())
        clock.set_time(datetime.combine(d, t).replace(tzinfo=clock.TIMEZONE))
    else:
        clock.clear_time()
    st.write("Now:", clock.get_now().strftime("%a %d %b %Y, %I:%M %p"))
    st.write("Business hours:", "Yes" if clock.is_business_hours() else "No")

    st.subheader("SLA hours")
    for p in ["P1", "P2", "P3", "P4"]:
        config.SLA_HOURS[p] = st.number_input(
            p, min_value=1, value=int(config.SLA_HOURS[p]), key="sla_" + p
        )

    st.subheader("Agents")
    names = [a["name"] for a in config.AGENTS]
    away = st.multiselect("Unavailable", names)
    for a in config.AGENTS:
        a["available"] = a["name"] not in away

    if st.button("Check SLA now"):
        st.session_state.sla_events = check_all_tickets()

    if st.button("Reset demo"):
        tickets.clear()
        for a in config.AGENTS:
            a["workload"] = 0
        st.session_state.history = []
        st.session_state.results = []
        st.session_state.sla_events = []

# ---------- Customer message ----------
with st.form("chat_form", clear_on_submit=True):
    message = st.text_area("Customer message")
    sent = st.form_submit_button("Send")

if sent and message:
    history = st.session_state.history
    history.append({"role": "customer", "content": message})
    with st.spinner("Creating ticket..."):
        results = process_conversation(history, st.session_state.session_id)
    st.session_state.results = results

    waiting = [r for r in results if r["status"] == "needs_info"]
    if waiting:
        history.append({"role": "bot", "content": waiting[0]["question"]})
    else:
        st.session_state.history = []

# ---------- Result ----------
if st.session_state.results:
    st.header("Result")
for r in st.session_state.results:
    if r["status"] == "created":
        tk = r["ticket"]
        place = tk.assigned_to or tk.queue
        st.success(f"{tk.ticket_id} created | {tk.priority} | {tk.category} | {place}")
        with st.expander("Handoff note"):
            st.text(r["handoff"])
    elif r["status"] == "duplicate":
        st.info(f"Duplicate of {r['duplicate_of']}, no new work needed")
    elif r["status"] == "needs_info":
        st.warning(r["question"])
    else:
        st.error(f"Extraction failed: {r.get('error')}")

for e in st.session_state.sla_events:
    st.warning(f"{e['ticket']}: {e['event']} | {e['detail']}")

# ---------- All tickets ----------
st.header("All tickets")
rows = []
for tk in tickets.values():
    rows.append({
        "ID": tk.ticket_id,
        "Category": tk.category,
        "Priority": tk.priority,
        "Status": tk.status,
        "Queue": tk.queue,
        "Agent": tk.assigned_to,
        "Due": tk.due_at.strftime("%a %d %b, %I:%M %p") if tk.due_at else "-",
        "Scheduled": tk.scheduled_for or "-",
        "SLA": tk.sla_status,
        "Group": tk.group_id,
        "Duplicate of": tk.duplicate_of,
    })
if rows:
    st.dataframe(rows)
else:
    st.write("No tickets yet.")