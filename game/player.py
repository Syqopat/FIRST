"""Moda gÃ¶re fizik â€” Cube, Ship, Ball, Spider, Robot, Wave."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from config import PLAYER_SCREEN_X, PLAYER_SIZE, SCREEN_H
from game.collision import triangle_hits_rect
from game.level_definitions import FLOOR_TOP
from game.modes import GameMode


CEILING_Y = 108
GRAVITY = 2500.0
JUMP_CUBE = -660.0
SHIP_GRAV = 820.0
SHIP_THRUST = 3600.0
ROBOT_JUMP_MIN = -440.0
ROBOT_JUMP_MAX = -820.0
ROBOT_CHARGE_TIME = 0.24
WAVE_VERT = 580.0


@dataclass
class Player:
    y: float = float(FLOOR_TOP - PLAYER_SIZE)
    vy: float = 0.0
    mode: GameMode = GameMode.CUBE
    gravity_dir: float = 1.0
    grounded: bool = False
    ceiling_stick: bool = False
    robot_holding: bool = False
    robot_charge: float = 0.0
    portal_cd: float = 0.0

    def rect_world(self, scroll: float) -> pygame.Rect:
        x = PLAYER_SCREEN_X + scroll
        return pygame.Rect(int(x), int(self.y), PLAYER_SIZE, PLAYER_SIZE)

    def reset(self) -> None:
        self.y = float(FLOOR_TOP - PLAYER_SIZE)
        self.vy = 0.0
        self.mode = GameMode.CUBE
        self.gravity_dir = 1.0
        self.grounded = True
        self.ceiling_stick = False
        self.robot_holding = False
        self.robot_charge = 0.0
        self.portal_cd = 0.0

    def _resolve_blocks(self, scroll: float, blocks: list[pygame.Rect], old_y: float) -> None:
        old_top = old_y
        old_bottom = old_y + PLAYER_SIZE
        for _ in range(8):
            pr = self.rect_world(scroll)
            moved = False
            for b in blocks:
                if not pr.colliderect(b):
                    continue
                overlap_bottom = pr.bottom - b.top
                overlap_top = b.bottom - pr.top
                overlap_left = b.right - pr.left
                overlap_right = pr.right - b.left
                m = min(overlap_bottom, overlap_top, overlap_left, overlap_right)

                if (
                    m == overlap_bottom
                    and old_bottom <= b.top + 12
                    and pr.bottom >= b.top - 2
                    and self.vy >= -120
                ):
                    self.y = float(b.top - PLAYER_SIZE)
                    self.vy = max(0.0, self.vy)
                    self.grounded = True
                    moved = True
                    break
                if (
                    m == overlap_top
                    and old_top >= b.bottom - 12
                    and pr.top <= b.bottom + 2
                    and self.vy <= 80
                ):
                    self.y = float(b.bottom)
                    self.vy = min(0.0, self.vy)
                    self.ceiling_stick = True
                    moved = True
                    break
                if m == overlap_bottom and self.vy >= 0 and overlap_bottom <= overlap_top + 4:
                    self.y = float(b.top - PLAYER_SIZE)
                    self.vy = 0.0
                    self.grounded = True
                    moved = True
                    break
                if m == overlap_top and self.vy <= 0 and overlap_top <= overlap_bottom + 4:
                    self.y = float(b.bottom)
                    self.vy = 0.0
                    self.ceiling_stick = True
                    moved = True
                    break
            if not moved:
                pr2 = self.rect_world(scroll)
                for b in blocks:
                    if not pr2.colliderect(b):
                        continue
                    od = [
                        (pr2.bottom - b.top, "up"),
                        (b.bottom - pr2.top, "down"),
                        (b.right - pr2.left, "left"),
                        (pr2.right - b.left, "right"),
                    ]
                    od.sort(key=lambda t: t[0])
                    kind = od[0][1]
                    if kind == "up" and self.vy >= -200:
                        self.y -= pr2.bottom - b.top
                        self.vy = max(0.0, self.vy)
                        self.grounded = True
                        moved = True
                        break
                    if kind == "down" and self.vy <= 200:
                        self.y += b.bottom - pr2.top
                        self.vy = min(0.0, self.vy)
                        moved = True
                        break
            if not moved:
                break
            old_top = self.y
            old_bottom = self.y + PLAYER_SIZE

    def update(
        self,
        dt: float,
        scroll: float,
        hold: bool,
        tap: bool,
        blocks: list[pygame.Rect],
        spikes: list[tuple[tuple, tuple, tuple]],
        portals: list[tuple[pygame.Rect, GameMode]],
    ) -> tuple[bool, GameMode | None]:
        self.portal_cd = max(0.0, self.portal_cd - dt)
        mode_changed: GameMode | None = None

        pr = self.rect_world(scroll)

        if self.portal_cd <= 0:
            for zone, target in portals:
                if pr.colliderect(zone):
                    if self.mode != target:
                        self.mode = target
                        self.vy = 0.0
                        if target == GameMode.BALL:
                            self.gravity_dir = 1.0
                        mode_changed = target
                    self.portal_cd = 0.38
                    break

        m = self.mode
        if m == GameMode.CUBE:
            self._cube(dt, tap)
        elif m == GameMode.SHIP:
            self._ship(dt, hold)
        elif m == GameMode.BALL:
            self._ball(dt, tap)
        elif m == GameMode.SPIDER:
            self._spider(dt, tap)
        elif m == GameMode.ROBOT:
            self._robot(dt, hold, tap)
        elif m == GameMode.WAVE:
            self._wave(dt, hold)

        old_y = self.y
        self.y += self.vy * dt

        self.grounded = False
        self.ceiling_stick = False
        self._resolve_blocks(scroll, blocks, old_y)

        pr = self.rect_world(scroll)

        for tri in spikes:
            a, b, c = tri
            if triangle_hits_rect(a, b, c, pr):
                return False, mode_changed

        if self.y > SCREEN_H + 120 or self.y < -160:
            return False, mode_changed

        return True, mode_changed

    def _cube(self, dt: float, tap: bool) -> None:
        self.vy += GRAVITY * dt
        if tap and self.grounded:
            self.vy = JUMP_CUBE

    def _ship(self, dt: float, hold: bool) -> None:
        self.vy += SHIP_THRUST * dt * (1.0 if hold else -0.42)
        self.vy += SHIP_GRAV * dt * (1.0 if self.vy > 0 else -0.25)
        self.vy = max(-560.0, min(560.0, self.vy))

    def _ball(self, dt: float, tap: bool) -> None:
        self.vy += GRAVITY * self.gravity_dir * dt
        if tap:
            self.gravity_dir *= -1.0

    def _spider(self, dt: float, tap: bool) -> None:
        self.vy += GRAVITY * dt
        if tap:
            floor_y = float(FLOOR_TOP - PLAYER_SIZE)
            if self.y > SCREEN_H * 0.48:
                self.y = float(CEILING_Y)
            else:
                self.y = floor_y
            self.vy = 0.0

    def _robot(self, dt: float, hold: bool, tap: bool) -> None:
        self.vy += GRAVITY * dt
        if hold:
            self.robot_holding = True
            self.robot_charge = min(ROBOT_CHARGE_TIME, self.robot_charge + dt)
        else:
            if self.robot_holding and self.grounded:
                t = min(1.0, self.robot_charge / ROBOT_CHARGE_TIME)
                self.vy = ROBOT_JUMP_MIN + (ROBOT_JUMP_MAX - ROBOT_JUMP_MIN) * t
            self.robot_holding = False
            self.robot_charge = 0.0

    def _wave(self, dt: float, hold: bool) -> None:
        target = -WAVE_VERT if hold else WAVE_VERT
        self.vy += (target - self.vy) * min(1.0, 15.0 * dt)
