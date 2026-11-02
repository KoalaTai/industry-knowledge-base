"""Ottoman Constantinople and Cappadocia - Assassin's Creed Revelations (2011), 1511-1512."""

from .. import structures as S
from ..palettes import OTTOMAN
from ..registry import Build, World
from ..voxel import Voxel

P = OTTOMAN


def hagia_sophia(v: Voxel) -> None:
    """Justinian's great church (537), by 1511 a mosque with minarets."""
    S.pad(v, -60, -50, 60, 80, "grass_block")
    cx, cz = 0, 0
    v.fill(cx - 30, 1, cz - 24, cx + 30, 18, cz + 24, P["wall"])
    v.fill(cx - 29, 1, cz - 23, cx + 29, 17, cz + 23, "air")
    v.fill(cx - 29, 1, cz - 23, cx + 29, 1, cz + 23, P["floor"])
    for y in (5, 6, 12, 13):
        v.windows(cx - 30, y, cz - 24, cx + 30, cz + 24, P["window"], period=3, offset=2)
    # buttress piers
    for px in (cx - 18, cx + 18):
        for pz in (cz - 24, cz + 24):
            v.fill(px - 2, 1, pz - 2, px + 2, 22, pz + 2, P["wall2"])
    # main dome on pendentives (drum with 40 windows), flanked by two half domes
    v.cylinder(cx, 19, cz, 17, 4, P["wall2"], hollow=True)
    for a in range(0, 360, 9):
        import math
        v.set(round(cx + 17 * math.cos(math.radians(a))), 21, round(cz + 17 * math.sin(math.radians(a))), P["window"])
    v.disc(cx, 19, cz, 16, "air")
    v.dome(cx, 23, cz, 17, P["roof"])
    v.set(cx, 41, cz, "gold_block")
    for dx in (-24, 24):
        v.dome(cx + dx, 18, cz, 11, P["roof"])
    for dx, dz in ((-12, -16), (12, -16), (-12, 16), (12, 16)):
        v.dome(cx + dx, 18, cz + dz, 5, P["roof"])
    for mx, mz in ((cx - 34, cz - 28), (cx + 34, cz - 28), (cx - 34, cz + 28), (cx + 34, cz + 28)):
        S.minaret(v, mx, mz, 46, P)
    v.fill(cx - 2, 1, cz + 24, cx + 2, 6, cz + 24, "air")
    S.city_block(v, -58, 40, P, cols=4, rows=2, lot=9, street=3, floors=(2, 3), roof="hip", seed=40)


def galata(v: Voxel) -> None:
    """The Genoese Galata Tower above the Golden Horn, with a harbour and ferry quay."""
    S.pad(v, -50, -40, 50, 60, "grass_block")
    v.fill(-50, -3, 30, 50, 0, 60, "water")
    v.fill(-50, 0, 28, 50, 0, 29, "stone_bricks")
    for k in range(8):
        v.disc(0, 1 + k, -5, 40 - k * 3, "coarse_dirt" if k % 2 else "grass_block", rz=28 - k * 2)
    t = Voxel()
    v_h = 36
    t.cylinder(0, 1, 0, 6, v_h, "stone_bricks", hollow=True)
    t.cylinder(0, 1, 0, 5, v_h, "stone_bricks", hollow=True)
    t.disc(0, 1, 0, 4, P["floor"])
    for y in range(8, v_h, 7):
        t.disc(0, y, 0, 4, P["floor"])
    t.disc(0, v_h + 1, 0, 8, "stone_bricks")
    t.cylinder(0, v_h + 2, 0, 7, 4, "stone_bricks", hollow=True)
    for a in range(0, 360, 30):
        import math
        t.set(round(7 * math.cos(math.radians(a))), v_h + 4, round(7 * math.sin(math.radians(a))), "air")
    t.disc(0, v_h + 6, 0, 7, "stone_bricks")
    t.cone(0, v_h + 7, 0, 7, 12, "deepslate_tiles")
    v.merge(t, 0, 8, -5)
    S.city_block(v, -45, 8, P, cols=3, rows=1, lot=9, street=3, floors=(2, 3), roof="hip", seed=41)
    S.city_block(v, 12, 8, P, cols=3, rows=1, lot=9, street=3, floors=(2, 3), roof="hip", seed=42)
    S.ship(v, -30, 40, {"hull": "dark_oak_planks", "deck": "oak_planks"}, length=30, beam=7, masts=2)


