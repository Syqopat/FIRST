# 🎮 FIRST (Pygame Platform Engine & Game)

![Status](https://img.shields.io/badge/Status-Working%20%2F%20Stable-brightgreen?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge)
![Pygame](https://img.shields.io/badge/Pygame-CE-green?style=for-the-badge)
![CI](https://img.shields.io/badge/CI%2FCD-Active-success?style=for-the-badge)

**FIRST** is a 2D platformer engine and game built with Pygame. It features a modular scene manager (Main Menu, Level Menu, Shop, Gameplay), collision detection, and JSON save progression.

---

## 📌 Project Status

- **Status:** 🟢 **Working / Stable**
- **CI/CD:** Automated GitHub Actions syntax checking active.
- **Configuration:** Resolution, FPS, and volume configurable via `config.json`.

---

## 🚀 Key Features

- **Modular Scene Architecture:** Decoupled scene classes for UI, menus, shop, and gameplay.
- **Skins & Customization:** In-game shop and character skin selection system.
- **Save System (`savegame.py`):** Saves player progress in JSON format.

---

## 🛠️ Installation & Execution

```bash
pip install -r requirements.txt
python main.py
```

---

## ⚙️ Configuration (`config.json`)

```json
{
  "screen_width": 1280,
  "screen_height": 720,
  "fps": 60,
  "sound_volume": 0.8,
  "music_volume": 0.5
}
```

---

## 📄 License

Licensed under the MIT License.
