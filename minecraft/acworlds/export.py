"""Turn a Voxel into vanilla ``/fill`` commands and write a datapack.

Greedy meshing: runs along x are merged into rectangles across z, then
into boxes across y, so a 101x101 pyramid layer is a single ``fill``.
Air is emitted last so carved rooms stay carved.
"""

from __future__ import annotations

import json
import os
from collections import defaultdict
from typing import Dict, List, Tuple

from .voxel import AIR, Voxel

FILL_LIMIT = 32768          # vanilla /fill volume limit
Box = Tuple[int, int, int, int, int, int, str]

# Blocks that need a support / neighbour and must be placed after solids.
_LATE = ("torch", "wall_torch", "lantern", "chain", "ladder", "vine", "water",
         "lava", "sugar_cane", "cactus", "dead_bush", "glass_pane", "iron_bars",
         "campfire", "bell", "lectern", "rail", "_fence", "carpet", "_sign",
         "scaffolding", "flower", "grass", "fern", "wheat", "banner", "leaves")


def _phase(block: str) -> int:
    if block == AIR:
        return 2
    base = block.split("[", 1)[0]
    return 1 if any(k in base for k in _LATE) else 0


def mesh(v: Voxel) -> List[Box]:
    by_block: Dict[str, List[Tuple[int, int, int]]] = defaultdict(list)
    for c, b in v.blocks.items():
        by_block[b].append(c)

    boxes: List[Box] = []
    for block, coords in by_block.items():
        # 1. runs along x for each (y, z)
        rows: Dict[Tuple[int, int], List[int]] = defaultdict(list)
        for x, y, z in coords:
            rows[(y, z)].append(x)
        runs: Dict[Tuple[int, int, int], List[int]] = defaultdict(list)  # (y,x1,x2) -> zs
        for (y, z), xs in rows.items():
            xs.sort()
            start = prev = xs[0]
            for x in xs[1:]:
                if x == prev + 1:
                    prev = x
                else:
                    runs[(y, start, prev)].append(z)
                    start = prev = x
            runs[(y, start, prev)].append(z)
        # 2. merge runs across z
        rects: Dict[Tuple[int, int, int, int], List[int]] = defaultdict(list)  # (x1,x2,z1,z2)->ys
        for (y, x1, x2), zs in runs.items():
            zs.sort()
            start = prev = zs[0]
            for z in zs[1:]:
                if z == prev + 1:
                    prev = z
                else:
                    rects[(x1, x2, start, prev)].append(y)
                    start = prev = z
            rects[(x1, x2, start, prev)].append(y)
        # 3. merge rectangles across y
        for (x1, x2, z1, z2), ys in rects.items():
            ys.sort()
            start = prev = ys[0]
            for y in ys[1:]:
                if y == prev + 1:
                    prev = y
                else:
                    boxes.append((x1, start, z1, x2, prev, z2, block))
                    start = prev = y
            boxes.append((x1, start, z1, x2, prev, z2, block))

    # split anything over the /fill limit along its longest axis
    out: List[Box] = []
    stack = boxes
    while stack:
        x1, y1, z1, x2, y2, z2, b = stack.pop()
        vol = (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)
        if vol <= FILL_LIMIT:
            out.append((x1, y1, z1, x2, y2, z2, b))
            continue
        dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
        if dx >= dy and dx >= dz:
            m = (x1 + x2) // 2
            stack += [(x1, y1, z1, m, y2, z2, b), (m + 1, y1, z1, x2, y2, z2, b)]
        elif dz >= dy:
            m = (z1 + z2) // 2
            stack += [(x1, y1, z1, x2, y2, m, b), (x1, y1, m + 1, x2, y2, z2, b)]
        else:
            m = (y1 + y2) // 2
            stack += [(x1, y1, z1, x2, m, z2, b), (x1, m + 1, z1, x2, y2, z2, b)]

    out.sort(key=lambda bx: (_phase(bx[6]), bx[1], bx[2], bx[0]))
    return out


def _rel(n: int) -> str:
    return "~" if n == 0 else f"~{n}"


def to_commands(v: Voxel) -> List[str]:
    cmds = []
    for x1, y1, z1, x2, y2, z2, b in mesh(v):
        if (x1, y1, z1) == (x2, y2, z2):
            cmds.append(f"setblock {_rel(x1)} {_rel(y1)} {_rel(z1)} {b}")
        else:
            cmds.append(f"fill {_rel(x1)} {_rel(y1)} {_rel(z1)} {_rel(x2)} {_rel(y2)} {_rel(z2)} {b}")
    return cmds


def tellraw(text: str, color: str = "gold", bold: bool = False) -> str:
    comp = {"text": text, "color": color}
    if bold:
        comp["bold"] = True
    return "tellraw @s " + json.dumps(comp, ensure_ascii=False)


class Datapack:
    """Collects mcfunction files and writes the folder structure."""

    def __init__(self, namespace: str = "ac", description: str = "") -> None:
        self.namespace = namespace
        self.description = description
        self.functions: Dict[str, List[str]] = {}
        self.structures: Dict[str, dict] = {}   # name -> template NBT (see structure.py)

    def add(self, name: str, commands: List[str]) -> None:
        self.functions[name] = commands

    def add_structure(self, name: str, nbt: dict) -> None:
        """Register a structure template, placed in game as ``<ns>:<name>``."""
        self.structures[name] = nbt

    def write(self, root: str) -> None:
        from .structure import write_template  # local import: structure.py imports this module

        os.makedirs(root, exist_ok=True)
        meta = {
            "pack": {
                # 1.21.0 - 1.21.8 read pack_format / supported_formats;
                # 1.21.9+ (format 82) and the 26.x releases read min_format /
                # max_format instead.  Both sets are allowed together as long
                # as the pack claims support below format 82, which it does.
                "pack_format": 48,
                "supported_formats": {"min_inclusive": 48, "max_inclusive": 999},
                "min_format": 48,
                "max_format": 999,
                "description": self.description,
            }
        }
        with open(os.path.join(root, "pack.mcmeta"), "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)
        fdir = os.path.join(root, "data", self.namespace, "function")
        for name, cmds in self.functions.items():
            path = os.path.join(fdir, *name.split("/")) + ".mcfunction"
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(cmds) + "\n")
        sdir = os.path.join(root, "data", self.namespace, "structure")
        for name, nbt in self.structures.items():
            path = os.path.join(sdir, *name.split("/")) + ".nbt"
            os.makedirs(os.path.dirname(path), exist_ok=True)
            write_template(path, nbt)
        # run `load` once when the pack is (re)loaded
        tagdir = os.path.join(root, "data", "minecraft", "tags", "function")
        os.makedirs(tagdir, exist_ok=True)
        with open(os.path.join(tagdir, "load.json"), "w", encoding="utf-8") as f:
            json.dump({"values": [f"{self.namespace}:load"]}, f, indent=2)
