from rapidfuzz import process

def match_ingredient(ingredient_name, products):
    names = [p.name for p in products]

    match, score, idx = process.extractOne(
        ingredient_name.lower(), names
    )

    if score >= 70:
        return products[idx]

    return None
