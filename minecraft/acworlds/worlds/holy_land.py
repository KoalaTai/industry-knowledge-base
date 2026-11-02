"""The Holy Land, Third Crusade - Assassin's Creed (2007), 1191."""

from .. import structures as S
from ..palettes import CRUSADER, LEVANT
from ..registry import Build, World
from ..voxel import Voxel


def masyaf(v: Voxel) -> None:
    """The Assassin fortress on its crag above the village."""
    P = CRUSADER
    S.pad(v, -60, -60, 60, 70, "grass_block")
    # the crag: stacked terraces
    for k in range(16):
        v.disc(0, 1 + k, -10, 30 - k * 1.3, "stone", rz=24 - k)
    top = 17
    base = v.translated(0, 0, 0)
    fort = Voxel()
    S.curtain_wall(fort, -18, -18, 18, 10, 8, P, gate="south", tower_r=3)
    S.keep(fort, 0, -6, 7, 16, P)
    # the library wing and the famous leap-of-faith tower
    S.house(fort, -14, -14, 9, 7, P, floors=2, roof="flat")
    S.tower(fort, 14, -14, 2.5, 26, P, top="flat")
    fort.fill(13, 27, -15, 15, 27, -13, "oak_planks")
    fort.set(14, 28, -17, "hay_block")
    v.merge(fort, 0, top - 1, 0)
    # garden and cliff-edge haystack landing
    v.fill(-30, 1, 8, -20, 2, 14, "hay_block")
    # switchback path up the crag
    for k in range(16):
        z = 14 - k * 1.5
        v.fill(-22 + k, 1 + k, int(z), -20 + k, 1 + k, int(z) + 2, "cobblestone")
    # village below the walls
    S.city_block(v, -30, 20, LEVANT, cols=5, rows=2, lot=8, street=3, floors=(1, 2), roof="flat", seed=3)
    S.plaza(v, -8, 48, 8, 60, LEVANT, fountain=True)
    for i in range(6):
        v.tree(-50 + i * 18, 1, 62, "oak_log", "oak_leaves[persistent=true]", height=5)


def jerusalem(v: Voxel) -> None:
    """Temple Mount: Dome of the Rock, al-Aqsa and the city wall with gate towers."""
    P = LEVANT
    S.pad(v, -70, -70, 70, 70, P["ground"])
    S.curtain_wall(v, -64, -64, 64, 64, 10, CRUSADER, gate="south", tower_r=3)
    v.fill(-50, 1, -50, 50, 1, 50, "smooth_sandstone")       # the platform
    # Dome of the Rock: octagonal arcade + drum + golden dome
    cx, cz = 0, -10
    v.cylinder(cx, 2, cz, 16, 10, "white_terracotta", hollow=True)     # octagon approximated
    v.cylinder(cx, 2, cz, 16, 10, "white_terracotta", hollow=True)
    for y in range(5, 10, 2):
        for a in range(0, 360, 20):
            import math
            v.set(round(cx + 16 * math.cos(math.radians(a))), y, round(cz + 16 * math.sin(math.radians(a))), "blue_glazed_terracotta")
    v.disc(cx, 11, cz, 16, "light_gray_terracotta")
    v.disc(cx, 2, cz, 15, "smooth_sandstone")
    v.cylinder(cx, 12, cz, 10, 8, "light_blue_terracotta", hollow=True)   # drum
    v.disc(cx, 2, cz, 9, "air"); v.disc(cx, 12, cz, 9, "air")
    v.dome(cx, 20, cz, 10, "gold_block")
    v.set(cx, 31, cz, "gold_block")
    v.fill(cx - 2, 2, cz - 1, cx + 2, 3, cz + 1, "stone")           # the Foundation Stone
    v.fill(cx - 1, 2, cz + 16, cx + 1, 5, cz + 16, "air")
    # al-Aqsa: long basilica-plan mosque with silver-grey dome
    S.basilica(v, 0, 18, LEVANT, length=40, width=25, h=14)
    v.dome(0, 14, 50, 7, "light_gray_concrete")
    # city quarters inside the walls
    S.city_block(v, -60, -60, LEVANT, cols=4, rows=3, lot=8, street=3, floors=(1, 3), roof="flat", seed=4)
    S.city_block(v, 20, -60, LEVANT, cols=4, rows=3, lot=8, street=3, floors=(1, 3), roof="flat", seed=8)
    # Church of the Holy Sepulchre with twin domes
    S.house(v, -58, 10, 24, 20, CRUSADER, floors=3, roof="flat")
    v.dome(-50, 13, 20, 6, "light_gray_concrete")
    v.dome(-40, 13, 20, 4, "light_gray_concrete")


