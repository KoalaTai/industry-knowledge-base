"""Reusable architecture generators.

Every function draws into a Voxel with the ground at y = 0 (the plinth
layer).  Structures rise from y = 1.  ``p`` is a palette dict.
"""

from __future__ import annotations

import math
import random
from typing import Optional, Tuple

from .palettes import Palette
from .voxel import Voxel

# --------------------------------------------------------------- ground

def pad(v: Voxel, x1: int, z1: int, x2: int, z2: int, block: str, y: int = 0) -> None:
    v.fill(x1, y, z1, x2, y, z2, block)


def plaza(v: Voxel, x1: int, z1: int, x2: int, z2: int, p: Palette,
          fountain: bool = True) -> None:
    pad(v, x1, z1, x2, z2, p["floor"])
    if fountain:
        cx, cz = (x1 + x2) // 2, (z1 + z2) // 2
        v.disc(cx, 1, cz, 3, p["trim"], hollow=True)
        v.disc(cx, 1, cz, 2, "water")
        v.column(cx, 1, cz, 3, p["trim"])
        v.set(cx, 4, cz, "water")


def road(v: Voxel, x1: int, z1: int, x2: int, z2: int, block: str) -> None:
    pad(v, x1, z1, x2, z2, block)


def garden(v: Voxel, x1: int, z1: int, x2: int, z2: int, p: Palette,
           trees: int = 4, seed: int = 1) -> None:
    pad(v, x1, z1, x2, z2, "grass_block")
    rng = random.Random(seed)
    for _ in range(trees):
        x = rng.randint(x1 + 2, x2 - 2)
        z = rng.randint(z1 + 2, z2 - 2)
        v.tree(x, 1, z, p["log"], p["leaves"], height=rng.randint(4, 6))


# --------------------------------------------------------------- buildings

