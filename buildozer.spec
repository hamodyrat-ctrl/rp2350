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
requirements = python3,kivy,pyserial

# (list) Permissions
android.permissions = INTERNET

# (bool) Fullscreen mode
fullscreen = 1

[buildozer]

# (int) Log level
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
