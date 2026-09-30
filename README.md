# 🎮 FIRST (Pygame Platform Engine & Game)

![Status](https://img.shields.io/badge/Durum-%C3%87al%C4%B1%C5%9F%C4%B1yor%20%2F%20Working-brightgreen?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge)
![Pygame](https://img.shields.io/badge/Pygame-CE-green?style=for-the-badge)
![CI](https://img.shields.io/badge/CI%2FCD-Active-success?style=for-the-badge)

**FIRST**, Pygame tabanlı 2D platform oyun motoru ve oyun projesidir. Modüler sahne yönetimi (main menu, level menu, shop, gameplay), çarpışma kontrol sistemi ve seviye kaydetme özellikleri sunar.

---

## 📌 Proje Durumu (Project Status)

- **Durum:** 🟢 **Çalışıyor (Working / Stable)**
- **Test & CI/CD:** GitHub Actions syntax denetimi aktif.
- **Konfigürasyon:** `config.json` ile çözünürlük, FPS ve ses seviyeleri ayarlanabilir.

---

## 🚀 Özellikler

- **Modüler Sahne Mimari:** Menü, seviye seçimi, market ve oyun sahneleri decoupled sınıflar halinde tasarlanmıştır.
- **Karakter ve Görünüşler (Skins):** Market ve görünüm seçimi entegredir.
- **Kaydetme Sistemi (`savegame.py`):** Oyuncu ilerlemesini JSON formatında saklar.

---

## 🛠️ Kurulum ve Kullanım

```bash
pip install -r requirements.txt
python main.py
```

---

## ⚙️ Yapılandırma (`config.json`)

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

## 📄 Lisans

MIT License
