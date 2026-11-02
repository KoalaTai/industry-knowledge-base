"""Viking-age England and Norway - Assassin's Creed Valhalla (2020), 873 CE."""

import math

from .. import structures as S
from ..palettes import ROME, SAXON, VIKING
from ..registry import Build, World
from ..voxel import Voxel

P = VIKING


def ravensthorpe(v: Voxel) -> None:
    """Eivor's settlement on the river: longhouse, barracks, forge, dock and a longship."""
    S.pad(v, -70, -50, 70, 60, "grass_block")
    v.fill(-70, -3, 30, 70, 0, 60, "water")
    S.longhouse(v, 0, -40, P, length=34, width=13)
    v.set(0, 1, -42, "gold_block")                                                 # the raven standard
    S.longhouse(v, -40, -30, P, length=22, width=9)
    S.longhouse(v, 36, -30, P, length=22, width=9)
    S.house(v, -50, 5, 10, 8, P, floors=1, roof="gable", wall="cobblestone")       # forge
    v.set(-45, 1, 8, "blast_furnace"); v.set(-47, 1, 8, "anvil"); v.set(-45, 7, 9, "campfire")
    S.house(v, 40, 5, 12, 8, P, floors=1, roof="gable")                             # trading post
    S.house(v, 20, 8, 8, 8, P, floors=1, roof="gable", wall="stripped_spruce_log")   # seer's hut
    for x in range(-60, 61, 2):                                                      # palisade
        v.column(x, 1, -48, 4, "spruce_fence")
    for z in range(-48, 26, 2):
        v.column(-60, 1, z, 4, "spruce_fence"); v.column(60, 1, z, 4, "spruce_fence")
    v.fill(-8, 0, 30, -4, 0, 46, "spruce_planks")                                    # dock
    S.ship(v, 0, 36, {"hull": "spruce_planks", "deck": "oak_planks"}, length=30, beam=7, style="longship")
    v.fill(-30, 1, 14, -10, 1, 24, "farmland[moisture=7]")
    for x in range(-30, -9, 2):
        v.set(x, 2, 16, "wheat[age=7]"); v.set(x, 2, 20, "wheat[age=7]")
    for i in range(8):
        v.tree(-66 + i * 19, 1, 56, "spruce_log", "spruce_leaves[persistent=true]", height=8, canopy=2)


def lunden(v: Voxel) -> None:
    """Lunden: Saxon timber houses among the crumbling Roman walls, the amphitheatre and the bridge."""
    S.pad(v, -80, -60, 80, 60, "grass_block")
    v.fill(-80, -3, 36, 80, 0, 60, "water")
    S.ruined_wall(v, -70, -50, 140, block="stone_bricks", seed=100)
    S.ruined_wall(v, -70, 30, 140, block="mossy_stone_bricks", seed=101)
    for k in range(6):                                                                # ruined amphitheatre
        v.disc(-35, 1 + k, -10, 26 - k * 2, "mossy_stone_bricks", hollow=True, rz=20 - k * 1.5)
    for a in range(0, 360, 50):                                                       # collapsed sections
        for rr in range(14, 26):
            for kk in range(1, 7):
                v.clear(round(-35 + rr * math.cos(math.radians(a))), kk, round(-10 + rr * 0.77 * math.sin(math.radians(a))))
    for i in range(6):
        S.house(v, -25 + i * 14, 5, 9, 8, SAXON, floors=1, roof="gable", wall="oak_planks")
    S.house(v, 30, -40, 20, 14, SAXON, floors=2, roof="gable", wall="cobblestone")   # St Paul's minster (Saxon)
    S.tower(v, 52, -36, 2.5, 16, SAXON, top="pyramid", square=True, wall="cobblestone")
    v.fill(-2, 1, 36, 2, 1, 60, "oak_planks")                                       # the wooden bridge
    for z in range(36, 61, 4):
        v.fill(-3, -3, z, -3, 0, z, "oak_log"); v.fill(3, -3, z, 3, 0, z, "oak_log")
    v.fill(-70, 1, -5, -30, 1, 25, "coarse_dirt")                                    # the Thames market strand


def jorvik(v: Voxel) -> None:
    """Jorvik (York): Viking trading town in a Saxon burh, the minster, Coppergate workshops, river wharves."""
    S.pad(v, -70, -60, 70, 60, "grass_block")
    v.fill(-70, -3, 40, 70, 0, 60, "water")
    # earthen rampart with palisade
    for k in range(4):
        v.walls(-60 + k, 1 + k, -52 + k, 60 - k, 1 + k, 36 - k, "coarse_dirt")
    for x in range(-57, 58, 2):
        v.column(x, 5, -49, 3, "oak_fence"); v.column(x, 5, 33, 3, "oak_fence")
    for z in range(-49, 34, 2):
        v.column(-57, 5, z, 3, "oak_fence"); v.column(57, 5, z, 3, "oak_fence")
    v.fill(-2, 1, 33, 2, 7, 36, "air")
    S.house(v, -20, -40, 36, 16, SAXON, floors=2, roof="gable", wall="cobblestone")    # the minster
    S.tower(v, -2, -44, 3, 20, SAXON, top="pyramid", square=True, wall="cobblestone")
    for i in range(5):                                                                 # Coppergate: narrow plots
        S.house(v, -45 + i * 12, -10, 7, 14, P, floors=1, roof="gable", wall="oak_planks", ridge="z")
        v.set(-42 + i * 12, 1, 6, ("loom", "smithing_table", "cartography_table", "fletching_table", "grindstone")[i])
    S.house(v, 20, -5, 16, 12, P, floors=1, roof="gable", wall="stripped_spruce_log")
    v.fill(-30, 0, 40, -24, 0, 52, "oak_planks"); v.fill(10, 0, 40, 16, 0, 52, "oak_planks")
    S.ship(v, -20, 46, {"hull": "spruce_planks", "deck": "oak_planks"}, length=24, beam=6, style="longship")


