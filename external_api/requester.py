import requests

from external_api.type_def import ApiItem, ApiRecipe, ApiSearchResult


class Requester:
    def __init__(self):
        self._base_url = "https://xivapi.com"

    def get(self, endpoint: str, id: int | str | None = None, **kwargs) -> dict:
        if id:
            endpoint = f"{endpoint}/{id}"
        response = requests.get(f"{self._base_url}/{endpoint}", params=kwargs)
        return response.json()

    def search(
        self,
        value: str,
        indexes: list[str] = ["Item"],
        algo: str = "match",
    ) -> list[ApiSearchResult]:
        response = requests.get(
            f"{self._base_url}/search",
            params={"indexes": ",".join(indexes), "string": value, "string_algo": algo},
        )
        return [
            ApiSearchResult.model_construct(**result)
            for result in response.json()["Results"]
        ]

    def get_item(self, item_id: int) -> ApiItem:
        return ApiItem.model_validate(self.get("Item", item_id))

    def get_recipe(self, recipe_id: int) -> ApiRecipe:
        return ApiRecipe.model_validate(self.get("Recipe", recipe_id))
