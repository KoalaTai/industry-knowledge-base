"""Classical Greece - Assassin's Creed Odyssey (2018), 431-422 BCE."""

import math

from .. import structures as S
from ..palettes import GREECE
from ..registry import Build, World
from ..voxel import Voxel

P = GREECE


def athens(v: Voxel) -> None:
    """The Acropolis: Parthenon, Propylaia, Erechtheion and the bronze Athena Promachos, with the agora below."""
    S.pad(v, -90, -80, 90, 80, "grass_block")
    rock = Voxel()
    for k in range(14):
        rock.disc(0, 1 + k, 0, 60 - k * 1.5, "stone" if k % 3 else "andesite", rz=40 - k)
    v.merge(rock)
    top = 15
    acro = Voxel()
    acro.disc(0, 0, 0, 40, "cobblestone", rz=26)
    S.greek_temple(acro, 10, 0, P, cols_long=17, cols_short=8, spacing=3, col_h=11, axis="x")   # Parthenon 8x17
    S.greek_temple(acro, -14, -16, P, cols_long=6, cols_short=4, spacing=3, col_h=8, axis="x")   # Erechtheion (simplified)
    for i in range(6):                                                                       # caryatid porch
        acro.column(-16 + i * 2, 4, -8, 6, "white_concrete")
    S.greek_temple(acro, -34, 0, P, cols_long=6, cols_short=3, spacing=3, col_h=9, axis="z")    # Propylaia
    S.statue(acro, -24, 8, 14, "copper_block")                                                  # Athena Promachos
    v.merge(acro, 0, top, 0)
    # the great ramp up to the Propylaia
    for k in range(16):
        v.fill(-70 + k, 1 + k, -3, -69 + k, 1 + k, 3, "smooth_quartz")
    # theatre of Dionysus on the south slope
    for i in range(12):
        v.disc(0, 1 + i, 50, 30 - i * 2, "smooth_stone", hollow=True, rz=22 - i * 1.5)
    v.disc(0, 1, 50, 7, "polished_andesite")                                                  # orchestra
    v.fill(-8, 1, 58, 8, 1, 58, "smooth_quartz")
    # agora with stoa
    v.fill(-85, 1, -70, -45, 1, -40, P["floor"])
    for x in range(-85, -44, 4):
        v.column(x, 2, -70, 7, "quartz_pillar")
    v.fill(-86, 9, -74, -44, 9, -69, "terracotta")
    S.city_block(v, 45, -75, P, cols=3, rows=2, lot=8, street=3, floors=(1, 2), roof="flat", seed=90)
    for i in range(10):
        v.tree(-80 + i * 17, 1, 70, "dark_oak_log", "dark_oak_leaves[persistent=true]", height=4, canopy=2)


def sparta(v: Voxel) -> None:
    """Austere Sparta: the Temple of Artemis Orthia, barracks, the training ground and the Eurotas."""
    S.pad(v, -70, -60, 70, 60, "grass_block")
    v.fill(-70, -3, 40, 70, 0, 60, "water")
    S.greek_temple(v, 0, -30, P, cols_long=6, cols_short=4, spacing=3, col_h=8, axis="x")
    for i in range(4):
        S.longhouse(v, -55 + i * 20, 0, {"wall2": "cobblestone", "floor": "stone", "roof": "terracotta"}, length=28, width=9)
    v.fill(30, 0, -10, 65, 0, 30, "coarse_dirt")                                               # training ground
    for x in range(32, 64, 8):
        v.column(x, 1, 32, 3, "oak_fence")
    S.statue(v, 45, -20, 12, "copper_block")                                                   # Leonidas
    for i in range(7):
        v.tree(-65 + i * 20, 1, 36, "oak_log", "oak_leaves[persistent=true]", height=5)


