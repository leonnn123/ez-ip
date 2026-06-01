import os
import sys
import shutil

def create_feather_logo():
    print("🎨 Drawing the blue feather logo natively in memory...")
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("🔧 Installing required graphics library...")
        os.system(f'"{sys.executable}" -m pip install pillow')
        from PIL import Image, ImageDraw

    # Create a clean 512x512 canvas with a transparent background
    img = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a stylized modern blue feather using native math coordinates
    draw.polygon([(400, 120), (310, 150), (240, 220), (180, 300), (150, 360), (260, 260)], fill="#00b4d8")
    draw.polygon([(310, 150), (200, 240), (140, 340), (220, 260)], fill="#90e0ef")
    draw.polygon([(400, 120), (350, 210), (290, 280), (220, 350), (190, 380), (290, 290)], fill="#0096c7")
    draw.line([(120, 400), (400, 120)], fill="#0077b6", width=10)
    
    img.save("blue_feather.png", "PNG")
    print("✅ Blue feather logo generated successfully as 'blue_feather.png'.")

def build_mac_bundle():
    print("📁 Building the official macOS Application Bundle structure...")
    
    # EXACT CASE SENSITIVE MACOS APPLICATION ARCHITECTURE
    base_dir = "QuickIPHost.app"
    contents_dir = os.path.join(base_dir, "Contents")
    macos_dir = os.path.join(contents_dir, "MacOS")
    resources_dir = os.path.join(contents_dir, "Resources")
    
    # Clean previous attempts to prevent folder merging errors
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
        
    os.makedirs(macos_dir, exist_ok=True)
    os.makedirs(resources_dir, exist_ok=True)
    
    # Official structure requires Info.plist directly inside Contents/
    plist_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://apple.com">
<plist version="1.0">
<dict>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>QuickIPHost</string>
    <key>CFBundleDisplayName</key>
    <string>Quick IP Host</string>
    <key>CFBundleIdentifier</key>
    <string>com.localip.hoster</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleExecutable</key>
    <string>QuickIPHost</string>
    <key>CFBundleIconFile</key>
    <string>icon.icns</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>\n"""
    
    with open(os.path.join(contents_dir, "Info.plist"), "w", newline="\n", encoding="utf-8") as f:
        f.write(plist_content)
        
    # The running python file goes in Resources to avoid binary verification issues
    if os.path.exists("hoster.py"):
        shutil.copy("hoster.py", os.path.join(resources_dir, "hoster.py"))
    else:
        with open(os.path.join(resources_dir, "hoster.py"), "w", newline="\n", encoding="utf-8") as f:
            f.write("# Fallback\nprint('Server Booted')\n")
        
    # The executable target inside MacOS/ MUST match CFBundleExecutable exactly
    # We use newline="\n" to force Unix line breaks even when built on Windows
    bootstrap_content = """#!/bin/sh
DIR=$(dirname "$0")
python3 "$DIR/../Resources/hoster.py"
"""
    with open(os.path.join(macos_dir, "QuickIPHost"), "w", newline="\n", encoding="utf-8") as f:
        f.write(bootstrap_content)

    # Place the icon file into Resources
    if os.path.exists("blue_feather.png"):
        shutil.copy("blue_feather.png", os.path.join(resources_dir, "icon.icns"))
        
    print(f"👉 Corrected macOS Bundle folder assembled: \\{base_dir}")

def build_linux_structures():
    print("📁 Building your native Linux packaging architectures...")
    
    # Official Debian file layouts require precise system folder setups
    deb_base = "quick-ip-host_1.0_amd64"
    deb_bin = os.path.join(deb_base, "usr", "bin")
    deb_meta = os.path.join(deb_base, "DEBIAN")
    deb_apps = os.path.join(deb_base, "usr", "share", "applications")
    deb_share = os.path.join(deb_base, "usr", "share", "pixmaps")
    
    if os.path.exists(deb_base):
        shutil.rmtree(deb_base)
        
    os.makedirs(deb_bin, exist_ok=True)
    os.makedirs(deb_meta, exist_ok=True)
    os.makedirs(deb_apps, exist_ok=True)
    os.makedirs(deb_share, exist_ok=True)
    
    if os.path.exists("hoster.py"):
        shutil.copy("hoster.py", os.path.join(deb_bin, "quick-ip-host.py"))
    if os.path.exists("blue_feather.png"):
        shutil.copy("blue_feather.png", os.path.join(deb_share, "quick-ip-host.png"))
        
    # Linux deb control configuration file
    control_content = """Package: quick-ip-host
Version: 1.0.0
Architecture: amd64
Maintainer: Developer <you@email.com>
Depends: python3, python3-tk, python3-pillow
Description: Simple GUI utility to host directories via a pure local IP address.
"""
    with open(os.path.join(deb_meta, "control"), "w", newline="\n", encoding="utf-8") as f:
        f.write(control_content)

    # Native Linux applications menu item integration (.desktop file)
    desktop_content = """[Desktop Entry]
Name=Quick IP Host
Exec=python3 /usr/bin/quick-ip-host.py
Icon=quick-ip-host
Type=Application
Categories=Development;Utility;
Terminal=false
"""
    with open(os.path.join(deb_apps, "quick-ip-host.desktop"), "w", newline="\n", encoding="utf-8") as f:
        f.write(desktop_content)

    # Setup AppDir for Linux AppImage builds
    appdir_base = "QuickIPHost.AppDir"
    if os.path.exists(appdir_base):
        shutil.rmtree(appdir_base)
        
    os.makedirs(appdir_base, exist_ok=True)
    
    if os.path.exists("hoster.py"):
        shutil.copy("hoster.py", os.path.join(appdir_base, "hoster.py"))
    if os.path.exists("blue_feather.png"):
        shutil.copy("blue_feather.png", os.path.join(appdir_base, "quick-ip-host.png"))
    with open(os.path.join(appdir_base, "quick-ip-host.desktop"), "w", newline="\n", encoding="utf-8") as f:
        f.write(desktop_content)
        
    print(f"👉 Linux DEB structure folder assembled: \\{deb_base}")
    print(f"👉 Linux AppImage structure folder assembled: \\{appdir_base}")

if __name__ == "__main__":
    create_feather_logo()
    build_mac_bundle()
    build_linux_structures()
    print("\n🎉 ALL ARCHITECTURES REMADE WITH STRICT CASE-SENSITIVE STRUCTURES!")
