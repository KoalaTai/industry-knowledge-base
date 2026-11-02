"""Ptolemaic Egypt - Assassin's Creed Origins (49-43 BCE)."""

from .. import structures as S
from ..palettes import EGYPT, GREECE, PYRAMID_CASING, PYRAMID_CORE
from ..registry import Build, World
from ..voxel import Voxel

P = EGYPT


def giza(v: Voxel) -> None:
    """Giza plateau at roughly 1 block = 2.3 m.

    Khufu 230 m / 146 m -> 101 x 64;  Khafre 215 m / 143 m -> 94 x 62 (keeps
    its casing near the top);  Menkaure 103 m / 65 m -> 45 x 28.  The Great
    Pyramid has its descending passage, Grand Gallery and King's Chamber
    carved out so you can walk in.
    """
    S.pad(v, -90, -110, 200, 120, "sand")
    # Khufu (Great Pyramid)
    cx, cz = 0, 0
    v.pyramid(cx, 1, cz, 101, 64, PYRAMID_CORE)
    v.fill(cx - 2, 1, cz + 50, cx + 2, 2, cz + 60, "sandstone")        # entrance ramp
    # descending passage from north face (-z) down under the pyramid
    for k in range(26):
        v.fill(cx - 1, 12 - k // 2, cz - 50 + k, cx + 1, 13 - k // 2, cz - 50 + k, "air")
    # ascending passage -> Grand Gallery -> King's Chamber
    for k in range(30):
        y = 1 + k // 2
        v.fill(cx - 1, y, cz - 26 + k, cx + 1, y + 1, cz - 26 + k, "air")
    v.fill(cx - 1, 16, cz + 4, cx + 1, 24, cz + 26, "air")              # Grand Gallery (corbelled)
    v.fill(cx - 2, 18, cz + 4, cx + 2, 22, cz + 26, "air")
    v.fill(cx - 5, 24, cz + 27, cx + 5, 30, cz + 37, "polished_granite")  # King's Chamber in granite
    v.fill(cx - 4, 25, cz + 28, cx + 4, 29, cz + 36, "air")
    v.fill(cx - 1, 25, cz + 29, cx + 1, 26, cz + 31, "polished_granite")  # sarcophagus
    v.fill(cx - 1, 25, cz + 26, cx + 1, 27, cz + 27, "air")
    v.fill(cx - 3, 8, cz + 2, cx + 3, 12, cz + 12, "air")               # Queen's Chamber
    # Khafre, with surviving casing on the upper quarter
    kx, kz = 120, 85
    v.pyramid(kx, 1, kz, 94, 62, PYRAMID_CORE)
    v.pyramid(kx, 47, kz, 24, 16, PYRAMID_CASING)
    # Menkaure
    mx, mz = 205, 150
    v.pyramid(mx, 1, mz, 45, 28, PYRAMID_CORE)
    v.pyramid(mx, 1, mz, 45, 8, "polished_granite", hollow=True)       # granite lower casing
    # queens' pyramids
    for i in range(3):
        v.pyramid(cx + 65, 1, cz - 30 + i * 22, 15, 10, PYRAMID_CORE)
        v.pyramid(mx - 38 + i * 16, 1, mz + 40, 11, 8, PYRAMID_CORE)
    # mastaba field west of Khufu
    for i in range(4):
        for j in range(3):
            v.fill(cx - 85 + j * 14, 1, cz - 40 + i * 20, cx - 76 + j * 14, 4, cz - 25 + i * 20, "cut_sandstone")
    # causeway and valley temple
    v.fill(cx + 50, 1, cz, cx + 150, 1, cz + 2, "smooth_sandstone")
    v.fill(cx + 150, 1, cz - 10, cx + 170, 6, cz + 12, "smooth_sandstone")
    v.fill(cx + 152, 1, cz - 8, cx + 168, 5, cz + 10, "air")
    v.fill(cx + 150, 1, cz, cx + 150, 3, cz + 2, "air")
    # Great Sphinx (body 73 m long -> 32 blocks) south-east of Khufu
    sx, sz = 150, 45
    v.fill(sx, 1, sz - 4, sx + 30, 6, sz + 4, "sandstone")              # body
    v.fill(sx - 4, 1, sz - 3, sx, 4, sz + 3, "sandstone")               # fore paws
    v.fill(sx - 1, 7, sz - 3, sx + 4, 9, sz + 3, "sandstone")           # chest
    v.fill(sx - 2, 10, sz - 3, sx + 3, 15, sz + 3, "smooth_sandstone")  # head
    v.fill(sx - 3, 12, sz - 4, sx + 4, 15, sz + 4, "smooth_sandstone")  # nemes headdress
    v.fill(sx - 3, 12, sz - 2, sx - 3, 14, sz + 2, "air")               # face
    v.fill(sx - 3, 12, sz - 1, sx - 3, 12, sz + 1, "smooth_sandstone")
    v.fill(sx + 4, 1, sz - 3, sx + 4, 5, sz + 3, "air")                 # tail gap
    for i in range(sx + 6, sx + 30, 3):
        v.set(i, 7, sz - 4, "sandstone")
        v.set(i, 7, sz + 4, "sandstone")
    # a few palms by the valley temple
    for i in range(3):
        v.palm(cx + 175 + i * 4, 1, cz + 15 + i * 3)


def alexandria(v: Voxel) -> None:
    """The Pharos lighthouse, the Library (Mouseion) and the harbour mole."""
    S.pad(v, -60, -40, 80, 90, "sand")
    v.fill(-60, -3, 50, 80, 0, 90, "water")                     # harbour
    v.fill(-60, 0, 46, 80, 0, 49, "smooth_sandstone")           # quay
    # Heptastadion mole out to the lighthouse island
    v.fill(30, 0, 50, 34, 0, 88, "cut_sandstone")
    v.fill(10, 0, 70, 60, 0, 90, "sandstone")                   # island
    # Pharos: square tier 30, octagonal tier 16, round tier 10, fire + statue
    cx, cz = 35, 80
    v.fill(cx - 10, 1, cz - 10, cx + 10, 30, cz + 10, "smooth_sandstone")
    v.fill(cx - 9, 1, cz - 9, cx + 9, 30, cz + 9, "air")
    for y in range(4, 29, 5):
        v.windows(cx - 10, y, cz - 10, cx + 10, cz + 10, "air", period=4, offset=2)
    v.fill(cx - 10, 31, cz - 10, cx + 10, 31, cz + 10, "cut_sandstone")
    # ramp spiralling inside (simplified as stacked floors)
    for y in range(1, 30, 6):
        v.fill(cx - 9, y, cz - 9, cx + 9, y, cz + 9, "cut_sandstone")
        v.fill(cx - 3, y, cz - 3, cx + 3, y, cz + 3, "air")
    v.cylinder(cx, 32, cz, 6.5, 16, "smooth_sandstone", hollow=True)   # (octagon approximated)
    v.disc(cx, 48, cz, 6.5, "cut_sandstone")
    v.cylinder(cx, 49, cz, 3.5, 10, "smooth_sandstone", hollow=True)
    v.disc(cx, 59, cz, 4, "cut_sandstone")
    v.fill(cx - 1, 60, cz - 1, cx + 1, 60, cz + 1, "netherrack")
    v.fill(cx - 1, 61, cz - 1, cx + 1, 61, cz + 1, "fire")
    for px in (cx - 3, cx + 3):
        for pz in (cz - 3, cz + 3):
            v.column(px, 60, pz, 4, "smooth_sandstone")
    v.fill(cx - 4, 64, cz - 4, cx + 4, 64, cz + 4, "cut_sandstone")
    S.statue(v, cx, cz, 9, "gold_block", y=65)                  # Zeus Soter statue on top
    # Library / Mouseion: colonnaded hall with reading rooms and scroll racks
    lx, lz = -40, 0
    S.pad(v, lx - 6, lz - 6, lx + 56, lz + 40, "smooth_sandstone")
    v.fill(lx, 1, lz, lx + 50, 12, lz + 34, "smooth_sandstone")
    v.fill(lx + 1, 1, lz + 1, lx + 49, 11, lz + 33, "air")
    v.fill(lx + 1, 1, lz + 1, lx + 49, 1, lz + 33, "cut_sandstone")
    for x in range(lx + 4, lx + 48, 5):
        v.column(x, 1, lz + 6, 11, "quartz_pillar")
        v.column(x, 1, lz + 28, 11, "quartz_pillar")
    for x in range(lx + 3, lx + 48, 3):
        v.fill(x, 2, lz + 1, x, 6, lz + 1, "bookshelf")
        v.fill(x, 2, lz + 33, x, 6, lz + 33, "bookshelf")
    v.fill(lx + 22, 1, lz + 34, lx + 28, 7, lz + 34, "air")
    for x in range(lx, lx + 51, 5):                              # portico
        v.column(x, 1, lz + 40, 10, "quartz_pillar")
    v.fill(lx - 1, 11, lz + 34, lx + 51, 12, lz + 41, "smooth_sandstone")
    v.set(lx + 25, 2, lz + 17, "lectern")
    # Greek-style grid of houses along the quay
    S.city_block(v, 0, 10, GREECE, cols=3, rows=2, lot=8, street=3, floors=(1, 2), roof="flat", seed=11)


def siwa(v: Voxel) -> None:
    """Bayek's home: the Oracle temple of Amun on its rock, the oasis and salt lake."""
    S.pad(v, -60, -60, 60, 60, "sand")
    v.disc(-30, 0, 30, 18, "water", rz=12)                      # salt lake
    v.disc(-30, 0, 30, 20, "white_concrete_powder", hollow=True, rz=14)
    # Aghurmi rock with temple
    for k in range(12):
        v.disc(20, 1 + k, -10, 22 - k * 1.2, "terracotta", rz=16 - k)
    v.fill(10, 13, -18, 30, 20, 0, "sandstone")
    v.fill(11, 13, -17, 29, 19, -1, "air")
    v.fill(19, 13, 0, 21, 16, 0, "air")
    v.fill(12, 13, -17, 28, 13, -1, "cut_sandstone")
    for z in range(-16, -1, 4):
        v.column(14, 13, z, 6, "sandstone")
        v.column(26, 13, z, 6, "sandstone")
    v.fill(19, 14, -16, 21, 15, -15, "gold_block")                # the oracle shrine
    for k in range(13):                                          # stair up the rock
        v.fill(19, 1 + k, 12 - k, 21, 1 + k, 12 - k, "cut_sandstone")
    # mud-brick village
    for i in range(5):
        for j in range(3):
            S.house(v, -20 + i * 9, 10 + j * 9, 6, 6, P, floors=1, roof="flat", wall="mud_bricks")
    # oasis palms and pool
    for i in range(14):
        v.palm(-50 + (i * 7) % 60, 1, -50 + (i * 11) % 40, height=6 + i % 3)
    v.disc(-20, 0, -30, 6, "water")


def memphis(v: Voxel) -> None:
    """Temple of Ptah with pylons, hypostyle hall and the colossus of Ramesses."""
    S.pad(v, -40, -30, 60, 80, "sand")
    S.egyptian_temple(v, 0, 0, P, width=31, length=60)
    S.statue(v, -20, -12, 18, "smooth_sandstone")
    S.city_block(v, 36, 0, P, cols=2, rows=3, lot=8, street=3, floors=(1, 2), roof="flat", seed=5)


def nile(v: Voxel) -> None:
    """A stretch of the Nile: shadufs, canals, papyrus marsh, a felucca and the Nilometer."""
    S.pad(v, -40, -60, 60, 60, "grass_block")
    v.fill(-40, -3, -12, 60, 0, 12, "water")                     # the river
    v.fill(-40, -4, -12, 60, -4, 12, "clay")
    for x in range(-38, 60, 3):                                   # papyrus banks
        v.set(x, 1, -13, "sugar_cane"); v.set(x, 2, -13, "sugar_cane")
        v.set(x, 1, 13, "sugar_cane"); v.set(x, 2, 13, "sugar_cane")
    # irrigation canals feeding fields in the floodplain
    for z in (20, 30, 40):
        v.fill(-30, 0, z, 50, 0, z, "water")
        v.fill(-30, 0, z + 2, 50, 0, z + 8, "farmland[moisture=7]")
        for x in range(-30, 50, 2):
            v.set(x, 1, z + 4, "wheat[age=7]")
            v.set(x + 1, 1, z + 6, "wheat[age=5]")
    # shadufs along the bank
    for x in (-20, 0, 20, 40):
        _shaduf(v, x, 14)
    # Nilometer: stone shaft with graduated stair down to the water
    nx, nz = 50, -20
    v.fill(nx - 4, -6, nz - 4, nx + 4, 3, nz + 4, "cut_sandstone")
    v.fill(nx - 3, -6, nz - 3, nx + 3, 3, nz + 3, "air")
    for k in range(9):
        v.fill(nx - 3, 3 - k, nz - 3 + k if k < 7 else nz + 3, nx - 1, 3 - k, nz - 3 + k if k < 7 else nz + 3, "smooth_sandstone")
    v.fill(nx - 2, -6, nz - 2, nx + 2, -1, nz + 2, "water")
    v.fill(nx - 4, -2, nz - 1, nx - 4, 0, nz + 1, "air")
    v.fill(nx - 6, -3, nz - 1, nx - 4, -2, nz + 1, "water")      # inlet from the river
    for k in range(10):
        v.set(nx + 3, -6 + k, nz, "chiseled_sandstone")           # cubit graduations
    # felucca
    v.fill(10, 0, -2, 24, 0, 2, "oak_planks")
    v.fill(11, -1, -1, 23, -1, 1, "dark_oak_planks")
    v.line((10, 0, 0), (8, 2, 0), "oak_planks")
    v.column(17, 1, 0, 10, "stripped_oak_log")
    v.line((17, 10, 0), (24, 4, 0), "stripped_oak_log")
    for k in range(6):
        v.fill(17 + k, 5 + k // 2, 0, 17 + k, 9 - k // 3, 0, "white_wool")
    for x in range(-35, 55, 12):
        v.palm(x, 1, -16, height=7)


def _shaduf(v: Voxel, x: int, z: int) -> None:
    """Counterweighted lever for lifting water; faces the river at -z."""
    v.column(x - 1, 1, z, 5, "stripped_oak_log")
    v.column(x + 1, 1, z, 5, "stripped_oak_log")
    v.fill(x - 1, 6, z, x + 1, 6, z, "stripped_oak_log")
    v.line((x, 6, z + 5), (x, 6, z - 6), "oak_fence")
    v.fill(x - 1, 5, z + 5, x + 1, 6, z + 6, "clay")              # counterweight
    v.line((x, 6, z - 6), (x, 2, z - 6), "chain")
    v.set(x, 1, z - 6, "water_cauldron[level=3]")


def cyrene(v: Voxel) -> None:
    """The Greek city of the Green Mountain: Temple of Zeus and agora."""
    S.pad(v, -50, -40, 60, 50, "grass_block")
    S.greek_temple(v, 0, 0, GREECE, cols_long=8, cols_short=17, spacing=3, col_h=10, axis="x")
    S.plaza(v, -45, 25, -5, 45, GREECE)
    S.city_block(v, 5, 25, GREECE, cols=3, rows=1, lot=8, street=3, floors=(1, 2), roof="flat", seed=2)
    for i in range(6):
        v.tree(-40 + i * 8, 1, -30, "dark_oak_log", "dark_oak_leaves[persistent=true]", height=4, canopy=2)


WORLD = World(
    id="egypt",
    name="Ptolemaic Egypt",
    game="Assassin's Creed Origins (2017)",
    era="49-43 BCE, reign of Ptolemy XIII and Cleopatra VII",
    description="Bayek's Egypt: Siwa, Alexandria, the Giza necropolis, Memphis and the Nile floodplain.",
).build(Build("giza", "Giza Plateau", "Khufu, Khafre and Menkaure with the Sphinx, mastabas, causeway and valley temple. Walk the Grand Gallery to the King's Chamber.", giza, "1 block = 2.3 m")
).build(Build("alexandria", "Alexandria: Pharos and Library", "The three-tier Pharos lighthouse on its island mole, and the Mouseion library hall lined with scroll racks.", alexandria, "1 block = 2 m")
).build(Build("siwa", "Siwa Oasis", "The Oracle temple of Amun on the Aghurmi rock, the salt lake, palms and Bayek's mud-brick village.", siwa)
).build(Build("memphis", "Memphis: Temple of Ptah", "Pylon gateway, obelisks, sphinx avenue, peristyle court, hypostyle hall and sanctuary, plus the colossus.", memphis)
).build(Build("nile", "The Nile", "River bank with shadufs, irrigation canals and wheat fields, papyrus marsh, a felucca and a Nilometer.", nile)
).build(Build("cyrene", "Cyrene", "Greek colony of the Green Mountain: Temple of Zeus, agora and houses.", cyrene))
