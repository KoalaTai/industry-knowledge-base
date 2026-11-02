"""Ottoman Constantinople and Cappadocia - Assassin's Creed Revelations (2011), 1511-1512."""

import math

from .. import structures as S
from ..palettes import OTTOMAN
from ..registry import Build, World
from ..voxel import Voxel

P = OTTOMAN


# ----------------------------------------------------------------- Hagia Sophia

_HS_LEAD = "light_gray_concrete"
_HS_TRIM = "light_gray_terracotta"
_HS_MARBLE = "polished_diorite"
_HS_MARBLE2 = "polished_andesite"
_HS_COLUMN = "quartz_pillar"
_HS_CAPITAL = "chiseled_quartz_block"
_HS_LEAVES = "spruce_leaves[persistent=true]"


def _hs_brick(x: int, y: int, z: int) -> str:
    """Byzantine brickwork: red courses, a stone band every sixth row, pink flecks."""
    if y % 6 == 0:
        return _HS_TRIM
    if (x * 31 + y * 17 + z * 7) % 12 == 0:
        return "pink_terracotta"
    return "red_terracotta" if y % 6 == 3 else "terracotta"


def _hs_gold(x: int, y: int, z: int) -> str:
    """Gold-ground mosaic: mostly gold with glazed tesserae."""
    return "gold_block" if (x * 5 + y * 3 + z * 11) % 3 else "yellow_glazed_terracotta"


def _hs_brick_box(v: Voxel, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> None:
    """Solid box whose four outer faces carry the mixed brick courses."""
    v.fill(x1, y1, z1, x2, y2, z2, "terracotta")
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            v.set(x, y, z1, _hs_brick(x, y, z1))
            v.set(x, y, z2, _hs_brick(x, y, z2))
        for z in range(z1, z2 + 1):
            v.set(x1, y, z, _hs_brick(x1, y, z))
            v.set(x2, y, z, _hs_brick(x2, y, z))


def _hs_opening(v: Voxel, axis: str, a1: int, a2: int, y1: int, c: int, half: int, h: int,
                stair: str = "") -> None:
    """Stepped-arch opening through a wall.

    ``axis`` 'x': the wall runs along x, the opening is centred on x = c and cuts
    through z = a1..a2 (the wall thickness).  'z': centred on z = c, through x = a1..a2.
    The straight part is ``h`` tall and 2*half+1 wide; above it the opening narrows by
    one block per row and upside-down ``stair`` blocks round the shoulders.
    """
    lo, hi = min(a1, a2), max(a1, a2)

    def put(i: int, y: int, block: str = "") -> None:
        for t in range(lo, hi + 1):
            x, z = (i, t) if axis == "x" else (t, i)
            if block:
                v.set(x, y, z, block)
            else:
                v.clear(x, y, z)

    for y in range(y1, y1 + h):
        for i in range(c - half, c + half + 1):
            put(i, y)
    pos, neg = ("east", "west") if axis == "x" else ("south", "north")
    for j in range(half):
        hw = half - 1 - j
        y = y1 + h + j
        for i in range(c - hw, c + hw + 1):
            put(i, y)
        if stair:
            put(c + hw + 1, y, f"{stair}[facing={pos},half=top]")
            put(c - hw - 1, y, f"{stair}[facing={neg},half=top]")


def _hs_half_cylinder(v: Voxel, cx: int, y1: int, cz: int, r: float, h: int, block,
                      sign: int = 1, hollow: bool = False) -> None:
    """Half cylinder on the ``sign`` side of x = cx; ``block`` may be a str or f(x, y, z)."""
    for x in range(int(cx - r - 1), int(cx + r + 2)):
        if (x - cx) * sign <= 0:
            continue
        for z in range(int(cz - r - 1), int(cz + r + 2)):
            d = math.hypot(x - cx, z - cz)
            if d <= r + 0.5 and (not hollow or d >= r - 0.5):
                for y in range(y1, y1 + h):
                    v.set(x, y, z, block if isinstance(block, str) else block(x, y, z))


def _hs_shell(v: Voxel, cx: int, cy: int, cz: int, r: float, block, hollow: bool = True,
              y_min: int = None, x_sign: int = 0) -> None:
    """Sphere (shell or solid) clipped below ``y_min`` and to one side of x = cx."""
    lo = int(cy - r - 1) if y_min is None else max(y_min, int(cy - r - 1))
    for x in range(int(cx - r - 1), int(cx + r + 2)):
        if x_sign and (x - cx) * x_sign <= 0:
            continue
        for y in range(lo, int(cy + r + 2)):
            for z in range(int(cz - r - 1), int(cz + r + 2)):
                d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2)
                if d <= r + 0.5 and (not hollow or d >= r - 0.5):
                    v.set(x, y, z, block if isinstance(block, str) else block(x, y, z))


