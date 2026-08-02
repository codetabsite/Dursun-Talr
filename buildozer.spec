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
requirements = python3,pygame
icon.filename = %(source.dir)s/assets/sprites/icon.png
orientation = landscape
fullscreen = 1

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.minapi = 21
android.api = 31
android.ndk = 23b
android.build_tools_version = 31.0.0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,VIBRATE
android.archs = arm64-v8a
p4a.branch = master
p4a.bootstrap = sdl2
