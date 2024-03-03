import time
from commons.domain.item.helpers import get_item_ingredients
from commons.helpers import take_snapshot
from commons.middleware.middleware import Middleware, MiddlewareItem
from commons.text_recognition.ocr_manager import OcrManager

middleware: Middleware

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


def search_item_ingredients(item_name: str) -> dict[str, int]:
    items = middleware.search_item(item_name)

    needed_ingredients = get_item_ingredients(items[0])
    return {item.name: needed_ingredients.count(item) for item in needed_ingredients}


def process_grand_company_items() -> dict[str, int]:
    ocr_manager = OcrManager()

    while True:
        time.sleep(1)
        screen_image = take_snapshot(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, grayscale=True)
        gui_position = ocr_manager.find_sentence_position(
            screen_image, "Grand Company Delivery Missions"
        )
        if gui_position is None:
            continue

        gui_image = take_snapshot(
            gui_position[0], gui_position[1] + 100, 300, 200, grayscale=True
        )
        item_names = ocr_manager.get_text_lines(gui_image)

        items_amount = {}

        for item_name in item_names:
            print("Looking for item ", item_name)
            item = middleware.search_item(item_name)

            if not item:
                print("Item not found. Abort")
                continue

            for needed_ingredient in get_item_ingredients(item[0]):
                if needed_ingredient.name not in items_amount:
                    items_amount[needed_ingredient.name] = 0

                items_amount[needed_ingredient.name] += 1

        return items_amount


def sandbox() -> None:
    items = middleware.search_item("copper ore")  # 5106
    item = middleware.get_item(5106)
    ...


def main() -> None:
    # Simple item search
    # item_ingredients = search_item_ingredients("chondrite magitek war scythe")
    # print(item_ingredients)

    # Grand company items ingredients
    # items_amount = process_grand_company_items()
    # print(items_amount)

    # Sandbox
    sandbox()


if __name__ == "__main__":
    middleware = Middleware()
    main()
