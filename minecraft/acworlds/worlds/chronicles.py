"""Assassin's Creed Chronicles (2015-2016): China 1526, India 1841, Russia 1918."""

from .. import structures as S
from ..palettes import CHINA, INDIA, RUSSIA
from ..registry import Build, World
from ..voxel import Voxel


def great_wall(v: Voxel) -> None:
    """A Ming-dynasty stretch of the Great Wall over hills, with beacon towers (Shao Jun's China, 1526)."""
    S.pad(v, -100, -40, 100, 40, "grass_block")
    import math
    for x in range(-100, 101):
        h = int(10 + 8 * math.sin(x / 23) + 4 * math.sin(x / 7))
        v.fill(x, 1, -40, x, h, 40, "grass_block" if h % 2 else "coarse_dirt")
        v.fill(x, h + 1, -3, x, h + 6, 3, "stone_bricks")                              # wall body
        v.fill(x, h + 2, -2, x, h + 6, 2, "air")
        v.fill(x, h + 6, -2, x, h + 6, 2, "stone_bricks")
        if x % 2 == 0:
            v.set(x, h + 7, -3, "stone_bricks"); v.set(x, h + 7, 3, "stone_bricks")
        if x % 40 == 0:
            tmp = Voxel()
            S.tower(tmp, 0, 0, 4, 10, CHINA, top="flat", square=True, wall="stone_bricks")
            tmp.fill(-3, 11, -3, 3, 11, 3, "gray_terracotta")
            tmp.crenellate(-4, 11, -4, 4, 4, "stone_bricks")
            v.merge(tmp, x, h + 1, 0)
            v.set(x, h + 13, 0, "campfire")                                               # beacon
    # Forbidden City style gate hall at the east end
    hx, hz = 70, 20
    v.fill(hx - 16, 1, hz, hx + 16, 8, hz + 10, "red_terracotta")
    v.fill(hx - 2, 1, hz, hx + 2, 6, hz + 10, "air")
    for x in range(hx - 14, hx + 15, 4):
        v.column(x, 9, hz + 2, 6, "red_terracotta"); v.column(x, 9, hz + 8, 6, "red_terracotta")
    v.fill(hx - 16, 15, hz - 1, hx + 16, 15, hz + 11, "yellow_terracotta")
    v.gable_roof(hx - 15, 16, hz, hx + 15, hz + 10, "yellow_terracotta", ridge_axis="x", overhang=1)


def amritsar(v: Voxel) -> None:
    """The Harmandir Sahib (Golden Temple) in its sacred pool, Sikh Empire 1841 (Arbaaz Mir's India)."""
    S.pad(v, -60, -60, 60, 60, "polished_diorite")
    v.fill(-50, -2, -50, 50, 0, 50, "water")
    v.fill(-52, 0, -52, 52, 0, -51, "polished_diorite"); v.fill(-52, 0, 51, 52, 0, 52, "polished_diorite")
    v.fill(-52, 0, -52, -51, 0, 52, "polished_diorite"); v.fill(51, 0, -52, 52, 0, 52, "polished_diorite")
    v.fill(-12, 0, -12, 12, 0, 12, "white_concrete")
    v.fill(-10, 1, -10, 10, 6, 10, "white_concrete")
    v.fill(-9, 1, -9, 9, 5, 9, "air")
    v.fill(-9, 1, -9, 9, 1, 9, "polished_diorite")
    v.fill(-10, 7, -10, 10, 7, 10, "gold_block")
    v.fill(-7, 8, -7, 7, 12, 7, "gold_block")
    v.fill(-6, 8, -6, 6, 11, 6, "air")
    v.fill(-7, 13, -7, 7, 13, 7, "gold_block")
    v.dome(0, 13, 0, 5, "gold_block")
    for px in (-9, 9):
        for pz in (-9, 9):
            v.column(px, 8, pz, 5, "gold_block"); v.dome(px, 13, pz, 1.5, "gold_block")
    v.fill(-1, 1, 12, 1, 1, 50, "white_concrete")                                       # the causeway
    for z in range(14, 50, 6):
        v.set(-2, 2, z, "lantern"); v.set(2, 2, z, "lantern")
    for x in range(-50, 51, 25):
        S.house(v, x - 6, 54, 12, 8, INDIA, floors=2, roof="flat", wall="white_concrete")
    S.stepwell(v, 0, -80, INDIA, half=10, depth=8)


