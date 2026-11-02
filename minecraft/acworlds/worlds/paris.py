"""Revolutionary Paris - Assassin's Creed Unity (2014), 1789-1794."""

from .. import structures as S
from ..palettes import PARIS
from ..registry import Build, World
from ..voxel import Voxel

P = PARIS


def notre_dame(v: Voxel) -> None:
    """Notre-Dame de Paris on the Ile de la Cite, with the Seine on both sides."""
    S.pad(v, -60, -40, 60, 110, "stone")
    v.fill(-60, -3, -40, -40, 0, 110, "water")
    v.fill(40, -3, -40, 60, 0, 110, "water")
    S.gothic_church(v, 0, 0, P, length=70, width=23, towers=True, nave_h=26, tower_h=48)
    S.plaza(v, -30, -36, 30, -4, P, fountain=False)
    S.arched_bridge(v, -40, 30, 20, 9, P, arches=3, axis="x", deck_y=3)
    S.arched_bridge(v, 40, 30, 20, 9, P, arches=3, axis="x", deck_y=3)
    S.city_block(v, -36, 80, P, cols=5, rows=1, lot=9, street=3, floors=(3, 4), roof="hip", seed=70)


def bastille(v: Voxel) -> None:
    """The eight-towered fortress-prison stormed on 14 July 1789, with the faubourg around it."""
    S.pad(v, -60, -60, 60, 60, "cobblestone")
    v.fill(-30, -3, -24, 30, 0, 24, "water")
    v.fill(-26, 0, -20, 26, 0, 20, "stone")
    v.fill(-26, 1, -20, 26, 14, 20, "stone_bricks")
    v.fill(-23, 1, -17, 23, 14, 17, "air")
    v.fill(-23, 1, -17, 23, 1, 17, "cobblestone")
    for x in (-26, -9, 9, 26):
        for z in (-20, 20):
            S.tower(v, x, z, 4.5, 18, P, top="crenel", wall="stone_bricks")
    v.crenellate(-26, 15, -20, 26, 20, "stone_bricks")
    v.fill(-1, 1, 17, 1, 4, 20, "air")
    v.fill(-2, 0, 20, 2, 0, 26, "oak_planks")                                     # drawbridge
    for y in range(3, 13, 4):
        v.windows(-26, y, -20, 26, 20, "iron_bars", period=4, offset=2)
    S.house(v, -20, -10, 12, 8, P, floors=2, roof="hip", wall="stone_bricks")        # governor's lodging
    S.city_block(v, -58, 30, P, cols=4, rows=1, lot=9, street=3, floors=(3, 4), roof="hip", seed=71)
    S.city_block(v, 10, 30, P, cols=4, rows=1, lot=9, street=3, floors=(3, 4), roof="hip", seed=72)
    S.catapult(v, 45, -40)
    v.fill(-50, 1, -45, -48, 1, -43, "iron_block")                                  # a cannon
    v.fill(-50, 2, -44, -44, 2, -44, "polished_blackstone")


