"""Avatar: The Last Airbender (2005-2008) - the Four Nations in Aang's time, 99-100 AG."""

import math
import random

from .. import structures as S
from ..palettes import _p
from ..registry import Build, World
from ..voxel import Voxel

WATER = _p(ground="snow_block", wall="packed_ice", wall2="snow_block", trim="blue_ice", roof="packed_ice",
           floor="snow_block", column="blue_ice", light="sea_lantern", path="snow_block",
           leaves="spruce_leaves[persistent=true]", log="spruce_log")
EARTH = _p(ground="grass_block", wall="stone_bricks", wall2="green_terracotta", trim="smooth_stone",
           roof="green_terracotta", floor="smooth_stone", column="stone_bricks", path="cobblestone",
           leaves="oak_leaves[persistent=true]", log="oak_log")
FIRE = _p(ground="blackstone", wall="red_terracotta", wall2="polished_blackstone", trim="gold_block",
          roof="black_concrete", floor="polished_blackstone", column="red_terracotta", path="polished_blackstone_bricks",
          leaves="dark_oak_leaves[persistent=true]", log="dark_oak_log")
AIR = _p(ground="stone", wall="smooth_quartz", wall2="orange_terracotta", trim="orange_terracotta", roof="light_blue_terracotta",
         floor="smooth_quartz", column="quartz_pillar", path="stone", leaves="cherry_leaves[persistent=true]", log="cherry_log")


def _air_spire(v: Voxel, cx: int, y: int, cz: int, half: int, stories: int) -> None:
    """Air Nomad tower: tapering tiers with blue conical caps."""
    for s in range(stories):
        h = max(2, half - s)
        v.walls(cx - h, y, cz - h, cx + h, y + 5, cz + h, AIR["wall"])
        v.fill(cx - h + 1, y, cz - h + 1, cx + h - 1, y + 5, cz + h - 1, "air")
        v.fill(cx - h, y, cz - h, cx + h, y, cz + h, AIR["floor"])
        v.windows(cx - h, y + 2, cz - h, cx + h, cz + h, "light_blue_stained_glass_pane", period=2, offset=1)
        v.fill(cx - h - 1, y + 6, cz - h - 1, cx + h + 1, y + 6, cz + h + 1, AIR["roof"])
        y += 7
    v.cone(cx, y, cz, half - stories + 2, 7, AIR["roof"])
    v.set(cx, y + 7, cz, "gold_block")


def southern_water_tribe(v: Voxel) -> None:
    """Katara and Sokka's village: igloos and tents inside a snow wall, Sokka's watchtower, a Fire Nation wreck in the ice."""
    S.pad(v, -70, -60, 70, 60, "snow_block")
    v.fill(-70, -3, 30, 70, 0, 60, "water")
    for x in range(-70, 71, 9):
        v.fill(x, 0, 30, x + 4, 0, 60, "ice")
    v.cylinder(0, 1, -10, 26, 3, "snow_block", hollow=True)                   # snow wall
    v.fill(-2, 1, 16, 2, 3, 16, "air")
    for (x, z, r) in ((-12, -18, 4), (10, -20, 4), (-16, -2, 3), (14, 0, 4), (0, -24, 3), (-6, 8, 3)):
        v.sphere(x, 1, z, r, "snow_block", hollow=True, y_min=1)
        v.fill(x, 1, z + r, x, 2, z + r, "air")
    for (x, z) in ((4, 6), (-4, -8)):                                            # hide tents
        v.cone(x, 1, z, 3, 5, "brown_wool")
        v.set(x, 1, z + 3, "air")
    v.fill(-2, 1, -2, 2, 1, 2, "campfire")
    v.fill(16, 1, -14, 18, 1, -12, "snow_block"); v.set(17, 2, -13, "snow_block")   # Sokka's watchtower
    v.fill(16, 3, -14, 18, 3, -12, "spruce_slab"); v.column(17, 3, -13, 6, "spruce_fence")
    v.fill(15, 9, -15, 19, 9, -11, "snow_block"); v.walls(15, 10, -15, 19, 10, -11, "spruce_fence")
    # the Fire Navy wreck frozen into the ice at the shore
    v.fill(40, -2, 34, 66, 4, 42, "polished_blackstone")
    v.fill(41, 1, 35, 65, 4, 41, "air")
    v.fill(40, 5, 34, 66, 5, 42, "polished_blackstone")
    v.fill(50, 6, 36, 56, 12, 40, "polished_blackstone"); v.column(53, 13, 38, 6, "blackstone")
    for k in range(6):
        v.fill(66 - k, 1 + k, 34 + k, 66 - k, 1 + k, 42 - k, "polished_blackstone")   # raked prow
    v.fill(36, 0, 30, 70, 0, 46, "ice"); v.fill(36, 1, 30, 48, 3, 33, "packed_ice")
    v.fill(-20, 1, 24, -14, 1, 29, "spruce_planks")                                 # canoe
    v.sphere(-40, 1, -30, 8, "packed_ice", hollow=False, y_min=1)                    # iceberg where Aang was found
    v.sphere(-40, 1, -30, 6, "light_blue_stained_glass", hollow=True, y_min=1)
    v.set(-40, 5, -30, "orange_wool")


