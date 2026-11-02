"""The Legend of Korra (2012-2014) - 170-174 AG."""

import math
import random

from .. import structures as S
from ..palettes import _p
from ..registry import Build, World
from ..voxel import Voxel

CITY = _p(ground="stone", wall="light_gray_concrete", wall2="smooth_quartz", trim="gold_block", roof="deepslate_tiles",
          floor="polished_andesite", column="quartz_pillar", path="gray_concrete", light="lantern")
AIR = _p(ground="stone", wall="smooth_quartz", wall2="orange_terracotta", trim="orange_terracotta", roof="light_blue_terracotta",
         floor="smooth_quartz", column="quartz_pillar", path="stone", leaves="cherry_leaves[persistent=true]", log="cherry_log")
METAL = _p(ground="iron_block", wall="iron_block", wall2="cut_copper", trim="lime_terracotta", roof="iron_block",
           floor="polished_deepslate", column="iron_block", path="polished_deepslate")


_TRIM = {                      # tower wall -> (stairs, slab) used for cornices, parapets, floors and crowns
    "light_gray_concrete": ("smooth_quartz_stairs", "smooth_quartz_slab"),
    "white_concrete": ("polished_andesite_stairs", "polished_andesite_slab"),
    "smooth_quartz": ("cut_copper_stairs", "cut_copper_slab"),
    "light_gray_terracotta": ("smooth_sandstone_stairs", "smooth_sandstone_slab"),
}


def _cornice(v: Voxel, x1: int, y: int, z1: int, x2: int, z2: int, stairs: str, slab: str) -> None:
    """Inverted stairs hugging the outside of the wall ring x1..x2 / z1..z2 at height ``y``."""
    v.fill(x1, y, z1 - 1, x2, y, z1 - 1, f"{stairs}[facing=south,half=top]")
    v.fill(x1, y, z2 + 1, x2, y, z2 + 1, f"{stairs}[facing=north,half=top]")
    v.fill(x1 - 1, y, z1, x1 - 1, y, z2, f"{stairs}[facing=east,half=top]")
    v.fill(x2 + 1, y, z1, x2 + 1, y, z2, f"{stairs}[facing=west,half=top]")
    for cx, cz in ((x1 - 1, z1 - 1), (x2 + 1, z1 - 1), (x1 - 1, z2 + 1), (x2 + 1, z2 + 1)):
        v.set(cx, y, cz, f"{slab}[type=top]")


def _lamp_post(v: Voxel, x: int, z: int, y: int = 1) -> None:
    v.column(x, y, z, 3, "oak_fence")
    v.set(x, y + 3, z, "lantern")


def _satomobile(v: Voxel, x: int, z: int, body: str, slab: str, east: bool = False) -> None:
    """A 6 x 3 Satomobile: four wheels, long hood, glass cabin, slab roof.  Front at x (x+5 when ``east``)."""
    def fx(i: int) -> int:
        return x + (5 - i if east else i)
    for i in (1, 4):
        v.set(fx(i), 1, z, "black_concrete"); v.set(fx(i), 1, z + 2, "black_concrete")
    v.fill(x, 2, z, x + 5, 2, z + 2, body)
    v.set(fx(0), 2, z, "sea_lantern"); v.set(fx(0), 2, z + 2, "sea_lantern")                   # headlights
    v.fill(fx(0), 3, z, fx(1), 3, z + 2, f"{slab}[type=bottom]")                                # hood
    v.fill(fx(5), 3, z, fx(5), 3, z + 2, f"{slab}[type=bottom]")                                # trunk
    v.fill(fx(2), 3, z, fx(4), 3, z + 2, "glass"); v.set(fx(3), 3, z + 1, body)                 # cabin
    v.fill(fx(2), 4, z, fx(4), 4, z + 2, f"{slab}[type=bottom]")                                # roof


