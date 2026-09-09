"""Skinler ve mod ikonları — sekmeli mağaza."""

from __future__ import annotations

import pygame

from config import SCREEN_W, UI_ACCENT, UI_BUTTON, UI_BUTTON_HOVER, UI_TEXT
from game_icons import GAME_ICONS, draw_game_icon
from savegame import save_to_disk
from scenes.base import Scene
from skins import SKINS
from widgets import Button, draw_gradient_bg


class ShopScene(Scene):
    def on_enter(self, **kwargs) -> None:
        self.btn_back = Button(pygame.Rect(36, 36, 160, 46), "Hub", self.app.font_ui)
        cx = SCREEN_W // 2
        self.btn_tab_skins = Button(pygame.Rect(cx - 210, 118, 200, 42), "Skinler", self.app.font_ui)
        self.btn_tab_icons = Button(pygame.Rect(cx + 10, 118, 200, 42), "Mod ikonları", self.app.font_ui)
        self.tab: str = "skins"
        self._rebuild()

    def _rebuild(self) -> None:
        self.buy_rows: list[tuple[Button, int, str, int]] = []
        y = 188
        row_h = 52
        if self.tab == "skins":
            for s in SKINS:
                sid = int(s["id"])
                if sid in self.app.save.owned_skins:
                    y += row_h
                    continue
                price = int(s["price"])
                b = Button(
                    pygame.Rect(SCREEN_W - 260, y, 220, 40),
                    f"Satın al ({price})",
                    self.app.font_ui,
                    data=("skin", sid),
                )
                self.buy_rows.append((b, price, "skin", sid))
                y += row_h
        else:
            for ic in GAME_ICONS:
                iid = int(ic["id"])
                if iid in self.app.save.owned_game_icon_ids:
                    y += row_h
                    continue
                price = int(ic["price"])
                b = Button(
                    pygame.Rect(SCREEN_W - 260, y, 220, 40),
                    f"Satın al ({price})",
                    self.app.font_ui,
                    data=("gicon", iid),
                )
                self.buy_rows.append((b, price, "gicon", iid))
                y += row_h

    def handle(self, events: list[pygame.event.Event]) -> None:
        for e in events:
            if e.type != pygame.MOUSEBUTTONDOWN or e.button != 1:
                continue
            if self.btn_back.contains(e.pos):
                self.app.goto_hub()
                return
            if self.btn_tab_skins.contains(e.pos):
                self.tab = "skins"
                self._rebuild()
                return
            if self.btn_tab_icons.contains(e.pos):
                self.tab = "icons"
                self._rebuild()
                return
            for b, price, kind, iid in self.buy_rows:
                if not b.contains(e.pos):
                    continue
                if self.app.save.coins < price:
                    return
                if kind == "skin":
                    if iid in self.app.save.owned_skins:
                        return
                    self.app.save.coins -= price
                    self.app.save.owned_skins.append(int(iid))
                    self.app.save.owned_skins.sort()
                else:
                    if iid in self.app.save.owned_game_icon_ids:
                        return
                    self.app.save.coins -= price
                    self.app.save.owned_game_icon_ids.append(int(iid))
                    self.app.save.owned_game_icon_ids.sort()
                save_to_disk(self.app.save)
                self._rebuild()
                return

    def update(self, dt: float) -> None:
        mp = pygame.mouse.get_pos()
        self.btn_back.update_hover(mp)
        self.btn_tab_skins.update_hover(mp)
        self.btn_tab_icons.update_hover(mp)
        for b, price, _k, _i in self.buy_rows:
            b._hover = False
            if self.app.save.coins >= price:
                b.update_hover(mp)

    def draw(self, surf: pygame.Surface) -> None:
        draw_gradient_bg(surf, (24, 20, 44), (10, 10, 24))
        self.btn_back.draw(surf, (UI_BUTTON, UI_BUTTON_HOVER, UI_TEXT))
        t = self.app.font_title.render("Mağaza", True, UI_ACCENT)
        surf.blit(t, (SCREEN_W // 2 - t.get_width() // 2, 72))
        c = self.app.font_ui.render(f"Paran: {self.app.save.coins}", True, UI_TEXT)
        surf.blit(c, (SCREEN_W // 2 - c.get_width() // 2, 122))

        cols = (UI_BUTTON, UI_BUTTON_HOVER, UI_TEXT)
        self.btn_tab_skins.draw(
            surf,
            (
                (75, 95, 140) if self.tab == "skins" else UI_BUTTON,
                UI_BUTTON_HOVER,
                UI_TEXT,
            ),
        )
        self.btn_tab_icons.draw(
            surf,
            (
                (75, 95, 140) if self.tab == "icons" else UI_BUTTON,
                UI_BUTTON_HOVER,
                UI_TEXT,
            ),
        )

        y = 188
        row_h = 52
        if self.tab == "skins":
            sub = self.app.font_large.render("Menü renk paketleri", True, UI_ACCENT)
            surf.blit(sub, (60, 158))
            for s in SKINS:
                sid = int(s["id"])
                owned = sid in self.app.save.owned_skins
                preview = pygame.Rect(60, y, 42, 42)
                pygame.draw.rect(surf, s["primary"], preview, border_radius=6)
                pygame.draw.rect(surf, s["accent"], preview.inflate(-8, -8), border_radius=3)
                name = self.app.font_ui.render(s["name"], True, UI_TEXT)
                surf.blit(name, (118, y + 4))
                st = self.app.font_small.render(
                    "Sahip" if owned else f"{s['price']} para",
                    True,
                    (140, 255, 160) if owned else (200, 200, 220),
                )
                surf.blit(st, (118, y + 26))
                y += row_h
        else:
            sub = self.app.font_large.render("Oyun içi mod ikonları", True, UI_ACCENT)
            surf.blit(sub, (60, 158))
            for ic in GAME_ICONS:
                iid = int(ic["id"])
                owned = iid in self.app.save.owned_game_icon_ids
                preview = pygame.Rect(60, y, 42, 42)
                pygame.draw.rect(surf, (36, 38, 52), preview, border_radius=6)
                if owned:
                    draw_game_icon(surf, preview.inflate(-6, -6), ic, ic["mode"])
                nm = f"{ic['name']}  ({ic['mode'].name})"
                name = self.app.font_ui.render(nm, True, UI_TEXT)
                surf.blit(name, (118, y + 4))
                st = self.app.font_small.render(
                    "Sahip" if owned else f"{ic['price']} para",
                    True,
                    (140, 255, 160) if owned else (200, 200, 220),
                )
                surf.blit(st, (118, y + 26))
                y += row_h

        for b, price, _k, _i in self.buy_rows:
            if self.app.save.coins < price:
                b._hover = False
            b.draw(surf, cols)