def versailles(v: Voxel) -> None:
    """Louis XIV's palace: the garden front, the Hall of Mirrors, the parterres and the Grand Canal."""
    S.pad(v, -120, -40, 120, 160, "grass_block")
    # the long garden front with projecting central block
    v.fill(-100, 1, -30, 100, 14, -10, P["wall"])
    v.fill(-99, 1, -29, 99, 13, -11, "air")
    v.fill(-99, 1, -29, 99, 1, -11, P["floor"])
    v.fill(-30, 1, -10, 30, 14, -4, P["wall"])
    v.fill(-29, 1, -9, 29, 13, -5, "air")
    for y in (3, 4, 8, 9):
        v.windows(-100, y, -30, 100, -10, P["window"], period=3, offset=2)
        v.windows(-30, y, -10, 30, -4, P["window"], period=3, offset=2)
    v.fill(-100, 15, -30, 100, 15, -10, "smooth_quartz")
    v.fill(-30, 15, -10, 30, 15, -4, "smooth_quartz")
    v.crenellate(-100, 16, -30, 100, -10, "gold_block", period=6)
    # Hall of Mirrors on the first floor of the central block
    v.fill(-28, 7, -9, 28, 7, -5, "polished_diorite")
    for x in range(-27, 28, 3):
        v.fill(x, 8, -9, x, 12, -9, "glass")
        v.set(x, 12, -7, "lantern")
    for x in range(-100, 101, 10):
        v.column(x, 2, -10, 12, "quartz_pillar")
    # parterres, fountain of Latona, the Tapis Vert and the Grand Canal
    S.plaza(v, -40, -2, 40, 30, P, fountain=False)
    for k in range(5):
        v.disc(0, 1 + k, 16, 8 - k * 1.5, "white_concrete", hollow=True)
    v.disc(0, 1, 16, 7, "water"); v.set(0, 6, 16, "gold_block")
    v.fill(-14, 0, 32, 14, 0, 90, "grass_block")
    for z in range(34, 90, 8):
        v.tree(-16, 1, z, "dark_oak_log", "dark_oak_leaves[persistent=true]", height=7, canopy=2)
        v.tree(16, 1, z, "dark_oak_log", "dark_oak_leaves[persistent=true]", height=7, canopy=2)
    v.fill(-6, -2, 94, 6, 0, 160, "water")                                          # Grand Canal
    v.fill(-60, -2, 110, 60, 0, 122, "water")
    for x in range(-100, 101, 25):
        for z in (0, 30):
            if abs(x) > 45:
                v.fill(x - 8, 0, z, x + 8, 0, z + 20, "moss_block")
                v.walls(x - 8, 1, z, x + 8, 1, z + 20, "oak_leaves[persistent=true]")


def paris_streets(v: Voxel) -> None:
    """A revolutionary quarter: tall limestone houses, a barricade, the guillotine on the square, a hot-air balloon."""
    S.pad(v, -60, -60, 60, 60, "cobblestone")
    S.city_block(v, -58, -58, P, cols=3, rows=3, lot=10, street=4, floors=(4, 5), roof="hip", seed=73)
    S.city_block(v, 14, -58, P, cols=3, rows=3, lot=10, street=4, floors=(4, 5), roof="hip", seed=74)
    S.plaza(v, -20, 0, 20, 30, P, fountain=False)
    # guillotine
    v.fill(-2, 1, 12, 2, 1, 16, "oak_planks")
    v.column(-1, 2, 14, 10, "stripped_oak_log"); v.column(1, 2, 14, 10, "stripped_oak_log")
    v.fill(-1, 12, 14, 1, 12, 14, "stripped_oak_log")
    v.set(0, 10, 14, "iron_block")
    # barricade across the street
    for x in range(-18, 19):
        v.set(x, 1, 40, ("barrel", "oak_planks", "cobblestone", "hay_block")[abs(x) % 4])
        if x % 3 == 0:
            v.set(x, 2, 40, "oak_fence")
    v.set(0, 3, 40, "blue_wool"); v.set(0, 4, 40, "white_wool"); v.set(0, 5, 40, "red_wool")
    # Montgolfier balloon tethered above the square
    v.sphere(0, 40, 15, 9, "light_blue_wool", hollow=True)
    for y in range(32, 49, 4):
        v.disc(0, y, 15, 9, "gold_block", hollow=True)
    v.fill(-2, 27, 13, 2, 28, 17, "oak_planks")
    v.fill(-1, 28, 14, 1, 28, 16, "air")
    v.fill(0, 29, 15, 0, 31, 15, "chain")
    v.fill(0, 2, 15, 0, 26, 15, "chain")


WORLD = World(
    id="paris",
    name="Revolutionary Paris",
    game="Assassin's Creed Unity (2014)",
    era="1789-1794",
    description="Arno's Paris: Notre-Dame, the Bastille, Versailles and the streets of the Revolution.",
).build(Build("notre_dame", "Notre-Dame", "The cathedral with flying buttresses, rose window and spire on the Ile de la Cite, with bridges over the Seine.", notre_dame)
).build(Build("bastille", "The Bastille", "The eight-towered fortress prison in its moat, with the faubourg Saint-Antoine around it.", bastille)
).build(Build("versailles", "Versailles", "The garden front, the Hall of Mirrors, the Latona fountain, the Tapis Vert and the Grand Canal.", versailles)
).build(Build("paris_streets", "Streets of the Revolution", "Tall houses, a barricade, the guillotine and a tethered Montgolfier balloon.", paris_streets))
