"""Renaissance Italy - Assassin's Creed II (2009) and Brotherhood (2010), 1476-1507."""

import math

from .. import structures as S
from ..palettes import ROME, TUSCANY, VENICE
from ..registry import Build, World
from ..voxel import Voxel


# ---------------------------------------------------------------- Florence helpers

_FL_WHITE = "white_concrete"
_FL_GREEN = "green_terracotta"
_FL_PINK = "pink_terracotta"
_FL_RIB = "smooth_quartz"


def _fl_oct_d(dx: float, dz: float) -> float:
    """Octagon 'radius' metric (apothem) of a point."""
    return max(abs(dx), abs(dz), (abs(dx) + abs(dz)) / math.sqrt(2))


def _fl_oct_ring(v: Voxel, cx: int, cz: int, y: int, r_out: float, r_in: float, pick) -> None:
    """One layer of an octagonal ring between ``r_in`` and ``r_out``.

    ``pick(angle_deg, d, x, z)`` returns the block for a cell (``d`` is its
    octagon radius, ``x``/``z`` its absolute position) or None to skip it."""
    lim = int(r_out + 2)
    for dx in range(-lim, lim + 1):
        for dz in range(-lim, lim + 1):
            d = _fl_oct_d(dx, dz)
            if r_in - 0.5 < d <= r_out + 0.5:
                ang = math.degrees(math.atan2(dz, dx)) % 360
                b = pick(ang, d, cx + dx, cz + dz)
                if b:
                    v.set(cx + dx, y, cz + dz, b)


def _fl_near_vertex(ang: float, r: float, width: float = 1.1) -> bool:
    """True when a cell at angle ``ang`` lies on an octagon corner rib."""
    delta = (ang - 22.5) % 45
    delta = min(delta, 45 - delta)
    return math.radians(delta) * r < width


def _fl_near_face(ang: float) -> float:
    """Angular distance (deg) to the nearest octagon face centre."""
    delta = ang % 45
    return min(delta, 45 - delta)


def _fl_banded(y: int, base: str = _FL_WHITE, band: str = _FL_GREEN) -> str:
    return band if y % 4 == 0 else base


def _fl_stair_gable(v: Voxel, x1: int, z1: int, x2: int, z2: int, y: int,
                    stair: str, block: str, slab: str, ridge: str = "z") -> int:
    """Pitched roof drawn with stairs; the ridge runs along ``ridge``.  Returns top y."""
    if ridge == "z":
        a, b = x1, x2
        while a < b:
            v.fill(a, y, z1, a, y, z2, f"{stair}[facing=east,half=bottom]")
            v.fill(b, y, z1, b, y, z2, f"{stair}[facing=west,half=bottom]")
            if a + 1 < b - 1:
                v.fill(a + 1, y, z1, b - 1, y, z2, block)
            a += 1; b -= 1; y += 1
        if a == b:
            v.fill(a, y, z1, a, y, z2, slab)
            return y
        return y - 1
    a, b = z1, z2
    while a < b:
        v.fill(x1, y, a, x2, y, a, f"{stair}[facing=south,half=bottom]")
        v.fill(x1, y, b, x2, y, b, f"{stair}[facing=north,half=bottom]")
        if a + 1 < b - 1:
            v.fill(x1, y, a + 1, x2, y, b - 1, block)
        a += 1; b -= 1; y += 1
    if a == b:
        v.fill(x1, y, a, x2, y, a, slab)
        return y
    return y - 1


def _fl_lamp(v: Voxel, x: int, z: int, y: int = 1, h: int = 3) -> None:
    v.column(x, y, z, h, "oak_fence")
    v.set(x, y + h, z, "lantern[hanging=false]")


def _fl_paired_window(v: Voxel, x: int, y: int, z: int, axis: str, h: int = 4,
                      fill: str = "air") -> None:
    """Two arched lights with a central colonnette, cut into a wall at (x, z).

    ``axis`` is the direction the wall runs.  ``h`` is the opening height."""
    for k in (-2, -1, 1, 2):
        px, pz = (x + k, z) if axis == "x" else (x, z + k)
        v.fill(px, y, pz, px, y + h - 1, pz, fill)
    mx, mz = x, z
    v.fill(mx, y, mz, mx, y + h - 1, mz, "quartz_pillar")
    # arch heads: upside-down stairs leaning on the mullion / jambs
    if axis == "x":
        v.set(x - 2, y + h - 1, z, "quartz_stairs[facing=east,half=top]")
        v.set(x - 1, y + h - 1, z, "quartz_stairs[facing=west,half=top]")
        v.set(x + 1, y + h - 1, z, "quartz_stairs[facing=east,half=top]")
        v.set(x + 2, y + h - 1, z, "quartz_stairs[facing=west,half=top]")
    else:
        v.set(x, y + h - 1, z - 2, "quartz_stairs[facing=south,half=top]")
        v.set(x, y + h - 1, z - 1, "quartz_stairs[facing=north,half=top]")
        v.set(x, y + h - 1, z + 1, "quartz_stairs[facing=south,half=top]")
        v.set(x, y + h - 1, z + 2, "quartz_stairs[facing=north,half=top]")


def _fl_corbel_ring(v: Voxel, x1: int, z1: int, x2: int, z2: int, y: int,
                    stair: str, slab: str) -> None:
    """Row of corbels one block outside the rectangle x1..x2 / z1..z2 at height y."""
    for x in range(x1, x2 + 1):
        n = f"{stair}[facing=south,half=top]" if x % 2 == 0 else f"{slab}[type=top]"
        s = f"{stair}[facing=north,half=top]" if x % 2 == 0 else f"{slab}[type=top]"
        v.set(x, y, z1 - 1, n)
        v.set(x, y, z2 + 1, s)
    for z in range(z1, z2 + 1):
        w = f"{stair}[facing=east,half=top]" if z % 2 == 0 else f"{slab}[type=top]"
        e = f"{stair}[facing=west,half=top]" if z % 2 == 0 else f"{slab}[type=top]"
        v.set(x1 - 1, y, z, w)
        v.set(x2 + 1, y, z, e)
    for (x, z) in ((x1 - 1, z1 - 1), (x2 + 1, z1 - 1), (x1 - 1, z2 + 1), (x2 + 1, z2 + 1)):
        v.set(x, y, z, f"{slab}[type=top]")


def _fl_ramp_z(v: Voxel, x1: int, x2: int, z: int, direction: int, y_top: int,
               stair: str, block: str) -> None:
    """Stairs from ground (y=0 top) up to a deck whose surface block is at ``y_top``.

    The ramp ends at ``z`` (the deck edge) and runs ``direction`` (-1 north / +1 south)
    away from it."""
    facing = "south" if direction < 0 else "north"      # rises toward the deck
    for k in range(y_top):
        zz = z + direction * (y_top - k)
        if k > 0:
            v.fill(x1, 1, zz, x2, k, zz, block)
        v.fill(x1, k + 1, zz, x2, k + 1, zz, f"{stair}[facing={facing},half=bottom]")