def northern_water_tribe(v: Voxel) -> None:
    """Agna Qel'a: the ice city behind its sea wall, canals, tiered palace and the Spirit Oasis."""
    S.pad(v, -80, -80, 80, 70, "packed_ice")
    v.fill(-80, -3, 40, 80, 0, 70, "water")
    v.fill(-80, 1, 36, 80, 12, 40, "packed_ice")                                      # the great sea wall
    v.fill(-6, 1, 36, 6, 8, 40, "water"); v.fill(-6, 9, 36, 6, 12, 40, "blue_ice")       # water gate
    for x in (-50, -25, 25, 50):
        S.tower(v, x, 38, 4, 16, WATER, top="dome", wall="packed_ice")
    for z in range(-60, 36, 20):                                                       # canals
        v.fill(-78, 0, z, 78, 0, z + 2, "water")
    for x in range(-60, 70, 24):
        v.fill(x, 0, -78, x + 2, 0, 36, "water")
    rng = random.Random(200)
    for x in range(-74, 60, 24):
        for z in range(-56, 30, 20):
            S.house(v, x + 4, z + 4, rng.randint(8, 12), rng.randint(7, 10), WATER, floors=rng.randint(1, 2), roof="dome", wall="packed_ice")
    # tiered palace at the head of the city
    for k in range(3):
        r = 30 - k * 8
        v.fill(-r, 1 + k * 8, -78, r, 8 + k * 8, -78 + 2 * r, "packed_ice")
        v.fill(-r + 1, 1 + k * 8, -77, r - 1, 7 + k * 8, -79 + 2 * r, "air")
        v.fill(-r + 1, 1 + k * 8, -77, r - 1, 1 + k * 8, -79 + 2 * r, "snow_block")
    v.fill(-2, 1, -50, 2, 5, -50, "air")
    v.cone(0, 25, -64, 8, 12, "blue_ice"); v.set(0, 37, -64, "sea_lantern")
    for k in range(24):                                                                 # great stair up to the palace
        v.fill(-3, 1 + k, -30 - k, 3, 1 + k, -30 - k, "blue_ice")
    # Spirit Oasis: warm grass and a pond with the koi behind the palace
    v.fill(-14, 20, -74, 14, 26, -56, "air")
    v.fill(-12, 19, -72, 12, 19, -58, "grass_block")
    v.disc(0, 19, -65, 5, "water")
    v.set(-1, 19, -65, "white_wool"); v.set(1, 19, -65, "black_wool")                   # Tui and La
    v.tree(-8, 20, -62, "cherry_log", "cherry_leaves[persistent=true]", height=4, canopy=2)
    v.tree(8, 20, -68, "cherry_log", "cherry_leaves[persistent=true]", height=4, canopy=2)
    v.fill(-3, 20, -57, 3, 23, -57, "air")


