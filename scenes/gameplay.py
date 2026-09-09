"""Kaydırmalı bölüm — diken (üçgen hitbox), hız kapıları, ikon dönüşü."""

from __future__ import annotations

import random

import pygame

from config import (
    BLOCK,
    PLAYER_SCREEN_X,
    PLAYER_SIZE,
    PORTAL_GLOW,
    SCREEN_H,
    SCREEN_W,
    SPEED_GATE,
    SPIKE,
    UI_ACCENT,
    UI_TEXT,
)
from game.level_runtime import parse_level
from game.modes import PORTAL_COLORS, mode_label
from game.player import Player
from game_icons import draw_game_icon, draw_game_icon_rotated, icon_by_id
from savegame import reward_for_level, save_to_disk
from scenes.base import Scene
from widgets import Button, draw_gradient_bg


class GameplayScene(Scene):
    def on_enter(self, level_index: int = 0, attempt: int = 1, **kwargs) -> None:
        self.level_index = int(level_index)
        self.attempt = max(1, int(attempt))
        self.parsed = parse_level(self.level_index)
        self.data = self.parsed["data"]
        self.blocks = self.parsed["blocks"]
        self.spikes = self.parsed["spikes"]
        self.portals = self.parsed["portals"]
        self.speed_gates = self.parsed["speed_gates"]
        self.spike_tris = [(s[1], s[2], s[3]) for s in self.spikes]
        self.scroll = 0.0
        self.run_speed = float(self.data["scroll_speed"])
        self.speed_gate_cd = 0.0
        self.player = Player()
        self.player.reset()
        self.hold = False
        self.tap = False
        self.dead = False
        self.won = False
        self.pause = False
        self._death_fx: list[dict] = []
        self._icon_angle = 0.0
        f = self.app.font_ui
        self.btn_retry = Button(pygame.Rect(SCREEN_W // 2 - 220, SCREEN_H // 2 + 100, 200, 48), "Tekrar", f)
        self.btn_menu = Button(pygame.Rect(SCREEN_W // 2 + 20, SCREEN_H // 2 + 100, 200, 48), "Menü", f)

    def handle(self, events: list[pygame.event.Event]) -> None:
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if self.dead or self.won:
                        self.app.goto_level_menu(self.level_index)
                    else:
                        self.pause = not self.pause
                if not self.pause and not self.dead and not self.won:
                    if e.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                        self._register_tap()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    if self.dead or self.won:
                        if self.btn_menu.contains(e.pos):
                            self.app.goto_level_menu(self.level_index)
                        if self.btn_retry.contains(e.pos):
                            self.on_enter(level_index=self.level_index, attempt=self.attempt + 1)
                    elif not self.pause:
                        self._register_tap()
        self._poll_input()

    def _register_tap(self) -> None:
        self.tap = True

    def _poll_input(self) -> None:
        keys = pygame.key.get_pressed()
        self.hold = bool(
            keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]
        ) or pygame.mouse.get_pressed()[0]

    def _spawn_death_fx(self) -> None:
        if not self.app.save.particles:
            return
        cx = PLAYER_SCREEN_X + PLAYER_SIZE // 2
        cy = int(self.player.y) + PLAYER_SIZE // 2
        skin = icon_by_id(int(self.app.save.selected_game_icons[self.player.mode.name]))
        col = skin["p"]
        for _ in range(14):
            self._death_fx.append(
                {
                    "x": float(cx),
                    "y": float(cy),
                    "vx": random.uniform(-220, 220),
                    "vy": random.uniform(-320, -80),
                    "life": random.uniform(0.35, 0.65),
                    "c": col,
                }
            )

    def update(self, dt: float) -> None:
        self._poll_input()
        if self.dead:
            for p in self._death_fx:
                p["life"] -= dt
                p["x"] += p["vx"] * dt
                p["y"] += p["vy"] * dt
                p["vy"] += 700 * dt
            self._death_fx = [p for p in self._death_fx if p["life"] > 0]

        if self.dead or self.won:
            mp = pygame.mouse.get_pos()
            self.btn_menu.update_hover(mp)
            self.btn_retry.update_hover(mp)
            return

        if self.pause:
            self.tap = False
            return

        self.speed_gate_cd = max(0.0, self.speed_gate_cd - dt)
        if self.speed_gate_cd <= 0.0:
            pr_gate = self.player.rect_world(self.scroll)
            for zone, spd in self.speed_gates:
                if pr_gate.colliderect(zone):
                    self.run_speed = float(spd)
                    self.speed_gate_cd = 0.3
                    break

        self.scroll += self.run_speed * dt

        alive, _mode_change = self.player.update(
            dt,
            self.scroll,
            self.hold,
            self.tap,
            self.blocks,
            self.spike_tris,
            self.portals,
        )
        self.tap = False

        if self.player.grounded and abs(self.player.vy) < 100.0:
            self._icon_angle *= 0.72
            if abs(self._icon_angle) < 1.5:
                self._icon_angle = 0.0
        else:
            self._icon_angle = (self._icon_angle + dt * 480.0) % 360.0

        if not alive:
            self.dead = True
            self._spawn_death_fx()
            return

        if self.scroll >= float(self.data["length"]):
            self._win()

    def _win(self) -> None:
        if self.won:
            return
        self.won = True
        s = self.app.save
        diff = int(self.data["difficulty"])
        first = not s.completed[self.level_index]
        gain = reward_for_level(diff, first)
        s.coins += gain
        s.completed[self.level_index] = True
        save_to_disk(s)
        self._last_reward = gain

    def _player_icon(self) -> dict:
        key = self.player.mode.name
        iid = int(self.app.save.selected_game_icons.get(key, 0))
        return icon_by_id(iid)

    def draw(self, surf: pygame.Surface) -> None:
        draw_gradient_bg(surf, (18, 20, 40), (8, 10, 22))
        sc = int(self.scroll)

        for b in self.blocks:
            r = pygame.Rect(b.x - sc, b.y, b.w, b.h)
            if r.colliderect((0, 0, SCREEN_W, SCREEN_H)):
                pygame.draw.rect(surf, BLOCK, r, border_radius=2)

        for _bounds, a, b, c in self.spikes:
            pa = (int(a[0] - sc), int(a[1]))
            pb = (int(b[0] - sc), int(b[1]))
            pc = (int(c[0] - sc), int(c[1]))
            minx = min(pa[0], pb[0], pc[0])
            maxx = max(pa[0], pb[0], pc[0])
            miny = min(pa[1], pb[1], pc[1])
            maxy = max(pa[1], pb[1], pc[1])
            if maxx < -50 or minx > SCREEN_W + 50 or maxy < -50 or miny > SCREEN_H + 50:
                continue
            pygame.draw.polygon(surf, SPIKE, [pa, pb, pc])

        for zone, _spd in self.speed_gates:
            r = pygame.Rect(zone.x - sc, zone.y, zone.w, zone.h)
            if r.colliderect((0, 0, SCREEN_W, SCREEN_H)):
                pygame.draw.rect(surf, SPEED_GATE, r, width=3, border_radius=8)
                inner = r.inflate(-10, -10)
                pygame.draw.rect(
                    surf,
                    (SPEED_GATE[0] // 3, SPEED_GATE[1] // 3, SPEED_GATE[2] // 3),
                    inner,
                    border_radius=6,
                )

        for zone, mode in self.portals:
            r = pygame.Rect(zone.x - sc, zone.y, zone.w, zone.h)
            if r.colliderect((0, 0, SCREEN_W, SCREEN_H)):
                c = PORTAL_COLORS.get(mode, PORTAL_GLOW)
                pygame.draw.rect(surf, c, r, width=3, border_radius=6)
                inner = r.inflate(-8, -8)
                fill = (c[0] // 4, c[1] // 4, c[2] // 4)
                pygame.draw.rect(surf, fill, inner, border_radius=4)

        icon = self._player_icon()
        screen_rect = pygame.Rect(
            PLAYER_SCREEN_X,
            int(self.player.y),
            PLAYER_SIZE,
            PLAYER_SIZE,
        )
        air_spin = (not self.player.grounded) or abs(self.player.vy) > 55
        ang = self._icon_angle
        if air_spin:
            draw_game_icon_rotated(surf, screen_rect, icon, self.player.mode, ang)
        elif abs(ang) < 0.5:
            draw_game_icon(surf, screen_rect, icon, self.player.mode)
        else:
            draw_game_icon_rotated(surf, screen_rect, icon, self.player.mode, ang)

        mode_txt = self.app.font_ui.render(f"Mod: {mode_label(self.player.mode)}", True, UI_ACCENT)
        surf.blit(mode_txt, (24, 20))
        att = self.app.font_small.render(f"Deneme: {self.attempt}", True, (200, 210, 230))
        surf.blit(att, (24, 46))
        spd_txt = self.app.font_small.render(f"Hız: {int(self.run_speed)}", True, (160, 200, 255))
        surf.blit(spd_txt, (24, 68))

        prog = min(1.0, self.scroll / max(float(self.data["length"]), 1.0))
        bar = pygame.Rect(24, 92, int((SCREEN_W - 48) * prog), 8)
        pygame.draw.rect(surf, (50, 55, 75), pygame.Rect(24, 92, SCREEN_W - 48, 8), border_radius=4)
        pygame.draw.rect(surf, UI_ACCENT, bar, border_radius=4)

        for p in self._death_fx:
            a = max(0, min(220, int(220 * (p["life"] / 0.65))))
            s = pygame.Surface((8, 8), pygame.SRCALPHA)
            s.fill((*p["c"][:3], a))
            surf.blit(s, (int(p["x"]) - 4, int(p["y"]) - 4))

        if self.pause:
            self._draw_overlay(surf, "Duraklatıldı", "ESC: devam", show_buttons=False)

        if self.dead:
            self._draw_overlay(
                surf,
                "Diken!",
                f"Deneme {self.attempt} — Tekrar veya Menü",
                show_buttons=True,
            )

        if self.won:
            msg = f"Bölüm bitti! +{getattr(self, '_last_reward', 0)} para"
            self._draw_overlay(surf, "Tamamdır", msg, show_buttons=True)

    def _draw_overlay(self, surf: pygame.Surface, title: str, sub: str, show_buttons: bool) -> None:
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 170))
        surf.blit(ov, (0, 0))
        t = self.app.font_title.render(title, True, UI_ACCENT)
        surf.blit(t, t.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 52)))
        s = self.app.font_ui.render(sub, True, UI_TEXT)
        surf.blit(s, s.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 6)))
        if show_buttons:
            self.btn_retry.draw(surf, ((55, 60, 90), (75, 85, 120), UI_TEXT))
            self.btn_menu.draw(surf, ((55, 60, 90), (75, 85, 120), UI_TEXT))