def _fl_duomo(v: Voxel, P) -> None:
    """Santa Maria del Fiore: banded marble nave, octagonal crossing, ribbed dome."""
    W, G, K, RIB = _FL_WHITE, _FL_GREEN, _FL_PINK, _FL_RIB
    cx, cz, R = 0, 0, 13                 # crossing centre and octagon radius
    zf, zn, za = -64, -11, -6            # facade / end of nave walls / end of aisles
    floor_a, floor_b = "polished_diorite", "polished_andesite"
    inside = lambda x, z: _fl_oct_d(x - cx, z - cz) < R - 0.5
    # --- nave shell: aisle walls (x +-13, y 1..9) and nave walls (x +-7, y 1..19)
    for y in range(1, 10):
        b = _fl_banded(y)
        v.fill(-13, y, zf, -13, y, za, b); v.fill(13, y, zf, 13, y, za, b)
    for y in range(1, 20):
        b = _fl_banded(y)
        v.fill(-7, y, zf, -7, y, zn, b); v.fill(7, y, zf, 7, y, zn, b)
    for z in range(zf, za + 1, 5):                           # green pilasters on the aisles
        v.fill(-13, 1, z, -13, 9, z, G); v.fill(13, 1, z, 13, 9, z, G)
    for z in range(zf + 2, za - 2, 5):                       # aisle windows and pink panels
        for x in (-13, 13):
            v.fill(x, 5, z, x, 7, z + 1, "glass")
            v.fill(x, 2, z, x, 3, z + 1, K)
    # arcade between nave and aisles: 10 bays of round arches on grey piers
    for z in range(zf, -14, 5):
        for x in (-7, 7):
            v.carve(x, 1, z + 1, x, 9, z + 4)
            v.arch(x, 1, z, 6, 9, 1, W, axis="z")
            v.fill(x, 1, z, x, 9, z, floor_a)
    for z in range(zf + 2, -14, 5):                          # clerestory
        for x in (-7, 7):
            v.fill(x, 14, z, x, 16, z + 1, "glass")
    # floors: grey aisles, chequered nave, a pink marble carpet down the middle
    v.fill(-12, 1, zf + 1, 12, 1, za, floor_b)
    for z in range(zf + 1, -12):
        for x in range(-6, 7):
            if (x + z) % 2 == 0:
                v.set(x, 1, z, floor_a)
    v.fill(0, 1, zf + 1, 0, 1, -13, K)
    # aisle roofs (lean-to in brick stairs) and the nave gable in red tile
    for side in (1, -1):
        face = "west" if side > 0 else "east"
        for k, x in enumerate((13, 11, 9)):
            v.fill(side * x, 10 + k, zf, side * x, 10 + k, za, f"brick_stairs[facing={face},half=bottom]")
            v.fill(side * (x - 1), 10 + k, zf, side * (x - 1), 10 + k, za, "terracotta")
    v.gable_roof(-7, 20, zf, 7, zn, "terracotta", ridge_axis="z", overhang=1)
    for z in range(zf + 4, -14, 10):                         # lanterns for the night
        for x in (-10, 10):
            v.set(x, 9, z, "lantern[hanging=true]")
        v.set(0, 19, z, "lantern[hanging=true]")
    # --- facade (north end): marble screen, three portals, rose window, gable
    v.fill(-13, 1, zf, 13, 19, zf, W)
    for y in range(20, 29):
        half = int(round(13 * (28 - y) / 9.0))
        v.fill(-half, y, zf, half, y, zf, W)
    for y in (4, 8, 12, 16, 20):
        v.fill(-13, y, zf, 13, y, zf, G)
    for x in (-13, -7, 7, 13):
        v.fill(x, 1, zf, x, 19, zf, G)
    for x in (-12, -10, 9, 11):
        v.fill(x, 13, zf, x + 1, 15, zf, K)
        v.fill(x, 5, zf, x + 1, 7, zf, K)
    v.fill(-6, 13, zf, 6, 13, zf, G)
    v.fill(-6, 17, zf, -5, 19, zf, K); v.fill(5, 17, zf, 6, 19, zf, K)
    v.carve(-3, 1, zf, 3, 9, zf); v.arch(-3, 1, zf, 7, 9, 1, W, axis="x")      # central portal
    v.carve(-12, 1, zf, -8, 6, zf); v.arch(-12, 1, zf, 5, 6, 1, W, axis="x")  # side portals
    v.carve(8, 1, zf, 12, 6, zf); v.arch(8, 1, zf, 5, 6, 1, W, axis="x")
    for x in (-11, 9):                                        # round heads on the side portals
        v.set(x, 6, zf, "quartz_stairs[facing=east,half=top]"); v.set(x + 2, 6, zf, "quartz_stairs[facing=west,half=top]")
    v.set(-4, 10, zf, "quartz_stairs[facing=east,half=bottom]")
    v.set(4, 10, zf, "quartz_stairs[facing=west,half=bottom]")
    v.fill(-3, 10, zf, 3, 10, zf, "quartz_slab[type=bottom]")
    for dx in range(-3, 4):                                  # rose window
        for dy in range(-3, 4):
            d2 = dx * dx + dy * dy
            if d2 <= 5:
                v.set(dx, 23 + dy, zf, "glass")
            elif d2 <= 11:
                v.set(dx, 23 + dy, zf, G)
    v.set(0, 29, zf, "quartz_block")
    # --- three tribune apses around the crossing (east, west, south)
    for ax, az in ((19, 0), (-19, 0), (0, 19)):
        ox, oz = cx + ax, cz + az
        for y in range(1, 12):
            _fl_oct_ring(v, ox, oz, y, 6, 6,
                         lambda a, d, x, z, y=y: None if inside(x, z) else
                         (G if _fl_near_vertex(a, 6, 0.8) else _fl_banded(y)))
        _fl_oct_ring(v, ox, oz, 1, 5, 0, lambda a, d, x, z: None if inside(x, z) else floor_b)
        for y in (4, 5, 6):
            _fl_oct_ring(v, ox, oz, y, 6, 6,
                         lambda a, d, x, z: None if inside(x, z) or _fl_near_face(a) > 2.5 else "glass")
        for k in range(7):                                   # half-dome in red tiles
            r = 6.5 * math.sqrt(max(0.0, 1 - (k / 6.5) ** 2))
            _fl_oct_ring(v, ox, oz, 12 + k, r, max(r - 1, 0),
                         lambda a, d, x, z, r=r: None if inside(x, z) else
                         (RIB if _fl_near_vertex(a, max(r, 1), 0.9) else "terracotta"))
        v.set(ox, 18, oz, RIB)
    # --- crossing walls: banded marble octagon, green corner pilasters
    for y in range(1, 20):
        _fl_oct_ring(v, cx, cz, y, R, R,
                     lambda a, d, x, z, y=y: G if _fl_near_vertex(a, R, 1.0) else _fl_banded(y))
    for x in range(-12, 13):                                 # nave / aisle roofs must not poke inside
        for z in range(-13, -5):
            if inside(x, z):
                v.carve(x, 10, z, x, 28, z)
    v.carve(-6, 1, cz - R - 1, 6, 12, cz - R + 1)            # arch from the nave
    v.carve(cx + 12, 1, cz - 4, cx + 14, 8, cz + 4)          # into the three apses
    v.carve(cx - 14, 1, cz - 4, cx - 12, 8, cz + 4)
    v.carve(cx - 4, 1, cz + 12, cx + 4, 8, cz + 14)
    v.carve(8, 1, -10, 11, 5, -8); v.carve(-11, 1, -10, -8, 5, -8)   # aisle doors
    for y in range(14, 18):                                  # tall windows in every face
        _fl_oct_ring(v, cx, cz, y, R, R, lambda a, d, x, z: "glass" if _fl_near_face(a) < 4 else None)
    # crossing floor: concentric octagons of grey / pink / green marble
    for d in range(0, R):
        ring_b = (floor_a, K, floor_b, G)[d % 4] if d > 3 else floor_a
        _fl_oct_ring(v, cx, cz, 1, d, d, lambda a, dd, x, z, b=ring_b: b)
    # high altar on a two-step platform
    for k, r in enumerate((5, 4)):
        _fl_oct_ring(v, cx, cz, 2 + k, r, 0, lambda a, d, x, z: "polished_diorite")
    v.fill(cx - 1, 4, cz, cx + 1, 4, cz, "quartz_block")
    v.fill(cx - 2, 5, cz, cx + 2, 5, cz, "quartz_slab[type=bottom]")
    v.set(cx - 2, 6, cz, "lantern[hanging=false]"); v.set(cx + 2, 6, cz, "lantern[hanging=false]")
    v.set(cx, 6, cz, "gold_block")
    # --- drum (y 20..25): white marble, green pilasters, eight round windows
    for y in range(20, 26):
        def drum(a, d, x, z, y=y):
            if _fl_near_vertex(a, R, 1.0):
                return G
            if abs(y - 22.5) + math.radians(_fl_near_face(a)) * R <= 2.1:
                return "glass"
            return G if y in (20, 25) else W
        _fl_oct_ring(v, cx, cz, y, R, R, drum)
    # --- the dome: pointed octagonal shell, red tile panels, eight white ribs
    y0, H, RD = 26, 17, 13.0
    radii = [RD * math.sqrt(max(0.0, 1 - (k / H) ** 2)) for k in range(H + 1)]
    for k in range(H):
        r_k = radii[k]
        _fl_oct_ring(v, cx, cz, y0 + k, r_k, min(r_k, radii[k + 1]),
                     lambda a, d, x, z, r=r_k: RIB if _fl_near_vertex(a, max(r, 1.0), 1.0) else "terracotta")
    v.fill(cx - 2, y0 + H - 1, cz - 2, cx + 2, y0 + H - 1, cz + 2, RIB)
    # lantern: eight marble piers, open arches, a small cone and a gilded ball
    ly = y0 + H                                              # 43
    for y in range(ly, ly + 6):
        _fl_oct_ring(v, cx, cz, y, 3, 3,
                     lambda a, d, x, z, y=y: RIB if (_fl_near_vertex(a, 3, 1.2) or y > ly + 3) else None)
    v.fill(cx - 3, ly + 6, cz - 3, cx + 3, ly + 6, cz + 3, "quartz_slab[type=bottom]")
    v.cone(cx, ly + 7, cz, 2.5, 3, RIB)
    v.set(cx, ly + 10, cz, "gold_block")                     # y 53
    v.set(cx, ly + 2, cz, "lantern[hanging=false]")


