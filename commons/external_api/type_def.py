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

    job_name: str = Field(alias="ClassJob")
    job_abbreviation: str = Field(alias="ClassJob")
    job_required_level: int = Field(alias="RecideLevelTable")

    @validator("job_name", pre=True)
    def get_job_name(cls, data: dict[str, str]) -> str:
        return data.get("Name", "")

    @validator("job_abbreviation", pre=True)
    def get_job_abbreviation(cls, data: dict[str, str]) -> str:
        return data.get("Abbreviation", "")

    @validator("job_required_level", pre=True)
    def get_job_required_level(cls, data: dict[str, str]) -> str:
        return data.get("ClassJobLevel", "")

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


@dataclass(frozen=True)
class ApiMap(BaseModel):
    id: int = Field(alias="ID")
    name: str = Field(alias="PlaceName")
    offset_x: float = Field(alias="OffsetX")
    offset_y: float = Field(alias="OffsetY")
    size_factor: float = Field(alias="SizeFactor")

    @validator("name", pre=True)
    def get_name(cls, data: dict[str, str]) -> str:
        return data.get("Name", "")
