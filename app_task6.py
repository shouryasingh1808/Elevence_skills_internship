from datetime import datetime, timedelta

import streamlit as st

from Task_1 import config as clock
from Task_1 import pipeline as task1_pipeline
from Task_2.tickets import tickets
import Task_6.sessions as sessions
from Task_6.config import SESSION_IDLE_MINUTES, SESSION_RESTORE_HOURS, SUPPORTED_LANGUAGES
from Task_6.summary import summarize_session
from chatbot import engine

BASE = datetime(2026, 10, 6, 11, 0, tzinfo=clock.TIMEZONE)

SAMPLES = [
    "(type your own)",
    "What is the refund policy?",
    "¿Cuál es la política de reembolso?",
    "Combien de temps dure la garantie ?",
    "रिफंड पॉलिसी क्या है?",
    "Refund policy kya hai?",
    "Mera order ORD-4521 3 din se nahi aaya, bahut gussa aa raha hai",
    "My order ORD-4521 is late and what is your refund policy?",
    "How do I fix a fast draining battery?",
    "laptop",
    "wat is the refnd polcy",
    "ok",
    "Guten Tag, wo ist meine Bestellung?",
]

st.title("MULTILINGUAL SESSIONS 🌍")

if "offset" not in st.session_state:
    st.session_state.offset = 0
    st.session_state.chats = {}
    st.session_state.last = {}


def reset_demo():
    sessions.customers.clear()
    task1_pipeline.sessions.clear()
    engine.ticketed.clear()
    engine.pending_questions.clear()
    tickets.clear()
    st.session_state.offset = 0
    st.session_state.chats = {}
    st.session_state.last = {}


with st.sidebar:
    st.header("Demo controls")
    customer_id = st.text_input("Customer ID", "asha")

    c1, c2, c3 = st.columns(3)
    if c1.button("+10 min"):
        st.session_state.offset += 10
    if c2.button("+31 min"):
        st.session_state.offset += 31
    if c3.button("+25 hours"):
        st.session_state.offset += 25 * 60
    clock.set_time(BASE + timedelta(minutes=st.session_state.offset))
    st.write("Demo clock:", clock.get_now().strftime("%a %d %b, %I:%M %p"))

    if st.button("End idle sessions now"):
        ended = sessions.expire_idle_sessions(summarize_session)
        st.write("Ended:", ended if ended else "none")
    if st.button("Reset demo"):
        reset_demo()
        clock.set_time(BASE)
        st.write("Demo reset")

    st.write(f"Languages: {', '.join(SUPPORTED_LANGUAGES)}")
    st.write(f"Idle limit: {SESSION_IDLE_MINUTES} min | Restore window: {SESSION_RESTORE_HOURS} h")

sample = st.selectbox("Sample message", SAMPLES)
typed = st.text_input("Or type a message: ")
text = typed or (sample if sample != SAMPLES[0] else "")
btn = st.button("Send")

chat = st.session_state.chats.setdefault(customer_id, [])
if btn and text:
    try:
        with st.spinner("Thinking..."):
            result = engine.handle_message(customer_id, text)
        chat.append(("Customer", text))
        chat.append(("Bot", result["reply"]))
        st.session_state.last[customer_id] = result
    except Exception as e:
        st.error(f"Error: {e}")

st.header(f"Chat with {customer_id}")
for role, content in chat:
    st.write(f"**{role}:** {content}")

last = st.session_state.last.get(customer_id)
if last:
    with st.expander("Details", expanded=True):
        a = last["analysis"]
        session = last["session"]
        kb = last["kb"]
        st.write(f"Session: {session['session_id']} ({session['event']})")
        if session["event"] == "restored" and session["summary"]:
            st.write("Restored summary: " + session["summary"])
        st.write(f"Language: {a['language']} ({a['language_confidence']})")
        st.write(f"Intent: {a['intent']} ({a['intent_confidence']}) | has question: {a.get('has_question')}")
        st.write("Clarification asked: " + (last["clarification"] or "no"))
        st.write("Knowledge base: " + (f"{kb['status']} | {', '.join(kb['sources'])}" if kb else "not used"))
        st.write(f"Mood: {a['sentiment']} | Risk: {a['risk_type']}")

st.header("Sessions")
now = clock.get_now()
for cid, rec in sessions.customers.items():
    idle = sessions.idle_minutes(rec, now)
    st.write(f"{cid} | {rec['session_id']} | {rec['status']} | idle {idle:.0f} min")
if not sessions.customers:
    st.write("No sessions yet.")

st.header("Tickets")
for tk in tickets.values():
    st.write(f"{tk.ticket_id} | {tk.priority} | {tk.category} | {tk.status}")