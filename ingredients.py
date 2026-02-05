def scale_ingredients(recipe, persons):
    factor = persons / recipe.servings
    for ing in recipe.ingredients:
        ing.quantity *= factor
    recipe.servings = persons
    return recipe.ingredients
