"""Holy Roman Empire, 16th century - Assassin's Creed Hexe (announced; setting as described by Ubisoft).

Hexe has not shipped, so this is a period-accurate placeholder: a
half-timbered Free Imperial town during the witch trials, with a
Burg above it.  Swap in real locations once the game is out.
"""

from .. import structures as S
from ..palettes import GERMAN
from ..registry import Build, World
from ..voxel import Voxel

P = GERMAN


def free_town(v: Voxel) -> None:
    """A walled Fachwerk town: market square with Rathaus and well, church spire, gallows field outside the gate."""
    S.pad(v, -70, -60, 70, 70, "grass_block")
    S.curtain_wall(v, -58, -50, 58, 40, 7, {**P, "wall": "cobblestone"}, gate="south", tower_r=3)
    for (x, z) in ((-54, -46), (6, -46), (-54, 4), (14, 4)):
        bx, bz = x, z
        for i in range(3):
            for j in range(2):
                S.timber_house(v, bx + i * 13, bz + j * 13, 9, 9, P, floors=2 + (i + j) % 2)
    S.plaza(v, -22, -20, 10, 0, P, fountain=True)
    S.timber_house(v, -20, -42, 28, 14, P, floors=3)                                    # Rathaus
    v.fill(-18, 14, -42, -14, 18, -40, "red_terracotta"); v.cone(-16, 19, -41, 2, 5, "red_terracotta")
    S.house(v, 20, -44, 16, 30, P, floors=2, roof="gable", wall="cobblestone", ridge="z")      # church
    S.tower(v, 28, -48, 3, 24, P, top="cone", square=True, wall="cobblestone")
    # outside the gate: the pyre and gallows field of the witch trials
    v.fill(-6, 1, 50, 6, 2, 62, "oak_log")
    v.column(0, 3, 56, 6, "stripped_oak_log")
    v.fill(-4, 2, 52, 4, 2, 60, "hay_block")
    v.column(20, 1, 56, 7, "stripped_oak_log"); v.fill(20, 8, 56, 26, 8, 56, "stripped_oak_log")
    v.fill(26, 5, 56, 26, 7, 56, "chain")
    for i in range(6):
        v.tree(-60 + i * 24, 1, 66, "dark_oak_log", "dark_oak_leaves[persistent=true]", height=7, canopy=3)


def burg(v: Voxel) -> None:
    """A hilltop Burg: bergfried keep, curtain wall, chapel, and the Black Forest below."""
    S.pad(v, -60, -60, 60, 60, "grass_block")
    for k in range(14):
        v.disc(0, 1 + k, 0, 34 - k * 1.6, "stone" if k % 3 else "coarse_dirt", rz=26 - k)
    castle = Voxel()
    S.curtain_wall(castle, -16, -12, 16, 12, 6, {**P, "wall": "cobblestone"}, gate="south", tower_r=2.5)
    S.tower(castle, 0, -4, 4, 24, P, top="cone", wall="stone_bricks")                   # bergfried
    S.timber_house(castle, -13, -9, 9, 7, P, floors=2)
    S.house(castle, 5, -9, 9, 7, P, floors=1, roof="gable", wall="cobblestone")          # chapel
    v.merge(castle, 0, 14, 0)
    for k in range(15):
        v.fill(-2, 1 + k, 30 - k * 1.3, 2, 1 + k, 31 - k * 1.3, "cobblestone")
    import random
    rng = random.Random(120)
    for _ in range(50):
        x, z = rng.randint(-58, 58), rng.randint(-58, 58)
        if abs(x) < 36 and abs(z) < 30:
            continue
        v.tree(x, 1, z, "spruce_log", "spruce_leaves[persistent=true]", height=rng.randint(7, 11), canopy=2)


WORLD = World(
    id="hexe",
    name="Holy Roman Empire (Hexe)",
    game="Assassin's Creed Hexe (announced, unreleased)",
    era="16th century, the witch trials",
    description="Placeholder for the announced Hexe setting: a Fachwerk town and a hilltop Burg in the Empire.",
).build(Build("free_town", "Free Imperial Town", "Walled half-timbered town with Rathaus, market well, church spire, and the pyre field outside the gate.", free_town)
).build(Build("burg", "Hilltop Burg", "Bergfried keep and curtain wall on a crag above the Black Forest.", burg))
