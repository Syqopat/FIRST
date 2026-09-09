"""Skin + mod ikonları — Hub'dan ayrı tam ekran menü."""

from __future__ import annotations

import pygame

from config import SCREEN_H, SCREEN_W, UI_ACCENT, UI_BUTTON, UI_BUTTON_HOVER, UI_TEXT
from game.modes import GameMode, mode_label
from game_icons import GAME_ICONS, draw_game_icon, icons_for_mode
from savegame import save_to_disk
from scenes.base import Scene
from skins import SKINS
from widgets import Button, draw_gradient_bg


class IconMenuScene(Scene):
    def on_enter(self, **kwargs) -> None:
        self.btn_back = Button(pygame.Rect(36, 36, 200, 46), "Hub'a dön", self.app.font_ui)
        self.icon_mode = GameMode.CUBE
        self.skin_rects: list[tuple[pygame.Rect, int]] = []
        self.mode_pills: list[tuple[pygame.Rect, GameMode]] = []
        self.icon_pick_rects: list[tuple[pygame.Rect, int]] = []

    def _layout_mode_pills(self) -> None:
        modes = list(GameMode)
        pill_w = 108
        gap = 8
        total = len(modes) * pill_w + (len(modes) - 1) * gap
        x0 = max(24, (SCREEN_W - total) // 2)
        y = 308
        self.mode_pills = []
        for i, m in enumerate(modes):
            r = pygame.Rect(x0 + i * (pill_w + gap), y, pill_w, 36)
            self.mode_pills.append((r, m))

    def handle(self, events: list[pygame.event.Event]) -> None:
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self.btn_back.contains(e.pos):
                    self.app.goto_hub()
                for rect, sid in self.skin_rects:
                    if rect.collidepoint(e.pos) and sid in self.app.save.owned_skins:
                        self.app.save.selected_skin = sid
                        save_to_disk(self.app.save)
                for rect, m in self.mode_pills:
                    if rect.collidepoint(e.pos):
                        self.icon_mode = m
                for rect, iid in self.icon_pick_rects:
                    if not rect.collidepoint(e.pos):
                        continue
                    if iid not in self.app.save.owned_game_icon_ids:
                        continue
                    ic = next((x for x in GAME_ICONS if int(x["id"]) == int(iid)), None)
                    if ic is None or ic["mode"] != self.icon_mode:
                        continue
                    self.app.save.selected_game_icons[self.icon_mode.name] = int(iid)
                    save_to_disk(self.app.save)

    def update(self, dt: float) -> None:
        self.btn_back.update_hover(pygame.mouse.get_pos())

    def draw(self, surf: pygame.Surface) -> None:
        draw_gradient_bg(surf, (24, 28, 58), (12, 14, 30))
        self.btn_back.draw(surf, (UI_BUTTON, UI_BUTTON_HOVER, UI_TEXT))

        t = self.app.font_title.render("Görünüm", True, UI_ACCENT)
        surf.blit(t, t.get_rect(center=(SCREEN_W // 2, 78)))

        lab = self.app.font_ui.render("Menü renkleri (skin)", True, UI_TEXT)
        surf.blit(lab, (SCREEN_W // 2 - lab.get_width() // 2, 118))

        self.skin_rects = []
        strip_y = 148
        cell = 52
        gap = 10
        n = len(SKINS)
        total_w = n * cell + (n - 1) * gap
        x0 = max(32, (SCREEN_W - total_w) // 2)
        for i, s in enumerate(SKINS):
            sid = s["id"]
            owned = sid in self.app.save.owned_skins
            sel = sid == self.app.save.selected_skin
            x = x0 + i * (cell + gap)
            r = pygame.Rect(x, strip_y, cell, cell)
            self.skin_rects.append((r, sid))
            col = s["primary"] if owned else (48, 50, 60)
            pygame.draw.rect(surf, col, r, border_radius=8)
            pygame.draw.rect(
                surf,
                (255, 230, 120) if sel else (85, 90, 110),
                r,
                width=3 if sel else 1,
                border_radius=8,
            )
            if not owned:
                lx = self.app.font_small.render("X", True, (200, 80, 90))
                surf.blit(lx, lx.get_rect(center=r.center))

        lab2 = self.app.font_ui.render("Oyun modu ikonları", True, UI_TEXT)
        surf.blit(lab2, (SCREEN_W // 2 - lab2.get_width() // 2, 268))

        self._layout_mode_pills()
        for rect, m in self.mode_pills:
            on = m == self.icon_mode
            bg = (70, 90, 140) if on else (48, 52, 72)
            pygame.draw.rect(surf, bg, rect, border_radius=8)
            pygame.draw.rect(surf, UI_ACCENT if on else (90, 95, 120), rect, width=2, border_radius=8)
            txt = self.app.font_small.render(mode_label(m)[:7], True, UI_TEXT)
            surf.blit(txt, txt.get_rect(center=rect.center))

        self.icon_pick_rects = []
        row_y = 358
        icell = 48
        igap = 10
        icons = icons_for_mode(self.icon_mode)
        iw = len(icons) * icell + max(0, len(icons) - 1) * igap
        ix0 = max(32, (SCREEN_W - iw) // 2)
        for j, ic in enumerate(icons):
            iid = int(ic["id"])
            r = pygame.Rect(ix0 + j * (icell + igap), row_y, icell, icell)
            self.icon_pick_rects.append((r, iid))
            owned = iid in self.app.save.owned_game_icon_ids
            sel = int(self.app.save.selected_game_icons.get(self.icon_mode.name, 0)) == iid
            pygame.draw.rect(surf, (32, 34, 48), r, border_radius=6)
            if owned:
                draw_game_icon(surf, r.inflate(-6, -6), ic, self.icon_mode)
            else:
                pygame.draw.line(surf, (120, 70, 80), r.topleft, r.bottomright, 2)
                pygame.draw.line(surf, (120, 70, 80), r.topright, r.bottomleft, 2)
            pygame.draw.rect(
                surf,
                (255, 220, 100) if sel else (70, 75, 95),
                r,
                width=2 if sel else 1,
                border_radius=6,
            )

        hint = self.app.font_small.render(
            "Kilitli ikonlar mağazada. Mod seç → ikon seç.",
            True,
            (150, 160, 185),
        )
        surf.blit(hint, hint.get_rect(center=(SCREEN_W // 2, SCREEN_H - 24)))
