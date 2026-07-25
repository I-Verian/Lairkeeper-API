"""
make_icon.py
------------
Downloads the Dragon Head icon from the wiki (same source as the app's
runtime window icon - assets/misc/dragonhead.png) and converts it into a
multi-resolution dragonhead.ico, so PyInstaller can embed it as the
actual .exe file icon (what Explorer/the taskbar shows) instead of its
generic default icon.

Run this before building: python make_icon.py
Then build with: pyinstaller --icon=dragonhead.ico ...
(build_exe.bat already does both steps for you.)
"""

import os
from PIL import Image
import wiki_icons

PNG_PATH = "dragonhead_source.png"
ICO_PATH = "dragonhead.ico"


def main():
    if not os.path.exists(PNG_PATH):
        print("Downloading Dragon Head icon from the wiki...")
        urls = wiki_icons.resolve_file_urls(["Dragon Head.png"], width=256)
        url = urls.get("Dragon Head.png")
        if not url:
            print("ERROR: could not resolve the Dragon Head icon from the wiki.")
            return False
        wiki_icons._download(url, PNG_PATH)
        print(f"Saved {PNG_PATH}")
    else:
        print(f"{PNG_PATH} already exists, skipping download.")

    img = Image.open(PNG_PATH).convert("RGBA")
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(ICO_PATH, format="ICO", sizes=sizes)
    print(f"Wrote {ICO_PATH} ({', '.join(f'{w}x{h}' for w, h in sizes)})")
    return True


if __name__ == "__main__":
    ok = main()
    if not ok:
        raise SystemExit(1)