def _skyscraper(v: Voxel, x: int, z: int, w: int, d: int, h: int, wall: str, seed: int = 0) -> None:
    """Art-deco tower: three setback tiers with stair cornices and slab parapets, vertical window
    strips lit every third floor, floor slabs every 4 blocks around a ladder shaft, a street-level
    lobby with double doors, and a spire or a rooftop water tower.  Needs w, d >= 12."""
    stairs, slab = _TRIM.get(wall, ("smooth_quartz_stairs", "smooth_quartz_slab"))
    glow = "sea_lantern" if seed % 2 else "glowstone"
    tiers = (h // 2, h // 4, h - h // 2 - h // 4)
    lx, lz = x + 5, z + 6                                                                       # ladder shaft
    v.walls(x - 1, 0, z - 1, x + w, 0, z + d, "polished_andesite")                              # sidewalk
    v.fill(x + 1, 0, z + 1, x + w - 2, 0, z + d - 2, "polished_diorite")                         # lobby floor
    y0, level = 1, 0
    x1 = x2 = z1 = z2 = top = 0
    for k, th in enumerate(tiers):
        x1, z1 = x + 2 * k, z + 2 * k
        x2, z2 = x + w - 1 - 2 * k, z + d - 1 - 2 * k
        top = y0 + th - 1
        v.walls(x1, y0, z1, x2, top, z2, wall)
        v.fill(x1 + 1, y0, z1 + 1, x2 - 1, top, z2 - 1, "air")
        yf = y0
        while yf + 2 <= top:                                                                    # one storey
            if yf > y0:
                v.fill(x1 + 1, yf, z1 + 1, x2 - 1, yf, z2 - 1, f"{slab}[type=bottom]")
            lit = level == 0 or (level + seed) % 3 == 0
            pane = "glass_pane" if lit else "light_gray_stained_glass_pane"
            for yy in (yf + 1, yf + 2):
                for px in range(x1 + 1, x2, 2):
                    v.set(px, yy, z1, pane); v.set(px, yy, z2, pane)
                    if lit and level:
                        v.set(px, yy, z1 + 1, glow); v.set(px, yy, z2 - 1, glow)
                for pz in range(z1 + 1, z2, 2):
                    v.set(x1, yy, pz, pane); v.set(x2, yy, pz, pane)
                    if lit and level:
                        v.set(x1 + 1, yy, pz, glow); v.set(x2 - 1, yy, pz, glow)
            level += 1
            yf += 4
        v.fill(x1, top + 1, z1, x2, top + 1, z2, wall)                                           # tier roof plate
        _cornice(v, x1, top + 1, z1, x2, z2, stairs, slab)
        if k < 2:
            v.walls(x1, top + 2, z1, x2, top + 2, z2, f"{slab}[type=bottom]")                   # setback parapet
        if k < 2:
            v.fill(lx - 1, y0, lz, lx - 1, top, lz, wall)                                        # shaft back wall
        v.fill(lx, y0, lz, lx, top + 1, lz, "ladder[facing=east]")                                # through the plate
        y0 = top + 2
    # lobby: double doors on the avenue side, canopy, lanterns, reception desk
    cx = x + w // 2
    for dx, hinge in ((-1, "left"), (0, "right")):
        v.set(cx + dx, 1, z + d - 1, f"dark_oak_door[facing=south,half=lower,hinge={hinge}]")
        v.set(cx + dx, 2, z + d - 1, f"dark_oak_door[facing=south,half=upper,hinge={hinge}]")
    v.fill(cx - 2, 4, z + d, cx + 1, 4, z + d, f"{slab}[type=top]")
    v.set(cx - 2, 3, z + d, "lantern[hanging=true]"); v.set(cx + 1, 3, z + d, "lantern[hanging=true]")
    v.fill(cx - 1, 1, z + 2, cx + 1, 1, z + 2, "dark_oak_planks"); v.fill(cx - 1, 2, z + 2, cx + 1, 2, z + 2, "dark_oak_slab[type=bottom]")
    v.set(x + 2, 4, z + 3, "lantern[hanging=true]"); v.set(x + w - 3, 4, z + d - 4, "lantern[hanging=true]")
    # crown: parapet ring plus a spire, or a water tower on the odd towers
    v.walls(x1, top + 2, z1, x2, top + 2, z2, f"{slab}[type=bottom]")
    tx, tz = (x1 + x2) // 2, (z1 + z2) // 2
    if seed % 2 == 0:
        v.column(tx, top + 2, tz, 3, "iron_bars")
        v.column(tx, top + 5, tz, 6, "end_rod")
        v.set(tx, top + 11, tz, "redstone_lamp[lit=true]")
    else:
        for ax in (tx - 1, tx + 1):
            for az in (tz - 1, tz + 1):
                v.column(ax, top + 2, az, 2, "oak_fence")
        v.fill(tx - 1, top + 4, tz - 1, tx + 1, top + 6, tz + 1, "spruce_planks")
        v.fill(tx - 1, top + 7, tz - 1, tx + 1, top + 7, tz + 1, "spruce_slab[type=bottom]")
        v.column(tx, top + 8, tz, 3, "end_rod")
        v.set(tx, top + 11, tz, "redstone_lamp[lit=true]")


def republic_city(v: Voxel) -> None:
    """Downtown Republic City: art-deco skyscrapers, City Hall, the elevated rail, Yue Bay with Aang's statue and the spirit portal of the finale."""
    S.pad(v, -90, -70, 90, 90, "gray_concrete")
    # ---- streets: a north street with the tram line, the City Hall avenue, the bay promenade
    v.fill(-90, 0, -47, 90, 0, -45, "polished_andesite"); v.fill(-90, 0, -29, 90, 0, -27, "polished_andesite")
    v.fill(-90, 0, 23, 90, 0, 23, "polished_andesite"); v.fill(-90, 0, 35, 90, 0, 39, "polished_andesite")
    for x in range(-88, 89, 4):                                                                 # avenue centre line
        v.set(x, 0, 26, "white_concrete")
    for x in (-56, -20, 16, 52):                                                                 # crosswalks
        for sx in (x, x + 2, x + 4):
            v.fill(sx, 0, 24, sx, 0, 28, "white_concrete"); v.fill(sx, 0, -44, sx, 0, -30, "white_concrete")
    for x in range(-84, 85, 12):
        if abs(x) > 10:
            _lamp_post(v, x, 23)
        _lamp_post(v, x + 6 if x + 6 <= 88 else x, 37)
    for x in range(-80, 81, 16):
        _lamp_post(v, x, -46); _lamp_post(v, x, -28)
    # tram line: rails, catenary masts and wire, one streetcar
    v.fill(-88, 1, -37, 88, 1, -37, "rail[shape=east_west]")
    v.fill(-88, 6, -37, 88, 6, -37, "chain[axis=x]")
    for x in range(-80, 81, 16):
        v.column(x, 1, -39, 6, "iron_bars"); v.set(x, 6, -38, "iron_bars")
    tx, tz = -14, -38
    for i in (1, 10):
        v.set(tx + i, 1, tz, "black_concrete"); v.set(tx + i, 1, tz + 2, "black_concrete")
    v.fill(tx, 2, tz, tx + 11, 3, tz + 2, "red_terracotta"); v.fill(tx + 1, 2, tz + 1, tx + 10, 3, tz + 1, "air")
    v.fill(tx + 1, 3, tz, tx + 10, 3, tz, "glass"); v.fill(tx + 1, 3, tz + 2, tx + 10, 3, tz + 2, "glass")
    v.set(tx, 3, tz + 1, "glass"); v.set(tx + 11, 3, tz + 1, "glass")
    v.fill(tx, 4, tz, tx + 11, 4, tz + 2, "smooth_stone_slab[type=bottom]"); v.set(tx + 5, 5, tz + 1, "iron_bars")
    # ---- ten art-deco towers in two rows
    rng = random.Random(400)
    for i in range(10):
        x = -86 + (i % 5) * 36; z = -66 + (i // 5) * 40
        _skyscraper(v, x, z, rng.randint(12, 16), rng.randint(12, 16), rng.randint(36, 68),
                    rng.choice(("light_gray_concrete", "white_concrete", "smooth_quartz", "light_gray_terracotta")), seed=i)
    # ---- City Hall: podium and steps, portico with pediment, hall, drum colonnade and copper dome
    v.fill(-22, 1, -8, 22, 2, 22, "smooth_quartz")
    v.fill(-19, 2, -5, 19, 2, 17, "polished_diorite"); v.disc(0, 2, 6, 3, "polished_andesite"); v.set(0, 2, 6, "gold_block")
    v.fill(-8, 1, 23, 8, 1, 23, "smooth_quartz"); v.fill(-8, 2, 23, 8, 2, 23, "smooth_quartz_stairs[facing=north,half=bottom]")
    v.fill(-8, 1, 24, 8, 1, 24, "smooth_quartz_stairs[facing=north,half=bottom]")
    v.walls(-20, 3, -6, 20, 14, 18, "smooth_quartz"); v.fill(-19, 3, -5, 19, 14, 17, "air")
    for y in (5, 6, 7, 8, 9, 12, 13):
        v.windows(-20, y, -6, 20, 18, "glass_pane", period=4, offset=2)
    for x in (-12, 12):
        for z in (0, 6, 12):
            v.column(x, 3, z, 12, "quartz_pillar")
    for x in (-6, 6):
        for z in (0, 6, 12):
            v.set(x, 14, z, "lantern[hanging=true]")
    for dx, hinge in ((-1, "left"), (0, "right")):                                              # entrance
        v.set(dx, 3, 18, f"dark_oak_door[facing=south,half=lower,hinge={hinge}]")
        v.set(dx, 4, 18, f"dark_oak_door[facing=south,half=upper,hinge={hinge}]")
    v.fill(-2, 3, 18, -2, 4, 18, "glass_pane"); v.fill(1, 3, 18, 1, 4, 18, "glass_pane"); v.fill(-2, 5, 18, 1, 6, 18, "glass_pane")
    for x in range(-16, 17, 4):                                                                 # portico
        v.column(x, 3, 21, 11, "quartz_pillar")
    v.fill(-18, 14, 19, 18, 14, 22, "smooth_quartz")
    for x in (-14, -6, 6, 14):
        v.set(x, 13, 21, "lantern[hanging=true]")
    v.fill(-21, 15, -7, 21, 15, 22, "smooth_quartz")                                            # roof, cornice, parapet
    _cornice(v, -21, 15, -7, 21, 22, "smooth_quartz_stairs", "smooth_quartz_slab")
    v.walls(-21, 16, -7, 21, 16, 22, "smooth_quartz_slab[type=bottom]")
    for k, half in enumerate((18, 14, 10, 6, 2)):                                               # pediment
        v.fill(-half, 16 + k, 20, half, 16 + k, 21, "smooth_quartz")
    v.set(0, 21, 20, "gold_block")
    for x in (-18, 18):                                                                         # flags
        v.column(x, 16, 19, 7, "polished_deepslate")
        v.set(x, 22, 20, "lime_wall_banner[facing=south]")
    v.cylinder(0, 16, 6, 11, 5, "smooth_quartz", hollow=True); v.cylinder(0, 18, 6, 11, 1, "yellow_stained_glass", hollow=True)
    for a in range(0, 360, 20):
        v.column(round(12.5 * math.cos(math.radians(a))), 16, round(6 + 12.5 * math.sin(math.radians(a))), 5, "quartz_pillar")
    v.disc(0, 21, 6, 13, "smooth_quartz")
    v.dome(0, 21, 6, 12, "oxidized_copper")
    v.column(0, 33, 6, 2, "gold_block"); v.set(0, 35, 6, "end_rod")
    # ---- elevated rail: stone-and-steel piers, deck with railings, track, station, a two-car train
    v.fill(-90, 12, 30, 90, 12, 34, "iron_block")
    v.fill(-90, 13, 30, 90, 13, 30, "iron_bars"); v.fill(-90, 13, 34, 90, 13, 34, "iron_bars")
    v.fill(-90, 13, 32, 90, 13, 32, "rail[shape=east_west]")
    for x in range(-84, 85, 12):
        v.fill(x - 1, 1, 30, x + 1, 2, 34, "stone_bricks")
        v.column(x, 3, 30, 9, "stone_brick_wall"); v.column(x, 3, 34, 9, "stone_brick_wall")
        v.fill(x, 3, 31, x, 11, 33, "iron_bars")
    v.fill(24, 13, 27, 44, 13, 30, "polished_andesite")                                           # station platform
    v.fill(24, 14, 27, 44, 14, 27, "iron_bars")
    for x in (25, 34, 43):
        v.column(x, 14, 27, 3, "iron_bars"); v.column(x, 14, 30, 3, "iron_bars")
    v.fill(23, 17, 26, 45, 17, 31, "cut_copper_slab[type=bottom]")
    for x in (28, 40):
        v.set(x, 16, 28, "lantern[hanging=true]")
    for x in (27, 28, 36, 37):
        v.set(x, 14, 28, "spruce_stairs[facing=north,half=bottom]")
    for i in range(11):                                                                         # stairs down to the avenue
        x, y = 45 + i, 12 - i
        v.set(x, y, 29, "stone_brick_stairs[facing=west,half=bottom]")
        if y > 2:
            v.fill(x, 1, 29, x, y - 1, 29, "stone_bricks")
        v.set(x, y + 1, 28, "stone_brick_wall"); v.set(x, y + 1, 30, "stone_brick_wall")
    for car in (48, 61):
        v.fill(car, 14, 31, car + 11, 14, 33, "polished_deepslate"); v.fill(car, 16, 31, car + 11, 16, 33, "dark_prismarine")
        v.fill(car, 15, 31, car + 11, 15, 33, "dark_prismarine")
        v.fill(car + 1, 15, 31, car + 10, 15, 31, "glass"); v.fill(car + 1, 15, 33, car + 10, 15, 33, "glass")
        v.fill(car + 1, 14, 32, car + 10, 16, 32, "air")
        v.set(car, 15, 32, "glass"); v.set(car + 11, 15, 32, "glass")
        v.fill(car, 17, 31, car + 11, 17, 33, "dark_prismarine_slab[type=bottom]")
        for i in (1, 2, 9, 10):
            v.set(car + i, 13, 31, "black_concrete"); v.set(car + i, 13, 33, "black_concrete")
    v.set(60, 14, 32, "iron_bars"); v.set(72, 14, 32, "redstone_lamp[lit=true]"); v.set(48, 14, 32, "redstone_lamp[lit=true]")
    # ---- Satomobiles on the avenue and the north street
    for x, z, body, slab, east in ((-72, 25, "red_nether_bricks", "red_nether_brick_slab", False),
                                   (-40, 27, "polished_blackstone", "polished_blackstone_slab", True),
                                   (-30, 25, "prismarine_bricks", "prismarine_brick_slab", False),
                                   (32, 27, "smooth_sandstone", "smooth_sandstone_slab", True),
                                   (64, 25, "dark_prismarine", "dark_prismarine_slab", False),
                                   (10, -32, "crimson_planks", "crimson_slab", True)):
        _satomobile(v, x, z, body, slab, east)
    # ---- Yue Bay: quay wall, railing with lantern posts, pier, ferry, water
    v.fill(-90, -1, 41, 90, 0, 90, "water")
    v.fill(-90, -1, 40, 90, 0, 40, "stone_bricks"); v.fill(-90, 1, 40, 90, 1, 40, "stone_brick_wall")
    for x in range(-84, 85, 12):
        v.fill(x, 1, 40, x, 2, 40, "stone_bricks"); v.set(x, 3, 40, "lantern")
    for x in range(-78, 79, 12):
        v.fill(x, 1, 38, x + 1, 1, 38, "spruce_stairs[facing=north,half=bottom]")                 # benches
    v.fill(8, 0, 41, 11, 0, 62, "oak_planks"); v.fill(9, 1, 40, 10, 1, 40, "air")
    for z in (46, 54, 62):
        v.column(8, 1, z, 2, "oak_fence"); v.column(11, 1, z, 2, "oak_fence")
        v.set(8, 3, z, "lantern"); v.set(11, 3, z, "lantern")
    v.fill(14, 0, 46, 25, 0, 50, "spruce_planks"); v.walls(14, 1, 46, 25, 1, 50, "spruce_planks")   # the island ferry
    v.fill(12, 0, 48, 13, 0, 48, "oak_planks"); v.set(14, 1, 48, "air")                           # gangway
    v.fill(17, 2, 47, 22, 3, 49, "white_concrete"); v.fill(18, 3, 47, 21, 3, 47, "glass"); v.fill(18, 3, 49, 21, 3, 49, "glass")
    v.fill(17, 4, 47, 22, 4, 49, "smooth_stone_slab[type=bottom]"); v.column(23, 2, 48, 4, "polished_blackstone")
    # ---- Avatar Aang Memorial Island: stepped plinth, the statue with robe and staff
    v.disc(40, 0, 70, 14, "stone"); v.disc(40, 0, 70, 14, "stone_bricks", hollow=True)
    v.fill(34, 1, 64, 46, 2, 76, "stone_bricks"); v.fill(36, 3, 66, 44, 6, 74, "stone_bricks", hollow=True)
    v.fill(38, 1, 63, 42, 1, 63, "stone_brick_stairs[facing=south,half=bottom]"); v.fill(38, 2, 64, 42, 2, 64, "stone_brick_stairs[facing=south,half=bottom]")
    for ax, az in ((34, 64), (46, 64), (34, 76), (46, 76)):
        v.set(ax, 3, az, "lantern")
    v.tree(30, 1, 64, "cherry_log", "cherry_leaves[persistent=true]", height=4, canopy=2)
    v.tree(50, 1, 76, "cherry_log", "cherry_leaves[persistent=true]", height=4, canopy=2)
    v.fill(36, 7, 67, 44, 9, 73, "orange_terracotta"); v.walls(36, 7, 67, 44, 7, 73, "yellow_terracotta")    # robe
    v.fill(37, 10, 68, 43, 13, 72, "orange_terracotta")
    v.fill(38, 14, 69, 42, 19, 71, "orange_terracotta"); v.walls(38, 14, 69, 42, 14, 71, "yellow_terracotta")  # torso, belt
    v.line((42, 14, 69), (38, 19, 69), "yellow_terracotta")                                      # sash
    v.fill(36, 20, 69, 44, 20, 71, "yellow_terracotta")                                          # shawl
    v.fill(39, 21, 70, 41, 21, 70, "smooth_sandstone"); v.fill(39, 22, 69, 41, 25, 71, "smooth_sandstone")   # neck, head
    v.fill(40, 25, 69, 40, 25, 71, "light_blue_concrete"); v.set(40, 24, 69, "light_blue_concrete")          # the arrow
    v.column(36, 15, 70, 5, "orange_terracotta"); v.set(36, 14, 70, "smooth_sandstone")          # left arm
    v.column(44, 21, 70, 4, "orange_terracotta"); v.set(44, 25, 70, "smooth_sandstone")          # right arm, raised, gripping the staff
    v.column(45, 3, 70, 27, "oak_fence")                                                         # the staff
    # ---- the spirit portal from the finale, in its crater, with the spirit wilds growing around it
    v.disc(-50, 0, 10, 11, "moss_block"); v.disc(-50, 1, 10, 11, "mossy_cobblestone", hollow=True)
    for gx, gz in ((-50, -1), (-50, 21), (-61, 10), (-39, 10)):
        v.fill(gx - 1, 1, gz - 1, gx + 1, 1, gz + 1, "air")
    v.disc(-50, 0, 10, 5, "yellow_terracotta", hollow=True)
    v.fill(-51, 0, 9, -49, 0, 11, "iron_block"); v.set(-50, 1, 10, "beacon")
    v.column(-50, 2, 10, 60, "end_rod")
    v.cylinder(-50, 1, 10, 3, 3, "yellow_stained_glass", hollow=True)
    for y in (12, 22, 32, 42, 52):
        v.disc(-50, y, 10, 2, "yellow_stained_glass", hollow=True)
    for dx, dz in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
        v.set(-50 + dx, 62, 10 + dz, "yellow_stained_glass")
    v.set(-50, 63, 10, "glowstone")
    rng = random.Random(401)
    for (x, z, hh) in ((-64, -2, 9), (-36, -2, 7), (-66, 18, 11), (-34, 18, 8), (-50, -5, 7)):   # spirit vines
        v.column(x, 1, z, hh, "warped_stem"); v.set(x, 1 + hh // 2, z, "shroomlight")
        v.sphere(x, hh + 1, z, 2, "flowering_azalea_leaves[persistent=true]", hollow=False)
        for yy in range(hh - 3, hh + 1):
            v.set(x, yy, z + 1, "vine[north=true]")
        for yy in (hh + 1, hh, hh - 1):
            v.set(x + 3, yy, z, "vine[west=true]"); v.set(x - 3, yy, z, "vine[east=true]")
        for k in range(6):
            bx, bz = x + rng.randint(-4, 4), z + rng.randint(-4, 4)
            if (bx, bz) != (x, z):
                v.set(bx, 0, bz, "moss_block")
                v.set(bx, 1, bz, rng.choice(("azalea", "flowering_azalea", "fern", "moss_carpet")))
    for _ in range(24):
        a, r = rng.uniform(0, 360), rng.uniform(6, 10)
        bx, bz = round(-50 + r * math.cos(math.radians(a))), round(10 + r * math.sin(math.radians(a)))
        v.set(bx, 1, bz, rng.choice(("moss_carpet", "fern", "azalea", "moss_carpet")))


def pro_bending_arena(v: Voxel) -> None:
    """The Pro-bending Arena on the bay: golden dome, the elevated ring over water, tiered stands."""
    S.pad(v, -60, -60, 60, 60, "water")
    v.fill(-60, -3, -60, 60, -1, 60, "water")
    v.disc(0, 0, 0, 50, "smooth_quartz")
    v.cylinder(0, 1, 0, 48, 16, "smooth_quartz", hollow=True)
    v.cylinder(0, 1, 0, 47, 16, "light_gray_concrete", hollow=True)
    for y in (4, 5, 10, 11):
        for a in range(0, 360, 6):
            v.set(round(48 * math.cos(math.radians(a))), y, round(48 * math.sin(math.radians(a))), "yellow_stained_glass_pane")
    v.disc(0, 17, 0, 48, "gold_block"); v.disc(0, 17, 0, 44, "air")
    v.dome(0, 17, 0, 46, "gold_block")
    v.set(0, 64, 0, "redstone_lamp[lit=true]")
    for i in range(10):                                                                           # tiered stands
        v.cylinder(0, 1 + i, 0, 44 - i * 2, 1, "light_gray_concrete", hollow=True)
        v.cylinder(0, 1 + i, 0, 43 - i * 2, 1, "red_concrete" if i % 2 else "blue_concrete", hollow=True)
    v.disc(0, 1, 0, 24, "water"); v.disc(0, 0, 0, 24, "polished_andesite")
    v.fill(-18, 6, -9, 18, 6, 9, "polished_andesite")                                                # the ring
    for x in (-18, -12, -6, 0, 6, 12):
        v.fill(x, 6, -9, x, 6, 9, "red_concrete" if x < 0 else "blue_concrete")
    v.fill(-18, 7, -9, 18, 7, -9, "iron_bars"); v.fill(-18, 7, 9, 18, 7, 9, "iron_bars")
    for x in (-18, 18):
        v.fill(x, 1, -1, x, 5, 1, "iron_block"); v.fill(x, 7, -1, x, 7, 1, "iron_bars")
    v.fill(-40, 1, 46, -34, 1, 60, "oak_planks")                                                     # the ferry pier


def air_temple_island(v: Voxel) -> None:
    """Tenzin's island in Yue Bay: the temple, the spinning gates, the bison stables and the sky bison."""
    S.pad(v, -60, -60, 60, 60, "water")
    v.fill(-60, -3, -60, 60, -1, 60, "water")
    for k in range(8):
        v.disc(0, 1 + k - 8, 0, 46 - k * 2, "stone", rz=40 - k * 2)
    v.disc(0, 0, 0, 38, "grass_block", rz=32)
    from .atla import _air_spire
    _air_spire(v, 0, 1, -12, 9, 4)
    _air_spire(v, -20, 1, 4, 5, 3); _air_spire(v, 20, 1, 4, 5, 3)
    for a in range(0, 360, 45):                                                                      # the spinning gates
        x = round(14 * math.cos(math.radians(a))); z = round(14 * math.sin(math.radians(a))) + 18
        v.column(x, 1, z, 6, "stripped_oak_log")
        for k in range(6):
            v.set(x + round(2 * math.cos(math.radians(a + k * 60))), 1 + k, z + round(2 * math.sin(math.radians(a + k * 60))), "orange_wool")
    v.disc(0, 0, 18, 16, "stone", hollow=True)
    v.fill(-30, 1, -34, -14, 7, -22, "stone_bricks"); v.fill(-29, 1, -33, -15, 6, -23, "air")        # bison stables
    v.fill(-22, 1, -22, -18, 5, -22, "air"); v.fill(-30, 8, -34, -14, 8, -22, "hay_block")
    v.fill(-26, 1, -31, -19, 3, -26, "white_wool"); v.fill(-27, 2, -30, -27, 3, -27, "white_wool")
    v.fill(-26, 4, -31, -19, 4, -31, "brown_wool"); v.fill(-26, 4, -26, -19, 4, -26, "brown_wool")   # Oogi
    v.fill(-2, 0, 34, 2, 0, 50, "oak_planks")
    for i in range(10):
        v.tree(-36 + i * 8, 1, -36 + (i % 2) * 70, "cherry_log", "cherry_leaves[persistent=true]", height=4, canopy=2)


def zaofu(v: Voxel) -> None:
    """The metal city of the Beifongs: petal domes of platinum that close at night, around the central estate."""
    S.pad(v, -90, -90, 90, 90, "grass_block")
    v.disc(0, 0, 0, 60, "polished_deepslate")
    for a in range(0, 360, 60):
        cx = round(50 * math.cos(math.radians(a))); cz = round(50 * math.sin(math.radians(a)))
        v.disc(cx, 0, cz, 24, "polished_deepslate")
        for p in range(6):                                                                          # six petals, open
            ang = p * 60 + a
            for k in range(26):
                r = 20 + k * 0.4
                y = 1 + int(k * 1.1)
                x = round(cx + r * math.cos(math.radians(ang))); z = round(cz + r * math.sin(math.radians(ang)))
                v.fill(x - 2, y, z - 2, x + 2, y, z + 2, "iron_block")
        S.city_block(v, cx - 14, cz - 14, METAL, cols=2, rows=2, lot=10, street=4, floors=(2, 3), roof="flat", seed=a)
    # Suyin's estate and the metalbending dance hall in the centre
    v.fill(-18, 1, -18, 18, 10, 18, "iron_block"); v.fill(-17, 1, -17, 17, 9, 17, "air")
    v.fill(-17, 1, -17, 17, 1, 17, "polished_deepslate")
    for y in (3, 4, 7, 8):
        v.windows(-18, y, -18, 18, 18, "glass_pane", period=3, offset=2)
    v.dome(0, 10, 0, 18, "iron_block"); v.dome(0, 10, 0, 17, "air")
    v.set(0, 29, 0, "lime_concrete")
    v.fill(-2, 1, 18, 2, 5, 18, "air")
    v.disc(0, 1, 0, 6, "polished_deepslate"); v.disc(0, 2, 0, 6, "iron_block", hollow=True)       # the dance / meteorite stage
    v.set(0, 2, 0, "ancient_debris")
    v.column(-30, 1, -30, 30, "iron_block")                                                         # the Metal Clan's mast
    v.fill(-32, 31, -32, -28, 31, -28, "lime_terracotta")


def spirit_wilds(v: Voxel) -> None:
    """The Spirit World after Harmonic Convergence: the Tree of Time, glowing wilds, floating islets and a spirit portal."""
    S.pad(v, -70, -70, 70, 70, "moss_block")
    rng = random.Random(410)
    for _ in range(80):
        x, z = rng.randint(-68, 68), rng.randint(-68, 68)
        if abs(x) < 20 and abs(z) < 20:
            continue
        kind = rng.random()
        if kind < 0.4:
            v.column(x, 1, z, rng.randint(4, 12), "warped_stem"); v.sphere(x, 1 + rng.randint(4, 12), z, 3, "warped_wart_block", hollow=False)
        elif kind < 0.7:
            v.set(x, 1, z, "shroomlight"); v.set(x, 2, z, "red_mushroom_block" if rng.random() < .5 else "crimson_fungus")
        else:
            v.sphere(x, rng.randint(14, 30), z, rng.randint(3, 6), "moss_block", hollow=False)
            v.set(x, rng.randint(31, 36), z, "glowstone")
    # Tree of Time: huge hollow trunk
    v.cylinder(0, 1, 0, 14, 40, "dark_oak_log", hollow=True)
    v.cylinder(0, 1, 0, 13, 40, "dark_oak_log", hollow=True)
    v.fill(-2, 1, 13, 2, 6, 14, "air")
    v.fill(-12, 1, -12, 12, 1, 12, "moss_block")
    v.set(0, 4, 0, "end_rod")
    for a in range(0, 360, 36):
        v.line((round(13 * math.cos(math.radians(a))), 40, round(13 * math.sin(math.radians(a)))),
               (round(30 * math.cos(math.radians(a))), 52, round(30 * math.sin(math.radians(a)))), "dark_oak_log")
        v.sphere(round(30 * math.cos(math.radians(a))), 52, round(30 * math.sin(math.radians(a))), 6, "azalea_leaves[persistent=true]", hollow=True)
    for k in range(10):                                                                            # roots
        for a in range(0, 360, 60):
            v.set(round((14 + k) * math.cos(math.radians(a + k * 5))), 1, round((14 + k) * math.sin(math.radians(a + k * 5))), "dark_oak_log")
    # the Southern spirit portal
    v.fill(50, 1, -50, 50, 50, -50, "yellow_stained_glass"); v.set(50, 1, -50, "beacon"); v.fill(49, 0, -51, 51, 0, -49, "iron_block")
    v.disc(50, 0, -50, 6, "packed_ice")
    v.disc(-50, 0, 50, 10, "water"); v.disc(-50, 1, 50, 10, "lily_pad")                              # Iroh's tea garden pond
    S.house(v, -40, 36, 8, 6, {**AIR, "roof": "lime_terracotta"}, floors=1, roof="hip", wall="dark_oak_planks")


def future_industries(v: Voxel) -> None:
    """Future Industries: Asami's factory, airfield with a biplane, Satomobile test track, and Kuvira's Colossus under construction."""
    S.pad(v, -80, -60, 80, 60, "gray_concrete")
    for i in range(3):
        S.house(v, -78 + i * 30, -56, 26, 20, {**CITY, "wall": "bricks", "roof": "light_gray_concrete"}, floors=2, roof="gable", wall="bricks")
        v.cylinder(-66 + i * 30, 1, -40, 2, 30, "bricks", hollow=True)
    v.fill(-78, 0, -30, 60, 0, -24, "polished_andesite")                                             # runway
    v.fill(-20, 1, -28, -8, 1, -26, "red_concrete"); v.fill(-20, 2, -34, -8, 2, -20, "white_concrete")   # biplane
    v.fill(-20, 4, -34, -8, 4, -20, "white_concrete"); v.fill(-6, 1, -27, -4, 2, -27, "iron_block")
    v.disc(20, 0, 20, 30, "gray_concrete", hollow=True, rz=20); v.disc(20, 0, 20, 29, "black_concrete", hollow=True, rz=19)   # track
    v.fill(48, 1, 19, 53, 1, 21, "blue_concrete"); v.fill(49, 2, 19, 52, 2, 21, "glass")
    # Kuvira's Colossus: a 25-storey mech on scaffolding
    cx, cz = -50, 20
    v.fill(cx - 4, 1, cz - 2, cx - 1, 24, cz + 2, "iron_block"); v.fill(cx + 1, 1, cz - 2, cx + 4, 24, cz + 2, "iron_block")
    v.fill(cx - 7, 25, cz - 4, cx + 7, 44, cz + 4, "iron_block")
    v.fill(cx - 11, 40, cz - 2, cx - 8, 44, cz + 2, "iron_block"); v.fill(cx - 11, 26, cz - 2, cx - 8, 39, cz + 2, "iron_block")
    v.fill(cx + 8, 40, cz - 2, cx + 11, 44, cz + 2, "iron_block"); v.fill(cx + 8, 26, cz - 2, cx + 11, 39, cz + 2, "iron_block")
    v.fill(cx - 3, 45, cz - 3, cx + 3, 50, cz + 3, "iron_block"); v.fill(cx - 2, 47, cz - 4, cx + 2, 48, cz - 4, "purple_stained_glass")
    v.fill(cx - 1, 34, cz - 5, cx + 1, 36, cz - 5, "purple_concrete")                                   # the spirit cannon mount
    for y in range(1, 50, 6):
        v.walls(cx - 13, y, cz - 6, cx + 13, y, cz + 6, "scaffolding")
    for x in (cx - 13, cx + 13):
        for z in (cz - 6, cz + 6):
            v.column(x, 1, z, 50, "scaffolding")


WORLD = World(
    id="korra",
    name="The Legend of Korra",
    game="The Legend of Korra (Nickelodeon, 2012-2014)",
    era="170-174 AG",
    description="Korra's world: Republic City, the Pro-bending Arena, Air Temple Island, Zaofu, the Spirit Wilds and Future Industries.",
    franchise="Avatar",
).build(Build("republic_city", "Republic City", "Art-deco skyscrapers, City Hall, the elevated rail, Satomobiles, Aang's memorial statue in Yue Bay and the downtown spirit portal.", republic_city)
).build(Build("pro_bending_arena", "Pro-bending Arena", "Golden dome on the bay, tiered stands, the ring over water with its zones.", pro_bending_arena)
).build(Build("air_temple_island", "Air Temple Island", "Tenzin's temple spires, the spinning airbending gates, the bison stables with Oogi.", air_temple_island)
).build(Build("zaofu", "Zaofu", "Six platinum petal domes around Suyin's estate and the meteorite stage.", zaofu)
).build(Build("spirit_wilds", "Spirit Wilds", "The Tree of Time, glowing spirit forest, floating islets, the Southern portal and Iroh's tea garden.", spirit_wilds)
).build(Build("future_industries", "Future Industries", "Asami's factory, airfield and biplane, test track, and Kuvira's Colossus on its scaffolding.", future_industries))
