from enum import Enum


class GameState(Enum):
    READY_TO_CAST = 1
    WAITING_FOR_FISHING_STATE = 2
    FISHING = 3
    FISH_ON_HOOK = 4,
    REELING_FISH = 5
