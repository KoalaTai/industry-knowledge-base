#!/usr/bin/env python3
"""Replay ac:hub on the server from the console, step by step, over RCON.

The player-facing ac:hub needs a player for @s; the console does not have
one.  This script reads the generated step functions ac:_s/hub/<n>, turns
their relative coordinates into absolute ones around ORIGIN, force-loads
each step's area, waits until it is loaded, runs the placement, releases
the chunks and moves on.  At the end it points storage ac:hub at ORIGIN so
ac:goto / ac:overview / ac:tour work for players on the server.

    python3 replay_hub.py [X Y Z]        # default origin 4000 -60 0

Progress goes to stdout; safe to re-run (placing twice is idempotent).
"""

from __future__ import annotations

import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import server  # noqa: E402

STEPS = Path(__file__).resolve().parents[1] / "datapack" / "ac_worlds" / "data" / "ac" / "function" / "_s" / "hub"
REL = re.compile(r"~(-?\d*)")


def rel(tok: str, base: int) -> int:
    return base + (int(tok) if tok else 0)


def main() -> None:
    ox, oy, oz = (int(a) for a in sys.argv[1:4]) if len(sys.argv) >= 4 else (4000, -60, 0)
    r = server.rcon()
    files = sorted(STEPS.glob("*.mcfunction"), key=lambda p: int(p.stem))
    t0 = time.time()
    placed = 0
    for f in files:
        lines = f.read_text().splitlines()
        loads = [ln for ln in lines if ln.startswith("forceload add")]
        runs = [ln for ln in lines if ln.startswith("execute positioned") and "run function ac:" in ln]
        if not runs:
            continue                                    # chunk-loading step or the "done" step
        # the matching forceload rectangles live in the previous step file
        prev = STEPS / f"{int(f.stem) - 1}.mcfunction"
        if prev.exists():
            loads = [ln for ln in prev.read_text().splitlines() if ln.startswith("forceload add")]
        rects = []
        for ln in loads:
            a = REL.findall(ln)
            rects.append((rel(a[0], ox), rel(a[1], oz), rel(a[2], ox), rel(a[3], oz)))
            r.command(f"forceload add {rects[-1][0]} {rects[-1][1]} {rects[-1][2]} {rects[-1][3]}")
        # wait for the corners of every rectangle
        deadline = time.time() + 30
        corners = [(x, z) for x1, z1, x2, z2 in rects for x, z in ((x1, z1), (x2, z1), (x1, z2), (x2, z2))]
        while time.time() < deadline:
            if all("passed" in r.command(f"execute if loaded {x} {oy} {z}").lower() for x, z in corners):
                break
            time.sleep(0.5)
        for ln in runs:
            m = re.match(r"execute positioned (\S+) (\S+) (\S+) run function (ac:\S+)", ln)
            px, py, pz, fn = m.groups()
            x, y, z = rel(px.lstrip("~"), ox), rel(py.lstrip("~"), oy), rel(pz.lstrip("~"), oz)
            out = r.command(f"execute positioned {x} {y} {z} run function {fn}")
            placed += 1
            print(f"[{int(time.time() - t0):4d}s] step {f.stem:>3} {fn} @ {x} {y} {z}: {out.strip()[:60]}", flush=True)
        for x1, z1, x2, z2 in rects:
            r.command(f"forceload remove {x1} {z1} {x2} {z2}")
    for k, v in (("x", ox), ("y", oy), ("z", oz)):
        r.command(f"data modify storage ac:hub {k} set value {v}")
    r.command("save-all")
    print(f"done: {placed} placements in {int(time.time() - t0)}s; storage ac:hub = {ox} {oy} {oz}")


if __name__ == "__main__":
    main()
