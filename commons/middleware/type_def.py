from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from commons.repository.repository import (
    RepositoryItem,
    RepositoryRecipe,
    RepositoryRecipeIngredient,
)

if TYPE_CHECKING:
    from .middleware import Middleware


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
