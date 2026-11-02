"""Ptolemaic Egypt - Assassin's Creed Origins (49-43 BCE)."""

import random

from .. import structures as S
from ..palettes import EGYPT, GREECE, PYRAMID_CASING, PYRAMID_CORE
from ..registry import Build, World
from ..voxel import Voxel

P = EGYPT


SLAB = "sandstone_slab[type=bottom]"
TOP_SLAB = "sandstone_slab[type=top]"
LANTERN = "lantern[hanging=true]"


def _pyr_r(base: int, height: int, k: int) -> int:
    """Half-width of the course ``k`` blocks above the base of ``Voxel.pyramid``."""
    return int(round(base / 2.0 * (1 - k / height)))


def _passage(v: Voxel, x1: int, x2: int, z0: int, n: int, y0: int, rise: int) -> None:
    """Walkable 3-high passage running +z from ``z0`` for ``n`` blocks.

    The floor moves by ``rise`` (+1 up, -1 down, 0 level) every second block;
    half-slabs smooth each step so the slope can be walked without jumping.
    """
    for k in range(n):
        z = z0 + k
        y = y0 + rise * (k // 2)
        v.carve(x1, y, z, x2, y + 2, z)
        if (rise > 0 and k % 2 == 1) or (rise < 0 and k % 2 == 0 and k > 0):
            v.fill(x1, y, z, x2, y, z, SLAB)


def _grand_gallery(v: Voxel, cx: int, z0: int, n: int, y0: int) -> None:
    """Corbelled gallery rising +z: 5 wide at the floor with side benches, 7
    wide above, then three courses stepping inward on top slabs to a 1-wide
    ceiling eight blocks up."""
    for k in range(n):
        z = z0 + k
        yf = y0 + k // 2
        v.carve(cx - 2, yf, z, cx + 2, yf, z)
        v.set(cx - 2, yf, z, SLAB)
        v.set(cx + 2, yf, z, SLAB)                      # side benches
        if k % 2 == 1:
            v.fill(cx - 1, yf, z, cx + 1, yf, z, SLAB)  # ramp step
        v.carve(cx - 3, yf + 1, z, cx + 3, yf + 4, z)
        for i, half in enumerate((3, 2, 1)):            # corbel courses
            y = yf + 4 + i
            v.carve(cx - half, y, z, cx + half, y, z)
            v.set(cx - half, y, z, TOP_SLAB)
            v.set(cx + half, y, z, TOP_SLAB)
        v.clear(cx, yf + 7, z)


def _steps_down(v: Voxel, x0: int, dx: int, z1: int, z2: int, floor: int = -3) -> None:
    """Half-slab stair from the plateau (stand at y 1) into a pit whose floor block is ``floor``."""
    for i in range(6):
        x = x0 + i * dx
        top = -(i // 2)
        if i % 2 == 0:
            v.fill(x, floor, z1, x, top, z2, "cut_sandstone")
        else:
            if top - 1 >= floor:
                v.fill(x, floor, z1, x, top - 1, z2, "cut_sandstone")
            v.fill(x, top, z1, x, top, z2, SLAB)


def _mastaba(v: Voxel, x: int, z: int, w: int, d: int, door: str) -> None:
    """Bench tomb with a battered top course, an offering chapel and a false door."""
    v.fill(x, 1, z, x + w - 1, 3, z + d - 1, "cut_sandstone")
    v.fill(x + 1, 4, z + 1, x + w - 2, 4, z + d - 2, "sandstone")
    zm = z + d // 2
    if door == "east":
        v.carve(x + w - 1, 1, zm - 1, x + w - 1, 2, zm)
        v.carve(x + w - 4, 1, zm - 2, x + w - 2, 2, zm + 1)
        v.fill(x + w - 5, 1, zm - 1, x + w - 5, 2, zm, "chiseled_sandstone")
    else:
        v.carve(x, 1, zm - 1, x, 2, zm)
        v.carve(x + 1, 1, zm - 2, x + 3, 2, zm + 1)
        v.fill(x + 4, 1, zm - 1, x + 4, 2, zm, "chiseled_sandstone")


def _mud_house(v: Voxel, x: int, z: int, w: int, d: int, wall: str, roof: str, door: str) -> None:
    v.walls(x, 1, z, x + w - 1, 3, z + d - 1, wall)
    v.fill(x, 4, z, x + w - 1, 4, z + d - 1, roof)
    dz = z if door == "north" else z + d - 1
    v.carve(x + w // 2, 1, dz, x + w // 2, 2, dz)
    v.clear(x, 2, z + d // 2)                            # a small window


def _dunes(v: Voxel, x1: int, z1: int, x2: int, z2: int, keep_out, count: int, seed: int) -> None:
    """Low elliptical sand mounds scattered over the pad, away from ``keep_out`` rectangles."""
    rng = random.Random(seed)
    placed = tries = 0
    while placed < count and tries < 5000:
        tries += 1
        r = rng.uniform(5, 13)
        rz = r * rng.uniform(0.45, 0.85)
        if rng.random() < 0.5:
            r, rz = rz, r
        cx = rng.randint(int(x1 + r + 2), int(x2 - r - 2))
        cz = rng.randint(int(z1 + rz + 2), int(z2 - rz - 2))
        bx1, bz1, bx2, bz2 = cx - r - 1, cz - rz - 1, cx + r + 1, cz + rz + 1
        if any(bx1 <= kx2 and bx2 >= kx1 and bz1 <= kz2 and bz2 >= kz1 for kx1, kz1, kx2, kz2 in keep_out):
            continue
        h = rng.randint(2, 4)
        for i in range(h):
            f = 1 - i / (h + 0.6)
            v.disc(cx, 1 + i, cz, r * f, "sand", rz=rz * f)
        placed += 1


def giza(v: Voxel) -> None:
    """Giza plateau at roughly 1 block = 2.3 m.

    Khufu 230 m / 146 m -> 101 x 64;  Khafre 215 m / 143 m -> 94 x 62 (keeps
    its casing near the top);  Menkaure 103 m / 65 m -> 45 x 28.  The Great
    Pyramid is walkable: north entrance, descending passage to the
    subterranean chamber, ascending passage, Grand Gallery, Queen's Chamber
    and the granite King's Chamber with its relieving chambers.  The Sphinx
    sits in its sunken quarry enclosure; causeways link mortuary and valley
    temples; boat pits, two mastaba cemeteries, the workers' village and
    dunes fill out the plateau.
    """
    S.pad(v, -90, -110, 227, 196, "sand")

    # ------------------------------------------------------------ Khufu
    cx, cz = 0, 0
    v.pyramid(cx, 1, cz, 101, 64, PYRAMID_CORE)
    # sandstone envelope so the parts of the route below ground stay enclosed
    v.fill(cx + 0, -3, cz - 33, cx + 8, 0, cz - 13, "sandstone")
    # approach ramp hugging the north face, up to the entrance at y 7
    for k in range(13):
        z = cz - 59 + k
        h = k // 2
        if h >= 1:
            v.fill(cx + 2, 1, z, cx + 6, h, z, "cut_sandstone")
        if k % 2 == 1:
            v.fill(cx + 2, h + 1, z, cx + 6, h + 1, z, SLAB)
    # junction room where the ascending passage leaves the descending one
    v.carve(cx - 1, 3, cz - 38, cx + 5, 7, cz - 36)
    # descending passage (east of centre, like the real one) from the north face
    _passage(v, cx + 3, cx + 5, cz - 46, 20, 7, -1)                 # y 7 -> -2
    _passage(v, cx + 3, cx + 5, cz - 26, 5, -2, 0)
    v.carve(cx + 1, -2, cz - 22, cx + 7, 0, cz - 14)                # subterranean chamber
    v.fill(cx + 1, -3, cz - 22, cx + 7, -3, cz - 14, "tuff")        # rough unfinished floor
    # gabled entrance stones above the opening
    for y, xs in ((10, range(cx + 2, cx + 7)), (11, (cx + 3, cx + 5)), (12, (cx + 4,))):
        zf = cz - _pyr_r(101, 64, y - 1)
        for x in xs:
            v.set(x, y, zf, "chiseled_sandstone")
    # ascending passage (on the axis) -> Grand Gallery -> King's Chamber
    v.fill(cx - 1, 3, cz - 36, cx + 1, 3, cz - 36, SLAB)
    _passage(v, cx - 1, cx + 1, cz - 35, 15, 4, 1)                  # y 4 -> 11
    _grand_gallery(v, cx, cz - 20, 21, 11)                          # y 11 -> 21
    v.fill(cx - 2, 20, cz + 1, cx + 2, 24, cz + 3, "polished_granite")   # antechamber
    v.carve(cx - 1, 21, cz + 1, cx + 1, 23, cz + 3)
    v.fill(cx - 5, 20, cz + 3, cx + 5, 37, cz + 15, "polished_granite")  # King's Chamber block
    v.carve(cx - 4, 21, cz + 4, cx + 4, 25, cz + 14)
    v.carve(cx - 1, 21, cz + 3, cx + 1, 23, cz + 3)                 # doorway from the antechamber
    for y in (28, 30, 32, 34, 36):                                  # relieving chambers
        v.carve(cx - 4, y, cz + 4, cx + 4, y, cz + 14)
    v.fill(cx - 3, 21, cz + 8, cx - 1, 22, cz + 10, "polished_blackstone")  # sarcophagus
    v.clear(cx - 2, 22, cz + 9)
    # Queen's Chamber: side passage east off the gallery foot, down and back under the axis
    v.carve(cx + 3, 11, cz - 21, cx + 9, 13, cz - 19)
    _passage(v, cx + 7, cx + 9, cz - 18, 9, 11, -1)                 # y 11 -> 7
    _passage(v, cx + 7, cx + 9, cz - 9, 13, 7, 0)
    v.carve(cx + 5, 7, cz + 1, cx + 9, 9, cz + 3)
    v.carve(cx - 4, 7, cz - 2, cx + 4, 10, cz + 8)
    for i, half in enumerate((3, 2, 1)):                            # pointed roof
        v.carve(cx - half, 11 + i, cz - 2, cx + half, 11 + i, cz + 8)
    v.carve(cx - 6, 7, cz + 2, cx - 5, 8, cz + 4)                   # corbelled niche
    v.carve(cx - 6, 9, cz + 3, cx - 5, 9, cz + 3)
    # sparse lanterns along the route
    for k in (3, 9, 15):
        v.set(cx + 3, 9 - k // 2, cz - 46 + k, LANTERN)
    v.set(cx + 2, 7, cz - 37, LANTERN)
    v.set(cx + 3, 0, cz - 24, LANTERN)
    v.set(cx + 4, 0, cz - 18, LANTERN)
    for k in (3, 9):
        v.set(cx - 1, 6 + k // 2, cz - 35 + k, LANTERN)
    for k in (2, 8, 14, 20):
        v.set(cx, 18 + k // 2, cz - 20 + k, LANTERN)
    for dx, dz in ((-3, 6), (3, 6), (-3, 12), (3, 12)):
        v.set(cx + dx, 25, cz + dz, LANTERN)
    v.set(cx + 8, 13, cz - 20, LANTERN)
    v.set(cx + 8, 9, cz - 4, LANTERN)
    v.set(cx, 13, cz + 3, LANTERN)
    # boat pits along the south side: one opened with the solar barque, one still sealed
    v.fill(cx - 34, -3, cz + 55, cx - 4, 0, cz + 61, "sandstone")
    v.carve(cx - 33, -2, cz + 56, cx - 5, 0, cz + 60)
    _steps_down(v, cx - 33, 1, cz + 56, cz + 56)
    v.fill(cx - 30, -2, cz + 57, cx - 8, -2, cz + 59, "dark_oak_planks")      # hull bottom
    v.fill(cx - 30, -1, cz + 57, cx - 8, -1, cz + 57, "dark_oak_planks")      # gunwales
    v.fill(cx - 30, -1, cz + 59, cx - 8, -1, cz + 59, "dark_oak_planks")
    v.fill(cx - 29, -1, cz + 58, cx - 9, -1, cz + 58, "spruce_planks")        # deck
    v.line((cx - 31, -1, cz + 58), (cx - 33, 1, cz + 58), "dark_oak_planks")  # papyriform prow
    v.line((cx - 7, -1, cz + 58), (cx - 5, 1, cz + 58), "dark_oak_planks")    # stern
    v.fill(cx - 21, 0, cz + 57, cx - 15, 1, cz + 59, "oak_planks")            # deckhouse
    v.carve(cx - 20, 0, cz + 58, cx - 16, 1, cz + 58)
    v.fill(cx - 21, 2, cz + 57, cx - 15, 2, cz + 59, "dark_oak_slab[type=bottom]")
    v.fill(cx + 6, 0, cz + 55, cx + 36, 0, cz + 61, "smooth_sandstone")       # sealed pit: cover stones
    # mortuary temple on the east face, causeway with low walls, queens' pyramids
    v.fill(cx + 52, 1, cz - 10, cx + 70, 6, cz + 12, "sandstone")
    v.carve(cx + 53, 1, cz - 9, cx + 69, 6, cz + 11)
    v.fill(cx + 53, 0, cz - 9, cx + 69, 0, cz + 11, "smooth_basalt")          # basalt pavement
    for px in (cx + 60, cx + 65):
        for pz in (cz - 6, cz + 8):
            v.column(px, 1, pz, 6, "polished_granite")
    v.fill(cx + 57, 1, cz - 9, cx + 57, 6, cz + 11, "sandstone")              # sanctuary wall
    v.carve(cx + 57, 1, cz, cx + 57, 3, cz + 2)
    v.fill(cx + 52, 1, cz, cx + 52, 3, cz + 2, "chiseled_sandstone")          # false door
    v.carve(cx + 70, 1, cz, cx + 70, 3, cz + 2)
    v.fill(cx + 71, 0, cz, cx + 149, 0, cz + 2, "smooth_sandstone")
    v.fill(cx + 71, 1, cz - 1, cx + 149, 2, cz - 1, "sandstone")
    v.fill(cx + 71, 1, cz + 3, cx + 149, 2, cz + 3, "sandstone")
    for i in range(3):
        v.pyramid(cx + 62, 1, cz + 22 + i * 18, 15, 10, PYRAMID_CORE)
    # valley temple at the foot of the causeway: pillared court
    v.fill(cx + 150, 1, cz - 11, cx + 172, 6, cz + 13, "sandstone")
    v.carve(cx + 151, 1, cz - 10, cx + 171, 6, cz + 12)
    v.fill(cx + 151, 0, cz - 10, cx + 171, 0, cz + 12, "smooth_sandstone")
    v.fill(cx + 151, 7, cz - 10, cx + 171, 7, cz + 12, "sandstone")
    v.carve(cx + 155, 7, cz - 6, cx + 167, 7, cz + 8)
    for px in (cx + 154, cx + 159, cx + 163, cx + 168):
        for pz in (cz - 7, cz + 9):
            v.column(px, 1, pz, 6, "polished_granite")
    for px in (cx + 154, cx + 168):
        for pz in (cz - 3, cz + 5):
            v.column(px, 1, pz, 6, "polished_granite")
    v.carve(cx + 150, 1, cz, cx + 150, 3, cz + 2)
    v.carve(cx + 172, 1, cz, cx + 172, 3, cz + 2)
    # cemeteries: western field (chapels face the pyramid) and eastern field
    for i in range(4):
        for j in range(3):
            _mastaba(v, cx - 89 + j * 13, cz - 42 + i * 20, 9, 14, "east")
    for i in range(3):
        for j in range(2):
            _mastaba(v, cx + 78 + j * 14, cz - 50 + i * 16, 10, 12, "west")

    # ------------------------------------------------------------ Khafre
    kx, kz = 120, 85
    v.pyramid(kx, 1, kz, 94, 62, PYRAMID_CORE)
    for y in range(1, 47):                       # stripped body: stepped courses, granite base
        r = _pyr_r(94, 62, y - 1)
        if y <= 2:
            v.walls(kx - r, y, kz - r, kx + r, y, kz + r, "polished_granite")
        elif y % 2 == 0:
            v.walls(kx - r, y, kz - r, kx + r, y, kz + r, "cut_sandstone")
    for y in range(47, 63):                      # surviving smooth casing at the apex
        r = _pyr_r(94, 62, y - 1)
        v.fill(kx - r, y, kz - r, kx + r, y, kz + r, PYRAMID_CASING)
    # mortuary temple against the east face
    v.fill(kx + 48, 1, kz - 19, kx + 58, 6, kz + 19, "sandstone")
    v.carve(kx + 49, 1, kz - 18, kx + 57, 6, kz + 18)
    v.fill(kx + 49, 0, kz - 18, kx + 57, 0, kz + 18, "smooth_sandstone")
    for pz in range(kz - 15, kz + 16, 6):
        v.column(kx + 51, 1, pz, 6, "polished_granite")
        v.column(kx + 55, 1, pz, 6, "polished_granite")
    v.carve(kx + 48, 1, kz - 1, kx + 48, 3, kz + 1)
    v.carve(kx + 58, 1, kz - 1, kx + 58, 3, kz + 1)
    # causeway down to the valley temple beside the Sphinx
    v.fill(kx + 59, 0, kz - 1, kx + 82, 0, kz + 1, "smooth_sandstone")
    v.fill(kx + 59, 1, kz - 2, kx + 82, 2, kz - 2, "sandstone")
    v.fill(kx + 59, 1, kz + 2, kx + 82, 2, kz + 2, "sandstone")
    # valley temple: limestone core faced in granite, alabaster floor, monolithic pillars
    vx, vz = 203, 70
    v.fill(vx, 1, vz, vx + 22, 8, vz + 28, "sandstone")
    v.fill(vx + 1, 1, vz + 1, vx + 21, 8, vz + 27, "polished_granite")
    v.carve(vx + 2, 1, vz + 2, vx + 20, 7, vz + 26)
    v.fill(vx + 2, 0, vz + 2, vx + 20, 0, vz + 26, "smooth_quartz")
    v.carve(vx + 8, 8, vz + 9, vx + 14, 8, vz + 19)                  # open light well
    for px in (vx + 5, vx + 9, vx + 13, vx + 17):
        for pz in (vz + 6, vz + 10, vz + 14, vz + 18, vz + 22):
            v.column(px, 1, pz, 7, "polished_granite")
    for pz in range(vz + 4, vz + 25, 4):                             # the seated statues of the king
        for px in (vx + 3, vx + 19):
            v.set(px, 1, pz, "smooth_stone")
            v.fill(px, 2, pz, px, 3, pz, "polished_diorite")
    v.carve(vx, 1, kz - 1, vx + 1, 4, kz + 1)                        # door from the causeway
    v.carve(vx + 21, 1, vz + 6, vx + 22, 4, vz + 8)                  # twin doors on the east front
    v.carve(vx + 21, 1, vz + 20, vx + 22, 4, vz + 22)

    # ------------------------------------------------------------ Menkaure
    mx, mz = 205, 150
    v.pyramid(mx, 1, mz, 45, 28, PYRAMID_CORE)
    for y in range(1, 10):                       # granite lower third, half of it left undressed
        r = _pyr_r(45, 28, y - 1)
        v.walls(mx - r, y, mz - r, mx + r, y, mz + r, "polished_granite" if y % 2 else "granite")
    for i in range(3):
        v.pyramid(mx - 38 + i * 16, 1, mz + 40, 11, 8, PYRAMID_CORE)

    # ------------------------------------------------------------ the Great Sphinx
    # facing east (+x) in its sunken quarry enclosure, 3 blocks below the plateau
    sx, sz = 180, 50
    v.fill(174, -3, sz - 10, 220, 0, sz + 10, "sandstone")
    v.carve(175, -2, sz - 9, 219, 0, sz + 9)
    _steps_down(v, 219, -1, sz - 9, sz - 7)
    v.fill(sx + 1, -2, sz - 4, sx + 24, 3, sz + 4, "sandstone")                # body
    v.carve(sx + 1, 2, sz - 4, sx + 1, 3, sz + 4)                              # rounded rump
    v.carve(sx + 1, 3, sz - 4, sx + 3, 3, sz - 4)
    v.carve(sx + 1, 3, sz + 4, sx + 3, 3, sz + 4)
    v.fill(sx + 6, 4, sz - 2, sx + 22, 4, sz + 2, "sandstone")                 # spine
    v.fill(sx + 4, -2, sz - 5, sx + 16, 1, sz - 5, "sandstone")                # haunches
    v.fill(sx + 4, -2, sz + 5, sx + 16, 1, sz + 5, "sandstone")
    v.fill(sx + 2, -2, sz + 6, sx + 14, -2, sz + 6, "sandstone")               # tail
    v.fill(sx + 14, -1, sz + 5, sx + 14, -1, sz + 6, "sandstone")
    v.fill(sx + 23, -2, sz - 3, sx + 28, 5, sz + 3, "sandstone")               # chest
    for dz in (-5, 2):                                                          # forelegs
        v.fill(sx + 24, -2, sz + dz, sx + 34, 0, sz + dz + 3, "sandstone")
        v.fill(sx + 33, -2, sz + dz, sx + 34, -1, sz + dz + 3, "cut_sandstone")  # paws
        v.carve(sx + 34, 0, sz + dz, sx + 34, 0, sz + dz + 3)
        for t in (dz + 1, dz + 3):
            v.clear(sx + 34, -1, sz + t)                                        # toe grooves
    v.fill(sx + 29, -2, sz - 1, sx + 29, 1, sz + 1, "polished_granite")        # Dream Stela
    v.set(sx + 29, 2, sz, "polished_granite")
    v.fill(sx + 32, -2, sz - 1, sx + 32, -2, sz + 1, "chiseled_sandstone")     # altar
    v.fill(sx + 24, 6, sz - 2, sx + 28, 7, sz + 2, "sandstone")                # neck
    v.fill(sx + 23, 8, sz - 3, sx + 29, 14, sz + 3, "smooth_sandstone")        # head, face at +x
    def stripe(y: int) -> str:
        return "yellow_terracotta" if y % 2 == 0 else "blue_terracotta"
    for y in range(10, 15):                                                     # nemes wings
        v.fill(sx + 23, y, sz - 4, sx + 29, y, sz - 4, stripe(y))
        v.fill(sx + 23, y, sz + 4, sx + 29, y, sz + 4, stripe(y))
    for y in range(6, 10):                                                      # lappets on the chest
        v.fill(sx + 28, y, sz - 4, sx + 29, y, sz - 4, stripe(y))
        v.fill(sx + 28, y, sz + 4, sx + 29, y, sz + 4, stripe(y))
    for y in range(7, 14):                                                      # pigtail down the back
        v.fill(sx + 22, y, sz - 1, sx + 22, y, sz + 1, stripe(y))
    v.fill(sx + 23, 15, sz - 3, sx + 29, 15, sz + 3, stripe(15))               # crown
    v.fill(sx + 24, 16, sz - 2, sx + 28, 16, sz + 2, stripe(16))
    v.fill(sx + 29, 14, sz - 3, sx + 30, 14, sz + 3, "yellow_terracotta")      # headband
    v.fill(sx + 30, 15, sz, sx + 30, 16, sz, "gold_block")                     # uraeus
    v.fill(sx + 29, 13, sz - 2, sx + 29, 13, sz + 2, "cut_sandstone")          # brow
    v.set(sx + 29, 12, sz - 1, "black_terracotta")                             # eyes
    v.set(sx + 29, 12, sz + 1, "black_terracotta")
    v.set(sx + 30, 10, sz, "cut_sandstone")                                    # what is left of the nose
    v.fill(sx + 29, 9, sz - 1, sx + 29, 9, sz + 1, "cut_sandstone")            # mouth

    # ------------------------------------------------------------ workers' village
    v.fill(170, 1, 100, 226, 4, 101, "sandstone")                   # the Wall of the Crow
    v.carve(196, 1, 100, 200, 3, 101)
    for i in range(6):
        x = 173 + i * 9
        wall, roof = ("terracotta", "brown_terracotta") if i % 2 == 0 else ("brown_terracotta", "terracotta")
        _mud_house(v, x, 106, 6, 6, wall, roof, "south")
        if i >= 2 and i < 5:
            _mud_house(v, x, 117, 6, 7, roof, wall, "north")
    # bakery with ovens, grain store and a chimney over the hearth
    v.walls(173, 1, 117, 186, 4, 123, "terracotta")
    v.fill(173, 5, 117, 186, 5, 123, "brown_terracotta")
    v.carve(179, 1, 117, 180, 2, 117)
    for x in (175, 178, 181):
        v.set(x, 1, 122, "smoker[facing=north]")
    v.fill(184, 1, 118, 185, 1, 119, "hay_block")
    v.set(174, 1, 118, "barrel[facing=up]")
    v.set(174, 1, 119, "barrel[facing=up]")
    v.set(179, 1, 120, "campfire[facing=north,lit=true]")
    v.clear(179, 5, 120)
    for gx in (220, 225):                                             # granaries
        v.cylinder(gx, 1, 119, 2.0, 4, "terracotta")
        v.dome(gx, 5, 119, 2.0, "brown_terracotta")
    # a few palms by the valley temple
    for i in range(3):
        v.palm(cx + 175 + i * 4, 1, cz + 15 + i * 3)

    # ------------------------------------------------------------ desert
    keep_out = [(-53, -63, 53, 53), (-37, 53, 39, 63), (-92, -45, -50, 40), (50, -54, 175, 70),
                (70, 35, 181, 137), (166, 10, 227, 127), (156, 123, 227, 196)]
    _dunes(v, -90, -110, 227, 196, keep_out, 48, seed=19)


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
).build(Build("giza", "Giza Plateau", "Khufu, Khafre and Menkaure with the Sphinx in its enclosure, mastaba cemeteries, causeways, temples, boat pits and the workers' village. Enter Khufu from the north face: descending passage, Grand Gallery, Queen's and King's Chambers.", giza, "1 block = 2.3 m")
).build(Build("alexandria", "Alexandria: Pharos and Library", "The three-tier Pharos lighthouse on its island mole, and the Mouseion library hall lined with scroll racks.", alexandria, "1 block = 2 m")
).build(Build("siwa", "Siwa Oasis", "The Oracle temple of Amun on the Aghurmi rock, the salt lake, palms and Bayek's mud-brick village.", siwa)
).build(Build("memphis", "Memphis: Temple of Ptah", "Pylon gateway, obelisks, sphinx avenue, peristyle court, hypostyle hall and sanctuary, plus the colossus.", memphis)
).build(Build("nile", "The Nile", "River bank with shadufs, irrigation canals and wheat fields, papyrus marsh, a felucca and a Nilometer.", nile)
).build(Build("cyrene", "Cyrene", "Greek colony of the Green Mountain: Temple of Zeus, agora and houses.", cyrene))
