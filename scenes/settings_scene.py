"""Görüntü, erişilebilirlik, ses ve tehlikeli sıfırlama."""

from __future__ import annotations

import pygame

from config import SCREEN_H, SCREEN_W, UI_ACCENT, UI_BUTTON, UI_BUTTON_HOVER, UI_TEXT
from game_icons import default_owned_icon_ids, default_selected_icons
from savegame import save_to_disk
from scenes.base import Scene
from widgets import Button, draw_gradient_bg


class SettingsScene(Scene):
    def on_enter(self, **kwargs) -> None:
        self.btn_back = Button(pygame.Rect(36, 36, 160, 46), "Hub", self.app.font_ui)
        cx = SCREEN_W // 2
        self.btn_m_down = Button(pygame.Rect(cx - 200, 168, 56, 40), "-", self.app.font_large)
        self.btn_m_up = Button(pygame.Rect(cx + 144, 168, 56, 40), "+", self.app.font_large)
        self.btn_s_down = Button(pygame.Rect(cx - 200, 248, 56, 40), "-", self.app.font_large)
        self.btn_s_up = Button(pygame.Rect(cx + 144, 248, 56, 40), "+", self.app.font_large)

        self.btn_fullscreen = Button(pygame.Rect(cx - 220, 318, 440, 44), "", self.app.font_ui)
        self.btn_motion = Button(pygame.Rect(cx - 220, 374, 440, 44), "", self.app.font_ui)
        self.btn_fps = Button(pygame.Rect(cx - 220, 430, 210, 44), "", self.app.font_ui)
        self.btn_particles = Button(pygame.Rect(cx + 10, 430, 210, 44), "", self.app.font_ui)

        self.btn_reset = Button(pygame.Rect(cx - 220, 520, 280, 46), "İlerlemeyi sıfırla", self.app.font_ui)
        self._reset_armed = False
        self._reset_timer = 0.0

    def _sync_labels(self) -> None:
        s = self.app.save
        self.btn_fullscreen.label = f"Tam ekran: {'Açık' if s.fullscreen else 'Kapalı'}"
        self.btn_motion.label = f"Hızlı geçiş (animasyonsuz): {'Açık' if s.reduce_motion else 'Kapalı'}"
        self.btn_fps.label = f"FPS göstergesi: {'Açık' if s.show_fps else 'Kapalı'}"
        self.btn_particles.label = f"Ölüm parçacıkları: {'Açık' if s.particles else 'Kapalı'}"

    def handle(self, events: list[pygame.event.Event]) -> None:
        s = self.app.save
        for e in events:
            if e.type != pygame.MOUSEBUTTONDOWN or e.button != 1:
                continue
            if self.btn_back.contains(e.pos):
                save_to_disk(s)
                self.app.goto_hub()
                return
            hit = False
            if self.btn_m_down.contains(e.pos):
                s.music_vol = max(0.0, round(s.music_vol - 0.1, 2))
                hit = True
            elif self.btn_m_up.contains(e.pos):
                s.music_vol = min(1.0, round(s.music_vol + 0.1, 2))
                hit = True
            elif self.btn_s_down.contains(e.pos):
                s.sfx_vol = max(0.0, round(s.sfx_vol - 0.1, 2))
                hit = True
            elif self.btn_s_up.contains(e.pos):
                s.sfx_vol = min(1.0, round(s.sfx_vol + 0.1, 2))
                hit = True
            elif self.btn_fullscreen.contains(e.pos):
                s.fullscreen = not s.fullscreen
                self.app._apply_display()
                hit = True
            elif self.btn_motion.contains(e.pos):
                s.reduce_motion = not s.reduce_motion
                hit = True
            elif self.btn_fps.contains(e.pos):
                s.show_fps = not s.show_fps
                hit = True
            elif self.btn_particles.contains(e.pos):
                s.particles = not s.particles
                hit = True
            elif self.btn_reset.contains(e.pos):
                if self._reset_armed and self._reset_timer > 0:
                    s.coins = 0
                    s.completed = [False] * 10
                    s.owned_skins = [0]
                    s.selected_skin = 0
                    s.owned_game_icon_ids = default_owned_icon_ids()
                    s.selected_game_icons = default_selected_icons()
                    self._reset_armed = False
                    self._reset_timer = 0.0
                else:
                    self._reset_armed = True
                    self._reset_timer = 2.4
                hit = True
            if hit:
                save_to_disk(s)
            self._sync_labels()

    def update(self, dt: float) -> None:
        if self._reset_armed:
            self._reset_timer -= dt
            if self._reset_timer <= 0:
                self._reset_armed = False
                self._reset_timer = 0.0
        mp = pygame.mouse.get_pos()
        for b in (
            self.btn_back,
            self.btn_m_down,
            self.btn_m_up,
            self.btn_s_down,
            self.btn_s_up,
            self.btn_fullscreen,
            self.btn_motion,
            self.btn_fps,
            self.btn_particles,
            self.btn_reset,
        ):
            b.update_hover(mp)
        self._sync_labels()

    def draw(self, surf: pygame.Surface) -> None:
        draw_gradient_bg(surf, (20, 24, 48), (10, 12, 26))
        self.btn_back.draw(surf, (UI_BUTTON, UI_BUTTON_HOVER, UI_TEXT))
        t = self.app.font_title.render("Ayarlar", True, UI_ACCENT)
        surf.blit(t, t.get_rect(center=(SCREEN_W // 2, 96)))

        s = self.app.save
        m = self.app.font_ui.render(f"Müzik: {int(s.music_vol * 100)}%", True, UI_TEXT)
        surf.blit(m, m.get_rect(center=(SCREEN_W // 2, 138)))
        self.btn_m_down.draw(surf, (UI_BUTTON, UI_BUTTON_HOVER, UI_TEXT))
        self.btn_m_up.draw(surf, (UI_BUTTON, UI_BUTTON_HOVER, UI_TEXT))

        sx = self.app.font_ui.render(f"SFX: {int(s.sfx_vol * 100)}%", True, UI_TEXT)
        surf.blit(sx, sx.get_rect(center=(SCREEN_W // 2, 218)))
        self.btn_s_down.draw(surf, (UI_BUTTON, UI_BUTTON_HOVER, UI_TEXT))
        self.btn_s_up.draw(surf, (UI_BUTTON, UI_BUTTON_HOVER, UI_TEXT))

        sec = self.app.font_small.render(
            "Görünüm ve performans — tam ekran anında uygulanır.", True, (150, 160, 185)
        )
        surf.blit(sec, sec.get_rect(center=(SCREEN_W // 2, 292)))

        cols = (UI_BUTTON, UI_BUTTON_HOVER, UI_TEXT)
        self.btn_fullscreen.draw(surf, cols)
        self.btn_motion.draw(surf, cols)
        self.btn_fps.draw(surf, cols)
        self.btn_particles.draw(surf, cols)

        tip = self.app.font_small.render(
            "Ses şimdilik menülerde kayıtlı; ileride müzik/SFX bağlanabilir.",
            True,
            (130, 140, 165),
        )
        surf.blit(tip, tip.get_rect(center=(SCREEN_W // 2, 492)))

        rs = (
            "Emin misin? Tekrar tıkla (süre dolmadan)"
            if self._reset_armed
            else "İlerlemeyi sıfırla: para, bölümler, skin ve ikonlar (ayarlar kalır)"
        )
        self.btn_reset.label = "İlerlemeyi sıfırla — ONAY" if self._reset_armed else "İlerlemeyi sıfırla"
        self.btn_reset.draw(surf, ((90, 50, 70), (120, 70, 90), UI_TEXT) if self._reset_armed else cols)
        rx = self.app.font_small.render(rs, True, (255, 180, 160) if self._reset_armed else (160, 170, 190))
        surf.blit(rx, rx.get_rect(center=(SCREEN_W // 2, SCREEN_H - 28)))
