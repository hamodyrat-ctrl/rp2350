[app]

# (str) Title of your application
title = RP2350 CyberDeck

# (str) Package name
package.name = rp2350touch

# (str) Package domain
package.domain = org.rp2350

# (str) Source code directory
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 1.0

# (list) Application requirements
requirements = python3,kivy==2.3.0,pyserial

# (list) Permissions
android.permissions = INTERNET

# (bool) Accept SDK license automatically
android.accept_sdk_license = True

# (str) Android NDK version to use (إصدار مستقر يمنع التعارض)
android.ndk = 25b

# (int) Target Android API
android.api = 33

# (int) Minimum API supported
android.minapi = 24

# (str) Android NDK architecture
android.archs = arm64-v8a

# (bool) Fullscreen mode
fullscreen = 1

[buildozer]

# (int) Log level
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
