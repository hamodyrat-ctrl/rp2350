[app]

# (str) Title of your application
title = RP2350 CyberDeck

# (str) Package name
package.name = rp2350touch

# (str) Package domain (needed for android packaging)
package.domain = org.rp2350

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.3.0,pyserial

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 24

# (str) Android NDK architecture to build for
android.archs = arm64-v8a

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) List of inclusions using pattern matching
# android.add_libs_xml =

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = error, 1 = warning)
warn_on_root = 1