def southern_air_temple(v: Voxel) -> None:
    """Aang's home on its mountain: spires, the airball court, the sanctuary of Avatar statues, Momo's orchard."""
    S.pad(v, -70, -70, 70, 70, "stone")
    for k in range(30):
        v.disc(0, 1 + k, 0, 60 - k * 1.5, "stone" if k % 4 else "andesite", rz=50 - k * 1.2)
    top = 31
    t = Voxel()
    t.disc(0, 0, 0, 30, AIR["floor"], rz=24)
    _air_spire(t, 0, 1, -8, 8, 4)
    _air_spire(t, -18, 1, 6, 5, 3)
    _air_spire(t, 18, 1, 6, 5, 3)
    _air_spire(t, 0, 1, 14, 4, 2)
    # sanctuary of the Avatars: a hall with rows of statues spiralling in
    t.fill(-14, 1, -30, 14, 10, -14, AIR["wall"]); t.fill(-13, 1, -29, 13, 9, -15, "air")
    t.fill(-2, 1, -14, 2, 5, -14, "air")
    for i, (x, z) in enumerate(((-10, -26), (-6, -24), (10, -26), (6, -24), (-10, -18), (10, -18), (0, -27))):
        t.fill(x, 1, z, x, 5, z, ("orange_terracotta", "blue_terracotta", "green_terracotta", "red_terracotta")[i % 4])
        t.set(x, 6, z, "smooth_quartz")
    t.set(0, 1, -27, "orange_terracotta")
    # airball court: a field of poles
    for x in range(-12, 13, 4):
        for z in range(22, 36, 4):
            t.column(x, 1, z, 8, "oak_fence")
    t.fill(-12, 9, 22, 12, 9, 34, "oak_fence")
    v.merge(t, 0, top - 1, 0)
    for k in range(31):                                                                  # stair from the valley
        v.fill(-2, 1 + k, 60 - k * 1.3, 2, 1 + k, 61 - k * 1.3, "smooth_stone")
    for i in range(8):                                                                   # the orchard where Momo lives
        v.tree(-40 + i * 10, 20, 40 - (i % 3) * 6, "cherry_log", "cherry_leaves[persistent=true]", height=4, canopy=2)
    v.fill(-35, 19, 34, 35, 19, 46, "grass_block")


def omashu(v: Voxel) -> None:
    """The mountain city of King Bumi: tiered walls, delivery chutes, the palace on top."""
    S.pad(v, -80, -80, 80, 80, "stone")
    for k in range(5):
        r = 70 - k * 14
        v.fill(-r, 1 + k * 12, -r, r, 12 + k * 12, r, EARTH["wall"] if k % 2 else "cobblestone")
        v.fill(-r + 2, 1 + k * 12, -r + 2, r - 2, 12 + k * 12, r - 2, "stone")
        v.fill(-r + 3, 12 + k * 12, -r + 3, r - 3, 12 + k * 12, r - 3, "cobblestone")
        rng = random.Random(300 + k)
        for i in range(10):
            x = rng.randint(-r + 6, r - 14); z = rng.randint(-r + 6, r - 14)
            if abs(x) < r - 20 and abs(z) < r - 20:
                continue
            tmp = Voxel()
            S.house(tmp, 0, 0, rng.randint(6, 9), rng.randint(6, 9), EARTH, floors=rng.randint(1, 2), roof="flat")
            v.merge(tmp, x, 12 + k * 12, z)
    # delivery chutes spiralling down the terraces
    for a in range(0, 1440, 3):
        r = 68 - a / 24
        y = 60 - int(a / 24.5)
        if r < 12:
            break
        x = round(r * math.cos(math.radians(a))); z = round(r * math.sin(math.radians(a)))
        v.set(x, y, z, "smooth_stone")
        v.set(x, y + 1, z, "air")
        v.set(round((r + 1) * math.cos(math.radians(a))), y + 1, round((r + 1) * math.sin(math.radians(a))), "smooth_stone_slab")
    v.fill(-8, 56, -8, 8, 56, 8, "stone")
    v.fill(-6, 57, 6, 6, 58, 8, "oak_planks")                                              # a delivery cart
    # Bumi's palace
    tmp = Voxel()
    S.house(tmp, -12, -12, 25, 25, EARTH, floors=3, roof="hip", wall="stone_bricks")
    tmp.pyramid(0, 14, 0, 27, 10, "green_terracotta")
    tmp.set(0, 24, 0, "gold_block")
    v.merge(tmp, 0, 60, 0)
    v.fill(-80, 0, 72, 80, 0, 80, "water")
    for k in range(12):                                                                      # the gate and ramp
        v.fill(-3, 1 + k, 70 - k, 3, 1 + k, 70 - k, "stone_bricks")
    v.fill(-3, 1, 68, 3, 6, 70, "air")


