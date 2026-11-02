"""Abbasid Baghdad - Assassin's Creed Mirage (2023), 861 CE."""

import math

from .. import structures as S
from ..palettes import ABBASID
from ..registry import Build, World
from ..voxel import Voxel

P = ABBASID


def round_city(v: Voxel) -> None:
    """Al-Mansur's Round City (762): double circular walls, four gates, the Golden Gate palace and great mosque."""
    S.pad(v, -80, -80, 80, 80, "sand")
    v.disc(0, 0, 0, 72, "water", hollow=True)
    v.disc(0, 0, 0, 71, "water", hollow=True)                                        # moat
    v.cylinder(0, 1, 0, 68, 10, "mud_bricks", hollow=True)
    v.cylinder(0, 1, 0, 67, 10, "mud_bricks", hollow=True)
    for a in range(0, 360, 10):
        S.tower(v, round(68 * math.cos(math.radians(a))), round(68 * math.sin(math.radians(a))), 3, 13, P, top="flat", wall="mud_bricks")
    v.cylinder(0, 1, 0, 56, 7, "mud_bricks", hollow=True)                            # inner wall
    v.disc(0, 0, 0, 66, "smooth_sandstone")
    for a in (45, 135, 225, 315):                                                      # Kufa, Basra, Khurasan, Damascus gates
        gx, gz = math.cos(math.radians(a)), math.sin(math.radians(a))
        for r in range(50, 73):
            for w in (-2, -1, 0, 1, 2):
                px = round(r * gx - w * gz); pz = round(r * gz + w * gx)
                v.fill(px, 1, pz, px, 5, pz, "air")
                v.set(px, 0, pz, "cut_sandstone")
        tx, tz = round(68 * gx), round(68 * gz)
        v.fill(tx - 4, 11, tz - 4, tx + 4, 14, tz + 4, "mud_bricks")
        v.dome(tx, 14, tz, 4, "lime_terracotta")
        for r in range(20, 50):                                                        # arcaded streets
            px, pz = round(r * gx), round(r * gz)
            if r % 4 == 0:
                v.column(round(px - 4 * gz), 1, round(pz + 4 * gx), 4, "smooth_sandstone")
                v.column(round(px + 4 * gz), 1, round(pz - 4 * gx), 4, "smooth_sandstone")
    # ring of houses between the walls
    for a in range(0, 360, 12):
        if (a + 45) % 90 < 12:
            continue
        x = round(62 * math.cos(math.radians(a))); z = round(62 * math.sin(math.radians(a)))
        S.house(v, x - 3, z - 3, 6, 6, P, floors=1 + (a // 12) % 2, roof="flat", wall="mud_bricks", windows=False)
    # the Golden Gate palace with its green dome, and the great mosque
    v.fill(-16, 1, -16, 16, 10, 16, "smooth_sandstone")
    v.fill(-15, 1, -15, 15, 9, 15, "air")
    v.fill(-15, 1, -15, 15, 1, 15, P["floor"])
    v.cylinder(0, 11, 0, 10, 4, "smooth_sandstone", hollow=True)
    v.dome(0, 15, 0, 10, "green_terracotta")
    v.set(0, 26, 0, "gold_block")
    v.fill(-2, 1, 16, 2, 5, 16, "air")
    S.mosque(v, 0, -40, P, half=12, dome_r=6, minarets=1, minaret_h=30)


def house_of_wisdom(v: Voxel) -> None:
    """Bayt al-Hikma: library, translation hall and observatory around a courtyard with a pool."""
    S.pad(v, -40, -40, 40, 40, "sand")
    v.fill(-30, 1, -30, 30, 9, 30, P["wall"])
    v.fill(-29, 1, -29, 29, 8, 29, "air")
    v.fill(-29, 1, -29, 29, 1, 29, P["floor"])
    v.fill(-16, 1, -16, 16, 9, 16, "air")                                            # courtyard open to the sky
    v.fill(-16, 9, -16, 16, 9, 16, "air")
    v.fill(-29, 9, -29, 29, 9, 29, P["wall"])
    v.fill(-15, 9, -15, 15, 9, 15, "air")
    v.disc(0, 0, 0, 6, "water"); v.disc(0, 1, 0, 7, P["trim"], hollow=True)
    for x in range(-14, 15, 7):                                                        # courtyard arcade
        for z in (-16, 16):
            v.column(x, 1, z, 8, "smooth_sandstone")
            v.arch(x - 3, 1, z, 7, 7, 1, "smooth_sandstone", axis="x")
    for z in range(-14, 15, 7):
        for x in (-16, 16):
            v.column(x, 1, z, 8, "smooth_sandstone")
    for x in range(-28, 29, 2):                                                        # scroll shelves
        v.fill(x, 2, -29, x, 7, -29, "bookshelf"); v.fill(x, 2, 29, x, 7, 29, "bookshelf")
    for z in range(-28, 29, 2):
        v.fill(-29, 2, z, -29, 7, z, "bookshelf"); v.fill(29, 2, z, 29, 7, z, "bookshelf")
    for i, x in enumerate(range(-24, 25, 8)):
        v.set(x, 2, -22, "lectern"); v.set(x + 2, 2, -22, "cartography_table")
    v.fill(-2, 1, 30, 2, 5, 30, "air")
    for y in (4, 5):
        v.windows(-30, y, -30, 30, 30, "cyan_stained_glass_pane", period=3, offset=2)
    # observatory tower with an armillary sphere
    S.tower(v, 34, -34, 4, 18, P, top="flat", wall="smooth_sandstone")
    v.sphere(34, 22, -34, 3, "gold_block", hollow=True)
    v.fill(34, 19, -34, 34, 25, -34, "iron_bars")
    for a in range(0, 360, 10):
        v.set(round(34 + 3 * math.cos(math.radians(a))), 22, round(-34 + 3 * math.sin(math.radians(a))), "copper_block")


def samarra(v: Voxel) -> None:
    """The Malwiya: the spiral minaret of the Great Mosque of Samarra (851), on the Tigris."""
    S.pad(v, -60, -40, 60, 60, "sand")
    v.fill(-60, -3, 40, 60, 0, 60, "water")
    v.fill(-50, 1, -30, 50, 7, 30, "mud_bricks")
    v.fill(-49, 1, -29, 49, 7, 29, "air")
    v.fill(-49, 1, -29, 49, 1, 29, "sand")
    v.fill(-20, 1, -29, 20, 1, -10, P["floor"])
    for x in range(-48, 49, 4):
        for z in range(-28, -11, 4):
            v.column(x, 1, z, 6, "mud_bricks")
    v.fill(-49, 7, -29, 49, 7, -10, "mud_bricks")
    v.fill(-2, 1, 30, 2, 5, 30, "air")
    # the spiral minaret: 52 m tall, ramp winding anticlockwise five times
    cx, cz = 0, -42
    v.fill(cx - 8, 1, cz - 8, cx + 8, 4, cz + 8, "mud_bricks")
    h = 34
    for k in range(h):
        r = 7.2 - k * 0.14
        v.disc(cx, 5 + k, cz, r, "mud_bricks")
    for t in range(0, 1800, 4):                                                         # the ramp
        a = math.radians(t)
        r = 7.6 - (t / 1800) * 5
        y = 5 + int(t / 1800 * (h - 2))
        v.set(round(cx + (r + 1) * math.cos(a)), y, round(cz + (r + 1) * math.sin(a)), "smooth_sandstone")
        v.set(round(cx + (r + 2) * math.cos(a)), y + 1, round(cz + (r + 2) * math.sin(a)), "cut_sandstone")
    v.cylinder(cx, 5 + h, cz, 2.5, 5, "mud_bricks", hollow=True)
    v.set(cx, 11 + h, cz, "gold_block")
    for x in range(-55, 60, 10):
        v.palm(x, 1, 36, height=7)


def alamut(v: Voxel) -> None:
    """The Hidden Ones' mountain fortress (Alamut, on its rock in the Alborz)."""
    S.pad(v, -60, -60, 60, 60, "stone")
    for k in range(28):
        v.disc(0, 1 + k, 0, 46 - k * 1.3, "stone" if k % 5 else "andesite", rz=30 - k * 0.8)
    top = 29
    fort = Voxel()
    S.curtain_wall(fort, -20, -12, 20, 12, 6, {**P, "wall": "stone_bricks"}, gate="south", tower_r=2.5)
    S.keep(fort, 0, -3, 6, 12, {**P, "wall": "stone_bricks", "roof": "deepslate_tiles"})
    S.house(fort, -16, -8, 10, 7, P, floors=1, roof="flat", wall="mud_bricks")      # the library / bureau
    fort.fill(-15, 2, -7, -8, 5, -7, "bookshelf")
    v.merge(fort, 0, top - 1, 0)
    for k in range(29):                                                                # the single stair path
        v.fill(30 - k, 1 + k, 20 - k // 2, 31 - k, 1 + k, 22 - k // 2, "cobblestone")
    v.fill(-10, 0, 40, 10, 0, 58, "water")                                             # mountain stream
    v.fill(-12, 1, 42, -11, 3, 56, "stone")


def bazaar(v: Voxel) -> None:
    """Karkh market quarter: covered suq, caravanserai, a public bath (hammam) and a water-wheel on a canal."""
    S.pad(v, -60, -40, 60, 50, "sand")
    sx, sz = -55, -10
    v.fill(sx, 1, sz, sx + 110, 6, sz + 9, "mud_bricks")
    v.fill(sx + 1, 1, sz + 1, sx + 109, 5, sz + 8, "air")
    for x in range(sx + 4, sx + 108, 8):
        v.fill(x - 1, 6, sz + 3, x + 1, 6, sz + 6, "air")
        v.dome(x, 6, sz + 4, 3, "light_blue_terracotta")
        v.fill(x - 2, 1, sz + 1, x + 1, 1, sz + 2, "barrel")
        v.fill(x - 2, 1, sz + 7, x + 1, 1, sz + 8, "barrel")
        v.set(x, 2, sz + 1, ("red_wool", "yellow_wool", "blue_wool", "lime_wool")[(x // 8) % 4])
        v.set(x, 2, sz + 8, ("orange_wool", "purple_wool", "white_wool", "cyan_wool")[(x // 8) % 4])
    v.fill(sx, 1, sz + 3, sx, 4, sz + 6, "air"); v.fill(sx + 110, 1, sz + 3, sx + 110, 4, sz + 6, "air")
    # caravanserai: arcaded courtyard
    v.fill(-50, 1, 10, -10, 7, 45, "mud_bricks")
    v.fill(-49, 1, 11, -11, 6, 44, "air")
    v.fill(-49, 1, 11, -11, 1, 44, "packed_mud")
    v.fill(-42, 1, 18, -18, 8, 37, "air")
    v.fill(-42, 7, 18, -18, 7, 37, "air")
    for x in range(-42, -17, 6):
        v.column(x, 1, 18, 6, "smooth_sandstone"); v.column(x, 1, 37, 6, "smooth_sandstone")
    v.fill(-32, 1, 45, -28, 5, 45, "air")
    v.set(-30, 1, 27, "hay_block"); v.set(-25, 1, 27, "water_cauldron[level=3]")
    # hammam: domed rooms with pierced oculi
    v.fill(10, 1, 15, 40, 6, 40, "mud_bricks")
    v.fill(11, 1, 16, 39, 5, 39, "air")
    for (dx, dz) in ((18, 22), (32, 22), (25, 33)):
        v.dome(dx, 6, dz, 6, "light_gray_terracotta")
        for a in range(0, 360, 60):
            v.set(round(dx + 3 * math.cos(math.radians(a))), 10, round(dz + 3 * math.sin(math.radians(a))), "glass")
        v.disc(dx, 1, dz, 3, "water")
    v.fill(23, 1, 15, 27, 4, 15, "air")
    # noria on the canal
    v.fill(-60, -2, 46, 60, 0, 50, "water")
    for a in range(0, 360, 15):
        v.set(50, 1 + round(5 * math.sin(math.radians(a))), 48 + round(5 * math.cos(math.radians(a))), "stripped_jungle_log")
    v.fill(49, 1, 48, 51, 1, 48, "iron_block")
    v.fill(45, 6, 44, 55, 6, 44, "smooth_sandstone")


WORLD = World(
    id="baghdad",
    name="Abbasid Baghdad",
    game="Assassin's Creed Mirage (2023)",
    era="861 CE, the Anarchy at Samarra",
    description="Basim's Baghdad: the Round City, the House of Wisdom, Samarra's spiral minaret, the Karkh bazaar and Alamut.",
).build(Build("round_city", "The Round City", "Al-Mansur's double circular wall with four gates, the Golden Gate palace and the great mosque.", round_city, "1 block = 4 m")
).build(Build("house_of_wisdom", "House of Wisdom", "Library, translation hall and observatory around a courtyard with a pool.", house_of_wisdom)
).build(Build("samarra", "Great Mosque of Samarra", "The walled mosque and the Malwiya spiral minaret on the Tigris.", samarra)
).build(Build("alamut", "Alamut", "The Hidden Ones' fortress on its rock with the single stair path.", alamut)
).build(Build("bazaar", "Karkh Bazaar", "Covered suq, caravanserai, hammam and a noria waterwheel on the canal.", bazaar))
