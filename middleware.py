from dataclasses import dataclass
from typing import Optional
from external_api.requester import Requester
from repository.repository import (
    Repository,
    RepositoryItem,
    RepositoryRecipe,
    RepositoryRecipeIngredient,
)


@dataclass(frozen=True)
class MiddlewareObjectBase:
    _middleware: "Middleware"


@dataclass(frozen=True)
class MiddlewareItem(MiddlewareObjectBase, RepositoryItem):
    @classmethod
    def from_repository_item(
        cls, middleware: "Middleware", repository_item: RepositoryItem
    ) -> "MiddlewareItem":
        return cls(_middleware=middleware, **repository_item.__dict__)

    @property
    def recipe(self) -> Optional["MiddlewareRecipe"]:
        if self.recipe_id is None:
            return None
        return self._middleware.get_recipe(self.recipe_id)


@dataclass(frozen=True)
class MiddlewareRecipeIngredient(MiddlewareObjectBase, RepositoryRecipeIngredient):
    @classmethod
    def from_repository_recipe_ingredient(
        cls,
        middleware: "Middleware",
        repository_recipe_ingredient: RepositoryRecipeIngredient,
    ) -> "MiddlewareRecipeIngredient":
        return cls(_middleware=middleware, **repository_recipe_ingredient.__dict__)

    @property
    def item(self) -> MiddlewareItem:
        return self._middleware.get_item(self.item_id)


@dataclass(frozen=True)
class MiddlewareRecipe(MiddlewareObjectBase, RepositoryRecipe):
    ingredients: list[MiddlewareRecipeIngredient]

    @classmethod
    def from_repository_recipe(
        cls, middleware: "Middleware", repository_recipe: RepositoryRecipe
    ) -> "MiddlewareRecipe":
        data = repository_recipe.__dict__.copy()
        ingredients = [
            MiddlewareRecipeIngredient.from_repository_recipe_ingredient(
                middleware, ingredient
            )
            for ingredient in data.pop("ingredients", [])
        ]
        return cls(_middleware=middleware, ingredients=ingredients, **data)

    @property
    def item(self) -> MiddlewareItem:
        return self._middleware.get_item(self.item_id)


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
