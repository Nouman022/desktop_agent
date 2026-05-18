import mss
from PIL import Image
import time


class ScreenshotTool:

    @staticmethod
    def capture():

        filename = f"screenshots/screen_{int(time.time())}.png"

        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)

            image = Image.frombytes(
                "RGB",
                screenshot.size,
                screenshot.rgb
            )

            image.save(filename)

        return filename