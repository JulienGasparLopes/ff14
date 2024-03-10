import json
from typing import Any, Callable

from backend.external_api.requester import Requester


def process_all_resources(
    object_type: str,
    process_function: Callable[[Any], tuple[Any, dict[str, Any]]],
    starting_page: int = 1,
    api_call_per_page: int = 20,
) -> None:
    requester = Requester()
    max_page = 99999
    current_page = starting_page
    mapping = {}
    while current_page <= max_page:
        print(f"Processing page {current_page} of {max_page}")
        response = requester.get(object_type, page=current_page)
        max_page = response["Pagination"]["PageTotal"]
        for item in response["Results"]:
            current_response = requester.get(item["Url"])
            object_id, object_data = process_function(current_response)
            mapping[object_id] = object_data

        if current_page % api_call_per_page == 0:
            with open(f"{object_type}_{current_page}.json", "w") as f:
                f.write(json.dumps(mapping, indent=4))
            mapping = {}

        current_page += 1

    if mapping:
        with open(f"{object_type}_{current_page}.json", "w") as f:
            f.write(json.dumps(mapping, indent=4))


# Processors


def process_territory(object: Any) -> tuple[Any, dict[str, Any]]:
    territory_id = object.get("ID")
    map_id = (object.get("Map") or {}).get("ID")
    place_name = (object.get("PlaceName") or {}).get("Name")
    place_id = (object.get("PlaceName") or {}).get("ID")
    return territory_id, {
        "territory_id": territory_id,
        "place_id": place_id,
        "map_id": map_id,
        "place_name": place_name,
    }


def process_level(object: Any) -> tuple[Any, dict[str, Any]]:
    level_id = object.get("ID")
    map_id = object.get("MapTargetID")
    territory_id = object.get("TerritoryTargetID")
    game_content = object.get("GameContentLinks") or {}
    object_id = object.get("Object")
    x = object.get("X")
    y = object.get("Y")
    z = object.get("Z")
    yaw = object.get("Yaw")
    return level_id, {
        "level_id": level_id,
        "territory_id": territory_id,
        "object_id": object_id,
        "map_id": map_id,
        "game_content": game_content,
        "x": x,
        "y": y,
        "z": z,
        "yaw": yaw,
    }


def process_gil_shop(object: Any) -> tuple[Any, dict[str, Any]]:
    gil_shop_id = object.get("ID")
    name = object.get("Name")
    game_content = object.get("GameContentLinks") or {}
    items = object.get("Items") or {}
    return gil_shop_id, {
        "gil_shop_id": gil_shop_id,
        "name": name,
        "game_content": game_content,
        "items": items,
    }


def process_enpc_resident(object: Any) -> tuple[Any, dict[str, Any]]:
    enpc_resident_id = object.get("ID")
    name = object.get("Name")
    map_id = object.get("Map")
    special_shop = object.get("SpecialShop")
    gil_shop = object.get("GilShop")
    game_content = object.get("GameContentLinks") or {}
    return enpc_resident_id, {
        "enpc_resident_id": enpc_resident_id,
        "name": name,
        "map_id": map_id,
        "special_shop": special_shop,
        "gil_shop": gil_shop,
        "game_content": game_content,
    }
