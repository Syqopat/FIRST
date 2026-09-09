"""10 bölüm — sol/sağ ok ve klavye; döngüsel gezinme."""

from __future__ import annotations

import pygame

from config import SCREEN_H, SCREEN_W, UI_ACCENT, UI_BUTTON, UI_BUTTON_HOVER, UI_TEXT
from game.level_definitions import LEVELS
from scenes.base import Scene
from widgets import Button, draw_gradient_bg


class LevelMenuScene(Scene):
    def on_enter(self, level_index: int = 0, **kwargs) -> None:
        self.index = max(0, min(9, int(level_index)))
        self._layout()
        self._hover_left = False
        self._hover_right = False

    def _layout(self) -> None:
        self.btn_back = Button(pygame.Rect(36, 36, 150, 46), "Hub'a dön", self.app.font_ui)
        self.btn_play_level = Button(
            pygame.Rect(SCREEN_W // 2 - 140, SCREEN_H - 160, 280, 62),
            "Bölümü Oyna",
            self.app.font_large,
        )
        aw, ah = 72, 128
        self.arrow_left = pygame.Rect(64, SCREEN_H // 2 - ah // 2, aw, ah)
        self.arrow_right = pygame.Rect(SCREEN_W - 64 - aw, SCREEN_H // 2 - ah // 2, aw, ah)

    def handle(self, events: list[pygame.event.Event]) -> None:
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    self.index = (self.index - 1) % 10
                elif e.key == pygame.K_RIGHT:
                    self.index = (self.index + 1) % 10
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self.btn_back.contains(e.pos):
                    self.app.goto_hub()
                elif self.btn_play_level.contains(e.pos):
                    self.app.goto_play(self.index, attempt=1)
                elif self.arrow_left.collidepoint(e.pos):
                    self.index = (self.index - 1) % 10
                elif self.arrow_right.collidepoint(e.pos):
                    self.index = (self.index + 1) % 10

    def update(self, dt: float) -> None:
        mp = pygame.mouse.get_pos()
        self.btn_back.update_hover(mp)
        self.btn_play_level.update_hover(mp)
        self._hover_left = self.arrow_left.collidepoint(mp)
        self._hover_right = self.arrow_right.collidepoint(mp)

    def draw(self, surf: pygame.Surface) -> None:
        draw_gradient_bg(surf, (22, 26, 52), (10, 12, 26))
        self.btn_back.draw(surf, (UI_BUTTON, UI_BUTTON_HOVER, UI_TEXT))

        lv = LEVELS[self.index]
        diff = lv["difficulty"]
        title = self.app.font_title.render(f"{self.index + 1}. {lv['name']}", True, UI_ACCENT)
        surf.blit(title, title.get_rect(center=(SCREEN_W // 2, 100)))

        stars = "★" * diff + "☆" * (10 - diff)
        st = self.app.font_large.render(stars, True, (255, 220, 120))
        surf.blit(st, st.get_rect(center=(SCREEN_W // 2, 158)))

        rew = self.app.save.completed[self.index]
        tip = (
            "Tamamlandı — tekrar oynayınca daha az para."
            if rew
            else "İlk kez bitirince ekstra ödül!"
        )
        t2 = self.app.font_ui.render(tip, True, UI_TEXT)
        surf.blit(t2, t2.get_rect(center=(SCREEN_W // 2, 200)))

        spd = self.app.font_ui.render(
            f"Hız: {lv['scroll_speed']}   Uzunluk: {lv['length']} px", True, UI_TEXT
        )
        surf.blit(spd, spd.get_rect(center=(SCREEN_W // 2, 236)))

        dot_r = 10
        gap = 18
        total = 10 * (dot_r * 2) + 9 * gap
        x0 = SCREEN_W // 2 - total // 2
        cy = 290
        for i in range(10):
            cx = x0 + i * (dot_r * 2 + gap) + dot_r
            col = (120, 255, 160) if self.app.save.completed[i] else (70, 75, 95)
            if i == self.index:
                pygame.draw.circle(surf, UI_ACCENT, (cx, cy), dot_r + 4, width=2)
            pygame.draw.circle(surf, col, (cx, cy), dot_r)

        def draw_arrow_box(r: pygame.Rect, hover: bool) -> None:
            pygame.draw.rect(
                surf,
                (55, 70, 110) if hover else (40, 46, 68),
                r,
                border_radius=10,
            )
            pygame.draw.rect(surf, UI_ACCENT, r, width=2, border_radius=10)

        draw_arrow_box(self.arrow_left, self._hover_left)
        draw_arrow_box(self.arrow_right, self._hover_right)

        # Sol ok (← uç sol tarafta)
        pygame.draw.polygon(
            surf,
            UI_ACCENT,
            [
                (self.arrow_left.left + 12, self.arrow_left.centery),
                (self.arrow_left.right - 10, self.arrow_left.top + 16),
                (self.arrow_left.right - 10, self.arrow_left.bottom - 16),
            ],
        )
        # Sağ ok
        pygame.draw.polygon(
            surf,
            UI_ACCENT,
            [
                (self.arrow_right.right - 12, self.arrow_right.centery),
                (self.arrow_right.left + 10, self.arrow_right.top + 16),
                (self.arrow_right.left + 10, self.arrow_right.bottom - 16),
            ],
        )

        hint = self.app.font_small.render(
            "Sol / Sağ ok veya ← → tuşları — 10. bölümde sağ: 1'e döner",
            True,
            (160, 170, 200),
        )
        surf.blit(hint, hint.get_rect(center=(SCREEN_W // 2, SCREEN_H - 220)))

        self.btn_play_level.draw(surf, (UI_BUTTON, UI_BUTTON_HOVER, UI_TEXT))
