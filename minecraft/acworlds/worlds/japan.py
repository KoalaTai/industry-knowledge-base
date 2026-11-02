"""Azuchi-Momoyama Japan - Assassin's Creed Shadows (2025), 1579-1581."""

from .. import structures as S
from ..palettes import JAPAN
from ..registry import Build, World
from ..voxel import Voxel

P = JAPAN


def azuchi(v: Voxel) -> None:
    """Oda Nobunaga's Azuchi Castle (1579): the seven-storey tenshu on its stone base above Lake Biwa."""
    S.pad(v, -70, -60, 70, 70, "grass_block")
    v.fill(-70, -3, 44, 70, 0, 70, "water")
    for k in range(10):
        v.disc(0, 1 + k, 0, 50 - k * 2.5, "coarse_dirt" if k % 2 else "grass_block", rz=36 - k * 2)
    tmp = Voxel()
    S.japanese_castle(tmp, 0, 0, P, stories=5)
    v.merge(tmp, 0, 10, 0)
    for k in range(10):                                                            # stone stair up the hill
        v.fill(-2, 1 + k, 36 - k * 2, 2, 1 + k, 37 - k * 2, "stone_bricks")
    for (x, z) in ((-30, -20), (30, -20), (-30, 20), (30, 20)):                     # yagura corner towers
        tmp = Voxel()
        S.tower(tmp, 0, 0, 3, 8, P, top="pyramid", square=True, wall="white_concrete")
        v.merge(tmp, x, 6, z)
    for x in range(-34, 35, 2):
        v.set(x, 7, -24, "white_concrete"); v.set(x, 7, 24, "white_concrete")        # plaster walls
    v.fill(-6, 1, 50, 6, 1, 66, "oak_planks")                                        # lake jetty
    for i in range(8):
        v.tree(-60 + i * 17, 1, -56, "cherry_log", "cherry_leaves[persistent=true]", height=5, canopy=3)


def kyoto(v: Voxel) -> None:
    """Kyoto: Kinkaku-ji on its pond, a five-storey pagoda, a torii-lined shrine path and a dry garden."""
    S.pad(v, -70, -60, 70, 60, "grass_block")
    # Kinkaku-ji, the Golden Pavilion (1397), reflected in the Mirror Pond
    v.disc(-35, 0, 10, 30, "water", rz=22)
    v.disc(-35, 0, 10, 10, "grass_block", rz=8)
    gx, gz = -35, 10
    v.fill(gx - 7, 1, gz - 6, gx + 7, 4, gz + 6, "white_concrete")
    v.fill(gx - 6, 1, gz - 5, gx + 6, 4, gz + 5, "air")
    v.fill(gx - 8, 5, gz - 7, gx + 8, 5, gz + 7, P["roof"])
    v.fill(gx - 6, 6, gz - 5, gx + 6, 9, gz + 5, "gold_block")
    v.fill(gx - 5, 6, gz - 4, gx + 5, 9, gz + 4, "air")
    v.fill(gx - 7, 10, gz - 6, gx + 7, 10, gz + 6, P["roof"])
    v.fill(gx - 4, 11, gz - 3, gx + 4, 14, gz + 3, "gold_block")
    v.fill(gx - 3, 11, gz - 2, gx + 3, 14, gz + 2, "air")
    v.pyramid(gx, 15, gz, 11, 4, P["roof"])
    v.set(gx, 19, gz, "gold_block")                                                 # the phoenix
    for i in range(3):
        v.disc(-50 + i * 10, 1, 25, 2, "stone")                                     # garden islands
    # To-ji pagoda
    S.pagoda(v, 30, -30, P, stories=5, half=6, story_h=5)
    # Fushimi Inari-style path of vermilion torii
    for z in range(-50, 40, 5):
        S.torii(v, 55, z, half=3, h=7)
    v.fill(53, 0, -52, 57, 0, 42, "gravel")
    # Ryoan-ji dry garden: raked gravel, fifteen stones, earthen wall
    v.fill(-10, 0, -50, 30, 0, -30, "white_concrete_powder")
    v.walls(-11, 1, -51, 31, 2, -29, "packed_mud")
    v.fill(-11, 1, -29, 31, 2, -29, "air")
    for (sx, sz) in ((-4, -44), (2, -42), (8, -45), (16, -38), (22, -44), (12, -34), (-6, -34)):
        v.set(sx, 1, sz, "mossy_cobblestone")
        v.set(sx + 1, 1, sz, "stone")
    S.house(v, -30, -50, 16, 10, P, floors=1, roof="hip", wall="dark_oak_planks")     # temple hall
    S.city_block(v, -68, 30, P, cols=4, rows=1, lot=9, street=3, floors=(1, 2), roof="gable", seed=110)