def acre(v: Voxel) -> None:
    """Crusader port: Hospitaller fortress, harbour wall and the Tower of Flies."""
    P = CRUSADER
    S.pad(v, -60, -40, 70, 70, "stone")
    v.fill(-60, -3, 40, 70, 0, 70, "water")
    v.fill(-60, 0, 38, 70, 0, 39, "stone_bricks")                      # quay
    v.fill(40, 0, 40, 44, 0, 68, "stone_bricks")                       # breakwater
    S.tower(v, 42, 66, 4, 14, P, top="crenel")                          # Tower of Flies
    S.curtain_wall(v, -40, -30, 30, 30, 9, P, gate="south", tower_r=4)
    S.keep(v, -5, -5, 10, 18, P)
    # Hospitaller vaulted hall (refectory) with pointed arches
    hx, hz = -36, 10
    v.fill(hx, 1, hz, hx + 30, 9, hz + 16, P["wall"])
    v.fill(hx + 1, 1, hz + 1, hx + 29, 8, hz + 15, "air")
    for x in range(hx + 5, hx + 28, 6):
        v.column(x, 1, hz + 8, 8, P["column"])
        v.fill(x - 1, 8, hz + 1, x + 1, 8, hz + 15, P["trim"])
    v.fill(hx + 14, 1, hz + 16, hx + 16, 4, hz + 16, "air")
    S.city_block(v, -56, 36 - 30, LEVANT, cols=2, rows=2, lot=7, street=3, floors=(1, 2), roof="flat", seed=6)
    S.ship(v, -40, 50, {"hull": "dark_oak_planks", "deck": "oak_planks"}, length=28, beam=7, masts=1, style="galleon")


def damascus(v: Voxel) -> None:
    """The Umayyad Mosque, Jesus Minaret and the covered souk."""
    P = LEVANT
    S.pad(v, -70, -50, 70, 70, P["ground"])
    S.mosque(v, 0, -10, LEVANT, half=20, dome_r=8, minarets=3, minaret_h=36)
    # covered souk: a long vaulted street with stalls
    sx, sz = -60, 40
    v.fill(sx, 1, sz, sx + 120, 7, sz + 9, P["wall"])
    v.fill(sx + 1, 1, sz + 1, sx + 119, 6, sz + 8, "air")
    v.fill(sx + 1, 7, sz + 2, sx + 119, 7, sz + 7, "iron_bars")           # light through the vault
    for x in range(sx + 3, sx + 118, 4):
        v.fill(x, 1, sz + 1, x + 1, 1, sz + 2, "barrel")
        v.fill(x, 1, sz + 7, x + 1, 1, sz + 8, "barrel")
        v.set(x, 2, sz + 1, "red_wool" if x % 8 else "yellow_wool")
        v.set(x, 2, sz + 8, "blue_wool" if x % 8 else "lime_wool")
    v.fill(sx, 1, sz + 3, sx, 5, sz + 6, "air")
    v.fill(sx + 120, 1, sz + 3, sx + 120, 5, sz + 6, "air")
    S.city_block(v, -65, -45, LEVANT, cols=3, rows=2, lot=8, street=3, floors=(1, 3), roof="flat", seed=9)
    S.city_block(v, 30, -45, LEVANT, cols=3, rows=2, lot=8, street=3, floors=(1, 3), roof="flat", seed=10)
    for x in range(-60, 60, 15):
        v.tree(x, 1, 55, "jungle_log", "jungle_leaves[persistent=true]", height=5)


WORLD = World(
    id="holy_land",
    name="The Holy Land",
    game="Assassin's Creed (2007)",
    era="1191, the Third Crusade",
    description="Altair's Levant: Masyaf, Jerusalem, Acre and Damascus.",
).build(Build("masyaf", "Masyaf", "The Assassin fortress on its crag with keep, library wing, leap-of-faith tower and haystack, above the village.", masyaf)
).build(Build("jerusalem", "Jerusalem", "Walled city with the Dome of the Rock, al-Aqsa and the Holy Sepulchre.", jerusalem)
).build(Build("acre", "Acre", "Crusader port: Hospitaller fortress and vaulted refectory, harbour, breakwater and the Tower of Flies.", acre)
).build(Build("damascus", "Damascus", "The Umayyad Mosque with three minarets and a 120-block covered souk.", damascus))
