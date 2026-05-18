import pyautogui


class KeyboardTools:

    @staticmethod
    def write(text):
        pyautogui.write(text, interval=0.05)

    @staticmethod
    def press(key):
        pyautogui.press(key)

    @staticmethod
    def hotkey(*keys):
        pyautogui.hotkey(*keys)