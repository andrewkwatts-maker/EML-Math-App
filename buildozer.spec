[app]

title = EML-Math-App
package.name = emlmathapp
package.domain = org.emlmath.app

source.dir = src
source.include_exts = py,png,jpg,kv,atlas,svg,ttf,otf,json
source.include_patterns = eml_math_app/kv/*.kv,eml_math_app/assets/*

version = 1.3.1

requirements = python3,kivy==2.3.1,kivymd==1.2.0,pillow,eml-math

orientation = portrait
fullscreen = 0

# UI / launcher
icon.filename = src/eml_math_app/assets/icon.png
presplash.filename = src/eml_math_app/assets/splash.png
android.permissions = INTERNET

# Build matrix
android.api = 33
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.private_storage = True

# log level: 0 = silent, 1 = info, 2 = debug
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1
