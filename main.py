from middleware import Middleware, MiddlewareItem


def main() -> None:

    middleware = Middleware()
    items = middleware.search_item("chondrite magitek war scythe")

    needed_ingredients = get_item_ingredients(items[0])
    items_amount = {
        item.name: needed_ingredients.count(item) for item in needed_ingredients
    }
    print(items_amount)
    ...


def get_item_ingredients(item: MiddlewareItem) -> list[MiddlewareItem]:
    if not item.recipe:
        return [item]

    items = []
    for ingredient in item.recipe.ingredients:
        items += get_item_ingredients(ingredient.item) * ingredient.amount
    return items


if __name__ == "__main__":
    main()
