"""Kozmetik ikonlar — mağaza ve seçim."""

from __future__ import annotations

SKINS: list[dict] = [
    {"id": 0, "name": "Klasik", "price": 0, "primary": (110, 190, 255), "accent": (40, 60, 120)},
    {"id": 1, "name": "Ateş", "price": 55, "primary": (255, 120, 60), "accent": (120, 30, 20)},
    {"id": 2, "name": "Orman", "price": 70, "primary": (80, 220, 120), "accent": (20, 80, 40)},
    {"id": 3, "name": "Gece", "price": 90, "primary": (160, 100, 255), "accent": (40, 20, 90)},
    {"id": 4, "name": "Altın", "price": 120, "primary": (255, 215, 80), "accent": (140, 90, 20)},
    {"id": 5, "name": "Buz", "price": 100, "primary": (180, 240, 255), "accent": (60, 120, 200)},
    {"id": 6, "name": "Neon", "price": 150, "primary": (255, 50, 180), "accent": (80, 0, 120)},
    {"id": 7, "name": "Gümüş", "price": 130, "primary": (200, 210, 230), "accent": (80, 90, 110)},
]


def skin_by_id(sid: int) -> dict:
    for s in SKINS:
        if s["id"] == sid:
            return s
    return SKINS[0]