def petrograd(v: Voxel) -> None:
    """Revolutionary Petrograd 1918: a Kremlin-style wall, an onion-domed cathedral and the Winter Palace facade (Nikolai Orelov's Russia)."""
    S.pad(v, -80, -60, 80, 60, "snow_block")
    S.curtain_wall(v, -60, -50, 60, 10, 9, {**RUSSIA, "wall": "bricks"}, gate="south", tower_r=4)
    for (x, z) in ((-60, -50), (60, -50), (-60, 10), (60, 10)):
        v.cone(x, 14, z, 5, 10, "green_terracotta")
    # cathedral with five onion domes
    cx, cz = 0, -20
    v.fill(cx - 14, 1, cz - 14, cx + 14, 14, cz + 14, "white_concrete")
    v.fill(cx - 13, 1, cz - 13, cx + 13, 13, cz + 13, "air")
    v.fill(cx - 13, 1, cz - 13, cx + 13, 1, cz + 13, RUSSIA["floor"])
    for (dx, dz, r, c) in ((0, 0, 6, "gold_block"), (-9, -9, 3, "blue_concrete"), (9, -9, 3, "lime_concrete"),
                           (-9, 9, 3, "red_concrete"), (9, 9, 3, "yellow_concrete")):
        v.cylinder(cx + dx, 15, cz + dz, r - 1, 4, "white_concrete", hollow=True)
        v.sphere(cx + dx, 21, cz + dz, r, c, hollow=True, y_min=19)
        v.cone(cx + dx, 21 + r, cz + dz, 1.5, 4, c)
        v.set(cx + dx, 26 + r, cz + dz, "gold_block")
    v.fill(cx - 2, 1, cz + 14, cx + 2, 5, cz + 14, "air")
    # Winter Palace long facade in green and white
    v.fill(-78, 1, 24, 78, 12, 40, "lime_terracotta")
    v.fill(-77, 1, 25, 77, 11, 39, "air")
    for y in (3, 4, 8, 9):
        v.windows(-78, y, 24, 78, 40, "glass_pane", period=3, offset=2)
    for x in range(-78, 79, 6):
        v.column(x, 1, 24, 12, "white_concrete")
    v.fill(-78, 13, 24, 78, 13, 40, "white_concrete")
    v.fill(-1, 1, 24, 1, 5, 24, "air")
    # armoured train on a siding
    v.fill(-70, 0, 50, 70, 0, 50, "rail")
    v.fill(-40, 1, 49, -10, 3, 51, "gray_concrete")
    v.fill(-8, 1, 49, 10, 3, 51, "black_concrete")
    v.column(6, 4, 50, 3, "black_concrete")
    for x in range(-38, -12, 4):
        v.set(x, 2, 48, "iron_bars"); v.set(x, 2, 52, "iron_bars")


WORLD = World(
    id="chronicles",
    name="Assassin's Creed Chronicles",
    game="AC Chronicles: China (2015), India (2016), Russia (2016)",
    era="1526, 1841 and 1918",
    description="Shao Jun's Ming China, Arbaaz Mir's Sikh Empire and Nikolai Orelov's revolutionary Russia.",
).build(Build("great_wall", "The Great Wall", "A Ming stretch of wall over rolling hills with beacon towers and a palace gate hall.", great_wall)
).build(Build("amritsar", "Amritsar", "The Golden Temple in its sacred pool with the causeway, plus a stepwell.", amritsar)
).build(Build("petrograd", "Petrograd", "Kremlin-style wall, an onion-domed cathedral, the Winter Palace facade and an armoured train.", petrograd))
