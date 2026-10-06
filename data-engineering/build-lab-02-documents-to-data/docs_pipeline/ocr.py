from pathlib import Path

import pytesseract
from PIL import Image


def ocr_folder(folder):
    texts = {}
    for png in sorted(Path(folder).glob("*.png")):
        img = Image.open(png).convert("L")
        # Tesseract: pixels in, characters out
        text = pytesseract.image_to_string(img)
        texts[png.name] = text
    return texts
