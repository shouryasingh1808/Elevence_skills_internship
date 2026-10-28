import streamlit as st
from datetime import datetime

from Task_1 import config as clock
from Task_4.assistant import answer_question
from Task_4.config import ACCESS_LEVELS
from Task_4.filters import valid_on
from Task_4.loader import load_documents
from Task_4.query import extract_date

st.title("KNOWLEDGE ASSISTANT 📚")

# Sidebar
with st.sidebar:
    st.header("Demo controls")
    user_level = st.selectbox("User level", list(ACCESS_LEVELS), index=1)
    region = st.selectbox("Region", ["(not set)", "india", "usa"])

    use_fake = st.checkbox("Use fake date")
    if use_fake:
        day = st.date_input("Date", datetime(2026, 10, 28))
        clock.set_time(datetime.combine(day, datetime.min.time()).replace(tzinfo=clock.TIMEZONE))
    else:
        clock.clear_time()
    st.write("Today:", clock.get_now().strftime("%d %b %Y"))

question = st.text_input("Question: ")
btn = st.button("Ask")

if btn and question:
    region_value = None if region == "(not set)" else region
    try:
        with st.spinner("Searching..."):
            result = answer_question(question, user_level=user_level, region=region_value)

        st.header("Answer")
        if result["status"] == "answered":
            st.write(result["answer"])
            st.write("Sources: " + ", ".join(result["sources"]))
        elif result["status"] in ("clarify", "refused"):
            st.write(result["answer"])
        else:
            st.error("I could not find a reliable answer to that. A support agent will help you.")

        with st.expander("Details"):
            asked = extract_date(question)
            st.write("Status:", result["status"])
            st.write("Date used:", asked or clock.get_now().date())
            st.write("User level:", user_level)
            st.write("Region:", region)
            if result.get("problems"):
                st.write("Rejected because:", ", ".join(result["problems"]))
    except Exception as e:
        st.error(f"Error: {e}")

st.header("Knowledge base")
today = clock.get_now().date()
for d in load_documents():
    valid = "valid" if valid_on(d, today) else "not valid"
    st.write(f"{d['file']} | v{d['version']} | {d['access']} | {d['region']} | {d['product']} | {valid} today")