"""Task 4 filters: rules that decide which documents may be used for a question."""

from Task_4.config import ACCESS_LEVELS

def allowed_by_access(doc,user_level):
    needed = ACCESS_LEVELS.get(doc["access"] , 99)
    return ACCESS_LEVELS[user_level] >= needed

def valid_on(doc , on_date):
    return doc["effective"] <= on_date and (doc["expires"] is None or on_date <= doc["expires"])

def allowed_by_region(doc, user_region):
    region = doc["region"].lower()
    return region == "global" or region == (user_region or "").lower()

def allowed_by_product(doc , product):
    if not product:
        return True
    return doc["product"].lower() in ("all", product.lower())

def usable_documents(docs, user_level, on_date, region=None, product=None):
    return[
        d for d in docs
        if allowed_by_access(d , user_level)
        and valid_on(d , on_date)
        and allowed_by_region(d , region)
        and allowed_by_product(d , product)

    ]