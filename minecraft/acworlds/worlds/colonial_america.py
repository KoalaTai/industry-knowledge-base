"""Colonial America - Assassin's Creed III (2012) and Rogue (2014), 1752-1783."""

from .. import structures as S
from ..palettes import COLONIAL, VIKING
from ..registry import Build, World
from ..voxel import Voxel

P = COLONIAL
SHIP = {"hull": "dark_oak_planks", "deck": "oak_planks"}


def boston(v: Voxel) -> None:
    """Old North Church and its steeple, brick row houses, Long Wharf and the harbour."""
    S.pad(v, -70, -60, 70, 60, "grass_block")
    v.fill(-70, -3, 30, 70, 0, 60, "water")
    v.fill(-70, 0, 28, 70, 0, 29, "cobblestone")
    v.fill(-5, 0, 30, 5, 0, 60, "oak_planks")                             # Long Wharf
    # Old North Church (1723): brick box with a tall white steeple
    cx, cz = -30, -20
    v.fill(cx - 8, 1, cz - 14, cx + 8, 12, cz + 14, "bricks")
    v.fill(cx - 7, 1, cz - 13, cx + 7, 11, cz + 13, "air")
    v.fill(cx - 7, 1, cz - 13, cx + 7, 1, cz + 13, "oak_planks")
    for z in range(cz - 10, cz + 12, 5):
        v.fill(cx - 8, 4, z, cx - 8, 9, z, "glass_pane")
        v.fill(cx + 8, 4, z, cx + 8, 9, z, "glass_pane")
    v.gable_roof(cx - 8, 13, cz - 14, cx + 8, cz + 14, "deepslate_tiles", ridge_axis="z")
    S.tower(v, cx, cz - 18, 3, 24, P, top="flat", square=True, wall="bricks")
    v.fill(cx - 2, 25, cz - 20, cx + 2, 32, cz - 16, "white_concrete")
    v.fill(cx - 1, 26, cz - 19, cx + 1, 31, cz - 17, "air")
    v.windows(cx - 2, 28, cz - 20, cx + 2, cz - 16, "air", period=2, offset=2)
    v.cone(cx, 33, cz - 18, 3, 14, "white_concrete")
    v.set(cx, 47, cz - 18, "gold_block")
    v.set(cx - 1, 30, cz - 21, "lantern"); v.set(cx + 1, 30, cz - 21, "lantern")   # two if by sea
    # Faneuil Hall-style market and brick streets
    S.house(v, 10, -30, 24, 12, P, floors=2, roof="hip", wall="bricks")
    v.cylinder(22, 13, -24, 2, 5, "white_concrete", hollow=True)
    v.cone(22, 18, -24, 2.5, 4, "white_concrete")
    S.city_block(v, -68, 0, P, cols=4, rows=2, lot=9, street=3, floors=(2, 3), roof="gable", seed=50)
    S.city_block(v, 10, 0, P, cols=4, rows=2, lot=9, street=3, floors=(2, 3), roof="gable", seed=51)
    S.ship(v, 15, 40, SHIP, length=36, beam=9, masts=3)


def new_york(v: Voxel) -> None:
    """1776 New York: Fort George at the Battery, Dutch step-gabled houses, Trinity's spire."""
    S.pad(v, -60, -50, 60, 60, "grass_block")
    v.fill(-60, -3, 40, 60, 0, 60, "water")
    S.fort_bastion(v, 0, 10, COLONIAL, half=22, h=7)
    for i in range(5):                                                     # Dutch step gables
        x = -55 + i * 11
        top = S.house(v, x, -40, 8, 10, P, floors=3, roof="gable", wall="bricks" if i % 2 else "white_concrete", ridge="z")
        for k in range(4):
            v.fill(x + k, 13 + k, -40, x + 7 - k, 13 + k, -40, "bricks")
    S.house(v, 20, -45, 14, 24, P, floors=2, roof="gable", wall="white_concrete", ridge="z")   # Trinity church
    S.tower(v, 27, -48, 2.5, 20, P, top="flat", square=True, wall="white_concrete")
    v.cone(27, 21, -48, 3, 10, "white_concrete")
    S.city_block(v, 0, -10, P, cols=3, rows=1, lot=9, street=3, floors=(2, 3), roof="gable", seed=52)
    S.road(v, -58, -14, 58, -11, "cobblestone")                            # Broadway
    S.ship(v, -40, 44, SHIP, length=32, beam=8, masts=2)


