#!/usr/bin/env python3
"""Generate the "AC Worlds" Minecraft datapack and the knowledge catalogue.

    python generate.py                 # writes minecraft/datapack/ac_worlds and knowledge/README.md
    python generate.py --out DIR       # custom output directory

Function layout (namespace ``ac``), all run as a player standing where the
build should appear (ground = the block under your feet):

    ac:hub                      every world and every technology model, laid out in rows
    ac:hub_assassins_creed      only the Assassin's Creed worlds
    ac:hub_avatar               only the Avatar worlds
    ac:hub_tech                 only the premodern-technology models
    ac:<world>/all              one world's builds in a row (e.g. ac:egypt/all)
    ac:<world>/<build>          one landmark (e.g. ac:egypt/giza)
    ac:tech/<model>             one technology model (e.g. ac:tech/aqueduct)
    ac:index                    list everything in chat
    ac:cancel                   stop a running build sequence / the auto-build
    ac:reset_auto               re-arm the automatic hub build on next join

Every build runs as a short scheduled sequence: force-load the chunks,
wait two seconds, place the blocks, release the chunks.  The raw
placement functions live under ``ac:raw/...`` for command blocks.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import textwrap
import zipfile
from typing import Dict, List, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from acworlds import Voxel, all_worlds  # noqa: E402
from acworlds.export import Datapack, tellraw, to_commands  # noqa: E402
from acworlds.technology import MODELS, TECH_BUILD_NOTES  # noqa: E402

NS = "ac"
GAP = 24                 # blocks between builds in a row
ROW_GAP = 40             # blocks between rows
WAIT_TICKS = 60          # ticks to wait after force-loading before placing


def say(text: str, color: str = "gold", bold: bool = False) -> str:
    comp = {"text": text, "color": color}
    if bold:
        comp["bold"] = True
    return "tellraw @a " + json.dumps(comp, ensure_ascii=False)


def forceload_cmds(x1: int, z1: int, x2: int, z2: int, dx: int, dz: int, add: bool = True) -> List[str]:
    """forceload accepts at most 256 chunks per call: tile the area in 256x256 blocks."""
    out = []
    verb = "add" if add else "remove"
    x1, z1, x2, z2 = x1 + dx, z1 + dz, x2 + dx, z2 + dz
    xs = list(range(x1, x2 + 1, 256)) + [x2 + 1]
    zs = list(range(z1, z2 + 1, 256)) + [z2 + 1]
    for i in range(len(xs) - 1):
        for j in range(len(zs) - 1):
            out.append(f"forceload {verb} ~{xs[i]} ~{zs[j]} ~{xs[i + 1] - 1} ~{zs[j + 1] - 1}")
    return out


class Item:
    """A placeable thing: either a world build or a tech model."""

    def __init__(self, seq_id: str, raw_fn: str, name: str, bounds: Tuple[int, int, int, int, int, int]) -> None:
        self.seq_id = seq_id          # e.g. "egypt_giza"
        self.raw_fn = raw_fn          # e.g. "raw/egypt/giza"
        self.name = name
        self.bounds = bounds          # x1 y1 z1 x2 y2 z2 relative to its own origin


def add_sequence(pack: Datapack, seq: str, items: List[Tuple[Item, int, int]], title: str) -> None:
    """Create ac:<seq> (entry) and ac:_s/<seq>/<n> (steps) for a list of (item, dx, dz)."""
    pack.add(seq, [
        f"execute store result storage {NS}:seq x int 1 run data get entity @s Pos[0]",
        f"execute store result storage {NS}:seq y int 1 run data get entity @s Pos[1]",
        f"execute store result storage {NS}:seq z int 1 run data get entity @s Pos[2]",
        f"data modify storage {NS}:seq seq set value \"{seq.replace('/', '.')}\"",
        f"data modify storage {NS}:seq step set value 0",
        say(f"{title}: {len(items)} build(s) queued. Chunks are force-loaded two seconds before each placement.", "aqua"),
        f"function {NS}:_next",
    ])
    sname = seq.replace("/", ".")
    n = 0
    for item, dx, dz in items:
        x1, _, z1, x2, _, z2 = item.bounds
        pack.add(f"_s/{sname}/{n}", [say(f"Loading chunks for {item.name} ...", "gray")]
                 + forceload_cmds(x1, z1, x2, z2, dx, dz, add=True)
                 + [f"function {NS}:_adv"])
        n += 1
        pos = "~ ~ ~" if (dx, dz) == (0, 0) else f"~{dx} ~ ~{dz}"
        pack.add(f"_s/{sname}/{n}", [
            f"execute positioned {pos} run function {NS}:{item.raw_fn}",
            *forceload_cmds(x1, z1, x2, z2, dx, dz, add=False),
            say(f"Placed {item.name} at offset ({dx}, {dz}).", "green"),
            f"function {NS}:_adv",
        ])
        n += 1
    pack.add(f"_s/{sname}/{n}", [say(f"{title}: done.", "gold", bold=True)])


def layout_rows(rows: List[List[Item]], z_start: int = 24) -> List[Tuple[Item, int, int]]:
    """Lay rows of items along +x, rows along +z; return (item, dx, dz) placements."""
    placed = []
    cz = z_start
    for row in rows:
        if not row:
            continue
        cx = 0
        depth = 0
        for it in row:
            x1, _, z1, x2, _, z2 = it.bounds
            placed.append((it, cx - x1, cz - z1))
            cx += (x2 - x1 + 1) + GAP
            depth = max(depth, z2 - z1 + 1)
        cz += depth + ROW_GAP
    return placed


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "datapack", "ac_worlds"))
    args = ap.parse_args()

    with open(os.path.join(HERE, "knowledge", "premodern_technology.json"), encoding="utf-8") as f:
        kb = json.load(f)
    records = kb["records"]
    by_model: Dict[str, dict] = {r["tech_model"]: r for r in records if r.get("tech_model")}

    pack = Datapack(NS, "AC Worlds: Assassin's Creed and Avatar settings plus premodern technology models")
    worlds = all_worlds()
    index_lines: List[str] = [say("AC Worlds - functions (run as a player, facing where you want the build):", "gold", True)]
    world_items: Dict[str, List[Item]] = {}
    total_cmds = 0
    manifest = []

    # ---- world builds
    for w in worlds:
        items = []
        index_lines.append(say(f"[{w.franchise}] {w.name} - {w.game} ({w.era})", "yellow", True))
        index_lines.append(say(f"  /function {NS}:{w.id}/all", "aqua"))
        for b in w.builds:
            v = Voxel()
            b.builder(v)
            cmds = to_commands(v)
            size = v.size()
            total_cmds += len(cmds)
            raw = f"raw/{w.id}/{b.id}"
            head = [say(f"{b.name} ({w.name})", "gold", True), say(b.description, "white")]
            if b.scale:
                head.append(say(f"Scale: {b.scale}", "gray"))
            pack.add(raw, head + cmds)
            item = Item(f"{w.id}_{b.id}", raw, b.name, v.bounds())
            items.append(item)
            add_sequence(pack, f"{w.id}/{b.id}", [(item, 0, 0)], b.name)
            index_lines.append(say(f"  /function {NS}:{w.id}/{b.id}  -  {b.name} ({size[0]}x{size[2]}, {size[1]} high)", "white"))
            manifest.append((w.franchise, w.name, f"{NS}:{w.id}/{b.id}", b.name, size, len(v), len(cmds)))
            print(f"{w.id:16s} {b.id:22s} {len(v):8d} blocks {len(cmds):6d} cmds {size}")
        world_items[w.id] = items
        add_sequence(pack, f"{w.id}/all", layout_rows([items], z_start=0), w.name)

    # ---- technology models
    tech_items: List[Item] = []
    index_lines.append(say("Premodern technology models (see knowledge/README.md)", "yellow", True))
    index_lines.append(say(f"  /function {NS}:hub_tech", "aqua"))
    for mid, fn in MODELS.items():
        v = Voxel()
        fn(v)
        cmds = to_commands(v)
        total_cmds += len(cmds)
        rec = by_model.get(mid)
        head = [say(f"Technology: {rec['name'] if rec else mid}", "gold", True),
                say(TECH_BUILD_NOTES.get(mid, ""), "white")]
        if rec:
            head.append(say(f"{rec['civilization']}, {rec['period']}", "yellow"))
            for para in (rec["summary"], rec["how_it_works"]):
                for line in textwrap.wrap(para, 90):
                    head.append(say(line, "gray"))
            if rec.get("build"):
                head.append(say(f"See it in context: /function {NS}:{rec['build']}", "aqua"))
        raw = f"raw/tech/{mid}"
        pack.add(raw, head + cmds)
        item = Item(f"tech_{mid}", raw, rec["name"] if rec else mid, v.bounds())
        tech_items.append(item)
        add_sequence(pack, f"tech/{mid}", [(item, 0, 0)], item.name)
        size = v.size()
        index_lines.append(say(f"  /function {NS}:tech/{mid}  -  {item.name} ({size[0]}x{size[2]})", "white"))
        manifest.append(("Technology", rec["civilization"] if rec else "", f"{NS}:tech/{mid}", item.name, size, len(v), len(cmds)))
        print(f"{'tech':16s} {mid:22s} {len(v):8d} blocks {len(cmds):6d} cmds {size}")

    # ---- personal notes: every knowledge/my_notes/*.md becomes ac:notes/<slug> (read aloud in chat)
    notes_dir = os.path.join(HERE, "knowledge", "my_notes")
    note_files = sorted(f for f in os.listdir(notes_dir) if f.endswith(".md") and f.lower() != "readme.md")
    if note_files:
        index_lines.append(say("Your notes (knowledge/my_notes)", "yellow", True))
    for fn in note_files:
        slug = os.path.splitext(fn)[0].lower().replace(" ", "_").replace("-", "_")
        slug = "".join(ch for ch in slug if ch.isalnum() or ch == "_")
        with open(os.path.join(notes_dir, fn), encoding="utf-8") as f:
            lines = [ln.rstrip() for ln in f.read().splitlines()]
        cmds = [say(f"Notes: {os.path.splitext(fn)[0]}", "gold", True)]
        for ln in lines:
            if not ln.strip():
                continue
            if ln.startswith("#"):
                cmds.append(say(ln.lstrip("# "), "yellow", True))
            else:
                for piece in textwrap.wrap(ln, 90):
                    cmds.append(say(piece, "white"))
        pack.add(f"notes/{slug}", [c.replace("tellraw @a", "tellraw @s") for c in cmds])
        index_lines.append(say(f"  /function {NS}:notes/{slug}", "white"))

    # ---- hubs
    ac_rows = [world_items[w.id] for w in worlds if w.franchise == "Assassin's Creed"]
    av_rows = [world_items[w.id] for w in worlds if w.franchise == "Avatar"]
    tech_rows = [tech_items[i:i + 8] for i in range(0, len(tech_items), 8)]
    add_sequence(pack, "hub", layout_rows(ac_rows + av_rows + tech_rows), "Everything")
    add_sequence(pack, "hub_assassins_creed", layout_rows(ac_rows), "Assassin's Creed worlds")
    add_sequence(pack, "hub_avatar", layout_rows(av_rows), "Avatar worlds")
    add_sequence(pack, "hub_tech", layout_rows(tech_rows), "Premodern technology")

    # ---- plumbing: sequence runner, load, tick, auto-build, cancel, index
    pack.add("_next", [f"function {NS}:_step with storage {NS}:seq"])
    pack.add("_step", [f"$execute positioned $(x) $(y) $(z) run function {NS}:_s/$(seq)/$(step)"])
    pack.add("_adv", [
        f"execute store result score #seq {NS}_step run data get storage {NS}:seq step",
        f"scoreboard players add #seq {NS}_step 1",
        f"execute store result storage {NS}:seq step int 1 run scoreboard players get #seq {NS}_step",
        f"schedule function {NS}:_next {WAIT_TICKS}t",
    ])
    pack.add("load", [
        f"scoreboard objectives add {NS}_step dummy",
        f"scoreboard objectives add {NS}_flag dummy",
        f"execute unless score #auto {NS}_flag = #auto {NS}_flag run scoreboard players set #auto {NS}_flag 1",
        "gamerule maxCommandChainLength 1000000",
        say("AC Worlds datapack loaded. /function ac:index lists every build; /function ac:hub builds everything.", "gold"),
    ])
    pack.add("tick", [
        f"execute if score #auto {NS}_flag matches 1 if entity @a run function {NS}:_autostart",
    ])
    pack.add("_autostart", [
        f"scoreboard players set #auto {NS}_flag 2",
        say("AC Worlds: auto-build of the full hub starts around the first player in 15 seconds.", "gold", True),
        say("Run /function ac:cancel to stop it, or /function ac:index to pick single builds instead.", "yellow"),
        f"schedule function {NS}:_autobuild 300t",
    ])
    pack.add("_autobuild", [
        f"execute if score #auto {NS}_flag matches 2 as @r at @s run function {NS}:hub",
        f"scoreboard players set #auto {NS}_flag 0",
    ])
    pack.add("cancel", [
        f"schedule clear {NS}:_autobuild",
        f"schedule clear {NS}:_next",
        f"scoreboard players set #auto {NS}_flag 0",
        "forceload remove all",
        say("AC Worlds: build sequence cancelled and chunks released.", "red"),
    ])
    pack.add("reset_auto", [f"scoreboard players set #auto {NS}_flag 1", say("Auto-build re-armed for the next player join.", "gold")])
    pack.add("index", [c.replace("tellraw @a", "tellraw @s") for c in index_lines])
    pack.add("help", [
        say("AC Worlds quick help", "gold", True),
        say("/function ac:index - list every world, landmark and technology model", "white"),
        say("/function ac:<world>/<build> - build one landmark where you stand (e.g. ac:egypt/giza)", "white"),
        say("/function ac:<world>/all - a whole world in a row; ac:hub - everything", "white"),
        say("/function ac:cancel - stop a running sequence; ac:reset_auto - re-arm the first-join auto-build", "white"),
        say("Builds place relative to your feet: stand on flat ground, face north (-z) for the 'front'.", "gray"),
    ])
    # the tick tag
    pack.write(args.out)
    tagdir = os.path.join(args.out, "data", "minecraft", "tags", "function")
    with open(os.path.join(tagdir, "tick.json"), "w", encoding="utf-8") as f:
        json.dump({"values": [f"{NS}:tick"]}, f, indent=2)
    write_zip(args.out, args.out + ".zip")

    # ---- INDEX.md next to the datapack
    with open(os.path.join(HERE, "datapack", "INDEX.md"), "w", encoding="utf-8") as f:
        f.write("# AC Worlds datapack - function index\n\n")
        f.write("Generated by `python generate.py`. Run any function as a player: `/function <name>`.\n\n")
        f.write("| Franchise | World | Function | Build | Footprint (x by z, height) | Blocks | Commands |\n|---|---|---|---|---|---|---|\n")
        for fr, wn, fn, bn, size, nblocks, ncmds in manifest:
            f.write(f"| {fr} | {wn} | `{fn}` | {bn} | {size[0]} x {size[2]}, {size[1]} | {nblocks:,} | {ncmds:,} |\n")
        f.write(f"\nTotal placement commands: {total_cmds:,}\n")

    # ---- knowledge catalogue
    write_catalogue(records)
    print(f"\nwrote {args.out}  ({len(pack.functions)} functions, {total_cmds:,} placement commands)")


def write_zip(folder: str, zip_path: str) -> None:
    """Zip the datapack so pack.mcmeta sits at the ROOT of the archive.

    Minecraft only recognises a zipped datapack when pack.mcmeta is at the top
    level; a zip that wraps everything in an ``ac_worlds/`` folder is silently
    ignored (no chat message, no builds).  So we never use ``zip -r`` on the
    folder itself; we add each file with a path relative to the folder.
    """
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for dirpath, dirnames, filenames in os.walk(folder):
            dirnames.sort()
            for fn in sorted(filenames):
                full = os.path.join(dirpath, fn)
                zf.write(full, os.path.relpath(full, folder).replace(os.sep, "/"))


def write_catalogue(records: List[dict]) -> None:
    path = os.path.join(HERE, "knowledge", "README.md")
    civs: Dict[str, List[dict]] = {}
    for r in records:
        civs.setdefault(r["civilization"], []).append(r)
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Premodern technology catalogue\n\n")
        f.write("Generated from `premodern_technology.json` by `python generate.py`. ")
        f.write(f"{len(records)} records. Each entry names the Minecraft function that shows it in context "
                "(`build`) and, where one exists, the small working-principle model (`/function ac:tech/<id>`).\n\n")
        f.write("## Contents\n\n")
        for civ, rs in civs.items():
            f.write(f"- **{civ}**: " + ", ".join(f"[{r['name']}](#{r['id']})" for r in rs) + "\n")
        f.write("\n")
        for civ, rs in civs.items():
            f.write(f"## {civ}\n\n")
            for r in rs:
                f.write(f"<a id=\"{r['id']}\"></a>\n### {r['name']}\n\n")
                f.write(f"*{r['region']} - {r['period']} - {r['category']}*\n\n")
                f.write(f"{r['summary']}\n\n**How it works.** {r['how_it_works']}\n\n**Why it matters.** {r['significance']}\n\n")
                f.write(f"**In the games.** {r['ac_connection']}\n\n")
                mc = []
                if r.get("build"):
                    mc.append(f"`/function ac:{r['build']}` (landmark)")
                if r.get("tech_model"):
                    mc.append(f"`/function ac:tech/{r['tech_model']}` (model)")
                if mc:
                    f.write("**In Minecraft.** " + "; ".join(mc) + "\n\n")
                f.write("**Sources.** " + "; ".join(r["sources"]) + "\n\n")


if __name__ == "__main__":
    main()
