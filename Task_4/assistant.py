"""Task 4 assistant: answers a customer question using the knowledge base."""

from Task_1 import config as clock
from Task_4.config import DEFAULT_USER_LEVEL
from Task_4.loader import load_documents
from Task_4.query import extract_date , extract_product
from Task_4.filters import usable_documents
from Task_4.retrieval import search
from Task_4.conflicts import resolve_conflicts
from Task_4.answer import REFUSAL , build_context , generate_answer , normalize_citations , check_citations , cited_numbers ,check_numbers

def answer_question(question , user_level=DEFAULT_USER_LEVEL , region = None , docs = None):
    docs = docs if docs is not None else load_documents()
    asked_date =  extract_date(question)
    on_date = asked_date or clock.get_now().date()
    product = extract_product(question, docs)
    
    pool = usable_documents(docs, user_level, on_date, region, product)
    results = resolve_conflicts(search(question , pool ), region)
    if not results:
        return {"status": "refused", "answer": REFUSAL + ".", "sources": []}
    products = {d["product"].lower() for s, d in results if d["product"].lower() != "all"}
    if product is None and len(products) > 1:
        return {"status": "clarify",
                "answer": "Which product is this about: " + " or ".join(sorted(products)) + "?",
                "sources": []}

    context = build_context(results)
    answer = generate_answer(question , context)
    if answer is None:
        return {"status": "error", "answer": None, "sources": []}
    answer = normalize_citations(answer)
    answer = " ".join(answer.split())
    if REFUSAL in answer.replace("’", "'"):
        return {"status": "refused", "answer": REFUSAL + ".", "sources": []}
    problems = check_citations(answer , len(results)) + check_numbers(answer , results)
    if problems:
        return {"status": "rejected", "answer": None, "sources": [] , "problems": problems}
    

    return {"status": "answered", "answer": answer , 
            "sources": [results[n - 1][1]["file"] for n in sorted(set(cited_numbers(answer)))]}

