from __future__ import annotations

from typing import Any

import pygame


class Scene:
    def __init__(self, app: Any) -> None:
        self.app = app

    def on_enter(self, **kwargs: Any) -> None:
        pass

    def handle(self, events: list[pygame.event.Event]) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, surf: pygame.Surface) -> None:
        pass
