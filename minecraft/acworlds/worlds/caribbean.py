"""The Caribbean - Assassin's Creed IV Black Flag (2013), Freedom Cry (2013) and Liberation (2012)."""

from .. import structures as S
from ..palettes import CARIBBEAN, COLONIAL
from ..registry import Build, World
from ..voxel import Voxel

P = CARIBBEAN
BRIG = {"hull": "dark_oak_planks", "deck": "oak_planks"}


def havana(v: Voxel) -> None:
    """Castillo del Morro guarding the harbour mouth, the cathedral plaza and Spanish streets."""
    S.pad(v, -80, -60, 80, 70, "sand")
    v.fill(-80, -3, 30, 80, 0, 70, "water")
    v.fill(-80, 0, 28, 80, 0, 29, "smooth_sandstone")
    S.fort_bastion(v, -50, 0, CARIBBEAN, half=22, h=9)
    S.tower(v, -50, -24, 3, 22, P, top="cone", wall="white_terracotta")             # the lighthouse
    S.basilica(v, 30, -55, CARIBBEAN, length=36, width=21, h=14)
    for tx in (18, 42):
        S.tower(v, tx, -52, 2.5, 22, P, top="dome", square=True, wall="smooth_sandstone")
    S.plaza(v, 10, -16, 50, 10, CARIBBEAN, fountain=True)
    S.city_block(v, 55, -50, P, cols=2, rows=4, lot=9, street=3, floors=(2, 3), roof="flat", seed=60)
    S.city_block(v, -20, -50, P, cols=3, rows=2, lot=9, street=3, floors=(2, 3), roof="flat", seed=61)
    for x in range(-75, 80, 12):
        v.palm(x, 1, 24, height=8)
    S.ship(v, 20, 40, BRIG, length=40, beam=9, masts=3)                                 # Spanish galleon


def nassau(v: Voxel) -> None:
    """The pirate republic: a tumbledown fort, shacks on the beach, the tavern, the Jackdaw."""
    S.pad(v, -70, -60, 70, 60, "sand")
    v.fill(-70, -3, 20, 70, 0, 60, "water")
    v.fill(-70, -2, 18, 70, -2, 24, "sand")
    for k in range(5):
        v.disc(-40, 1 + k, -30, 26 - k * 3, "grass_block", rz=18 - k * 2)
    S.curtain_wall(v, -52, -40, -28, -22, 5, {**CARIBBEAN, "wall": "cobblestone"}, gate="south", tower_r=2.5)
    v.merge(Voxel(), 0, 0, 0)
    S.ruined_wall(v, -52, -42, 24, block="cobblestone", seed=62)
    # beach shacks and the Old Avery tavern
    import random
    rng = random.Random(63)
    for i in range(9):
        x = -60 + i * 14
        S.house(v, x, rng.randint(-8, 6), rng.randint(5, 7), rng.randint(5, 7), P, floors=1,
                roof="gable", wall=rng.choice(("oak_planks", "spruce_planks", "jungle_planks")))
    S.house(v, 10, -40, 18, 12, P, floors=2, roof="hip", wall="spruce_planks")
    v.fill(8, 1, -28, 30, 1, -26, "oak_planks")
    for x in range(8, 31, 4):
        v.column(x, 2, -26, 4, "stripped_jungle_log")
    v.fill(7, 6, -29, 31, 6, -25, "jungle_leaves[persistent=true]")
    for x in range(-65, 70, 9):
        v.palm(x, 1, 14, height=6 + x % 3)
    v.fill(-10, 0, 20, -6, 0, 44, "oak_planks")                                        # jetty
    S.ship(v, -20, 36, BRIG, length=34, beam=8, masts=2)                                # the Jackdaw (brig)
    v.set(-3, 24, 40, "black_wool"); v.set(-3, 23, 40, "white_wool")                   # the black flag


def kingston(v: Voxel) -> None:
    """Jamaica: a sugar plantation with windmill, boiling house, great house and the enslaved workers' quarters."""
    S.pad(v, -70, -60, 70, 60, "grass_block")
    for z in range(-55, -20, 7):
        v.fill(-65, 1, z, 20, 1, z + 3, "sugar_cane")
        v.fill(-65, 2, z, 20, 2, z + 3, "sugar_cane")
        v.fill(-65, 0, z + 4, 20, 0, z + 5, "water")
    S.windmill(v, 40, -40, CARIBBEAN, style="tower")
    S.house(v, 30, -20, 22, 12, P, floors=1, roof="gable", wall="cobblestone")          # boiling house
    for x in range(34, 50, 6):
        v.column(x, 6, -10, 6, "bricks")
    S.house(v, -20, 10, 26, 16, COLONIAL, floors=2, roof="hip", wall="white_concrete")   # great house
    v.fill(-22, 1, 26, 8, 1, 28, "oak_planks")
    for x in range(-22, 9, 4):
        v.column(x, 2, 28, 4, "white_concrete")
    v.fill(-23, 6, 25, 9, 6, 29, "dark_oak_planks")
    for i in range(6):
        S.house(v, 20 + i * 8, 30, 5, 5, P, floors=1, roof="gable", wall="oak_planks")
    S.road(v, -60, 40, 65, 44, "dirt_path")
    for x in range(-60, 70, 15):
        v.palm(x, 1, 48, height=7)


