import pytesseract
from PIL import ImageGrab
import time
from middleware import Middleware, MiddlewareItem

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"


def main():
    middleware = Middleware()

    while True:
        time.sleep(1)
        screen_image = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
        screen_image = screen_image.convert("L")
        data = pytesseract.image_to_data(
            screen_image, output_type=pytesseract.Output.DICT
        )

        possibles_y = []
        possibles_x = []
        for word in ["Grand", "Company", "Delivery", "Missions"]:
            if word in data["text"]:
                idx = data["text"].index(word)
                possibles_x.append(data["left"][idx])
                possibles_y.append(data["top"][idx])

        if len(possibles_x) >= 3:
            print("Found !")
            screen_image = ImageGrab.grab(
                bbox=(
                    min(possibles_x),
                    min(possibles_y) + 100,
                    min(possibles_x) + 400,
                    min(possibles_y) + 300,
                )
            )
            # screen_image = screen_image.convert("L")
            data = pytesseract.image_to_data(
                screen_image, output_type=pytesseract.Output.DICT
            )
            item_names = process_words(data)

            items_amount = {}

            for item_name in item_names:
                print("Looking for items ", item_name)
                items = middleware.search_item(item_name)

                if not items:
                    print("Item not found. Abort")
                    continue

                needed_ingredients = get_item_ingredients(items[0])
                for needed_ingredient in needed_ingredients:
                    if needed_ingredient.name not in items_amount:
                        items_amount[needed_ingredient.name] = 0

                    items_amount[needed_ingredient.name] += 1

                local_items_amount = {
                    item.name: needed_ingredients.count(item)
                    for item in needed_ingredients
                }
                print(local_items_amount)

            print(items_amount)

        else:
            print("Not Found")


def get_item_ingredients(item: MiddlewareItem) -> list[MiddlewareItem]:
    if not item.recipe:
        return [item]

    items = []
    for ingredient in item.recipe.ingredients:
        items += get_item_ingredients(ingredient.item) * ingredient.amount
    return items


def process_words(data):
    lines: dict[int, list[str]] = {}
    for i in range(len(data["text"])):
        text = data["text"][i]
        width = data["width"][i]
        height = data["height"][i]
        left = data["left"][i]
        top = data["top"][i]

        if not text or text[0] == text[0].lower():
            continue

        if top - 1 in lines:
            top = top - 1
        elif top + 1 in lines:
            top = top + 1

        if top not in lines:
            lines[top] = []
        lines[top].append(text)

    objects = [" ".join(words) for words in lines.values() if len(" ".join(words)) > 6]
    return objects


if __name__ == "__main__":
    main()
