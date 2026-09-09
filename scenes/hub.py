"""Ana hub — oyun benzeri kayar arka plan; ikonlar ayrı menüde."""

from __future__ import annotations

import pygame

from config import BLOCK, SCREEN_H, SCREEN_W, UI_ACCENT, UI_BUTTON, UI_BUTTON_HOVER, UI_TEXT
from game.level_definitions import FLOOR_TOP
from scenes.base import Scene
from widgets import Button, draw_gradient_bg


class HubScene(Scene):
    def on_enter(self, **kwargs) -> None:
        w, h = 220, 54
        cx = SCREEN_W // 2
        y0 = 200
        gap = 20
        self.btn_play = Button(pygame.Rect(cx - w // 2, y0, w, h), "Bölümler", self.app.font_large)
        self.btn_look = Button(
            pygame.Rect(cx - w // 2, y0 + h + gap, w, h), "Görünüm (skin & ikon)", self.app.font_large
        )
        self.btn_settings = Button(
            pygame.Rect(cx - w // 2, y0 + (h + gap) * 2, w, h), "Ayarlar", self.app.font_large
        )
        self.btn_shop = Button(
            pygame.Rect(cx - w // 2, y0 + (h + gap) * 3, w, h), "Mağaza", self.app.font_large
        )
        self.btn_title = Button(pygame.Rect(36, 36, 180, 44), "Başlık ekranı", self.app.font_ui)
        self.bg_scroll = 0.0

    def handle(self, events: list[pygame.event.Event]) -> None:
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self.btn_title.contains(e.pos):
                    self.app.goto_main_menu()
                elif self.btn_play.contains(e.pos):
                    self.app.goto_level_menu(level_index=0)
                elif self.btn_look.contains(e.pos):
                    self.app.goto_icon_menu()
                elif self.btn_settings.contains(e.pos):
                    self.app.goto_settings()
                elif self.btn_shop.contains(e.pos):
                    self.app.goto_shop()

    def update(self, dt: float) -> None:
        self.bg_scroll = (self.bg_scroll + 95.0 * dt) % 2000.0
        mp = pygame.mouse.get_pos()
        for b in (
            self.btn_play,
            self.btn_look,
            self.btn_settings,
            self.btn_shop,
            self.btn_title,
        ):
            b.update_hover(mp)

    def draw(self, surf: pygame.Surface) -> None:
        draw_gradient_bg(surf, (18, 22, 48), (8, 10, 24))
        sc = int(self.bg_scroll)
        floor_y = FLOOR_TOP
        for i in range(-1, 18):
            x = i * 140 - (sc % 140)
            pygame.draw.rect(surf, BLOCK, (x, floor_y, 150, SCREEN_H - floor_y + 40), border_radius=3)
            if i % 3 == 0:
                pygame.draw.rect(surf, (55, 62, 90), (x + 30, floor_y - 36, 70, 22), border_radius=4)
        for i in range(12):
            sx = (i * 210 - sc) % (SCREEN_W + 210) - 80
            pygame.draw.circle(surf, (40, 48, 72), (int(sx), 90 + (i * 17) % 50), 3)

        self.btn_title.draw(surf, (UI_BUTTON, UI_BUTTON_HOVER, UI_TEXT))

        t = self.app.font_title.render("Ana Hub", True, UI_ACCENT)
        surf.blit(t, t.get_rect(center=(SCREEN_W // 2, 118)))

        colors = (UI_BUTTON, UI_BUTTON_HOVER, UI_TEXT)
        self.btn_play.draw(surf, colors)
        self.btn_look.draw(surf, colors)
        self.btn_settings.draw(surf, colors)
        self.btn_shop.draw(surf, colors)

        coin = self.app.font_ui.render(f"Para: {self.app.save.coins}", True, UI_ACCENT)
        surf.blit(coin, (SCREEN_W - coin.get_width() - 36, 40))

        tip = self.app.font_small.render(
            "Arka plan oyun gibi kayar — skin/ikon için «Görünüm» menüsüne gir.",
            True,
            (150, 165, 195),
        )
        surf.blit(tip, tip.get_rect(center=(SCREEN_W // 2, SCREEN_H - 28)))
