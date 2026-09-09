"""Mod başına kozmetik ikonlar (10 adet) — mağaza + Hub seçimi."""

from __future__ import annotations

from typing import Any

import pygame

from game.modes import GameMode

GAME_ICONS: list[dict[str, Any]] = [
    {"id": 0, "mode": GameMode.CUBE, "name": "Kare", "price": 0, "p": (110, 190, 255), "a": (40, 60, 120), "kind": "cube"},
    {"id": 1, "mode": GameMode.CUBE, "name": "Kapsül", "price": 48, "p": (255, 200, 90), "a": (140, 80, 20), "kind": "capsule"},
    {"id": 2, "mode": GameMode.CUBE, "name": "Çekirdek", "price": 72, "p": (120, 255, 200), "a": (20, 100, 80), "kind": "core"},
    {"id": 3, "mode": GameMode.SHIP, "name": "Delta", "price": 0, "p": (255, 140, 90), "a": (120, 40, 20), "kind": "ship_a"},
    {"id": 4, "mode": GameMode.SHIP, "name": "Kanat", "price": 52, "p": (200, 160, 255), "a": (80, 40, 140), "kind": "ship_b"},
    {"id": 5, "mode": GameMode.BALL, "name": "Top", "price": 0, "p": (180, 100, 255), "a": (60, 20, 100), "kind": "ball"},
    {"id": 6, "mode": GameMode.BALL, "name": "Halka", "price": 58, "p": (100, 240, 255), "a": (20, 80, 120), "kind": "ring"},
    {"id": 7, "mode": GameMode.SPIDER, "name": "Tırnak", "price": 0, "p": (90, 255, 150), "a": (20, 90, 50), "kind": "spider"},
    {"id": 8, "mode": GameMode.ROBOT, "name": "Bot", "price": 0, "p": (255, 220, 80), "a": (120, 80, 20), "kind": "robot"},
    {"id": 9, "mode": GameMode.WAVE, "name": "Dalga", "price": 0, "p": (100, 230, 255), "a": (30, 90, 130), "kind": "wave"},
]


def icons_for_mode(mode: GameMode) -> list[dict[str, Any]]:
    return [x for x in GAME_ICONS if x["mode"] == mode]


def icon_by_id(iid: int) -> dict[str, Any]:
    for x in GAME_ICONS:
        if int(x["id"]) == int(iid):
            return x
    return GAME_ICONS[0]


def default_owned_icon_ids() -> list[int]:
    return sorted({int(x["id"]) for x in GAME_ICONS if int(x["price"]) == 0})


def default_selected_icons() -> dict[str, int]:
    out: dict[str, int] = {}
    for m in GameMode:
        ids = [int(x["id"]) for x in icons_for_mode(m)]
        out[m.name] = ids[0] if ids else 0
    return out


def draw_game_icon(
    surf: pygame.Surface,
    rect: pygame.Rect,
    icon: dict[str, Any],
    _mode: GameMode,
) -> None:
    p = icon["p"]
    a = icon["a"]
    k = str(icon.get("kind", "cube"))
    cx, cy = rect.center
    if k == "cube":
        pygame.draw.rect(surf, p, rect, border_radius=5)
        pygame.draw.rect(surf, a, rect.inflate(-8, -8), border_radius=3)
    elif k == "capsule":
        pygame.draw.ellipse(surf, p, rect)
        pygame.draw.ellipse(surf, a, rect.inflate(-10, -10))
    elif k == "core":
        pygame.draw.circle(surf, p, (cx, cy), rect.w // 2 - 2)
        pygame.draw.circle(surf, a, (cx, cy), rect.w // 2 - 8)
    elif k in ("ship_a", "ship_b"):
        pts = [
            (rect.right - 4, cy),
            (rect.left + 6, rect.top + 6),
            (rect.left + 14, cy),
            (rect.left + 6, rect.bottom - 6),
        ]
        if k == "ship_b":
            pts = [
                (rect.right - 2, cy),
                (rect.left + 4, rect.top + 4),
                (rect.left + 20, cy - 5),
                (rect.left + 12, cy),
                (rect.left + 20, cy + 5),
                (rect.left + 4, rect.bottom - 4),
            ]
        pygame.draw.polygon(surf, p, pts)
        pygame.draw.polygon(surf, a, pts, width=2)
    elif k == "ball":
        pygame.draw.circle(surf, p, (cx, cy), rect.w // 2 - 2)
        arc_r = rect.w // 2 - 6
        pygame.draw.arc(surf, a, (cx - arc_r, cy - arc_r, arc_r * 2, arc_r * 2), 0.3, 3.8, 3)
    elif k == "ring":
        pygame.draw.circle(surf, p, (cx, cy), rect.w // 2 - 2, width=5)
        pygame.draw.circle(surf, a, (cx, cy), 5)
    elif k == "spider":
        pygame.draw.rect(surf, p, rect.inflate(-4, -8), border_radius=4)
        for ox in (-8, 0, 8):
            pygame.draw.line(
                surf,
                a,
                (cx + ox, rect.bottom - 4),
                (cx + ox + (6 if ox else 8), rect.bottom + 10),
                3,
            )
    elif k == "robot":
        head = rect.inflate(-6, -10)
        pygame.draw.rect(surf, p, head, border_radius=3)
        pygame.draw.rect(
            surf,
            a,
            pygame.Rect(rect.left + 6, rect.bottom - 10, rect.w - 12, 8),
            border_radius=2,
        )
    elif k == "wave":
        pts = [
            (rect.left + 4, cy + 6),
            (rect.left + 14, cy - 8),
            (rect.left + 24, cy + 6),
            (rect.left + 34, cy - 8),
            (rect.right - 6, cy),
        ]
        pygame.draw.lines(surf, p, False, pts, 4)
        pygame.draw.lines(surf, a, False, pts, 2)
    else:
        pygame.draw.rect(surf, p, rect, border_radius=4)


def draw_game_icon_rotated(
    surf: pygame.Surface,
    rect: pygame.Rect,
    icon: dict[str, Any],
    mode: GameMode,
    angle_deg: float,
) -> None:
    """Havada dönen ikon — pygame.rotate saat yönü tersi için işaret."""
    pad = max(rect.w, rect.h)
    side = int(pad * 1.65)
    tmp = pygame.Surface((side, side), pygame.SRCALPHA)
    ox = (side - rect.w) // 2
    oy = (side - rect.h) // 2
    inner = pygame.Rect(ox, oy, rect.w, rect.h)
    draw_game_icon(tmp, inner, icon, mode)
    rot = pygame.transform.rotate(tmp, -angle_deg)
    surf.blit(rot, rot.get_rect(center=rect.center))
