from commons.middleware.type_def import MiddlewareItem, MiddlewareRecipe
from commons.external_api.requester import Requester
from commons.repository.repository import (
    Repository,
    RepositoryItem,
    RepositoryRecipe,
    RepositoryRecipeIngredient,
)


class Middleware:
    _repository: Repository
    _requester: Requester

    def __init__(self) -> None:
        self._repository = Repository()
        self._requester = Requester()

    def search_item(self, item_name: str) -> list[MiddlewareItem]:
        api_search_results = self._requester.search(item_name)
        items = []
        for result in api_search_results:
            item = self.get_item(result.item_id)
            items.append(item)
        return items

    def get_item(self, item_id: int) -> MiddlewareItem:
        item: RepositoryItem | None = self._repository.get_item(item_id)
        if item is None:
            api_item = self._requester.get_item(item_id)
            item = RepositoryItem(
                id=api_item.id,
                name=api_item.name,
                recipe_id=api_item.recipe_id,
            )
            self._repository.add_item(item)
        return MiddlewareItem.from_repository_item(self, item)

    def get_recipe(self, recipe_id: int) -> MiddlewareRecipe:
        recipe = self._repository.get_recipe(recipe_id)
        if recipe is None:
            api_recipe = self._requester.get_recipe(recipe_id)
            recipe = RepositoryRecipe(
                id=api_recipe.id,
                name=api_recipe.name,
                item_id=api_recipe.item_id,
                ingredients=[
                    RepositoryRecipeIngredient(
                        item_id=ingredient.item.id, amount=ingredient.amount
                    )
                    for ingredient in api_recipe.ingredients
                ],
            )
            self._repository.add_recipe(recipe)
        return MiddlewareRecipe.from_repository_recipe(self, recipe)
