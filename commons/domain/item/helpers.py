from commons.middleware.type_def import MiddlewareItem


def get_item_ingredients(item: MiddlewareItem) -> list[MiddlewareItem]:
    if not item.recipe:
        return [item]

    items = []
    for ingredient in item.recipe.ingredients:
        items += get_item_ingredients(ingredient.item) * ingredient.amount
    return items
