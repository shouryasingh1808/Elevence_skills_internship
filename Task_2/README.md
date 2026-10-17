# Task 2: Support Ticket Workflow

Turns an unresolved conversation into structured support tickets with priority, SLA deadline and an assigned agent. The full project overview is in the [main README](../README.md).

## Flow

1. **Extract** customer, order, product, issue, evidence and contact. Email and phone come from regex, not from the LLM. An order ID that is not in the customer's text is dropped.
2. **Ask for missing details.** Order ID, issue and contact are mandatory. If one is missing, no ticket is created and a question is returned.
3. **Check duplicates.** Then create the ticket, calculate priority, set the SLA deadline, assign an agent and write a masked handoff note.

One message with two problems creates two tickets.

## Rules

- **Priority.** A score out of 100 from severity (40), sentiment (20), waiting time (20) and customer impact (20). P1 is 75 or more, P2 is 50 or more, P3 is 25 or more, otherwise P4. Critical severity is always at least P1.
- **SLA.** P1 4h, P2 8h, P3 24h, P4 48h, counted in working time only (no Sundays, no holidays). Warning at 75%, automatic escalation after 100%. The deadline is always calculated from the current config, so changing SLA hours or holidays at runtime works.
- **Routing.** Skill match, available, under max load, lowest workload. If the team is unavailable it falls back to the general team, otherwise the ticket waits in a queue (P1 goes to a supervisor queue). Outside business hours P1 goes to on-call and the rest to the next working day.
- **Duplicates.** Same order and category within 24 hours while the first ticket is open means duplicate (linked, no new work). Same order with a different category means related (same group ID, separate tickets). Anything else is a new ticket.
- **Privacy.** Emails, phone numbers and card numbers are masked before text goes to the LLM, in the handoff header and in the summary.

## Files

| File | Purpose |
|---|---|
| `config.py` | Teams, SLA hours, holidays, weights, agents, mandatory fields |
| `tickets.py` | The ticket card and a simple in-memory store |
| `masking.py` | Masks email, phone and card numbers |
| `extractor.py` | Groq extraction, missing fields and the question to the customer |
| `priority.py` | Priority score and P1 to P4 |
| `sla.py` | Working-time maths, deadline, warning and breach |
| `routing.py` | Agent selection and queues |
| `duplicates.py` | Duplicate, related and new decision, grouping |
| `handoff.py` | Masked handoff note for the agent |
| `pipeline.py` | Runs the whole flow for one conversation |
| `run_cases.py` | Test runner (PASS or FAIL per case) |

## Test

    python -m Task_2.run_cases

Result: **15/15 passed.** Cases cover two problems in one message, missing details, duplicates (inside and outside the 24-hour window), different orders, unavailable agents and teams, max load, after-hours requests, prompt injection, SLA warning and breach, a weekend and an SLA change at runtime.

![Task 2 tests](../docs/screenshots/task2_run_cases.png)

## Known limits

- Tickets are stored in memory and are lost when the app restarts.
- Severity, category and similar labels come from an LLM and can differ slightly between runs.
- When a high-risk issue is found, all tickets from that conversation are marked critical.