def iga(v: Voxel) -> None:
    """Naoe's Iga: a shinobi village of thatched farmhouses in terraced rice paddies, with a hidden training hall."""
    S.pad(v, -70, -60, 70, 60, "grass_block")
    for i in range(5):                                                                # terraced paddies
        z1 = -58 + i * 12
        v.fill(-68, i, z1, 68, i, z1 + 10, "water")
        v.fill(-68, i, z1 + 10, 68, i + 1, z1 + 11, "coarse_dirt")
        for x in range(-66, 68, 3):
            v.set(x, i + 1, z1 + 3, "sugar_cane"); v.set(x + 1, i + 1, z1 + 7, "sugar_cane")
    for (x, z) in ((-50, 10), (-25, 15), (0, 8), (25, 14), (50, 10)):
        S.house(v, x, z, 12, 9, {**P, "roof": "hay_block"}, floors=1, roof="gable", wall="dark_oak_planks")
    # training hall with hidden cellar (the ninja house)
    S.house(v, -10, 32, 20, 14, P, floors=2, roof="hip", wall="dark_oak_planks")
    v.fill(-6, -4, 36, 6, -1, 44, "air")
    v.fill(-7, -5, 35, 7, -5, 45, "stone")
    v.fill(-7, -4, 35, 7, -1, 35, "stone"); v.fill(-7, -4, 45, 7, -1, 45, "stone")
    v.fill(-7, -4, 35, -7, -1, 45, "stone"); v.fill(7, -4, 35, 7, -1, 45, "stone")
    v.fill(0, -4, 40, 0, 0, 40, "ladder[facing=north]")
    v.set(0, 1, 40, "oak_trapdoor[half=top]")
    for i in range(12):                                                               # cedar forest
        v.tree(-65 + i * 12, 1, 54, "spruce_log", "spruce_leaves[persistent=true]", height=9, canopy=2)
    v.fill(-60, 0, 28, 60, 0, 30, "gravel")


def shrine(v: Voxel) -> None:
    """A Shinto shrine: torii, water basin, stone lanterns, the haiden and honden among cherry trees."""
    S.pad(v, -40, -40, 40, 40, "grass_block")
    v.fill(-3, 0, -40, 3, 0, 40, "gravel")
    S.torii(v, 0, 36, half=5, h=9)
    for z in range(30, -5, -8):
        for x in (-6, 6):
            v.column(x, 1, z, 3, "stone"); v.set(x, 4, z, "lantern"); v.set(x, 5, z, "stone_slab")
    v.fill(10, 1, 20, 12, 1, 22, "stone"); v.set(11, 1, 21, "water")                 # temizuya basin
    S.house(v, -12, -14, 25, 12, P, floors=1, roof="hip", wall="dark_oak_planks")       # haiden
    v.fill(-13, 1, -1, 13, 1, 0, "oak_planks")
    S.house(v, -6, -36, 13, 10, {**P, "roof": "dark_oak_planks"}, floors=1, roof="gable", wall="stripped_dark_oak_log")   # honden
    for x in range(-7, 8, 2):
        v.set(x, 11, -30, "gold_block")
    for x in range(-35, 36, 14):
        v.tree(x, 1, -30, "cherry_log", "cherry_leaves[persistent=true]", height=5, canopy=3)
        v.tree(x, 1, 30, "cherry_log", "cherry_leaves[persistent=true]", height=5, canopy=3)


WORLD = World(
    id="japan",
    name="Sengoku Japan",
    game="Assassin's Creed Shadows (2025)",
    era="1579-1581, the Azuchi-Momoyama period",
    description="Naoe's and Yasuke's Japan: Azuchi Castle, Kyoto, the Iga shinobi villages and a Shinto shrine.",
).build(Build("azuchi", "Azuchi Castle", "Nobunaga's tenshu on its sloped stone base above the lake, with yagura towers and plaster walls.", azuchi)
).build(Build("kyoto", "Kyoto", "The Golden Pavilion on its pond, a five-storey pagoda, a torii path and the Ryoan-ji dry garden.", kyoto)
).build(Build("iga", "Iga Province", "Thatched farmhouses in terraced rice paddies with a shinobi training hall and hidden cellar.", iga)
).build(Build("shrine", "Shinto Shrine", "Torii, stone lanterns, water basin, haiden and honden among cherry trees.", shrine))
