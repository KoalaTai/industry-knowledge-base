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
from ..voxel import Voxel

HAVEN = _p(ground="stone", wall="deepslate_bricks", wall2="green_terracotta", trim="polished_deepslate",
           roof="lime_terracotta", floor="polished_andesite", column="deepslate_bricks", path="andesite",
           leaves="oak_leaves[persistent=true]", log="oak_log")
WASTE = "tuff"


def _crater(v: Voxel, cx: int, cz: int, r: int, depth: int) -> None:
    for k in range(depth):
        v.disc(cx, -k, cz, r * (1 - k / (depth + 1)), "air")
    v.disc(cx, -depth, cz, r * 0.4, "magma_block")


def haven(v: Voxel) -> None:
    """A surviving haven: concentric earthbent walls, terraced farms, a spirit-lit core, and the wastes outside."""
    S.pad(v, -90, -90, 90, 90, WASTE)
    for (x, z, r) in ((-70, 60, 14), (65, -55, 18), (-60, -70, 10)):
        _crater(v, x, z, r, 6)
    v.cylinder(0, 1, 0, 70, 14, "deepslate_bricks", hollow=True)                               # outer wall
    v.cylinder(0, 1, 0, 69, 14, "deepslate_bricks", hollow=True)
    v.disc(0, 15, 0, 70, "polished_deepslate", hollow=True); v.disc(0, 15, 0, 69, "polished_deepslate", hollow=True)
    for a in range(0, 360, 30):
        S.tower(v, round(70 * math.cos(math.radians(a))), round(70 * math.sin(math.radians(a))), 3, 18, HAVEN, top="flat", wall="deepslate_bricks")
    v.fill(-3, 1, 64, 3, 7, 70, "air")                                                             # the gate
    v.disc(0, 0, 0, 68, "grass_block")
    for k in range(4):                                                                              # terraced fields
        r = 60 - k * 6
        v.disc(0, 1 + k, 0, r, "grass_block"); v.disc(0, 1 + k, 0, r, "andesite", hollow=True)
        for a in range(0, 360, 5):
            x = round((r - 2) * math.cos(math.radians(a))); z = round((r - 2) * math.sin(math.radians(a)))
            v.set(x, 1 + k, z, "farmland[moisture=7]"); v.set(x, 2 + k, z, ("wheat[age=7]", "carrots[age=7]", "potatoes[age=7]")[k % 3])
    v.disc(0, 5, 0, 36, "andesite")
    rng = random.Random(500)
    for a in range(0, 360, 24):
        x = round(28 * math.cos(math.radians(a))); z = round(28 * math.sin(math.radians(a)))
        tmp = Voxel()
        S.house(tmp, -4, -3, rng.randint(7, 9), rng.randint(6, 8), HAVEN, floors=rng.randint(1, 3), roof="flat", wall=rng.choice(("deepslate_bricks", "green_terracotta", "smooth_sandstone")))
        v.merge(tmp, x, 5, z)
    # the core: a spirit-lit crystal that keeps the haven alive, on a stepped earthbent plinth
    for k in range(5):
        v.disc(0, 6 + k, 0, 12 - k * 2, "polished_deepslate")
    v.fill(-2, 11, -2, 2, 22, 2, "amethyst_block"); v.fill(-1, 23, -1, 1, 26, 1, "amethyst_block")
    v.set(0, 27, 0, "end_rod"); v.set(0, 11, 0, "sea_lantern")
    for a in range(0, 360, 90):
        v.set(round(4 * math.cos(math.radians(a))), 11, round(4 * math.sin(math.radians(a))), "lantern")
    v.disc(0, 5, 0, 16, "water", hollow=True); v.disc(0, 5, 0, 15, "water", hollow=True)            # moat around the core
    for i in range(14):
        v.tree(round(44 * math.cos(math.radians(i * 26))), 2, round(44 * math.sin(math.radians(i * 26))), "oak_log", "oak_leaves[persistent=true]", height=5, canopy=2)
    # a scavenger caravan approaching across the wastes
    v.fill(-6, 1, 78, 2, 2, 80, "dark_oak_planks"); v.fill(-7, 0, 77, 3, 0, 81, "coal_block")
    v.fill(-14, 1, 78, -10, 3, 80, "brown_wool")


