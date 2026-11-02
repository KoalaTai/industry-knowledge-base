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


def _skyscraper(v: Voxel, x: int, z: int, w: int, d: int, h: int, wall: str, seed: int = 0) -> None:
    """Art-deco tower: setbacks every third of the height, lit windows, a spire."""
    y = 1
    for tier in range(3):
        th = h // 3
        v.fill(x, y, z, x + w - 1, y + th - 1, z + d - 1, wall)
        v.fill(x + 1, y, z + 1, x + w - 2, y + th - 1, z + d - 2, "air")
        for yy in range(y + 1, y + th - 1, 3):
            v.windows(x, yy, z, x + w - 1, z + d - 1, "yellow_stained_glass_pane" if (yy + seed) % 2 else "glass_pane", period=2, offset=1)
            v.windows(x, yy + 1, z, x + w - 1, z + d - 1, "yellow_stained_glass_pane" if (yy + seed) % 2 else "glass_pane", period=2, offset=1)
        v.fill(x, y + th, z, x + w - 1, y + th, z + d - 1, CITY["trim"])
        y += th + 1
        x += 1; z += 1; w -= 2; d -= 2
        if w < 3 or d < 3:
            break
    v.column(x + max(0, w // 2), y, z + max(0, d // 2), 8, "iron_bars")
    v.set(x + max(0, w // 2), y + 8, z + max(0, d // 2), "redstone_lamp[lit=true]")


def republic_city(v: Voxel) -> None:
    """Downtown Republic City: art-deco skyscrapers, City Hall, the elevated rail, Yue Bay with Aang's statue and the spirit portal of the finale."""
    S.pad(v, -90, -70, 90, 90, "gray_concrete")
    v.fill(-90, -3, 40, 90, 0, 90, "water")
    v.fill(-90, 0, 38, 90, 0, 39, "smooth_stone")
    rng = random.Random(400)
    for i in range(10):
        x = -86 + (i % 5) * 36; z = -66 + (i // 5) * 40
        _skyscraper(v, x, z, rng.randint(12, 18), rng.randint(12, 18), rng.randint(36, 72),
                    rng.choice(("light_gray_concrete", "white_concrete", "smooth_quartz", "light_gray_terracotta")), seed=i)
    # City Hall with its dome, on the central avenue
    v.fill(-20, 1, -4, 20, 14, 24, "smooth_quartz"); v.fill(-19, 1, -3, 19, 13, 23, "air")
    for x in range(-18, 19, 4):
        v.column(x, 1, 24, 13, "quartz_pillar")
    v.fill(-21, 15, -5, 21, 15, 25, "light_gray_concrete")
    v.dome(0, 15, 10, 12, "lime_terracotta"); v.set(0, 28, 10, "gold_block")
    v.fill(-2, 1, 24, 2, 5, 24, "air")
    # elevated rail across the city
    v.fill(-90, 14, 30, 90, 14, 34, "iron_block"); v.fill(-90, 15, 32, 90, 15, 32, "rail")
    for x in range(-88, 90, 16):
        v.fill(x, 1, 31, x, 13, 33, "iron_block")
    v.fill(0, 16, 31, 14, 18, 33, "red_terracotta"); v.fill(1, 17, 32, 13, 17, 32, "air")     # a tram
    v.windows(0, 17, 31, 14, 33, "glass_pane", period=2, offset=1)
    # Avatar Aang Memorial Island in the bay
    v.disc(40, 0, 70, 14, "stone"); v.fill(36, 1, 66, 44, 6, 74, "stone_bricks")
    S.statue(v, 40, 70, 24, "copper_block", y=7)
    v.set(37, 7 + 2 * 24 // 3 + 6, 70, "oak_fence")                                               # the staff
    # the spirit portal from the finale, in the crater downtown
    v.disc(-50, 0, 10, 10, "yellow_terracotta", hollow=True)
    v.disc(-50, 0, 10, 9, "moss_block")
    v.fill(-50, 1, 10, -50, 60, 10, "yellow_stained_glass")
    for a in range(0, 360, 45):
        v.fill(round(-50 + 2 * math.cos(math.radians(a))), 1, round(10 + 2 * math.sin(math.radians(a))),
               round(-50 + 2 * math.cos(math.radians(a))), 50, round(10 + 2 * math.sin(math.radians(a))), "yellow_stained_glass")
    v.set(-50, 1, 10, "beacon"); v.fill(-51, 0, 9, -49, 0, 11, "iron_block")
    for (x, z) in ((-60, 0), (-40, 20), (-62, 22), (-38, -2)):                                      # spirit vines
        v.column(x, 1, z, 8, "warped_stem"); v.sphere(x, 9, z, 2, "warped_wart_block", hollow=False)
    # Satomobiles on the avenue
    for (x, z, c) in ((-30, 28, "red_concrete"), (10, 27, "black_concrete"), (40, 29, "blue_concrete")):
        v.fill(x, 1, z, x + 5, 1, z + 2, c); v.fill(x + 1, 2, z, x + 4, 2, z + 2, "glass")
        v.set(x, 0, z - 1, "coal_block"); v.set(x + 5, 0, z - 1, "coal_block")


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
