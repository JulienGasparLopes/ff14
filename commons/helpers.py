from PIL import ImageGrab


def take_snapshot(x: int, y: int, width: int, height: int, grayscale: bool = False):
    screen_image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    if grayscale:
        screen_image = screen_image.convert("L")
    return screen_image
