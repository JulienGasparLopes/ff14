import numpy as np
import pyautogui
import pytesseract
from PIL import ImageGrab

img2 = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
text = pytesseract.image_to_data(img2, output_type=pytesseract.Output.DICT)

print(text)

for i in range(len(text["text"])):
    if text["text"][i]:
        print("Text: ", text["text"][i])
        print(
            "Position: ",
            text["left"][i],
            text["top"][i],
            text["width"][i],
            text["height"][i],
        )
        print("======")


start_coord = None

# while True:
#     if keyboard.is_pressed(12):
#         start_coord = pyautogui.position()
#     else:
#         if start_coord:
#             end_coord = pyautogui.position()
#             bounds = (end_coord[0] - start_coord[0], end_coord[1] - start_coord[1])
#             screen_image = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
#             data = pytesseract.image_to_data(
#                 screen_image, output_type=pytesseract.Output.DICT
#             )
#             ...
#         is_pressing = False
