import pyautogui
import pydirectinput
pyautogui.FAILSAFE = False


class GameController:
    def __init__(self) -> None:
        pass

    def CatchFish(self):
        pyautogui.mouseDown()
        pyautogui.sleep(0.1)
        pyautogui.mouseUp()

    def CastFishingRod(self):
        pyautogui.mouseDown()
        pyautogui.sleep(1.92)
        pyautogui.mouseUp()

    def PullFish(self):
        pyautogui.mouseDown()

    def StopPulling(self):
        pyautogui.mouseUp()

    def MoveViewToRight(self):
        pydirectinput.move(1, 1)
        pydirectinput.move(110, 200)

    def Reset(self):
        pydirectinput.move(1, 1)
        pydirectinput.move(-1, 100)

    def SeekRightDirection(self):
        pydirectinput.move(5, 100)

    def RepairFishingRod(self):
        pydirectinput.press('tab')
        pydirectinput.moveTo(870, 665)
        pyautogui.sleep(0.5)
        pydirectinput.keyDown('r')
        pyautogui.sleep(0.5)
        pydirectinput.click()
        pydirectinput.keyUp('r')
        pyautogui.sleep(0.25)
        pydirectinput.press('e')
        pyautogui.sleep(0.5)
        pydirectinput.press('tab')
        pyautogui.sleep(0.5)
        pydirectinput.press('f3')
        pyautogui.sleep(0.5)
