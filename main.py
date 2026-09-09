"""Geometry Run — giriş noktası."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pygame

from config import FPS, SCREEN_H, SCREEN_W
from savegame import load_save, save_to_disk
from scenes.gameplay import GameplayScene
from scenes.hub import HubScene
from scenes.icon_menu import IconMenuScene
from scenes.level_menu import LevelMenuScene
from scenes.main_menu import MainMenuScene
from scenes.settings_scene import SettingsScene
from scenes.shop import ShopScene
from transitions import ScreenFade


ROOT = Path(__file__).resolve().parent


class App:
    def __init__(self) -> None:
        os.chdir(ROOT)
        pygame.init()
        pygame.display.set_caption("Geometry Run")
        self.save = load_save()
        self.fade = ScreenFade()
        self._apply_display()
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.Font(None, 64)
        self.font_large = pygame.font.Font(None, 38)
        self.font_ui = pygame.font.Font(None, 30)
        self.font_small = pygame.font.Font(None, 22)
        self.running = True
        self.scene: (
            MainMenuScene
            | HubScene
            | IconMenuScene
            | LevelMenuScene
            | GameplayScene
            | ShopScene
            | SettingsScene
        )
        self.scene = HubScene(self)
        self.scene.on_enter()

    def _apply_display(self) -> None:
        flags = pygame.FULLSCREEN if self.save.fullscreen else 0
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), flags)

    def _fade_goto(self, mid, *, force_instant: bool = False) -> None:
        instant = bool(force_instant or self.save.reduce_motion)
        self.fade.start(mid, instant=instant)

    def goto_main_menu(self) -> None:
        def mid() -> None:
            self.scene = MainMenuScene(self)
            self.scene.on_enter()

        self._fade_goto(mid)

    def goto_hub(self) -> None:
        def mid() -> None:
            self.scene = HubScene(self)
            self.scene.on_enter()

        self._fade_goto(mid)

    def goto_icon_menu(self) -> None:
        def mid() -> None:
            self.scene = IconMenuScene(self)
            self.scene.on_enter()

        self._fade_goto(mid)

    def goto_level_menu(self, level_index: int = 0) -> None:
        idx = int(level_index)

        def mid() -> None:
            self.scene = LevelMenuScene(self)
            self.scene.on_enter(level_index=idx)

        self._fade_goto(mid)

    def goto_play(self, level_index: int, attempt: int = 1) -> None:
        idx = int(level_index)
        att = max(1, int(attempt))

        def mid() -> None:
            self.scene = GameplayScene(self)
            self.scene.on_enter(level_index=idx, attempt=att)

        self._fade_goto(mid)

    def goto_shop(self) -> None:
        def mid() -> None:
            self.scene = ShopScene(self)
            self.scene.on_enter()

        self._fade_goto(mid)

    def goto_settings(self) -> None:
        def mid() -> None:
            self.scene = SettingsScene(self)
            self.scene.on_enter()

        self._fade_goto(mid)

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            events = list(pygame.event.get())
            for e in events:
                if e.type == pygame.QUIT:
                    self.running = False

            block = self.fade.active
            if not block:
                self.scene.handle(events)

            self.fade.update(dt)
            if not block:
                self.scene.update(dt)

            self.scene.draw(self.screen)
            self.fade.draw(self.screen)

            if self.save.show_fps:
                fps_t = self.font_small.render(f"{int(self.clock.get_fps())} FPS", True, (160, 255, 160))
                self.screen.blit(fps_t, (SCREEN_W - fps_t.get_width() - 8, 8))

            pygame.display.flip()

        save_to_disk(self.save)
        pygame.quit()


def main() -> None:
    App().run()
    sys.exit(0)


if __name__ == "__main__":
    main()
