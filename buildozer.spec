[app]

# Uygulama adı (ekranda görünür)
title = DursunVenture

# Paket adı (Java stili, küçük harf, nokta ile)
package.name = dursunventure

# Domain (değiştir: kendi adın)
package.domain = org.dursunventure

# Ana Python dosyası
source.main = dursunventure.py

# Dahil edilecek dosya uzantıları
source.include_exts = py,png,wav,json,md,txt

# Dahil edilecek klasörler
source.include_patterns =
    assets/**
    *.py
    *.json

# Hariç tutulacaklar
source.exclude_exts = spec,pyc
source.exclude_dirs = .git,.github,__pycache__,tests

# Versiyon
version = 6.0

# Gerekli Python paketleri
requirements =
    python3,
    pygame==2.5.2,
    kivy==2.3.0,
    sdl2_ttf,
    sdl2_image,
    sdl2_mixer

# Uygulama ikonu
icon.filename = %(source.dir)s/assets/sprites/icon.png

# Yön (portrait veya landscape)
orientation = landscape

# Tam ekran
fullscreen = 1

# Pygame modu (kivy yerine pygame kullan)
# p4a.bootstrap = pygame

[buildozer]

# Android SDK/NDK log level
log_level = 2

# Uyarıları hata sayma
warn_on_root = 1

[android]

# Min Android versiyonu (5.0 = API 21)
android.minapi = 21

# Hedef API
android.api = 33

# NDK versiyonu
android.ndk = 25b

# SDK build-tools
android.build_tools_version = 34.0.0

# İzinler
android.permissions =
    INTERNET,
    READ_EXTERNAL_STORAGE,
    WRITE_EXTERNAL_STORAGE,
    VIBRATE

# Ekran boyutu (1248x960)
android.window_softinput_mode = adjustResize

# x86_64 + arm64 (geniş cihaz desteği)
android.archs = arm64-v8a, armeabi-v7a

# Debug imzalama (test için)
android.debug_artifact = apk

# Gradle versiyonu
android.gradle_dependencies =

# p4a branch
p4a.branch = master

# Bootstrap (pygame_bootstrap)
p4a.bootstrap = pygame

# Ek p4a argümanları
p4a.local_recipes =

[ios]
# iOS build (şimdilik kapalı)
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0
