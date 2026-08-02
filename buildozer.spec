[app]
title = DursunVenture
package.name = dursunventure
package.domain = org.dursunventure
source.dir = .
source.main = dursunventure.py
source.include_exts = py,png,wav,json
source.include_patterns = assets/**,*.py,*.json
source.exclude_exts = spec,pyc
source.exclude_dirs = .git,.github,__pycache__
version = 6.0
requirements = python3,kivy,pygame
icon.filename = %(source.dir)s/assets/sprites/icon.png
orientation = landscape
fullscreen = 1

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.minapi = 21
android.api = 33
android.ndk = 28c
android.build_tools_version = 33.0.2
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,VIBRATE
android.archs = arm64-v8a
android.cmdline_tools_version = 11.0
p4a.branch = master
p4a.bootstrap = sdl2
