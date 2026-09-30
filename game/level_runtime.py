"""Seviye verisini Ã§arpÄ±ÅŸma listelerine dÃ¶nÃ¼ÅŸtÃ¼rÃ¼r."""

from __future__ import annotations

from typing import Any

import pygame

from game.level_definitions import LEVELS
from game.modes import GameMode, mode_from_name


def parse_level(level_index: int) -> dict[str, Any]:
    data = LEVELS[level_index]
    blocks: list[pygame.Rect] = []
    spikes: list[tuple[pygame.Rect, tuple, tuple, tuple]] = []
    portals: list[tuple[pygame.Rect, GameMode]] = []
    speed_gates: list[tuple[pygame.Rect, float]] = []

    for o in data["objects"]:
        t = o["type"]
        r = pygame.Rect(int(o["x"]), int(o["y"]), int(o["w"]), int(o["h"]))
        if t == "block":
            blocks.append(r)
        elif t == "spike":
            left, top, w, h = r.left, r.top, r.w, r.h
            cx = left + w // 2
            tip_y = top + max(6, int(h * 0.22))
            a = (float(left + w * 0.12), float(top + h))
            b = (float(cx), float(tip_y))
            c = (float(left + w * 0.88), float(top + h))
            spikes.append((r, a, b, c))
        elif t == "portal":
            portals.append((r, mode_from_name(str(o["mode"]))))
        elif t == "speed_gate":
            speed_gates.append((r, float(o["speed"])))

    return {
        "data": data,
        "blocks": blocks,
        "spikes": spikes,
        "portals": portals,
        "speed_gates": speed_gates,
    }
