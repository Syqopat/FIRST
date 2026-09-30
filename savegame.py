"""Oyuncu ilerlemesi ve ayarlar â€” JSON."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from config import SAVE_PATH
from game.modes import GameMode
from game_icons import default_owned_icon_ids, default_selected_icons


@dataclass
class SaveData:
    coins: int = 0
    completed: list[bool] = field(default_factory=lambda: [False] * 10)
    selected_skin: int = 0
    owned_skins: list[int] = field(default_factory=lambda: [0])
    owned_game_icon_ids: list[int] = field(default_factory=default_owned_icon_ids)
    selected_game_icons: dict[str, int] = field(default_factory=dict)
    music_vol: float = 0.5
    sfx_vol: float = 0.7
    fullscreen: bool = False
    reduce_motion: bool = False
    show_fps: bool = False
    particles: bool = True

    def __post_init__(self) -> None:
        if not self.selected_game_icons:
            self.selected_game_icons = default_selected_icons()
        for m in GameMode:
            if m.name not in self.selected_game_icons:
                self.selected_game_icons[m.name] = default_selected_icons()[m.name]
        for k in list(self.selected_game_icons.keys()):
            if k not in {x.name for x in GameMode}:
                del self.selected_game_icons[k]

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> SaveData:
        completed = d.get("completed")
        if not isinstance(completed, list) or len(completed) != 10:
            completed = [False] * 10
        owned = d.get("owned_skins")
        if not isinstance(owned, list) or not owned:
            owned = [0]

        ogi = d.get("owned_game_icon_ids")
        if not isinstance(ogi, list) or not ogi:
            ogi = default_owned_icon_ids()
        ogi = sorted({int(x) for x in ogi})

        sgi = d.get("selected_game_icons")
        base_sel = default_selected_icons()
        if not isinstance(sgi, dict):
            sgi = dict(base_sel)
        else:
            merged = dict(base_sel)
            for k, v in sgi.items():
                if k in merged:
                    merged[k] = int(v)
            sgi = merged

        return cls(
            coins=int(d.get("coins", 0)),
            completed=[bool(completed[i]) for i in range(10)],
            selected_skin=int(d.get("selected_skin", 0)),
            owned_skins=[int(x) for x in owned],
            owned_game_icon_ids=ogi,
            selected_game_icons=sgi,
            music_vol=float(d.get("music_vol", 0.5)),
            sfx_vol=float(d.get("sfx_vol", 0.7)),
            fullscreen=bool(d.get("fullscreen", False)),
            reduce_motion=bool(d.get("reduce_motion", False)),
            show_fps=bool(d.get("show_fps", False)),
            particles=bool(d.get("particles", True)),
        )


def load_save(path: str | Path | None = None) -> SaveData:
    p = Path(path or SAVE_PATH)
    if not p.is_file():
        return SaveData()
    try:
        with p.open("r", encoding="utf-8") as f:
            return SaveData.from_dict(json.load(f))
    except (json.JSONDecodeError, OSError, TypeError, ValueError):
        return SaveData()


def save_to_disk(data: SaveData, path: str | Path | None = None) -> None:
    p = Path(path or SAVE_PATH)
    with p.open("w", encoding="utf-8") as f:
        json.dump(data.to_dict(), f, indent=2)


def reward_for_level(difficulty: int, first_clear: bool) -> int:
    base = 8 + difficulty * 7
    return base + (15 if first_clear else 0)
