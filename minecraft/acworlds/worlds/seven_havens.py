"""Avatar: Seven Havens (announced 2025, in production).

What is public: a new animated series set after Korra, following Pavi, a
young Earthbender and the next Avatar, in a world devastated by a
cataclysm in which only seven "havens" survive.  Everything else here is
a stylised interpretation, built so it can be reshaped once the show airs.
"""

import math
import random

from .. import structures as S
from ..palettes import _p
from ..registry import Build, World
from ..voxel import AIR, Voxel

HAVEN = _p(ground="stone", wall="deepslate_bricks", wall2="green_terracotta", trim="polished_deepslate",
           roof="lime_terracotta", floor="polished_andesite", column="deepslate_bricks", path="andesite",
           leaves="oak_leaves[persistent=true]", log="oak_log")
WASTE = "tuff"

HANGING = "lantern[hanging=true]"
SOUL_HANGING = "soul_lantern[hanging=true]"


# ----------------------------------------------------------------- helpers

def _noise(seed: int, cell: int = 12):
    """Smooth 2-D value noise in [0, 1]: returns ``n(x, z)``.  Deterministic per seed."""
    lat = {}

    def _lat(i, j):
        k = (i, j)
        if k not in lat:
            h = (i * 73856093) ^ (j * 19349663) ^ (seed * 83492791)
            lat[k] = random.Random(h & 0xFFFFFFFF).random()
        return lat[k]

    def n(x, z):
        fx, fz = x / cell, z / cell
        i, j = math.floor(fx), math.floor(fz)
        u, w = fx - i, fz - j
        u = u * u * (3 - 2 * u)
        w = w * w * (3 - 2 * w)
        a = _lat(i, j) * (1 - u) + _lat(i + 1, j) * u
        b = _lat(i, j + 1) * (1 - u) + _lat(i + 1, j + 1) * u
        return a * (1 - w) + b * w

    return n


def _erase(v: Voxel, x: int, y: int, z: int) -> None:
    """Drop a block from the canvas (no explicit air)."""
    v.blocks.pop((x, y, z), None)


def _pol(r: float, a: float):
    return round(r * math.cos(math.radians(a))), round(r * math.sin(math.radians(a)))


def _crater(v: Voxel, cx: int, cz: int, r: int, depth: int, rim: str = "") -> None:
    for k in range(depth):
        v.disc(cx, -k, cz, r * (1 - k / (depth + 1)), "air")
    v.disc(cx, -depth, cz, r * 0.4, "magma_block")
    if rim:
        v.disc(cx, 1, cz, r + 1, rim, hollow=True)


def _crater_floor(cx: int, cz: int, r: int, depth: int, x: int, z: int) -> int:
    """y of the first solid block under (x, z) inside a crater drawn by ``_crater``."""
    y = 0
    for k in range(depth):
        rr = r * (1 - k / (depth + 1))
        if ((x - cx) / (rr + 0.5)) ** 2 + ((z - cz) / (rr + 0.5)) ** 2 <= 1.0:
            y = -k - 1
        else:
            break
    return y


def _post(v: Voxel, x: int, y: int, z: int, h: int, fence: str = "dark_oak_fence", light: str = "lantern") -> None:
    v.column(x, y, z, h, fence)
    v.set(x, y + h, z, light)


def _dead_tree(v: Voxel, x: int, z: int, rng: random.Random, y: int = 1) -> None:
    h = rng.randint(4, 7)
    v.column(x, y, z, h, "dark_oak_log")
    for dx, dz in rng.sample(((1, 0), (-1, 0), (0, 1), (0, -1)), 2):
        v.set(x + dx, y + h - 2, z + dz, "dark_oak_log[axis=%s]" % ("x" if dx else "z"))
        v.set(x + 2 * dx, y + h - 1, z + 2 * dz, "dark_oak_log")


def _scrub(v: Voxel, x1: int, z1: int, x2: int, z2: int, seed: int, skip=None) -> None:
    """Break a tuff pad into coarse dirt, gravel, basalt and blackstone with two noise fields."""
    n1, n2 = _noise(seed, 9), _noise(seed + 1, 4)
    for x in range(x1, x2 + 1):
        for z in range(z1, z2 + 1):
            if skip and skip(x, z):
                continue
            a, b = n1(x, z), n2(x, z)
            if a > 0.70:
                v.set(x, 0, z, "blackstone")
            elif a > 0.60:
                v.set(x, 0, z, "basalt")
            elif a < 0.30:
                v.set(x, 0, z, "coarse_dirt")
            elif b < 0.22:
                v.set(x, 0, z, "gravel")
            elif b > 0.90:
                v.set(x, 0, z, "cobbled_deepslate")


def _fissure(v: Voxel, rng: random.Random, x: float, z: float, length: int, limit: int = 88, depth: int = 4) -> None:
    d = rng.uniform(0, 2 * math.pi)
    w = rng.choice((1, 1, 2))
    for _ in range(length):
        d += rng.uniform(-0.35, 0.35)
        x += math.cos(d)
        z += math.sin(d)
        ix, iz = round(x), round(z)
        if abs(ix) > limit - w or abs(iz) > limit - w:
            break
        for dx in range(w):
            for dz in range(w):
                v.fill(ix + dx, -depth, iz + dz, ix + dx, 0, iz + dz, "air")
                v.set(ix + dx, -depth - 1, iz + dz, "lava")
        if rng.random() < 0.3:
            v.set(ix - 1, 0, iz, "magma_block")


# ------------------------------------------------------------------- haven

def _terrace_y(r: float) -> int:
    """Top block y of the haven's ground at radius r (walk level is one higher)."""
    if r > 60:
        return 0
    if r > 54:
        return 1
    if r > 48:
        return 2
    if r > 42:
        return 3
    if r > 36:
        return 4
    return 5


