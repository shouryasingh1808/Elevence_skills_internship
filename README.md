## Task 1: Multilingual Sentiment Analysis and Escalation

**What it does**
- Reads each message with the Groq LLM (gpt-oss-120b) and returns sentiment
  (positive, neutral, negative, frustrated, urgent, sarcastic), confidence,
  language and risk type, using recent conversation history.
- Adjusts the reply tone by sentiment; business policies stay fixed.
- Escalates on repeated negative messages, high-risk issues (account compromise,
  duplicate payment, legal threat) and negative conversations unresolved for 15+ minutes.
- After hours: urgent -> on-call queue, normal -> next working day.
- Every escalation saves reason, condition and conversation summary.

**Design**
- The LLM only understands the message; escalation rules are plain Python.
- All thresholds and business hours are in `Task_1/config.py`.
- A simulated clock (`set_time`) allows testing after-hours and timeout cases.

**Files**: config.py, analyzer.py, state.py, escalation.py, records.py,
responder.py, pipeline.py, run_cases.py

**Run**
pip install -r requirements.txt
python -m Task_1.run_cases
streamlit run app_task1.py

**Credit**: base chatbot adapted from the training course repo (aslin72/GEN---AI-course).