def port_au_prince(v: Voxel) -> None:
    """Saint-Domingue, 1735: the French fort and harbour where Adewale fought the slavers (Freedom Cry)."""
    S.pad(v, -60, -50, 60, 60, "sand")
    v.fill(-60, -3, 30, 60, 0, 60, "water")
    S.fort_bastion(v, 0, -10, CARIBBEAN, half=20, h=8)
    v.fill(-40, 0, 30, -34, 0, 56, "oak_planks")
    S.city_block(v, 25, -45, P, cols=2, rows=3, lot=9, street=3, floors=(1, 2), roof="gable", seed=64)
    S.city_block(v, -58, -45, P, cols=2, rows=3, lot=9, street=3, floors=(1, 2), roof="gable", seed=65)
    S.ship(v, -30, 40, BRIG, length=30, beam=8, masts=2)
    for x in range(-55, 60, 10):
        v.palm(x, 1, 26, height=7)


def new_orleans(v: Voxel) -> None:
    """Aveline's New Orleans (Liberation): the French Quarter with iron galleries, St Louis church, and the bayou."""
    S.pad(v, -80, -60, 80, 60, "grass_block")
    v.fill(-80, -3, 30, 80, 0, 60, "water")
    v.fill(-80, 0, 28, 80, 0, 29, "cobblestone")
    S.basilica(v, 0, -55, {**COLONIAL, "wall": "white_concrete", "roof": "deepslate_tiles"}, length=30, width=19, h=12)
    for tx in (-12, 12):
        S.tower(v, tx, -52, 2.5, 18, COLONIAL, top="cone", square=True, wall="white_concrete")
    S.plaza(v, -16, -24, 16, 0, COLONIAL, fountain=False)
    for (x, z) in ((-70, -50), (25, -50), (-70, -20), (25, -20)):
        x2, z2 = S.city_block(v, x, z, {**COLONIAL, "wall": "white_terracotta", "wall2": "yellow_terracotta"},
                              cols=3, rows=2, lot=9, street=4, floors=(2, 2), roof="hip", seed=x + z)
        for hx in range(x + 4, x2 - 4, 13):                                             # iron-lace galleries
            v.fill(hx, 5, z + 2, hx + 8, 5, z + 2, "iron_bars")
            v.fill(hx, 4, z + 2, hx + 8, 4, z + 2, "oak_slab")
    # bayou: cypress on stilts in shallow water
    v.fill(-80, 0, 5, 80, 0, 26, "water")
    for i in range(14):
        x = -75 + i * 11
        v.column(x, 1, 10 + (i * 5) % 14, 9, "stripped_mangrove_log")
        v.sphere(x, 11, 10 + (i * 5) % 14, 3, "mangrove_leaves[persistent=true]", hollow=False)
        v.set(x, 4, 11 + (i * 5) % 14, "vine")
    v.fill(-10, 0, 20, -6, 0, 40, "oak_planks")
    v.fill(0, 0, 32, 10, 0, 35, "oak_planks")                                           # flatboat


WORLD = World(
    id="caribbean",
    name="The Caribbean",
    game="Assassin's Creed IV Black Flag (2013) / Freedom Cry / Liberation",
    era="1715-1777, the Golden Age of Piracy to the eve of revolution",
    description="Edward Kenway's, Adewale's and Aveline's Caribbean: Havana, Nassau, Kingston, Port-au-Prince and New Orleans.",
).build(Build("havana", "Havana", "Castillo del Morro with lighthouse, the cathedral plaza, Spanish streets and a galleon.", havana)
).build(Build("nassau", "Nassau", "The pirate republic's beach shacks, ruined fort, tavern and the Jackdaw at the jetty.", nassau)
).build(Build("kingston", "Kingston", "A Jamaican sugar plantation: cane fields, windmill, boiling house, great house and quarters.", kingston)
).build(Build("port_au_prince", "Port-au-Prince", "The French fort and harbour of Saint-Domingue (Freedom Cry).", port_au_prince)
).build(Build("new_orleans", "New Orleans", "French Quarter galleries, St Louis church, and the cypress bayou (Liberation).", new_orleans))