def stonehenge(v: Voxel) -> None:
    """The sarsen circle and trilithon horseshoe on Salisbury Plain (a Valhalla standing-stone site)."""
    S.pad(v, -40, -40, 40, 40, "grass_block")
    S.stonehenge(v, 0, 0)
    v.fill(-1, 1, 24, 1, 1, 40, "dirt_path")                                          # the avenue
    v.column(0, 1, 36, 5, "stone")                                                     # heel stone


def asgard(v: Voxel) -> None:
    """Eivor's vision of Asgard: the golden hall Valhalla on its rock, Bifrost, Yggdrasil."""
    S.pad(v, -80, -80, 80, 80, "grass_block")
    for k in range(20):
        v.disc(0, 1 + k, 0, 40 - k * 1.5, "stone" if k % 4 else "gold_block", rz=30 - k)
    hall = Voxel()
    S.longhouse(hall, 0, -18, {"wall2": "gold_block", "floor": "polished_andesite", "roof": "yellow_terracotta"}, length=36, width=15)
    hall.walls(-7, 1, -18, 7, 4, 18, "gold_block")
    v.merge(hall, 0, 20, 0)
    # Bifrost: a rainbow arc from the plain to the rock
    cols = ("red_wool", "orange_wool", "yellow_wool", "lime_wool", "light_blue_wool", "purple_wool")
    for i, c in enumerate(cols):
        for t in range(0, 61):
            x = -78 + t
            y = int(1 + 24 * math.sin(math.pi * t / 60))
            v.set(x, y, 20 + i, c)
    # Yggdrasil
    v.cylinder(45, 1, -45, 5, 40, "oak_log")
    v.sphere(45, 44, -45, 18, "oak_leaves[persistent=true]", hollow=True)
    v.sphere(45, 44, -45, 10, "oak_leaves[persistent=true]", hollow=True)
    for a in range(0, 360, 45):
        v.line((45, 30, -45), (round(45 + 20 * math.cos(math.radians(a))), 44, round(-45 + 20 * math.sin(math.radians(a)))), "oak_log")
    v.disc(-40, 0, -40, 10, "water")                                                   # the well of Urd


def norway(v: Voxel) -> None:
    """A fjord in Rygjafylke: steep snowy slopes, a stave-style hall, a waterfall and a longship."""
    S.pad(v, -80, -60, 80, 60, "water")
    v.fill(-80, -3, -60, 80, -1, 60, "water")
    for side in (-1, 1):
        for k in range(30):
            z1 = side * (20 + k) if side > 0 else side * (60)
            z2 = side * 60 if side > 0 else side * (20 + k)
            v.fill(-80, 0 + k, min(z1, z2), 80, 0 + k, max(z1, z2), "snow_block" if k > 14 else "stone")
    v.fill(-80, 0, -20, 80, 0, 20, "water")
    v.fill(-80, 0, -24, 80, 0, -20, "gravel")
    S.longhouse(v, -40, -45, P, length=20, width=9)
    S.house(v, 10, -44, 10, 10, {**P, "roof": "dark_oak_planks"}, floors=2, roof="gable", wall="spruce_planks")   # stave-style
    v.pyramid(15, 10, -39, 7, 5, "dark_oak_planks")
    v.set(15, 15, -39, "gold_block")
    v.fill(60, 1, 20, 64, 30, 24, "water")                                              # waterfall
    v.fill(58, 31, 20, 66, 31, 30, "water")
    S.ship(v, -20, -4, {"hull": "spruce_planks", "deck": "oak_planks"}, length=30, beam=7, style="longship")
    for x in range(-75, 80, 9):
        v.tree(x, 2, -28, "spruce_log", "spruce_leaves[persistent=true]", height=9, canopy=2)
        v.tree(x + 4, 6, 32, "spruce_log", "spruce_leaves[persistent=true]", height=8, canopy=2)


WORLD = World(
    id="viking",
    name="Viking England and Norway",
    game="Assassin's Creed Valhalla (2020)",
    era="873 CE, the Great Heathen Army",
    description="Eivor's world: Ravensthorpe, Lunden, Jorvik, standing stones, the fjords of Norway and Asgard.",
).build(Build("ravensthorpe", "Ravensthorpe", "The riverside settlement: longhouse, barracks, forge, seer's hut, dock and longship inside a palisade.", ravensthorpe)
).build(Build("lunden", "Lunden", "Saxon houses among ruined Roman walls and amphitheatre, a wooden bridge and the market strand.", lunden)
).build(Build("jorvik", "Jorvik", "Viking York: earth-and-timber rampart, the minster, Coppergate craft plots and wharves.", jorvik)
).build(Build("stonehenge", "Stonehenge", "Sarsen circle, trilithon horseshoe, avenue and heel stone.", stonehenge)
).build(Build("asgard", "Asgard", "The golden hall on its rock, the Bifrost rainbow bridge, Yggdrasil and the well of Urd.", asgard)
).build(Build("norway", "Rygjafylke Fjord", "A snowy fjord with a hall, a stave-style chapel, a waterfall and a longship.", norway))
