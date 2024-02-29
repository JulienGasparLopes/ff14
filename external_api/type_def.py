from dataclasses import dataclass
from pydantic import BaseModel, Field, model_validator, validator


@dataclass(frozen=True)
class ApiSearchResult(BaseModel):
    name: str = Field(alias="Name")
    item_id: int = Field(alias="ID")


@dataclass(frozen=True)
class ApiItem(BaseModel):
    id: int = Field(alias="ID")
    name: str = Field(alias="Name")
    recipe_id: int | None = Field(default=None, alias="Recipes")

    @validator("recipe_id", pre=True)
    def get_recipe_id(cls, data: dict[str, list[dict]]) -> int | None:
        return data[0].get("ID") if data else None  # type: ignore


@dataclass(frozen=True)
class ApiRecipeIngredient(BaseModel):
    item: ApiItem = Field()
    amount: int = Field()


@dataclass(frozen=True)
class ApiRecipe(BaseModel):
    id: int = Field(alias="ID")
    name: str = Field(alias="Name")
    item_id: int = Field(alias="ItemResultTargetID")
    ingredients: list[ApiRecipeIngredient] = Field()

    @model_validator(mode="before")
    def aggregate_ingredients(cls, data: dict) -> dict:
        ingredients = []
        for i in range(10):
            if amont := data.get(f"AmountIngredient{i}"):
                ingredient_data = {
                    "amount": amont,
                    "item": data[f"ItemIngredient{i}"],
                }
                ingredients.append(ApiRecipeIngredient.model_validate(ingredient_data))
        return {"ingredients": ingredients, **data}