def wastes(v: Voxel) -> None:
    """The cataclysm's aftermath: a fallen city half buried in ash, cracked earth, a spirit-corrupted vine field and a cold portal."""
    S.pad(v, -90, -90, 90, 90, WASTE)
    rng = random.Random(510)
    for _ in range(40):                                                                             # cracks
        x, z = rng.randint(-85, 85), rng.randint(-85, 85)
        v.fill(x, -4, z, x + rng.randint(5, 30), 0, z + 1, "air"); v.fill(x, -5, z, x + 30, -5, z + 1, "lava")
    for (x, z, r) in ((40, 40, 26), (-50, -30, 18), (10, -60, 12)):
        _crater(v, x, z, r, 8)
    # toppled skyscrapers from an old Republic-style city
    for i, (x, z, h) in enumerate(((-70, 20, 30), (-55, 50, 24), (-30, 65, 36), (60, -20, 28))):
        v.fill(x, 1, z, x + 10, 14, z + 10, "light_gray_concrete"); v.fill(x + 1, 1, z + 1, x + 9, 13, z + 9, "air")
        for k in range(h):                                                                          # the fallen top lying on its side
            v.fill(x + 12 + k, 1, z + 1, x + 12 + k, 9, z + 9, "light_gray_concrete" if k % 4 else "air")
        v.fill(x + 12, 1, z + 1, x + 12 + h, 1, z + 9, "gray_concrete_powder")
        v.windows(x, 4, z, x + 10, z + 10, "air", period=2, offset=1)
    v.fill(-90, 0, -90, 90, 0, -70, "gray_concrete_powder")                                          # ash drifts
    for x in range(-88, 90, 7):
        v.cone(x, 1, -80 + (x % 5), 2, rng.randint(2, 5), "gray_concrete_powder")
    # corrupted spirit vines
    for _ in range(25):
        x, z = rng.randint(0, 80), rng.randint(0, 80)
        v.column(x, 1, z, rng.randint(3, 10), "crimson_stem"); v.set(x, 1 + rng.randint(3, 10), z, "shroomlight")
    # a dead portal
    v.disc(-60, 0, -40, 8, "obsidian"); v.fill(-60, 1, -40, -60, 20, -40, "crying_obsidian")
    v.fill(-30, 1, 10, -26, 4, 14, "iron_block"); v.set(-28, 5, 12, "campfire")                       # a ruined mech core, still warm
    S.ruined_wall(v, 20, 70, 50, block="deepslate_bricks", seed=511)


def seven_havens_map(v: Voxel) -> None:
    """A 1:12 model of the whole post-cataclysm world: seven havens as walled circles across a scarred continent."""
    S.pad(v, -80, -80, 80, 80, "water")
    v.fill(-80, -3, -80, 80, -1, 80, "water")
    v.disc(0, 0, 0, 72, WASTE, rz=60)
    v.disc(0, -1, 0, 74, "sand", rz=62)
    rng = random.Random(520)
    for _ in range(30):
        x, z = rng.randint(-60, 60), rng.randint(-50, 50)
        _crater(v, x, z, rng.randint(4, 10), 3)
    styles = (("packed_ice", "Southern haven"), ("red_terracotta", "Fire haven"), ("green_terracotta", "Earth haven"),
              ("smooth_quartz", "Air haven"), ("light_gray_concrete", "City haven"), ("sandstone", "Desert haven"),
              ("iron_block", "Metal haven"))
    for i, (block, _name) in enumerate(styles):
        a = i * 360 / 7
        x = round(44 * math.cos(math.radians(a))); z = round(36 * math.sin(math.radians(a)))
        v.disc(x, 1, z, 9, "grass_block"); v.disc(x, 1, z, 9, block, hollow=True); v.disc(x, 2, z, 9, block, hollow=True)
        v.fill(x - 1, 2, z - 1, x + 1, 5, z + 1, block); v.set(x, 6, z, "sea_lantern")
        for k in range(1, 9):                                                                       # roads between havens
            nx = round(44 * math.cos(math.radians(a + 360 / 7))); nz = round(36 * math.sin(math.radians(a + 360 / 7)))
            v.set(round(x + (nx - x) * k / 9), 1, round(z + (nz - z) * k / 9), "andesite")
    v.fill(-1, 1, -1, 1, 12, 1, "amethyst_block"); v.set(0, 13, 0, "end_rod")                           # the cataclysm's epicentre
    _crater(v, 0, 0, 14, 4); v.fill(-1, 1, -1, 1, 12, 1, "amethyst_block")


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
