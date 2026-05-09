[app]
title = BPI-COMMUNITY
package.name = bpicommunity
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, sqlite3
orientation = portrait
fullscreen = 1
android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True
android.archs = armeabi-v7a, arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
