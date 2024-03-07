import os

import pytesseract
from PIL import Image


class OcrManager:
    def __init__(self) -> None:
        if os.name == "nt":
            pytesseract.pytesseract.tesseract_cmd = (
                "C:/Program Files/Tesseract-OCR/tesseract.exe"
            )

    def find_sentence_position(
        self, image: Image.Image, sentence: str, confidence: float = 0.75
    ) -> tuple[int, int] | None:
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

        words = sentence.split(" ")
        possibles_y = []
        possibles_x = []
        for word in words:
            if word in data["text"]:
                idx = data["text"].index(word)
                possibles_x.append(data["left"][idx])
                possibles_y.append(data["top"][idx])

        if len(possibles_x) >= confidence * len(words) and (
            max(possibles_y) - min(possibles_y) <= 4
        ):
            return min(possibles_x), min(possibles_y)

        return None

    def get_text_lines(self, image: Image.Image) -> list[str]:
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

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

        objects = [
            " ".join(words) for words in lines.values() if len(" ".join(words)) > 6
        ]
        return objects
