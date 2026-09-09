"""Geometry Dash tarzı oyun modları ve portal renkleri."""

from __future__ import annotations

from enum import Enum, auto


class GameMode(Enum):
    CUBE = auto()
    SHIP = auto()
    BALL = auto()
    SPIDER = auto()
    ROBOT = auto()
    WAVE = auto()


MODE_ORDER: list[GameMode] = [
    GameMode.CUBE,
    GameMode.SHIP,
    GameMode.BALL,
    GameMode.SPIDER,
    GameMode.ROBOT,
    GameMode.WAVE,
]

# Portal çerçeve rengi (mod ayırt — GD benzeri)
PORTAL_COLORS: dict[GameMode, tuple[int, int, int]] = {
    GameMode.CUBE: (120, 200, 255),
    GameMode.SHIP: (255, 140, 90),
    GameMode.BALL: (180, 100, 255),
    GameMode.SPIDER: (80, 255, 160),
    GameMode.ROBOT: (255, 220, 80),
    GameMode.WAVE: (100, 240, 255),
}


def mode_label(m: GameMode) -> str:
    return {
        GameMode.CUBE: "Cube",
        GameMode.SHIP: "Ship",
        GameMode.BALL: "Ball",
        GameMode.SPIDER: "Spider",
        GameMode.ROBOT: "Robot",
        GameMode.WAVE: "Wave",
    }[m]


def mode_from_name(name: str) -> GameMode:
    n = name.lower().strip()
    for m in GameMode:
        if m.name.lower() == n:
            return m
    return GameMode.CUBE
