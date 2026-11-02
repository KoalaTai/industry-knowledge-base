"""Renaissance Italy - Assassin's Creed II (2009) and Brotherhood (2010), 1476-1507."""

import math

from .. import structures as S
from ..palettes import ROME, TUSCANY, VENICE
from ..registry import Build, World
from ..voxel import Voxel


def florence(v: Voxel) -> None:
    """Santa Maria del Fiore with Brunelleschi's dome, Giotto's campanile,
    the Palazzo Vecchio and the Ponte Vecchio over the Arno."""
    P = TUSCANY
    S.pad(v, -80, -70, 90, 80, "stone")
    # Duomo: long nave, octagonal crossing, dome in red tiles with white ribs
    cx, z0 = 0, -60
    S.basilica(v, cx, z0, TUSCANY, length=60, width=27, h=18)
    v.cylinder(cx, 2, z0 + 60, 17, 22, "white_terracotta", hollow=True)    # octagonal drum (approx)
    v.cylinder(cx, 2, z0 + 60, 16, 22, "air", hollow=True)
    v.disc(cx, 1, z0 + 60, 16, P["floor"])
    for y in range(6, 22, 5):
        for a in range(0, 360, 45):
            v.set(round(cx + 17 * math.cos(math.radians(a))), y, round(z0 + 60 + 17 * math.sin(math.radians(a))), "green_terracotta")
    v.disc(cx, 24, z0 + 60, 17, "white_terracotta")
    v.disc(cx, 24, z0 + 60, 15, "air")
    v.dome(cx, 24, z0 + 60, 17, "terracotta")
    for a in range(0, 360, 45):                                            # eight white ribs
        for k in range(18):
            r = math.sqrt(max(0, 17 ** 2 - k ** 2))
            v.set(round(cx + r * math.cos(math.radians(a))), 24 + k, round(z0 + 60 + r * math.sin(math.radians(a))), "white_concrete")
    v.cylinder(cx, 41, z0 + 60, 3, 6, "white_concrete", hollow=True)       # lantern
    v.cone(cx, 47, z0 + 60, 3, 4, "white_concrete")
    v.set(cx, 51, z0 + 60, "gold_block")
    # campanile: slender square tower in white/green/pink marble
    tx, tz = cx - 20, z0 + 3
    for y in range(1, 46):
        block = ("white_terracotta", "lime_terracotta", "pink_terracotta")[(y // 5) % 3]
        v.walls(tx - 3, y, tz - 3, tx + 3, y, tz + 3, block)
    v.fill(tx - 2, 1, tz - 2, tx + 2, 45, tz + 2, "air")
    for y in (20, 30, 40):
        v.windows(tx - 3, y, tz - 3, tx + 3, tz + 3, "air", period=2, offset=2)
        v.windows(tx - 3, y + 1, tz - 3, tx + 3, tz + 3, "air", period=2, offset=2)
    v.fill(tx - 4, 46, tz - 4, tx + 4, 46, tz + 4, "white_terracotta")
    # Palazzo Vecchio: rusticated block with crenellations and the Arnolfo tower
    px, pz = 40, 10
    v.fill(px, 1, pz, px + 30, 20, pz + 24, "stone_bricks")
    v.fill(px + 1, 1, pz + 1, px + 29, 19, pz + 23, "air")
    v.fill(px + 1, 1, pz + 1, px + 29, 1, pz + 23, P["floor"])
    for y in (6, 12, 17):
        v.windows(px, y, pz, px + 30, pz + 24, P["window"], period=3, offset=2)
    v.fill(px - 1, 21, pz - 1, px + 31, 22, pz + 25, "stone_bricks")
    v.crenellate(px - 1, 23, pz - 1, px + 31, pz + 25, "stone_bricks")
    S.tower(v, px + 8, pz + 2, 2.5, 50, TUSCANY, top="crenel", square=True, wall="stone_bricks")
    v.fill(px + 14, 1, pz + 24, px + 16, 5, pz + 24, "air")
    # Piazza della Signoria with the Loggia
    S.plaza(v, px - 40, pz, px - 2, pz + 24, TUSCANY, fountain=True)
    # Ponte Vecchio across the Arno (the river runs along x at z 50..62)
    v.fill(-80, -3, 50, 90, 0, 62, "water")
    S.arched_bridge(v, -20, 50, 45, 13, TUSCANY, arches=3, axis="z", deck_y=5, shops=False)
    for i in range(-18, 24, 7):                                            # the goldsmiths' shops
        for side in (-5, 13):
            v.fill(i, 7, 50 + side, i + 4, 9, 50 + side + 3, "orange_terracotta")
            v.fill(i + 1, 7, 51 + side, i + 3, 8, 51 + side + 2, "air")
            v.fill(i, 10, 50 + side, i + 4, 10, 50 + side + 3, "terracotta")
    # Florentine streets
    S.city_block(v, -78, -30, TUSCANY, cols=3, rows=3, lot=10, street=4, floors=(2, 3), roof="gable", seed=12)
    S.city_block(v, 45, -65, TUSCANY, cols=3, rows=3, lot=10, street=4, floors=(2, 3), roof="gable", seed=13)


def monteriggioni(v: Voxel) -> None:
    """Ezio's hill town: ring wall with 14 towers, the Villa Auditore, the market square."""
    P = TUSCANY
    S.pad(v, -60, -60, 60, 60, "grass_block")
    for k in range(6):
        v.disc(0, 1 + k, 0, 52 - k * 2, "coarse_dirt" if k % 2 else "grass_block")
    y0 = 7
    town = Voxel()
    town.cylinder(0, 1, 0, 40, 8, "stone_bricks", hollow=True)
    town.cylinder(0, 1, 0, 39, 8, "stone_bricks", hollow=True)
    town.disc(0, 1, 0, 38, "cobblestone")
    for a in range(0, 360, 26):                                            # 14 towers
        tx = round(40 * math.cos(math.radians(a)))
        tz = round(40 * math.sin(math.radians(a)))
        S.tower(town, tx, tz, 3, 13, TUSCANY, top="crenel", square=True, wall="stone_bricks")
    town.fill(-2, 1, 38, 2, 5, 40, "air")                                  # Porta Romana
    # Villa Auditore at the top of the main street
    S.house(town, -12, -34, 25, 16, TUSCANY, floors=3, roof="hip", wall="smooth_sandstone")
    town.fill(-14, 1, -18, 14, 1, -16, "stone_bricks")
    S.plaza(town, -14, -14, 14, 10, TUSCANY, fountain=True)
    for (hx, hz) in ((-34, -10), (-34, 6), (18, -10), (18, 6), (-30, 18), (14, 18)):
        S.house(town, hx, hz, 12, 10, TUSCANY, floors=2, roof="gable", wall="white_terracotta" if hx < 0 else "smooth_sandstone")
    v.merge(town, 0, y0 - 1, 0)
    for k in range(8):
        v.fill(-2, 1 + k, 58 - k * 2, 2, 1 + k, 59 - k * 2, "cobblestone")
    for i in range(10):
        v.tree(-55 + i * 11, 1, 56, "dark_oak_log", "dark_oak_leaves[persistent=true]", height=5)


def venice(v: Voxel) -> None:
    """Piazza San Marco, the campanile, the Doge's Palace, the Rialto and a canal."""
    P = VENICE
    S.pad(v, -80, -60, 80, 70, "stone")
    v.fill(-80, -3, 40, 80, 0, 70, "water")                                # the lagoon / Grand Canal
    v.fill(-80, -3, -10, -60, 0, 40, "water")
    v.fill(-80, 0, 38, 80, 0, 39, "stone_bricks")
    # Doge's Palace: pink diamond pattern over a double arcade
    px, pz = 0, 10
    v.fill(px, 1, pz, px + 50, 6, pz + 26, P["column"])
    v.fill(px + 1, 1, pz + 1, px + 49, 6, pz + 25, "air")
    for x in range(px, px + 51, 3):
        v.column(x, 1, pz + 26, 6, "quartz_pillar")
        v.column(x, 1, pz, 6, "quartz_pillar")
    for y in range(7, 20):
        for x in range(px, px + 51):
            for zz in (pz, pz + 26):
                v.set(x, y, zz, "pink_terracotta" if (x + y) % 4 < 2 else "white_terracotta")
        v.fill(px, y, pz + 1, px, y, pz + 25, "white_terracotta")
        v.fill(px + 50, y, pz + 1, px + 50, y, pz + 25, "white_terracotta")
    v.windows(px, 12, pz, px + 50, pz + 26, P["window"], period=5, offset=3)
    v.fill(px, 20, pz, px + 50, 20, pz + 26, "white_terracotta")
    v.crenellate(px, 21, pz, px + 50, pz + 26, "quartz_block", period=2)
    v.fill(px + 1, 1, pz + 1, px + 49, 1, pz + 25, P["floor"])
    # St Mark's basilica: five domes
    bx, bz = -60, 0
    v.fill(bx, 1, bz, bx + 40, 14, bz + 36, "white_terracotta")
    v.fill(bx + 1, 1, bz + 1, bx + 39, 13, bz + 35, "air")
    v.fill(bx + 1, 1, bz + 1, bx + 39, 1, bz + 35, "polished_diorite")
    for dx, dz in ((20, 18), (8, 18), (32, 18), (20, 6), (20, 30)):
        v.cylinder(bx + dx, 15, bz + dz, 6, 3, "light_gray_terracotta", hollow=True)
        v.dome(bx + dx, 17, bz + dz, 6, "gray_concrete")
        v.set(bx + dx, 24, bz + dz, "gold_block")
    for x in range(bx + 4, bx + 40, 8):
        v.fill(x - 2, 1, bz + 36, x + 2, 6, bz + 36, "air")
    v.fill(bx + 10, 15, bz + 32, bx + 30, 15, bz + 36, "gold_block")      # the four horses' terrace
    # campanile
    S.tower(v, -14, 2, 4, 55, VENICE, top="pyramid", square=True, wall="bricks")
    v.fill(-18, 50, -2, -10, 55, 6, "white_terracotta")
    v.fill(-17, 50, -1, -11, 54, 5, "air")
    v.set(-14, 66, 2, "gold_block")
    S.pad(v, -58, 0, 0, 38, "polished_diorite")                            # Piazza San Marco
    # Rialto bridge over the canal, with its arcade of shops
    S.arched_bridge(v, 20, 40, 30, 9, VENICE, arches=1, axis="z", deck_y=7, shops=False)
    for z in range(42, 66, 6):
        v.fill(21, 9, z, 22, 11, z + 3, "white_terracotta")
        v.fill(26, 9, z, 27, 11, z + 3, "white_terracotta")
        v.fill(20, 12, z - 1, 28, 12, z + 4, "terracotta")
    # gondolas
    for i, gx in enumerate((-40, -20, 50)):
        v.fill(gx, 0, 50 + i * 4, gx + 8, 0, 50 + i * 4, "black_concrete")
        v.set(gx - 1, 1, 50 + i * 4, "black_concrete"); v.set(gx + 9, 1, 50 + i * 4, "black_concrete")
    S.city_block(v, 54, -56, VENICE, cols=2, rows=3, lot=9, street=3, floors=(3, 4), roof="flat", seed=21)
    S.city_block(v, -78, -56, VENICE, cols=2, rows=3, lot=9, street=3, floors=(3, 4), roof="flat", seed=22)


def rome(v: Voxel) -> None:
    """Brotherhood's Rome: the Colosseum, the Pantheon, Castel Sant'Angelo and the Tiber."""
    S.pad(v, -120, -100, 120, 110, "grass_block")
    S.colosseum(v, -55, 30, ROME, rx=44, rz=36, tiers=3, tier_h=8)
    S.pantheon(v, 50, -40, ROME, r=16)
    # Castel Sant'Angelo: drum on a square base, by the river
    v.fill(-120, -3, 80, 120, 0, 100, "water")
    cx, cz = 40, 50
    v.fill(cx - 22, 1, cz - 22, cx + 22, 6, cz + 22, "stone_bricks")
    v.cylinder(cx, 7, cz, 18, 14, "smooth_stone", hollow=False)
    v.cylinder(cx, 21, cz, 12, 8, "bricks", hollow=True)
    v.disc(cx, 29, cz, 12, "smooth_stone")
    S.statue(v, cx, cz, 9, "copper_block", y=30)                            # the archangel
    v.crenellate(cx - 22, 7, cz - 22, cx + 22, cz + 22, "stone_bricks")
    S.arched_bridge(v, cx - 4, 80, 20, 9, ROME, arches=3, axis="z", deck_y=4)
    # ruined Forum colonnade and the Via
    S.roman_road(v, -110, -70, 200)
    for x in range(-60, 20, 6):
        v.column(x, 1, -84, 6 + (x // 6) % 4, "quartz_pillar")
    S.ruined_wall(v, -60, -90, 70, seed=4)
    S.city_block(v, -115, -50, ROME, cols=3, rows=2, lot=10, street=4, floors=(2, 3), roof="gable", seed=31)


def san_gimignano(v: Voxel) -> None:
    """Town of towers: competing families built 70 of them, 14 survive."""
    P = TUSCANY
    S.pad(v, -50, -50, 50, 50, "cobblestone")
    S.curtain_wall(v, -46, -46, 46, 46, 7, TUSCANY, gate="south", tower_r=3)
    heights = (40, 34, 30, 36, 28, 26, 32, 22, 24, 30, 20, 26, 34, 28)
    pos = ((0, -5), (6, 2), (-8, 4), (14, -12), (-16, -10), (20, 10), (-22, 12), (8, 18),
           (-6, 22), (26, -24), (-26, -26), (30, 24), (-30, 26), (2, -28))
    for (x, z), h in zip(pos, heights):
        S.tower(v, x, z, 2.5, h, TUSCANY, top="flat", square=True, wall="stone_bricks")
        S.house(v, x - 6, z + 3, 8, 7, TUSCANY, floors=2, roof="gable")
    S.plaza(v, -8, -2, 4, 10, TUSCANY, fountain=True)


WORLD = World(
    id="italy",
    name="Renaissance Italy",
    game="Assassin's Creed II (2009) / Brotherhood (2010)",
    era="1476-1507",
    description="Ezio's Italy: Florence, Monteriggioni, San Gimignano, Venice and Rome.",
).build(Build("florence", "Florence", "Santa Maria del Fiore with Brunelleschi's ribbed dome, Giotto's campanile, Palazzo Vecchio, Piazza della Signoria and the Ponte Vecchio.", florence, "1 block = 2 m")
).build(Build("monteriggioni", "Monteriggioni", "The hill town's ring wall with fourteen towers, the Villa Auditore and the square.", monteriggioni)
).build(Build("venice", "Venice", "St Mark's five domes, the campanile, the Doge's Palace, the Rialto bridge, canals and gondolas.", venice)
).build(Build("rome", "Rome", "The Colosseum, the Pantheon with its oculus, Castel Sant'Angelo on the Tiber, a Roman road and Forum ruins.", rome, "1 block = 2 m")
).build(Build("san_gimignano", "San Gimignano", "Fourteen family towers inside the town wall.", san_gimignano))