def ba_sing_se(v: Voxel) -> None:
    """A slice of the Earth Kingdom capital: the Outer Wall, the three rings, the monorail and the Earth King's palace."""
    S.pad(v, -60, -160, 60, 60, "grass_block")
    v.fill(-60, 1, 40, 60, 60, 50, "stone_bricks")                                          # the Outer Wall
    v.fill(-59, 2, 41, 59, 59, 49, "stone")
    v.fill(-60, 61, 40, 60, 61, 50, "cobblestone"); v.crenellate(-60, 62, 40, 60, 50, "stone_bricks", period=3)
    v.fill(-4, 1, 40, 4, 8, 50, "air")
    for x in (-50, -25, 0, 25, 50):
        v.fill(x - 3, 61, 42, x + 3, 68, 48, "stone_bricks"); v.fill(x - 2, 62, 43, x + 2, 67, 47, "air")
    v.fill(-40, 1, 52, 40, 3, 60, "coarse_dirt")                                             # the drill's track / scar
    # Lower Ring: dense poor housing
    S.city_block(v, -58, -10, {**EARTH, "wall": "cobblestone", "wall2": "mud_bricks", "roof": "dark_oak_planks"},
                 cols=6, rows=3, lot=8, street=3, floors=(1, 2), roof="gable", seed=310)
    v.fill(-60, 1, -14, 60, 20, -12, "stone_bricks")                                          # inner wall
    v.fill(-3, 1, -14, 3, 6, -12, "air")
    # Middle Ring: shops and the Jasmine Dragon tea shop
    S.city_block(v, -58, -60, EARTH, cols=5, rows=2, lot=10, street=4, floors=(2, 3), roof="hip", seed=311)
    S.house(v, 20, -58, 24, 16, {**EARTH, "roof": "lime_terracotta"}, floors=2, roof="hip", wall="green_terracotta")
    v.fill(-60, 1, -64, 60, 20, -62, "stone_bricks"); v.fill(-3, 1, -64, 3, 6, -62, "air")
    # Upper Ring: estates, and the palace at the far end
    S.garden(v, -58, -110, -10, -70, EARTH, trees=8, seed=312)
    S.house(v, 14, -100, 30, 20, EARTH, floors=2, roof="hip", wall="smooth_sandstone")
    v.fill(-30, 1, -150, 30, 12, -118, "stone_bricks"); v.fill(-29, 1, -149, 29, 11, -119, "air")
    v.fill(-29, 1, -149, 29, 1, -119, "polished_andesite")
    v.fill(-30, 13, -150, 30, 13, -118, "green_terracotta")
    v.fill(-20, 14, -142, 20, 22, -126, "stone_bricks"); v.fill(-19, 14, -141, 19, 21, -127, "air")
    v.hip_roof(-20, 23, -142, 20, -126, "green_terracotta", overhang=2)
    v.fill(-2, 1, -118, 2, 6, -118, "air")
    for k in range(10):
        v.fill(-6, 1 + k, -110 + 0 - k, 6, 1 + k, -110 - k, "smooth_stone")
    # the monorail along the city's axis
    v.fill(-24, 0, -156, -24, 11, 38, "stone_bricks")
    v.fill(-27, 12, -156, -21, 12, 38, "stone")
    v.fill(-24, 13, -156, -24, 13, 38, "rail")
    v.fill(-25, 14, -40, -23, 16, -20, "green_terracotta"); v.fill(-24, 15, -39, -24, 15, -21, "air")
    v.windows(-25, 15, -40, -23, -20, "glass_pane", period=2, offset=1)


