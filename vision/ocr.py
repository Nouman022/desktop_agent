import pytesseract
from PIL import Image
from config import TESSERACT_PATH


pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


class OCRTool:

    @staticmethod
    def extract_text(image_path):

        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)

        return text