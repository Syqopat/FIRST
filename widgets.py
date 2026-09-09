"""Basit düğme ve tıklama yardımcıları."""

from __future__ import annotations

import pygame

class Button:
    def __init__(
        self,
        rect: pygame.Rect,
        label: str,
        font: pygame.font.Font,
        data: object | None = None,
    ) -> None:
        self.rect = rect
        self.label = label
        self.font = font
        self.data = data
        self._hover = False

    def contains(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)

    def draw(self, surf: pygame.Surface, colors: tuple[tuple, tuple, tuple]) -> None:
        bg, bg_h, fg = colors
        r = self.rect
        pygame.draw.rect(surf, bg_h if self._hover else bg, r, border_radius=10)
        pygame.draw.rect(surf, fg, r, width=2, border_radius=10)
        text = self.font.render(self.label, True, fg)
        surf.blit(text, text.get_rect(center=r.center))

    def update_hover(self, mouse: tuple[int, int]) -> None:
        self._hover = self.rect.collidepoint(mouse)


def draw_gradient_bg(surf: pygame.Surface, top: tuple, bottom: tuple) -> None:
    h = surf.get_height()
    w = surf.get_width()
    for y in range(h):
        t = y / max(h - 1, 1)
        c = (
            int(top[0] * (1 - t) + bottom[0] * t),
            int(top[1] * (1 - t) + bottom[1] * t),
            int(top[2] * (1 - t) + bottom[2] * t),
        )
        pygame.draw.line(surf, c, (0, y), (w, y))


def wrap_text(font: pygame.font.Font, text: str, max_w: int) -> list[pygame.Surface]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if font.size(test)[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return [font.render(line, True, (240, 245, 255)) for line in lines]
