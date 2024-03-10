import json
import math
from os import listdir
from os.path import isfile

from PIL import Image

from backend.domain.item.helpers import get_item_ingredients
from backend.external_api.requester import Requester
from backend.middleware.middleware import Middleware
from backend.middleware.type_def import MiddlewareMap
from backend.repository.repository import RepositoryUser
from backend.text_recognition.ocr_manager import OcrManager

middleware: Middleware

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


def search_item_ingredients(item_name: str) -> dict[str, int]:
    items = middleware.search_item(item_name)

    needed_ingredients = get_item_ingredients(items[0])
    return {item.name: needed_ingredients.count(item) for item in needed_ingredients}


def process_grand_company_items(
    ocr_manager: OcrManager, image: Image.Image
) -> tuple[dict[int, int], dict[int, str]]:
    gui_position = ocr_manager.find_sentence_position(
        image, "Grand Company Delivery Missions"
    )
    if gui_position is None:
        return ({}, {})

    gui_image = image.crop(
        (
            gui_position[0],
            gui_position[1] + 100,
            gui_position[0] + 300,
            gui_position[1] + 150,
        )
    )
    item_names = ocr_manager.get_text_lines(gui_image)

    items_amount = {}
    items_name = {}

    for item_name in item_names:
        print("Looking for item ", item_name)
        item = middleware.search_item(item_name)

        if not item:
            print("Item not found. Abort")
            continue

        for needed_ingredient in get_item_ingredients(item[0]):
            if needed_ingredient.name not in items_amount:
                items_amount[needed_ingredient.id] = 0

            items_amount[needed_ingredient.id] += 1
            items_name[needed_ingredient.id] = needed_ingredient.name

    return items_amount, items_name


def to_map_coord(
    coord_x: float,
    coord_y: float,
    map_offset_x: float = 0,
    map_offset_y: float = 0,
    map_factor: float = 200,
) -> tuple[float, float]:
    c = map_factor / 100
    x1 = (coord_x + map_offset_x) * c
    y1 = (coord_y + map_offset_y) * c
    x = math.floor(((41.0 / c) * ((x1 + 1024.0) / 2048.0) + 1) * 100) / 100
    # y seems to be 3.6 to high, maybe 41 is not the right value
    y = math.floor(((41.0 / c) * ((y1 + 1024.0) / 2048.0) + 1) * 100) / 100

    return x, y


def _find_npc_vendors(item_id: int) -> list:
    file_names = [
        file_name
        for file_name in listdir("data")
        if isfile(f"data/{file_name}") and ("enpcResident" in file_name)
    ]
    results = []
    for file_name in file_names:
        file_path = f"data/{file_name}"
        with open(file_path, "r") as file:
            for _, npc in json.load(file).items():
                if not npc.get("gil_shop"):
                    continue
                if "material supplier" in npc.get("name") or "resupply node" in npc.get(
                    "name"
                ):
                    continue
                for gil_shop in npc.get("gil_shop"):
                    for item in gil_shop.get("Items"):
                        if item.get("ID") == item_id:
                            results.append(npc)

    return results


def get_npc_position_info(
    middleware: Middleware, npc_id: int
) -> tuple[MiddlewareMap, float, float] | None:
    file_names = [
        file_name
        for file_name in listdir("data")
        if isfile(f"data/{file_name}") and ("level_" in file_name)
    ]
    for file_name in file_names:
        file_path = f"data/{file_name}"
        with open(file_path, "r") as file:
            for _, level in json.load(file).items():
                if level.get("object_id") == npc_id:
                    map = middleware.get_map(level["map_id"])
                    x, y = to_map_coord(
                        float(level["x"]),
                        float(level["y"]),
                        map.offset_x,
                        map.offset_y,
                        map.size_factor,
                    )
                    return map, x, y
    return None


def get_item_vendor_info(item_id: int) -> dict[str, tuple[str, float, float]]:
    npc_vendors = _find_npc_vendors(item_id)
    npc_info = {}
    for npc in npc_vendors:
        map_info = get_npc_position_info(middleware, npc["enpc_resident_id"])
        if map_info:
            map_obj, x, y = map_info
            npc_info[npc["name"]] = (map_obj.name, x, y)
        else:
            npc_info[npc["name"]] = ("", -1, -1)
    return npc_info


def main() -> None:
    requester = Requester()
    middleware = Middleware()

    user = RepositoryUser(lodestone_id=51585086)
    user.job_levels["blacksmith"] = 12

    # ----- Simple item search -----
    item_ingredients = search_item_ingredients("chondrite magitek war scythe")
    print(item_ingredients)

    # ----- Grand Company Menu Fetch -----
    # ocr_manager = OcrManager()
    # while True:
    #     time.sleep(1)
    #     screen_image = take_snapshot(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, grayscale=True)
    #     item_amounts = process_grand_company_items(ocr_manager, screen_image)
    #     print(item_amounts)

    # ------ Test Grand Company Menu -----
    ocr_manager = OcrManager()
    screen_image = Image.open("grand_company_screenshot.png")
    item_amounts, item_names = process_grand_company_items(ocr_manager, screen_image)
    vendor_items_info = {}
    for item_id, amount in item_amounts.items():
        item_name = item_names[item_id]
        vendor_mapping = get_item_vendor_info(item_id)
        for vendor_name, (map_name, x, y) in vendor_mapping.items():
            if vendor_name not in vendor_items_info:
                vendor_items_info[vendor_name] = []
            vendor_items_info[vendor_name].append(item_name)
    print(vendor_items_info)

    # ----- Sandbox -----

    # ----- API resources fetch -----
    # process_all_resources("level", _process_level, starting_page=161)
    # process_all_resources("enpcResident", _process_enpc_resident, starting_page=41)
    # process_all_resources(
    #     "gilShop", process_gil_shop, starting_page=1, api_call_per_page=1
    # )
    # process_all_resources("territoryType", _process_territory)


if __name__ == "__main__":
    middleware = Middleware()
    main()
