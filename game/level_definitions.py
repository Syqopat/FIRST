"""10 bölüm: zorluk, hız, uzunluk ve nesneler (blok, diken, portal)."""

from __future__ import annotations

from typing import Any

FLOOR_TOP = 640
FLOOR_H = 200


def _floor(x: float, w: float) -> dict[str, Any]:
    return {"type": "block", "x": x, "y": FLOOR_TOP, "w": w, "h": FLOOR_H}


def _blk(x: float, y: float, w: float, h: float) -> dict[str, Any]:
    return {"type": "block", "x": x, "y": y, "w": w, "h": h}


def _spk(x: float, y: float, w: float = 26, h: float = 28) -> dict[str, Any]:
    return {"type": "spike", "x": x, "y": y, "w": w, "h": h}


def _prt(x: float, y: float, mode: str, h: float = 100) -> dict[str, Any]:
    return {"type": "portal", "x": x, "y": y, "w": 44, "h": h, "mode": mode}


def _gate(x: float, speed: float, y: float | None = None, w: float = 46, h: float = 112) -> dict[str, Any]:
    yy = FLOOR_TOP - 98 if y is None else y
    return {"type": "speed_gate", "x": x, "y": yy, "w": w, "h": h, "speed": speed}


def build_levels() -> list[dict[str, Any]]:
    """Zorluk 1–10 artar; her bölümde farklı portal dizilimi."""
    L: list[dict[str, Any]] = []

    # 1 — Cube tanıtım (taban hız düşük; hız kapıları ile artar)
    L.append(
        {
            "name": "Nefes",
            "difficulty": 1,
            "scroll_speed": 76,
            "length": 2800,
            "objects": [
                _floor(0, 4000),
                _gate(240, 96),
                _spk(520, FLOOR_TOP - 28),
                _spk(780, FLOOR_TOP - 28),
                _gate(920, 78),
                _spk(1100, FLOOR_TOP - 28),
                _blk(1400, 520, 180, 24),
                _gate(1360, 102),
                _spk(1580, 492),
                _spk(1750, FLOOR_TOP - 28),
                _gate(1880, 88),
            ],
        }
    )

    # 2 — Ship portalı
    L.append(
        {
            "name": "Rüzgar",
            "difficulty": 2,
            "scroll_speed": 74,
            "length": 3000,
            "objects": [
                _floor(0, 4500),
                _gate(200, 104),
                _spk(400, FLOOR_TOP - 28),
                _prt(700, FLOOR_TOP - 120, "ship"),
                _gate(980, 118),
                _blk(1100, 500, 120, 20),
                _blk(1350, 440, 120, 20),
                _spk(1280, FLOOR_TOP - 28),
                _gate(1520, 96),
                _prt(1700, FLOOR_TOP - 120, "cube"),
                _gate(1920, 128),
                _spk(2100, FLOOR_TOP - 28),
            ],
        }
    )

    # 3 — Ball
    L.append(
        {
            "name": "Yerçekimi",
            "difficulty": 3,
            "scroll_speed": 72,
            "length": 3200,
            "objects": [
                _floor(0, 5000),
                _gate(280, 110),
                _prt(450, FLOOR_TOP - 120, "ball"),
                _spk(750, FLOOR_TOP - 28),
                _gate(820, 88),
                _spk(900, FLOOR_TOP - 28),
                _blk(1050, 380, 200, 22),
                _spk(1180, 350),
                _gate(1320, 122),
                _prt(1500, 300, "cube"),
                _spk(1900, FLOOR_TOP - 28),
                _gate(2100, 98),
            ],
        }
    )

    # 4 — Robot (zıplama süresi)
    L.append(
        {
            "name": "Mekanik",
            "difficulty": 4,
            "scroll_speed": 72,
            "length": 3400,
            "objects": [
                _floor(0, 5200),
                _gate(220, 108),
                _prt(380, FLOOR_TOP - 120, "robot"),
                _blk(700, 520, 90, 18),
                _blk(880, 470, 90, 18),
                _spk(820, FLOOR_TOP - 28),
                _gate(1040, 92),
                _prt(1250, FLOOR_TOP - 120, "cube"),
                _gate(1420, 126),
                _spk(1600, FLOOR_TOP - 28),
                _spk(1750, FLOOR_TOP - 28),
                _gate(1880, 100),
            ],
        }
    )

    # 5 — Wave kısa
    L.append(
        {
            "name": "Dalga",
            "difficulty": 5,
            "scroll_speed": 74,
            "length": 3500,
            "objects": [
                _floor(0, 5500),
                _gate(260, 112),
                _prt(400, FLOOR_TOP - 130, "wave", 120),
                _blk(900, 520, 60, 20),
                _blk(1050, 420, 60, 20),
                _gate(1120, 94),
                _blk(1200, 520, 60, 20),
                _prt(1550, 360, "cube", 120),
                _gate(1680, 132),
                _spk(1850, FLOOR_TOP - 28),
            ],
        }
    )

    # 6 — Spider
    L.append(
        {
            "name": "Tavan",
            "difficulty": 6,
            "scroll_speed": 76,
            "length": 3800,
            "objects": [
                _floor(0, 6000),
                _blk(0, 100, 6000, 40),
                _gate(360, 118),
                _prt(500, 420, "spider", 110),
                _spk(900, FLOOR_TOP - 28),
                _spk(1050, 130, 26, 28),
                _gate(1180, 96),
                _prt(1400, 400, "cube", 110),
                _spk(1800, FLOOR_TOP - 28),
                _gate(1920, 136),
                _spk(2100, FLOOR_TOP - 28),
            ],
        }
    )

    # 7 — Karışık portal zinciri
    L.append(
        {
            "name": "Geçit",
            "difficulty": 7,
            "scroll_speed": 78,
            "length": 4200,
            "objects": [
                _floor(0, 6500),
                _blk(0, 100, 7000, 36),
                _gate(240, 120),
                _spk(350, FLOOR_TOP - 28),
                _prt(600, FLOOR_TOP - 120, "ship"),
                _blk(1000, 480, 100, 18),
                _gate(1120, 98),
                _prt(1250, 380, "ball", 100),
                _spk(1500, FLOOR_TOP - 28),
                _prt(1750, FLOOR_TOP - 120, "robot"),
                _gate(1960, 138),
                _prt(2150, FLOOR_TOP - 120, "cube"),
                _spk(2450, FLOOR_TOP - 28),
                _gate(2580, 108),
            ],
        }
    )

    # 8 — Wave + diken koridoru
    L.append(
        {
            "name": "Dar Koridor",
            "difficulty": 8,
            "scroll_speed": 80,
            "length": 4500,
            "objects": [
                _floor(0, 7000),
                _blk(0, 100, 8000, 34),
                _gate(300, 124),
                _prt(420, 400, "wave", 120),
                _spk(800, FLOOR_TOP - 28),
                _gate(880, 102),
                _spk(950, 130),
                _spk(1100, FLOOR_TOP - 28),
                _prt(1450, 380, "cube"),
                _gate(1620, 142),
                _spk(1900, FLOOR_TOP - 28),
                _spk(2100, FLOOR_TOP - 28),
                _spk(2300, 130),
                _gate(2380, 112),
            ],
        }
    )

    # 9 — Yoğun
    L.append(
        {
            "name": "Kaos",
            "difficulty": 9,
            "scroll_speed": 82,
            "length": 4800,
            "objects": [
                _floor(0, 7500),
                _blk(0, 100, 9000, 32),
                _gate(220, 128),
                _spk(300, FLOOR_TOP - 28),
                _prt(550, FLOOR_TOP - 118, "ball"),
                _spk(800, FLOOR_TOP - 28),
                _spk(880, 130),
                _gate(980, 108),
                _prt(1100, 360, "spider", 105),
                _spk(1400, FLOOR_TOP - 28),
                _prt(1650, FLOOR_TOP - 118, "ship"),
                _blk(2000, 460, 80, 16),
                _spk(2120, FLOOR_TOP - 28),
                _gate(2220, 146),
                _prt(2350, FLOOR_TOP - 118, "cube"),
                _spk(2700, FLOOR_TOP - 28),
                _spk(2900, FLOOR_TOP - 28),
            ],
        }
    )

    # 10 — Final
    L.append(
        {
            "name": "Son Sınır",
            "difficulty": 10,
            "scroll_speed": 84,
            "length": 5200,
            "objects": [
                _floor(0, 9000),
                _blk(0, 98, 10000, 30),
                _gate(200, 132),
                _spk(280, FLOOR_TOP - 28),
                _prt(480, FLOOR_TOP - 125, "robot"),
                _spk(720, FLOOR_TOP - 28),
                _gate(820, 118),
                _prt(950, 350, "wave", 125),
                _spk(1200, 130),
                _spk(1350, FLOOR_TOP - 28),
                _gate(1460, 152),
                _prt(1580, FLOOR_TOP - 125, "ball"),
                _spk(1820, FLOOR_TOP - 28),
                _prt(2050, 340, "spider", 108),
                _gate(2160, 128),
                _spk(2300, FLOOR_TOP - 28),
                _prt(2550, FLOOR_TOP - 125, "ship"),
                _spk(2800, FLOOR_TOP - 28),
                _gate(2880, 158),
                _prt(3050, FLOOR_TOP - 125, "cube"),
                _spk(3300, FLOOR_TOP - 28),
                _spk(3500, FLOOR_TOP - 28),
                _spk(3700, 130),
                _gate(3580, 134),
                _spk(3950, FLOOR_TOP - 28),
            ],
        }
    )

    return L


LEVELS = build_levels()
