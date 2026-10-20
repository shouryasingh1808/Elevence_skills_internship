"""Task 4 retrieval: finds the documents that best match a question."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Task_4.config import MAX_CHUNKS , MIN_SCORE

def search(questions, docs):
    if not docs:
        return []
    texts = [d["title"] + " " + d["text"] for d in docs]

    vec = TfidfVectorizer(stop_words="english")
    matrix = vec.fit_transform(texts)
    query = vec.transform([questions])
    scores = cosine_similarity(query , matrix)[0]
    ranked = sorted(
        [(float(s), d) for s, d in zip(scores, docs) if s >= MIN_SCORE],
        key=lambda x: x[0],
        reverse=True,
    )
    return ranked[:MAX_CHUNKS]