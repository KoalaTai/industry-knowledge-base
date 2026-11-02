"""The Holy Land, Third Crusade - Assassin's Creed (2007), 1191."""

import math
import random

from .. import structures as S
from ..palettes import CRUSADER, LEVANT
from ..registry import Build, World
from ..voxel import AIR, Voxel


# ----------------------------------------------------------------- Masyaf helpers

_ROCK_SIDE = ["stone"] * 5 + ["andesite"] * 3 + ["cobblestone"] * 2 + ["mossy_cobblestone"]
_ROCK_TOP = ["stone"] * 3 + ["andesite"] * 2 + ["cobblestone", "gravel", "gravel",
                                                "coarse_dirt", "coarse_dirt", "mossy_cobblestone"]


def _squircle(cx: int, cz: int, r: float, rz: float, n: int = 4):
    """Cells of a rounded rectangle |x/r|^n + |z/rz|^n <= 1."""
    cells = set()
    for x in range(int(cx - r) - 1, int(cx + r) + 2):
        for z in range(int(cz - rz) - 1, int(cz + rz) + 2):
            if (abs(x - cx) / (r + 0.5)) ** n + (abs(z - cz) / (rz + 0.5)) ** n <= 1.0:
                cells.add((x, z))
    return cells


def _crag(v: Voxel, cx: int, cz: int, layers: int, r0: float, rz0: float,
          tx: float, tz: float, seed: int = 11):
    """Terraced crag of varied stone with two protruding ledges (overhangs).

    Returns two per-layer edge maps, ``{x: southernmost z}`` and ``{z: easternmost x}``,
    so paths can be cut into the south and east faces.
    """
    rng = random.Random(seed)
    shapes = []
    for k in range(layers):
        bump = 1.5 if k in (5, 10) else (0.7 if k in (6, 11) else 0.0)
        shapes.append(_squircle(cx, cz, r0 - tx * k + bump, rz0 - tz * k + bump, n=5))
    south_edges, east_edges = [], []
    for k, cells in enumerate(shapes):
        y = 1 + k
        above = shapes[k + 1] if k + 1 < layers else set()
        below = shapes[k - 1] if k else None
        south, east = {}, {}
        for (x, z) in cells:
            south[x] = max(south.get(x, z), z)
            east[z] = max(east.get(z, x), x)
            exposed_top = (x, z) not in above
            edge = any((x + dx, z + dz) not in cells for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if exposed_top:
                b = rng.choice(_ROCK_TOP)
                if b == "gravel" and below is not None and (x, z) not in below:
                    b = "cobblestone"            # nothing under it: gravel would fall
            elif edge:
                b = rng.choice(_ROCK_SIDE)
            else:
                b = "stone"
            v.set(x, y, z, b)
        south_edges.append(south)
        east_edges.append(east)
    return south_edges, east_edges


def _cliff_ramp(v: Voxel, edges, axis: str, a1: int, a2: int, y1: int, y2: int, top: int) -> None:
    """Two-wide path cut into a cliff face, from a1 to a2 along ``axis`` ('x' = the
    south face, 'z' = the east face) rising y1 -> y2: kerb, railing, a stair block on
    every rise, lanterns, and corbelled stone under any lane left hanging by a ledge."""
    n = abs(a2 - a1)
    step = 1 if a2 > a1 else -1
    face = ("east" if step > 0 else "west") if axis == "x" else ("south" if step > 0 else "north")
    stair = f"cobblestone_stairs[facing={face},half=bottom]"

    def at(p, q):                      # (along, across) -> (x, z)
        return (p, q) if axis == "x" else (q, p)

    for i in range(n + 1):
        p = a1 + i * step
        y = y1 + round((y2 - y1) * i / n)
        prev_y = y1 + round((y2 - y1) * (i - 1) / n) if i else y - 1
        e = edges[y - 1].get(p)
        if e is None:
            continue
        block = stair if y != prev_y else "cobblestone"
        for q in (e - 2, e - 1):
            v.set(at(p, q)[0], y, at(p, q)[1], block)
        v.set(at(p, e)[0], y, at(p, e)[1], "cobblestone")                 # kerb
        for q in (e - 2, e - 1, e):                                       # corbel under overhangs
            x, z = at(p, q)
            yy = y - 1
            while yy >= 1 and y - yy <= 3 and v.get(x, yy, z) is None:
                v.set(x, yy, z, "stone")
                yy -= 1
        if y < top:
            for q in (e - 2, e - 1):
                x, z = at(p, q)
                v.carve(x, y + 1, z, x, y + 3, z)                           # headroom
            v.set(at(p, e)[0], y + 1, at(p, e)[1], "cobblestone_wall")    # railing
        if i % 9 == 4:
            v.set(at(p, e)[0], y + 2, at(p, e)[1], "lantern")


def _levant_house(v: Voxel, x: int, z: int, w: int, d: int, floors: int, wall: str,
                  door: str, awning: str, rng: random.Random) -> None:
    """Flat-roofed village house with a real door, an awning, windows and furniture."""
    x2, z2 = x + w - 1, z + d - 1
    h = floors * 4
    v.fill(x, 1, z, x2, h, z2, wall)
    v.carve(x + 1, 1, z + 1, x2 - 1, h, z2 - 1)
    v.fill(x + 1, 0, z + 1, x2 - 1, 0, z2 - 1, "smooth_sandstone")
    for f in range(floors):
        y0 = 1 + f * 4
        if f:
            v.fill(x + 1, y0 - 1, z + 1, x2 - 1, y0 - 1, z2 - 1, "oak_planks")
        v.windows(x, y0 + 1, z, x2, z2, "glass_pane", period=3, offset=2)
    v.fill(x, h + 1, z, x2, h + 1, z2, "smooth_sandstone")               # flat roof
    v.walls(x, h + 2, z, x2, h + 2, z2, "sandstone_slab[type=bottom]")   # low parapet
    # door + striped awning on the street side
    dx = x + w // 2
    dz, out, face = (z2, z2 + 1, "south") if door == "south" else (z, z - 1, "north")
    v.carve(dx, 1, dz, dx, 2, dz)
    v.set(dx, 1, dz, f"oak_door[facing={face},half=lower]")
    v.set(dx, 2, dz, f"oak_door[facing={face},half=upper]")
    for i, ax in enumerate(range(dx - 1, dx + 2)):
        v.set(ax, 3, out, awning if i % 2 == 0 else "white_wool")
    v.fill(dx - 1, 1, out, dx - 1, 2, out, "oak_fence")
    v.fill(dx + 1, 1, out, dx + 1, 2, out, "oak_fence")
    # furniture
    ix, iz = x + 1, z + 1 if door == "south" else z2 - 1
    v.set(ix, 1, iz, "barrel")
    v.set(x2 - 1, 1, iz, rng.choice(["crafting_table", "barrel", "chest[facing=south]"]))
    if rng.random() < 0.5 and w >= 6:
        bz = z + 2 if door == "south" else z2 - 2
        v.set(x + 2, 1, bz + 1, "red_bed[facing=north,part=foot]")
        v.set(x + 2, 1, bz, "red_bed[facing=north,part=head]")
    if floors > 1:
        lz = z + 1 if door == "south" else z2 - 1
        v.fill(x2 - 1, 1, lz, x2 - 1, h, lz, f"ladder[facing={face}]")   # through the floor hatch
        v.set(x + 1, 5, z2 - 1, "barrel")
    cx, cz = (x + x2) // 2, (z + z2) // 2
    v.set(cx, h - 1, cz, "chain")
    v.set(cx, h - 2, cz, "lantern[hanging=true]")
    if rng.random() < 0.6:                                     # rooftop clutter
        v.set(x + 1, h + 2, z + 1, "hay_block")
        v.set(x2 - 1, h + 2, z2 - 1, "barrel")


def _stall(v: Voxel, x: int, z: int, cloth: str, goods: str) -> None:
    """3x3 market stall: fence posts, striped awning, barrel counter, lantern."""
    for px, pz in ((x, z), (x + 2, z), (x, z + 2), (x + 2, z + 2)):
        v.fill(px, 1, pz, px, 2, pz, "oak_fence")
    for i, px in enumerate(range(x, x + 3)):
        v.fill(px, 3, z, px, 3, z + 2, cloth if i % 2 == 0 else "white_wool")
    v.fill(x, 1, z + 1, x + 2, 1, z + 1, "barrel")
    v.set(x + 1, 2, z + 1, goods)
    v.set(x, 2, z + 1, "lantern")


def _well(v: Voxel, x: int, z: int) -> None:
    v.fill(x - 1, 1, z - 1, x + 1, 1, z + 1, "cobblestone")
    v.set(x, 0, z, "water")
    v.set(x, 1, z, "water")
    for px, pz in ((x - 1, z - 1), (x + 1, z + 1)):
        v.fill(px, 2, pz, px, 3, pz, "oak_fence")
    v.fill(x - 1, 4, z - 1, x + 1, 4, z + 1, "oak_slab[type=bottom]")
    v.set(x, 3, z, "chain")
    v.set(x + 1, 1, z + 2, "oak_sign[rotation=0]")


def _bookwall(v: Voxel, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> None:
    v.fill(x1, y1, z1, x2, y2, z2, "bookshelf")


def masyaf(v: Voxel) -> None:
    """The Assassin fortress on its crag above the village."""
    P = CRUSADER
    rng = random.Random(1191)
    S.pad(v, -60, -60, 60, 70, "grass_block")

    # ---------------------------------------------------------------- the crag
    TOP = 16                                                    # plateau surface y
    south, east = _crag(v, 0, -6, TOP, 32, 27, 0.47, 0.55)
    for bx, bz, r, b in ((-37, 2, 2, "andesite"), (36, -12, 2, "cobblestone"),
                         (-31, -30, 2, "stone"), (30, 20, 1.5, "andesite"), (-20, -36, 1.5, "mossy_cobblestone")):
        v.sphere(bx, 1, bz, r, b, hollow=False, y_min=1)       # boulders at the foot
    # bastion plinths so the corner towers rise out of the rock
    for px, pz in ((-18, -21), (18, -21), (-18, 7), (18, 7)):
        v.cylinder(px, 1, pz, 3, TOP, P["wall"])
    # the notch below the leap-of-faith platform: open to the north, hay cart on the grass
    v.carve(10, 1, -36, 18, TOP, -25)
    for px in (11, 17):
        for pz in (-31, -27):
            v.set(px, 1, pz, "dark_oak_log[axis=x]")
    v.fill(12, 1, -31, 16, 2, -27, "oak_planks")
    v.carve(13, 2, -30, 15, 2, -28)
    v.fill(13, 2, -30, 15, 4, -28, "hay_block")
    v.fill(14, 5, -30, 14, 5, -28, "hay_block")
    v.set(14, 5, -29, "hay_block"); v.set(14, 6, -29, "hay_block")
    v.fill(14, 1, -26, 14, 1, -25, "oak_fence")                 # drawbar
    for px, pz in ((10, -28), (18, -30), (12, -33), (16, -34), (17, -25)):
        v.set(px, 1, pz, "hay_block")
    v.set(11, 1, -34, "oak_sign[rotation=8]")

    # ---------------------------------------------------------------- the fortress
    fort = Voxel()
    S.curtain_wall(fort, -18, -18, 18, 10, 8, P, gate="south", tower_r=3)
    fort.fill(-16, 0, -16, 16, 0, 8, "stone_bricks")             # courtyard paving
    fort.fill(-1, 0, 1, 1, 0, 8, "cobblestone")                  # gate -> keep
    # wall walk: wooden ledge widening the inner ring, stairs up on both sides
    for x in (-16, 16):
        fort.fill(x, 8, -16, x, 8, -1, "oak_slab[type=top]")
        fort.fill(x, 8, 2, x, 8, 8, "oak_slab[type=top]")
    for z in (-16, 8):
        fort.fill(-16, 8, z, 16, 8, z, "oak_slab[type=top]")
    for sx in (-16, 16):
        for i in range(8):
            z, y = 6 - i, 1 + i
            if y > 1:
                fort.fill(sx, 1, z, sx, y - 1, z, P["wall"])
            fort.set(sx, y, z, "stone_brick_stairs[facing=north,half=bottom]")
    # arrow slits through both rings, lanterns on the merlons
    for x in range(-14, 15, 4):
        fort.carve(x, 5, -18, x, 6, -17)
        if abs(x) > 6:
            fort.carve(x, 5, 9, x, 6, 10)
    for z in range(-14, 7, 4):
        fort.carve(-18, 5, z, -17, 6, z)
        fort.carve(17, 5, z, 18, 6, z)
    for x in (-12, -6, 6, 12):
        fort.set(x, 11, -18, "lantern"); fort.set(x, 11, 10, "lantern")
    for z in (-12, -6, 0, 6):
        fort.set(-18, 11, z, "lantern"); fort.set(18, 11, z, "lantern")
    # gatehouse: passage with arch, half-raised portcullis, guard room, banners, sign
    fort.fill(-3, 1, 7, 3, 12, 11, P["wall"])
    fort.carve(-1, 1, 6, 1, 4, 11)
    for z in (7, 11):
        fort.set(-1, 4, z, "stone_brick_stairs[facing=west,half=top]")
        fort.set(1, 4, z, "stone_brick_stairs[facing=east,half=top]")
    fort.fill(-1, 3, 9, 1, 4, 9, "iron_bars")
    for z in (8, 10):
        fort.set(0, 4, z, "lantern[hanging=true]")
    fort.carve(-2, 9, 8, 2, 11, 10)                               # guard room
    fort.carve(-3, 9, 9, -3, 10, 9); fort.carve(3, 9, 9, 3, 10, 9)   # doors from the wall walk
    for x in (-2, 0, 2):
        fort.set(x, 10, 11, "air")                                # slits over the gate
    fort.set(0, 10, 9, "lantern[hanging=true]"); fort.set(0, 11, 9, "chain")
    fort.crenellate(-3, 13, 7, 3, 11, P["wall"])
    fort.set(-2, 8, 12, "red_wall_banner[facing=south]")
    fort.set(2, 8, 12, "red_wall_banner[facing=south]")
    fort.set(0, 6, 12, "oak_wall_sign[facing=south]")
    # the keep: three floors, great hall, stairs, study, roof ladder
    S.keep(fort, 0, -6, 7, 16, P)
    fort.carve(-6, 2, -12, 6, 15, 0)
    fort.fill(-1, 1, 1, 1, 1, 1, P["wall"]); fort.carve(-1, 2, 1, 1, 4, 1)
    fort.set(-1, 4, 1, "stone_brick_stairs[facing=west,half=top]")
    fort.set(1, 4, 1, "stone_brick_stairs[facing=east,half=top]")
    fort.fill(-6, 6, -12, 6, 6, 0, "oak_planks")
    fort.fill(-6, 11, -12, 6, 11, 0, "oak_planks")
    # great hall (y 2..5): long table, benches, dais, hanging lanterns, banners
    fort.fill(-4, 2, -6, 4, 2, -6, "oak_slab[type=top]")
    fort.set(-5, 2, -6, "oak_planks"); fort.set(5, 2, -6, "oak_planks")
    for x in range(-4, 5):
        fort.set(x, 2, -7, "oak_stairs[facing=north,half=bottom]")
        fort.set(x, 2, -5, "oak_stairs[facing=south,half=bottom]")
    fort.fill(-3, 2, -12, 3, 2, -11, "stone_brick_slab[type=bottom]")
    fort.set(0, 2, -12, "dark_oak_stairs[facing=south,half=bottom]")
    for x in (-3, 0, 3):
        fort.set(x, 5, -6, "chain"); fort.set(x, 4, -6, "lantern[hanging=true]")
    for z in (-10, -6, -2):
        fort.set(-6, 4, z, "red_wall_banner[facing=east]")
    for z in (-10, -6):
        fort.set(6, 4, z, "white_wall_banner[facing=west]")
    # stairs: east wall up to floor 2, west wall up to floor 3
    for i in range(5):
        z, y = -i, 2 + i
        if y > 2:
            fort.fill(6, 2, z, 6, y - 1, z, P["wall"])
        fort.set(6, y, z, "stone_brick_stairs[facing=north,half=bottom]")
    fort.carve(5, 6, -3, 6, 6, 0)
    for i in range(5):
        z, y = -11 + i, 7 + i
        if y > 7:
            fort.fill(-6, 7, z, -6, y - 1, z, P["wall"])
        fort.set(-6, y, z, "stone_brick_stairs[facing=south,half=bottom]")
    fort.carve(-6, 11, -10, -5, 11, -8)
    # floor 2 (y 7..10): armoury / dormitory
    for x in range(-4, 5, 2):
        fort.set(x, 7, -12, "barrel")
    for x in (-3, 3):
        fort.set(x, 10, -6, "chain"); fort.set(x, 9, -6, "lantern[hanging=true]")
    for x in (-2, 2):
        fort.set(x, 7, -2, "red_bed[facing=north,part=foot]")
        fort.set(x, 7, -3, "red_bed[facing=north,part=head]")
    # floor 3 (y 12..15): the master's study, ladder to the roof
    _bookwall(fort, -5, 12, -12, 5, 14, -12)
    _bookwall(fort, -6, 12, -4, -6, 13, -1)
    fort.set(0, 12, -9, "lectern[facing=south]")
    fort.fill(-2, 12, -5, 2, 12, -5, "oak_slab[type=top]")
    fort.set(0, 15, -6, "chain"); fort.set(0, 14, -6, "lantern[hanging=true]")
    fort.set(3, 12, -5, "white_wall_banner[facing=north]")
    fort.carve(6, 16, -12, 6, 16, -12)
    fort.fill(6, 12, -12, 6, 16, -12, "ladder[facing=west]")
    # the library wing: two floors of shelves, lecterns, a reading room
    fort.fill(-16, 1, -16, -10, 10, -7, P["wall"])
    fort.carve(-15, 2, -15, -11, 9, -8)
    fort.fill(-15, 6, -15, -11, 6, -8, "oak_planks")
    fort.carve(-10, 2, -9, -10, 3, -9)
    fort.set(-10, 2, -9, "oak_door[facing=west,half=lower]")
    fort.set(-10, 3, -9, "oak_door[facing=west,half=upper]")
    for z in (-14, -11):
        fort.set(-10, 3, z, "glass_pane"); fort.set(-10, 8, z, "glass_pane")
    for x in (-14, -12):
        fort.set(x, 3, -7, "glass_pane"); fort.set(x, 8, -7, "glass_pane")
    _bookwall(fort, -15, 2, -15, -11, 4, -15)
    _bookwall(fort, -15, 2, -14, -15, 4, -9)
    fort.set(-13, 2, -12, "lectern[facing=south]")
    fort.set(-12, 2, -10, "lectern[facing=west]")
    fort.set(-13, 5, -11, "chain"); fort.set(-13, 4, -11, "lantern[hanging=true]")
    for i in range(5):
        z, y = -8 - i, 2 + i
        if y > 2:
            fort.fill(-11, 2, z, -11, y - 1, z, P["wall"])
        fort.set(-11, y, z, "stone_brick_stairs[facing=north,half=bottom]")
    fort.carve(-12, 6, -11, -11, 6, -8)
    _bookwall(fort, -15, 7, -14, -15, 8, -9)
    _bookwall(fort, -14, 7, -15, -12, 8, -15)
    fort.fill(-14, 7, -11, -13, 7, -11, "oak_slab[type=top]")
    fort.set(-14, 7, -10, "oak_stairs[facing=south,half=bottom]")
    fort.set(-13, 7, -10, "oak_stairs[facing=south,half=bottom]")
    fort.set(-13, 8, -11, "lantern")
    fort.set(-12, 7, -13, "lectern[facing=east]")
    fort.walls(-16, 11, -16, -10, 11, -7, "stone_brick_slab[type=bottom]")
    fort.set(-16, 11, -7, "lantern"); fort.set(-10, 11, -7, "lantern")
    # the leap-of-faith tower: ladder inside, parapet, platform jutting north over the notch
    S.tower(fort, 14, -14, 2.5, 26, P, top="flat")
    fort.carve(11, 1, -14, 11, 2, -14)
    fort.set(11, 1, -14, "oak_door[facing=west,half=lower]")
    fort.set(11, 2, -14, "oak_door[facing=west,half=upper]")
    fort.fill(14, 1, -12, 14, 25, -12, "ladder[facing=north]")
    fort.carve(14, 26, -12, 14, 26, -12)
    for y in (6, 12, 18, 24):
        fort.set(14, y, -16, "wall_torch[facing=south]")
        fort.set(17, y, -14, "glass_pane")
    for x in range(11, 18):
        for z in range(-17, -11):
            d = math.hypot(x - 14, z + 14)
            if 2.0 < d <= 3.0 and z >= -15:
                fort.set(x, 27, z, "stone_brick_wall")
    fort.fill(13, 26, -17, 15, 26, -26, "oak_planks")
    fort.fill(13, 27, -18, 13, 27, -25, "oak_fence")
    fort.fill(15, 27, -18, 15, 27, -25, "oak_fence")
    fort.line((13, 22, -17), (13, 25, -21), "oak_log[axis=z]")
    fort.line((15, 22, -17), (15, 25, -21), "oak_log[axis=z]")
    fort.set(14, 27, -26, "oak_fence"); fort.set(14, 28, -26, "lantern")
    # courtyard: training ring with a dummy, an olive tree, lamp posts
    fort.disc(12, 0, 5, 3, "coarse_dirt")
    fort.disc(12, 1, 5, 3, "oak_fence", hollow=True)
    fort.set(12, 1, 5, "oak_fence"); fort.set(12, 2, 5, "hay_block"); fort.set(12, 3, 5, "carved_pumpkin[facing=south]")
    fort.tree(-12, 1, 3, "dark_oak_log", "oak_leaves[persistent=true]", height=4, canopy=2)
    for px, pz in ((-5, 4), (5, 4), (-14, -3), (15, -5)):
        fort.fill(px, 1, pz, px, 2, pz, "oak_fence"); fort.set(px, 3, pz, "lantern")
    v.merge(fort, 0, TOP, -3)

    # ---------------------------------------------------------------- switchback path
    # run 1 climbs the south face eastward, run 2 the east face northward, then a paved
    # walk follows the plateau rim round the south-east tower to the gate
    _cliff_ramp(v, south, "x", -23, 20, 1, 8, TOP)
    ze = south[7][20]
    v.fill(20, 8, ze - 4, 23, 8, ze - 1, "cobblestone")           # corner landing
    v.carve(20, 9, ze - 4, 23, 11, ze - 1)
    v.fill(21, 9, ze, 23, 9, ze, "cobblestone_wall")
    _cliff_ramp(v, east, "z", 13, -14, 9, TOP, TOP)
    xe = east[TOP - 1][-14]
    for x in range(22, xe):                                      # rim walk, skipping the cut of run 2
        for z in range(-14, 11):
            if v.get(x, TOP, z) != AIR:
                v.set(x, TOP, z, "cobblestone")
    v.fill(15, TOP, 11, 22, TOP, 11, "cobblestone")
    v.fill(2, TOP, 11, 14, TOP, 11, "cobblestone")
    v.fill(-3, TOP, 9, 1, TOP, 11, P["wall"])                    # apron before the gate
    for px, pz in ((-4, 9), (2, 9), (12, 12)):
        v.fill(px, TOP + 1, pz, px, TOP + 2, pz, "oak_fence"); v.set(px, TOP + 3, pz, "lantern")
    v.set(-24, 1, 18, "oak_sign[rotation=0]")

    # ---------------------------------------------------------------- the village
    v.fill(-32, 0, 21, 27, 0, 44, "dirt_path")
    v.fill(-32, 0, 32, 27, 0, 33, "gravel")
    walls = ["sandstone", "smooth_sandstone", "white_terracotta", "cut_sandstone"]
    cloths = ["red_wool", "orange_wool", "yellow_wool", "light_blue_wool", "lime_wool"]
    row_a = ((-30, 23, 7, 7, 2), (-21, 23, 8, 6, 1), (-11, 23, 7, 7, 2),
             (-2, 23, 6, 6, 1), (6, 23, 8, 7, 2), (16, 23, 7, 6, 1))
    row_b = ((-29, 36, 8, 7, 1), (-19, 35, 7, 8, 2), (-10, 36, 7, 6, 1),
             (0, 35, 8, 8, 2), (10, 36, 6, 6, 1), (18, 35, 8, 7, 2))
    for i, (hx, hz, w, d, f) in enumerate(row_a):
        _levant_house(v, hx, hz, w, d, f, walls[i % 4], "south", cloths[i % 5], rng)
    for i, (hx, hz, w, d, f) in enumerate(row_b):
        _levant_house(v, hx, hz, w, d, f, walls[(i + 2) % 4], "north", cloths[(i + 3) % 5], rng)
    for x in (-21, -12, -2, 8, 18):                               # street lamps
        v.fill(x, 1, 34, x, 2, 34, "oak_fence"); v.set(x, 3, 34, "lantern")
    # market square with fountain, stalls, well, palms and olive trees
    S.plaza(v, -8, 48, 8, 60, LEVANT, fountain=True)
    _stall(v, -7, 49, "red_wool", "hay_block")
    _stall(v, 4, 49, "yellow_wool", "melon")
    _stall(v, -7, 57, "lime_wool", "pumpkin")
    _stall(v, 4, 57, "light_blue_wool", "blue_wool")
    _well(v, -18, 52)
    for px, pz in ((-14, 46), (14, 46), (22, 56), (-26, 58)):
        v.palm(px, 1, pz, height=6)
    for i in range(6):
        v.tree(-50 + i * 18, 1, 62, "dark_oak_log", "oak_leaves[persistent=true]", height=4, canopy=2)
    for px, pz in ((-36, 30), (30, 40), (-40, 48)):
        v.tree(px, 1, pz, "dark_oak_log", "oak_leaves[persistent=true]", height=4, canopy=2)


def jerusalem(v: Voxel) -> None:
    """Temple Mount: Dome of the Rock, al-Aqsa and the city wall with gate towers."""
    P = LEVANT
    S.pad(v, -70, -70, 70, 70, P["ground"])
    S.curtain_wall(v, -64, -64, 64, 64, 10, CRUSADER, gate="south", tower_r=3)
    v.fill(-50, 1, -50, 50, 1, 50, "smooth_sandstone")       # the platform
    # Dome of the Rock: octagonal arcade + drum + golden dome
    cx, cz = 0, -10
    v.cylinder(cx, 2, cz, 16, 10, "white_terracotta", hollow=True)     # octagon approximated
    v.cylinder(cx, 2, cz, 16, 10, "white_terracotta", hollow=True)
    for y in range(5, 10, 2):
        for a in range(0, 360, 20):
            import math
            v.set(round(cx + 16 * math.cos(math.radians(a))), y, round(cz + 16 * math.sin(math.radians(a))), "blue_glazed_terracotta")
    v.disc(cx, 11, cz, 16, "light_gray_terracotta")
    v.disc(cx, 2, cz, 15, "smooth_sandstone")
    v.cylinder(cx, 12, cz, 10, 8, "light_blue_terracotta", hollow=True)   # drum
    v.disc(cx, 2, cz, 9, "air"); v.disc(cx, 12, cz, 9, "air")
    v.dome(cx, 20, cz, 10, "gold_block")
    v.set(cx, 31, cz, "gold_block")
    v.fill(cx - 2, 2, cz - 1, cx + 2, 3, cz + 1, "stone")           # the Foundation Stone
    v.fill(cx - 1, 2, cz + 16, cx + 1, 5, cz + 16, "air")
    # al-Aqsa: long basilica-plan mosque with silver-grey dome
    S.basilica(v, 0, 18, LEVANT, length=40, width=25, h=14)
    v.dome(0, 14, 50, 7, "light_gray_concrete")
    # city quarters inside the walls
    S.city_block(v, -60, -60, LEVANT, cols=4, rows=3, lot=8, street=3, floors=(1, 3), roof="flat", seed=4)
    S.city_block(v, 20, -60, LEVANT, cols=4, rows=3, lot=8, street=3, floors=(1, 3), roof="flat", seed=8)
    # Church of the Holy Sepulchre with twin domes
    S.house(v, -58, 10, 24, 20, CRUSADER, floors=3, roof="flat")
    v.dome(-50, 13, 20, 6, "light_gray_concrete")
    v.dome(-40, 13, 20, 4, "light_gray_concrete")


def acre(v: Voxel) -> None:
    """Crusader port: Hospitaller fortress, harbour wall and the Tower of Flies."""
    P = CRUSADER
    S.pad(v, -60, -40, 70, 70, "stone")
    v.fill(-60, -3, 40, 70, 0, 70, "water")
    v.fill(-60, 0, 38, 70, 0, 39, "stone_bricks")                      # quay
    v.fill(40, 0, 40, 44, 0, 68, "stone_bricks")                       # breakwater
    S.tower(v, 42, 66, 4, 14, P, top="crenel")                          # Tower of Flies
    S.curtain_wall(v, -40, -30, 30, 30, 9, P, gate="south", tower_r=4)
    S.keep(v, -5, -5, 10, 18, P)
    # Hospitaller vaulted hall (refectory) with pointed arches
    hx, hz = -36, 10
    v.fill(hx, 1, hz, hx + 30, 9, hz + 16, P["wall"])
    v.fill(hx + 1, 1, hz + 1, hx + 29, 8, hz + 15, "air")
    for x in range(hx + 5, hx + 28, 6):
        v.column(x, 1, hz + 8, 8, P["column"])
        v.fill(x - 1, 8, hz + 1, x + 1, 8, hz + 15, P["trim"])
    v.fill(hx + 14, 1, hz + 16, hx + 16, 4, hz + 16, "air")
    S.city_block(v, -56, 36 - 30, LEVANT, cols=2, rows=2, lot=7, street=3, floors=(1, 2), roof="flat", seed=6)
    S.ship(v, -40, 50, {"hull": "dark_oak_planks", "deck": "oak_planks"}, length=28, beam=7, masts=1, style="galleon")


def damascus(v: Voxel) -> None:
    """The Umayyad Mosque, Jesus Minaret and the covered souk."""
    P = LEVANT
    S.pad(v, -70, -50, 70, 70, P["ground"])
    S.mosque(v, 0, -10, LEVANT, half=20, dome_r=8, minarets=3, minaret_h=36)
    # covered souk: a long vaulted street with stalls
    sx, sz = -60, 40
    v.fill(sx, 1, sz, sx + 120, 7, sz + 9, P["wall"])
    v.fill(sx + 1, 1, sz + 1, sx + 119, 6, sz + 8, "air")
    v.fill(sx + 1, 7, sz + 2, sx + 119, 7, sz + 7, "iron_bars")           # light through the vault
    for x in range(sx + 3, sx + 118, 4):
        v.fill(x, 1, sz + 1, x + 1, 1, sz + 2, "barrel")
        v.fill(x, 1, sz + 7, x + 1, 1, sz + 8, "barrel")
        v.set(x, 2, sz + 1, "red_wool" if x % 8 else "yellow_wool")
        v.set(x, 2, sz + 8, "blue_wool" if x % 8 else "lime_wool")
    v.fill(sx, 1, sz + 3, sx, 5, sz + 6, "air")
    v.fill(sx + 120, 1, sz + 3, sx + 120, 5, sz + 6, "air")
    S.city_block(v, -65, -45, LEVANT, cols=3, rows=2, lot=8, street=3, floors=(1, 3), roof="flat", seed=9)
    S.city_block(v, 30, -45, LEVANT, cols=3, rows=2, lot=8, street=3, floors=(1, 3), roof="flat", seed=10)
    for x in range(-60, 60, 15):
        v.tree(x, 1, 55, "jungle_log", "jungle_leaves[persistent=true]", height=5)


WORLD = World(
    id="holy_land",
    name="The Holy Land",
    game="Assassin's Creed (2007)",
    era="1191, the Third Crusade",
    description="Altair's Levant: Masyaf, Jerusalem, Acre and Damascus.",
).build(Build("masyaf", "Masyaf", "The Assassin fortress on its crag with keep, library wing, leap-of-faith tower and haystack, above the village.", masyaf)
).build(Build("jerusalem", "Jerusalem", "Walled city with the Dome of the Rock, al-Aqsa and the Holy Sepulchre.", jerusalem)
).build(Build("acre", "Acre", "Crusader port: Hospitaller fortress and vaulted refectory, harbour, breakwater and the Tower of Flies.", acre)
).build(Build("damascus", "Damascus", "The Umayyad Mosque with three minarets and a 120-block covered souk.", damascus))
