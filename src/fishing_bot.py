
from .game.game_controller import GameController
from .game.screenshot_analyzer import ScreenshotAnalyzer
from .game.game_state import GameState
from time import sleep
from timeit import default_timer as timer


class FishingBot:
    def __init__(self) -> None:
        self.gc = GameController()
        self.sa = ScreenshotAnalyzer()
        self.state = None

    def IdentifyState(self):
        state = self.sa.GetGameState()

    def start(self):

        sleep(5)
        self.sa.capture_start_direction()
        self.gc.Reset()

        while(True):
            sessionStart = timer()
            if (timer() - sessionStart > 3600):
                self.gc.RepairFishingRod()
                sessionStart = timer()

            while(self.sa.Is_Facing_Saved_Direction() == False):
                self.gc.SeekRightDirection()

            if (self.sa.IsReadyToCastState()):
                self.gc.CastFishingRod()
                self.state = GameState.FISHING

            elif (self.state == GameState.FISHING):
                if (self.sa.IsFishOnHook()):
                    self.gc.CatchFish()
                    self.state = GameState.REELING_FISH

            elif (self.state == GameState.REELING_FISH):
                if (self.sa.IsSafeToPull()):
                    self.gc.PullFish()
                else:
                    self.gc.StopPulling()
            sleep(0.1)
