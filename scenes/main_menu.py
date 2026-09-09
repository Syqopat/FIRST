from __future__ import annotations

import pygame

from config import SCREEN_H, SCREEN_W, UI_ACCENT, UI_BUTTON, UI_BUTTON_HOVER, UI_TEXT
from scenes.base import Scene
from widgets import Button, draw_gradient_bg


class MainMenuScene(Scene):
    def on_enter(self, **kwargs) -> None:
        f = self.app.font_large
        self.btn_start = Button(
            pygame.Rect(SCREEN_W // 2 - 160, SCREEN_H // 2 - 30, 320, 64),
            "Oyuna Gir",
            f,
        )
        self.btn_quit = Button(
            pygame.Rect(SCREEN_W // 2 - 120, SCREEN_H // 2 + 70, 240, 52),
            "Çıkış",
            self.app.font_ui,
        )

    def handle(self, events: list[pygame.event.Event]) -> None:
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self.btn_start.contains(e.pos):
                    self.app.goto_hub()
                elif self.btn_quit.contains(e.pos):
                    self.app.running = False

    def update(self, dt: float) -> None:
        self.btn_start.update_hover(pygame.mouse.get_pos())
        self.btn_quit.update_hover(pygame.mouse.get_pos())

    def draw(self, surf: pygame.Surface) -> None:
        draw_gradient_bg(surf, (28, 32, 72), (10, 12, 28))
        title = self.app.font_title.render("Geometry Run", True, UI_ACCENT)
        surf.blit(title, title.get_rect(center=(SCREEN_W // 2, 120)))
        sub = self.app.font_ui.render("Oyun doğrudan Hub ile açılır — buradan da girebilirsin.", True, UI_TEXT)
        surf.blit(sub, sub.get_rect(center=(SCREEN_W // 2, 175)))
        colors = (UI_BUTTON, UI_BUTTON_HOVER, UI_TEXT)
        self.btn_start.draw(surf, colors)
        self.btn_quit.draw(surf, colors)
