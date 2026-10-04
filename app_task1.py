import uuid
from datetime import datetime

import streamlit as st

from Task_1 import config
from Task_1.pipeline import handle_message

st.title("CUSTOMER SERVICE CHATBOT 🤖")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.last = None

with st.form("chat_form", clear_on_submit=True):
    question = st.text_input("Question: ")
    sent = st.form_submit_button("Send")

if sent and question:
    with st.spinner("Just a sec.."):
        st.session_state.last = handle_message(st.session_state.session_id, question)

last = st.session_state.last
if last:
    st.header("Answer")
    st.write(last["reply"])

    with st.expander("Details"):
        a = last["analysis"]
        st.write(f"Sentiment: {a['sentiment']} ({a['sentiment_confidence']})")
        st.write(f"Language: {a['language']}")
        st.write(f"Risk: {a['risk_type']}")
        st.write(f"Queue: {last['route']['queue']}")
        if last["triggers"]:
            st.write("Escalation: " + ", ".join(t["condition"] for t in last["triggers"]))