def _hs_ring(cx: int, cz: int, r: float):
    """Cells of a one-block ring of radius r, sorted by angle."""
    cells = []
    for x in range(int(cx - r - 1), int(cx + r + 2)):
        for z in range(int(cz - r - 1), int(cz + r + 2)):
            d_out = ((x - cx) / (r + 0.5)) ** 2 + ((z - cz) / (r + 0.5)) ** 2
            d_in = ((x - cx) / (r - 0.5)) ** 2 + ((z - cz) / (r - 0.5)) ** 2
            if d_out <= 1.0 < d_in:
                cells.append((x, z))
    cells.sort(key=lambda c: math.atan2(c[1] - cz, c[0] - cx))
    return cells


def _hs_arcade(v: Voxel, axis: str, fixed: int, y1: int, h: int, a1: int, a2: int,
               step: int = 4) -> None:
    """Columns every ``step`` blocks with capitals, stair-built arches and a spandrel row."""
    yc = y1 + h
    pos, neg = ("west", "east") if axis == "x" else ("north", "south")
    for i in range(a1, a2 + 1, step):
        x, z = (i, fixed) if axis == "x" else (fixed, i)
        v.fill(x, y1, z, x, yc - 1, z, _HS_COLUMN)
        v.set(x, yc, z, _HS_CAPITAL)
        for d, face in ((1, pos), (-1, neg)):
            j = i + d
            if a1 <= j <= a2:
                xx, zz = (j, fixed) if axis == "x" else (fixed, j)
                v.set(xx, yc, zz, f"quartz_stairs[facing={face},half=top]")
    if axis == "x":
        v.fill(a1, yc + 1, fixed, a2, yc + 1, fixed, _HS_MARBLE)
    else:
        v.fill(fixed, yc + 1, a1, fixed, yc + 1, a2, _HS_MARBLE)