def house(v: Voxel, x: int, z: int, w: int, d: int, p: Palette, floors: int = 2,
          roof: str = "gable", floor_h: int = 4, wall: Optional[str] = None,
          ridge: str = "x", windows: bool = True) -> int:
    """Simple multi-storey house.  Returns the top y."""
    wall = wall or p["wall"]
    x2, z2 = x + w - 1, z + d - 1
    h = floors * floor_h
    v.walls(x, 1, z, x2, h, z2, wall)
    v.fill(x + 1, 1, z + 1, x2 - 1, h, z2 - 1, "air")
    for f in range(floors):
        y0 = 1 + f * floor_h
        if f > 0:
            v.fill(x + 1, y0 - 1, z + 1, x2 - 1, y0 - 1, z2 - 1, p["floor"])
        if windows:
            v.windows(x, y0 + 1, z, x2, z2, p["window"], period=3, offset=2)
            v.windows(x, y0 + 2, z, x2, z2, p["window"], period=3, offset=2)
    # door on the south face
    v.set(x + w // 2, 1, z2, "air")
    v.set(x + w // 2, 2, z2, "air")
    v.fill(x, 1, z, x2, 1, z2, p["floor"])
    if roof == "gable":
        top = v.gable_roof(x, h + 1, z, x2, z2, p["roof"], ridge_axis=ridge)
    elif roof == "hip":
        top = v.hip_roof(x, h + 1, z, x2, z2, p["roof"])
    elif roof == "flat":
        v.fill(x, h + 1, z, x2, h + 1, z2, p["roof"])
        v.crenellate(x, h + 2, z, x2, z2, p["trim"], period=2)
        top = h + 2
    else:  # dome
        v.fill(x, h + 1, z, x2, h + 1, z2, p["roof"])
        r = min(w, d) // 2
        v.dome((x + x2) // 2, h + 1, (z + z2) // 2, r - 0.5, p["roof"])
        top = h + 1 + r
    return top


def timber_house(v: Voxel, x: int, z: int, w: int, d: int, p: Palette, floors: int = 2) -> int:
    """Half-timbered: plaster walls with log frame, jettied upper floor."""
    top = house(v, x, z, w, d, p, floors=floors, roof="gable", floor_h=4)
    x2, z2 = x + w - 1, z + d - 1
    for f in range(floors):
        y0 = 1 + f * 4
        for px in (x, x2):
            for pz in (z, z2):
                v.column(px, y0, pz, 4, p["trim"])
        v.walls(x, y0 + 3, z, x2, y0 + 3, z2, p["trim"])
    return top


def tower(v: Voxel, cx: int, cz: int, r: float, h: int, p: Palette, top: str = "crenel",
          wall: Optional[str] = None, square: bool = False) -> int:
    wall = wall or p["wall"]
    if square:
        ri = int(r)
        v.walls(cx - ri, 1, cz - ri, cx + ri, h, cz + ri, wall)
        v.fill(cx - ri + 1, 1, cz - ri + 1, cx + ri - 1, h, cz + ri - 1, "air")
        v.fill(cx - ri, h, cz - ri, cx + ri, h, cz + ri, p["floor"])
    else:
        v.cylinder(cx, 1, cz, r, h, wall, hollow=True)
        v.disc(cx, h, cz, r, p["floor"])
    top_y = h
    if top == "crenel":
        if square:
            v.crenellate(cx - int(r), h + 1, cz - int(r), cx + int(r), cz + int(r), wall)
        else:
            for a in range(0, 360, 30):
                v.set(round(cx + r * math.cos(math.radians(a))), h + 1,
                      round(cz + r * math.sin(math.radians(a))), wall)
        top_y = h + 1
    elif top == "cone":
        ch = int(r * 2) + 2
        v.cone(cx, h + 1, cz, r + 1, ch, p["roof"])
        top_y = h + ch
    elif top == "dome":
        v.dome(cx, h, cz, r, p["roof"])
        top_y = h + int(r)
    elif top == "pyramid":
        ph = int(r) + 2
        v.pyramid(cx, h + 1, cz, int(r * 2) + 2, ph, p["roof"])
        top_y = h + ph
    return top_y


def curtain_wall(v: Voxel, x1: int, z1: int, x2: int, z2: int, h: int, p: Palette,
                 towers: bool = True, gate: str = "south", thickness: int = 2,
                 tower_r: float = 3) -> None:
    wall = p["wall"]
    for t in range(thickness):
        v.walls(x1 + t, 1, z1 + t, x2 - t, h, z2 - t, wall)
    v.walls(x1, h + 1, z1, x2, h + 1, z2, wall)             # parapet
    v.crenellate(x1, h + 2, z1, x2, z2, wall)
    if towers:
        for px in (x1, x2):
            for pz in (z1, z2):
                tower(v, px, pz, tower_r, h + 4, p)
    # gate
    cx, cz = (x1 + x2) // 2, (z1 + z2) // 2
    if gate == "south":
        v.fill(cx - 1, 1, z2 - thickness + 1, cx + 1, 4, z2, "air")
        tower(v, cx - 4, z2, tower_r, h + 5, p)
        tower(v, cx + 4, z2, tower_r, h + 5, p)
    elif gate == "north":
        v.fill(cx - 1, 1, z1, cx + 1, 4, z1 + thickness - 1, "air")
    elif gate == "east":
        v.fill(x2 - thickness + 1, 1, cz - 1, x2, 4, cz + 1, "air")
    elif gate == "west":
        v.fill(x1, 1, cz - 1, x1 + thickness - 1, 4, cz + 1, "air")


def keep(v: Voxel, cx: int, cz: int, half: int, h: int, p: Palette) -> None:
    """Square great tower with four corner turrets."""
    v.fill(cx - half, 1, cz - half, cx + half, h, cz + half, p["wall"])
    v.fill(cx - half + 1, 2, cz - half + 1, cx + half - 1, h - 1, cz + half - 1, "air")
    for f in range(2, h - 1, 5):
        v.fill(cx - half + 1, f, cz - half + 1, cx + half - 1, f, cz + half - 1, p["floor"])
        v.windows(cx - half, f + 2, cz - half, cx + half, cz + half, p["window"], period=4, offset=2)
    v.crenellate(cx - half, h + 1, cz - half, cx + half, cz + half, p["wall"])
    for px in (cx - half, cx + half):
        for pz in (cz - half, cz + half):
            tower(v, px, pz, 2, h + 3, p, top="cone")
    v.fill(cx - 1, 1, cz + half, cx + 1, 3, cz + half, "air")


def greek_temple(v: Voxel, cx: int, cz: int, p: Palette, cols_long: int = 8,
                 cols_short: int = 6, spacing: int = 3, col_h: int = 9,
                 axis: str = "x") -> None:
    """Peripteral temple on a three-step crepidoma."""
    lx = (cols_long - 1) * spacing
    lz = (cols_short - 1) * spacing
    if axis == "z":
        lx, lz = lz, lx
        cols_long, cols_short = cols_short, cols_long
    hx, hz = lx // 2, lz // 2
    for s in range(3):
        v.fill(cx - hx - 4 + s, 1 + s, cz - hz - 4 + s, cx + hx + 4 - s, 1 + s, cz + hz + 4 - s, p["floor"])
    y0 = 4
    for i in range(cols_long):
        for j in range(cols_short):
            if i in (0, cols_long - 1) or j in (0, cols_short - 1):
                x = cx - hx + i * spacing
                z = cz - hz + j * spacing
                v.column(x, y0, z, col_h, p["column"])
                v.set(x, y0 + col_h, z, p["trim"])
    # cella
    v.walls(cx - hx + spacing, y0, cz - hz + spacing, cx + hx - spacing, y0 + col_h, cz + hz - spacing, p["wall"])
    v.fill(cx - hx + spacing + 1, y0, cz - hz + spacing + 1, cx + hx - spacing - 1, y0 + col_h, cz + hz - spacing - 1, "air")
    v.fill(cx - hx + spacing + 1, y0 - 1, cz - hz + spacing + 1, cx + hx - spacing - 1, y0 - 1, cz + hz - spacing - 1, p["floor"])
    door_x = cx - hx + spacing if axis == "x" else cx
    door_z = cz if axis == "x" else cz - hz + spacing
    v.fill(door_x, y0, door_z - 1, door_x, y0 + 3, door_z + 1, "air") if axis == "x" else \
        v.fill(door_x - 1, y0, door_z, door_x + 1, y0 + 3, door_z, "air")
    # entablature + pediment roof
    yt = y0 + col_h + 1
    v.fill(cx - hx - 1, yt, cz - hz - 1, cx + hx + 1, yt + 1, cz + hz + 1, p["wall2"])
    v.gable_roof(cx - hx - 1, yt + 2, cz - hz - 1, cx + hx + 1, cz + hz + 1, p["roof"],
                 ridge_axis=axis, overhang=1)


def egyptian_temple(v: Voxel, x: int, z: int, p: Palette, width: int = 31, length: int = 60) -> None:
    """Pylon gateway, open court, hypostyle hall, sanctuary (north to south = +z)."""
    x2 = x + width - 1
    cx = (x + x2) // 2
    pad(v, x - 6, z - 20, x2 + 6, z + length + 4, p["path"])
    # processional way with sphinxes
    for i in range(z - 18, z - 2, 4):
        for px in (cx - 5, cx + 5):
            v.fill(px, 1, i, px, 1, i + 1, p["wall2"])
            v.set(px, 2, i, p["trim"])
    # obelisks
    for px in (cx - 7, cx + 7):
        obelisk(v, px, z - 3, 14, p["wall2"])
    # pylon: two tapered towers with gate between
    ph = 16
    for side in (-1, 1):
        for k in range(ph):
            shrink = k // 4
            if side < 0:
                v.fill(x + shrink, 1 + k, z, cx - 3, 1 + k, z + 5 - shrink, p["wall"])
            else:
                v.fill(cx + 3, 1 + k, z, x2 - shrink, 1 + k, z + 5 - shrink, p["wall"])
    v.fill(cx - 2, 1, z, cx + 2, 8, z + 5, p["wall"])
    v.fill(cx - 1, 1, z, cx + 1, 6, z + 5, "air")
    # open court with colonnade
    cz1, cz2 = z + 6, z + 26
    v.walls(x, 1, cz1, x2, 8, cz2, p["wall"])
    v.fill(x + 1, 1, cz1 + 1, x2 - 1, 8, cz2 - 1, "air")
    v.fill(cx - 1, 1, cz1, cx + 1, 6, cz1, "air")
    v.fill(cx - 1, 1, cz2, cx + 1, 6, cz2, "air")
    for i in range(cz1 + 3, cz2 - 2, 3):
        for px in (x + 3, x2 - 3):
            v.column(px, 1, i, 7, p["column"])
            v.set(px, 8, i, p["trim"])
    # hypostyle hall: forest of columns under a roof
    hz1, hz2 = cz2 + 1, cz2 + 18
    v.walls(x, 1, hz1, x2, 10, hz2, p["wall"])
    v.fill(x + 1, 1, hz1 + 1, x2 - 1, 10, hz2 - 1, "air")
    v.fill(x, 11, hz1, x2, 11, hz2, p["wall"])
    v.fill(cx - 1, 1, hz1, cx + 1, 5, hz1, "air")
    v.fill(cx - 1, 1, hz2, cx + 1, 4, hz2, "air")
    for i in range(hz1 + 3, hz2 - 2, 4):
        for px in range(x + 3, x2 - 2, 4):
            if abs(px - cx) <= 2:
                continue
            v.column(px, 1, i, 10, p["column"])
            v.set(px, 10, i, p["trim"])
    # sanctuary
    sz1, sz2 = hz2 + 1, z + length - 1
    v.fill(x + 4, 1, sz1, x2 - 4, 8, sz2, p["wall"])
    v.fill(x + 5, 1, sz1 + 1, x2 - 5, 7, sz2 - 1, "air")
    v.fill(cx - 1, 1, sz1, cx + 1, 3, sz1, "air")
    v.fill(cx - 1, 1, sz2 - 2, cx + 1, 2, sz2 - 2, "gold_block")  # shrine


def obelisk(v: Voxel, x: int, z: int, h: int, block: str) -> None:
    v.fill(x - 1, 1, z - 1, x + 1, 1, z + 1, block)
    v.column(x, 2, z, h - 3, block)
    v.set(x, h - 1, z, block)
    v.set(x, h, z, "gold_block")


def mosque(v: Voxel, cx: int, cz: int, p: Palette, half: int = 14, dome_r: float = 8,
           minarets: int = 2, minaret_h: int = 34) -> None:
    v.fill(cx - half, 1, cz - half, cx + half, 10, cz + half, p["wall"])
    v.fill(cx - half + 1, 1, cz - half + 1, cx + half - 1, 9, cz + half - 1, "air")
    v.fill(cx - half + 1, 1, cz - half + 1, cx + half - 1, 1, cz + half - 1, p["floor"])
    v.windows(cx - half, 4, cz - half, cx + half, cz + half, p["window"], period=3, offset=2)
    v.windows(cx - half, 5, cz - half, cx + half, cz + half, p["window"], period=3, offset=2)
    v.fill(cx - 2, 1, cz + half, cx + 2, 5, cz + half, "air")
    # drum + dome + half domes
    v.cylinder(cx, 11, cz, dome_r, 3, p["wall2"], hollow=True)
    v.disc(cx, 11, cz, dome_r - 1, "air")
    v.dome(cx, 13, cz, dome_r, p["roof"])
    v.set(cx, 13 + int(dome_r) + 1, cz, "gold_block")
    for dx, dz in ((half - 5, 0), (-(half - 5), 0), (0, half - 5), (0, -(half - 5))):
        v.dome(cx + dx, 10, cz + dz, dome_r / 2, p["roof"])
    # courtyard with ablution fountain
    v.walls(cx - half, 1, cz + half + 1, cx + half, 4, cz + half + 2 * half, p["wall"])
    v.fill(cx - half + 1, 1, cz + half + 2, cx + half - 1, 4, cz + half + 2 * half - 1, "air")
    v.fill(cx - half + 1, 1, cz + half + 2, cx + half - 1, 1, cz + half + 2 * half - 1, p["floor"])
    v.fill(cx - 2, 1, cz + half + 2 * half, cx + 2, 4, cz + half + 2 * half, "air")
    v.disc(cx, 1, cz + half + half, 2, "water")
    v.disc(cx, 1, cz + half + half, 3, p["trim"], hollow=True)
    pos = [(cx - half, cz - half), (cx + half, cz - half), (cx - half, cz + 2 * half),
           (cx + half, cz + 2 * half)]
    for mx, mz in pos[:minarets]:
        minaret(v, mx, mz, minaret_h, p)


def minaret(v: Voxel, x: int, z: int, h: int, p: Palette) -> None:
    v.cylinder(x, 1, z, 2, h, p["column"], hollow=False)
    v.disc(x, h * 2 // 3, z, 3, p["trim"])
    v.disc(x, h, z, 3, p["trim"])
    v.cone(x, h + 1, z, 2.5, 6, p["roof"])
    v.set(x, h + 7, z, "gold_block")


def gothic_church(v: Voxel, cx: int, z: int, p: Palette, length: int = 60, width: int = 21,
                  towers: bool = True, nave_h: int = 24, tower_h: int = 44) -> None:
    """West front at z, nave running +z.  Flying buttresses, rose window, apse."""
    half = width // 2
    x1, x2 = cx - half, cx + half
    z2 = z + length
    v.fill(x1, 1, z, x2, nave_h, z2, p["wall"])
    v.fill(x1 + 1, 1, z + 1, x2 - 1, nave_h - 1, z2 - 1, "air")
    v.fill(x1 + 1, 1, z + 1, x2 - 1, 1, z2 - 1, p["floor"])
    # tall lancet windows
    for zz in range(z + 4, z2 - 4, 4):
        for px in (x1, x2):
            v.fill(px, 6, zz, px, nave_h - 6, zz, "blue_stained_glass_pane")
            v.fill(px, 8, zz, px, nave_h - 8, zz, "red_stained_glass_pane")
    # flying buttresses
    for zz in range(z + 6, z2 - 4, 8):
        for side in (-1, 1):
            bx = x2 + 1 if side > 0 else x1 - 1
            v.fill(bx + side * 3, 1, zz, bx + side * 4, nave_h - 6, zz, p["wall2"])
            v.line((bx + side * 3, nave_h - 6, zz), (bx, nave_h - 1, zz), p["wall2"])
            v.set(bx + side * 3, nave_h - 5, zz, p["trim"])
            v.set(bx + side * 3, nave_h - 4, zz, p["trim"])
    # roof
    v.gable_roof(x1, nave_h + 1, z, x2, z2, p["roof"], ridge_axis="z", overhang=1)
    # apse
    v.cylinder(cx, 1, z2, half - 2, nave_h - 4, p["wall"], hollow=True)
    v.disc(cx, 1, z2, half - 3, p["floor"])
    v.dome(cx, nave_h - 4, z2, half - 2, p["roof"])
    v.fill(cx - half + 3, 1, z2, cx + half - 3, nave_h - 5, z2, "air")
    # west front: rose window + great door
    v.fill(cx - 2, 1, z, cx + 2, 7, z, "air")
    v.disc(cx, nave_h - 8, z, 4, "purple_stained_glass_pane")
    for y in range(nave_h - 12, nave_h - 4):
        for x in range(cx - 4, cx + 5):
            d = math.hypot(x - cx, y - (nave_h - 8))
            if d <= 4.5:
                v.set(x, y, z, "purple_stained_glass_pane" if int(d) % 2 else "yellow_stained_glass_pane")
    if towers:
        for tx in (x1 - 3, x2 + 3):
            tower(v, tx, z + 3, 4, tower_h, p, top="crenel", square=True)
    # spire over the crossing
    v.cone(cx, nave_h + half, z + length // 2, 3, 18, p["trim"])


def basilica(v: Voxel, cx: int, z: int, p: Palette, length: int = 50, width: int = 25, h: int = 16) -> None:
    """Roman / early Christian basilica: high nave, low aisles, apse."""
    half = width // 2
    nave = half // 2
    v.fill(cx - half, 1, z, cx + half, h // 2, z + length, p["wall"])
    v.fill(cx - half + 1, 1, z + 1, cx + half - 1, h // 2, z + length - 1, "air")
    v.fill(cx - nave, 1, z, cx + nave, h, z + length, p["wall"])
    v.fill(cx - nave + 1, 1, z + 1, cx + nave - 1, h - 1, z + length - 1, "air")
    for zz in range(z + 3, z + length - 2, 4):
        for px in (cx - nave, cx + nave):
            v.fill(px, 1, zz, px, h // 2 - 1, zz, "air")
            v.fill(px, h // 2 + 2, zz, px, h - 3, zz, p["window"])
    v.fill(cx - half, 1, z, cx + half, 1, z + length, p["floor"])
    v.gable_roof(cx - nave, h + 1, z, cx + nave, z + length, p["roof"], ridge_axis="z")
    for side in (-1, 1):
        a = cx + side * nave
        b = cx + side * half
        v.fill(min(a, b), h // 2 + 1, z, max(a, b), h // 2 + 1, z + length, p["roof"])
    v.cylinder(cx, 1, z + length, nave - 1, h - 2, p["wall"], hollow=True)
    v.dome(cx, h - 2, z + length, nave - 1, p["roof"])
    v.fill(cx - nave + 2, 1, z + length, cx + nave - 2, h - 3, z + length, "air")
    v.fill(cx - 2, 1, z, cx + 2, 5, z, "air")


def colosseum(v: Voxel, cx: int, cz: int, p: Palette, rx: float = 44, rz: float = 36,
              tiers: int = 3, tier_h: int = 8) -> None:
    """Elliptical amphitheatre: arcaded tiers outside, stepped seating inside."""
    for t in range(tiers):
        y0 = 1 + t * tier_h
        r1, r2 = rx - t * 0.0, rz - t * 0.0
        v.cylinder(cx, y0, cz, r1, tier_h, p["wall"], hollow=True, rz=r2)
        v.cylinder(cx, y0, cz, r1 - 1, tier_h, p["wall"], hollow=True, rz=r2 - 1)
        # arches: punch openings around the ring
        for a in range(0, 360, 9):
            ax = round(cx + r1 * math.cos(math.radians(a)))
            az = round(cz + r2 * math.sin(math.radians(a)))
            for dx in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for y in range(y0 + 1, y0 + tier_h - 2):
                        if (ax + dx, y, az + dz) in v.blocks:
                            v.set(ax + dx, y, az + dz, "air")
        v.disc(cx, y0 + tier_h - 1, cz, r1, p["floor"], rz=r2)
        v.disc(cx, y0 + tier_h - 1, cz, r1 - 2, "air", rz=r2 - 2)
    # attic
    v.cylinder(cx, 1 + tiers * tier_h, cz, rx, 4, p["wall2"], hollow=True, rz=rz)
    # seating bowl: stepped rings
    steps = int(min(rx, rz) - 8)
    for i in range(steps):
        r = rx - 3 - i
        rr = rz - 3 - i
        y = 1 + tiers * tier_h - 1 - int(i * (tiers * tier_h - 2) / steps)
        if rr < 8:
            break
        v.cylinder(cx, 1, cz, r, max(1, y), p["wall2"], hollow=True, rz=rr)
    # arena floor and hypogeum
    v.disc(cx, 1, cz, rx - 3 - steps, "sand", rz=rz - 3 - steps)
    v.disc(cx, 0, cz, rx - 3 - steps, p["floor"], rz=rz - 3 - steps)


def pantheon(v: Voxel, cx: int, cz: int, p: Palette, r: float = 16) -> None:
    """Rotunda with coffered dome and oculus, pedimented portico to the south."""
    h = int(r)
    v.cylinder(cx, 1, cz, r, h, p["wall"], hollow=True)
    v.cylinder(cx, 1, cz, r - 1, h, p["wall"], hollow=True)
    v.disc(cx, 1, cz, r - 2, p["floor"])
    v.dome(cx, h, cz, r, p["wall"])
    v.dome(cx, h, cz, r - 1, p["wall2"])
    v.disc(cx, h + int(r), cz, 2.5, "air")
    v.disc(cx, h + int(r) - 1, cz, 2.5, "air")
    # portico
    pz = cz + int(r)
    v.fill(cx - 10, 1, pz, cx + 10, 1, pz + 12, p["floor"])
    for i in range(0, 21, 4):
        for j in (1, 11):
            v.column(cx - 10 + i, 2, pz + j, 10, p["column"])
            v.set(cx - 10 + i, 12, pz + j, p["trim"])
    v.fill(cx - 11, 13, pz, cx + 11, 14, pz + 12, p["wall2"])
    v.gable_roof(cx - 11, 15, pz, cx + 11, pz + 12, p["roof"], ridge_axis="z")
    v.fill(cx - 2, 1, pz - 1, cx + 2, 8, pz + 1, "air")


def ship(v: Voxel, x: int, z: int, p: Palette, length: int = 40, beam: int = 9,
         masts: int = 3, style: str = "galleon") -> None:
    """Hull along +x starting at x, resting on water level y = 0."""
    hull = p.get("hull", "dark_oak_planks")
    deck = p.get("deck", "oak_planks")
    cz = z + beam // 2
    hb = beam // 2
    depth = 4 if style == "galleon" else 3
    for i in range(length):
        t = i / (length - 1)
        taper = min(t, 1 - t) * 4
        w = min(hb, max(1, round(hb * min(1.0, taper + 0.15))))
        for y in range(-depth + 1, 1):
            shrink = max(0, (-y) - 1)
            ww = max(1, w - shrink)
            v.fill(x + i, y, cz - ww, x + i, y, cz + ww, hull)
            if ww > 1 and y > -depth + 1:
                v.fill(x + i, y, cz - ww + 1, x + i, y, cz + ww - 1, "air")
        v.fill(x + i, 1, cz - w, x + i, 1, cz + w, deck)
        if style in ("galleon", "longship"):
            v.set(x + i, 2, cz - w, hull)
            v.set(x + i, 2, cz + w, hull)
    if style == "galleon":
        # raised stern castle and bow
        v.fill(x + length - 10, 2, cz - hb + 1, x + length - 2, 4, cz + hb - 1, hull)
        v.fill(x + length - 9, 2, cz - hb + 2, x + length - 3, 4, cz + hb - 2, "air")
        v.fill(x + length - 10, 5, cz - hb + 1, x + length - 2, 5, cz + hb - 1, deck)
        v.fill(x + 3, 2, cz - 2, x + 8, 3, cz + 2, hull)
        v.fill(x + 3, 4, cz - 2, x + 8, 4, cz + 2, deck)
        v.line((x, 2, cz), (x - 8, 6, cz), "stripped_oak_log")  # bowsprit
        for m in range(masts):
            mx = x + length * (m + 1) // (masts + 1)
            mh = 24 if m == masts // 2 else 20
            v.column(mx, 2, cz, mh, "stripped_spruce_log")
            for yy, w in ((mh - 4, 7), (mh - 11, 9), (mh - 17, 10)):
                if yy < 4:
                    continue
                v.fill(mx, 2 + yy, cz - w, mx, 2 + yy, cz + w, "stripped_oak_log")
                v.fill(mx, 2 + yy - 5, cz - w + 1, mx, 2 + yy - 1, cz + w - 1, "white_wool")
    elif style == "longship":
        for i in range(0, length, 4):
            v.set(x + i, 2, cz - hb, "red_wool" if (i // 4) % 2 else "yellow_wool")
            v.set(x + i, 2, cz + hb, "red_wool" if (i // 4) % 2 else "yellow_wool")
        v.line((x, 1, cz), (x - 2, 8, cz), hull)       # dragon prow
        v.set(x - 3, 9, cz, "gold_block")
        v.line((x + length - 1, 1, cz), (x + length + 1, 7, cz), hull)
        mx = x + length // 2
        v.column(mx, 2, cz, 16, "stripped_spruce_log")
        v.fill(mx, 15, cz - 7, mx, 15, cz + 7, "stripped_oak_log")
        for yy in range(6, 15):
            for zz in range(cz - 6, cz + 7):
                v.set(mx, yy, zz, "red_wool" if (zz - cz + 6) // 2 % 2 else "white_wool")
        for i in range(2, length - 2, 2):
            v.set(x + i, 1, cz - hb - 1, "oak_fence")
            v.set(x + i, 1, cz + hb + 1, "oak_fence")
    elif style == "trireme":
        v.line((x, 1, cz), (x - 4, 0, cz), "iron_block")   # bronze ram
        v.line((x + length - 1, 1, cz), (x + length + 2, 6, cz), hull)
        for i in range(3, length - 3, 2):
            for side in (-1, 1):
                v.line((x + i, 0, cz + side * (hb + 1)), (x + i, -1, cz + side * (hb + 3)), "oak_fence")
        mx = x + length // 2
        v.column(mx, 2, cz, 14, "stripped_spruce_log")
        v.fill(mx, 13, cz - 6, mx, 13, cz + 6, "stripped_oak_log")
        v.fill(mx, 6, cz - 5, mx, 12, cz + 5, "white_wool")
        v.fill(x + length - 8, 2, cz - 2, x + length - 3, 3, cz + 2, deck)


def arched_bridge(v: Voxel, x: int, z: int, length: int, width: int, p: Palette,
                  arches: int = 3, axis: str = "x", deck_y: int = 6, shops: bool = False) -> None:
    span = length // arches
    for a in range(arches):
        if axis == "x":
            v.arch(x + a * span, 1, z, span + 1, deck_y, width, p["wall"], axis="x")
        else:
            v.arch(x, 1, z + a * span, span + 1, deck_y, width, p["wall"], axis="z")
    if axis == "x":
        v.fill(x, deck_y + 1, z, x + length, deck_y + 1, z + width - 1, p["floor"])
        v.fill(x, deck_y + 2, z, x + length, deck_y + 2, z, p["trim"])
        v.fill(x, deck_y + 2, z + width - 1, x + length, deck_y + 2, z + width - 1, p["trim"])
        if shops:
            for i in range(x + 2, x + length - 4, 7):
                v.fill(i, deck_y + 2, z - 3, i + 4, deck_y + 5, z - 1, p["wall2"])
                v.fill(i + 1, deck_y + 2, z - 2, i + 3, deck_y + 4, z - 1, "air")
                v.fill(i, deck_y + 6, z - 3, i + 4, deck_y + 6, z - 1, p["roof"])
                v.fill(i, deck_y + 2, z + width, i + 4, deck_y + 5, z + width + 2, p["wall2"])
                v.fill(i + 1, deck_y + 2, z + width, i + 3, deck_y + 4, z + width + 1, "air")
                v.fill(i, deck_y + 6, z + width, i + 4, deck_y + 6, z + width + 2, p["roof"])
    else:
        v.fill(x, deck_y + 1, z, x + width - 1, deck_y + 1, z + length, p["floor"])
        v.fill(x, deck_y + 2, z, x, deck_y + 2, z + length, p["trim"])
        v.fill(x + width - 1, deck_y + 2, z, x + width - 1, deck_y + 2, z + length, p["trim"])


def aqueduct(v: Voxel, x: int, z: int, length: int, p: Palette, span: int = 7,
             tiers: int = 2, tier_h: int = 9, thickness: int = 3) -> None:
    """Multi-tier arcade carrying a water channel along +x."""
    arches = max(1, length // span)
    y = 1
    for t in range(tiers):
        for a in range(arches):
            v.arch(x + a * span, y, z, span + 1, tier_h, thickness, p["wall"], axis="x")
        y += tier_h
    top = y
    v.fill(x, top, z, x + arches * span, top, z + thickness - 1, p["wall"])
    v.fill(x, top + 1, z, x + arches * span, top + 1, z, p["wall"])
    v.fill(x, top + 1, z + thickness - 1, x + arches * span, top + 1, z + thickness - 1, p["wall"])
    if thickness >= 3:
        v.fill(x, top + 1, z + 1, x + arches * span, top + 1, z + thickness - 2, "water")


def windmill(v: Voxel, x: int, z: int, p: Palette, style: str = "tower") -> None:
    """Tower mill with four sails on the +z face (style 'post' = wooden box on a post)."""
    if style == "post":
        v.fill(x - 2, 1, z - 2, x + 2, 3, z + 2, p["wall2"])
        v.column(x, 4, z, 2, "stripped_oak_log")
        v.fill(x - 3, 6, z - 3, x + 3, 12, z + 3, p["roof"])
        v.fill(x - 2, 7, z - 2, x + 2, 11, z + 2, "air")
        v.gable_roof(x - 3, 13, z - 3, x + 3, z + 3, p["roof"], ridge_axis="x", overhang=0)
        hub_y, hub_z = 10, z + 4
    else:
        for k in range(12):
            r = 4.5 - k * 0.12
            v.disc(x, 1 + k, z, r, p["wall"], hollow=True)
        v.cone(x, 13, z, 5, 5, p["roof"])
        hub_y, hub_z = 11, z + 5
    v.line((x, hub_y, z), (x, hub_y, hub_z), "stripped_oak_log")
    for ang in (45, 135, 225, 315):
        dx = math.cos(math.radians(ang))
        dy = math.sin(math.radians(ang))
        for i in range(1, 11):
            px, py = round(x + dx * i), round(hub_y + dy * i)
            v.set(px, py, hub_z, "stripped_oak_log")
            if i > 2:
                v.set(px + (1 if dx > 0 else -1), py, hub_z, "white_wool")


def pagoda(v: Voxel, cx: int, cz: int, p: Palette, stories: int = 5, half: int = 5, story_h: int = 5) -> None:
    y = 1
    for s in range(stories):
        h = half - s // 2
        v.walls(cx - h, y, cz - h, cx + h, y + story_h - 1, cz + h, p["wall"])
        v.fill(cx - h + 1, y, cz - h + 1, cx + h - 1, y + story_h - 1, cz + h - 1, "air")
        v.fill(cx - h, y, cz - h, cx + h, y, cz + h, p["floor"])
        for px, pz in ((cx - h, cz - h), (cx + h, cz - h), (cx - h, cz + h), (cx + h, cz + h)):
            v.column(px, y, pz, story_h, p["column"])
        v.windows(cx - h, y + 2, cz - h, cx + h, cz + h, p["window"], period=2, offset=1)
        v.pagoda_roof(cx, y + story_h, cz, h + 2, p["roof"], p["trim"])
        y += story_h + 2
    v.column(cx, y, cz, 6, "gold_block")


def japanese_castle(v: Voxel, cx: int, cz: int, p: Palette, stories: int = 5) -> None:
    """Tenshu on a sloped stone base (ishigaki)."""
    base = 18
    for k in range(10):
        r = base - k // 2
        v.fill(cx - r, 1 + k, cz - r, cx + r, 1 + k, cz + r, "stone_bricks" if k % 3 else "mossy_stone_bricks")
    y = 11
    half = 12
    for s in range(stories):
        h = half - s * 2
        sh = 5
        v.fill(cx - h, y, cz - h, cx + h, y + sh - 1, cz + h, p["wall"])
        v.fill(cx - h + 1, y, cz - h + 1, cx + h - 1, y + sh - 1, cz + h - 1, "air")
        v.fill(cx - h, y, cz - h, cx + h, y, cz + h, p["floor"])
        v.walls(cx - h, y + sh - 1, cz - h, cx + h, y + sh - 1, cz + h, p["wall2"])
        v.windows(cx - h, y + 2, cz - h, cx + h, cz + h, p["window"], period=3, offset=1)
        v.pagoda_roof(cx, y + sh, cz, h + 2, p["roof"], p["trim"])
        # gabled dormers on alternate floors
        if s % 2 == 1:
            v.gable_roof(cx - 3, y + sh + 1, cz - h - 2, cx + 3, cz - h + 1, p["roof"], ridge_axis="z", overhang=0)
        y += sh + 2
    v.fill(cx - 1, y, cz - 1, cx + 1, y, cz + 1, p["roof"])
    v.set(cx - 2, y + 1, cz, "gold_block")
    v.set(cx + 2, y + 1, cz, "gold_block")


def torii(v: Voxel, cx: int, z: int, half: int = 4, h: int = 8) -> None:
    for px in (cx - half, cx + half):
        v.column(px, 1, z, h, "red_concrete")
    v.fill(cx - half - 2, h, z, cx + half + 2, h, z, "red_concrete")
    v.fill(cx - half - 2, h + 1, z, cx + half + 2, h + 1, z, "black_concrete")
    v.fill(cx - half, h - 2, z, cx + half, h - 2, z, "red_concrete")


def longhouse(v: Voxel, cx: int, z: int, p: Palette, length: int = 30, width: int = 11) -> None:
    half = width // 2
    v.walls(cx - half, 1, z, cx + half, 4, z + length, p["wall2"])
    v.fill(cx - half + 1, 1, z + 1, cx + half - 1, 4, z + length - 1, "air")
    v.fill(cx - half, 1, z, cx + half, 1, z + length, p["floor"])
    # curved bowed walls suggested by stepping the roof
    top = v.gable_roof(cx - half, 5, z, cx + half, z + length, p["roof"], ridge_axis="z", overhang=1)
    v.fill(cx - 1, 1, z, cx + 1, 3, z, "air")
    v.set(cx, 1, z + length // 2, "campfire")
    v.set(cx, top + 1, z + length // 2, "air")
    for i in range(z + 2, z + length - 2, 4):
        v.set(cx - half, 2, i, "oak_fence")
        v.set(cx + half, 2, i, "oak_fence")
    v.fill(cx - half - 1, 0, z - 1, cx + half + 1, 0, z + length + 1, "dirt_path")


def ziggurat(v: Voxel, cx: int, cz: int, p: Palette, base: int = 44, tiers: int = 3, tier_h: int = 7) -> None:
    v.step_pyramid(cx, 1, cz, base, tiers, tier_h, p["wall"], shrink=base // (tiers * 2) - 1)
    # three stairways on the south face converging on the first terrace
    r = base // 2
    for k in range(tier_h):
        v.fill(cx - 2, 1 + k, cz + r - k + 3, cx + 2, 1 + k, cz + r - k + 3, p["trim"])
    for k in range(tier_h * tiers):
        if cz + r - k > cz - r // 3:
            v.set(cx, 1 + k, cz + r - k, p["trim"])
    # shrine on top
    rt = r - (tiers) * (base // (tiers * 2) - 1)
    top = 1 + tiers * tier_h
    v.fill(cx - max(2, rt - 2), top, cz - max(2, rt - 2), cx + max(2, rt - 2), top + 4, cz + max(2, rt - 2), p["trim"])
    v.fill(cx - max(1, rt - 3), top, cz - max(1, rt - 3), cx + max(1, rt - 3), top + 3, cz + max(1, rt - 3), "air")
    v.fill(cx - 1, top, cz + max(2, rt - 2), cx + 1, top + 2, cz + max(2, rt - 2), "air")


def stepwell(v: Voxel, cx: int, cz: int, p: Palette, half: int = 14, depth: int = 12) -> None:
    """Inverted step pyramid carved into the ground (Chand Baori style)."""
    for k in range(depth):
        r = half - k
        if r < 2:
            break
        v.fill(cx - r, -k, cz - r, cx + r, -k, cz + r, "air")
        v.walls(cx - r - 1, -k, cz - r - 1, cx + r + 1, -k, cz + r + 1, p["wall"])
        # stair pattern on the three closed sides
        for i in range(-r, r + 1, 2):
            v.set(cx + i, -k, cz - r, p["trim"])
            v.set(cx - r, -k, cz + i, p["trim"])
            v.set(cx + r, -k, cz + i, p["trim"])
    bottom = -depth + 1
    v.fill(cx - 2, bottom, cz - 2, cx + 2, bottom, cz + 2, "water")
    v.fill(cx - 2, bottom - 1, cz - 2, cx + 2, bottom - 1, cz + 2, p["wall"])
    pad(v, cx - half - 2, cz - half - 2, cx + half + 2, cz + half + 2, p["floor"])
    v.fill(cx - half, 0, cz - half, cx + half, 0, cz + half, "air")
    # pavilion on the open (south) side
    v.fill(cx - 4, 1, cz + half + 1, cx + 4, 1, cz + half + 5, p["floor"])
    for px in (cx - 4, cx + 4):
        for pz in (cz + half + 1, cz + half + 5):
            v.column(px, 2, pz, 4, p["column"])
    v.fill(cx - 5, 6, cz + half, cx + 5, 6, cz + half + 6, p["roof"])
    v.dome(cx, 6, cz + half + 3, 3, p["roof"])


def stonehenge(v: Voxel, cx: int, cz: int) -> None:
    r = 16
    for a in range(0, 360, 12):
        rad = math.radians(a)
        x = round(cx + r * math.cos(rad))
        z = round(cz + r * math.sin(rad))
        v.fill(x, 1, z, x, 7, z, "stone")
        x2 = round(cx + r * math.cos(math.radians(a + 12)))
        z2 = round(cz + r * math.sin(math.radians(a + 12)))
        if a < 240:
            v.line((x, 8, z), (x2, 8, z2), "stone")
    for a in range(30, 360, 72):
        rad = math.radians(a)
        x = round(cx + 7 * math.cos(rad))
        z = round(cz + 7 * math.sin(rad))
        v.fill(x - 1, 1, z, x - 1, 11, z, "andesite")
        v.fill(x + 1, 1, z, x + 1, 11, z, "andesite")
        v.fill(x - 1, 12, z, x + 1, 12, z, "andesite")
    v.disc(cx, 0, cz, 22, "grass_block")


def trebuchet(v: Voxel, x: int, z: int) -> None:
    """Counterweight trebuchet facing -x."""
    wood = "stripped_dark_oak_log"
    v.fill(x - 4, 1, z - 3, x + 6, 1, z + 3, wood)
    for pz in (z - 2, z + 2):
        v.line((x - 3, 1, pz), (x, 9, pz), wood)
        v.line((x + 5, 1, pz), (x, 9, pz), wood)
    v.fill(x, 9, z - 2, x, 9, z + 2, "iron_block")      # axle
    v.line((x - 10, 14, z), (x + 5, 7, z), wood)          # beam
    v.fill(x + 5, 3, z - 1, x + 7, 6, z + 1, "stone")     # counterweight
    v.line((x - 10, 14, z), (x - 14, 3, z), "chain")      # sling
    v.set(x - 14, 2, z, "stone")


def siege_tower(v: Voxel, x: int, z: int) -> None:
    v.fill(x, 1, z, x + 6, 20, z + 6, "spruce_planks")
    v.fill(x + 1, 1, z + 1, x + 5, 19, z + 5, "air")
    for f in range(1, 20, 5):
        v.fill(x + 1, f, z + 1, x + 5, f, z + 5, "oak_planks")
        v.windows(x, f + 2, z, x + 6, z + 6, "air", period=2, offset=1)
    v.fill(x, 21, z, x + 6, 21, z + 6, "oak_planks")
    v.fill(x - 6, 17, z + 1, x - 1, 17, z + 5, "oak_planks")    # drawbridge
    for px in (x - 1, x + 7):
        for pz in (z - 1, z + 7):
            v.fill(px, 0, pz, px, 1, pz, "stripped_oak_log")   # wheels
    v.fill(x, 1, z, x, 20, z + 6, "oak_planks")           # hide-covered front (sheathed)


def catapult(v: Voxel, x: int, z: int) -> None:
    wood = "stripped_oak_log"
    v.fill(x - 3, 1, z - 2, x + 3, 1, z + 2, wood)
    for pz in (z - 2, z + 2):
        v.line((x - 2, 1, pz), (x, 5, pz), wood)
        v.line((x + 2, 1, pz), (x, 5, pz), wood)
    v.fill(x, 5, z - 2, x, 5, z + 2, "iron_block")
    v.line((x + 3, 2, z), (x - 4, 7, z), wood)
    v.set(x - 4, 8, z, "stone")
    v.fill(x - 4, 5, z - 2, x - 4, 5, z + 2, wood)       # crossbar


def roman_road(v: Voxel, x: int, z: int, length: int, width: int = 7) -> None:
    half = width // 2
    v.fill(x, -3, z - half - 1, x + length, -1, z + half + 1, "gravel")
    v.fill(x, 0, z - half, x + length, 0, z + half, "polished_andesite")
    v.fill(x, 0, z - half - 1, x + length, 0, z - half - 1, "stone")
    v.fill(x, 0, z + half + 1, x + length, 0, z + half + 1, "stone")
    for i in range(x, x + length, 20):
        v.column(i, 1, z + half + 2, 3, "smooth_stone")   # milestone


def fort_bastion(v: Voxel, cx: int, cz: int, p: Palette, half: int = 26, h: int = 8) -> None:
    """Star fort / Spanish colonial fortress: thick walls, arrow bastions."""
    v.fill(cx - half, 1, cz - half, cx + half, h, cz + half, p["wall"])
    v.fill(cx - half + 4, 1, cz - half + 4, cx + half - 4, h, cz + half - 4, "air")
    v.fill(cx - half + 4, 1, cz - half + 4, cx + half - 4, 1, cz + half - 4, p["floor"])
    for sx in (-1, 1):
        for sz in (-1, 1):
            bx, bz = cx + sx * half, cz + sz * half
            for k in range(10):            # arrow-head bastion projecting from the corner
                ex, ez = bx + sx * (10 - k), bz + sz * k
                v.fill(min(bx, ex), 1, min(bz, ez), max(bx, ex), h, max(bz, ez), p["wall"])
    v.crenellate(cx - half, h + 1, cz - half, cx + half, cz + half, p["wall2"], period=3)
    v.fill(cx - 2, 1, cz + half - 4, cx + 2, 5, cz + half, "air")
    house(v, cx - 8, cz - 8, 17, 12, p, floors=2, roof="hip")


def ruined_wall(v: Voxel, x: int, z: int, length: int, block: str = "mossy_stone_bricks", seed: int = 3) -> None:
    rng = random.Random(seed)
    for i in range(length):
        h = rng.choice((1, 2, 2, 3, 4, 5))
        v.fill(x + i, 1, z, x + i, h, z, block if rng.random() > .3 else "cracked_stone_bricks")


def statue(v: Voxel, x: int, z: int, h: int, block: str, y: int = 1) -> None:
    """Abstract colossus: plinth, legs, torso, head.  ``y`` is the plinth base."""
    v.fill(x - 2, y, z - 2, x + 2, y + 1, z + 2, "smooth_stone")
    y += 2
    v.column(x - 1, y, z, h // 3, block)
    v.column(x + 1, y, z, h // 3, block)
    v.fill(x - 2, y + h // 3, z - 1, x + 2, y + 2 * h // 3, z + 1, block)
    v.fill(x - 1, y + 1 + 2 * h // 3, z - 1, x + 1, y + 3 + 2 * h // 3, z + 1, block)
    v.fill(x - 3, y + 2 * h // 3, z, x - 3, y + 2 * h // 3 + 5, z, block)   # raised arm


def city_block(v: Voxel, x: int, z: int, p: Palette, cols: int = 3, rows: int = 2,
               lot: int = 9, street: int = 3, floors: Tuple[int, int] = (2, 3),
               roof: str = "gable", seed: int = 7) -> Tuple[int, int]:
    """Grid of houses with streets.  Returns the (x2, z2) far corner."""
    rng = random.Random(seed)
    walls = [p["wall"], p["wall2"], p["wall"]]
    x2 = x + cols * (lot + street)
    z2 = z + rows * (lot + street)
    pad(v, x, z, x2, z2, p["path"])
    for c in range(cols):
        for r in range(rows):
            hx = x + street + c * (lot + street)
            hz = z + street + r * (lot + street)
            w = rng.randint(lot - 3, lot)
            d = rng.randint(lot - 3, lot)
            house(v, hx, hz, w, d, p, floors=rng.randint(*floors), roof=roof,
                  wall=rng.choice(walls), ridge=rng.choice("xz"))
    return x2, z2
