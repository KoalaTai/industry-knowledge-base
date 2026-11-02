#!/usr/bin/env python3
"""One-step installer for the AC Worlds datapack.

    python3 minecraft/install.py            # interactive: pick a world, done
    python3 minecraft/install.py --world "My World"
    python3 minecraft/install.py --list     # just show your worlds

(On Windows use ``py`` instead of ``python3``.)

It finds your .minecraft folder (Windows, macOS, Linux), copies
ac_worlds.zip into <world>/datapacks/, and tells you what to type in game.
If the zip is not next to this script it is downloaded from GitHub.
Needs only Python 3; nothing else to install.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ZIP_NAME = "ac_worlds.zip"
LOCAL_ZIP = os.path.join(HERE, "datapack", ZIP_NAME)
RAW_URL = "https://raw.githubusercontent.com/KoalaTai/industry-knowledge-base/main/minecraft/datapack/ac_worlds.zip"


def minecraft_dir() -> str | None:
    env = os.environ.get("MINECRAFT_DIR")
    candidates = [env] if env else []
    home = os.path.expanduser("~")
    if sys.platform.startswith("win"):
        candidates.append(os.path.join(os.environ.get("APPDATA", ""), ".minecraft"))
    elif sys.platform == "darwin":
        candidates.append(os.path.join(home, "Library", "Application Support", "minecraft"))
    candidates += [
        os.path.join(home, ".minecraft"),
        os.path.join(home, ".var", "app", "com.mojang.Minecraft", ".minecraft"),      # Flatpak
        os.path.join(home, "snap", "mc-installer", "current", ".minecraft"),
    ]
    for c in candidates:
        if c and os.path.isdir(os.path.join(c, "saves")):
            return c
    return None


def get_zip() -> str:
    if os.path.isfile(LOCAL_ZIP):
        return LOCAL_ZIP
    dest = os.path.join(HERE, ZIP_NAME)
    print(f"Downloading the datapack from GitHub ...")
    urllib.request.urlretrieve(RAW_URL, dest)
    return dest


def main() -> None:
    ap = argparse.ArgumentParser(description="Install the AC Worlds datapack into a Minecraft world.")
    ap.add_argument("--world", help="world folder name under saves/ (default: ask)")
    ap.add_argument("--minecraft-dir", help="override the .minecraft location")
    ap.add_argument("--list", action="store_true", help="list worlds and exit")
    args = ap.parse_args()

    mc = args.minecraft_dir or minecraft_dir()
    if not mc:
        print("Could not find your .minecraft folder. Run again with --minecraft-dir <path> "
              "(the folder that contains 'saves'), or set MINECRAFT_DIR.")
        sys.exit(1)
    saves = os.path.join(mc, "saves")
    worlds = sorted(d for d in os.listdir(saves) if os.path.isdir(os.path.join(saves, d)))
    print(f"Minecraft folder: {mc}")
    if not worlds:
        print("No worlds yet. In Minecraft: Create New World > (Creative, Superflat) > More > Data Packs > "
              f"Open Pack Folder, drop in {LOCAL_ZIP}, move it to Selected, create the world. It builds itself.")
        sys.exit(0)
    if args.list or not args.world:
        print("Your worlds:")
        for i, w in enumerate(worlds, 1):
            print(f"  {i}. {w}")
        if args.list:
            return
    world = args.world
    if not world:
        choice = input("Install into which world? (number, or Enter to cancel) ").strip()
        if not choice:
            print("Cancelled. Tip: make a new Creative Superflat world first, then run this again.")
            return
        try:
            world = worlds[int(choice) - 1]
        except (ValueError, IndexError):
            print("Not a valid number."); sys.exit(1)
    wdir = os.path.join(saves, world)
    if not os.path.isdir(wdir):
        print(f"No world called '{world}' in {saves}"); sys.exit(1)

    src = get_zip()
    dp = os.path.join(wdir, "datapacks")
    os.makedirs(dp, exist_ok=True)
    dst = os.path.join(dp, ZIP_NAME)
    shutil.copyfile(src, dst)
    print(f"\nInstalled: {dst}")
    print("\nNow, in Minecraft:")
    print(f"  1. Open the world '{world}' (if it is already open, type /reload).")
    print("  2. Wait: 15 seconds after you join, the pack auto-builds everything north of you.")
    print("     Type /function ac:cancel within those 15 seconds to skip the auto-build.")
    print("  3. /function ac:index   lists every world, landmark and technology model.")
    print("     /function ac:egypt/giza   (or any other) builds it where you stand, facing north.")
    print("\nWorks best in a Creative world with a Superflat world type and cheats enabled.")


if __name__ == "__main__":
    main()
