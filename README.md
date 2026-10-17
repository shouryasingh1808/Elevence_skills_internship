# Elevence Support Chatbot

A customer-support chatbot that understands how the customer feels, escalates risky or unresolved conversations, and turns them into prioritised support tickets with SLA tracking.

Built with Python, Streamlit and the Groq LLM API (`openai/gpt-oss-120b`).

**Status:** Task 1 and Task 2 are done and tested. Tasks 3 to 6 are in progress.

## What it does

- **Understands each message.** Sentiment (positive, neutral, negative, frustrated, urgent, sarcastic), language, risk type and confidence scores, using the recent conversation history.
- **Adjusts the reply tone** to the customer's mood. Business policies stay fixed (no refund promises, no sensitive data).
- **Escalates** on repeated negative messages, on high-risk issues (account compromise, duplicate payment, legal threat, even when the customer is calm) and when a negative conversation stays unresolved for more than 15 minutes.
- **Routes by time.** Outside business hours, urgent cases go to an on-call queue and normal ones are scheduled for the next working day.
- **Creates support tickets** from escalated conversations: extracts order, product, issue, evidence and contact, asks for missing details, calculates priority, sets an SLA deadline and assigns an agent.
- **Tracks SLAs** in working time only (weekends and holidays are skipped), warns at 75% of the time and escalates automatically after a breach.
- **Detects duplicates**, groups related issues of the same order and keeps unrelated issues separate.
- **Protects privacy.** Emails, phone numbers and card numbers are masked before anything is sent to the LLM or shown in a handoff note.

## Design idea

The LLM only **understands** text (mood, risk, extracted details). All **decisions** (escalate or not, which queue, priority, deadline, which agent) are plain Python rules, so results are consistent and easy to test. All thresholds, business hours, SLA hours, holidays and agents live in config files, and a simulated clock (`set_time`) makes after-hours and SLA cases testable.

## Project structure

| Folder / file | Purpose |
|---|---|
| `Task_1/` | Sentiment analyzer, conversation state, escalation rules, queue routing, escalation records, tone-based replies |
| `Task_2/` | Ticket extraction, masking, priority, SLA engine, routing, duplicate detection, handoff summary |
| `chatbot/` | `engine.py` joins Task 1 and Task 2: a ticket is created when Task 1 escalates a conversation |
| `app.py` | Main Streamlit app (chat, mood, escalation, tickets, fake time) |
| `app_task1.py`, `app_task2.py` | Separate demos for each task |
| `Base_chatbot/` | Chatbot from the training course (FAQ bot) |
| `Data/` | Test case files |

## How to run

1. Python 3.10 or newer.
2. Create a virtual environment and install the packages:

        python -m venv .venv
        source .venv/bin/activate        # Windows: .venv\Scripts\activate
        pip install groq python-dotenv tzdata streamlit

3. Create a `.env` file in the project root:

        GROQ_API_KEY=your_key_here

4. Start the app:

        streamlit run app.py

The sidebar has a **fake time** option and a **Run timeouts** button to try after-hours cases and the 15-minute rule.

## Tests

Each part has a runner that prints PASS or FAIL for every case.

| Command | Cases | Result |
|---|---|---|
| `python -m Task_1.run_cases` | Sarcasm, calm high-risk, after-hours, repeated negative, 15-minute timeout | 14/14 |
| `python -m Task_2.run_cases` | Duplicates, unavailable teams, after-hours, SLA runtime changes, weekends | 15/15 |
| `python -m chatbot.run_cases` | Task 1 and Task 2 together, session isolation | 8/8 |

The runners call the Groq API, so a label (for example severity) can occasionally differ between runs.

## Known limits

- If a conversation contains a high-risk issue, all tickets created from it are marked critical.
- Replies and tickets are not yet fully multilingual (planned in Task 6).

## Credits

- The base chatbot comes from the training course repository (`aslin72/GEN---AI-course`) and was adapted for this internship.