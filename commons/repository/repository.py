from dataclasses import dataclass


@dataclass(frozen=True)
class RepositoryItem:
    id: int
    name: str
    recipe_id: int | None


@dataclass(frozen=True)
class RepositoryRecipeIngredient:
    item_id: int
    amount: int


@dataclass(frozen=True)
class RepositoryRecipe:
    id: int
    name: str
    item_id: int
    ingredients: list[RepositoryRecipeIngredient]


class Repository:
    _items: dict[int, RepositoryItem]
    _recipes: dict[int, RepositoryRecipe]

    def __init__(self):
        self._items = {}
        self._recipes = {}

    def add_item(self, item: RepositoryItem) -> None:
        self._items[item.id] = item

    def get_item(self, item_id: int) -> RepositoryItem | None:
        return self._items.get(item_id)

    def add_recipe(self, recipe: RepositoryRecipe) -> None:
        self._recipes[recipe.id] = recipe

    def get_recipe(self, recipe_id: int) -> RepositoryRecipe | None:
        return self._recipes.get(recipe_id)