def theodosian_walls(v: Voxel) -> None:
    """Triple land walls (inner wall, outer wall, moat) of 413 CE with a gate."""
    S.pad(v, -20, -80, 50, 80, "grass_block")
    v.fill(30, -3, -80, 40, 0, 80, "water")                             # moat
    v.fill(20, 1, -80, 23, 7, 80, "stone_bricks")                       # outer wall
    v.crenellate(20, 8, -80, 23, 80, "stone_bricks")
    for z in range(-70, 80, 25):
        S.tower(v, 21, z, 3, 10, P, top="crenel", square=True, wall="stone_bricks")
    v.fill(0, 1, -80, 6, 12, 80, "stone_bricks")                        # inner wall with brick bands
    for y in range(3, 12, 4):
        v.fill(0, y, -80, 6, y, 80, "bricks")
    v.crenellate(0, 13, -80, 6, 80, "stone_bricks")
    for z in range(-60, 80, 25):
        S.tower(v, 3, z, 4.5, 18, P, top="crenel", square=True, wall="stone_bricks")
    v.fill(0, 1, -2, 6, 6, 2, "air")                                    # the gate passage
    v.fill(20, 1, -2, 23, 5, 2, "air")
    v.fill(30, 0, -3, 40, 0, 3, "oak_planks")                            # moat bridge
    v.fill(7, 0, -80, 19, 0, 80, "cobblestone")                          # the peribolos terrace


def derinkuyu(v: Voxel) -> None:
    """The Cappadocian underground city: shafts, galleries, rolling stone doors, going down 7 levels."""
    S.pad(v, -40, -40, 40, 40, "terracotta")
    for i in range(8):
        for j in range(8):
            v.cone(-35 + i * 10, 1, -35 + j * 10, 3, 7 + (i + j) % 4, "white_terracotta")  # fairy chimneys
    # vertical ventilation shaft
    v.fill(0, -40, 0, 0, 1, 0, "air")
    v.fill(-1, -40, -1, 1, -40, 1, "water")
    for level in range(7):
        y = -4 - level * 5
        # ring gallery + four rooms
        for dx, dz in ((14, 0), (-14, 0), (0, 14), (0, -14)):
            v.fill(dx - 5, y, dz - 5, dx + 5, y + 3, dz + 5, "air")
            v.fill(min(0, dx) - 1, y, min(0, dz) - 1, max(0, dx) + 1, y + 2, max(0, dz) + 1, "air")
            # rolling stone door: a disc beside the tunnel mouth
            v.set(dx // 2, y, dz // 2 + (2 if dz == 0 else 0), "polished_andesite")
            v.set(dx // 2, y + 1, dz // 2 + (2 if dz == 0 else 0), "polished_andesite")
        v.set(14, y, 0, "barrel"); v.set(-14, y, 0, "water_cauldron[level=2]")
        v.set(0, y, 14, "loom"); v.set(0, y, -14, "furnace")
        v.set(-3, y, -3, "wall_torch[facing=east]")
        v.set(3, y + 1, 3, "lantern")
        # stair to the next level
        for k in range(5):
            v.fill(18 + k, y - k, -1, 18 + k, y - k + 2, 1, "air")
    v.fill(-2, 0, 20, 2, 1, 22, "air")                                     # surface entrance
    for k in range(5):
        v.fill(-1, 0 - k, 20 - k, 1, 2 - k, 20 - k, "air")


def grand_bazaar(v: Voxel) -> None:
    """Kapalicarsi: a grid of vaulted streets with stalls, under domed roofs."""
    S.pad(v, -40, -40, 40, 40, "stone_bricks")
    for z in (-30, -10, 10, 30):
        v.fill(-40, 1, z - 4, 40, 6, z + 4, P["wall"])
        v.fill(-39, 1, z - 3, 39, 5, z + 3, "air")
        for x in range(-38, 40, 8):
            v.dome(x, 6, z, 4, P["roof"])
            v.set(x, 6, z, "air")
        for x in range(-37, 38, 4):
            v.set(x, 1, z - 3, "barrel"); v.set(x, 1, z + 3, "barrel")
            v.set(x, 2, z - 3, ("red_wool", "blue_wool", "yellow_wool", "lime_wool")[(x // 4) % 4])
            v.set(x, 2, z + 3, ("orange_wool", "purple_wool", "cyan_wool", "white_wool")[(x // 4) % 4])
            v.set(x + 1, 5, z, "lantern")
    for x in (-20, 0, 20):
        v.fill(x - 3, 1, -40, x + 3, 6, 40, P["wall"])
        v.fill(x - 2, 1, -39, x + 2, 5, 39, "air")
        for z in range(-30, 40, 20):
            v.fill(x - 2, 1, z - 4, x + 2, 5, z + 4, "air")


WORLD = World(
    id="constantinople",
    name="Ottoman Constantinople",
    game="Assassin's Creed Revelations (2011)",
    era="1511-1512",
    description="Ezio's last journey: Hagia Sophia, Galata, the Theodosian walls, the Grand Bazaar and Derinkuyu.",
).build(Build("hagia_sophia", "Hagia Sophia", "Justinian's domed church of 537 with its pendentive dome, half domes and Ottoman minarets.", hagia_sophia)
).build(Build("galata", "Galata Tower", "The Genoese tower on its hill above the Golden Horn with the ferry quay.", galata)
).build(Build("theodosian_walls", "Theodosian Walls", "Triple land walls: moat, outer wall, inner wall with brick bands and a gate.", theodosian_walls)
).build(Build("derinkuyu", "Derinkuyu", "Cappadocian underground city carved seven levels below the fairy chimneys.", derinkuyu)
).build(Build("grand_bazaar", "Grand Bazaar", "Vaulted market streets under rows of small domes.", grand_bazaar))