def _fl_campanile(v: Voxel, tx: int, tz: int) -> None:
    """Giotto's bell tower: 7x7, 44 high, banded marble, paired arched windows, terrace."""
    W, G, K = _FL_WHITE, _FL_GREEN, _FL_PINK
    top = 44
    for y in range(1, top + 1):
        v.walls(tx - 3, y, tz - 3, tx + 3, y, tz + 3, _fl_banded(y))
    for (dx, dz) in ((-3, -3), (3, -3), (-3, 3), (3, 3)):      # green corner pilasters
        v.fill(tx + dx, 1, tz + dz, tx + dx, top, tz + dz, G)
    v.fill(tx - 2, 1, tz - 2, tx + 2, top, tz + 2, "air")
    v.fill(tx - 2, 1, tz - 2, tx + 2, 1, tz + 2, "polished_andesite")
    for y in (2, 3, 6, 7):                                     # lozenge panels on the base
        for s in (-3, 3):
            v.set(tx - 1, y, tz + s, K); v.set(tx + 1, y, tz + s, K)
            v.set(tx + s, y, tz - 1, K); v.set(tx + s, y, tz + 1, K)
    for y in (10, 11):
        v.walls(tx - 3, y, tz - 3, tx + 3, y, tz + 3, K)
    for y0 in (14, 22):                                        # two storeys of paired windows
        for s in (-3, 3):
            _fl_paired_window(v, tx, y0, tz + s, "x", h=5)
            _fl_paired_window(v, tx + s, y0, tz, "z", h=5)
        v.walls(tx - 3, y0 + 6, tz - 3, tx + 3, y0 + 6, tz + 3, K)
    for s in (-3, 3):                                          # tall triple-light top storey
        v.fill(tx - 1, 31, tz + s, tx + 1, 39, tz + s, "air")
        v.fill(tx + s, 31, tz - 1, tx + s, 39, tz + 1, "air")
        v.set(tx, 39, tz + s, "quartz_slab[type=top]"); v.set(tx + s, 39, tz, "quartz_slab[type=top]")
        v.fill(tx - 1, 35, tz + s, tx + 1, 35, tz + s, "quartz_slab[type=bottom]")
        v.fill(tx + s, 35, tz - 1, tx + s, 35, tz + 1, "quartz_slab[type=bottom]")
    for y in (14, 22, 31):                                     # floors behind the windows
        v.fill(tx - 2, y - 1, tz - 2, tx + 2, y - 1, tz + 2, "oak_planks")
    v.fill(tx + 2, 1, tz + 2, tx + 2, top - 1, tz + 2, "ladder[facing=north]")
    v.set(tx, 20, tz, "bell[attachment=ceiling]")
    v.set(tx, 38, tz, "bell[attachment=ceiling]")
    # projecting cornice on corbels, terrace floor and a balustrade
    _fl_corbel_ring(v, tx - 3, tz - 3, tx + 3, tz + 3, top, "quartz_stairs", "quartz_slab")
    v.fill(tx - 4, top + 1, tz - 4, tx + 4, top + 1, tz + 4, W)
    v.walls(tx - 4, top + 2, tz - 4, tx + 4, top + 2, tz + 4, "quartz_slab[type=bottom]")
    for (dx, dz) in ((-4, -4), (4, -4), (-4, 4), (4, 4)):
        v.set(tx + dx, top + 2, tz + dz, G)
        v.set(tx + dx, top + 3, tz + dz, "lantern[hanging=false]")


