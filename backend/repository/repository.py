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


@dataclass(frozen=True)
class RepositoryMap:
    id: int
    name: str
    offset_x: float
    offset_y: float
    size_factor: float


@dataclass()
class RepositoryUser:
    lodestone_id: int
    job_levels: dict[str, int]

    def __init__(self, lodestone_id: int) -> None:
        self.lodestone_id = lodestone_id
        self.job_levels = {}


class Repository:
    _items: dict[int, RepositoryItem]
    _recipes: dict[int, RepositoryRecipe]
    _maps: dict[int, RepositoryMap]

    def __init__(self):
        self._items = {}
        self._recipes = {}
        self._maps = {}

    def add_item(self, item: RepositoryItem) -> None:
        self._items[item.id] = item

    def get_item(self, item_id: int) -> RepositoryItem | None:
        return self._items.get(item_id)

    def add_recipe(self, recipe: RepositoryRecipe) -> None:
        self._recipes[recipe.id] = recipe

    def get_recipe(self, recipe_id: int) -> RepositoryRecipe | None:
        return self._recipes.get(recipe_id)

    def add_map(self, map: RepositoryMap) -> None:
        self._maps[map.id] = map

    def get_map(self, map_id: int) -> RepositoryMap | None:
        return self._maps.get(map_id)
