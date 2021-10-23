import numpy as np
import cv2
import math
from timeit import default_timer as timer
from PIL import ImageGrab


class ScreenshotAnalyzer:
    def __init__(self) -> None:
        pass

    def capture_start_direction(self):
        img = np.array(ImageGrab.grab(bbox=(950, 20, 963, 38)))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        self.start_direction = img
        return img

    def capture_compas(self):
        img = np.array(ImageGrab.grab(bbox=(875, 0, 1035, 40)))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        return img

    def Is_Facing_Saved_Direction(self):
        img = self.capture_compas()
        return self.is_template_present(img, self.start_direction, .6)

    def capture_screen(self):
        img = np.array(ImageGrab.grab(bbox=(0, 0, 1920, 1080)))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = img[0:800, 500: 1250]
        return img

    def MemorizeStartDirection(self):
        pass

    def capture_cast_box(self):
        img = np.array(ImageGrab.grab(bbox=(1040, 740, 1240, 790)))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img

    def get_euclidian_distance(self, c1, c2):
        return math.sqrt((c2[0] - c1[0]) ** 2 + (c2[1] - c1[1])
                         ** 2 + (c2[2] - c1[2]) ** 2)

    def GetReelIndicator(self):
        image = self.capture_screen()

        template = cv2.imread(
            './images/reel-marker.png', cv2.IMREAD_UNCHANGED)

        output = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        result = np.where(output >= .9)

        if (len(result[0]) > 0):
            for pt in zip(*result[::-1]):
                return image[pt[1]-35:pt[1]+2, pt[0]-10:pt[0]+25]
        return None

    def IsSafeToPull(self):
        image = self.GetReelIndicator()

        if (image is None):
            return False

        goodGreen = [177, 235, 47]
        minDistance = 1000

        for h in range(len(image)):
            for v in range(len(image[h])):
                px = image[h][v]
                distance = self.get_euclidian_distance(goodGreen, px)

                if minDistance > distance:
                    minDistance = distance

                if (distance < 75):
                    return True
        return False

    def is_template_present(self, image, template, threshold=0.9):
        res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        threshold = .9
        loc = np.where(res >= threshold)
        return len(loc[0]) > 0

    def IsReadyToCastState(self):
        image = self.capture_cast_box()
        template = cv2.imread(
            './images/change_bait_button.png', cv2.IMREAD_UNCHANGED)
        return self.is_template_present(image, template)

    def FindFishIndicator(self, sc=None):
        if (sc is None):
            sc = self.capture_screen()

        template = cv2.imread(
            './images/is-fishing-icon.png', cv2.IMREAD_UNCHANGED)

        output = cv2.matchTemplate(sc, template, cv2.TM_CCOEFF_NORMED)
        result = np.where(output >= .9)

        if (len(result[0]) > 0):
            return True
        return False

    def IsFishOnHook(self, image=None):
        if (image is None):
            image = self.capture_screen()

        template = cv2.imread(
            './images/fish-on-hook.png', cv2.IMREAD_UNCHANGED)
        return self.is_template_present(image, template)
