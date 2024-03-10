import json
from typing import Any

from PIL import Image, ImageGrab


def take_snapshot(
    x: int, y: int, width: int, height: int, grayscale: bool = False
) -> Image.Image:
    screen_image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    if grayscale:
        screen_image = screen_image.convert("L")
    return screen_image


def retrieve_file(file_name: str) -> dict[str, Any]:
    with open(file_name, "r") as f:
        return json.loads(f.read())