def frontier(v: Voxel) -> None:
    """The Davenport Homestead manor, a Kanien'keha:ka longhouse village, forest and a sawmill."""
    S.pad(v, -80, -60, 80, 60, "grass_block")
    v.fill(-80, -3, -8, 80, 0, 8, "water")                                 # the river
    S.house(v, 20, 20, 20, 14, P, floors=2, roof="gable", wall="white_concrete")   # the manor
    v.fill(18, 1, 34, 40, 1, 36, "oak_planks")                             # porch
    for x in range(18, 41, 4):
        v.column(x, 2, 36, 4, "white_concrete")
    v.fill(17, 6, 34, 41, 6, 37, "dark_oak_planks")
    # Kanatahseton: bark longhouses inside a palisade
    for i in range(3):
        S.longhouse(v, -50 + i * 16, 20, {"wall2": "stripped_oak_log", "floor": "dirt_path", "roof": "oak_planks"}, length=24, width=7)
    for x in range(-62, -8, 2):
        v.column(x, 1, 16, 4, "oak_fence")
        v.column(x, 1, 50, 4, "oak_fence")
    for z in range(16, 51, 2):
        v.column(-62, 1, z, 4, "oak_fence")
        v.column(-8, 1, z, 4, "oak_fence")
    v.fill(-36, 1, 16, -34, 4, 16, "air")
    # water-powered sawmill on the river
    v.fill(50, 1, -14, 62, 5, -9, "spruce_planks")
    v.fill(51, 1, -13, 61, 4, -10, "air")
    v.gable_roof(50, 6, -14, 62, -9, "dark_oak_planks", ridge_axis="x")
    # undershot waterwheel in the stream: a ring of paddles on an axle
    import math
    for a in range(0, 360, 20):
        v.set(56 + round(3.5 * math.cos(math.radians(a))), 1 + round(3.5 * math.sin(math.radians(a))), -8, "stripped_spruce_log")
    v.fill(56, 1, -9, 56, 1, -7, "iron_block")
    # forest and the bear's cave
    import random
    rng = random.Random(53)
    for _ in range(60):
        x, z = rng.randint(-78, 78), rng.choice((rng.randint(-58, -12), rng.randint(12, 58)))
        if (x, z) in {(c[0], c[2]) for c in v.blocks if c[1] == 2}:
            continue
        if -64 < x < -6 and 14 < z < 52:
            continue
        if 16 < x < 44 and 18 < z < 38:
            continue
        v.tree(x, 1, z, "spruce_log", "spruce_leaves[persistent=true]", height=rng.randint(6, 10), canopy=2)
    v.fill(-70, 1, -56, -60, 5, -48, "stone")
    v.fill(-69, 1, -55, -61, 4, -50, "air")


def north_atlantic(v: Voxel) -> None:
    """Shay's Morrigan among icebergs, and a Hudson Valley fort (Rogue)."""
    S.pad(v, -80, -60, 80, 60, "water")
    v.fill(-80, -3, -60, 80, -1, 60, "water")
    for (ix, iz, r) in ((-50, -30, 12), (40, 30, 16), (-20, 40, 8), (60, -40, 10)):
        v.sphere(ix, -2, iz, r, "packed_ice", hollow=False, y_min=-4)
        v.cone(ix, r - 3, iz, r * 0.6, r // 2, "blue_ice")
    S.ship(v, -20, -8, {"hull": "dark_oak_planks", "deck": "spruce_planks"}, length=36, beam=9, masts=2)
    v.fill(30, 0, -60, 80, 0, -10, "grass_block")
    v.fill(30, 0, -60, 80, 0, -10, "snow_block")
    S.fort_bastion(v, 55, -35, COLONIAL, half=18, h=6)
    for i in range(8):
        v.tree(34 + i * 6, 1, -14, "spruce_log", "spruce_leaves[persistent=true]", height=8, canopy=2)


WORLD = World(
    id="colonial_america",
    name="Colonial America",
    game="Assassin's Creed III (2012) / Rogue (2014)",
    era="1752-1783, the Seven Years' War and the Revolution",
    description="Connor's and Shay's America: Boston, New York, the Frontier and the North Atlantic.",
).build(Build("boston", "Boston", "Old North Church with its lantern steeple, Long Wharf, brick streets and a ship at anchor.", boston)
).build(Build("new_york", "New York", "Fort George at the Battery, Dutch step-gabled houses, Trinity Church and Broadway.", new_york)
).build(Build("frontier", "The Frontier", "Davenport Homestead manor, a palisaded Kanien'keha:ka longhouse village, a water-powered sawmill and forest.", frontier)
).build(Build("north_atlantic", "North Atlantic", "The Morrigan among icebergs with a Hudson Valley fort on the shore (Rogue).", north_atlantic))
