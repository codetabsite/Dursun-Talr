# 🎮 DursunVenture v6.0

Undertale tarzı Türkçe RPG — 120x80 dev dünya

## 📦 APK İndirme

1. GitHub'a push et
2. Actions sekmesine git
3. **DursunVenture Android APK Build** workflow'unu aç
4. Build bitince **Artifacts** bölümünden `DursunVenture-debug-apk` indir
5. `.apk` dosyasını Android'e kopyala → Kur

## 🚀 GitHub'a Yükleme (ilk kez)

```bash
git init
git add .
git commit -m "DursunVenture v6.0 ilk commit"
git remote add origin https://github.com/codetabsite/Dursun-Talr.git
git push -u origin main
```

Push atınca Actions **otomatik** başlar!

## 🎮 Kontroller

| Tuş | Eylem |
|-----|-------|
| ↑↓←→ | Hareket |
| Z / Enter | Konuş / Onayla |
| X / Esc | Geri |
| S | Kaydet |
| J | Görev günlüğü |
| Q | Pause |
| F11 | Tam ekran |

## 🗺️ Bölgeler (120x80 harita)

- **Dursunköy** — Köy merkezi, NPC'ler
- **Pazar Yeri** — Hüsrev'in mağazası, tezgahlar
- **Gizemli Orman** — Karşılaşmalar, Orman Ruhu boss
- **Gizli Mağara** — Sandıklar, yeraltı boss
- **Terk Edilmiş Fabrika** — Fabrika düşmanları
- **Göl Kenarı** — Balıkçı köyü, tekne
- **THE ALGO Geçişi** — Final boss bölgesi

## 🏃 Yerel Çalıştırma

```bash
# Bağımlılıklar
pip install pygame

# Sprite & ses üret (ilk çalıştırmada)
python3 sprite_gen.py
cd assets/sounds && python3 gen_sounds.py && cd ../..
python3 mapgen.py

# Oyunu başlat
python3 dursunventure.py
```

## 📁 Dosya Yapısı

```
dursunventure_v6/
├── .github/
│   └── workflows/
│       └── build_apk.yml    ← GitHub Actions
├── assets/
│   ├── sprites/             ← 66 PNG sprite
│   └── sounds/              ← 33 WAV ses
├── dursunventure.py         ← Ana oyun (1496 satır)
├── dialogues.py             ← Diyaloglar (746 satır)
├── systems.py               ← Gece/Gündüz, Quest, Cutscene
├── mapgen.py                ← Harita üretici
├── sprite_gen.py            ← Sprite üretici
├── buildozer.spec           ← Android build ayarları
└── map_data.json            ← 120x80 harita verisi
```

## ⚠️ Önemli Notlar

- İlk build ~30-45 dakika sürer (SDK/NDK indirir)
- Sonraki buildler cache sayesinde ~10 dakika
- APK debug imzalıdır (test için) — yayınlamak için keystore gerekir
- Android 5.0+ (API 21) desteklenir
