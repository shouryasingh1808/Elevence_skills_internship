import shutil
from datetime import datetime
from pathlib import Path

import streamlit as st

from Task_1 import config as clock
import Task_3.config as t3
import Task_3.pipeline as pipeline
import Task_3.quality as quality
import Task_3.run_cases as rc
import Task_3.scanner as scanner
from Task_3 import monitor
from Task_3.activation import run_health_check
from Task_3.pipeline import manual_rollback, run_update
from Task_3.scheduler import tick
from Task_4.assistant import answer_question
from Task_4.config import ACCESS_LEVELS
from Task_4.loader import load_documents

DEMO = Path("Data/task3_demo")


def apply_demo_paths():
    for module, name, value in rc.PATCHES:
        setattr(module, name, DEMO / value.relative_to(rc.ROOT))


def reset_demo():
    shutil.rmtree(DEMO, ignore_errors=True)
    for name in ("incoming", "quarantine", "versions"):
        (DEMO / name).mkdir(parents=True)
    shutil.copytree("Data/kb", DEMO / "kb")


if not (DEMO / "kb").exists():
    reset_demo()
apply_demo_paths()
scanner.ensure_baseline()

if not hasattr(quality, "_real_evaluate"):
    quality._real_evaluate = quality.evaluate
    pipeline._real_health = pipeline.health_check

st.title("KNOWLEDGE BASE UPDATE PIPELINE 🔄")

with st.sidebar:
    st.header("Demo controls")
    role = st.selectbox("Role", list(ACCESS_LEVELS), index=3)
    fast = st.checkbox("Fast demo (no Groq tests)", value=True)
    outage = st.checkbox("Simulate service outage", disabled=not fast)
    unhealthy = st.checkbox("Simulate unhealthy update", disabled=not fast)

    use_fake = st.checkbox("Use fake time")
    if use_fake:
        day = st.date_input("Date", datetime(2026, 10, 6))
        hour = st.time_input("Time", datetime(2026, 10, 6, 11, 0).time())
        clock.set_time(datetime.combine(day, hour).replace(tzinfo=clock.TIMEZONE))
    else:
        clock.clear_time()
    st.write("Now:", clock.get_now().strftime("%a %d %b %Y, %I:%M %p"))
    st.write("Maintenance window: 02:00 - 04:00")

    if st.button("Reset demo"):
        reset_demo()
        apply_demo_paths()
        scanner.ensure_baseline()
        st.session_state.result = None

if fast:
    quality.evaluate = rc.fake_evaluate
    pipeline.health_check = rc.fake_health
else:
    quality.evaluate = quality._real_evaluate
    pipeline.health_check = pipeline._real_health
rc.FAKE["outage"] = fast and outage
rc.FAKE["health"] = "bad" if (fast and unhealthy) else "ok"

# ---------- Add documents ----------
st.header("1. Add a document")
SAMPLES = {
    "Valid new document": ("return_shipping.txt", rc.GOOD),
    "Invalid file (no header)": ("bad.txt", "This file has no header."),
    "Prompt injection": ("injected.txt", rc.INJECTED),
    "Wrong fact (quality drop, fast mode)": ("wrong_fact.txt", rc.WRONG),
    "Duplicate of an existing document": ("refund_copy.txt", None),
}
choice = st.selectbox("Sample document", list(SAMPLES))
if st.button("Add sample to incoming"):
    name, text = SAMPLES[choice]
    if text is None:
        text = (Path(t3.ACTIVE_KB) / "refund_policy_v2.txt").read_text(encoding="utf-8")
    (t3.INCOMING / name).write_text(text, encoding="utf-8")
    st.success(f"Added {name} to incoming")

uploaded = st.file_uploader("Or upload your own .txt document", type=["txt"])
if uploaded is not None and st.button("Save upload to incoming"):
    (t3.INCOMING / uploaded.name).write_bytes(uploaded.getvalue())
    st.success(f"Saved {uploaded.name} to incoming")

# ---------- Run the pipeline ----------
st.header("2. Run the pipeline")
c1, c2, c3, c4 = st.columns(4)
if c1.button("Run update"):
    with st.spinner("Running update..."):
        st.session_state.result = run_update("demo_user", role)
if c2.button("Scheduler tick"):
    with st.spinner("Running scheduler tick..."):
        st.session_state.result = tick(lambda: run_update("scheduler", "admin"))
if c3.button("Health check"):
    with st.spinner("Checking..."):
        st.session_state.result = run_health_check(pipeline.health_check)
if c4.button("Roll back"):
    st.session_state.result = manual_rollback("demo_user", role)

if st.session_state.get("result"):
    st.write("Result:")
    st.json(st.session_state.result)

# ---------- Status ----------
st.header("3. Status")
manifest = scanner.load_manifest()
st.write(f"Active version: {manifest['active_version']} | previous: {manifest.get('previous_version')} | "
         f"pending: {manifest.get('pending')} | health: {manifest.get('health', '-')}")
st.write("Schedule:", manifest.get("schedule", "not started"))
st.write("Live KB:", sorted(p.name for p in Path(t3.ACTIVE_KB).glob("*.txt")))
st.write("Incoming:", sorted(p.name for p in Path(t3.INCOMING).glob("*.txt")))
st.write("Quarantine:", sorted(p.name for p in Path(t3.QUARANTINE).glob("*.txt")))

with st.expander("Monitoring"):
    st.json(monitor.summary())

with st.expander("Audit log (last 5)"):
    if Path(t3.AUDIT_FILE).exists():
        for line in Path(t3.AUDIT_FILE).read_text(encoding="utf-8").splitlines()[-5:]:
            st.code(line)

# ---------- Ask the live KB ----------
st.header("4. Ask the live knowledge base")
question = st.text_input("Question: ")
if st.button("Ask") and question:
    with st.spinner("Searching..."):
        answer = answer_question(question, docs=load_documents(t3.ACTIVE_KB))
    if answer["status"] == "answered":
        st.write(answer["answer"])
        st.write("Sources: " + ", ".join(answer["sources"]))
    elif answer["status"] in ("clarify", "refused"):
        st.write(answer["answer"])
    else:
        st.error("Could not find a reliable answer.")