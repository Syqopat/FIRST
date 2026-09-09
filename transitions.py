"""Sahne geçişi — kararma / açılma."""

from __future__ import annotations

from typing import Callable

import pygame


class ScreenFade:
    OUT_DUR = 0.26
    IN_DUR = 0.28

    def __init__(self) -> None:
        self.active = False
        self._out = True
        self._t = 0.0
        self._pending: Callable[[], None] | None = None

    def start(self, on_mid: Callable[[], None], *, instant: bool) -> None:
        if instant:
            on_mid()
            return
        self.active = True
        self._out = True
        self._t = 0.0
        self._pending = on_mid

    def update(self, dt: float) -> None:
        if not self.active:
            return
        dur = self.OUT_DUR if self._out else self.IN_DUR
        self._t += dt / dur
        if self._t < 1.0:
            return
        self._t = 0.0
        if self._out:
            self._out = False
            if self._pending:
                self._pending()
                self._pending = None
        else:
            self.active = False

    def draw(self, surf: pygame.Surface) -> None:
        if not self.active:
            return
        if self._out:
            a = min(1.0, self._t)
        else:
            a = max(0.0, 1.0 - self._t)
        alpha = int(235 * a)
        if alpha <= 0:
            return
        overlay = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        overlay.fill((10, 12, 26, alpha))
        surf.blit(overlay, (0, 0))