def kyoshi_island(v: Voxel) -> None:
    """The island village under the statue of Avatar Kyoshi, with the Kyoshi Warriors' dojo and the bay."""
    S.pad(v, -60, -50, 60, 60, "water")
    v.fill(-60, -3, -50, 60, -1, 60, "water")
    v.disc(0, 0, 0, 50, "grass_block", rz=40)
    v.disc(0, -1, 0, 52, "sand", rz=42)
    for i in range(10):
        S.house(v, -36 + (i % 5) * 15, -20 + (i // 5) * 18, 9, 7, {**EARTH, "roof": "dark_oak_planks"}, floors=1, roof="gable", wall="oak_planks")
    S.house(v, -10, 20, 20, 12, {**EARTH, "roof": "lime_terracotta"}, floors=1, roof="hip", wall="green_terracotta")   # dojo
    # Kyoshi's statue on the shore, in green and gold with fans
    sx, sz = 30, -30
    v.fill(sx - 3, 1, sz - 3, sx + 3, 3, sz + 3, "smooth_stone")
    v.fill(sx - 2, 4, sz - 2, sx + 2, 16, sz + 2, "green_terracotta")
    v.fill(sx - 3, 10, sz - 3, sx + 3, 12, sz + 3, "gold_block")
    v.fill(sx - 1, 17, sz - 1, sx + 1, 19, sz + 1, "white_concrete")
    v.fill(sx - 2, 19, sz - 2, sx + 2, 21, sz + 2, "black_concrete")
    v.fill(sx + 3, 12, sz - 1, sx + 6, 12, sz + 1, "gold_block"); v.fill(sx + 6, 10, sz - 2, sx + 7, 14, sz + 2, "yellow_terracotta")   # fan
    v.fill(-8, 0, 42, -2, 0, 56, "oak_planks")                                               # jetty
    for i in range(12):
        v.tree(-45 + i * 8, 1, -36 + (i % 3) * 4, "spruce_log", "spruce_leaves[persistent=true]", height=7, canopy=2)
    v.set(20, 0, 55, "prismarine"); v.fill(18, 0, 54, 22, 1, 56, "prismarine")               # the Unagi's back breaking the water


def fire_nation_capital(v: Voxel) -> None:
    """The caldera city: the volcanic rim, the Royal Palace with red pagoda roofs, the plaza of the Agni Kai arena."""
    S.pad(v, -90, -90, 90, 90, "blackstone")
    for k in range(18):
        v.disc(0, 1 + k, 0, 88 - k, "blackstone" if k % 3 else "basalt", hollow=True)
        v.disc(0, 1 + k, 0, 87 - k, "blackstone" if k % 3 else "basalt", hollow=True)
    v.fill(-4, 1, 70, 4, 10, 90, "air")                                                      # the gate through the rim
    v.disc(0, 1, 0, 70, "polished_blackstone_bricks")
    # Royal Palace
    v.fill(-40, 2, -60, 40, 14, -20, "red_terracotta"); v.fill(-39, 2, -59, 39, 13, -21, "air")
    v.fill(-39, 2, -59, 39, 2, -21, "polished_blackstone")
    for y in (6, 7, 11, 12):
        v.windows(-40, y, -60, 40, -20, "orange_stained_glass_pane", period=4, offset=2)
    v.fill(-41, 15, -61, 41, 15, -19, "black_concrete")
    v.walls(-42, 16, -62, 42, 16, -18, "gold_block")
    v.fill(-16, 16, -48, 16, 28, -32, "red_terracotta"); v.fill(-15, 16, -47, 15, 27, -33, "air")
    v.pagoda_roof(0, 29, -40, 18, "black_concrete", "gold_block")
    v.pagoda_roof(0, 33, -40, 12, "black_concrete", "gold_block")
    v.cone(0, 35, -40, 6, 8, "black_concrete"); v.set(0, 43, -40, "gold_block")
    v.fill(-3, 2, -20, 3, 8, -20, "air")
    v.fill(-8, 2, -44, 8, 2, -38, "lava"); v.fill(-8, 3, -45, 8, 3, -45, "gold_block")        # the Fire Lord's throne behind a wall of flame
    v.fill(-2, 3, -47, 2, 5, -47, "gold_block")
    # Agni Kai arena
    v.disc(0, 1, 30, 24, "polished_blackstone", hollow=True); v.disc(0, 2, 30, 24, "red_terracotta", hollow=True)
    v.disc(0, 1, 30, 22, "polished_blackstone")
    for a in range(0, 360, 30):
        v.column(round(24 * math.cos(math.radians(a))), 3, round(30 + 24 * math.sin(math.radians(a))), 6, "red_terracotta")
        v.set(round(24 * math.cos(math.radians(a))), 9, round(30 + 24 * math.sin(math.radians(a))), "campfire")
    S.city_block(v, -66, -10, FIRE, cols=3, rows=2, lot=9, street=4, floors=(2, 3), roof="hip", seed=320)
    S.city_block(v, 28, -10, FIRE, cols=3, rows=2, lot=9, street=4, floors=(2, 3), roof="hip", seed=321)
    for x in range(-60, 61, 30):
        S.tower(v, x, 66, 2.5, 14, FIRE, top="pyramid", square=True, wall="red_terracotta")


def wan_shi_tong_library(v: Voxel) -> None:
    """Wan Shi Tong's Spirit Library in the Si Wong desert: only the spire shows above the sand; the great domed hall, galleries and planetarium are buried below."""
    S.pad(v, -60, -60, 60, 60, "sand")
    # the visible spire
    for k in range(22):
        r = 6 - k * 0.2
        v.disc(0, 1 + k, 0, r, "sandstone", hollow=True)
    v.cone(0, 23, 0, 5, 8, "cut_sandstone")
    v.fill(0, 1, 6, 0, 4, 6, "air"); v.fill(-1, 1, -5, 1, 1, 5, "air")
    v.fill(-1, 5, -4, 1, 8, -4, "orange_stained_glass_pane")                                # the window Sokka climbed
    v.fill(-2, -40, -2, 2, 0, 2, "air")                                                    # the rope shaft down
    v.fill(0, -40, 0, 0, 0, 0, "chain")
    # the great hall: a dome 50 wide, buried
    v.sphere(0, -22, 0, 26, "sandstone", hollow=True)
    v.sphere(0, -22, 0, 25, "air", hollow=False)
    v.fill(-25, -44, -25, 25, -44, 25, "cut_sandstone")
    v.disc(0, -44, 0, 25, "cut_sandstone")
    # bridges, galleries and bookshelves on four levels
    for lvl, y in enumerate((-42, -36, -30, -24)):
        r = int(math.sqrt(max(0, 25 ** 2 - (y + 22) ** 2))) - 1
        v.disc(0, y, 0, r, "smooth_sandstone", hollow=True)
        v.disc(0, y, 0, r - 1, "smooth_sandstone", hollow=True)
        v.disc(0, y, 0, r - 2, "smooth_sandstone", hollow=True)
        for a in range(0, 360, 6):
            x = round((r - 1) * math.cos(math.radians(a))); z = round((r - 1) * math.sin(math.radians(a)))
            v.fill(x, y + 1, z, x, y + 4, z, "bookshelf")
            if a % 36 == 0:
                v.set(round((r - 3) * math.cos(math.radians(a))), y + 3, round((r - 3) * math.sin(math.radians(a))), "lantern")
        v.fill(-r + 3, y, -1, r - 3, y, 1, "smooth_sandstone")                             # bridges across
        v.fill(-1, y, -r + 3, 1, y, r - 3, "smooth_sandstone")
        for a in (45, 135, 225, 315):                                                       # ladders between levels
            x = round((r - 4) * math.cos(math.radians(a))); z = round((r - 4) * math.sin(math.radians(a)))
            v.fill(x, y + 1, z, x, y + 5, z, "ladder[facing=north]")
    v.fill(-3, -43, -3, 3, -43, 3, "smooth_sandstone")                                     # central reading dais
    v.set(0, -42, 0, "lectern")
    v.fill(-1, -41, -1, 1, -38, 1, "black_concrete"); v.fill(-2, -37, -2, 2, -36, 2, "white_concrete")   # Wan Shi Tong
    v.set(-1, -36, -3, "lantern"); v.set(1, -36, -3, "lantern")
    # the planetarium: a side room with a star-dome and the calendar dial
    v.fill(26, -36, -10, 46, -26, 10, "sandstone"); v.fill(27, -35, -9, 45, -27, 9, "air")
    v.sphere(36, -30, 0, 8, "black_concrete", hollow=True, y_min=-30)
    for (dx, dy, dz) in ((2, 5, 1), (-3, 6, -2), (4, 4, -4), (-5, 3, 4), (0, 7, 0), (6, 2, 3)):
        v.set(36 + dx, -30 + dy, dz, "sea_lantern")
    v.disc(36, -35, 0, 5, "gold_block", hollow=True); v.disc(36, -35, 0, 3, "copper_block", hollow=True)
    v.fill(25, -35, -2, 26, -30, 2, "air")
    # the fox spirit's tunnel and the Professor's catalogue room
    v.fill(-46, -36, -4, -26, -30, 4, "air"); v.fill(-26, -35, -2, -25, -31, 2, "air")
    v.fill(-46, -35, -4, -30, -31, -4, "bookshelf"); v.fill(-46, -35, 4, -30, -31, 4, "bookshelf")
    v.set(-44, -35, 0, "cartography_table")
    for i in range(1, 6, 2):                                                                   # sandbender rock spires
        v.cone(-50 + i * 20, 1, 40, 2, 6, "sandstone")


def western_air_temple(v: Voxel) -> None:
    """The temple that hangs upside down beneath the cliff edge: inverted pagodas under an overhang."""
    S.pad(v, -60, -40, 60, 60, "stone")
    v.fill(-60, -70, -40, 60, 0, 10, "stone")                                                # the cliff mass
    v.fill(-60, -70, 10, 60, 0, 60, "air")                                                   # the canyon
    v.fill(-60, -72, 10, 60, -71, 60, "water")
    v.fill(-60, 1, 10, 60, 1, 60, "air")
    for (x, half, stories) in ((-30, 8, 4), (0, 10, 5), (30, 8, 4), (-15, 5, 3), (15, 5, 3)):
        y = -1
        for s in range(stories):
            h = half - s
            v.fill(x - h - 1, y, 10, x + h + 1, y, 10 + 2 * h + 2, AIR["roof"])              # inverted eave
            v.walls(x - h, y - 6, 11, x + h, y - 1, 11 + 2 * h, AIR["wall"])
            v.fill(x - h + 1, y - 6, 12, x + h - 1, y - 1, 10 + 2 * h, "air")
            v.fill(x - h, y - 7, 11, x + h, y - 7, 11 + 2 * h, AIR["floor"])
            v.windows(x - h, y - 4, 11, x + h, 11 + 2 * h, "light_blue_stained_glass_pane", period=2, offset=1)
            y -= 8
        for k in range(8):                                                                   # the downward point
            v.disc(x, y - k, 11 + half, (half - stories + 2) * (k / 8), AIR["roof"])
    v.fill(-50, -8, 10, 50, -8, 14, "smooth_quartz")                                         # the main terrace walkway
    v.fill(-2, -8, 10, 2, -8, 40, "smooth_quartz")
    v.disc(0, -8, 40, 8, "smooth_quartz"); v.disc(0, -7, 40, 3, "water")                     # the fountain terrace
    v.fill(-1, -1, 14, 1, 0, 14, "air")


def boiling_rock(v: Voxel) -> None:
    """The Fire Nation's island prison in a boiling volcanic lake, with the gondola line to the crater rim."""
    S.pad(v, -80, -80, 80, 80, "water")
    v.fill(-80, -3, -80, 80, -1, 80, "water")
    for k in range(12):
        v.disc(0, 1 + k, 0, 78 - k * 2, "blackstone", hollow=True)
        v.disc(0, 1 + k, 0, 77 - k * 2, "blackstone", hollow=True)
    for a in range(0, 360, 15):                                                              # bubbles
        for r in (20, 35, 50):
            v.set(round(r * math.cos(math.radians(a))), -3, round(r * math.sin(math.radians(a))), "magma_block")
    v.disc(0, 0, 0, 24, "polished_blackstone")
    v.disc(0, 1, 0, 24, "polished_blackstone_bricks", hollow=True)
    v.cylinder(0, 1, 0, 24, 12, "polished_blackstone", hollow=True)
    v.cylinder(0, 1, 0, 18, 10, "red_terracotta", hollow=True)
    v.disc(0, 11, 0, 18, "black_concrete"); v.disc(0, 12, 0, 18, "iron_bars", hollow=True)
    for y in range(3, 10, 3):
        for a in range(0, 360, 12):
            v.set(round(18 * math.cos(math.radians(a))), y, round(18 * math.sin(math.radians(a))), "iron_bars")
    for i in range(4):                                                                        # the coolers
        v.fill(-3 + i * 3, 1, -8, -2 + i * 3, 3, -6, "iron_block"); v.set(-3 + i * 3, 2, -8, "iron_bars")
    v.fill(-6, 1, 4, 6, 1, 14, "polished_blackstone"); v.fill(-6, 2, 4, 6, 2, 14, "smooth_stone")    # the yard
    for x in (-24, 24):
        S.tower(v, x, 0, 2.5, 18, FIRE, top="flat", square=True, wall="polished_blackstone")
    v.fill(-24, 14, 0, 78, 14, 0, "chain")                                                    # the gondola cable
    v.fill(0, 12, 0, 0, 13, 0, "chain"); v.fill(-2, 10, -2, 2, 11, 2, "red_terracotta"); v.fill(-1, 11, -1, 1, 11, 1, "air")   # gondola
    v.fill(74, 13, -3, 80, 18, 3, "blackstone"); v.fill(75, 14, -2, 79, 17, 2, "air")


WORLD = World(
    id="atla",
    name="Avatar: The Last Airbender",
    game="Avatar: The Last Airbender (Nickelodeon, 2005-2008)",
    era="99-100 AG, the end of the Hundred Year War",
    description="Team Avatar's world: the Water Tribes, the Air Temples, Omashu, Ba Sing Se, Kyoshi Island, the Fire Nation and the Spirit Library.",
    franchise="Avatar",
).build(Build("southern_water_tribe", "Southern Water Tribe", "Igloos and tents inside the snow wall, Sokka's watchtower, the Fire Navy wreck and the iceberg.", southern_water_tribe)
).build(Build("northern_water_tribe", "Northern Water Tribe", "Agna Qel'a: sea wall and water gate, canals, ice houses, the tiered palace and the Spirit Oasis with Tui and La.", northern_water_tribe)
).build(Build("southern_air_temple", "Southern Air Temple", "Spires on the peak, the sanctuary of Avatar statues, the airball court and Momo's orchard.", southern_air_temple)
).build(Build("omashu", "Omashu", "Five-tier mountain city with spiralling delivery chutes and Bumi's palace on top.", omashu)
).build(Build("ba_sing_se", "Ba Sing Se", "The Outer Wall, Lower, Middle and Upper Rings, the Jasmine Dragon, the monorail and the Earth King's palace.", ba_sing_se)
).build(Build("kyoshi_island", "Kyoshi Island", "The village, the Kyoshi Warriors' dojo, the statue of Avatar Kyoshi and the Unagi's bay.", kyoshi_island)
).build(Build("fire_nation_capital", "Fire Nation Capital", "The caldera city: volcanic rim, Royal Palace with the throne behind flames, and the Agni Kai arena.", fire_nation_capital)
).build(Build("wan_shi_tong_library", "Wan Shi Tong's Library", "Only the spire shows above the desert; below, the great dome with four gallery levels, the owl spirit, the planetarium and the catalogue room.", wan_shi_tong_library)
).build(Build("western_air_temple", "Western Air Temple", "Inverted pagodas hanging under the cliff edge above a canyon.", western_air_temple)
).build(Build("boiling_rock", "The Boiling Rock", "Island prison in a boiling lake with coolers, yard, towers and the gondola to the rim.", boiling_rock))