def _haven_house(v: Voxel, x: int, z: int, w: int, d: int, floors: int, wall: str, rng: random.Random,
                 base: int = 5) -> None:
    """A flat-roofed town house set on the plateau (floor at ``base``), door lanterns, awning, roof lantern."""
    tmp = Voxel()
    S.house(tmp, -(w // 2), -(d // 2), w, d, HAVEN, floors=floors, roof="flat", wall=wall)
    v.merge(tmp, x, base - 1, z)
    dx, dz = x, z - (d // 2) + d - 1                                       # door (south face)
    v.set(dx - 1, base, dz + 1, "lantern")
    v.set(dx + 1, base, dz + 1, "lantern")
    v.fill(dx - 1, base + 3, dz + 1, dx + 1, base + 3, dz + 1, "dark_oak_stairs[facing=north,half=top]")
    top = base + floors * 4                                                # the flat roof slab
    if rng.random() < 0.5:                                                 # a smaller house stacked on the roof
        tmp = Voxel()
        S.house(tmp, -((w - 2) // 2), -((d - 2) // 2), w - 2, d - 2, HAVEN, floors=1, roof="flat",
                wall=rng.choice(("green_terracotta", "smooth_sandstone", "mud_bricks")))
        v.merge(tmp, x, top, z)
        v.set(x - 2, top + 1, z + (d - 2) - (d - 2) // 2, "lantern")
    else:
        v.set(x, top + 1, z, "lantern")
        v.set(x - (w // 2) + 1, top + 1, z + (d // 2) - 1, "barrel[facing=up]")
        v.fill(x + 1, top + 1, z - 1, x + 2, top + 1, z, "green_wool")   # drying awning


def _market_stall(v: Voxel, x: int, z: int, y: int, cloth: str, goods: str) -> None:
    for px in (x - 1, x + 1):
        for pz in (z - 1, z + 1):
            v.column(px, y, pz, 3, "dark_oak_fence")
    v.fill(x - 2, y + 3, z - 2, x + 2, y + 3, z + 2, cloth)
    v.fill(x - 1, y + 4, z - 1, x + 1, y + 4, z + 1, cloth)
    v.set(x, y + 2, z, HANGING)
    v.fill(x - 1, y, z + 1, x + 1, y, z + 1, "barrel[facing=up]")      # counter
    v.set(x, y, z, goods)
    v.set(x - 1, y, z - 1, "hay_block")


def _shrine(v: Voxel, cx: int, cz: int, y: int) -> None:
    """A small spirit shrine: stepped plinth, dark-oak frame, flared lime roof, amethyst altar."""
    v.fill(cx - 5, y, cz - 5, cx + 5, y, cz + 5, "polished_deepslate")
    v.fill(cx - 4, y + 1, cz - 4, cx + 4, y + 1, cz + 4, "polished_deepslate")
    v.fill(cx - 2, y + 1, cz + 5, cx + 2, y + 1, cz + 5, "polished_deepslate_stairs[facing=north,half=bottom]")
    v.walls(cx - 3, y + 2, cz - 3, cx + 3, y + 5, cz + 3, "green_terracotta")
    for px in (cx - 3, cx + 3):
        for pz in (cz - 3, cz + 3):
            v.column(px, y + 2, pz, 4, "dark_oak_log")
    v.fill(cx - 2, y + 2, cz - 2, cx + 2, y + 5, cz + 2, "air")
    v.fill(cx - 1, y + 2, cz + 3, cx + 1, y + 4, cz + 3, "air")                       # open front
    v.windows(cx - 3, y + 3, cz - 3, cx + 3, cz + 3, "glass_pane", period=2, offset=1)
    v.fill(cx - 2, y + 1, cz - 2, cx + 2, y + 1, cz + 2, "dark_oak_planks")
    v.pagoda_roof(cx, y + 6, cz, 5, "lime_terracotta", "polished_deepslate")
    v.walls(cx - 2, y + 7, cz - 2, cx + 2, y + 8, cz + 2, "green_terracotta")
    v.fill(cx - 1, y + 7, cz - 1, cx + 1, y + 8, cz + 1, "air")
    v.pagoda_roof(cx, y + 9, cz, 3, "lime_terracotta", "polished_deepslate")
    v.fill(cx, y + 10, cz, cx, y + 11, cz, "lime_terracotta")
    v.set(cx, y + 12, cz, "end_rod")
    v.set(cx, y + 2, cz - 1, "chiseled_deepslate")                                     # the altar
    v.set(cx, y + 3, cz - 1, "amethyst_cluster[facing=up]")
    v.set(cx - 1, y + 2, cz - 1, "candle[candles=3,lit=true]")
    v.set(cx + 1, y + 2, cz - 1, "candle[candles=3,lit=true]")
    for px in (cx - 4, cx + 4):
        for pz in (cz - 4, cz + 4):
            v.set(px, y + 5, pz, HANGING)
    # a dark-oak torii on the approach
    for px in (cx - 3, cx + 3):
        v.column(px, y + 1, cz + 8, 6, "dark_oak_log")
    v.fill(cx - 4, y + 7, cz + 8, cx + 4, y + 7, cz + 8, "dark_oak_log[axis=x]")
    v.fill(cx - 3, y + 5, cz + 8, cx + 3, y + 5, cz + 8, "dark_oak_planks")
    v.set(cx - 1, y + 6, cz + 8, HANGING)
    v.set(cx + 1, y + 6, cz + 8, HANGING)


def haven(v: Voxel) -> None:
    """A surviving haven: concentric earthbent walls, terraced farms, a spirit-lit core, and the wastes outside."""
    rng = random.Random(500)
    # ---- the wastes outside the wall: scrub ground, craters, cracks, dead trees, a road and a caravan
    S.pad(v, -90, -90, 90, 90, WASTE)
    _scrub(v, -90, -90, 90, 90, 501, skip=lambda x, z: x * x + z * z <= 72 * 72)
    for (x, z, r) in ((-70, 60, 14), (65, -55, 18), (-60, -70, 10)):
        _crater(v, x, z, r, 6, rim="blackstone")
    for _ in range(8):
        a = rng.uniform(0, 360)
        if 60 < a < 120:
            continue
        x, z = _pol(rng.uniform(76, 86), a)
        _fissure(v, rng, x, z, rng.randint(8, 16), limit=89, depth=2)
    for _ in range(12):
        a = rng.uniform(0, 360)
        if 65 < a < 115:
            continue
        x, z = _pol(rng.uniform(75, 87), a)
        if v.get(x, 0, z) != AIR and v.get(x, 1, z) is None:
            _dead_tree(v, x, z, rng)
    for a in (20, 150, 200, 330):                                            # spirit lights in the dark
        x, z = _pol(80, a)
        if v.get(x, 0, z) != AIR:
            _post(v, x, 1, z, 2, light="soul_lantern")
    v.fill(-3, 0, 71, 3, 0, 90, "andesite")                                   # the road to the gate
    v.fill(-4, 0, 71, -4, 0, 90, "gravel"); v.fill(4, 0, 71, 4, 0, 90, "gravel")
    for z in (75, 81, 87):
        _post(v, -5, 1, z, 3); _post(v, 5, 1, z, 3)
    # the scavenger caravan: ox-cart, tents, campfire and supplies
    v.fill(10, 2, 80, 15, 2, 83, "dark_oak_planks")
    v.walls(10, 3, 80, 15, 3, 83, "dark_oak_fence")
    for px in (11, 14):
        v.set(px, 1, 79, "stripped_dark_oak_log[axis=z]"); v.set(px, 1, 84, "stripped_dark_oak_log[axis=z]")
    v.fill(11, 5, 80, 14, 5, 83, "white_wool")
    v.fill(10, 4, 80, 10, 4, 83, "white_wool"); v.fill(15, 4, 80, 15, 4, 83, "white_wool")
    v.set(12, 4, 81, HANGING)
    v.fill(11, 3, 81, 13, 3, 82, "barrel[facing=up]"); v.set(14, 3, 81, "hay_block"); v.set(14, 3, 82, "chest[facing=south]")
    v.fill(12, 1, 77, 13, 1, 78, "dark_oak_fence")                            # the ox
    v.fill(11, 2, 76, 14, 3, 79, "brown_wool")
    v.fill(12, 3, 74, 13, 4, 75, "brown_wool"); v.set(11, 5, 74, "bone_block"); v.set(14, 5, 74, "bone_block")
    v.fill(12, 2, 79, 13, 2, 80, "dark_oak_fence")
    for tx in (8, 24):                                                        # two tents
        for i in range(3):
            v.fill(tx - 2 + i, 1 + i, 84, tx - 2 + i, 1 + i, 88, "orange_wool")
            v.fill(tx + 2 - i, 1 + i, 84, tx + 2 - i, 1 + i, 88, "orange_wool")
        v.fill(tx - 1, 1, 88, tx + 1, 1, 88, "orange_wool"); v.set(tx, 2, 88, "orange_wool")
    v.set(16, 1, 86, "campfire[lit=true]")
    v.fill(19, 1, 85, 20, 1, 86, "barrel[facing=up]"); v.set(19, 2, 85, "hay_block"); v.set(21, 1, 86, "hay_block")
    _post(v, 16, 1, 82, 2)

    # ---- the outer wall: two rings, string courses, walkway, merlons, slits, twelve towers, the gatehouse
    v.cylinder(0, 1, 0, 70, 14, "deepslate_bricks", hollow=True)
    v.cylinder(0, 1, 0, 69, 14, "deepslate_bricks", hollow=True)
    v.cylinder(0, 5, 0, 70, 1, "polished_deepslate", hollow=True)
    v.cylinder(0, 10, 0, 70, 1, "polished_deepslate", hollow=True)
    v.disc(0, 15, 0, 70, "polished_deepslate", hollow=True); v.disc(0, 15, 0, 69, "polished_deepslate", hollow=True)
    for a3 in range(0, 1080, 8):
        x, z = _pol(70, a3 / 3)
        v.set(x, 16, z, "deepslate_bricks")
    for a in range(5, 360, 10):
        if 80 < a < 100:
            continue
        x, z = _pol(70, a); v.set(x, 12, z, "air")
        x, z = _pol(69, a); v.set(x, 12, z, "air")
    for a in range(0, 360, 30):
        cx, cz = _pol(70, a)
        S.tower(v, cx, cz, 3, 18, HAVEN, top="flat", wall="deepslate_bricks")
        v.disc(cx, 19, cz, 3, "polished_deepslate", hollow=True)
        _post(v, cx, 19, cz, 2)
        ux, uz = round(math.cos(math.radians(a))), round(math.sin(math.radians(a)))
        if abs(ux) + abs(uz) == 1:                                            # banner on the four cardinal towers
            facing = {(1, 0): "east", (-1, 0): "west", (0, 1): "south", (0, -1): "north"}[(ux, uz)]
            v.set(cx + 4 * ux, 13, cz + 4 * uz, "green_wall_banner[facing=%s]" % facing)
    v.fill(-3, 1, 68, 3, 7, 71, "air")                                        # the gate
    v.fill(-4, 8, 68, 4, 9, 71, "polished_deepslate")
    v.set(0, 11, 70, "chiseled_deepslate"); v.set(0, 12, 70, "chiseled_deepslate")
    v.fill(-2, 6, 69, 2, 7, 69, "iron_bars")                                   # raised portcullis
    v.set(-3, 7, 69, HANGING); v.set(3, 7, 69, HANGING)
    for gx in (-6, 6):
        S.tower(v, gx, 70, 2, 20, HAVEN, top="crenel", wall="deepslate_bricks", square=True)
        v.fill(gx - 1, 8, 68, gx + 1, 9, 68, "glass_pane"); v.fill(gx - 1, 14, 68, gx + 1, 15, 68, "glass_pane")
        v.set(gx, 21, 70, "lantern")
        v.set(gx, 12, 73, "green_wall_banner[facing=south]")

    # ---- the ground inside: grass, four terraces of farmland with channels, hay, scarecrows and sheds
    v.disc(0, 0, 0, 68, "grass_block")
    crops = ("wheat[age=7]", "carrots[age=7]", "potatoes[age=7]", "beetroots[age=3]")
    for k in range(4):
        r, y = 60 - k * 6, 1 + k
        v.disc(0, y, 0, r, "grass_block"); v.disc(0, y, 0, r, "andesite", hollow=True)
        for a in range(0, 360, 3):
            for rr, crop in ((r - 2, crops[k]), (r - 4, crops[(k + 1) % 4])):
                x, z = _pol(rr, a)
                v.set(x, y, z, "farmland[moisture=7]"); v.set(x, y + 1, z, crop)
        for a3 in range(0, 1080, 2):                                         # the irrigation channel
            x, z = _pol(r - 3, a3 / 3)
            v.set(x, y, z, "water")
        for a in range(22, 360, 45):                                          # radial dirt paths
            for rr in range(r - 5, r + 1):
                x, z = _pol(rr, a)
                v.set(x, y, z, "dirt_path")
        for _ in range(3):
            x, z = _pol(r - 1, rng.uniform(0, 360))
            v.set(x, y + 1, z, "hay_block")
        x, z = _pol(r - 5, rng.uniform(100, 350))
        v.column(x, y + 1, z, 2, "oak_fence"); v.set(x - 1, y + 3, z, "oak_fence"); v.set(x + 1, y + 3, z, "oak_fence")
        v.set(x, y + 3, z, "hay_block"); v.set(x, y + 4, z, "carved_pumpkin[facing=south]")
    for a in (45, 135, 225, 315):                                             # farm sheds on the lowest terrace
        x, z = _pol(57, a)
        tmp = Voxel()
        S.house(tmp, -2, -2, 5, 5, HAVEN, floors=1, roof="gable", wall="mud_bricks", windows=False)
        v.merge(tmp, x, 1, z)
        v.set(x + 1, 2, z + 3, "lantern"); v.set(x - 2, 2, z + 3, "composter")
    for a in (45, 135, 225, 315):                                             # cisterns under pergolas
        x, z = _pol(45, a)
        v.disc(x, 4, z, 4, "polished_deepslate"); v.disc(x, 5, z, 4, "polished_deepslate", hollow=True)
        v.disc(x, 3, z, 3, "polished_deepslate"); v.set(x, 3, z, "sea_lantern")
        v.disc(x, 4, z, 3, "water"); v.disc(x, 5, z, 3, "water")
        for px in (x - 4, x + 4):
            for pz in (z - 4, z + 4):
                v.column(px, 4, pz, 5, "dark_oak_fence")
        v.fill(x - 4, 9, z - 4, x + 4, 9, z + 4, "dark_oak_slab[type=bottom]")
        v.set(x, 8, z, HANGING)
    for a in range(0, 360, 20):                                               # orchard ring by the wall
        if 60 <= a <= 120:
            continue
        x, z = _pol(64, a)
        v.tree(x, 1, z, "oak_log", "oak_leaves[persistent=true]", height=rng.randint(5, 7), canopy=2)
    for a in (30, 150, 210, 330):
        x, z = _pol(51, a)
        v.tree(x, 3, z, "birch_log", "birch_leaves[persistent=true]", height=5, canopy=2)

    # ---- the town plateau, inner wall with four gates, avenues with stairs and lamp posts
    v.disc(0, 5, 0, 36, "andesite")
    v.disc(0, 5, 0, 27, "polished_andesite"); v.disc(0, 5, 0, 24, "andesite")
    v.cylinder(0, 5, 0, 38, 5, "deepslate_bricks", hollow=True)
    v.disc(0, 10, 0, 38, "polished_deepslate", hollow=True)
    for a3 in range(0, 1080, 12):
        x, z = _pol(38, a3 / 3); v.set(x, 11, z, "deepslate_bricks")
    for a in range(15, 360, 30):
        x, z = _pol(38, a); v.set(x, 11, z, "lantern")
    for ux, uz in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        v.fill(min(ux * 36, ux * 40) if ux else -2, 5, min(uz * 36, uz * 40) if uz else -2,
               max(ux * 36, ux * 40) if ux else 2, 8, max(uz * 36, uz * 40) if uz else 2, "air")   # the inner gate
        for r in range(17, 61):                                               # paving at terrace height
            y = _terrace_y(r)
            for s in (-2, -1, 0, 1, 2):
                x, z = (ux * r + (s if uz else 0)), (uz * r + (s if ux else 0))
                v.set(x, y, z, "stone_bricks")
        for r in (37, 43, 49, 55, 61):                                        # a stair at each terrace rise
            y = _terrace_y(r)
            facing = {(0, 1): "north", (0, -1): "south", (1, 0): "west", (-1, 0): "east"}[(ux, uz)]
            for s in (-2, -1, 0, 1, 2):
                x, z = (ux * r + (s if uz else 0)), (uz * r + (s if ux else 0))
                v.set(x, y + 1, z, "stone_brick_stairs[facing=%s,half=bottom]" % facing)
        for r in range(20, 60, 7):                                            # lamp posts
            y = _terrace_y(r)
            for s in (-3, 3):
                x, z = (ux * r + (s if uz else 0)), (uz * r + (s if ux else 0))
                _post(v, x, y + 1, z, 3)
    for ux, uz in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        for s in (-3, 3):
            x, z = (ux * 38 + (s if uz else 0)), (uz * 38 + (s if ux else 0))
            v.set(x, 11, z, "lantern")
    v.fill(-3, 0, 61, 3, 0, 67, "stone_bricks")                                # gate yard

    # ---- the town: two rings of layered houses, a market square and the shrine on the north terrace
    walls = ("deepslate_bricks", "green_terracotta", "smooth_sandstone", "mud_bricks")
    for a in range(15, 360, 30):
        if a in (75, 105):                                                    # the market takes their place
            continue
        x, z = _pol(30, a)
        _haven_house(v, x, z, rng.randint(7, 9), rng.randint(6, 8), rng.randint(1, 2), rng.choice(walls), rng, base=6)
    for a in (22, 157, 202, 247, 292, 337):
        x, z = _pol(22, a)
        _haven_house(v, x, z, rng.randint(5, 7), rng.randint(5, 6), 1, rng.choice(walls), rng, base=6)
    v.fill(-12, 5, 17, 12, 5, 34, "polished_andesite")                         # the market along the south avenue
    for (x, z, cloth, goods) in ((-8, 20, "lime_wool", "melon"), (8, 20, "green_wool", "pumpkin"),
                                 (-8, 26, "white_wool", "hay_block"), (8, 26, "orange_wool", "barrel[facing=up]"),
                                 (-8, 32, "brown_wool", "composter"), (8, 32, "lime_wool", "chest[facing=south]")):
        _market_stall(v, x, z, 6, cloth, goods)
    v.column(-4, 6, 29, 3, "dark_oak_fence"); v.set(-4, 9, 29, "bell[attachment=floor,facing=south]")
    v.set(4, 6, 29, "lantern")
    _shrine(v, 0, -46, 5)

    # ---- the core: a spirit crystal on a stepped plinth in a lantern-lit moat with four bridges
    v.disc(0, 4, 0, 16, "polished_deepslate")
    v.disc(0, 5, 0, 16, "water"); v.disc(0, 5, 0, 13, "polished_deepslate")
    for a in range(0, 360, 30):
        x, z = _pol(15, a); v.set(x, 4, z, "sea_lantern")
    for ux, uz in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        v.fill(ux * 13 - (1 if uz else 0), 5, uz * 13 - (1 if ux else 0), ux * 17 + (1 if uz else 0), 5, uz * 17 + (1 if ux else 0), "polished_deepslate")
        for r in (13, 17):
            for s in (-2, 2):
                x, z = (ux * r + (s if uz else 0)), (uz * r + (s if ux else 0))
                _post(v, x, 6, z, 1, fence="polished_deepslate_wall")
    for k in range(5):
        v.disc(0, 6 + k, 0, 12 - k * 2, "polished_deepslate")
    for a in (45, 135, 225, 315):
        x, z = _pol(10, a)
        v.column(x, 8, z, 4, "polished_deepslate_wall"); v.set(x, 12, z, "end_rod")
    v.fill(-2, 11, -2, 2, 22, 2, "amethyst_block"); v.fill(-1, 23, -1, 1, 26, 1, "amethyst_block")
    for (x, y, z) in ((2, 13, 0), (-2, 16, 1), (0, 14, 2), (1, 19, -2), (-1, 21, 2), (2, 12, -1)):
        v.set(x, y, z, "budding_amethyst")
    for (x, y, z, f) in ((3, 14, 0, "east"), (-3, 17, 1, "west"), (0, 15, 3, "south"), (1, 20, -3, "north"), (3, 19, -1, "east")):
        v.set(x, y, z, "amethyst_cluster[facing=%s]" % f)
    v.set(0, 27, 0, "end_rod"); v.set(0, 11, 0, "sea_lantern")
    for a in range(0, 360, 90):
        x, z = _pol(4, a); v.set(x, 11, z, "lantern")
    for a in range(0, 360, 45):
        x, z = _pol(6, a); v.set(x, 10, z, "sea_lantern")


# ------------------------------------------------------------------ wastes

def _ruined_tower(v: Voxel, x: int, z: int, w: int, h: int, rng: random.Random,
                  wall: str = "light_gray_concrete", floor: str = "gray_concrete") -> None:
    """A gutted high-rise: floors, blown-out windows, a bite out of one side, a crumbling crown, debris."""
    x2, z2 = x + w - 1, z + w - 1
    v.walls(x, 1, z, x2, h, z2, wall)
    v.fill(x + 1, 1, z + 1, x2 - 1, h, z2 - 1, "air")
    for y0 in range(1, h, 4):
        v.fill(x + 1, y0, z + 1, x2 - 1, y0, z2 - 1, floor)
        for yy in (y0 + 1, y0 + 2):
            v.windows(x, yy, z, x2, z2, "air", period=2, offset=1)
    v.set(x + 2, h // 2 - (h // 2 - 1) % 4 + 1, z + 2, "campfire[lit=true]")           # a squatter's fire
    bx, by, bz = rng.choice((x, x2)), int(h * 0.6), rng.randint(z + 2, z2 - 2)
    for px in range(bx - 4, bx + 5):
        for py in range(by - 4, by + 5):
            for pz in range(bz - 4, bz + 5):
                if (px - bx) ** 2 + (py - by) ** 2 + (pz - bz) ** 2 <= 16:
                    _erase(v, px, py, pz)
    for py in range(h - 7, h + 1):
        p = (py - (h - 8)) / 9
        for px in range(x, x2 + 1):
            for pz in range(z, z2 + 1):
                if (px in (x, x2) or pz in (z, z2)) and rng.random() < p:
                    _erase(v, px, py, pz)
    for _ in range(5):
        px, pz = rng.choice((x, x2)), rng.choice((z, z2))
        v.column(px, h + 1, pz, rng.randint(1, 3), "iron_bars")
    for _ in range(24):
        px, pz = rng.randint(x - 5, x2 + 5), rng.randint(z - 5, z2 + 5)
        if x <= px <= x2 and z <= pz <= z2:
            continue
        if abs(px) > 89 or abs(pz) > 89:
            continue
        v.set(px, 1, pz, rng.choice((wall, floor, "cobbled_deepslate", "iron_bars")))
        if rng.random() < 0.3:
            v.set(px, 2, pz, rng.choice((wall, floor)))


def _fallen_section(v: Voxel, x: int, z: int, length: int, w: int, rng: random.Random,
                    wall: str = "light_gray_concrete") -> None:
    """The top of a tower lying on its side: a square tube along x, cracked and sagging."""
    for i in range(length):
        if rng.random() < 0.12:
            continue
        px = x + i
        v.fill(px, 1, z, px, w, z, wall); v.fill(px, 1, z + w - 1, px, w, z + w - 1, wall)
        v.fill(px, 1, z, px, 1, z + w - 1, wall); v.fill(px, w, z, px, w, z + w - 1, wall)
        if i % 4 == 2:
            v.fill(px, 3, z, px, 4, z, "air"); v.fill(px, 3, z + w - 1, px, 4, z + w - 1, "air")
        if i % 4 == 0 and i > 0:
            v.fill(px, 2, z + 1, px, w - 1, z + w - 2, "gray_concrete"); v.fill(px, 2, z + 2, px, w - 1, z + w - 3, "air")
    v.cone(x + length + 3, 1, z + w // 2, 5, 4, "gray_concrete_powder")
    v.set(x + 2, 2, z + w // 2, "campfire[lit=true]")


def _airship(v: Voxel, x0: int, z0: int, rng: random.Random, crater) -> None:
    """A Republic-era airship nosed into its own impact crater: torn plating over iron ribs, tail in the air."""
    L, R = 44, 7
    cx, cz, cr, cd = crater
    for i in range(L + 1):
        t = i / L
        rr = R * math.sqrt(max(0.0, 1 - ((t - 0.5) / 0.5) ** 2))
        cy = round(-3 + 14 * t)
        x = x0 + i
        rib = i % 5 == 0
        for dy in range(-R - 1, R + 2):
            for dz in range(-R - 1, R + 2):
                d = math.hypot(dy, dz)
                if not (rr - 1 < d <= rr + 0.2) and not (rr <= 0.6 and d <= 0.6):
                    continue
                y, z = cy + dy, z0 + dz
                if y < -7:
                    continue
                torn = (t < 0.3 and rng.random() < 0.4) or (0.42 < t < 0.68 and dy > 1 and dz > 1)
                if torn and not rib:
                    continue
                if rib or dy == -round(rr):
                    block = "iron_block"
                elif (dy + dz) % 7 == 0:
                    block = "light_gray_concrete"
                else:
                    block = "gray_concrete"
                v.set(x, y, z, block)
        v.set(x, cy, z0, "iron_block")                                             # keel girder
        if i % 8 == 4 and rr > 2:
            v.set(x, cy - 1, z0, SOUL_HANGING)
        if 14 <= i <= 30 and rr > 3:                                               # the gondola, crushed at the nose
            gy = cy - round(rr) - 3
            v.fill(x, max(gy, -7), z0 - 2, x, max(gy + 2, -7), z0 + 2, "dark_oak_planks")
            if i % 3 == 0:
                v.set(x, max(gy + 1, -7), z0 - 2, "glass_pane"); v.set(x, max(gy + 1, -7), z0 + 2, "glass_pane")
            if i == 22:
                v.set(x, max(gy + 1, -7), z0, "lantern")
    # tail fins and the propeller
    for i in range(L - 9, L + 1):
        t = i / L
        rr = R * math.sqrt(max(0.0, 1 - ((t - 0.5) / 0.5) ** 2))
        cy = round(-3 + 14 * t)
        k = (i - (L - 9)) // 2 + 1
        x = x0 + i
        v.fill(x, cy + round(rr), z0, x, cy + round(rr) + k, z0, "red_terracotta")
        v.fill(x, cy, z0 + round(rr), x, cy, z0 + round(rr) + k, "red_terracotta")
        v.fill(x, cy, z0 - round(rr) - k, x, cy, z0 - round(rr), "red_terracotta")
    px, py = x0 + L + 1, 11
    v.set(px, py, z0, "iron_block")
    for k in range(1, 5):
        v.set(px, py + k, z0, "iron_bars"); v.set(px, py - k, z0, "iron_bars")
        v.set(px, py, z0 + k, "iron_bars"); v.set(px, py, z0 - k, "iron_bars")
    # chains, fires and scattered wreckage on the crater floor
    for i in (18, 24):
        x = x0 + i
        rr = R * math.sqrt(max(0.0, 1 - ((i / L - 0.5) / 0.5) ** 2))
        top = round(-3 + 14 * i / L) - round(rr) - 4
        floor = _crater_floor(cx, cz, cr, cd, x, z0 + 3)
        v.fill(x, floor + 1, z0 + 3, x, min(top, floor + 6), z0 + 3, "chain[axis=y]")
    for _ in range(40):
        x, z = rng.randint(cx - cr + 2, cx + cr - 2), rng.randint(cz - cr + 2, cz + cr - 2)
        if (x - cx) ** 2 + (z - cz) ** 2 > (cr - 2) ** 2:
            continue
        y = _crater_floor(cx, cz, cr, cd, x, z) + 1
        if v.get(x, y, z) is not None and v.get(x, y, z) != AIR:
            continue
        v.set(x, y, z, rng.choice(("gray_concrete", "iron_block", "red_terracotta", "light_gray_concrete", "campfire[lit=true]", "iron_bars")))


def _skeleton(v: Voxel, x0: int, z0: int, length: int, rng: random.Random) -> None:
    """A spirit-beast's bones half sunk in the ash: spine, ribcage, skull, a few limbs."""
    for i in range(length + 1):
        ys = 4 + round(4 * math.sin(math.pi * i / length))
        v.set(x0 + i, ys, z0, "bone_block[axis=x]")
        if i % 4 == 2 and i < length - 4:
            r = ys - 1
            pts = []
            for a in range(0, 181, 15):
                pts.append((x0 + i, 1 + round(r * math.sin(math.radians(a))), z0 + round(r * math.cos(math.radians(a)))))
            for p, q in zip(pts, pts[1:]):
                v.line(p, q, "bone_block[axis=z]")
            v.set(x0 + i, ys, z0, "bone_block[axis=x]")
    sx = x0 + length + 1
    v.fill(sx, 1, z0 - 3, sx + 7, 6, z0 + 3, "bone_block")                          # skull
    v.fill(sx + 8, 1, z0 - 2, sx + 9, 3, z0 + 2, "bone_block")                      # snout
    v.fill(sx + 5, 4, z0 - 4, sx + 6, 5, z0 - 3, "air"); v.fill(sx + 5, 4, z0 + 3, sx + 6, 5, z0 + 4, "air")   # eye sockets
    v.fill(sx + 1, 1, z0 - 4, sx + 9, 1, z0 + 4, "air"); v.fill(sx + 1, 1, z0 - 1, sx + 9, 1, z0 + 1, "bone_block")  # jaw gap
    for z in (z0 - 3, z0 + 3):
        v.fill(sx + 2, 1, z, sx + 9, 1, z, "bone_block")
    v.set(sx + 5, 4, z0 - 3, "soul_lantern"); v.set(sx + 5, 4, z0 + 3, "soul_lantern")
    v.line((x0 + 6, 3, z0), (x0 - 2, 1, z0 + 9), "bone_block[axis=z]")
    v.line((x0 + 6, 3, z0), (x0 - 1, 1, z0 - 9), "bone_block[axis=z]")
    v.line((x0 + length - 6, 4, z0), (x0 + length - 1, 1, z0 + 10), "bone_block[axis=z]")
    for _ in range(14):
        v.set(max(-89, x0 + rng.randint(-6, length + 14)), 1, z0 + rng.randint(-14, 14), "bone_block[axis=%s]" % rng.choice("xyz"))


def wastes(v: Voxel) -> None:
    """The cataclysm's aftermath: a fallen city half buried in ash, cracked earth, a spirit-corrupted vine field and a cold portal."""
    rng = random.Random(510)
    S.pad(v, -90, -90, 90, 90, WASTE)
    _scrub(v, -90, -90, 90, 90, 511)
    n1, n2 = _noise(513, 10), _noise(514, 5)
    for x in range(-90, 91):                                                       # ash drifts and dunes in the north
        for z in range(-90, -58):
            if n2(x, z) > (z + 90) / 36:
                v.set(x, 0, z, "gray_concrete_powder")
                h = int(5 * (n1(x, z) - 0.45)) if z < -68 else 0
                if h > 0:
                    v.fill(x, 1, z, x, h, z, "gray_concrete_powder")
    for _ in range(14):                                                            # lava-veined fissures
        _fissure(v, rng, rng.uniform(-80, 80), rng.uniform(-80, 80), rng.randint(18, 45))
    craters = ((40, 40, 26, 8), (-50, -30, 18, 8), (10, -60, 12, 6))
    for (x, z, r, d) in craters:
        _crater(v, x, z, r, d, rim="blackstone")
    # the ruined road from the south edge, ending at a crater lip
    for z in range(-46, 89):
        for x in range(-2, 3):
            if v.get(x, 0, z) == AIR:
                continue
            b = n2(x * 3, z)
            v.set(x, 0, z, "gravel" if b < 0.15 else "cracked_stone_bricks" if b < 0.35 else "cobblestone" if b > 0.88 else "stone_bricks")
        if z % 10 == 0:
            for lx in (-4, 4):
                h = rng.choice((1, 2, 3, 3, 3))
                v.column(lx, 1, z, h, "stripped_dark_oak_log")
                if h == 3:
                    v.set(lx, 4, z, "lantern" if rng.random() < 0.5 else "iron_bars")
    # the dead city: five gutted towers, one of them snapped and lying across the plain
    _ruined_tower(v, -72, 20, 12, 34, rng)
    _fallen_section(v, -58, 21, 30, 10, rng)
    _ruined_tower(v, -50, 55, 10, 26, rng, wall="gray_concrete", floor="light_gray_concrete")
    _ruined_tower(v, -24, 68, 14, 40, rng)
    _ruined_tower(v, 62, -25, 10, 30, rng, wall="light_gray_terracotta", floor="gray_concrete")
    _ruined_tower(v, -26, -24, 16, 20, rng, wall="gray_concrete")
    v.dome(-18, 21, -16, 7, "gray_concrete")                                         # the hall's broken dome
    for px in range(-25, -11):
        for py in range(21, 29):
            for pz in range(-23, -9):
                if (px + 14) ** 2 + (py - 24) ** 2 + (pz + 12) ** 2 <= 20:
                    _erase(v, px, py, pz)
    v.set(-18, 14, -16, "soul_lantern")
    # the crashed airship in the great crater
    _airship(v, 20, 40, rng, craters[0])
    # the dead portal standing in the second crater
    pcx, pcz = -50, -30
    v.fill(pcx - 1, -7, pcz - 1, pcx + 1, -7, pcz + 1, "obsidian")
    for a in range(0, 360, 5):
        x, y = pcx + round(6 * math.cos(math.radians(a))), -1 + round(6 * math.sin(math.radians(a)))
        v.set(x, y, pcz, "crying_obsidian" if a % 15 == 0 else "obsidian")
    v.set(pcx, -1, pcz, "end_rod")
    for a in (30, 150, 270):
        x, z = pcx + round(11 * math.cos(math.radians(a))), pcz + round(11 * math.sin(math.radians(a)))
        y = _crater_floor(pcx, pcz, 18, 8, x, z) + 1
        h = rng.randint(2, 5)
        v.column(x, y, z, h, "obsidian"); v.set(x, y + h, z, "soul_lantern")
    # a half-buried mecha, one arm still raised, its core still warm
    v.fill(-34, 1, 0, -26, 6, 10, "iron_block")
    for _ in range(30):
        px, pz = rng.randint(-34, -26), rng.randint(0, 10)
        v.set(px, 6, pz, rng.choice(("oxidized_copper", "weathered_copper")))
    v.fill(-34, 1, 0, -34, 6, 0, "oxidized_copper"); v.fill(-26, 1, 10, -26, 6, 10, "weathered_copper")
    v.fill(-31, 7, 3, -29, 9, 7, "iron_block"); v.set(-30, 8, 3, "sea_lantern")
    for i in range(10):
        v.fill(-25 + i, 4 + i // 2, 4, -25 + i, 5 + i // 2, 6, "iron_block")
    v.fill(-15, 9, 3, -13, 11, 7, "iron_block")
    v.set(-30, 7, 9, "campfire[lit=true]"); v.set(-33, 7, 1, "soul_lantern")
    # corrupted spirit vines in the east, glowing
    for _ in range(28):
        x, z = rng.randint(44, 87), rng.randint(-78, -30)
        if 60 <= x <= 74 and -27 <= z <= -13 or v.get(x, 0, z) == AIR:
            continue
        h = rng.randint(3, 10)
        v.column(x, 1, z, h, "crimson_stem")
        v.sphere(x, 1 + h, z, 1.5, "nether_wart_block", hollow=False)
        v.set(x, 2 + h, z, "shroomlight")
        v.set(x + 1, h - 1, z, "weeping_vines_plant"); v.set(x + 1, h - 2, z, "weeping_vines")
    # the spirit-beast's bones in the ash, and a ruined boundary wall
    _skeleton(v, -84, -58, 36, rng)
    S.ruined_wall(v, 20, 70, 50, block="deepslate_bricks", seed=511)
    S.ruined_wall(v, 50, -85, 32, block="cracked_deepslate_bricks", seed=512)
    # dead trees and scattered spirit lights wherever the ground is free
    def free(x, z):
        return v.get(x, 1, z) is None and v.get(x, 0, z) not in (None, AIR) and (x - 40) ** 2 + (z - 40) ** 2 > 31 ** 2
    placed = 0
    while placed < 16:
        x, z = rng.randint(-86, 86), rng.randint(-86, 86)
        if free(x, z) and all(v.get(x + dx, 2, z + dz) is None for dx in (-2, 2) for dz in (-2, 2)):
            _dead_tree(v, x, z, rng); placed += 1
    placed = 0
    while placed < 34:
        x, z = rng.randint(-86, 86), rng.randint(-86, 86)
        if not free(x, z):
            continue
        kind = rng.random()
        if kind < 0.4:
            _post(v, x, 1, z, rng.randint(1, 2), light="soul_lantern")
        elif kind < 0.7:
            y = rng.randint(2, 5)
            v.set(x, y, z, "light_blue_stained_glass"); v.set(x, y + 1, z, "end_rod")
            v.set(x + 1, y, z, "end_rod[facing=east]"); v.set(x - 1, y, z, "end_rod[facing=west]")
        elif kind < 0.85:
            v.set(x, 0, z, "soul_soil"); v.set(x, 1, z, "soul_fire")
        else:
            v.set(x, 1, z, "amethyst_block"); v.set(x, 2, z, "amethyst_cluster[facing=up]")
        placed += 1


# --------------------------------------------------------------------- map

_HAVENS = (("packed_ice", "light_blue_stained_glass"), ("red_terracotta", "red_stained_glass"),
           ("green_terracotta", "green_stained_glass"), ("smooth_quartz", "white_stained_glass"),
           ("light_gray_concrete", "light_gray_stained_glass"), ("sandstone", "yellow_stained_glass"),
           ("iron_block", "cyan_stained_glass"))
_BANDS = ("tuff", "coarse_dirt", "gravel", "stone", "andesite", "cobbled_deepslate", "deepslate", "snow_block")


def seven_havens_map(v: Voxel) -> None:
    """A 1:12 model of the whole post-cataclysm world: seven havens as walled circles across a scarred continent."""
    rng = random.Random(520)
    S.pad(v, -80, -80, 80, 80, "water")
    v.fill(-80, -3, -80, 80, -1, 80, "water")
    RX, RZ = 72, 60
    n1, n2 = _noise(521, 14), _noise(522, 6)
    H = {}

    def massif(x, z, mx, mz, s):
        return math.exp(-((x - mx) ** 2 + (z - mz) ** 2) / (s * s))

    for x in range(-76, 77):                                                       # relief: banded by height
        for z in range(-64, 65):
            e = 1 - (x / RX) ** 2 - (z / RZ) ** 2
            if e <= -0.06:
                continue
            if e <= 0:
                v.set(x, -1, z, "sand"); continue
            v.fill(x, -3, z, x, -1, z, "stone")
            n = n1(x, z) * 0.7 + n2(x, z) * 0.3
            h = 7 * (n - 0.3) * min(1.0, e * 2.5) + 3.5 * massif(x, z, -28, -24, 22) + 2.5 * massif(x, z, 46, 8, 14)
            h = max(0, min(7, int(round(h))))
            if e < 0.05 and h == 0:
                v.set(x, 0, z, "sand")
            else:
                v.set(x, 0, z, _BANDS[0] if h == 0 else "stone")
            for y in range(1, h + 1):
                v.set(x, y, z, _BANDS[h] if y == h else "stone")
            H[(x, z)] = h

    for (x, z, r) in ((-70, 70, 4), (72, -66, 3), (-74, -60, 3)):                     # islets
        v.disc(x, 0, z, r, "sand")

    # ---- the epicentre: a crater with the shard, a crying-obsidian ring, blackstone scars
    for (x, z), h in list(H.items()):
        if x * x + z * z <= 16 * 16:
            for y in range(1, h + 1):
                _erase(v, x, y, z)
            H[(x, z)] = 0
    _crater(v, 0, 0, 14, 4)
    for a in range(0, 360, 4):
        x, z = _pol(15, a)
        v.set(x, H.get((x, z), 0) + 1, z, "crying_obsidian" if a % 12 == 0 else "obsidian")
    for a in range(0, 360, 45):
        for r in range(17, 29):
            x, z = _pol(r, a)
            if (x, z) in H:
                v.set(x, H[(x, z)], z, "blackstone")
        x, z = _pol(15, a + 22)
        v.set(x, H.get((x, z), 0) + 2, z, "soul_lantern")
    v.fill(-1, -3, -1, 1, 12, 1, "amethyst_block"); v.set(0, 13, 0, "end_rod")
    for a in (0, 90, 180, 270):
        x, z = _pol(6, a)
        v.column(x, -2, z, 5, "amethyst_block"); v.set(x, 3, z, "amethyst_cluster[facing=up]")

    # ---- the seven havens: flattened plateaus, coloured walls, towers, a glowing column, little houses
    centres = []
    for i, (block, glass) in enumerate(_HAVENS):
        a = i * 360 / 7
        cx, cz = round(44 * math.cos(math.radians(a))), round(36 * math.sin(math.radians(a)))
        hh = max(1, H.get((cx, cz), 1))
        centres.append((cx, cz, hh))
        for x in range(cx - 10, cx + 11):
            for z in range(cz - 10, cz + 11):
                if (x - cx) ** 2 + (z - cz) ** 2 > 10 * 10 or (x, z) not in H:
                    continue
                for y in range(hh + 1, H[(x, z)] + 1):
                    _erase(v, x, y, z)
                for y in range(1, hh + 1):
                    v.set(x, y, z, "grass_block" if y == hh else "stone")
                H[(x, z)] = hh
        v.disc(cx, hh + 1, cz, 9, block, hollow=True); v.disc(cx, hh + 2, cz, 9, block, hollow=True)
        ga = math.degrees(math.atan2(-cz, -cx))                                     # gate faces the centre
        for da in (-7, 0, 7):
            x, z = _pol(9, ga + da)
            _erase(v, cx + x, hh + 1, cz + z); _erase(v, cx + x, hh + 2, cz + z)
        for ux, uz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            tx, tz = cx + 9 * ux, cz + 9 * uz
            v.fill(tx - 1, hh + 1, tz - 1, tx, hh + 4, tz, block); v.set(tx, hh + 5, tz, "lantern")
        v.fill(cx - 1, hh + 1, cz - 1, cx + 1, hh + 4, cz + 1, block)
        v.set(cx, hh + 5, cz, "sea_lantern"); v.fill(cx, hh + 6, cz, cx, hh + 8, cz, glass); v.set(cx, hh + 9, cz, "end_rod")
        for _ in range(7):
            hx, hz = cx + rng.randint(-6, 5), cz + rng.randint(-6, 5)
            if abs(hx - cx) <= 2 and abs(hz - cz) <= 2 or (hx - cx) ** 2 + (hz - cz) ** 2 > 49:
                continue
            v.fill(hx, hh + 1, hz, hx + 1, hh + 2, hz + 1, "stone_bricks")
            v.fill(hx, hh + 3, hz, hx + 1, hh + 3, hz + 1, "spruce_slab[type=bottom]")
        v.set(cx + 3, hh + 1, cz + 3, "lantern")

    # ---- rivers from the crater to the coast, cut one block into the relief
    for a in (40, 150, 230, 320):
        d = math.radians(a)
        px, pz = 17 * math.cos(d), 17 * math.sin(d)
        for _ in range(100):
            d += rng.uniform(-0.3, 0.3) + 0.08 * ((math.radians(a) - d))
            px += math.cos(d); pz += math.sin(d)
            cells = ((round(px), round(pz)), (round(px) + (1 if abs(math.sin(d)) > 0.7 else 0), round(pz) + (0 if abs(math.sin(d)) > 0.7 else 1)))
            if cells[0] not in H:
                break
            for (x, z) in cells:
                if (x, z) not in H or any((x - cx) ** 2 + (z - cz) ** 2 <= 100 for cx, cz, _ in centres):
                    continue
                h = H[(x, z)]
                _erase(v, x, h, z)
                v.set(x, h - 1, z, "water")

    # ---- routes between the havens (ring plus two crossings), lantern posts, plank fords
    links = [(i, (i + 1) % 7) for i in range(7)] + [(0, 3), (1, 5)]
    for i, j in links:
        (ax, az, _), (bx, bz, _) = centres[i], centres[j]
        n = max(abs(bx - ax), abs(bz - az))
        for k in range(n + 1):
            x, z = round(ax + (bx - ax) * k / n), round(az + (bz - az) * k / n)
            if (x, z) not in H:
                continue
            gate = False
            for cx, cz, hh in centres:
                d2 = (x - cx) ** 2 + (z - cz) ** 2
                if d2 < 72:
                    gate = True
                elif d2 <= 90:                                                 # the route pierces the wall
                    _erase(v, x, hh + 1, z); _erase(v, x, hh + 2, z); v.set(x, hh, z, "dirt_path"); gate = True
            if gate:
                continue
            h = H[(x, z)]
            if v.get(x, h - 1, z) == "minecraft:water" and v.get(x, h, z) is None:
                v.set(x, h, z, "oak_planks")
            else:
                v.set(x, h, z, "dirt_path")
            if k % 11 == 5 and (x + 1, z) in H:
                _post(v, x + 1, H[(x + 1, z)] + 1, z, 1, fence="oak_fence")

    # ---- the viewing platform on an islet off the south coast, reached by a jetty
    v.disc(0, 0, 70, 5, "sand"); v.disc(0, -1, 70, 5, "stone"); v.disc(0, -2, 70, 5, "stone"); v.disc(0, -3, 70, 5, "stone")
    v.cylinder(0, 1, 70, 3.5, 14, "deepslate_bricks", hollow=True)
    v.disc(0, 1, 70, 3, "polished_deepslate")
    v.fill(0, 1, 66, 0, 2, 66, "air")                                              # door on the jetty side
    v.fill(0, 2, 73, 0, 15, 73, "ladder[facing=north]")
    v.cylinder(0, 7, 70, 3.5, 1, "polished_deepslate", hollow=True)
    v.disc(0, 15, 70, 7, "dark_oak_planks"); _erase(v, 0, 15, 73)
    v.disc(0, 16, 70, 7, "dark_oak_fence", hollow=True)
    for a in range(0, 360, 45):
        x, z = _pol(7, a); v.set(x, 17, 70 + z, "lantern")
    v.set(0, 15, 64, "white_concrete"); v.set(-1, 15, 65, "white_concrete"); v.set(1, 15, 65, "white_concrete")   # north arrow
    for i, (block, glass) in enumerate(_HAVENS):                                     # the legend
        x = -6 + 2 * i
        v.set(x, 16, 72, block); v.set(x, 17, 72, glass)
    v.column(0, 16, 70, 2, "dark_oak_fence"); v.set(0, 18, 70, "sea_lantern")
    for z in range(57, 66):
        v.fill(-1, 1, z, 1, 1, z, "oak_planks")
        if z % 4 == 1:
            v.set(-2, 0, z, "oak_fence"); v.set(2, 0, z, "oak_fence")
            v.set(-2, 1, z, "oak_fence"); v.set(2, 1, z, "oak_fence"); v.set(-2, 2, z, "lantern"); v.set(2, 2, z, "lantern")


WORLD = World(
    id="seven_havens",
    name="Avatar: Seven Havens",
    game="Avatar: Seven Havens (announced 2025; stylised interpretation)",
    era="after Korra: the post-cataclysm age of Avatar Pavi",
    description="A world reduced to seven havens: one haven in full, the wastes between them, and a scale map of all seven.",
    franchise="Avatar",
).build(Build("haven", "A Haven", "Concentric earthbent walls with twelve towers, terraced farms, a ring of houses and the spirit crystal core in its moat; wastes and craters outside the gate.", haven)
).build(Build("wastes", "The Wastes", "Cracked, lava-veined ground, toppled skyscrapers, ash drifts, corrupted spirit vines and a dead portal.", wastes)
).build(Build("seven_havens_map", "Seven Havens Map", "1:12 model of the scarred continent with seven walled havens linked by roads around the epicentre.", seven_havens_map, "1 block = 12 m"))
