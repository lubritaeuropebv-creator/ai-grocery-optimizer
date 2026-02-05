import itertools
from core.matcher import match_ingredient

def compute_cart(ingredients, products):
    total = 0
    cart = []

    for ing in ingredients:
        product = match_ingredient(ing.name, products)
        if not product:
            return None

        cart.append({
            "ingredient": ing.name,
            "product": product.name,
            "shop": product.shop,
            "price": product.price
        })
        total += product.price

    return total, cart


def best_carts(ingredients, shop_products: dict):
    results = {}

    shops = list(shop_products.keys())

    for k in [1, 2, 3]:
        best = None

        for combo in itertools.combinations(shops, k):
            merged = []
            for s in combo:
                merged.extend(shop_products[s])

            cart = compute_cart(ingredients, merged)
            if cart and (best is None or cart[0] < best[0]):
                best = (*cart, combo)

        results[f"{k}_shop"] = best

    return results