def _fl_palazzo_vecchio(v: Voxel, px: int, pz: int) -> None:
    """Rusticated block 31 x 25 with corbelled gallery, courtyard and the Arnolfo tower."""
    x2, z2 = px + 30, pz + 24
    H = 20
    rust = ("stone_bricks", "cobblestone", "andesite", "stone_bricks", "cobblestone")
    for y in range(1, H + 1):                                  # staggered rusticated courses
        for i, x in enumerate(range(px, x2 + 1, 3)):
            b = rust[(i + y) % 5]
            v.fill(x, y, pz, min(x + 2, x2), y, pz, b); v.fill(x, y, z2, min(x + 2, x2), y, z2, b)
        for i, z in enumerate(range(pz, z2 + 1, 3)):
            b = rust[(i + y + 2) % 5]
            v.fill(px, y, z, px, y, min(z + 2, z2), b); v.fill(x2, y, z, x2, y, min(z + 2, z2), b)
    v.fill(px + 1, 1, pz + 1, x2 - 1, H, z2 - 1, "air")
    v.fill(px + 1, 1, pz + 1, x2 - 1, 1, z2 - 1, "stone")
    for y in (5, 11, 16):                                      # paired windows under round arches
        for x in range(px + 3, x2 - 2, 5):
            if y > 5 or x < px + 10 or x > px + 20:
                _fl_paired_window(v, x, y, pz, "x", h=3, fill="glass_pane")
                _fl_paired_window(v, x, y, z2, "x", h=3, fill="glass_pane")
        for z in range(pz + 3, z2 - 2, 5):
            if y > 5:
                _fl_paired_window(v, px, y, z, "z", h=3, fill="glass_pane")
                _fl_paired_window(v, x2, y, z, "z", h=3, fill="glass_pane")
    # interior: two floors around an arcaded courtyard (Michelozzo's cortile)
    cx1, cz1, cx2, cz2 = px + 10, pz + 7, px + 20, pz + 17
    for y in (8, 15):
        v.fill(px + 1, y, pz + 1, x2 - 1, y, z2 - 1, "oak_planks")
    v.carve(cx1, 2, cz1, cx2, H, cz2)                           # courtyard open to the sky
    v.fill(cx1, 1, cz1, cx2, 1, cz2, "polished_andesite")
    for x in (cx1, cx2):
        for z in range(cz1, cz2, 5):
            v.carve(x, 1, z + 1, x, 6, z + 4)
            v.arch(x, 1, z, 6, 7, 1, "smooth_stone", axis="z")
            v.fill(x, 1, z, x, 6, z, "polished_andesite")
    for z in (cz1, cz2):
        for x in range(cx1, cx2, 5):
            v.carve(x + 1, 1, z, x + 4, 6, z)
            v.arch(x, 1, z, 6, 7, 1, "smooth_stone", axis="x")
            v.fill(x, 1, z, x, 6, z, "polished_andesite")
    v.walls(cx1, 8, cz1, cx2, 14, cz2, "smooth_stone")          # upper courtyard walls
    v.walls(cx1, 15, cz1, cx2, H, cz2, "smooth_stone")
    for y in (10, 17):
        v.windows(cx1, y, cz1, cx2, cz2, "glass_pane", period=2, offset=1)
    v.carve(cx1 + 1, 2, cz1 + 1, cx2 - 1, H + 1, cz2 - 1)      # clear floors above the courtyard
    v.fill(cx1 + 1, 1, cz1 + 1, cx2 - 1, 1, cz2 - 1, "polished_andesite")
    fx, fz = (cx1 + cx2) // 2, (cz1 + cz2) // 2                 # putto fountain
    v.disc(fx, 1, fz, 2, "polished_diorite", hollow=True); v.disc(fx, 1, fz, 1, "water")
    v.column(fx, 1, fz, 2, "polished_diorite"); v.set(fx, 3, fz, "copper_block"); v.set(fx, 4, fz, "water")
    for (lx, lz) in ((cx1 + 1, cz1 + 1), (cx2 - 1, cz1 + 1), (cx1 + 1, cz2 - 1), (cx2 - 1, cz2 - 1)):
        v.set(lx, 6, lz, "lantern[hanging=true]")
    # main door (west face, onto the piazza) and stairs up inside
    v.carve(px, 1, pz + 12, px, 5, pz + 14); v.arch(px, 1, pz + 11, 5, 6, 1, "stone_bricks", axis="z")
    v.set(px, 5, pz + 12, "stone_brick_stairs[facing=south,half=top]")
    v.set(px, 5, pz + 14, "stone_brick_stairs[facing=north,half=top]")
    v.set(px - 1, 6, pz + 11, "lantern[hanging=false]"); v.set(px - 1, 6, pz + 15, "lantern[hanging=false]")
    v.fill(px - 1, 5, pz + 11, px - 1, 5, pz + 15, "stone_brick_slab[type=top]")
    for k in range(7):
        v.fill(px + 2 + k, 1 + k, z2 - 2, px + 2 + k, 1 + k, z2 - 2, "stone_brick_stairs[facing=east,half=bottom]")
        v.fill(px + 2 + k, 1, z2 - 2, px + 2 + k, k, z2 - 2, "stone_bricks")
    v.carve(px + 1, 8, z2 - 3, px + 9, 8, z2 - 2)
    v.carve(px + 1, 15, z2 - 3, px + 9, 15, z2 - 2)
    for k in range(7):
        v.fill(px + 2 + k, 8 + k, z2 - 3, px + 2 + k, 8 + k, z2 - 3, "stone_brick_stairs[facing=east,half=bottom]")
        v.fill(px + 2 + k, 8, z2 - 3, px + 2 + k, 7 + k, z2 - 3, "stone_bricks")
    # roof, corbelled gallery with Guelph crenellation
    v.fill(px + 1, H, pz + 1, x2 - 1, H, z2 - 1, "stone")
    _fl_corbel_ring(v, px, pz, x2, z2, H, "stone_brick_stairs", "stone_brick_slab")
    v.walls(px - 1, H + 1, pz - 1, x2 + 1, H + 2, z2 + 1, "stone_bricks")
    v.windows(px - 1, H + 2, pz - 1, x2 + 1, z2 + 1, "air", period=2, offset=1)   # gallery loopholes
    v.crenellate(px - 1, H + 3, pz - 1, x2 + 1, z2 + 1, "stone_bricks", period=2)
    v.fill(px, H + 1, pz, x2, H + 1, z2, "stone_brick_slab[type=bottom]")          # gallery walkway
    v.fill(px + 2, H + 2, pz + 2, x2 - 2, H + 2, z2 - 2, "terracotta")              # low tiled roof
    v.fill(px + 4, H + 3, pz + 4, x2 - 4, H + 3, z2 - 4, "terracotta")
    v.carve(cx1, H + 1, cz1, cx2, H + 3, cz2)
    v.carve(cx1 + 1, H, cz1 + 1, cx2 - 1, H, cz2 - 1)              # courtyard open to the sky
    v.walls(cx1, H + 1, cz1, cx2, H + 1, cz2, "stone_brick_wall")
    v.fill(x2 - 2, 16, z2 - 1, x2 - 2, H, z2 - 1, "ladder[facing=north]")   # top floor -> gallery
    v.carve(x2 - 2, H + 1, z2 - 1, x2 - 2, H + 1, z2 - 1)
    # Torre di Arnolfo: off-centre on the west front, rising through the gallery
    tx1, tz1, tx2, tz2 = px, pz + 2, px + 6, pz + 8
    TH = 42
    for y in range(1, TH + 1):
        v.walls(tx1, y, tz1, tx2, y, tz2, rust[(y // 2) % 2 * 2])
    v.fill(tx1 + 1, 1, tz1 + 1, tx2 - 1, TH, tz2 - 1, "air")
    v.fill(tx1 + 1, 1, tz1 + 1, tx2 - 1, 1, tz2 - 1, "stone")
    v.fill(tx1 + 3, 1, tz2 - 1, tx1 + 3, TH - 1, tz2 - 1, "ladder[facing=north]")
    v.carve(tx2, 2, tz1 + 3, tx2, 3, tz1 + 3)                   # door from the palace floor
    for y in (12, 20, 28):
        for x in (tx1 + 2, tx1 + 4):
            v.set(x, y, tz1, "glass_pane"); v.set(x, y + 1, tz1, "glass_pane")
        v.fill(tx1 - 1, y - 1, tz1 - 1, tx1 - 1, y - 1, tz2 + 1, "stone_brick_slab[type=top]")
    for dy in range(-2, 3):                                      # the clock on the west face
        for dz in range(-2, 3):
            if abs(dy) + abs(dz) < 4:
                b = "white_concrete"
                if (dz == 0 and dy >= 0) or (dy == 0 and dz > 0):
                    b = "black_concrete"
                v.set(tx1, 34 + dy, tz1 + 3 + dz, b)
    v.fill(tx1 - 1, 31, tz1 + 1, tx1 - 1, 31, tz1 + 5, "stone_brick_slab[type=top]")
    _fl_corbel_ring(v, tx1, tz1, tx2, tz2, TH, "stone_brick_stairs", "stone_brick_slab")
    v.fill(tx1 - 1, TH + 1, tz1 - 1, tx2 + 1, TH + 1, tz2 + 1, "stone_bricks")
    v.walls(tx1 - 1, TH + 2, tz1 - 1, tx2 + 1, TH + 2, tz2 + 1, "stone_bricks")
    v.crenellate(tx1 - 1, TH + 3, tz1 - 1, tx2 + 1, tz2 + 1, "stone_bricks", period=2)
    # belfry: four piers, open arches, pyramid cap and a gilded lion weathervane
    bx1, bz1, bx2, bz2 = tx1 + 1, tz1 + 1, tx2 - 1, tz2 - 1
    for (x, z) in ((bx1, bz1), (bx2, bz1), (bx1, bz2), (bx2, bz2)):
        v.fill(x, TH + 2, z, x, TH + 8, z, "stone_bricks")
    v.walls(bx1, TH + 8, bz1, bx2, TH + 9, bz2, "stone_bricks")
    for (x, z) in ((bx1 + 1, bz1), (bx2 - 1, bz1), (bx1 + 1, bz2), (bx2 - 1, bz2)):
        v.set(x, TH + 7, z, "stone_brick_stairs[facing=%s,half=top]" % ("east" if x == bx1 + 1 else "west"))
    for (x, z) in ((bx1, bz1 + 1), (bx1, bz2 - 1), (bx2, bz1 + 1), (bx2, bz2 - 1)):
        v.set(x, TH + 7, z, "stone_brick_stairs[facing=%s,half=top]" % ("south" if z == bz1 + 1 else "north"))
    v.set((bx1 + bx2) // 2, TH + 6, (bz1 + bz2) // 2, "bell[attachment=ceiling]")
    v.fill(bx1, TH + 7, bz1, bx2, TH + 7, bz2, "stone_bricks")
    v.carve(bx1 + 1, TH + 7, bz1 + 1, bx2 - 1, TH + 7, bz2 - 1)
    v.fill(bx1, TH + 10, bz1, bx2, TH + 10, bz2, "stone_brick_slab[type=bottom]")
    v.pyramid((bx1 + bx2) // 2, TH + 10, (bz1 + bz2) // 2, 5, 3, "terracotta")
    v.set((bx1 + bx2) // 2, TH + 13, (bz1 + bz2) // 2, "gold_block")    # y 55
    v.set((bx1 + bx2) // 2, TH + 14, (bz1 + bz2) // 2, "gold_block")


def _fl_piazza(v: Voxel, x1: int, z1: int, x2: int, z2: int, px: int, pz: int) -> None:
    """Piazza della Signoria: Loggia dei Lanzi, Neptune fountain, David, lamp posts."""
    S.pad(v, x1, z1, x2, z2, "polished_andesite")
    for x in range(x1, x2 + 1, 6):                               # paving pattern
        v.fill(x, 0, z1, x, 0, z2, "stone_bricks")
    for z in range(z1, z2 + 1, 6):
        v.fill(x1, 0, z, x2, 0, z, "stone_bricks")
    # Neptune fountain
    fx, fz = x1 + 12, z1 + 7
    v.disc(fx, 1, fz, 5, "polished_diorite", hollow=True)
    v.disc(fx, 2, fz, 5, "quartz_slab[type=bottom]", hollow=True)
    v.disc(fx, 1, fz, 4, "water")
    v.disc(fx, 2, fz, 2, "polished_diorite"); v.disc(fx, 3, fz, 1, "polished_diorite")
    v.column(fx, 4, fz, 3, "quartz_block"); v.fill(fx - 1, 6, fz, fx + 1, 6, fz, "quartz_block")
    v.set(fx, 7, fz, "quartz_block"); v.set(fx + 1, 7, fz, "quartz_block"); v.set(fx + 1, 8, fz, "quartz_block")
    for (dx, dz) in ((3, 3), (-3, 3), (3, -3), (-3, -3)):
        v.set(fx + dx, 2, fz + dz, "copper_block"); v.set(fx + dx, 3, fz + dz, "water")
    # David on his pedestal beside the palace door
    dx_, dz_ = px - 3, pz + 9
    v.fill(dx_ - 1, 1, dz_ - 1, dx_ + 1, 3, dz_ + 1, "stone_bricks")
    v.fill(dx_ - 1, 4, dz_ - 1, dx_ + 1, 4, dz_ + 1, "quartz_slab[type=bottom]")
    v.column(dx_, 5, dz_, 3, "quartz_block"); v.column(dx_, 5, dz_ + 1, 2, "quartz_block")
    v.fill(dx_ - 1, 8, dz_, dx_ + 1, 9, dz_ + 1, "quartz_block")
    v.set(dx_ - 1, 10, dz_ + 1, "quartz_block"); v.set(dx_, 10, dz_, "quartz_block"); v.set(dx_, 11, dz_, "quartz_block")
    v.set(dx_ + 1, 10, dz_, "quartz_block")
    # Loggia dei Lanzi: three round arches onto the square, terrace on top
    lx1, lz1, lx2, lz2 = x2 - 15, z2 + 2, x2, z2 + 9
    v.fill(lx1, 1, lz1, lx2, 9, lz2, "smooth_sandstone")
    v.fill(lx1 + 1, 1, lz1 + 1, lx2 - 1, 8, lz2 - 1, "air")
    v.fill(lx1 + 1, 1, lz1 + 1, lx2 - 1, 1, lz2 - 1, "polished_andesite")
    for k in range(3):
        x = lx1 + k * 5
        v.carve(x + 1, 1, lz1, x + 4, 8, lz1)
        v.arch(x, 1, lz1, 6, 9, 1, "smooth_sandstone", axis="x")
    v.carve(lx1, 1, lz1 + 1, lx1, 8, lz2 - 1); v.arch(lx1, 1, lz1, 8, 9, 1, "smooth_sandstone", axis="z")
    v.walls(lx1, 10, lz1, lx2, 10, lz2, "sandstone_wall")
    v.fill(lx1 - 1, 9, lz1 - 1, lx2 + 1, 9, lz1 - 1, "sandstone_slab[type=top]")
    for (sx, blk) in ((lx1 + 3, "oxidized_copper"), (lx2 - 3, "quartz_block")):   # Perseus / Sabines
        v.fill(sx - 1, 1, lz2 - 2, sx + 1, 2, lz2 - 2, "polished_andesite")
        v.fill(sx - 1, 1, lz2 - 3, sx + 1, 2, lz2 - 1, "polished_andesite")
        v.column(sx, 3, lz2 - 2, 4, blk); v.set(sx, 7, lz2 - 2, blk)
        v.set(sx + 1, 6, lz2 - 2, blk); v.set(sx - 1, 5, lz2 - 2, blk)
    for x in range(lx1 + 2, lx2, 5):
        v.set(x, 8, lz1 + 3, "lantern[hanging=true]")
    # lamp posts around the square
    for x in range(x1 + 3, x2, 8):
        _fl_lamp(v, x, z1 + 1); _fl_lamp(v, x, z2 - 1)
    for z in range(z1 + 7, z2, 8):
        _fl_lamp(v, x1 + 1, z)


def _fl_ponte_vecchio(v: Voxel, bx: int, zr1: int, zr2: int) -> None:
    """The Arno with quays, the three-arch bridge, its shops and the Vasari corridor."""
    P = TUSCANY
    stair, blk, slab = "brick_stairs", "terracotta", "brick_slab[type=bottom]"
    shop_w = "smooth_sandstone"
    # river bed, water and stone quays
    v.fill(-80, -3, zr1, 90, -1, zr2, "gravel")
    v.fill(-80, 0, zr1, 90, 0, zr2, "water")
    v.fill(-80, 0, zr1 - 1, 90, 0, zr1 - 1, "stone_bricks"); v.fill(-80, 0, zr2 + 1, 90, 0, zr2 + 1, "stone_bricks")
    v.fill(-80, 1, zr1 - 1, 90, 1, zr1 - 1, "stone_brick_wall"); v.fill(-80, 1, zr2 + 1, 90, 1, zr2 + 1, "stone_brick_wall")
    v.fill(-80, -3, zr1, 90, -1, zr1, "stone_bricks"); v.fill(-80, -3, zr2, 90, -1, zr2, "stone_bricks")
    # three segmental arches of span 11; piers in the water; deck at y 4
    x1, x2 = bx - 8, bx + 7                                      # 16 wide
    z1 = zr1 - 4
    L = 31
    for a in range(3):
        v.arch(x1, 1, z1 + a * 10, 11, 4, 16, "stone_bricks", axis="z")
    v.fill(x1, 4, z1, x2, 4, z1 + L - 1, "stone")
    v.fill(bx - 2, 4, z1, bx + 1, 4, z1 + L - 1, "cobblestone")  # the roadway
    v.carve(x1, 1, zr1 - 1, x2, 1, zr1 - 1); v.carve(x1, 1, zr2 + 1, x2, 1, zr2 + 1)
    for z in (z1 + 10, z1 + 20):                                 # cutwaters
        v.fill(x1 - 1, 0, z - 1, x1 - 1, 3, z + 1, "stone_bricks"); v.fill(x2 + 1, 0, z - 1, x2 + 1, 3, z + 1, "stone_bricks")
    _fl_ramp_z(v, bx - 2, bx + 1, z1, -1, 4, "stone_brick_stairs", "stone_bricks")
    _fl_ramp_z(v, bx - 2, bx + 1, z1 + L - 1, 1, 4, "stone_brick_stairs", "stone_bricks")
    # the goldsmiths' shops: west row (gable roofs) and east row (under the corridor)
    for k in range(6):
        za = z1 + 1 + k * 5
        zb = za + 3
        for (sx1, sx2, side) in ((bx - 8, bx - 3, -1), (bx + 2, bx + 7, 1)):
            v.fill(sx1, 5, za, sx2, 8, zb, shop_w)
            v.fill(sx1 + 1, 5, za + 1, sx2 - 1, 7, zb - 1, "air")
            v.fill(sx1, 8, za, sx2, 8, zb, "oak_planks")         # ceiling
            v.set(sx1 + 1 if side < 0 else sx2 - 1, 7, za + 2, "lantern[hanging=true]")
            rx = sx2 if side < 0 else sx1                        # the road-side wall
            v.carve(rx, 5, za + 1, rx, 6, za + 1)                 # door
            v.set(rx, 6, zb - 1, "glass_pane")
            face_out = "east" if side < 0 else "west"
            v.set(rx + (1 if side < 0 else -1), 6, zb, f"oak_trapdoor[facing={face_out},half=top,open=true]")
            v.set(rx + (1 if side < 0 else -1), 6, zb - 2, f"oak_trapdoor[facing={face_out},half=top,open=true]")
            v.set(rx + (1 if side < 0 else -1), 7, za + 1, f"wall_torch[facing={face_out}]")
            ox = sx1 if side < 0 else sx2                        # the river-side wall, overhanging
            v.set(ox, 6, za + 2, "glass_pane")
            v.set(ox + side, 4, za + 1, f"oak_stairs[facing={'east' if side < 0 else 'west'},half=top]")
            v.set(ox + side, 4, zb - 1, f"oak_stairs[facing={'east' if side < 0 else 'west'},half=top]")
            v.fill(ox + side, 5, za, ox + side, 8, zb, "oak_planks")
            v.fill(ox + side, 6, za + 1, ox + side, 6, zb - 1, "glass_pane")
            if side < 0:
                _fl_stair_gable(v, sx1 - 1, za, sx2, zb, 9, stair, blk, slab, ridge="z")
    # Vasari corridor along the east shops, continuing north on arches toward the Uffizi
    cx1, cx2 = bx + 2, bx + 8
    za, zb = z1 - 17, z1 + L + 4                                   # north end wall / south end
    for k in range(4):                                            # arches on the north bank
        v.arch(cx1, 1, z1 - 4 - k * 4, 5, 8, 7, "smooth_sandstone", axis="z")
    v.fill(cx1, 9, za, cx2, 12, zb, "smooth_sandstone")
    v.fill(cx1 + 1, 10, za + 1, cx2 - 1, 12, zb, "air")
    v.fill(cx1 + 1, 9, za + 1, cx2 - 1, 9, zb, "oak_planks")       # corridor floor
    v.fill(cx1, 13, za - 1, cx2, 13, zb + 1, "terracotta")
    v.fill(cx1 + 1, 14, za - 1, cx2 - 1, 14, zb + 1, "brick_slab[type=bottom]")
    for z in range(za + 2, zb, 3):
        v.set(cx1, 11, z, "glass_pane"); v.set(cx2, 11, z, "glass_pane")
    for z in range(za + 3, zb, 8):
        v.set(cx1 + 3, 12, z, "lantern[hanging=true]")
    v.fill(cx1, 1, zb - 3, cx2, 8, zb, "smooth_sandstone")         # south-bank stair tower
    v.fill(cx1 + 1, 1, zb - 2, cx2 - 1, 12, zb - 1, "air")
    v.fill(cx1 + 3, 1, zb - 1, cx1 + 3, 8, zb - 1, "ladder[facing=north]")
    v.carve(cx1 + 2, 1, zb, cx1 + 4, 3, zb)
    # a few boats on the Arno
    for (gx, gz) in ((bx - 30, zr1 + 5), (bx + 25, zr2 - 6), (bx - 45, zr2 - 4)):
        v.fill(gx, 0, gz, gx + 6, 0, gz + 1, "spruce_planks")
        v.set(gx - 1, 1, gz, "spruce_planks"); v.set(gx + 7, 1, gz + 1, "spruce_planks")


def florence(v: Voxel) -> None:
    """Santa Maria del Fiore with Brunelleschi's dome, Giotto's campanile,
    the Palazzo Vecchio and the Ponte Vecchio over the Arno."""
    P = TUSCANY
    S.pad(v, -80, -70, 90, 96, "stone")
    # Piazza del Duomo paving and the cathedral (nave runs north-south, facade at the north)
    S.pad(v, -24, -70, 26, 26, "polished_andesite")
    _fl_duomo(v, P)
    _fl_campanile(v, -18, -61)
    for (lx, lz) in ((-8, -68), (8, -68), (-22, -50), (22, -40), (22, -20), (-22, -30), (-10, 24), (10, 24)):
        _fl_lamp(v, lx, lz)
    for (tx_, tz_) in ((-22, 12), (22, 12)):
        v.tree(tx_, 1, tz_, P["log"], P["leaves"], height=5)
    # Palazzo Vecchio and the Piazza della Signoria in front of it
    px, pz = 40, 10
    _fl_palazzo_vecchio(v, px, pz)
    _fl_piazza(v, 0, pz, px - 2, pz + 24, px, pz)
    S.road(v, px - 2, 0, px + 30, 9, "cobblestone")
    # the Arno (z 58..80) with the Ponte Vecchio and the Vasari corridor
    _fl_ponte_vecchio(v, -2, 58, 80)
    for x in range(-70, 86, 12):
        _fl_lamp(v, x, 56); _fl_lamp(v, x, 82)
    # Florentine streets around the monuments, and the Oltrarno across the river
    S.city_block(v, -78, -30, TUSCANY, cols=3, rows=3, lot=10, street=4, floors=(2, 3), roof="gable", seed=12)
    S.city_block(v, 45, -65, TUSCANY, cols=3, rows=3, lot=10, street=4, floors=(2, 3), roof="gable", seed=13)
    S.city_block(v, 45, -21, TUSCANY, cols=3, rows=2, lot=10, street=4, floors=(2, 3), roof="gable", seed=14)
    S.city_block(v, -78, 16, TUSCANY, cols=3, rows=2, lot=10, street=4, floors=(2, 3), roof="gable", seed=15)
    S.city_block(v, 14, 44, TUSCANY, cols=2, rows=1, lot=9, street=3, floors=(2, 3), roof="gable", seed=16)
    for i, hx in enumerate(range(-72, 80, 15)):
        if -16 <= hx <= 10:
            continue                                               # keep the bridgehead clear
        S.house(v, hx, 86, 10, 9, TUSCANY, floors=2 + i % 2, roof="gable",
                wall=("smooth_sandstone", "white_terracotta")[i % 2], ridge="xz"[i % 2])
    S.pad(v, -80, 83, 90, 85, "cobblestone")                     # Lungarno on the south bank
    S.pad(v, -80, 52, 90, 55, "cobblestone")                     # and on the north bank


def monteriggioni(v: Voxel) -> None:
    """Ezio's hill town: ring wall with 14 towers, the Villa Auditore, the market square."""
    P = TUSCANY
    S.pad(v, -60, -60, 60, 60, "grass_block")
    for k in range(6):
        v.disc(0, 1 + k, 0, 52 - k * 2, "coarse_dirt" if k % 2 else "grass_block")
    y0 = 7
    town = Voxel()
    town.cylinder(0, 1, 0, 40, 8, "stone_bricks", hollow=True)
    town.cylinder(0, 1, 0, 39, 8, "stone_bricks", hollow=True)
    town.disc(0, 1, 0, 38, "cobblestone")
    for a in range(0, 360, 26):                                            # 14 towers
        tx = round(40 * math.cos(math.radians(a)))
        tz = round(40 * math.sin(math.radians(a)))
        S.tower(town, tx, tz, 3, 13, TUSCANY, top="crenel", square=True, wall="stone_bricks")
    town.fill(-2, 1, 38, 2, 5, 40, "air")                                  # Porta Romana
    # Villa Auditore at the top of the main street
    S.house(town, -12, -34, 25, 16, TUSCANY, floors=3, roof="hip", wall="smooth_sandstone")
    town.fill(-14, 1, -18, 14, 1, -16, "stone_bricks")
    S.plaza(town, -14, -14, 14, 10, TUSCANY, fountain=True)
    for (hx, hz) in ((-34, -10), (-34, 6), (18, -10), (18, 6), (-30, 18), (14, 18)):
        S.house(town, hx, hz, 12, 10, TUSCANY, floors=2, roof="gable", wall="white_terracotta" if hx < 0 else "smooth_sandstone")
    v.merge(town, 0, y0 - 1, 0)
    for k in range(8):
        v.fill(-2, 1 + k, 58 - k * 2, 2, 1 + k, 59 - k * 2, "cobblestone")
    for i in range(10):
        v.tree(-55 + i * 11, 1, 56, "dark_oak_log", "dark_oak_leaves[persistent=true]", height=5)


def venice(v: Voxel) -> None:
    """Piazza San Marco, the campanile, the Doge's Palace, the Rialto and a canal."""
    P = VENICE
    S.pad(v, -80, -60, 80, 70, "stone")
    v.fill(-80, -3, 40, 80, 0, 70, "water")                                # the lagoon / Grand Canal
    v.fill(-80, -3, -10, -60, 0, 40, "water")
    v.fill(-80, 0, 38, 80, 0, 39, "stone_bricks")
    # Doge's Palace: pink diamond pattern over a double arcade
    px, pz = 0, 10
    v.fill(px, 1, pz, px + 50, 6, pz + 26, P["column"])
    v.fill(px + 1, 1, pz + 1, px + 49, 6, pz + 25, "air")
    for x in range(px, px + 51, 3):
        v.column(x, 1, pz + 26, 6, "quartz_pillar")
        v.column(x, 1, pz, 6, "quartz_pillar")
    for y in range(7, 20):
        for x in range(px, px + 51):
            for zz in (pz, pz + 26):
                v.set(x, y, zz, "pink_terracotta" if (x + y) % 4 < 2 else "white_terracotta")
        v.fill(px, y, pz + 1, px, y, pz + 25, "white_terracotta")
        v.fill(px + 50, y, pz + 1, px + 50, y, pz + 25, "white_terracotta")
    v.windows(px, 12, pz, px + 50, pz + 26, P["window"], period=5, offset=3)
    v.fill(px, 20, pz, px + 50, 20, pz + 26, "white_terracotta")
    v.crenellate(px, 21, pz, px + 50, pz + 26, "quartz_block", period=2)
    v.fill(px + 1, 1, pz + 1, px + 49, 1, pz + 25, P["floor"])
    # St Mark's basilica: five domes
    bx, bz = -60, 0
    v.fill(bx, 1, bz, bx + 40, 14, bz + 36, "white_terracotta")
    v.fill(bx + 1, 1, bz + 1, bx + 39, 13, bz + 35, "air")
    v.fill(bx + 1, 1, bz + 1, bx + 39, 1, bz + 35, "polished_diorite")
    for dx, dz in ((20, 18), (8, 18), (32, 18), (20, 6), (20, 30)):
        v.cylinder(bx + dx, 15, bz + dz, 6, 3, "light_gray_terracotta", hollow=True)
        v.dome(bx + dx, 17, bz + dz, 6, "gray_concrete")
        v.set(bx + dx, 24, bz + dz, "gold_block")
    for x in range(bx + 4, bx + 40, 8):
        v.fill(x - 2, 1, bz + 36, x + 2, 6, bz + 36, "air")
    v.fill(bx + 10, 15, bz + 32, bx + 30, 15, bz + 36, "gold_block")      # the four horses' terrace
    # campanile
    S.tower(v, -14, 2, 4, 55, VENICE, top="pyramid", square=True, wall="bricks")
    v.fill(-18, 50, -2, -10, 55, 6, "white_terracotta")
    v.fill(-17, 50, -1, -11, 54, 5, "air")
    v.set(-14, 66, 2, "gold_block")
    S.pad(v, -58, 0, 0, 38, "polished_diorite")                            # Piazza San Marco
    # Rialto bridge over the canal, with its arcade of shops
    S.arched_bridge(v, 20, 40, 30, 9, VENICE, arches=1, axis="z", deck_y=7, shops=False)
    for z in range(42, 66, 6):
        v.fill(21, 9, z, 22, 11, z + 3, "white_terracotta")
        v.fill(26, 9, z, 27, 11, z + 3, "white_terracotta")
        v.fill(20, 12, z - 1, 28, 12, z + 4, "terracotta")
    # gondolas
    for i, gx in enumerate((-40, -20, 50)):
        v.fill(gx, 0, 50 + i * 4, gx + 8, 0, 50 + i * 4, "black_concrete")
        v.set(gx - 1, 1, 50 + i * 4, "black_concrete"); v.set(gx + 9, 1, 50 + i * 4, "black_concrete")
    S.city_block(v, 54, -56, VENICE, cols=2, rows=3, lot=9, street=3, floors=(3, 4), roof="flat", seed=21)
    S.city_block(v, -78, -56, VENICE, cols=2, rows=3, lot=9, street=3, floors=(3, 4), roof="flat", seed=22)


def rome(v: Voxel) -> None:
    """Brotherhood's Rome: the Colosseum, the Pantheon, Castel Sant'Angelo and the Tiber."""
    S.pad(v, -120, -100, 120, 110, "grass_block")
    S.colosseum(v, -55, 30, ROME, rx=44, rz=36, tiers=3, tier_h=8)
    S.pantheon(v, 50, -40, ROME, r=16)
    # Castel Sant'Angelo: drum on a square base, by the river
    v.fill(-120, -3, 80, 120, 0, 100, "water")
    cx, cz = 40, 50
    v.fill(cx - 22, 1, cz - 22, cx + 22, 6, cz + 22, "stone_bricks")
    v.cylinder(cx, 7, cz, 18, 14, "smooth_stone", hollow=False)
    v.cylinder(cx, 21, cz, 12, 8, "bricks", hollow=True)
    v.disc(cx, 29, cz, 12, "smooth_stone")
    S.statue(v, cx, cz, 9, "copper_block", y=30)                            # the archangel
    v.crenellate(cx - 22, 7, cz - 22, cx + 22, cz + 22, "stone_bricks")
    S.arched_bridge(v, cx - 4, 80, 20, 9, ROME, arches=3, axis="z", deck_y=4)
    # ruined Forum colonnade and the Via
    S.roman_road(v, -110, -70, 200)
    for x in range(-60, 20, 6):
        v.column(x, 1, -84, 6 + (x // 6) % 4, "quartz_pillar")
    S.ruined_wall(v, -60, -90, 70, seed=4)
    S.city_block(v, -115, -50, ROME, cols=3, rows=2, lot=10, street=4, floors=(2, 3), roof="gable", seed=31)


def san_gimignano(v: Voxel) -> None:
    """Town of towers: competing families built 70 of them, 14 survive."""
    P = TUSCANY
    S.pad(v, -50, -50, 50, 50, "cobblestone")
    S.curtain_wall(v, -46, -46, 46, 46, 7, TUSCANY, gate="south", tower_r=3)
    heights = (40, 34, 30, 36, 28, 26, 32, 22, 24, 30, 20, 26, 34, 28)
    pos = ((0, -5), (6, 2), (-8, 4), (14, -12), (-16, -10), (20, 10), (-22, 12), (8, 18),
           (-6, 22), (26, -24), (-26, -26), (30, 24), (-30, 26), (2, -28))
    for (x, z), h in zip(pos, heights):
        S.tower(v, x, z, 2.5, h, TUSCANY, top="flat", square=True, wall="stone_bricks")
        S.house(v, x - 6, z + 3, 8, 7, TUSCANY, floors=2, roof="gable")
    S.plaza(v, -8, -2, 4, 10, TUSCANY, fountain=True)


WORLD = World(
    id="italy",
    name="Renaissance Italy",
    game="Assassin's Creed II (2009) / Brotherhood (2010)",
    era="1476-1507",
    description="Ezio's Italy: Florence, Monteriggioni, San Gimignano, Venice and Rome.",
).build(Build("florence", "Florence", "Santa Maria del Fiore with Brunelleschi's ribbed dome, Giotto's campanile, Palazzo Vecchio, Piazza della Signoria and the Ponte Vecchio.", florence, "1 block = 2 m")
).build(Build("monteriggioni", "Monteriggioni", "The hill town's ring wall with fourteen towers, the Villa Auditore and the square.", monteriggioni)
).build(Build("venice", "Venice", "St Mark's five domes, the campanile, the Doge's Palace, the Rialto bridge, canals and gondolas.", venice)
).build(Build("rome", "Rome", "The Colosseum, the Pantheon with its oculus, Castel Sant'Angelo on the Tiber, a Roman road and Forum ruins.", rome, "1 block = 2 m")
).build(Build("san_gimignano", "San Gimignano", "Fourteen family towers inside the town wall.", san_gimignano))
