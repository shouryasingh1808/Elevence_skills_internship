"""Task 4 conflicts: picks the most applicable document when a policy has several versions."""

def rank_key(doc , user_region):
    exact = 1 if doc["region"].lower() == (user_region or "").lower() else 0
    return (exact , doc["effective"]  , doc["version"])

def resolve_conflicts(results , user_region):
    best = {}
    for score , doc in results:
        current = best.get(doc["doc_id"])
        if current is None or rank_key(doc, user_region) > rank_key(current[1], user_region):
            best[doc["doc_id"]] = (score, doc)
    return sorted(best.values() , key=lambda x : x[0] , reverse=True)