def _hs_minaret(v: Voxel, x: int, z: int, h: int) -> None:
    """Slender Ottoman minaret: square base, round shaft, two balconies, lead cap."""
    v.fill(x - 1, 1, z - 1, x + 1, 8, z + 1, _HS_TRIM)
    v.fill(x - 2, 9, z - 2, x + 2, 9, z + 2, _HS_TRIM)
    v.cylinder(x, 10, z, 1, h - 9, "smooth_quartz")
    for by in (h * 3 // 5, h * 5 // 6):
        v.disc(x, by, z, 2.5, "quartz_slab[type=bottom]")
        v.disc(x, by + 1, z, 2.5, "iron_bars", hollow=True)
        v.disc(x, by, z, 1, "smooth_quartz")
        v.disc(x, by + 1, z, 1, "smooth_quartz")
    v.cone(x, h + 1, z, 2, 7, _HS_LEAD)
    v.set(x, h + 8, z, "gold_block")


def _hs_cypress(v: Voxel, x: int, z: int, h: int = 9) -> None:
    v.column(x, 1, z, h, "dark_oak_log")
    for y in range(2, h + 1):
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            v.set(x + dx, y, z + dz, _HS_LEAVES)
    for y in range(3, h - 3):
        for dx, dz in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
            v.set(x + dx, y, z + dz, _HS_LEAVES)
    v.set(x, h + 1, z, _HS_LEAVES)
    v.set(x, h + 2, z, _HS_LEAVES)


def _hs_lamp(v: Voxel, x: int, z: int) -> None:
    v.fill(x, 1, z, x, 3, z, "polished_blackstone_wall")
    v.set(x, 4, z, "lantern")


def _hs_chandelier(v: Voxel, cx: int, cz: int, r: float, y: int, ceiling, chains: int = 8) -> None:
    """A low iron ring with hanging lanterns, hung from the vault on chains.

    ``ceiling(x, z)`` returns the highest air block under the vault at (x, z)."""
    cells = _hs_ring(cx, cz, r)
    for x, z in cells:
        v.set(x, y, z, "polished_blackstone")
    for x, z in cells[::3]:
        v.set(x, y - 1, z, "lantern[hanging=true]")
    for k in range(chains):
        x, z = cells[(k * len(cells)) // chains]
        top = ceiling(x, z)
        if top > y:
            v.fill(x, y + 1, z, x, top, z, "chain[axis=y]")


def hagia_sophia(v: Voxel) -> None:
    """Justinian's great church (537), by 1511 a mosque with minarets."""
    S.pad(v, -60, -50, 60, 80, "grass_block")
    L, T, M, M2 = _HS_LEAD, _HS_TRIM, _HS_MARBLE, _HS_MARBLE2
    STAIR_OUT, STAIR_IN = "polished_andesite_stairs", "quartz_stairs"

    # ---- main block: 61 x 49, two-thick brick walls lined with marble, lead roof at y 18
    _hs_brick_box(v, -30, 1, -24, 30, 18, 24)
    v.walls(-29, 2, -23, 29, 17, 23, M)
    v.fill(-28, 2, -22, 28, 17, 22, "air")
    v.fill(-30, 18, -24, 30, 18, 24, L)
    for x, z in ((-30, -24), (30, -24), (-30, 24), (30, 24)):
        v.fill(x, 1, z, x, 17, z, T)                                   # corner quoins
    for x in range(-30, 31):
        v.set(x, 17, -24, T); v.set(x, 17, 24, T)                       # cornice
    for z in range(-24, 25):
        v.set(-30, 17, z, T); v.set(30, 17, z, T)

    # ---- marble floor: diorite with andesite bands and the omphalion
    v.fill(-28, 1, -22, 28, 1, 22, M)
    for x in range(-28, 29):
        if (x + 28) % 7 == 0:
            v.fill(x, 1, -22, x, 1, 22, M2)
    for z in range(-22, 23):
        if (z + 22) % 7 == 0:
            v.fill(-28, 1, z, 28, 1, z, M2)
    v.disc(5, 1, 5, 4, M2)
    v.disc(5, 1, 5, 3, "polished_granite", hollow=True)
    v.disc(5, 1, 5, 2, "dark_prismarine", hollow=True)
    v.disc(5, 1, 5, 1, "polished_granite")
    for dx, dz in ((4, 0), (-4, 0), (0, 4), (0, -4)):
        v.set(5 + dx, 1, 5 + dz, "dark_prismarine")

    # ---- windows: a ground row and a gallery row on every face (pane outside, recess inside)
    for x in range(-26, 27, 4):
        if abs(abs(x) - 14) <= 2:
            continue                                                    # buttresses
        for y in (4, 5, 6, 12, 13, 14):
            if y < 10 and abs(x) <= 3:
                v.set(x, y, -24, "glass_pane"); v.clear(x, y, -23)     # south door below
                continue
            for zo, zi in ((-24, -23), (24, 23)):
                v.set(x, y, zo, "glass_pane"); v.clear(x, y, zi)
    for z in range(-20, 21, 4):
        for y in (4, 5, 6, 12, 13, 14):
            if y > 10 or (abs(z) > 2 and not 8 <= abs(z) <= 12):
                v.set(-30, y, z, "glass_pane"); v.clear(-29, y, z)
            if y > 10 or abs(z) > 5:
                v.set(30, y, z, "glass_pane"); v.clear(29, y, z)

    # ---- doors: south (to the courtyard) and the three west doors into the narthex
    v.fill(-2, 1, 23, 2, 1, 24, M)
    _hs_opening(v, "x", 23, 24, 2, 0, 2, 4, STAIR_OUT)
    v.fill(-3, 1, 25, 3, 1, 25, f"{STAIR_OUT}[facing=north,half=bottom]")
    for z in (-10, 0, 10):
        v.fill(-30, 1, z - 1, -29, 1, z + 1, M)
        _hs_opening(v, "z", -30, -29, 2, z, 1, 4, STAIR_OUT)
        v.fill(-31, 1, z - 2, -31, 1, z + 2, f"{STAIR_OUT}[facing=east,half=bottom]")

    # ---- narthex wall with the Imperial Door, galleries on arcades, the four piers
    v.fill(-23, 2, -22, -23, 8, 22, M)
    for z in (-16, -8, 0, 8, 16):
        _hs_opening(v, "z", -23, -23, 2, z, 1, 5 if z == 0 else 4, STAIR_IN)
    v.set(-23, 7, 0, "gold_block")                                      # Imperial Door lintel
    for zz in (-14, 14):
        _hs_arcade(v, "x", zz, 2, 5, -22, 26)
    v.fill(-28, 9, 14, 28, 9, 22, M)                                    # gallery floors
    v.fill(-28, 9, -22, 28, 9, -14, M)
    v.fill(-28, 9, -22, -23, 9, 22, M)
    v.fill(-22, 10, 14, 28, 10, 14, "quartz_slab[type=bottom]")         # balustrades
    v.fill(-22, 10, -14, 28, 10, -14, "quartz_slab[type=bottom]")
    v.fill(-23, 10, -22, -23, 10, 22, "quartz_slab[type=bottom]")
    for zz in (-14, 14):
        _hs_arcade(v, "x", zz, 10, 5, -22, 26)
        v.fill(-22, 17, zz, 28, 17, zz, M)
    _hs_arcade(v, "z", -23, 10, 5, -20, 20)
    v.fill(-23, 17, -22, -23, 17, 22, M)
    for px, pz in ((-14, -14), (14, -14), (-14, 14), (14, 14)):
        v.fill(px - 1, 2, pz - 1, px + 1, 17, pz + 1, M)
        for y in (9, 16):
            v.fill(px - 1, y, pz - 1, px + 1, y, pz + 1, "polished_granite")
    # ramps up to the galleries (south-west corner of the narthex, north-east corner)
    for i in range(8):
        y = 2 + i
        for x in (-27, -26):
            if i:
                v.fill(x, 2, 15 + i, x, y - 1, 15 + i, M)
            v.set(x, y, 15 + i, f"{STAIR_IN}[facing=south,half=bottom]")
        for x in (26, 27):
            if i:
                v.fill(x, 2, -15 - i, x, y - 1, -15 - i, M)
            v.set(x, y, -15 - i, f"{STAIR_IN}[facing=north,half=bottom]")
    v.fill(-27, 9, 19, -26, 9, 21, "air")
    v.fill(26, 9, -21, 27, 9, -19, "air")
    for x in range(-20, 25, 6):                                         # lamps under the galleries
        v.set(x, 8, 18, "lantern[hanging=true]"); v.set(x, 8, -18, "lantern[hanging=true]")
    for z in range(-20, 13, 8):                                       # (the ramp takes z 15..22)
        v.set(-26, 8, z, "lantern[hanging=true]")
    # mosaic panels on the gallery walls (the Deesis and its pair)
    for z in (-23, 23):
        for x in range(2, 9):
            for y in range(11, 16):
                v.set(x, y, z, _hs_gold(x, y, z))

    # ---- apse with its conch, the mihrab and the minbar
    _hs_opening(v, "z", 29, 30, 2, 0, 4, 10, STAIR_OUT)
    _hs_half_cylinder(v, 30, 1, 0, 6, 12, _hs_brick)
    _hs_shell(v, 30, 12, 0, 6, L, y_min=12, x_sign=1)
    _hs_half_cylinder(v, 30, 2, 0, 5, 10, "air")
    _hs_shell(v, 30, 12, 0, 5, "air", hollow=False, y_min=12, x_sign=1)
    _hs_half_cylinder(v, 30, 1, 0, 5, 1, M)
    _hs_shell(v, 30, 12, 0, 5, _hs_gold, y_min=14, x_sign=1)
    for z in (-2, 2):
        v.fill(34, 2, z, 34, 6, z, _HS_CAPITAL)
    v.fill(34, 7, -2, 34, 7, 2, "gold_block")
    v.set(34, 6, 1, f"{STAIR_IN}[facing=south,half=top]")
    v.set(34, 6, -1, f"{STAIR_IN}[facing=north,half=top]")
    v.fill(35, 7, -1, 35, 7, 1, "gold_block")
    v.set(35, 6, 0, "lantern[hanging=true]")
    v.fill(31, 2, -2, 34, 2, 2, "red_carpet")
    for i, x in enumerate((23, 24, 25)):                                # minbar steps
        if i:
            v.fill(x, 2, 5, x, 1 + i, 7, M)
        v.fill(x, 2 + i, 5, x, 2 + i, 7, f"{STAIR_IN}[facing=east,half=bottom]")
        v.set(x, 3 + i, 4, "quartz_slab[type=bottom]"); v.set(x, 3 + i, 8, "quartz_slab[type=bottom]")
    v.fill(26, 2, 5, 26, 4, 7, M)
    v.fill(26, 5, 5, 26, 5, 7, "quartz_slab[type=bottom]")
    v.fill(26, 6, 5, 26, 8, 5, _HS_COLUMN); v.fill(26, 6, 7, 26, 8, 7, _HS_COLUMN)
    v.fill(25, 9, 4, 27, 9, 8, M)
    v.fill(26, 10, 5, 26, 10, 7, "gold_block"); v.set(26, 11, 6, "gold_block")

    # ---- buttresses: four heavy ones on the long sides, two at the west front
    for bx in (-14, 14):
        for z1, z2, z3 in ((25, 29, 27), (-29, -25, -27)):
            _hs_brick_box(v, bx - 2, 1, z1, bx + 2, 18, z2)
            _hs_brick_box(v, bx - 2, 19, min(z1, z3), bx + 2, 22, max(z1, z3))
            v.fill(bx - 2, 23, min(z1, z3), bx + 2, 23, max(z1, z3), "polished_andesite_slab[type=bottom]")
    for z1, z2 in ((17, 20), (-20, -17)):
        _hs_brick_box(v, -35, 1, z1, -31, 16, z2)
        _hs_brick_box(v, -33, 17, z1, -31, 20, z2)
        v.fill(-33, 21, z1, -31, 21, z2, "polished_andesite_slab[type=bottom]")

    # ---- domes: shells first (half domes, exedrae, drum, main dome), then the carves
    for sx in (-20, 20):
        v.dome(sx, 18, 0, 10, L)
    exedrae = ((-21, -14), (21, -14), (-21, 14), (21, 14))
    for sx, sz in exedrae:
        v.dome(sx, 18, sz, 5, L)
    drum = _hs_ring(0, 0, 17)
    for y in range(19, 23):
        for x, z in drum:
            v.set(x, y, z, _hs_brick(x, y, z))
    v.dome(0, 23, 0, 17, L)
    for x, z in drum:
        v.set(x, 23, z, "gray_concrete")                                # lead skirt
    v.fill(0, 41, 0, 0, 42, 0, "gold_block")
    v.sphere(0, 23, 0, 16, "air", hollow=False, y_min=19)
    v.disc(0, 18, 0, 16, "air")
    for sx in (-20, 20):
        v.sphere(sx, 18, 0, 9, "air", hollow=False, y_min=19)
        v.disc(sx, 18, 0, 9, "air")
    for sx, sz in exedrae:
        v.sphere(sx, 18, sz, 4, "air", hollow=False, y_min=19)
        v.disc(sx, 18, sz, 4, "air")
    # the ring of 40 windows in the drum, five at the foot of each half dome
    for i in range(40):
        x, z = drum[(i * len(drum)) // 40]
        v.set(x, 20, z, "glass_pane"); v.set(x, 21, z, "glass_pane")
    for sx in (-20, 20):
        for a in (-54, -27, 0, 27, 54):
            x = sx + (1 if sx > 0 else -1) * round(10 * math.cos(math.radians(a)))
            z = round(10 * math.sin(math.radians(a)))
            for y in (19, 20):
                if 9.5 <= math.sqrt((x - sx) ** 2 + (y - 18) ** 2 + z * z) <= 10.5:
                    v.set(x, y, z, "glass_pane")
    # gold mosaics lining the vaults
    _hs_shell(v, 0, 23, 0, 16, _hs_gold, y_min=36)
    for sx in (-20, 20):
        _hs_shell(v, sx, 18, 0, 9, _hs_gold, y_min=23)

    # ---- chandeliers hanging low on chains
    _hs_chandelier(v, 0, 0, 9, 6, lambda x, z: 23 + int(math.sqrt(max(0.0, 272.25 - x * x - z * z))), 12)
    for sx in (-20, 20):
        _hs_chandelier(v, sx, 0, 4, 6,
                       lambda x, z, sx=sx: 18 + int(math.sqrt(max(0.0, 90.25 - (x - sx) ** 2 - z * z))), 4)

    # ---- the four minarets
    for mx, mz in ((-34, -28), (34, -28), (-34, 28), (34, 28)):
        _hs_minaret(v, mx, mz, 46)

    # ---- courtyard to the south: walls, paths, ablution fountain, cypresses, lamps
    for x in (-30, 30):
        for z in range(25, 54):
            for y in range(1, 5):
                v.set(x, y, z, _hs_brick(x, y, z))
        v.fill(x, 5, 25, x, 5, 53, "polished_andesite_slab[type=bottom]")
        _hs_opening(v, "z", x, x, 1, 40, 1, 3, STAIR_OUT)
    for x in range(-30, 31):
        for y in range(1, 5):
            v.set(x, y, 53, _hs_brick(x, y, 53))
    v.fill(-30, 5, 53, 30, 5, 53, "polished_andesite_slab[type=bottom]")
    _hs_brick_box(v, -4, 1, 52, 4, 8, 54)                               # gatehouse
    v.fill(-4, 9, 52, 4, 9, 54, T)
    v.dome(0, 9, 53, 3, L)
    _hs_opening(v, "x", 52, 54, 1, 0, 1, 5, STAIR_OUT)
    v.fill(-2, 0, 25, 2, 0, 57, "stone_bricks")
    v.fill(-29, 0, 38, 29, 0, 42, "stone_bricks")
    v.disc(0, 0, 40, 7, "stone_bricks")
    v.disc(0, 1, 40, 4, "smooth_quartz", hollow=True)
    v.disc(0, 1, 40, 3, "water")
    v.column(0, 1, 40, 3, _HS_COLUMN)
    v.set(0, 4, 40, "water")
    for k in range(8):
        a = math.radians(45 * k + 22.5)
        v.fill(round(5.5 * math.cos(a)), 1, round(40 + 5.5 * math.sin(a)),
               round(5.5 * math.cos(a)), 5, round(40 + 5.5 * math.sin(a)), _HS_COLUMN)
    v.disc(0, 6, 40, 6, L)
    v.cone(0, 7, 40, 6, 5, L)
    for x in (-24, -18, -10, 10, 18, 24):
        _hs_cypress(v, x, 30); _hs_cypress(v, x, 48)
    for x, z in ((-4, 27), (4, 27), (-4, 50), (4, 50), (-8, 36), (8, 36), (-8, 44), (8, 44),
                 (-22, 37), (22, 37), (-22, 43), (22, 43)):
        _hs_lamp(v, x, z)

    # ---- Fountain of Ahmed III: a marble kiosk with corner sebils and a wide lead roof
    v.fill(-6, 1, 60, 6, 1, 72, M2)
    v.fill(-5, 1, 61, 5, 6, 71, "quartz_block")
    v.walls(-5, 4, 61, 5, 4, 71, "light_blue_terracotta")
    v.walls(-5, 6, 61, 5, 6, 71, "gold_block")
    for sx, sz in ((-5, 61), (5, 61), (-5, 71), (5, 71)):
        v.cylinder(sx, 1, sz, 2, 6, "quartz_block")
        v.fill(sx + (2 if sx > 0 else -2), 2, sz, sx + (2 if sx > 0 else -2), 3, sz, "iron_bars")
        v.fill(sx, 2, sz + (2 if sz > 66 else -2), sx, 3, sz + (2 if sz > 66 else -2), "iron_bars")
        v.sphere(sx, 8, sz, 1.5, L, hollow=False, y_min=8)
    for x, z, px, pz in ((6, 66, 5, 66), (-6, 66, -5, 66), (0, 60, 0, 61), (0, 72, 0, 71)):
        v.set(x, 1, z, "water_cauldron[level=3]")
        v.fill(px, 2, pz, px, 3, pz, "blue_glazed_terracotta")
    v.fill(-8, 7, 58, 8, 7, 74, L)
    v.fill(-6, 8, 60, 6, 8, 72, L)
    v.dome(0, 8, 66, 3, L)
    v.set(0, 12, 66, "gold_block")
    v.fill(-9, 0, 57, 9, 0, 75, "stone_bricks")
    v.fill(-2, 0, 76, 2, 0, 80, "stone_bricks")
    for x in (-12, 12):
        _hs_cypress(v, x, 60); _hs_cypress(v, x, 72)
    for x, z in ((-10, 66), (10, 66), (-3, 56), (3, 56)):
        _hs_lamp(v, x, z)
    for x in range(-24, 25, 8):                                         # a row behind the apse end
        _hs_cypress(v, x, -32)

    # ---- the Ottoman neighbourhood flanking the forecourt
    S.city_block(v, -58, 40, P, cols=2, rows=2, lot=9, street=3, floors=(2, 3), roof="hip", seed=40)
    S.city_block(v, 34, 40, P, cols=2, rows=2, lot=9, street=3, floors=(2, 3), roof="hip", seed=43)


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