def delphi(v: Voxel) -> None:
    """The sanctuary of Apollo on terraces under Parnassus: treasuries, temple, theatre and the Pythia's tripod."""
    S.pad(v, -60, -60, 60, 80, "grass_block")
    for k in range(5):
        v.fill(-60, 1 + k * 6, -60 + k * 24, 60, 6 + k * 6, 80, "stone")
    # sacred way zigzagging up the terraces
    for k in range(4):
        y = 1 + k * 6
        v.fill(-50 if k % 2 else -10, y + 6, -60 + (k + 1) * 24 - 2, 10 if k % 2 else 50, y + 6, -60 + (k + 1) * 24 + 2, "smooth_quartz")
    S.greek_temple(v, -30, -50, P, cols_long=4, cols_short=2, spacing=3, col_h=6, axis="z")     # Athenian treasury
    v.merge(Voxel())
    tmp = Voxel()
    S.greek_temple(tmp, 0, 0, P, cols_long=15, cols_short=6, spacing=3, col_h=10, axis="x")     # Temple of Apollo
    v.merge(tmp, 0, 13, 0)
    v.set(0, 18, 0, "gold_block")                                                               # the tripod
    v.set(0, 19, 0, "campfire")
    tmp = Voxel()
    for i in range(10):
        tmp.disc(0, 1 + i, 20, 26 - i * 2, "smooth_stone", hollow=True, rz=18 - i)
    tmp.disc(0, 1, 20, 7, "polished_andesite")
    v.merge(tmp, 0, 24, 30)
    v.column(30, 13, -10, 8, "quartz_pillar"); v.set(30, 21, -10, "gold_block")                  # serpent column
    for k in range(8):
        v.set(31, 13 + k, -10, "lime_terracotta")
    for i in range(8):
        v.tree(-55 + i * 15, 1, -58, "dark_oak_log", "dark_oak_leaves[persistent=true]", height=4)


def trireme(v: Voxel) -> None:
    """An Athenian trireme at a stone mole; 170 rowers in three banks, bronze ram."""
    S.pad(v, -30, -20, 50, 20, "water")
    v.fill(-30, -3, -20, 50, -1, 20, "water")
    v.fill(-30, 0, 12, 50, 0, 16, "cobblestone")
    S.ship(v, -20, -4, {"hull": "spruce_planks", "deck": "oak_planks"}, length=36, beam=5, masts=1, style="trireme")
    for i in range(-18, 16, 3):                                                              # painted eye & shields
        v.set(i, 1, -2, "white_wool" if i % 2 else "red_wool")
    v.set(-19, 1, -2, "cyan_wool"); v.set(-19, 1, 2, "cyan_wool")


def atlantis(v: Voxel) -> None:
    """Plato's Atlantis (Critias): alternating rings of land and sea around the central island with the temple of Poseidon."""
    S.pad(v, -80, -80, 80, 80, "water")
    v.fill(-80, -3, -80, 80, -1, 80, "water")
    rings = ((75, "prismarine"), (62, "water"), (50, "prismarine"), (40, "water"), (28, "prismarine"), (20, "water"))
    for r, b in rings:
        v.disc(0, 0, 0, r, b)
        if b != "water":
            v.disc(0, -1, 0, r, b)
    v.disc(0, 0, 0, 14, "dark_prismarine")
    for r in (75, 50, 28):
        v.disc(0, 1, 0, r, "sea_lantern", hollow=True)
        v.disc(0, 1, 0, r - 11, "prismarine_bricks", hollow=True)
    # canal cuts to the sea and bridges between rings
    v.fill(-1, 0, -80, 1, 0, 80, "water")
    for r in (62, 40, 20):
        v.fill(r - 12, 1, -2, r + 1, 1, 2, "prismarine_bricks")
        v.fill(-r - 1, 1, -2, -r + 12, 1, 2, "prismarine_bricks")
    tmp = Voxel()
    S.greek_temple(tmp, 0, 0, {**P, "column": "gold_block", "wall": "dark_prismarine", "roof": "dark_prismarine"},
                   cols_long=6, cols_short=4, spacing=3, col_h=9, axis="x")
    v.merge(tmp)
    v.set(0, 20, 0, "beacon")
    for a in range(0, 360, 30):
        v.column(round(60 * math.cos(math.radians(a))), 1, round(60 * math.sin(math.radians(a))), 4 + (a // 30) % 3, "copper_block")


WORLD = World(
    id="greece",
    name="Classical Greece",
    game="Assassin's Creed Odyssey (2018)",
    era="431-422 BCE, the Peloponnesian War",
    description="Kassandra's and Alexios's Greece: Athens, Sparta, Delphi, the trireme fleet and Atlantis.",
).build(Build("athens", "Athens", "The Acropolis rock with Parthenon, Erechtheion, Propylaia and Athena Promachos; the theatre and agora below.", athens, "1 block = 2 m")
).build(Build("sparta", "Sparta", "Temple of Artemis Orthia, barracks, the training ground and the Eurotas.", sparta)
).build(Build("delphi", "Delphi", "Terraced sanctuary: the sacred way, treasuries, Temple of Apollo, theatre and the Pythia's tripod.", delphi)
).build(Build("trireme", "Athenian Trireme", "A three-banked warship with bronze ram at a stone mole.", trireme)
).build(Build("atlantis", "Atlantis", "Plato's concentric rings of land and sea around the temple of Poseidon.", atlantis))
