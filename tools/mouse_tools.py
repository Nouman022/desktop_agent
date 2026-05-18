import pyautogui


class MouseTools:

    @staticmethod
    def move(x, y):
        pyautogui.moveTo(x, y, duration=0.5)

    @staticmethod
    def click(x=None, y=None):
        pyautogui.click(x, y)

    @staticmethod
    def double_click(x=None, y=None):
        pyautogui.doubleClick(x, y)